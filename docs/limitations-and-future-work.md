# Limitations and Future Work

## Limitations

### Data
- 39 episodes (about 13 minutes) of one task with one instruction, below the ~50-episode starting point the SmolVLA guide recommends.
- Cube and tray position coverage was not logged, so generalization cannot be assessed rigorously.
- There is no held-out split, so overfitting cannot be quantified.
- The gripper camera recorded with auto white balance, so its colour varies across sessions.
- No colour augmentation was used during training (Run 1).

### Model and training
- Small batches (2–4), imposed by a 6 GB GPU, mean only ≈ 1.7–3.4 passes over the data.
- Run 1's initialization (base model vs VLM only) is unverified.
- Run 1 and Run 2 use different LeRobot versions and camera conventions, so their checkpoints are not interchangeable.
- The learning-rate schedule may not have fully decayed in Run 1 (30k decay steps against 20k training steps).

### System
- An unstable USB hub chain is still used for some devices.
- The custom ROS nodes (`bridge.py`, `inference_bridge.py`) are not version-controlled in a public repository.
- There is no UPS, so long runs are vulnerable to power cuts.
- The calibration procedure and files are not documented.

### Evaluation
- The offline check used only a training episode.
- No real-world success rate has been measured.

## Future work (prioritized)

| Priority | Item | Expected benefit | Effort |
|----------|------|------------------|--------|
| P0 | Verify Run 1's initialization and checkpoint integrity; check whether Run 2 finished | Know exactly what is being tested | Minutes |
| P0 | Re-test inference with matched conditions (one cube, trained position, locked white balance, ≥ 20 s, same rest pose) | Isolates distribution shift as a cause | 1 hour |
| P1 | Log the predicted gripper command during a failed grasp | Distinguishes "the model never asks to close" from "the bridge blocks closing" | 1 hour |
| P1 | Try a shorter execution horizon (`n_action_steps` 10–25) at inference | More reactive grasping | 1 hour |
| P1 | Record 10–20 more episodes with locked white balance, a grid of positions and a position log | Better coverage; matches SmolVLA guidance | Half a day |
| P1 | Run the [evaluation protocol](evaluation.md) on in-distribution positions (≥ 10 trials) | First real success rate | Half a day |
| P2 | Retrain with colour augmentation and more samples (for example batch 4–8 with AMP, or more steps) | Robustness and grasp precision | Overnight |
| P2 | Train an ACT baseline on the same data | A smaller, faster comparison point; ACT is a standard baseline for SO-arm tasks | Overnight |
| P2 | Hold out episodes and report offline per-joint MAE | Measures generalization offline | 1 hour |
| P3 | Move the adapters to direct USB ports; add a UPS | Reliability | Hardware |
| P3 | Publish the custom ROS nodes and the robot config | Reproducibility | 1 hour |
| P3 | Try the host `lerobot-rollout` path after confirming the calibration units match | Removes the ROS bridge from the loop | 1 day |
| P4 | Multiple objects, shapes and target positions with distinct instructions | Exercises the language channel of the VLA | Weeks |
| P4 | Asynchronous inference (LeRobot async stack) | Smoother, faster execution, as in the SmolVLA paper | 1 day |
