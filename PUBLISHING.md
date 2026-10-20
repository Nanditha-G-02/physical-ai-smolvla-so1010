# Publishing to GitHub

Step-by-step commands to publish this documentation repository under your account. Nothing here pushes anything until you run the final command yourself.

**Repository name:** `physical-ai-smolvla-so101`
**Description:** End-to-end Physical AI project using SO-ARM101, ROS 2, LeRobot, SmolVLA, Hugging Face datasets, imitation learning, and vision-based robotic manipulation. Includes implementation documentation, research notes, tutorials, experiments, and troubleshooting.
**Suggested topics:** `physical-ai`, `robotics`, `lerobot`, `smolvla`, `vision-language-action`, `imitation-learning`, `ros2`, `so-arm101`, `hugging-face`

Keep this repository **separate** from the folders containing your robot code, datasets and checkpoints (`~/lerobot`, `~/so101_training`, the container workspace). Do not copy it into those folders.

## 0. Before the first commit

Replace the placeholders:

```bash
grep -rn "<your-github-username>" .
```

Edit `CITATION.cff` (and any other match) with your GitHub username. Optionally add real photos to `assets/` and your custom scripts to `src/`.

## 1. Initialize Git

```bash
cd ~/physical-ai-smolvla-so101        # wherever you unpacked the repository
git init -b main
git config user.name  "Nanditha G"     # if not set globally
git config user.email "<your-email>"
```

## 2. Run the checks

```bash
python scripts/check_links.py
python scripts/scan_secrets.py
```

Both must report 0 problems.

## 3. Stage and review

```bash
git add .
git status
git diff --cached --stat
```

Review the staged list. It should contain only Markdown, `.py`, `.mmd`, `.json`, `.csv`, `.cff`, `.bib`, `.yml`, `LICENSE` and `.gitignore`, with no datasets, videos, checkpoints, `.env` files or tokens.

Extra secret check on exactly what is staged:

```bash
git diff --cached | grep -nE "hf_[A-Za-z0-9]{30,}|sk-[A-Za-z0-9]{20,}|BEGIN .*PRIVATE KEY" || echo "no secrets in staged diff"
```

## 4. First commit

```bash
git commit -m "Initial documentation: SO-ARM101 + SmolVLA physical AI project"
```

## 5. Create the GitHub repository

**Option A, web:** create an empty repository named `physical-ai-smolvla-so101` at https://github.com/new. Do **not** add a README, licence or .gitignore there (they exist locally).

**Option B, GitHub CLI:**

```bash
gh auth login
gh repo create physical-ai-smolvla-so101 --public \
  --description "End-to-end Physical AI project using SO-ARM101, ROS 2, LeRobot, SmolVLA, Hugging Face datasets, imitation learning, and vision-based robotic manipulation. Includes implementation documentation, research notes, tutorials, experiments, and troubleshooting." \
  --source . --remote origin
```

## 6. Add the remote (Option A only)

```bash
git remote add origin https://github.com/<your-github-username>/physical-ai-smolvla-so101.git
git remote -v
```

## 7. Push

```bash
git push -u origin main
```

## 8. After publishing

- Check that the Mermaid diagrams render on GitHub (README, `docs/system-architecture.md`).
- Check that the **docs-check** workflow passes under the *Actions* tab.
- Add topics in *About → Settings*.
- Optionally link the repository from the Hugging Face dataset card.

## Clean history plan

| Commit | Content |
|--------|---------|
| 1 | Initial documentation (this commit) |
| 2 | Add custom scripts (`src/`) once reviewed for secrets and hard-coded paths |
| 3 | Add real photos and screenshots |
| 4+ | One commit per experiment: config, log, evaluation CSV, experiment-log update |

If a secret is ever committed, **revoke it first** (Hugging Face → Settings → Access Tokens), then rewrite history (for example with `git filter-repo`). Deleting the file in a later commit is not enough.
