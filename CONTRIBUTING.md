# Contributing

This is a personal research and learning repository, but corrections and reproduction reports are welcome.

## Ground rules

1. **Evidence first.** Label every claim with the evidence levels defined in [VERIFICATION_STATUS.md](VERIFICATION_STATUS.md). Do not upgrade a 🟡 *Reported* item to ✅ *Verified* without attaching the terminal output, log or file that proves it.
2. **No secrets.** Never commit Hugging Face tokens, `.env` files, SSH keys, or serial numbers you consider private. Run `python scripts/scan_secrets.py` before every commit.
3. **No large binaries.** Datasets and checkpoints live on the Hugging Face Hub. The `.gitignore` blocks `*.safetensors`, `*.mp4`, `*.parquet` and similar files.
4. **Label where commands run.** Prefix command blocks with `# [HOST]` or `# [CONTAINER]`, and note the LeRobot version when a command is version-dependent.
5. **Cite real sources.** Add new papers to [research/references.bib](research/references.bib) with an arXiv ID or DOI, and summarize them in your own words.

## Reporting a reproduction

Open an issue with the *Experiment report* template and include: hardware, LeRobot version, dataset revision, the exact command, and the measured results (or "not measured").

## Checks before a pull request

```bash
python scripts/check_links.py      # all relative links resolve
python scripts/scan_secrets.py     # no tokens or keys
```

The same checks run in CI ([.github/workflows/docs-check.yml](.github/workflows/docs-check.yml)).
