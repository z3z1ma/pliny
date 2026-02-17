# Loom Team subsystem (agent guide)

Scope: `src/agent_loom/team/**`

## What this module owns

Team is Loom's tmux-native multi-agent orchestrator. It coordinates manager/architect/workers/integrator personas, run lifecycle, inbox messaging, and merge queue workflows on top of workspace/ticket primitives.

## Architectural boundaries (critical)

### 1) CLI + command handler layer (thin)

- `team/cli.py`: argparse surface and dispatch only.
- `team/commands/*.py`: thin command adapters grouped by domain.

These files should parse args, call core/domain functions, and emit output. They should not hold heavy business logic.

### 2) Core orchestration layer

- `team/core.py`: orchestration hotspot for lifecycle, worker flows, messaging, merge queue, tmux integration.

### 3) Domain/state/policy helpers

- `run_state.py`: canonical run-path resolution and persisted run state IO (`run.json` lifecycle).
- `start_state.py`: typed mutations used by start/resume flows.
- `team_config.py`: team config schema and runtime defaults (`--config`).
- `health.py`: sidecar heartbeat artifacts and state transitions.
- `communication_policy.py`: route authorization and delivery policy.
- `permissions.py`: role/environment guardrails.
- `targets.py`: target resolution for send/capture.
- `inbox.py`: durable inbox storage.
- `merge_queue.py`: merge queue persistence.
- `tmux.py`: tmux command wrappers.
- `output.py`: team wrappers around shared core output utilities.

## Command/control flow

Typical command flow:

1. `cli.py` parses command and routes to `commands/*.py`.
2. Command module calls `core.py` (or domain helper when appropriate).
3. `core.py` reads/writes run state via `run_state.py` (usually with locking).
4. `core.py` invokes policy modules (`permissions`, `communication_policy`, `targets`) and tmux wrappers (`tmux.py`).
5. Results are emitted through `output.py`/shared `core.cli_output` helpers.

Start/resume path centers on `run_state.py` and `start_state.py`; messaging path centers on `core.send` + communication/target modules; worker lifecycle path centers on `core.spawn/retire/resume-worker` + tmux/run-state coordination.

## Storage contract

Canonical run root:

- `.loom/team/runs/<team>/`
  - `run.json`
  - `CHARTER.md`
  - `inbox/`
  - `worktrees/`
  - merge queue files
  - captures/events/snapshots/sidecars (module-managed)

`run.json` is the source of truth for persisted team state. Live pane/process state is managed through tmux and reconciled through core helpers.

## Where to change code

- New command surface: `cli.py` + matching `commands/*.py` module.
- New orchestration behavior: `core.py` (extract reusable helpers into domain modules when possible).
- New run-state schema/persistence behavior: `run_state.py` and `start_state.py`.
- Messaging/routing rules: `communication_policy.py` + `targets.py`.
- Role/permission logic: `permissions.py`.
- tmux interaction behavior: `tmux.py`.

## Guardrails

- Keep `commands/*.py` thin (size and responsibility).
- Domain modules must not import from `team/commands/*`.
- Keep JSON output plumbing shared through core output helpers.
- Preserve `run_state.py` as canonical persistence path; avoid ad-hoc writes.
- Preserve built-in persona semantics (manager/architect/worker/integrator operating model).
- `team/core.py` is a known hotspot; prefer decomposition over growth when adding substantial logic.

## Team config model

Team config YAML is optional and loaded by `loom team start --config <path>`.

- Core operating model is fixed: manager + architect + workers + integrator.
- Config supports run-level `harness`/`model`, role prompt appends, worker subagent policy, and liveness thresholds.
- Communication/targeting is limited to core targets (`manager`, `architect`, `integrator`, `workers`, `worker:<id>`, `ticket:<id>`).

## Fast tests for team changes

- `uv run pytest tests/test_architecture_guardrails.py`
- `uv run pytest tests/test_team_cli_ux.py`
- `uv run pytest tests/test_team_start_state.py`
- `uv run pytest tests/test_team_comms_policy.py`
- `uv run pytest tests/test_team_targets.py`
- `uv run pytest tests/test_team_helpers.py`

Add scenario-specific suites for spawn/ship/sprint/harness changes as needed.
