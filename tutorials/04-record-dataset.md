# Tutorial 04 — Record a Dataset with Physical AI Tools

**Goal:** a LeRobot dataset of consistent pick-and-place demonstrations on the Hugging Face Hub.
**Evidence:** the project recorded 39 episodes this way. The step-by-step UI clicks were not recorded; follow the [Physical AI Tools docs](https://ai.robotis.com/) for exact screens.

## 1. Prepare the scene (checklist)

- [ ] One red cube, one tray; nothing else on the table.
- [ ] Gripper camera white balance and exposure **locked** (see [camera integration](../docs/camera-integration.md#gripper-camera-gamma-and-white-balance)); write the values down.
- [ ] Camera mounts tight; positions marked.
- [ ] Cube positions marked with tape and numbered (e.g. P1–P5).
- [ ] A CSV ready to log `episode_index, cube_position, tray_position, notes`.

## 2. Start the stack

Cameras + `bridge.py` as in [tutorial 03](03-teleoperate.md). Confirm all four topics are live.

## 3. Configure recording in the web UI

| Field | Project value |
|-------|---------------|
| Robot configuration | `s101_dataset_config.yaml` |
| Repo ID | `NandithaaaG/s101_dataset_pick_and_place` (or a new repo for new data) |
| Task instruction | `Move the SO-ARM101 follower arm to pick up an object from the starting position and place it at the target location. Perform the task smoothly and safely.` |
| FPS | 30 |
| Episode time | ≈ 20 s (the existing dataset averages 20.0 s) |

> Recording **new** data into a **new** repo ID is safer than appending to the existing dataset: training runs stay reproducible and the old data stay untouched.

## 4. Record

For each episode: place the cube at the next position, log it, start from rest, record, demonstrate, return to rest, stop. Re-record any episode with a hesitation, a failed grasp or a bump.

Suggested plan: 5 positions × 4 episodes = 20 new episodes ([dataset design](../learning/dataset-design-and-generalization.md#a-recording-plan-for-this-project)).

## 5. Push and validate

Push to the Hub from the UI, then open the visualizer:

```
https://huggingface.co/spaces/lerobot/visualize_dataset?path=/<HF_USER>/<REPO>/episode_0
```

Check that the cameras are not swapped, all six joints are present, state follows action, and the gripper actually closes on the cube.

## Next

[Tutorial 05 — Inspect and convert the dataset](05-inspect-and-convert-dataset.md)
