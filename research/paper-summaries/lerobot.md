# LeRobot (Cadene et al., ICLR 2026)

**LeRobot: An Open-Source Library for End-to-End Robot Learning.** Remi Cadene and 16 co-authors (Hugging Face). arXiv:2602.22818 (February 2026); published at ICLR 2026. **Status:** peer-reviewed conference paper. [arXiv](https://arxiv.org/abs/2602.22818) · [GitHub](https://github.com/huggingface/lerobot) · [docs](https://huggingface.co/docs/lerobot)

## Problem

Robot-learning work is slowed by fragmented, often closed tools that each cover only part of the pipeline: motor drivers, data collection, storage, training, deployment.

## Contribution (in our words)

LeRobot is a vertically integrated, open-source stack:

- **Hardware integration:** a unified robot/teleoperator interface for low-cost platforms such as SO-100/101 and ALOHA, extensible to new robots.
- **Datasets:** LeRobotDataset, a standard format for multimodal time series (Parquet for low-dimensional signals, MP4 for video, JSON/Parquet metadata), hosted and streamable on the Hugging Face Hub.
- **Policies:** PyTorch implementations of imitation-learning, reinforcement-learning and VLA policies (ACT, Diffusion Policy, π0, SmolVLA and others).
- **Inference:** a generalized asynchronous inference stack.
- **Philosophy:** prefer scalable, learning-based methods that improve with more data and compute over hand-crafted pipelines, and lower the cost of entry with affordable hardware.

## Relevance to this project

| LeRobot component | Use here |
|-------------------|----------|
| LeRobotDataset v2.1 | Format of the recorded dataset (via Physical AI Tools) |
| LeRobotDataset v3.0 | Format required by the host's LeRobot 0.6.2; converted locally |
| SmolVLA policy + `lerobot/smolvla_base` | The fine-tuned model |
| `lerobot-train` / `python -m lerobot.scripts.train` | Training in the host and container respectively |
| `lerobot-rollout` | Installed; planned for host-side inference |
| SO-101 drivers | Not used directly (the arms are driven through custom ROS bridges) |

## Notes

The library evolves quickly: commands, flags and dataset formats changed between the version bundled with Physical AI Tools and 0.6.2. Always check `--help` in the installed version.
