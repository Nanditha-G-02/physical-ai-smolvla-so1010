# OpenVLA (2024) and π0 (2024)

## OpenVLA

**OpenVLA: An Open-Source Vision-Language-Action Model.** Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti et al. Conference on Robot Learning 2024. arXiv:2406.09246. **Status:** peer-reviewed. [arXiv](https://arxiv.org/abs/2406.09246)

**In our words.** A 7B-parameter open VLA: a Llama 2 language model with a fused visual encoder (DINOv2 + SigLIP features), trained on about 970k episodes from Open X-Embodiment, outputting discretized action tokens. The authors report that it outperforms the much larger closed RT-2-X on their generalist manipulation evaluations, and that **parameter-efficient fine-tuning (LoRA)** adapts it to new setups on consumer GPUs while staying close to full fine-tuning performance; quantization makes serving cheaper.

**Why it matters here.** OpenVLA showed that open VLAs and consumer-GPU fine-tuning are feasible, but at 7B parameters it is still too large to fine-tune comfortably on a 6 GB RTX 3050. SmolVLA's paper compares against it on LIBERO.

## π0

**π0: A Vision-Language-Action Flow Model for General Robot Control.** Kevin Black et al. (Physical Intelligence). arXiv:2410.24164, October 2024. **Status:** preprint. [arXiv](https://arxiv.org/abs/2410.24164)

**In our words.** π0 combines a pretrained VLM (PaliGemma, ~3B) with a separate **action expert** trained by **flow matching** to output continuous action chunks at high frequency (up to 50 Hz), so it can perform dexterous tasks such as laundry folding. It is pretrained on a large cross-embodiment mixture (about 10k hours, as reported) and then fine-tuned for specific tasks.

**Why it matters here.** SmolVLA's action expert directly follows π0's recipe (flow matching, Beta-distributed time sampling, VLM + expert split) at about 1/7 of the size. π0 is the main baseline in the SmolVLA paper, which reports SmolVLA matching or beating it on SO-100 tasks while training about 40 % faster with 6× less memory.

## Comparison

| | OpenVLA | π0 | SmolVLA |
|---|---|---|---|
| Size | 7B | 3.3B | 0.45B |
| Action output | Discrete tokens | Continuous chunks (flow matching) | Continuous chunks (flow matching) |
| Pretraining data | Open X-Embodiment | Proprietary cross-embodiment mixture | Community LeRobot datasets |
| Practical on a 6 GB GPU | No (LoRA + quantization help, but tight) | No | Yes (frozen VLM, batch 2–4) |
