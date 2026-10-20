# Experiments

| Path | Contents |
|------|----------|
| [experiment-log.md](experiment-log.md) | Structured table for every training run and inference experiment, plus planned experiments |
| [lessons-learned.md](lessons-learned.md) | What the project taught, grouped by area |
| [training-configs/run1_container_train_config.json](training-configs/run1_container_train_config.json) | Run 1 configuration, reconstructed from the verified config dump |
| [training-configs/run2_host_lerobot062.md](training-configs/run2_host_lerobot062.md) | Run 2 settings and reconstructed command |
| [evaluation-results/](evaluation-results/) | Trial log template and evaluation results (none measured yet) |

## Rules

- Never paste invented numbers. If a value was not measured, write **Not measured**.
- Training logs and plots belong here; checkpoints and videos do not (they are blocked by `.gitignore`; link to the Hugging Face Hub or local storage instead).
- Every run entry should list: command, LeRobot version, dataset repo and revision, initialization, batch size, steps, LR schedule, final loss, checkpoint path, and evaluation results.
