# Evaluation Results

**Measured so far:** none under the [evaluation protocol](../../docs/evaluation.md). The three informal inference attempts are described in the [experiment log](../experiment-log.md#inference-experiments-run-1-checkpoint).

## How to record a session

1. Copy `trial_log_template.csv` to `YYYY-MM-DD_<checkpoint>_<position-set>.csv`.
2. Fill the session header fields in the first row of every trial (they repeat, which keeps each row self-contained).
3. One row per trial. Use the failure-mode vocabulary below.
4. Summarize in the experiment log: successes / trials with a Wilson 95 % interval (code in [docs/evaluation.md](../../docs/evaluation.md#statistics-how-many-trials)).

## Column reference

| Column | Values |
|--------|--------|
| `date`, `checkpoint`, `lerobot_version`, `instruction`, `wb_value`, `bridge_rate_limit`, `bridge_distance_cap` | Session conditions |
| `trial` | 1, 2, … |
| `position_set` | `ID`, `Interp`, `OOD-cube`, `OOD-tray`, `OOD-combo` |
| `cube_pos`, `tray_pos` | Marked position IDs, e.g. `P3`, `T1` |
| `grasp` / `place` | 0 or 1 |
| `score` | 0.5 × grasp + 0.5 × place |
| `drop` | 0 or 1 |
| `time_s` | Seconds to release in the tray (successes only) |
| `grasp_attempts` | Integer |
| `recovered` | 0 or 1 |
| `safety_stop` | 0 or 1 |
| `failure_mode` | `none`, `no_motion`, `wrong_target`, `hover_no_close`, `close_miss`, `slip`, `drop_transport`, `misplace`, `collision`, `timeout` |
| `video` | Path or link to the trial video (stored outside Git) |
| `notes` | Free text |

Offline evaluation outputs (per-joint MAE tables, trajectory plots) also belong in this folder.
