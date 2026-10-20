# Software Setup

Covers the host environment, Docker, ROS 2, LeRobot and Hugging Face authentication.

## Contents
- [Overview](#overview)
- [Host environment (conda)](#host-environment-conda)
- [Docker: Physical AI Tools](#docker-physical-ai-tools)
- [ROS 2 configuration](#ros-2-configuration)
- [LeRobot versions and entry points](#lerobot-versions-and-entry-points)
- [Hugging Face authentication](#hugging-face-authentication)
- [Version-dependency warnings](#version-dependency-warnings)

## Overview

| Component | Host | Container |
|-----------|------|-----------|
| Python | 3.12 (reported) | Container default (not recorded) |
| PyTorch | 2.11.0+cu130 ✅ | Container build (not recorded) |
| CUDA available | True ✅ | Yes (training ran on `cuda`) ✅ |
| LeRobot | 0.6.2 ✅ | Bundled with Physical AI Tools (version not recorded) |
| Video decoding | — | `pyav` (log: "torchcodec is not available... falling back to pyav") ✅ |
| ROS 2 | Not used | Jazzy with `rmw_zenoh_cpp` ✅ |

## Host environment (conda)

The host environment is named `lerobot` and lives in `~/miniconda3/envs/lerobot`. LeRobot is installed from a source checkout in `~/lerobot` (the converter script is under `src/lerobot/scripts/`).

Verification commands that were run and passed:

```bash
# [HOST]
conda activate lerobot
cd ~/lerobot
python -c "import sys, importlib.metadata as m, torch; print(sys.executable); print('lerobot', m.version('lerobot')); print('torch', torch.__version__, '| cuda', torch.cuda.is_available(), '|', torch.cuda.get_device_name(0))"
python -c "import lerobot.policies.smolvla.modeling_smolvla; print('smolvla OK')"
which lerobot-train lerobot-rollout
ls src/lerobot/scripts | grep -i convert
nvidia-smi --query-gpu=memory.used,memory.total --format=csv
nvidia-smi --query-compute-apps=pid,used_memory --format=csv
```

Verified output (abridged):

```text
/home/ihub/miniconda3/envs/lerobot/bin/python
lerobot 0.6.2
torch 2.11.0+cu130 | cuda True | NVIDIA GeForce RTX 3050
smolvla OK
/home/ihub/miniconda3/envs/lerobot/bin/lerobot-train
/home/ihub/miniconda3/envs/lerobot/bin/lerobot-rollout
convert_dataset_v21_to_v30.py
lerobot_convert_dcp.py
660 MiB, 6144 MiB
```

The same checks are packaged in [scripts/verify_environment.py](../scripts/verify_environment.py).

**Installing from scratch** (reference, follows the official [LeRobot installation guide](https://huggingface.co/docs/lerobot/installation); the exact install commands used on this PC were not recorded):

```bash
# [HOST] reference only
conda create -y -n lerobot python=3.12
conda activate lerobot
git clone https://github.com/huggingface/lerobot.git ~/lerobot
cd ~/lerobot
git checkout v0.6.2            # pin to the version this project used, if the tag exists
pip install -e ".[smolvla]"
```

## Docker: Physical AI Tools

[ROBOTIS Physical AI Tools](https://github.com/ROBOTIS-GIT/physical_ai_tools) packages a ROS 2 interface around LeRobot, with a web UI for recording, training and inference. It is cloned recursively (LeRobot is a git submodule) on the `jazzy` branch:

```bash
# [HOST] reference: clone command from the Physical AI Tools README
git clone -b jazzy https://github.com/ROBOTIS-GIT/physical_ai_tools.git --recursive
```

On this PC the repository lives at `~/lerobot/physical_ai_tools`. Entering the container (verified):

```bash
# [HOST]
cd ~/lerobot/physical_ai_tools/docker
./container.sh enter
```

The script sets up X11 forwarding and drops you into `/root/ros2_ws` inside the container. The LeRobot checkout used for training inside the container is at `/root/ros2_ws/src/physical_ai_tools/lerobot`.

| Service | Role |
|---------|------|
| `physical_ai_server` | ROS 2 node that records datasets, launches training and runs inference |
| `physical_ai_manager` | Web UI served at `http://localhost` |
| `open_manipulator` | ROBOTIS manipulator packages |

## ROS 2 configuration

| Setting | Value |
|---------|-------|
| Distribution | Jazzy |
| RMW | `rmw_zenoh_cpp` (default since Physical AI Tools v1.0.0; set in the container's `~/.bashrc`) |
| Domain | `ROS_DOMAIN_ID=30` |

Useful checks inside the container:

```bash
# [CONTAINER]
echo $RMW_IMPLEMENTATION $ROS_DOMAIN_ID
ros2 topic list
ros2 topic hz /camera/color/image_raw/compressed
ros2 topic echo --once /follower_joint_states
```

Every terminal that runs a ROS node (bridges, camera script) must use the same `RMW_IMPLEMENTATION` and `ROS_DOMAIN_ID`, or the nodes will not see each other.

## LeRobot versions and entry points

| Task | Container (verified) | Host LeRobot 0.6.2 (verified installed) |
|------|----------------------|-----------------------------------------|
| Train | `python -m lerobot.scripts.train --config_path=... --resume=true` | `lerobot-train ...` |
| Run policy on robot | Physical AI Tools web UI + `inference_bridge.py` | `lerobot-rollout ...` (installed; not yet used) |
| Convert dataset | — | `python -m lerobot.scripts.convert_dataset_v21_to_v30` |

## Hugging Face authentication

```bash
# [HOST]
hf auth whoami        # verified output: "✓ Logged in  user: NandithaaaG"
hf auth login         # only if not logged in; paste the token at the hidden prompt
```

Rules:

- A **read** token is enough to download. Uploading datasets or models needs **write** permission.
- Answer `n` to "Add token as git credential?" unless you need it.
- Never write the token into scripts, notebooks or this repository. For non-interactive use, export it in the shell: `export HF_TOKEN=...` (and never commit shell history files).

## Version-dependency warnings

- **Dataset format.** LeRobot ≥ 0.4.0 uses dataset format v3.0; the container's LeRobot reads v2.1. Do not push a converted v3.0 dataset over the v2.1 Hub copy while the container still depends on it. Check whether the converter pushes by default before running it (`--help`).
- **Training CLI.** Older LeRobot uses `python -m lerobot.scripts.train`; current LeRobot uses `lerobot-train`. Flags also changed between versions (for example the camera `rename_map`). Always confirm with `--help` in the environment you are using.
- **Checkpoints are version-bound.** A checkpoint trained in the container may not load in LeRobot 0.6.2 without conversion, and vice versa. Treat Run 1 and Run 2 as separate model families.
