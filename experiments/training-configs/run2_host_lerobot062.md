# Run 2 — Host Training Configuration (LeRobot 0.6.2)

**Status:** 🟡 settings reported during the project; 🔧 command reconstructed. Replace the command with the exact one from your shell history (`history | grep lerobot-train`) and attach the log.

## Reported settings

| Setting | Value |
|---------|-------|
| LeRobot | 0.6.2 (host conda env `lerobot`) |
| PyTorch / CUDA | 2.11.0+cu130 |
| GPU | RTX 3050 6 GB |
| Base model | `lerobot/smolvla_base` |
| Dataset | `NandithaaaG/s101_dataset_pick_and_place`, converted locally v2.1 → v3.0 (not pushed) |
| Camera mapping | `observation.images.global → observation.images.camera1`, `observation.images.gripper → observation.images.camera2`, `empty_cameras = 1` |
| Batch size | 4 |
| Steps | 20,000 |
| Save frequency | 2,000 |
| Output | `~/so101_training/outputs/train/smolvla_so101_pick_place/` |
| Speed | ≈ 0.53 s/step |
| GPU memory | ≈ 2.5 GB |
| Loss | ≈ 0.09 at step 7,500 |
| Completed? | Not verified |

## Reconstructed command

```bash
# [HOST]
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

## To verify

```bash
# [HOST]
ls -l ~/so101_training/outputs/train/smolvla_so101_pick_place/checkpoints/
cat ~/so101_training/outputs/train/smolvla_so101_pick_place/checkpoints/last/pretrained_model/train_config.json | python -m json.tool | head -80
```

Copy that `train_config.json` into this folder as `run2_host_train_config.json`.
