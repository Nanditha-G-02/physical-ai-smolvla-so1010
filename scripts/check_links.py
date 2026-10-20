#!/usr/bin/env python3
"""Check that every relative link in the repository's Markdown files resolves.

Checks file targets and, for Markdown targets, '#anchor' fragments using
GitHub's heading-slug rules. External (http/https/mailto) links are skipped.

Usage:
    python scripts/check_links.py [repo_root]

Exit code 1 if any link is broken.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
FENCE_RE = re.compile(r"^\s*(```|~~~)")


def github_slug(text: str) -> str:
    text = re.sub(r"<[^>]+>", "", text)            # strip HTML tags
    text = re.sub(r"`([^`]*)`", r"\1", text)       # inline code -> text
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)  # links -> text
    text = text.strip().lower()
    out = []
    for ch in text:
        if ch.isalnum() or ch in "-_":
            out.append(ch)
        elif ch == " ":
            out.append("-")
        # all other punctuation is dropped
    return "".join(out)


def anchors(path: Path) -> set[str]:
    found: set[str] = set()
    counts: dict[str, int] = {}
    in_fence = False
    for line in path.read_text(encoding="utf-8").splitlines():
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        m = HEADING_RE.match(line)
        if m:
            slug = github_slug(m.group(2))
            n = counts.get(slug, 0)
            found.add(slug if n == 0 else f"{slug}-{n}")
            counts[slug] = n + 1
    return found


def links(path: Path) -> list[tuple[int, str]]:
    result = []
    in_fence = False
    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        line = re.sub(r"`[^`]*`", "", line)   # ignore inline code
        for m in LINK_RE.finditer(line):
            result.append((i, m.group(1)))
    return result


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent)
    md_files = [p for p in root.rglob("*.md") if ".git" not in p.parts]
    cache: dict[Path, set[str]] = {}
    broken = 0
    checked = 0
    for md in sorted(md_files):
        for line_no, target in links(md):
            if re.match(r"^[a-z]+:", target) or target.startswith("//"):
                continue
            checked += 1
            path_part, _, frag = target.partition("#")
            dest = md if not path_part else (md.parent / path_part).resolve()
            if not dest.exists():
                print(f"{md.relative_to(root)}:{line_no}: missing target '{target}'")
                broken += 1
                continue
            if frag and dest.is_file() and dest.suffix == ".md":
                if dest not in cache:
                    cache[dest] = anchors(dest)
                if frag.lower() not in cache[dest]:
                    print(f"{md.relative_to(root)}:{line_no}: missing anchor '#{frag}' in {dest.relative_to(root)}")
                    broken += 1
    print(f"Checked {checked} relative links in {len(md_files)} Markdown files: {broken} broken.")
    return 1 if broken else 0


if __name__ == "__main__":
    sys.exit(main())
