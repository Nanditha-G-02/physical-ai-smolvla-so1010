# Verification Status

This repository was reconstructed from the project's working conversation (terminal outputs, configuration dumps, and the project summary written during development) plus public sources checked on **20 October 2026**. No files from the robot PC were directly inspected while writing it. This page lists what is verified, what is only reported, and what is still missing.

## Evidence levels used throughout the repository

| Label | Meaning |
|-------|---------|
| ✅ **Verified** | Seen directly in a terminal output, configuration dump, or public metadata |
| 🟡 **Reported** | Stated in the project summary or conversation, but the raw output is not archived here |
| 🔧 **Reconstructed** | A command or configuration rebuilt from known facts; must be checked against shell history |
| ❌ **Not verified / not measured** | No evidence available |
| ⏳ **Planned** | Future work |

## Verified facts

| Fact | Source |
|------|--------|
| Host: LeRobot 0.6.2, torch 2.11.0+cu130, CUDA available, RTX 3050, 6144 MiB total GPU memory | Host check output |
| `lerobot-train`, `lerobot-rollout` installed in conda env `lerobot`; SmolVLA module imports | Host check output |
| `convert_dataset_v21_to_v30.py` and `lerobot_convert_dcp.py` exist in `src/lerobot/scripts/` | Host `ls` output |
| Logged in to Hugging Face as `NandithaaaG` | `hf auth whoami` |
| Dataset: v2.1, 39 episodes, 23,424 frames, 30 fps, 1 task, 78 videos, `robot_type: s101_dataset`, libx264 yuv420p, Apache-2.0, 458 MB | Hub page and `meta/info.json` |
| Features: `observation.images.global` 720×1280×3, `observation.images.gripper` 480×640×3, `observation.state` [6], `action` [6] with joint names | `meta/info.json` |
| Run 1 checkpoints `002000`–`020000`, `last -> 020000`, dated 17 Oct, 11:27–15:47 | Container `ls` output |
| Run 1 full configuration (batch 2, 20k steps, AdamW, cosine schedule, SmolVLA settings) | `train_config.json` dump on resume |
| Run 1 learnable parameters 99,880,992; total 450,046,212 | Training log |
| Resuming Run 1 at step 20,000 exits immediately ("End of training") | Container output, 20 Oct |
| Physical AI Tools is a ROBOTIS project combining LeRobot and ROS 2 (Apache-2.0) | GitHub |
| Second public dataset `NandithaaaG/grab_place_training`: 20 episodes, 29,917 frames, front + side 640×480 | Hub dataset card |

## Reported but not archived (🟡)

- Run 1 final loss ≈ 0.04.
- Run 1 offline evaluation: per-joint error ≈ 2–5 units on episode 0; reach/open/grasp/transport timing matched.
- Run 1 power cut at ~8,000 steps; checkpoint `008000` had 0-byte files; resumed from `006000`; later extended to 20,000.
- Run 2: `lerobot/smolvla_base`, batch 4, 20k steps, save every 2k steps, rename map (global→camera1, gripper→camera2, one empty camera), ≈ 0.53 s/step, ≈ 2.5 GB GPU, loss ≈ 0.09 at step 7,500.
- Three inference attempts and their diagnosed causes.
- Hardware fault history (USB hub resets, gamma crash, swapped cameras, Femto Bolt depth node).
- Earlier dataset `nanditha123/s101_dataset_SO101_Pick_and_Place` (21 episodes) validated in the dataset viewer. **This repository could not be found publicly** (it may be private, renamed, or deleted).

## Not verified / not measured (❌)

- Whether Run 1 was initialised from `lerobot/smolvla_base` or only from the SmolVLM-2 backbone. Check with:
  `grep -n pretrained_path outputs/train/so101_pick_and_place_policy/checkpoints/last/pretrained_model/train_config.json`
- Whether Run 2 completed 20,000 steps.
- The exact LeRobot version/commit inside the container.
- Ubuntu release on the host (ROS 2 Jazzy targets Ubuntu 24.04; not confirmed for the host itself).
- Integrity of checkpoint `020000` files (command in [docs/smolvla-training.md](docs/smolvla-training.md)).
- How many distinct cube and tray positions the 39 demonstrations cover.
- Motor calibration procedure and calibration files used.
- Any real-world success rate.

## Missing files you should add

| Needed | Where it goes | Why |
|--------|---------------|-----|
| `bridge.py`, `inference_bridge.py`, `start_cameras.sh`, `find_femto.sh`, `offline_eval.py` | A separate code repository, or `src/` here | The docs describe their behaviour, but the source was not available to include |
| `s101_dataset_config.yaml` (Physical AI Tools robot config) | `experiments/training-configs/` | Documents the exact topic mapping |
| Run 1 `train_config.json` (original file) | `experiments/training-configs/` | Replace the reconstructed JSON with the real one |
| Run 1 and Run 2 training logs (loss curves) | `experiments/` | Turn 🟡 loss values into ✅ |
| Offline evaluation output / plots | `experiments/evaluation-results/` | Evidence for the offline check |
| Exact Run 2 command (from `history`) | `experiments/training-configs/run2_host_lerobot062.md` | Replace the reconstructed command |
| Photos of the setup, screenshots of the web UI and dataset viewer | `assets/` | No real images were available; none were fabricated |
| Your GitHub username | README badges, `CITATION.cff` | Currently placeholders |
| Licence choice confirmation | `LICENSE` | MIT was chosen as a default |
