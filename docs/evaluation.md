# Evaluation

## Contents
- [Two kinds of evaluation](#two-kinds-of-evaluation)
- [Offline evaluation (done for Run 1)](#offline-evaluation-done-for-run-1)
- [Real-robot evaluation protocol (planned)](#real-robot-evaluation-protocol-planned)
- [Metrics](#metrics)
- [Statistics: how many trials?](#statistics-how-many-trials)
- [Recording results](#recording-results)
- [Measured results so far](#measured-results-so-far)

## Two kinds of evaluation

| | Offline (open-loop) | Real robot (closed-loop) |
|---|---|---|
| Question | Does the model reproduce the recorded actions given recorded observations? | Does the robot complete the task when the model's own actions shape what it sees next? |
| Needs robot | No | Yes |
| Catches | Bugs in normalization, camera mapping, wrong checkpoint | Compounding errors, controller interface bugs, distribution shift |
| Misses | Everything that only happens in closed loop | — |

Both are needed. Run 1 passed the offline check yet failed on the robot for reasons (rate limiting, scene differences) that offline evaluation cannot see. Background: [learning/evaluation-metrics.md](../learning/evaluation-metrics.md).

## Offline evaluation (done for Run 1)

`offline_eval.py` (custom script; source not included yet) feeds recorded observations from an episode into the policy and compares predicted actions with the recorded ones.

| Item | Result | Level |
|------|--------|-------|
| Episode tested | 0 (a training episode) | 🟡 Reported |
| Per-joint error | ≈ 2–5 units on every joint | 🟡 Reported |
| Phase timing (reach, open, grasp, move toward tray) | Matched the demonstration | 🟡 Reported |

**Caveat:** episode 0 was in the training set, so this shows the model fits its training data. It does not show generalization. Recommended next steps:

1. Hold out 3–4 episodes from training and evaluate on them.
2. Report per-joint MAE and the error specifically around the grasp (gripper closing frames).
3. Save plots of predicted vs recorded trajectories to `experiments/evaluation-results/`.

## Real-robot evaluation protocol (planned)

The protocol follows the recommendations of Kress-Gazit et al. (2024): report conditions explicitly, use several metrics alongside success rate, apply statistics, and describe failure modes ([summary](../research/paper-summaries/evaluation-and-data-scaling.md)). The task scoring mirrors the SmolVLA paper's real-world evaluation (0.5 for grasping, 0.5 for placing).

### Fixed conditions (record once per session)

Checkpoint path and step; LeRobot version; instruction text; lighting; camera settings (white balance value); rest pose; episode time limit; bridge settings (rate limit, distance cap); operator; date.

### Position sets

Mark positions on the table with tape and photograph the layout.

| Set | Definition | Purpose |
|-----|------------|---------|
| **ID** (in-distribution) | Cube and tray positions used in the demonstrations | Does the policy work where it was trained? |
| **Interp** | Cube positions between trained positions | Interpolation |
| **OOD-cube** | Cube outside the trained region, tray fixed | Extrapolation in object position |
| **OOD-tray** | Tray moved, cube in a trained position | Target generalization |
| **OOD-combo** | Both moved to an unseen combination | Compositional generalization |

Start with ID only. There is no point testing OOD before ID works.

### Trials

- At least **10 trials per position set** (more for comparing two policies).
- Randomize trial order across positions to avoid drift effects.
- One trial = start at rest pose, start policy, stop at success, at the time limit, or on a safety stop.
- Video-record every trial (store outside Git).

## Metrics

| Metric | Definition |
|--------|-----------|
| Grasp success | Cube lifted clear of the table and held |
| Place success | Cube released inside the tray and resting there |
| Task score | 0.5 × grasp + 0.5 × place (SmolVLA convention) |
| Full success | Grasp **and** place without human intervention |
| Drops | Cube released outside the tray after grasping |
| Completion time | Seconds from first motion to release in tray (successes only) |
| Grasp attempts | Number of closing motions before success or timeout |
| Recovery | Re-grasp after a miss or drop without intervention |
| Safety stops | Trials ended by the operator for safety |
| Failure mode | Categorical: *no motion*, *wrong target*, *hover/no close*, *close-miss*, *slip*, *drop in transport*, *misplace*, *collision*, *timeout* |

## Statistics: how many trials?

Real-robot trials are expensive, so report uncertainty. For *k* successes out of *n* trials, report a **Wilson 95 % interval**:

```python
from math import sqrt
def wilson(k, n, z=1.96):
    p = k / n
    d = 1 + z*z/n
    c = (p + z*z/(2*n)) / d
    h = z * sqrt(p*(1-p)/n + z*z/(4*n*n)) / d
    return c - h, c + h
print(wilson(7, 10))   # ≈ (0.40, 0.89)
```

With 10 trials, 7/10 success is consistent with anything from about 40 % to 89 %. To claim policy A beats policy B, use more trials, a two-proportion test, or a sequential testing method such as STEP ("Is Your Imitation Learning Policy Better than Mine?", arXiv:2503.10966).

## Recording results

Use [experiments/evaluation-results/trial_log_template.csv](../experiments/evaluation-results/trial_log_template.csv). One row per trial; summarize in [experiments/experiment-log.md](../experiments/experiment-log.md).

## Measured results so far

| Metric | Value |
|--------|-------|
| Real-world trials run under this protocol | 0 |
| Grasp success | Not measured |
| Place success | Not measured |
| Qualitative (3 informal attempts) | Reach achieved in attempt 3; no grasp |
