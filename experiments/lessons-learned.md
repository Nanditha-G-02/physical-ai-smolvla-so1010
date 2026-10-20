# Lessons Learned

Grouped by area. Each lesson comes from something that actually happened in the project.

## Hardware and systems

1. **USB topology is a first-class design decision.** A chain of USB 2.0 hubs caused intermittent "No status packet" errors and camera dropouts. Check `dmesg` before debugging code.
2. **One program per serial port.** Two processes on one Feetech bus produce garbage that looks like a motor fault.
3. **Use stable device names everywhere** (`/dev/serial/by-id`, `/dev/v4l/by-id`). Enumeration order changed between reboots and swapped the cameras.
4. **Read the camera's control ranges.** A default gamma outside the camera's own valid range crashed the driver.
5. **RGB-D cameras expose several nodes.** Choose by pixel format (YUYV), not by index.
6. **Protect long jobs from power loss.** A power cut corrupted a checkpoint; a UPS and integrity checks are cheap insurance.

## Data

7. **Log variations when you record them.** Cube and tray positions were not logged, so in- and out-of-distribution tests cannot be defined after the fact.
8. **Lock automatic camera settings** before recording and reuse them at inference.
9. **Copy repo IDs from the Hub.** A missing prefix produced "dataset not found".
10. **Keep the dataset format the container needs.** Convert locally for the newer LeRobot; never push over the v2.1 copy while the container still reads it.

## Training

11. **Count samples, not steps.** 20k steps at batch 2 is under 2 passes over the data, versus about 55 in the reference recipe.
12. **Know your initialization.** Whether training started from `smolvla_base` is the single most important unknown of Run 1.
13. **Read the whole config.** Augmentation was off and the LR schedule outlasted the run; both were visible in the config dump.
14. **GUIs hide failure modes.** When the web UI could not resume, the CLI could.

## Deployment

15. **Exactly one publisher per action topic.** The model "did nothing" because the teleop bridge was still in control.
16. **Rate-limit goals, not measured positions.** Limiting around the measured position, under gravity, froze the arm and fooled the model.
17. **Offline success ≠ robot success.** 2–5 units of offline error coexisted with zero grasps.
18. **Match the training scene.** Extra cubes and a different camera colour are enough to change behaviour.
19. **Change one variable at a time** when debugging on the robot.

## Process

20. **Label evidence.** Separating verified, reported and planned items made it clear what is actually known and what still needs a test.
