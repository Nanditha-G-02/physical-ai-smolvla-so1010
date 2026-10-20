# Hardware Setup

## Contents
- [Bill of materials](#bill-of-materials)
- [Robot arms and joints](#robot-arms-and-joints)
- [Motor interfaces and serial ports](#motor-interfaces-and-serial-ports)
- [USB topology: what went wrong and what to do](#usb-topology-what-went-wrong-and-what-to-do)
- [Cameras](#cameras)
- [Compute](#compute)
- [Calibration](#calibration)
- [Status](#status)

## Bill of materials

| Item | Qty | Verified detail |
|------|-----|-----------------|
| SO-ARM101 arm kit (leader + follower) | 1 pair | 6 joints per arm |
| Feetech STS3215 serial bus servos (model number 777 as reported by the bus) | 12 | 1 Mbps bus |
| CH34x USB–serial driver boards | 2 | USB vendor:product `1a86:55d3` |
| Orbbec Femto Bolt (model F00364-152) | 1 | Colour stream 1280×720 used; depth (Y16) unused |
| USB gripper camera ("HZ") | 1 | 640×480 |
| PC: MSI MS-7C95 motherboard, NVIDIA RTX 3050 6 GB | 1 | Ubuntu |
| Red cube, tray | — | Task objects |

The SO-ARM100/101 is an open-source, 3D-printable arm design by TheRobotStudio, integrated into LeRobot ([SO-ARM100 repository](https://github.com/TheRobotStudio/SO-ARM100), [LeRobot SO-101 guide](https://huggingface.co/docs/lerobot/so101)).

## Robot arms and joints

Both arms share the same kinematic layout. The joint order below is the order used in `observation.state` and `action` in the dataset (verified from `meta/info.json`):

| Index | Joint | Function in pick-and-place |
|-------|-------|---------------------------|
| 0 | `shoulder_pan` | Rotates the arm toward the cube or the tray |
| 1 | `shoulder_lift` | Raises / lowers the upper arm |
| 2 | `elbow_flex` | Extends / retracts the forearm |
| 3 | `wrist_flex` | Pitches the gripper toward the table |
| 4 | `wrist_roll` | Aligns the jaws with the cube's faces |
| 5 | `gripper` | Opens / closes the jaws |

The **leader** arm is moved by hand and acts as a joint-space input device. The **follower** arm reproduces the leader's joint positions. Because both arms have the same geometry, no inverse kinematics is needed: the action is simply "go to these six joint positions".

## Motor interfaces and serial ports

| Arm | Board serial number | Role |
|-----|---------------------|------|
| Follower | `5A7C120749` | Receives position goals; reports measured positions |
| Leader | `5B14111828` | Read-only during teleoperation (torque off so it can be moved by hand) |

Use the stable symlinks under `/dev/serial/by-id/` rather than `/dev/ttyACM*` / `/dev/ttyUSB*`, whose numbers change when devices are replugged:

```bash
# [HOST] List serial adapters by stable ID
ls -l /dev/serial/by-id/
# [HOST] Confirm both CH34x boards are enumerated
lsusb | grep -i 1a86:55d3
```

**Rule learned the hard way: one program per serial port.** If `bridge.py`, a calibration script and the Physical AI server all try to open the same port, packets collide and the servos stop answering ("No status packet"). See [troubleshooting T1](troubleshooting.md#t1-no-status-packet-and-missing-motor-ids).

## USB topology: what went wrong and what to do

The adapters and the gripper camera were originally connected through a **chain of USB 2.0 hubs**. The hubs repeatedly reset, which dropped the serial adapters and the camera mid-session. Symptoms were intermittent missing motor IDs and cameras disappearing.

| Recommendation | Status |
|----------------|--------|
| Connect each motor adapter directly to a motherboard USB port | ⏳ Planned |
| Put the Femto Bolt on a USB 3 port with its own power supply | ✅ Done |
| Avoid daisy-chained, unpowered hubs for the gripper camera | ⏳ Planned |
| Use a UPS to protect long training runs from power cuts | ⏳ Planned (a power cut corrupted checkpoint `008000`) |

Diagnosing hub resets:

```bash
# [HOST] Watch the kernel log while reproducing the problem
sudo dmesg -w | grep -iE "usb|ch34|disconnect|reset"
```

Repeated `USB disconnect` / `reset high-speed USB device` lines for the adapters indicate a power or hub problem, not a software problem.

## Cameras

| Camera | Stream used | Resolution | Dataset key |
|--------|-------------|------------|-------------|
| Orbbec Femto Bolt | Colour (YUYV via V4L2) | 1280×720 | `observation.images.global` |
| Gripper camera | Colour | 640×480 | `observation.images.gripper` |

Configuration details, device naming and fixes: [camera-integration.md](camera-integration.md).

## Compute

| Item | Verified value |
|------|----------------|
| GPU | NVIDIA GeForce RTX 3050, 6144 MiB |
| Idle GPU use (desktop only) | 660 MiB |
| Run 2 training footprint | ≈ 2.5 GB at batch size 4 (reported) |
| PyTorch | 2.11.0+cu130 (host) |

## Calibration

Calibration maps each servo's raw encoder range to a consistent joint range so that the leader and follower agree.

| Item | Status |
|------|--------|
| Motor IDs 1–6 respond on both buses | ✅ Verified ("all 12 motors respond") |
| Leader and follower agree after calibration (mirroring works) | ✅ Verified |
| Exact calibration procedure, tool and calibration files | ❌ Not recorded in the project history |

If you are reproducing this setup with LeRobot's own tooling, the official SO-101 guide covers motor ID setup and calibration ([LeRobot SO-101 docs](https://huggingface.co/docs/lerobot/so101)). Those commands talk to the servos directly, so stop every ROS bridge first. See [tutorial 02](../tutorials/02-connect-and-calibrate-so101.md).

> **Important for learning:** The dataset's state and action values are in whatever units the recording pipeline produced (reported offline errors of "2–5 units"). Re-calibrating the arms after recording changes the meaning of those numbers and silently breaks a trained policy. Record the calibration files alongside each dataset.

## Status

| Item | Level |
|------|-------|
| 12 motors respond, mirroring works | ✅ Tested |
| Cameras stream at 30 Hz | ✅ Tested |
| USB topology fixed permanently | ⏳ Planned |
| Calibration procedure documented | ❌ Missing |
