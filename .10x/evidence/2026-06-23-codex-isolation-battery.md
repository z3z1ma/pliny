Status: recorded
Created: 2026-06-23
Updated: 2026-06-23
Relates-To: .10x/tickets/done/2026-06-23-broaden-codex-live-harness-isolation.md

# Codex Isolation Battery Evidence

## What Was Observed

The Codex isolation battery tooling exists at:

- `autoresearch/run_codex_isolation.py`

Dry-run planning produced a two-run plan using generated workspaces,
`--disable plugins`, `--ignore-user-config`, `--sandbox read-only`, and no-write
prompts.

Live battery command:

```text
$ python3 autoresearch/run_codex_isolation.py --out .10x/evidence/.storage/2026-06-23-codex-isolation-battery --max-runs 2 --run
exit_code 0
run_count 2
all_exit_zero true
all_expected_fragments_present true
any_plugin_or_skill_warnings false
any_workspace_contamination false
```

Recorded artifacts:

- `.10x/evidence/.storage/2026-06-23-codex-isolation-battery/summary.json`
- `.10x/evidence/.storage/2026-06-23-codex-isolation-battery/run-0001/command.json`
- `.10x/evidence/.storage/2026-06-23-codex-isolation-battery/run-0001/codex.stdout.jsonl`
- `.10x/evidence/.storage/2026-06-23-codex-isolation-battery/run-0001/codex.stderr`
- `.10x/evidence/.storage/2026-06-23-codex-isolation-battery/run-0001/last-message.txt`
- `.10x/evidence/.storage/2026-06-23-codex-isolation-battery/run-0001/workspace-manifest.json`
- matching `run-0002` files.

Each live run exited zero, included its expected isolation marker in the final
message, recorded four JSONL events, used no tools, and produced no observed
plugin/skill loader warning or workspace contamination signal.

Observed token fields for each run:

```text
input_tokens=19318
cached_input_tokens=2432
output_tokens=14
reasoning_output_tokens=0
```

Unit tests passed:

```text
$ python3 -m unittest autoresearch.tests.test_run_codex_isolation
Ran 3 tests in 0.012s
OK
```

## Procedure

1. Implemented a bounded two-run isolation battery for Codex CLI.
2. Ran dry-run planning to inspect argv and environment policy.
3. Ran the live battery into `.10x/evidence/.storage/`.
4. Inspected summary fields for exit codes, expected fragments, warnings,
   workspace contamination, token usage, and tool-use observations.

## What This Supports Or Challenges

This supports:

- `.10x/tickets/done/2026-06-23-broaden-codex-live-harness-isolation.md#AC-001`
- `.10x/tickets/done/2026-06-23-broaden-codex-live-harness-isolation.md#AC-002`
- `.10x/tickets/done/2026-06-23-broaden-codex-live-harness-isolation.md#AC-003`
- `.10x/tickets/done/2026-06-23-broaden-codex-live-harness-isolation.md#AC-004`

This challenges the prior limitation that Codex live isolation evidence covered
only one tiny smoke.

## Limits

This battery does not prove complete hidden-context absence. It used no-tool,
no-write prompts and did not run candidate research tasks. It supports only the
observed isolation properties of this small battery.
