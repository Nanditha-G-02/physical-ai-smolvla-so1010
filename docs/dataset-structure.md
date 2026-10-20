# Dataset Structure and Hugging Face Dataset

## Contents
- [Repository](#repository)
- [Verified metadata](#verified-metadata)
- [Features](#features)
- [On-disk layout: v2.1](#on-disk-layout-v21)
- [v2.1 vs v3.0](#v21-vs-v30)
- [Downloading and inspecting](#downloading-and-inspecting)
- [Loading in Python](#loading-in-python)
- [Converting to v3.0 safely](#converting-to-v30-safely)
- [Dataset quality](#dataset-quality)
- [Limitations](#limitations)

## Repository

| | |
|---|---|
| Hub URL | https://huggingface.co/datasets/NandithaaaG/s101_dataset_pick_and_place |
| Accessibility | ✅ Public (checked 20 Oct 2026) |
| Licence | Apache-2.0 |
| Created with | ROBOTIS Physical AI Tools + LeRobot (per the auto-generated dataset card) |
| Tags | `robotis`, `LeRobot`, `s101_dataset` |
| Purpose | Fine-tuning SmolVLA for single-task pick-and-place on the SO-ARM101 |

## Verified metadata

From `meta/info.json` (Hub copy, and the fresh local download on 19 Oct):

| Field | Value |
|-------|-------|
| `codebase_version` | `v2.1` |
| `robot_type` | `s101_dataset` |
| `total_episodes` | 39 |
| `total_frames` | 23,424 |
| `total_tasks` | 1 |
| `total_videos` | 78 (39 episodes × 2 cameras) |
| `total_chunks` / `chunks_size` | 1 / 1000 |
| `fps` | 30 |
| `splits` | `train: 0:39` (no held-out split) |
| Size | 458 MB on the Hub; 438 MB on disk after download |

Derived: mean episode length ≈ 600.6 frames ≈ **20.0 s**; total ≈ **13.0 min** of demonstration.

## Features

| Key | dtype | Shape | Notes |
|-----|-------|-------|-------|
| `observation.images.global` | video | 720×1280×3 | Femto Bolt; libx264, yuv420p |
| `observation.images.gripper` | video | 480×640×3 | Gripper camera; libx264, yuv420p |
| `observation.state` | float32 | 6 | Follower measured joints: `shoulder_pan, shoulder_lift, elbow_flex, wrist_flex, wrist_roll, gripper` |
| `action` | float32 | 6 | Leader commanded joints, same names and order |
| `timestamp` | float32 | 1 | Seconds since episode start |
| `frame_index` | int64 | 1 | Index within episode |
| `episode_index` | int64 | 1 | 0–38 |
| `index` | int64 | 1 | Global frame index |
| `task_index` | int64 | 1 | Always 0 (single task) |

**Units.** Joint values are stored in the units produced by the recording pipeline. The joint names carry no `.pos` suffix (unlike native LeRobot SO-101 datasets such as `grab_place_training`), and the unit convention (degrees, normalized range, or raw ticks) is **not verified**. Check it before mixing this dataset with any other SO-101 data.

## On-disk layout: v2.1

```text
s101_dataset_pick_and_place/
├── meta/
│   ├── info.json             # schema, fps, path templates
│   ├── episodes.jsonl        # per-episode length and task
│   ├── episodes_stats.jsonl  # per-episode statistics
│   └── tasks.jsonl           # task index -> instruction text
├── data/chunk-000/
│   └── episode_000000.parquet … episode_000038.parquet
└── videos/chunk-000/
    ├── observation.images.global/episode_000000.mp4 …
    └── observation.images.gripper/episode_000000.mp4 …
```

Path templates (verified): `data/chunk-{episode_chunk:03d}/episode_{episode_index:06d}.parquet` and `videos/chunk-{episode_chunk:03d}/{video_key}/episode_{episode_index:06d}.mp4`. The names of the `meta/*.jsonl` files follow the v2.1 convention and were not individually listed in the project history.

## v2.1 vs v3.0

| | v2.1 (Hub, container) | v3.0 (host, LeRobot ≥ 0.4) |
|---|---|---|
| Files | One parquet and one MP4 per episode per camera | Many episodes concatenated into larger parquet / MP4 shards |
| Episode boundaries | Implied by file names | Stored as offsets in `meta/episodes/` (chunked parquet) |
| Streaming from Hub | Limited | Native (`StreamingLeRobotDataset`) |
| Reader | Older LeRobot (Physical AI Tools) | LeRobot 0.6.2 |

Source: [LeRobotDataset v3.0 documentation](https://huggingface.co/docs/lerobot/lerobot-dataset-v3).

## Downloading and inspecting

Verified commands:

```bash
# [HOST]
D=~/.cache/huggingface/lerobot/NandithaaaG/s101_dataset_pick_and_place
mkdir -p ~/dataset_backups
[ -d "$D" ] && mv "$D" ~/dataset_backups/s101_pick_and_place_old_$(date +%Y%m%d_%H%M)
hf download NandithaaaG/s101_dataset_pick_and_place --repo-type dataset --local-dir "$D"
du -sh "$D"
```

Verified output: `Fetching 123 files: 100%`, `format v2.1 | episodes 39 | frames 23424 | fps 30`, `438M`.

Inspect with the repository script (works for v2.1 and v3.0 layouts):

```bash
# [HOST]
python scripts/inspect_dataset.py "$D"
```

## Loading in Python

```python
# [HOST] LeRobot 0.6.2 expects v3.0. Point it at the converted copy.
from lerobot.datasets import LeRobotDataset

ds = LeRobotDataset("NandithaaaG/s101_dataset_pick_and_place")  # or root=<local v3.0 path>
print(ds.num_episodes, ds.num_frames, ds.fps)
sample = ds[0]
print(sample["observation.state"], sample["action"])
print(sample["observation.images.global"].shape)  # [3, 720, 1280]
```

> The import path and the behaviour when the Hub copy is v2.1 are version-dependent. With LeRobot 0.6.2 a v2.1 dataset must be converted first; loading it directly is expected to raise a version error.

## Converting to v3.0 safely

The converter exists on the host (`src/lerobot/scripts/convert_dataset_v21_to_v30.py`). The documented usage converts a Hub dataset by repo ID:

```bash
# [HOST] documented form; check the flags first
python -m lerobot.scripts.convert_dataset_v21_to_v30 --help
python -m lerobot.scripts.convert_dataset_v21_to_v30 --repo-id=NandithaaaG/s101_dataset_pick_and_place
```

⚠️ **Check before running:** some converter versions push the converted dataset to the Hub by default, which would replace the v2.1 copy the container still needs. In Run 2 the conversion was done **without pushing** (reported). The exact no-push flag for 0.6.2 was being checked at the time of writing (`--help` plus `grep -n push ...`) and is **not recorded here**. Make a backup of the local v2.1 copy first.

## Dataset quality

| Check | Result |
|-------|--------|
| Episode count / frames / fps consistent with metadata | ✅ |
| Cameras present, not swapped (21-episode set) | ✅ Verified in viewer |
| State follows action (21-episode set) | ✅ Verified in viewer |
| Same checks on the 39-episode set | 🟡 Not explicitly recorded |
| Failed or aborted demonstrations removed | ❌ Not verified |
| Distribution of cube / tray positions | ❌ Not recorded |
| Camera colour settings consistent across sessions | ❌ Auto white balance was on |

## Limitations

- **Size:** 39 episodes (~13 minutes), below the ~50 episodes the SmolVLA guide recommends as a starting point.
- **Single task, single instruction:** the language channel carries no task-discriminating information.
- **Unknown position coverage:** without per-episode cube/tray positions, in-distribution and out-of-distribution test positions cannot be defined rigorously.
- **No validation split:** `splits` contains only `train`; overfitting cannot be measured from the dataset alone.
- **Uncontrolled colour:** gripper-camera auto white balance makes images session-dependent.
- **Format split:** v2.1 on the Hub, v3.0 on the host; the two must not be confused.
