# Tutorial 08 — Run Inference on the Robot

**Goal:** the trained policy drives the follower safely, under the same conditions as training, and each trial is logged.
**Evidence:** the web-UI path with `inference_bridge.py` v2 is verified to reach the cube; no successful grasp yet.

## 0. Safety

Clear the workspace, keep a hand near the power switch, and do a dry run first. Never run teleoperation and inference together.

## 1. Match the training conditions

- [ ] One red cube, at a position used in the demonstrations; no other cubes.
- [ ] Gripper-camera white balance locked (ideally the value used when recording).
- [ ] Arm at the recording rest pose.
- [ ] Same instruction text as the dataset.
- [ ] Episode duration ≥ 20–30 s.

## 2. Start cameras; stop teleoperation

```bash
# [CONTAINER]
~/start_cameras.sh
pkill -f "bridge.py" || true          # careful: this also matches inference_bridge.py, so run it before starting that
pgrep -af bridge                       # should print nothing
```

## 3. Dry run, then live

```bash
# [CONTAINER] argument names are illustrative; use your script's flags
python3 inference_bridge.py --dry-run
```

Start inference in the web UI (`http://localhost`) with the checkpoint `.../checkpoints/020000/pretrained_model`, the instruction, and the duration. Read the logged goals: are they plausible joint values that move toward the cube?

Then restart the bridge without `--dry-run` and run again.

## 4. Diagnose a non-grasp

While the arm hovers over the cube, record:

```bash
# [CONTAINER]
ros2 topic echo /leader/joint_trajectory | grep -A6 positions     # does the gripper command change?
ros2 topic echo /follower_joint_states                            # does the measured gripper follow?
```

| Observation | Likely meaning |
|-------------|---------------|
| Gripper command never moves toward "closed" | The model does not recognize the grasp moment (distribution shift, under-training) |
| Command closes but follower does not | The bridge's cap or rate limit is blocking it |
| Command and follower close, but on air | Misalignment: perception or open-loop chunk too long |

## 5. Log the trial

Add a row to [experiments/evaluation-results/trial_log_template.csv](../experiments/evaluation-results/trial_log_template.csv) (copy it first). Follow the [evaluation protocol](../docs/evaluation.md) when you are ready to measure success rates.

## Alternative: host `lerobot-rollout` (planned, unverified)

See [docs/inference.md](../docs/inference.md#host-path-lerobot-rollout-planned). Confirm that LeRobot's calibration of the follower produces the same joint units as the dataset before trying it.
