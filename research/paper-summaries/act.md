# ACT and ALOHA (Zhao et al., RSS 2023)

**Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware.** Tony Z. Zhao, Vikash Kumar, Sergey Levine, Chelsea Finn. Robotics: Science and Systems 2023. arXiv:2304.13705. **Status:** peer-reviewed. [arXiv](https://arxiv.org/abs/2304.13705)

## Problem

Fine manipulation (threading, opening a cup lid, inserting a battery) traditionally needs expensive, precise robots and sensors. Can low-cost hardware plus learning do it?

## Contributions (in our words)

1. **ALOHA**, a low-cost bimanual leader–follower teleoperation system built from off-the-shelf servos and 3D-printed parts. Operators move leader arms; followers copy joint positions.
2. **ACT (Action Chunking with Transformers)**, a policy that:
   - predicts a **chunk** of *k* future actions from the current observation instead of one action;
   - is trained as a **conditional VAE** (CVAE) with a transformer encoder–decoder and ResNet image features, so it can model variability in human demonstrations;
   - uses **temporal ensembling** at inference: a new chunk is predicted every step and the overlapping predictions for the current step are averaged with exponential weights, giving smooth motion.
3. Results: high success rates on several fine-grained real-world tasks from roughly 50 demonstrations per task (about 10 minutes of data), as reported by the authors.

## Why chunking helps (authors' argument)

Predicting several steps at once shortens the effective decision horizon, reducing compounding errors, and makes it easier to model pauses and non-Markovian behaviour in human demonstrations.

## Relevance to this project

- The SO-ARM leader–follower kits follow the ALOHA idea at lower cost and in a single-arm form.
- SmolVLA inherits action chunking (chunk size 50).
- ACT is the standard small baseline in LeRobot. The SmolVLA paper reports ACT at 48.3 % average on its SO-100 tasks versus 78.3 % for SmolVLA, and ACT at 70 % / 40 % (in/out of distribution) on the SO-101 task.
- The author's earlier dataset (`NandithaaaG/grab_place_training`) was prepared for ACT. Training ACT on the current dataset is a planned baseline.

## Limitations

ACT is trained from scratch per task, with no language conditioning and no pretraining, so it typically needs task-specific data for each new task.
