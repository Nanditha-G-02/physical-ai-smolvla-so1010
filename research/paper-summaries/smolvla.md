# SmolVLA (Shukor et al., 2025)

**SmolVLA: A Vision-Language-Action Model for Affordable and Efficient Robotics.** Mustafa Shukor, Dana Aubakirova, Francesco Capuano, Pepijn Kooijmans, Steven Palma, Adil Zouitine, Michel Aractingi, Caroline Pascal, Martino Russi, Andres Marafioti, Simon Alibert, Matthieu Cord, Thomas Wolf, Remi Cadene. arXiv:2506.01844, June 2025. **Status:** preprint. [arXiv](https://arxiv.org/abs/2506.01844) · [docs](https://huggingface.co/docs/lerobot/smolvla) · [model](https://huggingface.co/lerobot/smolvla_base)

## Problem

Existing VLAs have billions of parameters, need large compute, and are pretrained on academic or industrial datasets from expensive robots. The authors ask whether a small, open VLA trained on community data from low-cost arms can be competitive.

## Approach (in our words)

1. **Small backbone, cut in half.** SmolVLM-2 is used as the perception backbone, but only its first half of language-model layers; later layers are skipped. Each image is reduced to 64 visual tokens and the image is not tiled.
2. **Separate action expert.** A ~100M-parameter transformer generates a chunk of 50 continuous actions with flow matching, conditioned on the VLM's features. Its blocks alternate between cross-attention to the VLM features and causal self-attention among action tokens.
3. **Community pretraining.** 481 public LeRobot datasets (~22.9k episodes, ~10.6M frames), mostly from SO-100-class arms, are cleaned: task descriptions are regenerated with a VLM, and camera views are mapped to standard slots.
4. **Asynchronous inference.** Execution of the current action queue overlaps with computing the next chunk, triggered when the queue falls below a threshold.

## Reported findings

- Comparable to or better than much larger VLAs on LIBERO (87.3 % average at 0.45B) and Meta-World (57.3 %).
- On SO-100 real-world tasks, 78.3 % average versus 61.7 % for π0 and 48.3 % for ACT.
- On an SO-101 Lego pick-place task: 90 % in distribution, 50 % out of distribution.
- Community pretraining improved real-world average success from 51.7 % to 78.3 %.
- Ablations favour interleaved cross/self-attention, causal masking within the chunk, skipping layers of a larger VLM rather than using a smaller VLM, and flow matching over plain regression.
- Async inference finished tasks ~30 % faster at similar success.

## Real-world protocol details worth copying

- 50 demonstrations per task: 5 starting positions × 10 episodes.
- Partial-credit scoring: 0.5 for grasp, 0.5 for place.
- Synchronous inference (full chunk executed) for real-world evaluation.

## Relevance to this project

| Paper | This project |
|-------|-------------|
| 50 demos per task, 5 positions × 10 | 39 demos, positions not logged |
| Pretrained on community data | Run 2 started from `smolvla_base`; Run 1 unverified |
| Standard camera slots | Run 2 rename map `global→camera1`, `gripper→camera2` |
| Real-world fine-tuning for many steps | 20k steps at batch 2–4 |
| Partial-credit success rate | Adopted in the [evaluation protocol](../../docs/evaluation.md); not yet measured |

## Limitations (paper and our view)

The paper's real-world tests use a controlled lab setup with fixed boxes and few distractors. Out-of-distribution performance drops sharply. Results are from the authors' hardware and are not independently replicated here.
