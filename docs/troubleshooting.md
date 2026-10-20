# Troubleshooting

Every issue below was encountered in this project. Each entry gives the symptoms, the cause (marked **inferred** when not proven), the diagnostics, the fix (marked **verified** only if it was confirmed to work), and the lesson.

## Index

| ID | Issue | Fix status |
|----|-------|-----------|
| [T1](#t1-no-status-packet-and-missing-motor-ids) | "No status packet" / missing motor IDs | ✅ Mitigated; permanent USB fix pending |
| [T2](#t2-gripper-camera-crashes-on-start-gamma) | Gripper camera crashes on start (gamma) | ✅ Verified |
| [T3](#t3-cameras-swapped-after-replugging) | Cameras swapped after replugging | ✅ Verified |
| [T4](#t4-femto-bolt-crash-with-y16-encoding-error) | Femto Bolt crash with Y16 encoding error | ✅ Verified |
| [T5](#t5-femto-bolt-not-detected) | Femto Bolt not detected | ✅ Verified |
| [T6](#t6-dataset-not-found-in-training-or-viewer) | Dataset "not found" | ✅ Verified |
| [T7](#t7-training-interrupted-by-a-power-cut) | Power cut corrupted a checkpoint | ✅ Verified |
| [T8](#t8-web-ui-cannot-resume-training) | Web UI cannot resume training | ✅ Workaround verified |
| [T9](#t9-model-runs-but-the-arm-does-not-move) | Model runs, arm does not move | ✅ Verified |
| [T10](#t10-arm-creeps-or-hovers-near-rest) | Arm creeps or hovers near rest | ✅ Verified (bridge v2) |
| [T11](#t11-arm-reaches-the-cube-but-does-not-grasp) | Arm reaches but does not grasp | ⏳ Open |
| [T12](#t12-host-training-fails-dataset-format-or-camera-names) | Host training fails (format / camera names) | 🟡 Reported fixed |
| [T13](#t13-resume-ends-immediately-with-end-of-training) | Resume ends immediately | ✅ Expected behaviour |
| [T14](#t14-torchcodec-not-available-warning) | `torchcodec` not available warning | ℹ️ Harmless |
| [T15](#t15-ros-nodes-do-not-see-each-other) | ROS nodes do not see each other | General guidance |

---

### T1. "No status packet" and missing motor IDs

- **Symptoms:** Feetech reads fail with "No status packet"; motor scans find only some IDs; the failures are intermittent.
- **Cause:** (a) a chain of USB 2.0 hubs repeatedly reset and dropped the CH34x adapters (and the gripper camera); (b) two programs opened the same serial port at once.
- **Diagnostics:**
  ```bash
  # [HOST]
  sudo dmesg -w | grep -iE "usb|ch34|reset|disconnect"
  ls -l /dev/serial/by-id/
  sudo lsof /dev/ttyUSB* /dev/ttyACM* 2>/dev/null   # who has the port open?
  ```
- **Fix:** One program per serial port (✅ verified). Move the adapters off the hub chain to direct motherboard ports (⏳ planned).
- **Verification:** All 12 motors respond; mirroring runs without dropouts.
- **Lesson:** Intermittent communication errors usually come from power, cabling or port contention, not from firmware or code.

### T2. Gripper camera crashes on start (gamma)

- **Symptoms:** `v4l2_camera` exits while applying parameters.
- **Cause:** The camera reports a default gamma of 300, which is outside its own valid range of 90–150.
- **Diagnostics:** `v4l2-ctl -d <device> --list-ctrls | grep -i gamma`
- **Fix (✅ verified):** Always launch with `gamma:=100` (built into `start_cameras.sh`).
- **Lesson:** Cheap UVC cameras can report invalid defaults, so read the control ranges.

### T3. Cameras swapped after replugging

- **Symptoms:** The scene and gripper images appear on the wrong topics.
- **Cause:** `/dev/videoN` numbering depends on enumeration order.
- **Diagnostics:** `ls -l /dev/v4l/by-id/ /dev/v4l/by-path/`; `v4l2-ctl --list-devices`
- **Fix (✅ verified):** Address the cameras by `by-id` / `by-path`, and use `find_femto.sh` for the Femto Bolt.
- **Verification:** View both topics, or a recorded episode in the dataset viewer, and confirm which camera is which.
- **Lesson:** A swapped camera silently corrupts a dataset. Check one episode in the viewer after every session.

### T4. Femto Bolt crash with Y16 encoding error

- **Symptoms:** The Femto Bolt node crashes with an encoding error mentioning `Y16`.
- **Cause:** The script opened the depth node (16-bit greyscale) instead of the colour node.
- **Diagnostics:** `v4l2-ctl -d /dev/videoN --list-formats` for each Femto node.
- **Fix (✅ verified):** Select the node that offers `YUYV`.
- **Lesson:** RGB-D cameras expose several V4L2 nodes; select a node by its format, not by its index.

### T5. Femto Bolt not detected

- **Symptoms:** No Femto Bolt nodes appear in `v4l2-ctl --list-devices`.
- **Cause:** The camera was not connected, or not sufficiently powered.
- **Fix (✅ verified):** Reconnect it to a USB 3 port with its own power supply.
- **Lesson:** Depth cameras need USB 3 bandwidth and stable power.

### T6. Dataset "not found" in training or viewer

- **Symptoms:** Training and the dataset viewer report the dataset as missing.
- **Cause:** The selected folder was empty; the real repo ID has the `s101_dataset_` prefix.
- **Diagnostics:** `ls ~/.cache/huggingface/lerobot/NandithaaaG/`, then compare with the repo name on the Hub page.
- **Fix (✅ verified):** Use `NandithaaaG/s101_dataset_pick_and_place`.
- **Lesson:** Copy repo IDs from the Hub page instead of retyping them.

### T7. Training interrupted by a power cut

- **Symptoms:** Run 1 stopped at about 8,000 steps; checkpoint `008000` contained 0-byte files.
- **Cause:** Power was lost while the checkpoint was being written.
- **Diagnostics:** `find checkpoints/008000 -size 0`
- **Fix (✅ verified):** Resume from the last intact checkpoint (`006000`). Procedure: [smolvla-training.md](smolvla-training.md#recovering-from-a-corrupted-checkpoint).
- **Lesson:** Check checkpoint integrity after any crash, and use a UPS for long runs.

### T8. Web UI cannot resume training

- **Symptoms:** The resume option in the Physical AI Tools web UI fails.
- **Cause:** A path check on the page side (details not recorded).
- **Fix (✅ workaround verified):** Resume from the command line with `--config_path=.../checkpoints/last/pretrained_model/train_config.json --resume=true`.
- **Lesson:** Know the CLI underneath every GUI.

### T9. Model runs but the arm does not move

- **Symptoms:** Inference runs without errors, but the follower stays still or follows the leader.
- **Cause:** `bridge.py` (teleoperation) was still running and commanding the follower. Before `inference_bridge.py` existed, no node turned the policy's actions into servo commands at all.
- **Diagnostics:**
  ```bash
  # [CONTAINER]
  ros2 node list
  ros2 topic info -v /leader/joint_trajectory   # who publishes, who subscribes?
  pgrep -af bridge.py
  ```
- **Fix (✅ verified):** Stop `bridge.py`, then run `inference_bridge.py`.
- **Lesson:** When an action topic is shared, exactly one publisher must be active.

### T10. Arm creeps or hovers near rest

- **Symptoms:** The arm barely leaves rest and drifts slowly toward the tray.
- **Cause:** v1 rate-limited each goal to ±2 units around the **measured** position. Under gravity the servos lagged, so the arm made almost no progress and the model kept seeing a static scene.
- **Fix (✅ verified):** `inference_bridge.py` v2 rate-limits relative to the previous **commanded goal** and separately caps the distance from the arm.
- **Verification:** In attempt 3 the arm reached the cube.
- **Lesson:** Controller wrappers change the closed-loop dynamics the policy experiences; they must not distort the motion the policy expects.

### T11. Arm reaches the cube but does not grasp

- **Symptoms:** The gripper is positioned over the cube, then hovers and never closes.
- **Likely causes (inferred, untested):** extra red cubes in view; a different gripper-camera colour (auto white balance); an inference episode that is too short; long open-loop chunks (`n_action_steps = 50`); limited training samples; possible clipping of gripper commands by the bridge.
- **Diagnostics:** Log the predicted gripper action over time (does the model ask to close?). Compare a live gripper frame with a training frame side by side. Check the bridge logs for clipping.
- **Planned fix:** Match conditions ([inference.md](inference.md#matching-inference-to-training-conditions)), then test the hypotheses one at a time.
- **Lesson:** Change one variable per test, or you will not know what fixed it.

### T12. Host training fails (dataset format or camera names)

- **Symptoms:** `lerobot-train` (0.6.2) rejects the dataset or complains about missing image features.
- **Cause:** (a) the dataset is v2.1, but LeRobot 0.6.2 requires v3.0; (b) `smolvla_base` expects `camera1/2/3`, not `global`/`gripper`.
- **Fix (🟡 reported working):** Convert v2.1 → v3.0 locally **without pushing**, then pass a `rename_map` and `empty_cameras=1`.
- **Lesson:** Read the converter's `--help` before running it; some versions push to the Hub by default.

### T13. Resume ends immediately with "End of training"

- **Symptoms:** `--resume=true` loads everything, then prints "End of training" (observed on 20 Oct).
- **Cause:** The run had already reached `steps=20000`.
- **Fix:** None needed. To extend the run, pass a higher `--steps`.

### T14. "torchcodec not available" warning

- **Symptoms:** `'torchcodec' is not available in your platform, falling back to 'pyav'`.
- **Cause:** The container lacks a compatible `torchcodec` build.
- **Impact:** Harmless; video decoding is slower with `pyav`.

### T15. ROS nodes do not see each other

- **Checks:** Use the same `RMW_IMPLEMENTATION` (`rmw_zenoh_cpp`) and `ROS_DOMAIN_ID` (30) in every terminal. If your Zenoh setup uses a router, it must be running. `ros2 topic list` should show the expected topics.
- **Status:** General guidance; no specific incident was recorded.
