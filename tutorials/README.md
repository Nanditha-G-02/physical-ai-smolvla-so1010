# Tutorials

Numbered, hands-on walkthroughs. Each command block is labelled **[HOST]** (Ubuntu shell, conda env `lerobot`) or **[CONTAINER]** (inside the Physical AI Tools Docker container). Each tutorial states which steps were verified in this project and which are references or reconstructions.

| # | Tutorial | Verified in project? |
|---|----------|----------------------|
| 01 | [Environment setup](01-environment-setup.md) | ✅ Checks; install commands are a reference |
| 02 | [Connect and calibrate the SO-101](02-connect-and-calibrate-so101.md) | ✅ Connection; calibration is a LeRobot reference |
| 03 | [Teleoperate](03-teleoperate.md) | ✅ |
| 04 | [Record a dataset](04-record-dataset.md) | ✅ Workflow; UI details not recorded |
| 05 | [Inspect and convert the dataset](05-inspect-and-convert-dataset.md) | ✅ Download/inspect; conversion flags pending |
| 06 | [Train SmolVLA](06-train-smolvla.md) | 🟡 Run 2 command reconstructed |
| 07 | [Resume and manage checkpoints](07-resume-and-manage-checkpoints.md) | ✅ Resume; 🔧 recovery reconstructed |
| 08 | [Run inference](08-run-inference.md) | 🟡 Reaches the cube; no grasp yet |

The original brief proposed ten tutorials; calibration was merged with connection (02), and resuming, loading and checkpoint management were merged into 07, because the project history did not contain enough material to fill them separately.
