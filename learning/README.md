# Learning Guides

These guides explain the science behind each part of the project. Each one follows the same structure: what the topic is, why it matters here, core concepts (with maths where it helps), what the key papers found, how the research maps onto this project, limitations, lessons, and further reading.

> **Research vs this project.** Paper results are reported as the authors' findings. What was actually built and tested in this project is always marked separately ("In this project"). Where a guide offers an interpretation of a failure seen here, it is labelled as an interpretation.

## Reading order

| # | Guide | Covers topics |
|---|-------|---------------|
| 1 | [Physical AI and embodied intelligence](physical-ai-and-embodied-intelligence.md) | Physical AI, embodiment, the perception–action loop, sim-to-real |
| 2 | [Robot teleoperation, state and actions](robot-teleoperation.md) | Leader–follower teleoperation, joint space, state vs action, control loops |
| 3 | [Imitation learning and behavioral cloning](imitation-learning-and-behavioral-cloning.md) | Imitation learning, behavioral cloning, covariate shift, DAgger, multimodality |
| 4 | [Action chunking](action-chunking.md) | Action chunks, temporal ensembling, execution horizon, asynchronous inference |
| 5 | [Vision-based manipulation](vision-based-manipulation.md) | Multimodal observations, wrist cameras, camera calibration and coordinate frames |
| 6 | [Dataset design and generalization](dataset-design-and-generalization.md) | Demonstration collection, data quality and diversity, overfitting, generalization to unseen positions |
| 7 | [Vision-language-action models](vision-language-action-models.md) | RT-1, RT-2, OpenVLA, π0, Octo: how VLAs evolved |
| 8 | [SmolVLA architecture](smolvla-architecture.md) | SmolVLM-2 backbone, layer skipping, flow-matching action expert, community pretraining |
| 9 | [Training and fine-tuning](training-and-fine-tuning.md) | Fine-tuning on limited GPU memory, normalization, schedules, PEFT |
| 10 | [Evaluation metrics](evaluation-metrics.md) | Loss vs success, success rate, statistics, failure taxonomies |

## Topic coverage map

The project brief listed 18 topics. This is where each one is covered:

| Topic | Guide |
|-------|-------|
| Physical AI and embodied intelligence | [1](physical-ai-and-embodied-intelligence.md) |
| Vision-language-action models | [7](vision-language-action-models.md) |
| SmolVLA architecture and training | [8](smolvla-architecture.md), [9](training-and-fine-tuning.md) |
| LeRobot architecture and workflows | [7](vision-language-action-models.md#the-lerobot-ecosystem), [research summary](../research/paper-summaries/lerobot.md) |
| Imitation learning; behavioral cloning | [3](imitation-learning-and-behavioral-cloning.md) |
| Robot demonstration collection | [2](robot-teleoperation.md), [6](dataset-design-and-generalization.md) |
| Dataset quality and distribution | [6](dataset-design-and-generalization.md) |
| Action chunking and temporal prediction | [4](action-chunking.md) |
| Vision-based manipulation; multimodal observations | [5](vision-based-manipulation.md) |
| Camera calibration and coordinate frames | [5](vision-based-manipulation.md#camera-calibration-and-coordinate-frames) |
| Robot teleoperation | [2](robot-teleoperation.md) |
| Sim-to-real transfer | [1](physical-ai-and-embodied-intelligence.md#sim-to-real-and-why-this-project-skipped-simulation) |
| Generalization; data diversity and overfitting | [6](dataset-design-and-generalization.md) |
| Evaluation of manipulation policies | [10](evaluation-metrics.md) |
| Efficient fine-tuning on limited GPU memory | [9](training-and-fine-tuning.md) |

All citations resolve to [research/references.bib](../research/references.bib).
