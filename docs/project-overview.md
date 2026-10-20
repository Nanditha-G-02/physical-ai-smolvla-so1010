# Project Overview

## Contents
- [Goal](#goal)
- [The task](#the-task)
- [Approach in one paragraph](#approach-in-one-paragraph)
- [Status by component](#status-by-component)
- [Project journey](#project-journey)
- [What has been learned so far](#what-has-been-learned-so-far)

## Goal

Teach a low-cost SO-ARM101 arm to perform a pick-and-place task **by imitation**, using a vision-language-action model (SmolVLA) fine-tuned on demonstrations collected by the author, on consumer hardware (RTX 3050, 6 GB).

## The task

Pick up a small red cube from the table and place it in a tray. Every demonstration and every inference run uses the same instruction string:

> *"Move the SO-ARM101 follower arm to pick up an object from the starting position and place it at the target location. Perform the task smoothly and safely."*

Because there is one task and one instruction, the language input does not have to distinguish between tasks. The model still receives it, because SmolVLA conditions on text.

## Approach in one paragraph

A person moves the **leader** arm by hand. A custom ROS 2 node (`bridge.py`) reads the leader's joint positions, sends them to the **follower** arm, and publishes both the leader command (the *action*) and the follower's measured joints (the *state*). Two cameras, the Orbbec Femto Bolt (scene) and a gripper-mounted USB camera, publish images. ROBOTIS **Physical AI Tools** records these synchronized streams at 30 fps into a **LeRobot** dataset, which is pushed to the Hugging Face Hub. **SmolVLA** is fine-tuned on that dataset. At inference time the policy publishes predicted actions on the same action topic, and a second custom node (`inference_bridge.py`) turns them into rate-limited, distance-capped servo goals.

## Status by component

| Component | Implemented | Tested | Notes |
|-----------|:-----------:|:------:|-------|
| Leader–follower teleoperation | ✅ | ✅ | All 12 servos respond; mirroring works |
| Two-camera streaming (30 Hz) | ✅ | ✅ | Stable device naming, gamma fix |
| Recording in Physical AI Tools | ✅ | ✅ | 39 + 21 episodes recorded |
| Dataset on Hugging Face | ✅ | ✅ | Metadata verified on the Hub |
| SmolVLA training in container (Run 1) | ✅ | ✅ | 20,000 steps; checkpoints present |
| Offline check of Run 1 | ✅ | 🟡 | Reported good agreement on episode 0 |
| v2.1 → v3.0 conversion for host | ✅ (earlier) | 🟡 | Re-run on a fresh download is pending |
| SmolVLA training on host (Run 2) | ✅ | ❌ | Completion not verified |
| Inference through web UI + `inference_bridge.py` | ✅ | 🟡 | Reaches the cube; no grasp |
| Inference with `lerobot-rollout` on host | ⏳ | ❌ | Planned |
| Real-world success rate | ⏳ | ❌ | Protocol written, not run |

## Project journey

The timeline below is reconstructed from the conversation history and checkpoint timestamps. Exact dates are given only where a terminal output shows them.

| Phase | What happened | Outcome |
|-------|---------------|---------|
| **0. Earlier experiment** | A 20-episode SO-101 grab-and-place dataset with front and side cameras was published for ACT experiments ([grab_place_training](https://huggingface.co/datasets/NandithaaaG/grab_place_training), updated ~3 Oct 2026). | Predecessor dataset; how it relates to this pipeline is not documented |
| **1. Hardware bring-up** | Assembled the leader and follower; connected two CH34x serial boards. Saw "No status packet" errors and missing motor IDs. | Root cause: a chain of USB 2.0 hubs repeatedly resetting the adapters, plus two programs opening the same serial port. Fixed by "one program per port"; long-term USB fix still pending. |
| **2. Cameras** | Added the Femto Bolt and the gripper camera via `v4l2_camera`. Hit a gamma crash, swapped cameras after replugging, and a Femto Bolt crash with a `Y16` encoding error. | `gamma:=100`, stable `/dev/v4l/by-id` / `by-path` names, `find_femto.sh` to pick the YUYV colour node, and a powered USB 3 port |
| **3. Teleoperation bridge** | Wrote `bridge.py` to mirror leader → follower and publish `/follower_joint_states` and `/leader/joint_trajectory`. | Verified mirroring |
| **4. Recording** | Configured `s101_dataset_config.yaml` in Physical AI Tools; recorded 21 episodes (`nanditha123/...`), validated in the dataset viewer (cameras not swapped, 6 joints, state follows action); then recorded 39 episodes (`NandithaaaG/s101_dataset_pick_and_place`). | Main dataset: 39 episodes, 23,424 frames |
| **5. Training "not found" errors** | Training and the viewer reported the dataset as missing. | The selected folder was empty; the real repo ID carries the `s101_dataset_` prefix |
| **6. Run 1 training (container), 17 Oct** | SmolVLA, batch 2, 20k steps. A power cut at ~8k steps left `008000` with 0-byte files. The web UI could not resume (a page-side path check), so training was resumed from `006000` on the command line, ran to 10k, then was extended to 20k. | `last -> 020000` at 15:47; reported loss ≈ 0.04 |
| **7. Offline check** | `offline_eval.py` compared predicted vs recorded actions on episode 0. | Within ≈ 2–5 units per joint; phase timing matched (reported) |
| **8. Inference attempt 1** | Arm did not move. | `bridge.py` was still running, so the follower obeyed the leader |
| **9. Inference attempt 2** | Arm hovered near rest and drifted toward the tray. | The bridge limited speed relative to the *measured* position (2 units per tick); under gravity the servos lagged, so the model saw an arm that barely moved |
| **10. Inference attempt 3 (bridge v2)** | Arm reached out and positioned the gripper over the cube, then hovered without grasping. | Likely distribution shift: extra red cubes in view, gripper-camera auto white balance, short inference episode |
| **11. Run 2 training (host, LeRobot 0.6.2)** | Converted dataset v2.1 → v3.0 without pushing; fine-tuned from `lerobot/smolvla_base` with a camera rename map; batch 4. | ≈ 0.53 s/step, ≈ 2.5 GB GPU, loss ≈ 0.09 at 7.5k steps; completion not verified |
| **12. Fresh download, 19 Oct** | Moved the cached dataset to a backup and re-downloaded it (123 files, 438 MB on disk) to start the host pipeline cleanly. Converter options check (Step 4a) pending. | Verified v2.1 metadata locally |
| **13. Run 1 resume check, 20 Oct** | Resuming Run 1 printed "End of training" immediately. | Confirms Run 1 is complete at 20,000 steps |

## What has been learned so far

1. **Most failures were systems problems, not learning problems.** USB power and topology, device naming, process contention on serial ports and ROS topic wiring caused more lost time than the model.
2. **Closed-loop control exposes what offline metrics hide.** A model that matches recorded actions within a few units can still fail on the robot if the controller interface (rate limiting relative to measured position) changes what the model observes.
3. **Test conditions must match training conditions.** Extra cubes and a different camera white balance are small to a human but significant to a policy trained on 39 episodes.
4. **Small GPUs force small batches.** Batch 2–4 over 20k steps gives the model only a few passes over the data (see [smolvla-training.md](smolvla-training.md#how-much-data-did-the-model-actually-see)).

More in [experiments/lessons-learned.md](../experiments/lessons-learned.md).
