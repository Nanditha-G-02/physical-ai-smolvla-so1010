# Tutorial 05 — Inspect and Convert the Dataset

**Goal:** a fresh local copy of the dataset, verified metadata, and a v3.0 copy for LeRobot 0.6.2, **without** overwriting the v2.1 copy on the Hub.
**Evidence:** steps 1–2 are the verified commands from 19 Oct. Step 3 (conversion flags) still needs checking on your machine.

## 1. Download a fresh copy (keep a backup of the old one)

```bash
# [HOST]
conda activate lerobot
D=~/.cache/huggingface/lerobot/NandithaaaG/s101_dataset_pick_and_place
mkdir -p ~/dataset_backups
[ -d "$D" ] && mv "$D" ~/dataset_backups/s101_pick_and_place_old_$(date +%Y%m%d_%H%M)
hf download NandithaaaG/s101_dataset_pick_and_place --repo-type dataset --local-dir "$D"
du -sh "$D"            # verified: 438M
```

## 2. Inspect

```bash
# [HOST]
python scripts/inspect_dataset.py "$D"
```

Verified metadata: `v2.1`, 39 episodes, 23,424 frames, 30 fps, `observation.images.global` [720, 1280, 3], `observation.images.gripper` [480, 640, 3], `observation.state` [6], `action` [6].

Also open a few episodes in the [visualizer](https://huggingface.co/spaces/lerobot/visualize_dataset?path=/NandithaaaG/s101_dataset_pick_and_place/episode_0).

## 3. Check the converter **before** running it

```bash
# [HOST] read-only
cd ~/lerobot
python -m lerobot.scripts.convert_dataset_v21_to_v30 --help
grep -n -iE "push|hub|root|def convert|argparse|add_argument" src/lerobot/scripts/convert_dataset_v21_to_v30.py | head -n 40
```

Answer three questions from the output:

1. Does it **push to the Hub** by default? If yes, which flag disables it?
2. Does it convert a **local** directory, or download its own copy?
3. Does it keep a **backup** of the v2.1 files?

## 4. Convert

The documented form is:

```bash
# [HOST] only after step 3; add the no-push / local-root flags you found
python -m lerobot.scripts.convert_dataset_v21_to_v30 --repo-id=NandithaaaG/s101_dataset_pick_and_place
```

Do **not** run it in a way that pushes to `NandithaaaG/s101_dataset_pick_and_place` while the container still trains or records with v2.1. If in doubt, copy the dataset to a scratch directory and convert the copy.

## 5. Verify the conversion

```bash
# [HOST]
python scripts/inspect_dataset.py <path-to-converted-copy>     # expect codebase_version v3.0, same totals
python -c "from lerobot.datasets import LeRobotDataset as D; d=D('NandithaaaG/s101_dataset_pick_and_place', root='<path-to-converted-copy>'); print(d.num_episodes, d.num_frames)"
```

Expected: 39 episodes and 23,424 frames, unchanged. The import path may differ by version.

## Next

[Tutorial 06 — Train SmolVLA](06-train-smolvla.md)
