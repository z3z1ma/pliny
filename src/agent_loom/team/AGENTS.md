## Module architecture

### Responsibility boundaries

**CLI layer** (`team/cli.py`):
- Parser construction and argument validation only
- Dispatches to command handler modules
- Must NOT contain business logic or state manipulation
- Uses shared output helpers from `core/cli_output.py`

**Command handlers** (`team/commands/*.py`):
- Grouped by domain: lifecycle, workers, objective, inbox, merge, utils
- Each module owns command implementation for its domain
- Delegates to `team/core.py` for run state and tmux orchestration
- Uses `team/output.py` for JSON/text emission via shared primitives

**Core orchestration** (`team/core.py`):
- Run state management (start/pause/resume/disband)
- Worker lifecycle and worktree coordination
- Inbox and messaging
- Merge queue
- Sprint and objective state
- tmux session/window/pane management
- **Critical:** This file is a known hotspot (~6500 LOC) undergoing decomposition

**Domain modules**:
- `team/permissions.py`: role guards and environment checks
- `team/utilities.py`: shared helpers (parsing, git, pathing)
- `team/inbox.py`: inbox storage backend
- `team/merge_queue.py`: merge queue storage
- `team/models.py`: run state and message dataclasses
- `team/tmux.py`: tmux subprocess wrappers

**Output contract** (`team/output.py`):
- Wraps `core/cli_output.py` shared primitives
- Adds team-specific JSON envelope metadata if needed
- All CLI commands MUST use these helpers, not local duplicates

### Guardrails

1. **No duplicate output helpers**: All CLI serialization/emission uses `core/cli_output.py` primitives via `team/output.py`. Local helper duplication is a regression.
2. **Command handlers stay thin**: Business logic belongs in `team/core.py` or domain modules, not in `team/commands/*.py`.
3. **Hotspot size control**: `team/core.py` is monitored for growth. New functionality should extract to domain modules when feasible.
4. **Import direction**: Domain modules may NOT import from `team/commands/*`. Command handlers import from domain modules and core.

