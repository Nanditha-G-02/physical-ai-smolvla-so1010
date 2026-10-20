# Experiment Log

Evidence labels: ✅ verified · 🟡 reported · 🔧 reconstructed · ❌ not measured. See [VERIFICATION_STATUS](../VERIFICATION_STATUS.md).

## Summary table

| Field | Run 1 (container) | Run 2 (host) |
|-------|-------------------|--------------|
| ID | `so101_pick_and_place_policy` | `smolvla_so101_pick_place` |
| Date | 17 Oct 2026 (checkpoints 11:27–15:47) ✅ | Not recorded; started after Run 1 |
| Model | SmolVLA ✅ | SmolVLA 🟡 |
| VLM | `HuggingFaceTB/SmolVLM2-500M-Video-Instruct` ✅ | Same (via `smolvla_base`) 🟡 |
| Pretrained checkpoint | ❌ Not verified (`pretrained_path` not in the log) | `lerobot/smolvla_base` 🟡 |
| Dataset | `NandithaaaG/s101_dataset_pick_and_place` ✅ | Same, v3.0 local conversion 🟡 |
| Dataset revision | `null` (latest at the time) ✅ | Not recorded |
| Dataset format | v2.1 ✅ | v3.0 🟡 |
| Episodes / frames | 39 / 23,424 ✅ | 39 / 23,424 🟡 |
| Camera keys | `global`, `gripper` ✅ | `camera1`, `camera2` (+1 empty) 🟡 |
| LeRobot | Bundled with Physical AI Tools (version not recorded) | 0.6.2 ✅ |
| GPU | RTX 3050 6 GB ✅ | RTX 3050 6 GB ✅ |
| Batch size | 2 ✅ | 4 🟡 |
| Steps | 20,000 ✅ | 20,000 planned 🟡 |
| Optimizer | AdamW, lr 1e-4, betas (0.9, 0.95), wd 1e-10, clip 10 ✅ | Policy preset (not recorded) |
| Scheduler | Cosine with warmup: 1k warmup, 30k decay, floor 2.5e-6 ✅ | Not recorded |
| Mixed precision | Off ✅ | Not recorded |
| Image augmentation | Off ✅ | Not recorded |
| Trainable / total params | 99,880,992 / 450,046,212 ✅ | Not recorded |
| Speed | ≈ 0.35–0.36 s/step (derived from checkpoint times) | ≈ 0.53 s/step 🟡 |
| GPU memory | Not recorded | ≈ 2.5 GB 🟡 |
| Duration | ≈ 4.3 h wall clock including power-cut recovery and extension (11:15–15:47, approx.) | ≈ 3 h expected |
| Final loss | ≈ 0.04 🟡 | ≈ 0.09 at 7.5k 🟡; final ❌ |
| Checkpoints | `.../checkpoints/{002000..020000}`, `last → 020000` ✅ | Not verified |
| Offline eval | Episode 0: ≈ 2–5 units per joint; phase timing matched 🟡 | ❌ |
| Real-robot eval | 3 informal attempts; reach yes, grasp no 🟡 | ❌ |
| Success rate | ❌ Not measured | ❌ Not measured |

## Run 1 — events

| Time (17 Oct) | Event |
|---------------|-------|
| ≈ 11:15 (estimated) | Training started from the web UI |
| 11:27 / 11:39 / 11:51 | Checkpoints 2k / 4k / 6k |
| ≈ 12:00–12:30 | Power cut during the 8k checkpoint write; `008000` left with 0-byte files 🟡 |
| — | Web UI resume failed (page-side path check); resumed from `006000` on the CLI 🟡 |
| 12:46 / 13:03 | Checkpoints 8k / 10k (original target) |
| — | Extended to 20k steps |
| 14:21 → 15:47 | Checkpoints 12k → 20k; `last → 020000` |

20 Oct: resuming printed `End of training` immediately, which confirms the run is complete ✅.

## Inference experiments (Run 1 checkpoint)

| # | Setup | Result | Diagnosis | Change made |
|---|-------|--------|-----------|-------------|
| I-1 | Web UI inference, `bridge.py` still running | No motion from the model | Teleop bridge commanding the follower | Stop `bridge.py` |
| I-2 | `inference_bridge.py` v1 (±2 units around measured position) | Hover near rest, drift to tray | Gravity lag + measured-position rate limit | Bridge v2 |
| I-3 | `inference_bridge.py` v2 (goal-based limit + distance cap) | Reached cube, gripper over cube, no grasp | Suspected: extra cubes, gripper-camera WB, short episode | Pending: matched-condition re-test |

## Training loss vs task success

Run 1's loss (≈ 0.04) is a **flow-matching velocity loss on normalized actions**, averaged over training samples. It measures how well the model imitates recorded data, not whether the robot completes the task. Run 1 has a low loss and a good offline match, yet **0 measured task successes**. Only the [evaluation protocol](../docs/evaluation.md) produces evidence of task success.

## Planned experiments

| ID | Hypothesis | Change | Measure |
|----|-----------|--------|---------|
| E-1 | Distribution shift prevents the grasp | One cube, trained position, locked WB, ≥ 20 s episode | Grasp yes/no over 10 ID trials |
| E-2 | Open-loop chunks are too long for the grasp | `n_action_steps` 50 → 15 at inference | Same as E-1 |
| E-3 | The bridge blocks gripper closing | Log the commanded vs measured gripper | Does the command close? |
| E-4 | Under-training | Retrain with more samples, augmentation, held-out episodes | Held-out MAE; E-1 metric |
| E-5 | More, structured data helps | +20 episodes on a 5-position grid | ID and Interp success |
| E-6 | ACT is competitive on this data | Train ACT on the same dataset | Same protocol |

Template for new entries: copy a column of the summary table, and log trials in [evaluation-results/trial_log_template.csv](evaluation-results/trial_log_template.csv).
