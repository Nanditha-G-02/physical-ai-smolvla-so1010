#!/usr/bin/env python3
"""Check the host environment used for SmolVLA training and inference.

Mirrors the manual checks run on the project PC (Step 1 of the host workflow):
Python, PyTorch + CUDA, LeRobot version, SmolVLA import, CLI entry points,
GPU memory, and Hugging Face login. It never prints or reads token values.

Usage:
    conda activate lerobot
    python scripts/verify_environment.py [--min-free-gb 3]

Exit code is 0 if all required checks pass, 1 otherwise.
"""
from __future__ import annotations

import argparse
import importlib
import importlib.metadata as md
import shutil
import subprocess
import sys

OK, WARN, FAIL = "PASS", "WARN", "FAIL"
results: list[tuple[str, str, str]] = []


def record(name: str, status: str, detail: str) -> None:
    results.append((name, status, detail))


def run(cmd: list[str]) -> str | None:
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=30, check=True).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--min-free-gb", type=float, default=3.0,
                        help="GPU memory that should be free for training (default: 3 GB)")
    args = parser.parse_args()

    # Python
    v = sys.version_info
    record("Python", OK if v >= (3, 10) else WARN, f"{v.major}.{v.minor}.{v.micro} at {sys.executable}")

    # PyTorch / CUDA
    try:
        torch = importlib.import_module("torch")
        record("PyTorch", OK, torch.__version__)
        if torch.cuda.is_available():
            name = torch.cuda.get_device_name(0)
            free, total = torch.cuda.mem_get_info(0)
            free_gb, total_gb = free / 2**30, total / 2**30
            status = OK if free_gb >= args.min_free_gb else WARN
            record("CUDA", OK, f"{name}, CUDA {torch.version.cuda}")
            record("GPU memory", status, f"{free_gb:.1f} GB free of {total_gb:.1f} GB")
        else:
            record("CUDA", FAIL, "torch.cuda.is_available() is False")
    except ImportError:
        record("PyTorch", FAIL, "torch not importable")

    # LeRobot
    try:
        lr_version = md.version("lerobot")
        record("LeRobot", OK if lr_version == "0.6.2" else WARN,
               f"{lr_version} (project used 0.6.2 on the host)")
    except md.PackageNotFoundError:
        record("LeRobot", FAIL, "package 'lerobot' not installed in this environment")

    try:
        importlib.import_module("lerobot.policies.smolvla.modeling_smolvla")
        record("SmolVLA import", OK, "lerobot.policies.smolvla.modeling_smolvla")
    except Exception as exc:  # noqa: BLE001 - report any import problem
        record("SmolVLA import", FAIL, f"{type(exc).__name__}: {exc}")

    # CLI entry points
    for cli in ("lerobot-train", "lerobot-rollout"):
        path = shutil.which(cli)
        record(cli, OK if path else FAIL, path or "not on PATH")

    # Hugging Face login (never prints the token)
    hf = shutil.which("hf")
    if hf:
        out = run([hf, "auth", "whoami"])
        if out and "not logged" not in out.lower():
            user = next((line.split(":", 1)[1].strip() for line in out.splitlines() if "user" in line.lower()), "logged in")
            record("Hugging Face", OK, f"logged in as {user}")
        else:
            record("Hugging Face", WARN, "not logged in (run: hf auth login)")
    else:
        record("Hugging Face", WARN, "'hf' CLI not found (pip install -U huggingface_hub)")

    # Other GPU processes
    smi = shutil.which("nvidia-smi")
    if smi:
        procs = run([smi, "--query-compute-apps=pid,used_memory", "--format=csv,noheader"])
        record("Other GPU processes", OK if not procs else WARN, procs or "none")

    width = max(len(n) for n, _, _ in results)
    for name, status, detail in results:
        print(f"[{status}] {name.ljust(width)}  {detail}")

    failed = [n for n, s, _ in results if s == FAIL]
    print("\nAll required checks passed." if not failed else f"\nFailed: {', '.join(failed)}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
