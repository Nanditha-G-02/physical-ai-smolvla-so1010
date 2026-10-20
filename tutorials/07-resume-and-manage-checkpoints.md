# Tutorial 07 — Resume Training and Manage Checkpoints

**Evidence:** the resume command and the "End of training" behaviour are verified (container, 20 Oct).

## 1. List checkpoints

```bash
# [CONTAINER] Run 1
ls -lah /root/ros2_ws/src/physical_ai_tools/lerobot/outputs/train/so101_pick_and_place_policy/checkpoints/
# [HOST] Run 2
ls -l ~/so101_training/outputs/train/smolvla_so101_pick_place/checkpoints/
```

Verified Run 1 output: `002000` … `020000` and `last -> 020000`.

## 2. Check integrity

```bash
# [CONTAINER]
C=/root/ros2_ws/src/physical_ai_tools/lerobot/outputs/train/so101_pick_and_place_policy/checkpoints
ls -lah $C/020000/pretrained_model/
find $C/020000 -size 0          # must print nothing
```

## 3. Resume an interrupted run

```bash
# [CONTAINER] verified
cd /root/ros2_ws/src/physical_ai_tools/lerobot
python -m lerobot.scripts.train \
  --config_path=outputs/train/so101_pick_and_place_policy/checkpoints/last/pretrained_model/train_config.json \
  --resume=true
```

```bash
# [HOST] LeRobot 0.6.2 equivalent (check with --help)
lerobot-train \
  --config_path=$HOME/so101_training/outputs/train/smolvla_so101_pick_place/checkpoints/last/pretrained_model/train_config.json \
  --resume=true
```

If the run is already at its final step, you will see `End of training` immediately. That is expected.

## 4. Recover from a corrupted checkpoint

If `last` points to a checkpoint with 0-byte files (as happened to `008000` after a power cut), move it aside and point `last` at the previous intact one:

```bash
# [CONTAINER]
cd $C
mv 008000 ../008000_corrupt_backup
ln -sfn 006000 last
```

Then resume as in step 3.

## 5. Extend a finished run

Pass a higher `--steps` when resuming (check that your version allows overriding it with `--config_path`). Consider data before steps: with 39 episodes, more demonstrations are likely to help more.

## 6. Load a checkpoint in Python

```python
# [HOST] LeRobot 0.6.2; import path may differ by version
from lerobot.policies.smolvla.modeling_smolvla import SmolVLAPolicy
policy = SmolVLAPolicy.from_pretrained(
    "/home/ihub/so101_training/outputs/train/smolvla_so101_pick_place/checkpoints/last/pretrained_model"
)
policy.eval()
print(sum(p.numel() for p in policy.parameters()) / 1e6, "M parameters")
```

Container (Run 1) checkpoints were produced by an older LeRobot and may not load in 0.6.2 without conversion. The host has `lerobot_convert_dcp.py` in `src/lerobot/scripts/`; check its `--help` to see what it converts.

## 7. Back up and share

```bash
# [HOST] optional: upload a chosen checkpoint to a private model repo (requires a write token)
hf upload <HF_USER>/smolvla_so101_pick_place <checkpoint>/pretrained_model . --repo-type model --private
```

Never commit checkpoints to Git.

## Next

[Tutorial 08 — Run inference](08-run-inference.md)
