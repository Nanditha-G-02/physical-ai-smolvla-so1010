# Literature Review: From Behavioral Cloning to Small Vision-Language-Action Models

*A narrative review written for this project. The interpretations are the author's; the citations are in [references.bib](references.bib).*

## Contents
1. [Scope](#1-scope)
2. [Learning from demonstrations](#2-learning-from-demonstrations)
3. [Better action representations](#3-better-action-representations)
4. [Scaling data and models: RT-1 to Open X-Embodiment](#4-scaling-data-and-models-rt-1-to-open-x-embodiment)
5. [Vision-language-action models](#5-vision-language-action-models)
6. [Small, open, affordable: SmolVLA and LeRobot](#6-small-open-affordable-smolvla-and-lerobot)
7. [What matters in the data](#7-what-matters-in-the-data)
8. [How to evaluate](#8-how-to-evaluate)
9. [Implications for this project](#9-implications-for-this-project)
10. [Open questions](#10-open-questions)

## 1. Scope

This review traces the ideas that make it possible to fine-tune a 450M-parameter VLA on 39 demonstrations from a $300-class robot arm: behavioral cloning, action chunking, generative action models, VLM-based policies, community data, and evaluation methodology. It focuses on manipulation from RGB images and proprioception.

## 2. Learning from demonstrations

Behavioral cloning (BC) treats control as supervised learning on expert observation–action pairs. ALVINN (Pomerleau, 1988) steered a vehicle from camera images this way. Its central weakness was formalized by Ross and Bagnell (2010) and Ross, Gordon and Bagnell (2011): because the learner's own mistakes take it to states the expert never visited, errors compound over the horizon. DAgger addressed this by iteratively labelling the learner's own states. Deep visuomotor learning (Levine et al., 2016) showed that convolutional networks could map raw pixels to motor torques for real manipulation, making image-based BC practical.

*Takeaway:* BC is simple and data-efficient but fragile out of distribution; covering the states the policy will actually reach is essential.

## 3. Better action representations

Two ideas from 2023 changed what small-data BC can achieve.

**Action chunking (ACT; Zhao et al., 2023).** Predicting a sequence of future actions instead of one reduces the number of decisions per episode and lets the model represent temporally extended motions, including pauses that confuse single-step policies. Combined with a CVAE and temporal ensembling, ACT learned fine bimanual tasks from about 50 demonstrations on low-cost ALOHA hardware, which itself made leader–follower teleoperation widely affordable.

**Generative action models (Diffusion Policy; Chi et al., 2023).** Representing the action distribution with a denoising diffusion model handles multimodal demonstrations without averaging modes and works well with action sequences. Flow matching (Lipman et al., 2023) offers a closely related, often cheaper training objective, later adopted by π0 and SmolVLA.

*Takeaway:* chunked, generative action heads are now the default for manipulation policies.

## 4. Scaling data and models: RT-1 to Open X-Embodiment

RT-1 (Brohan et al., 2023) showed that a transformer trained on ~130k real episodes across hundreds of instructions generalizes to new instructions and distractors, and that data diversity matters. The Open X-Embodiment collaboration (2024) pooled over a million trajectories from 22 robot types and showed positive transfer across embodiments. Octo (2024) released an open generalist policy trained on this data and designed for fine-tuning.

*Takeaway:* broad pretraining data helps, but it was assembled from expensive lab robots, and models trained on it are not tuned for low-cost arms.

## 5. Vision-language-action models

RT-2 (2023) fine-tuned web-scale VLMs to emit robot actions as text tokens and showed that semantic knowledge from web data transfers to control. OpenVLA (Kim et al., 2024) made a 7B VLA fully open and showed that LoRA fine-tuning on consumer GPUs is viable. π0 (Black et al., 2024) separated perception (a VLM) from action generation (a flow-matching expert producing continuous chunks), reaching high-frequency dexterous control.

*Takeaway:* VLAs combine the semantic generality of VLMs with the action machinery of section 3. Their size, however, puts them out of reach of small labs.

## 6. Small, open, affordable: SmolVLA and LeRobot

SmolVLA (Shukor et al., 2025) compresses the π0 recipe: a small SmolVLM-2 backbone using only half its layers and 64 tokens per image, plus a ~100M flow-matching expert with interleaved cross/self-attention. It is pretrained not on lab data but on 481 community datasets recorded with low-cost arms. The authors report performance comparable to π0 at a fraction of the size, a large gain from community pretraining, and faster execution with asynchronous inference.

LeRobot (Cadene et al., 2026) provides the surrounding infrastructure: hardware drivers for SO-100/101, a Hub-native dataset format, policy implementations, and deployment tools. Together they are what make this project feasible on an RTX 3050.

## 7. What matters in the data

robomimic (Mandlekar et al., 2021) found that operator proficiency and demonstration consistency strongly affect results, and that the lowest-validation-loss checkpoint is often not the best performer. Lin et al. (2025) found that generalization scales roughly as a power law in the number of environments and objects, with diminishing returns from repeating demonstrations in the same conditions. The SmolVLA guide's practical advice (≈ 50 episodes, several per variation) is consistent with both.

## 8. How to evaluate

Kress-Gazit et al. (2024) argue that single success rates over a few trials, with unreported conditions, are not scientific evidence. They recommend explicit conditions, complementary metrics, statistical analysis and qualitative failure analysis. Sequential testing (STEP, 2025) can reduce the number of trials needed to compare policies.

## 9. Implications for this project

| Literature finding | Implication | Status |
|--------------------|-------------|--------|
| Compounding errors in BC | Expect drift in rare, precise phases such as the grasp | Observed: reach without grasp |
| Pretraining on similar robots helps small datasets | Fine-tune from `smolvla_base` | Done in Run 2; unverified in Run 1 |
| ~50 demos, several per variation | Record more episodes with logged positions | Planned |
| Diversity beats repetition | Add positions and objects before repetitions | Planned |
| Chunk execution affects reactivity | Try a shorter `n_action_steps` | Planned |
| Evaluate with protocol and statistics | Use the evaluation protocol before claiming success | Protocol written |
| Lowest loss ≠ best policy | Select checkpoints on the robot | Planned |

## 10. Open questions

1. How much of the grasp failure is distribution shift (scene, colour) versus under-training versus open-loop execution? Controlled experiments can separate them.
2. Does the language channel help at all in a single-task setting? Testing with paraphrased or irrelevant instructions would show it.
3. Would a small ACT baseline match SmolVLA on this specific task and data budget? The SmolVLA paper suggests not, but it used more data per task.
