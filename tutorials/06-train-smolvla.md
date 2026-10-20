# Tutorial 06 — Train SmolVLA

Two paths, matching the project's two runs. **Path A** is the host (LeRobot 0.6.2) and is recommended for new work. **Path B** is the container (Run 1).

## Path A — Host, LeRobot 0.6.2 (Run 2 style)

**Evidence:** Run 2 settings are reported; the command below is 🔧 reconstructed. Verify every flag with `lerobot-train --help`.

```bash
# [HOST]
conda activate lerobot
nvidia-smi --query-compute-apps=pid,used_memory --format=csv     # nothing else on the GPU

lerobot-train \
  --policy.path=lerobot/smolvla_base \
  --dataset.repo_id=NandithaaaG/s101_dataset_pick_and_place \
  --dataset.root=<path-to-local-v3.0-copy> \
  --rename_map='{"observation.images.global": "observation.images.camera1", "observation.images.gripper": "observation.images.camera2"}' \
  --policy.empty_cameras=1 \
  --batch_size=4 \
  --steps=20000 \
  --save_freq=2000 \
  --output_dir=$HOME/so101_training/outputs/train/smolvla_so101_pick_place \
  --job_name=smolvla_so101_pick_place \
  --policy.device=cuda \
  --policy.push_to_hub=false \
  --wandb.enable=false
```

What to watch:

| Signal | Project reference |
|--------|-------------------|
| Speed | ≈ 0.53 s/step at batch 4 |
| GPU memory (`watch -n 5 nvidia-smi`) | ≈ 2.5 GB |
| Loss | ≈ 0.09 at step 7,500 |

Run it inside `tmux` or `screen` so a closed terminal does not kill training, and save the log:

```bash
# [HOST]
tmux new -s train
lerobot-train ... 2>&1 | tee ~/so101_training/run2.log
```

## Path B — Container (Run 1 style)

Run 1 was started from the web UI. To start a new run from the command line in the container, check the bundled version's flags first:

```bash
# [CONTAINER]
cd /root/ros2_ws/src/physical_ai_tools/lerobot
python -m lerobot.scripts.train --help | less
```

The verified Run 1 configuration is in [experiments/training-configs/run1_container_train_config.json](../experiments/training-configs/run1_container_train_config.json).

## Before you train: check the initialization

Fine-tuning from `lerobot/smolvla_base` (pretrained on community SO-arm data) is strongly preferable to training the action expert from scratch. For an existing run:

```bash
grep -n pretrained_path <output_dir>/checkpoints/last/pretrained_model/train_config.json
```

## After training

Record the run in [experiments/experiment-log.md](../experiments/experiment-log.md): command, dataset revision, final loss, duration, checkpoint path.

## Next

[Tutorial 07 — Resume and manage checkpoints](07-resume-and-manage-checkpoints.md)
