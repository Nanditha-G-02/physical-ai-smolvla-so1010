#!/usr/bin/env python3
"""Scan the repository for accidentally committed secrets and large files.

Looks for Hugging Face tokens, common API-key formats, private keys, .env
files, and files above a size limit. Matches are printed with the secret
masked. Run it before every commit.

Usage:
    python scripts/scan_secrets.py [repo_root] [--max-mb 5]

Exit code 1 if anything suspicious is found.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

PATTERNS = {
    "Hugging Face token": re.compile(r"\bhf_[A-Za-z0-9]{30,}\b"),
    "OpenAI-style key": re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    "Anthropic-style key": re.compile(r"\bsk-ant-[A-Za-z0-9_-]{20,}\b"),
    "GitHub token": re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}\b"),
    "AWS access key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "Private key block": re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    "Token assignment": re.compile(r"(?i)\b(hf_token|huggingface_token|api_key|secret_key|password)\s*[:=]\s*['\"][^'\"\s]{8,}['\"]"),
}
SKIP_DIRS = {".git", "__pycache__", ".venv", "venv", "node_modules"}
BLOCKED_NAMES = {".env", "credentials.json", "token", "hf_token"}
BLOCKED_SUFFIXES = {".pem", ".key", ".safetensors", ".pt", ".pth", ".ckpt", ".mp4", ".parquet"}


def mask(s: str) -> str:
    return s[:6] + "…" + s[-2:] if len(s) > 10 else "…"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("root", nargs="?", default=str(Path(__file__).resolve().parent.parent))
    ap.add_argument("--max-mb", type=float, default=5.0)
    args = ap.parse_args()
    root = Path(args.root)
    issues = 0

    for p in sorted(root.rglob("*")):
        if any(part in SKIP_DIRS for part in p.parts) or not p.is_file():
            continue
        rel = p.relative_to(root)
        if p.name in BLOCKED_NAMES or (p.name.startswith(".env") and p.name != ".env.example"):
            print(f"[BLOCKED FILE] {rel}")
            issues += 1
        if p.suffix.lower() in BLOCKED_SUFFIXES:
            print(f"[BLOCKED TYPE] {rel}")
            issues += 1
        size_mb = p.stat().st_size / 2**20
        if size_mb > args.max_mb:
            print(f"[LARGE FILE]   {rel} ({size_mb:.1f} MB)")
            issues += 1
        if p.name == "scan_secrets.py":
            continue  # this file contains the patterns themselves
        try:
            text = p.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for i, line in enumerate(text.splitlines(), 1):
            for label, rx in PATTERNS.items():
                for m in rx.finditer(line):
                    print(f"[{label}] {rel}:{i}: {mask(m.group(0))}")
                    issues += 1

    print(f"Secret scan finished: {issues} issue(s).")
    return 1 if issues else 0


if __name__ == "__main__":
    sys.exit(main())
