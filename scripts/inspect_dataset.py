#!/usr/bin/env python3
"""Inspect a local LeRobot dataset (format v2.1 or v3.0) without importing LeRobot.

Reads meta/info.json and, when present, the task and episode metadata, then
prints a summary: format, totals, fps, features, cameras, episode-length
statistics, tasks, and simple consistency checks.

Usage:
    python scripts/inspect_dataset.py <dataset_root> [--json]

Example:
    python scripts/inspect_dataset.py \
        ~/.cache/huggingface/lerobot/NandithaaaG/s101_dataset_pick_and_place

Only the Python standard library is required. Episode lengths for v3.0
(stored in Parquet) are read if pyarrow is installed.
"""
from __future__ import annotations

import argparse
import json
import statistics
import sys
from pathlib import Path


def load_jsonl(path: Path) -> list[dict]:
    rows = []
    with path.open() as fh:
        for line in fh:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def episode_lengths(root: Path, version: str) -> list[int]:
    if version.startswith("v2"):
        p = root / "meta" / "episodes.jsonl"
        if p.exists():
            return [int(r["length"]) for r in load_jsonl(p) if "length" in r]
        return []
    ep_dir = root / "meta" / "episodes"
    if ep_dir.is_dir():
        try:
            import pyarrow.parquet as pq  # type: ignore
        except ImportError:
            return []
        lengths: list[int] = []
        for f in sorted(ep_dir.rglob("*.parquet")):
            table = pq.read_table(f, columns=["length"])
            lengths.extend(int(x) for x in table.column("length").to_pylist())
        return lengths
    return []


def tasks(root: Path) -> list[str]:
    jl = root / "meta" / "tasks.jsonl"
    if jl.exists():
        return [r.get("task", "") for r in load_jsonl(jl)]
    pq_path = root / "meta" / "tasks.parquet"
    if pq_path.exists():
        try:
            import pyarrow.parquet as pq  # type: ignore
            t = pq.read_table(pq_path).to_pandas()
            return [str(i) for i in t.index]
        except Exception:  # noqa: BLE001
            return ["<tasks.parquet present; install pyarrow and pandas to read>"]
    return []


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("root", type=Path, help="dataset root containing meta/info.json")
    ap.add_argument("--json", action="store_true", help="print the summary as JSON")
    args = ap.parse_args()

    root = args.root.expanduser()
    info_path = root / "meta" / "info.json"
    if not info_path.exists():
        print(f"error: {info_path} not found", file=sys.stderr)
        return 2
    info = json.loads(info_path.read_text())

    version = str(info.get("codebase_version", "unknown"))
    feats = info.get("features", {})
    cameras = {k: v for k, v in feats.items() if v.get("dtype") in ("video", "image")}
    vectors = {k: v for k, v in feats.items() if k not in cameras}
    lengths = episode_lengths(root, version)
    task_list = tasks(root)
    fps = info.get("fps")

    checks = []
    if lengths:
        checks.append(("episode count matches", len(lengths) == info.get("total_episodes")))
        checks.append(("frame count matches", sum(lengths) == info.get("total_frames")))
    if cameras and info.get("total_videos") is not None and info.get("total_episodes"):
        checks.append(("videos = episodes x cameras",
                       info["total_videos"] == info["total_episodes"] * len(cameras)))
    if "observation.state" in feats and "action" in feats:
        checks.append(("state/action dims equal",
                       feats["observation.state"].get("shape") == feats["action"].get("shape")))

    summary = {
        "root": str(root),
        "format": version,
        "robot_type": info.get("robot_type"),
        "total_episodes": info.get("total_episodes"),
        "total_frames": info.get("total_frames"),
        "fps": fps,
        "total_tasks": info.get("total_tasks"),
        "cameras": {k: v.get("shape") for k, v in cameras.items()},
        "vectors": {k: {"shape": v.get("shape"), "names": v.get("names")} for k, v in vectors.items()},
        "episode_length_frames": (
            {"min": min(lengths), "mean": round(statistics.mean(lengths), 1), "max": max(lengths)}
            if lengths else None
        ),
        "tasks": task_list,
        "checks": {name: ok for name, ok in checks},
    }

    if args.json:
        print(json.dumps(summary, indent=2))
        return 0

    print(f"Dataset:   {root}")
    print(f"Format:    {version}   robot_type: {summary['robot_type']}")
    print(f"Episodes:  {summary['total_episodes']}   frames: {summary['total_frames']}   fps: {fps}")
    if fps and summary["total_frames"]:
        print(f"Duration:  {summary['total_frames'] / fps / 60:.1f} min total")
    if lengths and fps:
        e = summary["episode_length_frames"]
        print(f"Episode length: min {e['min']}  mean {e['mean']}  max {e['max']} frames "
              f"({e['mean'] / fps:.1f} s mean)")
    print("Cameras:")
    for k, shape in summary["cameras"].items():
        print(f"  {k:32s} {shape}")
    print("Vectors:")
    for k, v in summary["vectors"].items():
        names = v["names"] if isinstance(v["names"], list) else ""
        print(f"  {k:32s} {v['shape']} {names}")
    if task_list:
        print("Tasks:")
        for t in task_list:
            print(f"  - {t}")
    if checks:
        print("Checks:")
        for name, ok in checks:
            print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    if version.startswith("v2"):
        print("\nNote: v2.1 format. LeRobot >= 0.4 needs v3.0; see tutorials/05-inspect-and-convert-dataset.md.")
    return 0 if all(ok for _, ok in checks) else 1


if __name__ == "__main__":
    sys.exit(main())
