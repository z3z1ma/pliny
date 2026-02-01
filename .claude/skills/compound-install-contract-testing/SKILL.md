---
name: compound-install-contract-testing
description: Use when changing src/agent_loom/compound/install.py or src/agent_loom/compound/cli.py to keep installed .opencode outputs deterministic and covered by tests/test_compound_install.py.
license: MIT
compatibility: opencode,claude
metadata:
  created_at: "2026-02-01T04:25:40.311Z"
  updated_at: "2026-02-01T04:25:40.311Z"
  version: "1"
---
<!-- BEGIN:compound:skill-managed -->
## When to use

- You changed `src/agent_loom/compound/install.py`.
- You changed `src/agent_loom/compound/cli.py` in a way that affects installation/scaffolding.
- You changed any file that is expected to be installed/generated under `.opencode/`.

## Goal

Keep Compound installation outputs deterministic and regression-tested.

## Checklist

1. Identify the install contract
   - What files must be created under `.opencode/`?
   - Pay special attention to:
     - `.opencode/skills/`
     - `.opencode/commands/`
   - Which files are templates mirrored under `src/agent_loom/compound/opencode/.opencode/`?
   - Which files must be gitignored (for example `.opencode/memory/observations.jsonl`)?

2. Ensure deterministic content
   - Stable ordering (no set/dict iteration).
   - No timestamps, random IDs, or machine-specific absolute paths.

3. Update/add contract tests
   - Edit `tests/test_compound_install.py` to assert:
     - required files exist
     - required file contents include key markers/blocks
     - gitignore entries are present and correct

4. Verification gate
   - `uv run basedpyright`
   - `uv run ruff check .`
   - `uv run pytest tests/test_compound_install.py`

## Common failure modes

- Template drift between `.opencode/` and `src/agent_loom/compound/opencode/.opencode/`.
- Tests asserting full file contents that include nondeterministic data.
- Installing files that should be ignored/ephemeral (logs, observations) without adding `.gitignore` rules.
<!-- END:compound:skill-managed -->

## Manual notes

_This section is preserved when the skill is updated. Put human notes, caveats, and exceptions here._
