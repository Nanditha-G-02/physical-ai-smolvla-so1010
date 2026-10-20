# Tutorial 02 — Connect and Calibrate the SO-101

**Goal:** both arms enumerated with stable names, all 12 motors answering, arms calibrated.
**Evidence:** the connection checks reflect the project's verified state ("all 12 motors respond"). The project's own calibration procedure **was not recorded**, so step 4 uses the official LeRobot tooling as a reference.

## 1. Plug in directly, not through a hub chain

Connect each CH34x board to a motherboard USB port. A chain of USB 2.0 hubs caused repeated disconnects in this project ([T1](../docs/troubleshooting.md#t1-no-status-packet-and-missing-motor-ids)).

## 2. Find stable device names

```bash
# [HOST]
lsusb | grep -i 1a86:55d3        # expect two lines (leader and follower boards)
ls -l /dev/serial/by-id/          # note the symlink for each board
```

Identify which is which by unplugging one board and listing again. In this project: follower board serial `5A7C120749`, leader `5B14111828`.

## 3. Make sure nothing else owns the ports

```bash
# [HOST]
sudo lsof /dev/ttyUSB* /dev/ttyACM* 2>/dev/null
pgrep -af "bridge.py|inference_bridge.py|lerobot"
```

Stop anything listed before continuing. **One program per serial port.**

## 4. Calibrate (reference: official LeRobot commands)

```bash
# [HOST] reference from the LeRobot SO-101 docs; not the procedure recorded in this project
lerobot-calibrate --robot.type=so101_follower --robot.port=/dev/serial/by-id/<follower> --robot.id=so101_follower
lerobot-calibrate --teleop.type=so101_leader --teleop.port=/dev/serial/by-id/<leader> --teleop.id=so101_leader
```

Check flag names with `lerobot-calibrate --help` in your version. Motor ID assignment for new arms is covered by `lerobot-setup-motors` in the [SO-101 guide](https://huggingface.co/docs/lerobot/so101).

> ⚠️ **Calibration defines your action units.** If you recalibrate after recording a dataset, the joint values of new observations no longer match the dataset, and a trained policy will be mis-scaled. Save the calibration files next to each dataset.

## 5. Verify

Run the teleoperation of [tutorial 03](03-teleoperate.md) and confirm that every joint of the follower mirrors the leader across its full range, including the gripper.

## Next

[Tutorial 03 — Teleoperate](03-teleoperate.md)
