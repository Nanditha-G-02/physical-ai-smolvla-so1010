# Architecture Diagrams

Mermaid sources for every diagram in the documentation. GitHub renders Mermaid inside Markdown code blocks; these `.mmd` files are the same diagrams as standalone sources, for editing or exporting with the [Mermaid CLI](https://github.com/mermaid-js/mermaid-cli) (`mmdc -i file.mmd -o file.svg`) or the [Mermaid Live Editor](https://mermaid.live).

| # | Diagram | Source | Explained in |
|---|---------|--------|--------------|
| A | Overall system architecture | [system-architecture.mmd](system-architecture.mmd) | [docs/system-architecture.md](../docs/system-architecture.md#diagram-a-overall-system) |
| B | Camera → policy → robot data flow | [data-flow.mmd](data-flow.mmd) | [docs/system-architecture.md](../docs/system-architecture.md#diagram-b-camera--policy--robot-data-flow) |
| C | Leader–follower teleoperation | [teleoperation.mmd](teleoperation.mmd) | [docs/teleoperation.md](../docs/teleoperation.md#diagram-c-leaderfollower-teleoperation) |
| D | Dataset recording pipeline | [recording-pipeline.mmd](recording-pipeline.mmd) | [docs/dataset-recording.md](../docs/dataset-recording.md#diagram-d-recording-pipeline) |
| E | SmolVLA training pipeline | [training-pipeline.mmd](training-pipeline.mmd) | [docs/smolvla-training.md](../docs/smolvla-training.md#diagram-e-training-pipeline) |
| F | Inference pipeline | [inference-pipeline.mmd](inference-pipeline.mmd) | [docs/inference.md](../docs/inference.md#diagram-f-inference-pipeline) |
| G | End-to-end project workflow | [end-to-end-workflow.mmd](end-to-end-workflow.mmd) | [docs/system-architecture.md](../docs/system-architecture.md#diagram-g-end-to-end-project-workflow) |

## Conventions

- **Dashed arrows** mark planned or unverified paths (for example `lerobot-rollout` on the host).
- Labels say **(planned)** or **(pending)** where a component does not yet exist or has not been verified.
- Topic names and configuration values in the diagrams are the verified ones from the project.

If you edit a diagram, update both the `.mmd` file and the Markdown document that embeds it.
