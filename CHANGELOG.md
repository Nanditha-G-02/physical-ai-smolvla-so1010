# Changelog

All notable changes to this documentation repository. The project timeline itself is in [docs/project-overview.md](docs/project-overview.md#project-journey).

## [0.1.0] — 2026-10-20

### Added
- Initial documentation reconstructed from the project history: hardware, software, camera, teleoperation, recording, dataset, training, inference, evaluation and troubleshooting.
- Learning guides (physical AI, VLAs, SmolVLA, imitation learning, action chunking, teleoperation, vision-based manipulation, dataset design, fine-tuning, evaluation).
- Research section with paper summaries, literature review, comparison table and BibTeX.
- Experiment log for Run 1 (container) and Run 2 (host), reconstructed Run 1 training configuration, evaluation templates.
- Mermaid diagrams for architecture, data flow, teleoperation, recording, training, inference and the end-to-end workflow.
- Scripts: `verify_environment.py`, `inspect_dataset.py`, `check_links.py`, `scan_secrets.py`.
- CI workflow for link and secret checks; issue templates.

### Known gaps
- Source code of the custom ROS nodes and scripts is not yet included (see [VERIFICATION_STATUS.md](VERIFICATION_STATUS.md)).
- No real-world success rate has been measured yet.
