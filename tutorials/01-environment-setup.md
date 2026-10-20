# Tutorial 01 — Environment Setup

**Goal:** a host conda environment with LeRobot 0.6.2 and CUDA, plus the Physical AI Tools container.
**Time:** 30–60 min. **Evidence:** the checks in step 3 are the exact commands that passed on the project PC.

## Prerequisites

| Item | Project value |
|------|---------------|
| OS | Ubuntu (release not recorded; ROS 2 Jazzy targets 24.04) |
| GPU | NVIDIA with CUDA support (RTX 3050 6 GB used) |
| NVIDIA driver | Recent enough for CUDA 13.0 wheels (torch `+cu130`) |
| Docker | Installed, with your user able to run it (for Physical AI Tools) |
| Conda | Miniconda |

## 1. Host: create the conda environment

```bash
# [HOST] reference install; the original install commands were not recorded
conda create -y -n lerobot python=3.12
conda activate lerobot
git clone https://github.com/huggingface/lerobot.git ~/lerobot
cd ~/lerobot
git tag | grep -E "^v0\.6" && git checkout v0.6.2   # pin if the tag exists
pip install -e ".[smolvla]"
```

If PyTorch does not detect CUDA, install the wheel that matches your driver from pytorch.org, then re-run the check below.

## 2. Host: log in to Hugging Face

```bash
# [HOST]
hf auth whoami || hf auth login     # paste the token at the hidden prompt; answer "n" to git credential
```

## 3. Host: verify

```bash
# [HOST]
python scripts/verify_environment.py    # from this repository
```

or the original one-liners:

```bash
# [HOST]
python -c "import importlib.metadata as m, torch; print('lerobot', m.version('lerobot')); print('torch', torch.__version__, torch.cuda.is_available(), torch.cuda.get_device_name(0))"
python -c "import lerobot.policies.smolvla.modeling_smolvla; print('smolvla OK')"
which lerobot-train lerobot-rollout
nvidia-smi --query-gpu=memory.used,memory.total --format=csv
```

Expected (project PC): `lerobot 0.6.2`, `torch 2.11.0+cu130 True NVIDIA GeForce RTX 3050`, `smolvla OK`, both commands found, `660 MiB, 6144 MiB`.

## 4. Container: Physical AI Tools

```bash
# [HOST]
cd ~/lerobot
git clone -b jazzy https://github.com/ROBOTIS-GIT/physical_ai_tools.git --recursive
cd physical_ai_tools/docker
./container.sh enter
```

Inside the container:

```bash
# [CONTAINER]
echo $RMW_IMPLEMENTATION      # expect rmw_zenoh_cpp
export ROS_DOMAIN_ID=30        # if not already set by your setup
ros2 topic list
```

Follow the [Physical AI Tools documentation](https://ai.robotis.com/) for starting the server and web UI. The web UI is served at `http://localhost`.

## Next

[Tutorial 02 — Connect and calibrate the SO-101](02-connect-and-calibrate-so101.md)
