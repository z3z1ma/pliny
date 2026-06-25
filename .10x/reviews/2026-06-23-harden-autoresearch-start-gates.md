Status: recorded
Created: 2026-06-23
Updated: 2026-06-23
Target: .10x/tickets/done/2026-06-23-harden-autoresearch-start-gates.md
Verdict: pass

# Harden Autoresearch Start Gates Review

## Target

Start-gate hardening for multiday autoresearch:

- canonical guard;
- results ledger helper;
- scenario split validation;
- `program.md` start-gate updates;
- guarded `run_once.py`.

## Findings

- **No blocking issue:** `run_once.py` now produces a canonical guard artifact
  and fails if canonical files change during the one-shot run.
- **No blocking issue:** `--require-clean-canonical` fails when canonical files
  are dirty or untracked in git. The current dirty setup correctly fails until
  committed.
- **No blocking issue:** The results ledger helper prevents malformed statuses,
  commas, tabs, and newline corruption.
- **No blocking issue:** The split file gives the LLM a concrete exploration vs
  held-out boundary and is validated.
- **Residual risk, accepted:** The current scorer remains Trust Level 1, so
  promotion confidence cannot honestly reach 99% from automated scores alone.
- **Residual risk, accepted:** The guard covers `SKILL.md` and
  `autoresearch/program.md`, not every possible project instruction file.

## Verdict

Pass. The feasible operational safeguards are in place. After committing this
setup, the process can start with high confidence that canonical files will not
be accidentally mutated during autoresearch runs.

## Residual Risk

Before a real multiday run, commit the setup and verify:

```text
python3 autoresearch/canonical_guard.py --require-clean
```

Then invoke `run_once.py` with `--require-clean-canonical` for every experiment.
