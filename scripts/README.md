# Scripts

Small utilities written for this documentation repository. They use only the Python standard library unless noted.

| Script | Run where | Purpose |
|--------|-----------|---------|
| [verify_environment.py](verify_environment.py) | [HOST], conda env `lerobot` | Checks Python, PyTorch/CUDA, LeRobot version, SmolVLA import, `lerobot-train`/`lerobot-rollout`, free GPU memory and Hugging Face login (never prints the token) |
| [inspect_dataset.py](inspect_dataset.py) | [HOST] | Summarizes a local LeRobot dataset (v2.1 or v3.0): totals, cameras, joint names, episode lengths, tasks, consistency checks. Reading v3.0 episode metadata needs `pyarrow` |
| [check_links.py](check_links.py) | Anywhere | Verifies every relative Markdown link and `#anchor` in the repository |
| [scan_secrets.py](scan_secrets.py) | Anywhere | Flags tokens, keys, `.env` files, weights, videos and files above 5 MB before you commit |

```bash
python scripts/verify_environment.py
python scripts/inspect_dataset.py ~/.cache/huggingface/lerobot/NandithaaaG/s101_dataset_pick_and_place
python scripts/check_links.py
python scripts/scan_secrets.py
```

## Project scripts not included yet

The robot-side scripts written during the project (`bridge.py`, `inference_bridge.py`, `start_cameras.sh`, `find_femto.sh`, `offline_eval.py`) are documented in [docs/](../docs/) but their source was not available when this repository was assembled. Add them under `src/` (or a separate code repository) and update the docs; see [VERIFICATION_STATUS](../VERIFICATION_STATUS.md#missing-files-you-should-add).
