# Tutorial 03 — Teleoperate (Leader → Follower over ROS 2)

**Goal:** the follower mirrors the leader, and the state and action topics are published for recording.
**Evidence:** this is the verified project setup (custom `bridge.py`), whose source is not yet in this repository.

## 1. Start the cameras

```bash
# [CONTAINER] terminal 1
~/start_cameras.sh
```

Expected: both camera nodes start without the gamma crash ([T2](../docs/troubleshooting.md#t2-gripper-camera-crashes-on-start-gamma)).

## 2. Start the teleoperation bridge

```bash
# [CONTAINER] terminal 2
python3 bridge.py          # adjust path and arguments to your copy
```

## 3. Check the topics

```bash
# [CONTAINER] terminal 3
ros2 topic list
ros2 topic hz /follower_joint_states
ros2 topic echo --once /follower_joint_states
ros2 topic echo --once /leader/joint_trajectory
ros2 topic hz /camera/color/image_raw/compressed
ros2 topic hz /gripper_camera/color/image_raw/compressed
```

Expected: joint names `shoulder_pan … gripper`; cameras at ~30 Hz.

## 4. Practise the task

Before recording, practise until the motion is smooth and consistent:

1. Start from the rest pose.
2. Move above the cube, align the jaws, descend, close.
3. Lift, move to the tray, release.
4. Return to the rest pose.

Watch the **follower** (it lags under gravity), not the leader.

## Common problems

| Symptom | Fix |
|---------|-----|
| "No status packet" | Another process owns the port, or a hub reset: [T1](../docs/troubleshooting.md#t1-no-status-packet-and-missing-motor-ids) |
| Cameras on the wrong topics | Use stable names: [T3](../docs/troubleshooting.md#t3-cameras-swapped-after-replugging) |
| Topics invisible from another terminal | RMW / domain mismatch: [T15](../docs/troubleshooting.md#t15-ros-nodes-do-not-see-each-other) |

## Next

[Tutorial 04 — Record a dataset](04-record-dataset.md)
