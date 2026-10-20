# RT-1 and RT-2 (Google, 2022–2023)

## RT-1

**RT-1: Robotics Transformer for Real-World Control at Scale.** Anthony Brohan et al. Robotics: Science and Systems 2023. arXiv:2212.06817. **Status:** peer-reviewed. [arXiv](https://arxiv.org/abs/2212.06817)

**In our words.** RT-1 is a transformer trained from scratch on a large real-robot dataset (about 130k episodes covering 700+ instructions, collected with a fleet of mobile manipulators). Images pass through an EfficientNet conditioned on the instruction embedding (FiLM), are compressed into a small set of tokens (TokenLearner), and a transformer outputs **discretized** actions (each dimension binned into 256 values). The authors report strong generalization to new instructions, distractors and backgrounds compared with earlier baselines, and that data diversity mattered more than data quantity in their ablations.

**Why it matters here.** RT-1 established the "images + instruction → transformer → discrete actions" template and the importance of diverse real-world data, at a scale (~130k episodes) far beyond a single-person project.

## RT-2

**RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control.** Conference on Robot Learning 2023 (PMLR 229); arXiv:2307.15818. The arXiv version lists Anthony Brohan et al.; the PMLR version lists Brianna Zitkovich, Tianhe Yu et al. **Status:** peer-reviewed. [arXiv](https://arxiv.org/abs/2307.15818)

**In our words.** RT-2 takes large pretrained vision-language models (PaLI-X and PaLM-E, up to 55B parameters) and fine-tunes them jointly on web vision-language data and robot trajectories, with actions written as strings of discrete tokens. This lets the robot use web-scale semantic knowledge: the authors show instructions involving concepts never seen in robot data (for example, picking the object that matches a described category) and simple chain-of-thought reasoning. The paper popularized the term **vision-language-action model**.

**Why it matters here.** SmolVLA follows RT-2's core idea (start from a pretrained VLM) but makes three different choices: a tiny VLM, continuous actions via a flow-matching expert, and community data from low-cost arms.

## Limitations noted

Both models are large, proprietary in weights or data, and trained on robots and datasets unavailable to most labs. Discrete action tokens limit precision and speed.
