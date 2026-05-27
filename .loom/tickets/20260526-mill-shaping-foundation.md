# Shaping Session Foundation + Context Document

ID: ticket:20260526-mill-shaping-foundation
Type: Ticket
Status: open
Created: 2026-05-26
Updated: 2026-05-26
Risk: medium - new backend module with new data model; must get the persistence and event shapes right since everything else builds on them

## Summary

Create the stateless foundation for shaping sessions: the data model, session
lifecycle, internal context document, file persistence, API endpoints, and
WebSocket event infrastructure.

After this ticket, a shaping session can be created, seeded with operator input,
its context document grown and read, its state persisted and recovered across
restarts, and structured events streamed to any connected frontend.

No intelligence, no harness invocations, no proposals. Just the shell that
everything else plugs into.

Closure claim: A shaping session can be created, persisted, recovered, streamed
to, and read through a complete API and event surface.

## Related Records

- `plan:20260526-mill-shaping-sessions` - parent plan
- `spec:mill-shaping-sessions` - behavioral contract
- `loom-mill/src/loom_mill/chat/session.py` - existing session persistence pattern to follow
- `loom-mill/src/loom_mill/state/models.py` - existing event types to extend
- `loom-mill/src/loom_mill/state/store.py` - pub/sub for WebSocket streaming
- `loom-mill/src/loom_mill/api/ws.py` - WebSocket event serialization
- `loom-mill/src/loom_mill/app.py` - route registration

## Scope

Write:
- `loom-mill/src/loom_mill/shaping/__init__.py` (new package)
- `loom-mill/src/loom_mill/shaping/models.py` — session state, interaction block types, staged record model
- `loom-mill/src/loom_mill/shaping/session.py` — session lifecycle, context doc management, persistence
- `loom-mill/src/loom_mill/shaping/events.py` — WebSocket event definitions
- `loom-mill/src/loom_mill/api/shaping.py` — REST endpoints
- `loom-mill/src/loom_mill/state/models.py` — add shaping event types
- `loom-mill/src/loom_mill/api/ws.py` — add shaping event serialization
- `loom-mill/src/loom_mill/app.py` — register new routes
- `loom-mill/tests/test_shaping_session.py` — full test coverage

Read:
- `loom-mill/src/loom_mill/chat/session.py` — persistence pattern
- `loom-mill/src/loom_mill/workstation/models.py` — state model pattern
- `loom-mill/frontend/src/lib/ws.svelte.ts` — understand event envelope format

Non-goals:
- Do NOT implement harness invocations (ticket 2)
- Do NOT implement interaction block generation logic (ticket 3)
- Do NOT implement staging area record CRUD or commit (ticket 4)
- Do NOT build frontend components (ticket 5)
- Do NOT implement branching (ticket 4)

## Detailed Design

### Data Model

```python
# loom_mill/shaping/models.py

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

class SessionPhase(str, Enum):
    EXPLORING = "exploring"      # gathering initial context
    NARROWING = "narrowing"      # focused questions
    PROPOSING = "proposing"      # generating record drafts
    REFINING = "refining"        # iterating on proposals
    READY = "ready"              # operator ready to commit

class BlockType(str, Enum):
    OPERATOR_INPUT = "operator_input"
    AGENT_QUESTION = "agent_question"
    AGENT_OBSERVATION = "agent_observation"
    AGENT_PROPOSAL = "agent_proposal"
    EXPLORATION_START = "exploration_start"
    EXPLORATION_COMPLETE = "exploration_complete"
    BRANCH_POINT = "branch_point"
    SYSTEM = "system"            # session created, committed, etc.

@dataclass
class InteractionBlock:
    id: str                      # unique block ID (uuid)
    type: BlockType
    timestamp: str               # ISO 8601
    content: dict[str, Any]      # type-specific payload
    # For OPERATOR_INPUT: {"text": "..."}
    # For AGENT_QUESTION: {"question": "...", "options": [...] | null, "context_ref": "..."}
    # For AGENT_OBSERVATION: {"observation": "...", "evidence": [...]}
    # For AGENT_PROPOSAL: {"record_id": "temp:...", "surface": "...", "title": "...", "content": "..."}
    # For EXPLORATION_START: {"invocation_id": "...", "goal": "...", "command": "..."}
    # For EXPLORATION_COMPLETE: {"invocation_id": "...", "summary": "...", "context_added": int}
    # For BRANCH_POINT: {"branches": [{"id": "...", "label": "...", "description": "..."}]}
    # For SYSTEM: {"message": "..."}

@dataclass
class StagedRecord:
    temp_id: str                 # temporary ID (e.g., "temp:ticket:auth-fix")
    surface: str                 # "tickets", "specs", "plans", etc.
    title: str
    content: str                 # full Markdown content
    branch: str                  # which branch this belongs to ("main" or branch ID)
    status: str                  # "proposed" | "accepted" | "rejected" | "modified"
    proposed_at: str             # ISO 8601
    modified_at: str | None = None

@dataclass
class SessionState:
    id: str                      # session UUID
    phase: SessionPhase
    created_at: str              # ISO 8601
    updated_at: str
    blocks: list[InteractionBlock] = field(default_factory=list)
    staged_records: list[StagedRecord] = field(default_factory=list)
    active_branch: str = "main"
    branches: list[str] = field(default_factory=lambda: ["main"])
    active_explorations: list[str] = field(default_factory=list)  # invocation IDs
    ended_at: str | None = None
```

### Context Document

The context document is a Markdown file that grows throughout the session. It
accumulates everything the engine has learned, preventing re-exploration.

```python
# loom_mill/shaping/session.py

class ShapingSession:
    """Manages a single shaping session's lifecycle and persistence."""
    
    def __init__(self, session_id: str, workspace_root: Path):
        self.session_id = session_id
        self.workspace_root = workspace_root
        self._base_dir = workspace_root / ".mill" / "shaping-sessions" / session_id
        self._state_path = self._base_dir / "state.json"
        self._context_path = self._base_dir / "context.md"
        self.state: SessionState = ...
    
    @classmethod
    def create(cls, workspace_root: Path, initial_input: str) -> "ShapingSession":
        """Create a new session seeded with operator input."""
        session_id = str(uuid4())
        session = cls(session_id, workspace_root)
        session._base_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize context document with seed
        session._write_context(f"# Shaping Session\n\n## Operator Input\n\n{initial_input}\n")
        
        # Initialize state
        session.state = SessionState(
            id=session_id,
            phase=SessionPhase.EXPLORING,
            created_at=utc_now(),
            updated_at=utc_now(),
            blocks=[InteractionBlock(
                id=str(uuid4()),
                type=BlockType.OPERATOR_INPUT,
                timestamp=utc_now(),
                content={"text": initial_input}
            )]
        )
        session._persist_state()
        return session
    
    @classmethod
    def load(cls, session_id: str, workspace_root: Path) -> "ShapingSession":
        """Load an existing session from disk."""
        ...
    
    def append_context(self, section_heading: str, content: str) -> int:
        """Append a new section to the context document. Returns new byte length."""
        ...
    
    def read_context(self) -> str:
        """Read the full context document."""
        ...
    
    def add_block(self, block: InteractionBlock) -> None:
        """Add an interaction block to the session timeline."""
        self.state.blocks.append(block)
        self.state.updated_at = utc_now()
        self._persist_state()
    
    def update_phase(self, phase: SessionPhase) -> None:
        """Transition session phase."""
        ...
    
    def _persist_state(self) -> None:
        """Atomically persist session state to disk."""
        ...
    
    def _write_context(self, content: str) -> None:
        """Write or overwrite context document."""
        ...
```

### Persistence Layout

```text
.mill/shaping-sessions/
  {session-id}/
    state.json         # SessionState serialized
    context.md         # Growing internal context document
```

### API Endpoints

```python
# loom_mill/api/shaping.py

# POST /shaping/sessions
# Body: {"input": "raw text dump of operator thoughts"}
# Returns: {"session_id": "...", "state": {...}}
# Creates a new session, seeds context doc, returns initial state.

# GET /shaping/sessions
# Returns: [{"id": "...", "phase": "...", "created_at": "...", "block_count": N, "staged_count": N}]
# Lists all active (non-ended) sessions.

# GET /shaping/sessions/{session_id}
# Returns: full SessionState JSON
# Gets current session state including all blocks and staged records.

# GET /shaping/sessions/{session_id}/context
# Returns: {"content": "...", "byte_length": N}
# Gets the raw context document (for debugging/audit).

# POST /shaping/sessions/{session_id}/input
# Body: {"text": "operator response or direction"}
# Adds operator input block, appends to context. Returns the new block.

# DELETE /shaping/sessions/{session_id}
# Ends and archives the session without committing.

# POST /shaping/sessions/{session_id}/commit
# (Implemented in ticket 4 - staging/commit)
```

### WebSocket Events

```python
# In state/models.py, add:

@dataclass
class ShapingEvent:
    """Generic shaping session event for WebSocket streaming."""
    session_id: str
    event: str        # "block_added", "phase_changed", "exploration_started", etc.
    data: dict        # event-specific payload

# Event types:
# - shaping:block_added       {"session_id", "block": InteractionBlock}
# - shaping:phase_changed     {"session_id", "phase": "exploring"|...}
# - shaping:exploration_start {"session_id", "invocation_id", "goal"}
# - shaping:exploration_stream {"session_id", "invocation_id", "delta"}
# - shaping:exploration_complete {"session_id", "invocation_id", "summary"}
# - shaping:record_staged     {"session_id", "record": StagedRecord}
# - shaping:record_updated    {"session_id", "record": StagedRecord}
# - shaping:record_removed    {"session_id", "temp_id"}
# - shaping:session_ended     {"session_id", "reason": "committed"|"cancelled"}
```

WebSocket serialization in `api/ws.py`:
```python
# In _event_payload():
if isinstance(event, ShapingEvent):
    return {"type": f"shaping:{event.event}", "data": {"session_id": event.session_id, **event.data}}
```

### Frontend Event Handling

In `ws.svelte.ts`, add state for shaping sessions:
```typescript
shapingSession = $state<{
  id: string | null;
  phase: string;
  blocks: InteractionBlock[];
  stagedRecords: StagedRecord[];
  activeBranch: string;
  branches: string[];
  activeExplorations: string[];
} | null>(null);
```

Handle `shaping:*` events by updating this state.

## Acceptance

- ACC-001: `POST /shaping/sessions` creates a session, persists state.json and
  context.md to `.mill/shaping-sessions/{id}/`, and returns the session state.
  - Evidence: Test creates session, verifies files on disk, reads back state.
  - Audit: Verify atomic writes, correct timestamps, valid UUIDs.

- ACC-002: `POST /shaping/sessions/{id}/input` appends operator input to the
  context document and adds an OPERATOR_INPUT block to session state.
  - Evidence: Test adds input, reads context doc, verifies content appended.
  - Audit: Verify context doc grows monotonically, blocks are ordered.

- ACC-003: Session state survives process restart (load from disk).
  - Evidence: Create session, simulate restart, load session, verify state intact.
  - Audit: Verify all fields round-trip through JSON serialization.

- ACC-004: WebSocket events are streamed for `shaping:block_added` and
  `shaping:phase_changed` when blocks are added or phase transitions.
  - Evidence: Test uses WebSocket client, creates session, verifies events arrive.
  - Audit: Verify event format matches the contract above.

- ACC-005: `GET /shaping/sessions` lists active sessions. `DELETE` ends a session.
  - Evidence: Test creates multiple sessions, lists, deletes one, verifies list shrinks.

- ACC-006: Backend tests pass (`pytest`). Frontend builds.
  - Evidence: Test output and build output.

## Current State

Ready to start. This is the first ticket in the shaping sessions implementation.
No dependencies on other shaping tickets. Follows existing patterns from
`chat/session.py` and `state/models.py`.

## Journal

- 2026-05-26: Created ticket. First in the shaping sessions plan. Establishes the
  data model and persistence that all subsequent tickets build on.
