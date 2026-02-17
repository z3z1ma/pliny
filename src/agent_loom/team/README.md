# Loom Team

Team is Loom's tmux-native collaboration runtime for one operating model:

- `manager`
- `architect`
- `workers`
- `integrator`

The manager orchestrates. Workers execute tickets. Architect shapes sprint plans/tickets. Integrator performs deterministic fan-in merges.

## Architecture

Team has a simple control-plane split:

- CLI/commands parse inputs and invoke orchestration.
- `core.py` coordinates lifecycle, messaging, and tmux sidecars.
- Domain modules own policy/state surfaces (`team_config`, `targets`, `communication_policy`, `health`, `run_state`, `inbox`).

Architecture boundaries and guardrails: command adapters stay thin, `run_state` owns persisted run IO, and cross-role messaging must use canonical core targets only.
Output contract: team commands should emit through shared output helpers (`cli_output` and `team/output.py`) rather than ad-hoc prints.

## Team Cookbook

## Quickstart

```bash
loom team init
loom team start my-team --objective "Ship X" --config ./team-config.yaml
loom team attach my-team
```

## First 10 Commands (Happy Path)

1. `loom team start <TEAM> --objective "..." --config <PATH>`
2. `loom team status <TEAM>`
3. `loom team prep-sprint <TEAM> --name "..."`
4. `loom team spawn <TEAM> <TICKET_ID>`
5. `loom team send <TEAM> worker:<id> "..."`
6. `loom team merge <TEAM> enqueue --ticket <id> --branch <branch> --from-worker <id>`
7. `loom team spawn-integrator <TEAM>`
8. `loom team ship <TEAM>`
9. `loom team doctor <TEAM>`
10. `loom team disband <TEAM>`

## Team Config (`--config`)

`loom team start --config` accepts a YAML config with a minimal schema:

```yaml
harness: codex            # optional; run-level default
model: gpt-5-codex        # optional; run-level default
role_prompts:
  append:
    manager: ""
    architect: ""
    worker: ""
    integrator: ""
worker:
  subagents: encouraged
liveness:
  heartbeat_interval_s: 20
  stale_after_s: 90
  dead_after_s: 240
  recovery_cooldown_s: 180
  max_recoveries_per_hour: 3
```

Runtime state persists this under `run.json` as `team_config`.

## Messaging Targets

`loom team send` supports only core targets:

- `manager`
- `architect`
- `integrator`
- `workers`
- `worker:<id>`
- `ticket:<id>`

## Liveness Model

Each sidecar emits heartbeats to `.loom/team/runs/<TEAM>/health/<recipient>.json`.

Health states:

- `alive`
- `stale`
- `dead`
- `missing`

Team uses bounded auto-recovery with cooldown and hourly caps. `loom team status` and `loom team doctor` include heartbeat health and remediation hints.

## Notes

- `loom team init` syncs canonical prompts from `team/prompts.py` into managed prompt blocks in `.opencode/agents/*` and `.claude/agents/*`.
- `loom team wait`/`snooze` are manager/worker-friendly blocking waits with wake-on-inbox signaling.
- `loom team bounce` force-restarts a worker child process through the inbox control channel.
