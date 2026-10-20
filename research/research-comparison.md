# Research Comparison

Values are as reported by each paper; "—" means not applicable or not reported in a comparable form. See [references.bib](references.bib) for full citations.

## Policies and VLAs

| Model | Year / venue | Params | Backbone | Action representation | Chunking | Language | Pretraining data | Open weights |
|-------|-------------|--------|----------|----------------------|----------|----------|------------------|-------------|
| ACT | 2023 / RSS | ~80M (per SmolVLA paper) | ResNet + transformer CVAE | Continuous (CVAE) | ✅ + temporal ensembling | ❌ | None (per task) | ✅ |
| Diffusion Policy | 2023 / RSS | — | CNN or transformer + diffusion | Continuous (diffusion) | ✅ receding horizon | ❌ | None (per task) | ✅ |
| RT-1 | 2023 / RSS | ~35M | EfficientNet + FiLM + transformer | Discrete (256 bins) | ❌ | ✅ | ~130k real episodes | Partial |
| RT-2 | 2023 / CoRL | up to 55B | PaLI-X / PaLM-E | Discrete text tokens | ❌ | ✅ | Web + RT-1 data | ❌ |
| Octo | 2024 / RSS | 27M / 93M | Transformer + diffusion head | Continuous | ✅ | ✅ | ~800k OXE trajectories | ✅ |
| OpenVLA | 2024 / CoRL | 7B | Llama 2 + DINOv2/SigLIP | Discrete tokens | ❌ | ✅ | ~970k OXE episodes | ✅ |
| π0 | 2024 / preprint | 3.3B | PaliGemma + flow-matching expert | Continuous (flow matching) | ✅ | ✅ | ~10k h cross-embodiment | ✅ (later release) |
| **SmolVLA** | 2025 / preprint | **0.45B** | SmolVLM-2 (half the layers) + flow-matching expert | Continuous (flow matching) | ✅ (n = 50) + async | ✅ | 481 community datasets, ~23k episodes | ✅ |

## Reported results most relevant to SO-arm tasks (from the SmolVLA paper)

| Setting | ACT | π0 (3.5B) | SmolVLA (0.45B) |
|---------|-----|-----------|-----------------|
| SO-100 pick-place / stacking / sorting (avg) | 48.3 % | 61.7 % | 78.3 % |
| SO-101 Lego pick-place, in distribution | 70 % | — | 90 % |
| SO-101 Lego pick-place, out of distribution | 40 % | — | 50 % |
| LIBERO average (simulation) | — | 86.0 % (pretrained) | 87.3 % |

## Fit to this project's constraints

| Constraint | ACT | Diffusion Policy | OpenVLA | π0 | SmolVLA |
|-----------|-----|-----------------|---------|----|---------|
| Trains on a 6 GB GPU | ✅ | ✅ | ❌ | ❌ | ✅ (frozen VLM, small batch) |
| Uses language | ❌ | ❌ | ✅ | ✅ | ✅ |
| Benefits from pretraining on SO-arm data | ❌ | ❌ | ❌ | Partly | ✅ |
| Available in LeRobot | ✅ | ✅ | — | ✅ | ✅ |
| Used in this project | Planned baseline | — | — | — | ✅ |
