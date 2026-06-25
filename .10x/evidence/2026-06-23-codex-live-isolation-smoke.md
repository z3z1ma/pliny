Status: recorded
Created: 2026-06-23
Updated: 2026-06-23
Relates-To: .10x/tickets/done/2026-06-23-codex-live-isolation-smoke.md, .10x/evidence/2026-06-23-autoresearch-codex-full-harness.md

# Codex Live No-10x Isolation Smoke

## What Was Observed

One live Codex no-10x isolation smoke was run in an empty generated workspace.

Artifacts:

- `.10x/evidence/.storage/2026-06-23-codex-live-isolation-smoke/command.json`
- `.10x/evidence/.storage/2026-06-23-codex-live-isolation-smoke/workspace-manifest.json`
- `.10x/evidence/.storage/2026-06-23-codex-live-isolation-smoke/codex.jsonl`
- `.10x/evidence/.storage/2026-06-23-codex-live-isolation-smoke/codex.stderr`
- `.10x/evidence/.storage/2026-06-23-codex-live-isolation-smoke/last-message.txt`
- `.10x/evidence/.storage/2026-06-23-codex-live-isolation-smoke/raw/live-codex-isolation-smoke.json`
- `.10x/evidence/.storage/2026-06-23-codex-live-isolation-smoke/scores/live-codex-isolation-smoke.score.json`

The actual command used the top-level approval flag form accepted by this Codex
CLI version:

```text
codex --ask-for-approval never exec --cd <workspace> --ephemeral --json --output-last-message <last-message> --ignore-user-config --sandbox read-only <prompt>
```

The smoke prompt was:

```text
This is a harness isolation smoke test. Do not use tools. Do not write files. Reply exactly: LIVE_CODEX_SMOKE_OK
```

Observed command metadata:

```text
codex_version codex-cli 0.132.0
exit_code 0
timed_out False
start_timestamp_utc 2026-06-23T07:53:38.158350+00:00
end_timestamp_utc 2026-06-23T07:53:42.798358+00:00
ignore_user_config_present True
sandbox read-only
```

`last-message.txt` contained exactly:

```text
LIVE_CODEX_SMOKE_OK
```

`codex.jsonl` contained four events:

```text
thread.started
turn.started
item.completed: LIVE_CODEX_SMOKE_OK
turn.completed: input_tokens=20328, cached_input_tokens=2432, output_tokens=10, reasoning_output_tokens=0
```

Workspace manifest observations:

```text
pre_run_present_suppressed_instruction_files []
post_run_present_suppressed_instruction_files []
pre_run_non_git_workspace_files []
post_run_non_git_workspace_files []
workspace_lacked_suppressed_instruction_files_before_run True
workspace_lacked_suppressed_instruction_files_after_run True
```

The live output was converted into an offline-score-compatible raw artifact and
scored:

```text
scenario_id SCN-008
variant_id no-10x-control-live-smoke
scores {'S004': {'value': 100.0, 'confidence': 'low', 'floor_triggered': False, ...}}
manual_inspection.status required-not-done
cost.wall_seconds 4.640008
cost.input_tokens 20328
cost.output_tokens 10
cost.tool_calls 0
```

The run also produced an important negative observation. `codex.stderr` included
CODEX_HOME plugin and skill loader warnings despite `--ignore-user-config`,
including plugin manifest warnings and skill loader warnings. This indicates
that the smoke does not prove complete user/plugin/skill isolation.

## Procedure

1. Created an artifact root under
   `.10x/evidence/.storage/2026-06-23-codex-live-isolation-smoke/`.
2. Created an empty generated workspace initialized as its own git repository.
3. Checked that the workspace lacked `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`,
   `.cursor/rules`, and `.agents/skills` before the run.
4. Ran one live `codex exec` smoke with `--ephemeral`, `--json`,
   `--output-last-message`, `--ignore-user-config`, `--sandbox read-only`, and
   approval policy `never`.
5. Captured stdout JSONL, stderr, command metadata, final message, and workspace
   manifest.
6. Checked that the workspace still lacked the suppressed instruction files and
   non-git files after the run.
7. Converted the observation into a raw fixture artifact.
8. Ran `python3 autoresearch/offline_score.py --fixtures <raw-artifact> --out
   <scores-dir>` and inspected the generated score artifact.

## What This Supports Or Challenges

This supports:

- `.10x/tickets/done/2026-06-23-codex-live-isolation-smoke.md#AC-001`
- `.10x/tickets/done/2026-06-23-codex-live-isolation-smoke.md#AC-002`
- `.10x/tickets/done/2026-06-23-codex-live-isolation-smoke.md#AC-003`
- `.10x/tickets/done/2026-06-23-codex-live-isolation-smoke.md#AC-004`
- `.10x/tickets/done/2026-06-23-codex-live-isolation-smoke.md#AC-005`

The observation supports the narrow claim that one live Codex exec command, run
from an empty generated workspace with no project instruction files and with
`--ignore-user-config`, returned the requested final answer, emitted no JSONL
tool events, left no non-git workspace files, and produced raw output that the
offline scorer can consume.

The observation challenges the stronger claim that `--ignore-user-config` alone
fully isolates Codex from user/plugin/skill context. CODEX_HOME plugin and skill
loader warnings still appeared in stderr, and the JSONL usage reported 20,328
input tokens for a tiny prompt.

## Limits

This evidence does not show that:

- Long-running Codex tasks remain isolated.
- Real 10x benchmark tasks avoid all user/plugin/skill context contamination.
- `--ignore-user-config` suppresses CODEX_HOME plugins or skills.
- The subject agent saw no hidden system, plugin, or skill context.
- Offline score `S004=100` is calibrated beyond Trust Level 1.
- Any no-10x control comparison is clean enough for promotion decisions.

Stronger CODEX_HOME isolation is tracked in
`.10x/tickets/done/2026-06-23-codex-home-isolation.md`.
