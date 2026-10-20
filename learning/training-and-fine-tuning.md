# Training and Fine-Tuning on Limited GPU Memory

## Contents
- [Introduction](#introduction)
- [Why it matters here](#why-it-matters-here)
- [Where GPU memory goes](#where-gpu-memory-goes)
- [Techniques for small GPUs](#techniques-for-small-gpus)
- [Normalization](#normalization)
- [Learning-rate schedules](#learning-rate-schedules)
- [Samples seen, not just steps](#samples-seen-not-just-steps)
- [A suggested next run](#a-suggested-next-run)
- [Limitations](#limitations)
- [Further reading](#further-reading)

## Introduction

**Fine-tuning** adapts a pretrained model to a new task with a smaller dataset. For VLAs the standard recipe is to keep most of the pretrained model frozen and train a smaller set of parameters on the robot's demonstrations.

## Why it matters here

Training ran on an RTX 3050 with 6 GB of memory (660 MiB already used by the desktop). That forced batch sizes of 2–4 and shaped every other choice.

## Where GPU memory goes

| Component | Scales with | SmolVLA (frozen VLM) |
|-----------|------------|----------------------|
| Model weights | All parameters (450M) | ~1.8 GB in fp32; ~0.9 GB in bf16 |
| Gradients | Trainable parameters (~100M) | ~0.4 GB fp32 |
| Adam optimizer state | 2 × trainable parameters | ~0.8 GB fp32 |
| Activations | Batch size × sequence length × layers | Grows linearly with batch |

These are back-of-the-envelope figures, not measurements. Freezing the VLM is what makes training possible here: only ~22 % of the parameters need gradients and optimizer state. The observed ≈ 2.5 GB at batch 4 (Run 2) is consistent with this.

## Techniques for small GPUs

| Technique | What it does | Trade-off | Status here |
|-----------|--------------|-----------|-------------|
| Freeze backbone | Train only the action expert | Less adaptation of perception | ✅ Default |
| Small batch | Fewer activations | Noisier gradients; fewer samples per step | ✅ 2 / 4 |
| Mixed precision (bf16/fp16) | Halves activation and weight memory; faster on tensor cores | Rare numerical issues | ❌ `use_amp: false` |
| Gradient accumulation | Sum gradients over *k* micro-batches before stepping | *k*× slower per optimizer step | ❌ Check support in your version |
| Gradient checkpointing | Recompute activations in the backward pass | ~30 % slower | ❌ |
| LoRA / PEFT | Train low-rank adapters instead of full weights ([Hu et al., 2022](../research/references.bib)) | Lower capacity | ❌ LeRobot documents PEFT training |
| Fewer camera views / lower resolution | Fewer tokens | Less information | Not applicable (fixed 512×512) |

OpenVLA's paper is a useful reference point: it reports LoRA fine-tuning a 7B VLA on consumer GPUs with little loss of performance relative to full fine-tuning. SmolVLA avoids that need by being small.

## Normalization

Inputs and outputs have different units and ranges, so LeRobot normalizes them with dataset statistics (`meta/stats.json` or the v2.1 equivalent):

- **state and action:** MEAN_STD, *x̂* = (*x* − μ) / σ;
- **images:** IDENTITY in the policy config (image scaling is handled inside the model).

Consequences:

1. The model predicts **normalized** actions, which are un-normalized with the dataset's μ and σ at inference. Using a checkpoint with statistics from a different dataset silently mis-scales every action.
2. A joint that barely moved in the demonstrations has a small σ, so small noise in it is amplified. Watch `wrist_roll` if it was nearly constant.
3. The `max_state_dim` / `max_action_dim` of 32 means the 6-D vectors are zero-padded; this is internal to SmolVLA.

## Learning-rate schedules

Run 1 used **cosine decay with linear warmup**: the LR rises linearly to 1e-4 over 1,000 steps, then follows a cosine down toward 2.5e-6 over `num_decay_steps`.

$$
\eta(t) = \eta_{\min} + \tfrac12(\eta_{\max} - \eta_{\min})\left(1 + \cos\frac{\pi\, t}{T_{\text{decay}}}\right)
$$

With *T*<sub>decay</sub> = 30,000 and training stopped at 20,000, the cosine had not finished (≈ 2.7 × 10⁻⁵ at the end if applied literally). Some LeRobot versions rescale the schedule when `steps < num_decay_steps`. Check the logged LR. Warmup protects pretrained weights from large early updates; decay lets the model settle.

## Samples seen, not just steps

"20,000 steps" means very different things at batch 2 and at batch 64:

| Config | Samples | Passes over 23,424 frames |
|--------|---------|---------------------------|
| Run 1 (batch 2) | 40k | ≈ 1.7 |
| Run 2 (batch 4) | 80k | ≈ 3.4 |
| LeRobot SmolVLA example (batch 64) | 1.28M | ≈ 55 |

The SmolVLA docs estimate ~4 h for 20k steps at batch 64 on one A100. On an RTX 3050 at ~0.13 s per sample (Run 2's 0.53 s/step ÷ 4), matching 1.28M samples would take roughly 46 hours. Matching even a quarter of that is a reasonable overnight-plus experiment.

## A suggested next run

*Proposal, not yet run; verify each flag with `lerobot-train --help` in LeRobot 0.6.2.*

| Change | Rationale |
|--------|-----------|
| Start from `lerobot/smolvla_base` | Pretraining effect reported in the paper |
| Hold out 4 episodes | Measure offline generalization |
| Enable image transforms (colour jitter) | Robustness to white balance and lighting |
| Mixed precision on, batch 8 if it fits | More samples per step |
| 40k–60k steps; `num_decay_steps` equal to `steps` | ≈ 14–20 passes over the data; schedule completes |
| Save every 5k; evaluate 3 checkpoints on the robot | Select by success rate, not loss |

## Limitations

GPU memory estimates depend on the exact implementation and sequence lengths; measure with `nvidia-smi` during training. More samples help only if the data cover the test conditions.

## Further reading

- Hu, E. J. et al. (2022). *LoRA: Low-Rank Adaptation of Large Language Models.* ICLR. arXiv:2106.09685.
- Kim, M. J. et al. (2024). *OpenVLA.* CoRL. arXiv:2406.09246. Section on parameter-efficient fine-tuning.
- [LeRobot: Training with PEFT](https://huggingface.co/docs/lerobot/peft_training) and [Compute hardware guide](https://huggingface.co/docs/lerobot/hardware_guide).
