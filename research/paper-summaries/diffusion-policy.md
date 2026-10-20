# Diffusion Policy (Chi et al., RSS 2023)

**Diffusion Policy: Visuomotor Policy Learning via Action Diffusion.** Cheng Chi, Siyuan Feng, Yilun Du, Zhenjia Xu, Eric Cousineau, Benjamin Burchfiel, Shuran Song. Robotics: Science and Systems 2023; extended version in the International Journal of Robotics Research (2024). arXiv:2303.04137. **Status:** peer-reviewed. [arXiv](https://arxiv.org/abs/2303.04137)

## Problem

Human demonstrations are multimodal: the same situation can be handled in several valid ways. Policies trained with regression (MSE) average these modes, producing invalid actions. Policies that discretize actions lose precision.

## Contribution (in our words)

- Represent the policy as a **conditional denoising diffusion model** over action sequences: start from noise and iteratively denoise into an action sequence, conditioned on visual observations.
- Predict a **sequence of future actions** (receding-horizon control): execute part of it, then re-plan from a new observation.
- Engineering choices for real robots: visual conditioning, a time-series transformer or CNN backbone, and position (not velocity) action spaces.
- Across many simulated and real manipulation tasks, the authors report consistent gains over prior behavioral-cloning methods, especially on multimodal tasks.

## Relation to flow matching

Flow matching (used by π0 and SmolVLA) is closely related to diffusion: both learn to transform noise into data. Flow matching regresses a velocity field along a simple (often straight) path and typically needs fewer integration steps at inference. SmolVLA uses 10.

## Relevance to this project

- It explains why SmolVLA uses a generative action expert rather than direct regression; the SmolVLA paper's ablation found flow matching better than regression.
- Receding-horizon execution is the alternative to this project's full-chunk execution (`n_action_steps = 50`); see [action chunking](../../learning/action-chunking.md).
- Diffusion Policy is also available in LeRobot as a possible baseline.
