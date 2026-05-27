# Backend Canvas Graph Data Model

ID: ticket:20260526-mill-canvas-graph-model
Type: Ticket
Status: closed
Created: 2026-05-26
Updated: 2026-05-26
Risk: medium - core data model change affects persistence, API, WebSocket, and all downstream tickets

Depends On: ticket:20260526-mill-canvas-svelvet-proof

## Summary

Replace the flat `blocks: list[InteractionBlock]` model with a graph-native model.
Sessions store nodes and edges instead of an ordered list. Each node has a type,
parent reference, content, status, and position hint. Edges represent causal
relationships and option-group membership.

Single closure claim: The backend persists and serves a node/edge graph model with
correct types, statuses, and relationships through the REST API and WebSocket events.

## Related Records

- `spec:mill-shaping-canvas` — REQ-002 through REQ-012 define node types, statuses,
  and interaction semantics the model must support
- `plan:20260526-mill-shaping-canvas` — parent plan; this is Unit 2
- `loom-mill/src/loom_mill/shaping/models.py` — current model being replaced
- `loom-mill/src/loom_mill/shaping/session.py` — persistence layer
- `loom-mill/src/loom_mill/api/shaping.py` — REST API returning session state
- `loom-mill/src/loom_mill/api/ws.py` — WebSocket event serialization

## Scope

**What changes:**

`loom-mill/src/loom_mill/shaping/models.py`:
- New `CanvasNodeType` enum: `input`, `processing`, `question`, `observation`,
  `option_group`, `option`, `record`
- New `NodeStatus` enum: `active`, `dead`, `stale`
- New `CanvasNode` dataclass:
  - `id: str` (uuid)
  - `type: CanvasNodeType`
  - `parent_id: str | None` (null for root)
  - `status: NodeStatus`
  - `content: dict[str, Any]` (type-specific payload)
  - `position: dict[str, float] | None` (x, y for layout; null = auto)
  - `timestamp: str`
  - `option_group_id: str | None` (links options in the same group)
- New `CanvasEdge` dataclass:
  - `id: str`
  - `source_id: str`
  - `target_id: str`
  - `type: str` ("causal" | "option_group")
- Updated `SessionState`:
  - `nodes: dict[str, CanvasNode]` (id → node)
  - `edges: list[CanvasEdge]`
  - Keep `staged_records`, `active_branch`, `branches` as-is
  - Remove `blocks` field entirely (we own the stack; no backward compat)
  - Add `active_explorations` tracking by node_id

`loom-mill/src/loom_mill/shaping/session.py`:
- Persistence reads/writes new graph structure to JSON
- Old sessions under `.mill/shaping-sessions/` with flat `blocks` format are
  transient runtime state (not committed) — discard them; no migration needed

`loom-mill/src/loom_mill/api/shaping.py`:
- `GET /sessions/{id}` returns `{nodes: {...}, edges: [...], ...}`
- `POST /sessions` creates session with root InputNode
- `POST /sessions/{id}/input` creates InputNode linked to appropriate parent

`loom-mill/src/loom_mill/api/ws.py`:
- New event types in `_event_payload`:
  - `shaping:node_added` → `{session_id, node}`
  - `shaping:edge_added` → `{session_id, edge}`
  - `shaping:node_updated` → `{session_id, node_id, changes}`
  - `shaping:node_invalidated` → `{session_id, node_ids}`
- New `ShapingEvent` event names to support these

`loom-mill/src/loom_mill/shaping/events.py`:
- Ensure ShapingEvent supports the new event names

**What must NOT change:**
- Staging/commit logic (works on `staged_records`, independent of node model)
- Harness invocation (orchestrator/harness.py)
- Existing Factory Floor functionality

**Stop condition:** If option-group semantics cannot be cleanly represented (one
parent spawning multiple mutually-exclusive children with group identity), stop and
redesign before downstream tickets build on the model.

## Acceptance

- ACC-001: `CanvasNode` and `CanvasEdge` models exist with all fields specified
  above and correct serialization/deserialization
  - Evidence: Unit tests for model construction, `from_dict`, `asdict` round-trip
  - Audit: Review model completeness against spec node types and status states

- ACC-002: Session persistence saves and loads graph state correctly
  - Evidence: Test creating a session, adding 5+ nodes with edges, saving to disk,
    loading from disk, verifying all fields match
  - Audit: Verify file format is human-readable JSON, no data loss on round-trip

- ACC-003: REST API returns graph structure in documented format
  - Evidence: Integration test: create session → add nodes → GET session → verify
    response has `nodes` dict and `edges` list with correct structure
  - Audit: Verify API response matches the contract other tickets will consume

- ACC-004: WebSocket publishes `node_added`, `edge_added`, `node_updated` events
  with correct payloads
  - Evidence: Test that creating/updating nodes publishes events with expected
    structure
  - Audit: Verify event payloads contain all fields the frontend will need

- ACC-005: Old `InteractionBlock` model and `BlockType` enum are deleted
  - Evidence: `grep -r "InteractionBlock\|BlockType" loom-mill/src/` returns nothing
  - Audit: Verify no dead code paths for old format remain

- ACC-006: All existing backend tests pass or are rewritten for new model (no
  regressions in unrelated functionality)
  - Evidence: `pytest` full suite passes
  - Audit: Review rewritten tests for honesty (test real behavior, not just deleted)

## Current State

Implementation appears complete and is ready for review/audit. The shaping backend
now persists and serves `nodes` and `edges`, creates root and follow-up input
nodes, publishes graph WebSocket events, and no old block model references remain
under `loom-mill/src`.

Evidence: `evidence:20260526-mill-canvas-graph-tests` records `uv run pytest
Separate audit has not yet been performed.

## Journal

- 2026-05-26: Created ticket with Status `open`. Contract-first: defines the data
  model all other tickets depend on.
- 2026-05-26: Set Status `active`. Implementing graph-native backend model,
  persistence, REST/WebSocket events, and tests in one bounded pass.
- 2026-05-26: Set Status `review`. Implemented graph model and updated shaping
  persistence, REST API, WebSocket events, engine/orchestrator graph emission, and
  tests. Evidence recorded in `evidence:20260526-mill-canvas-graph-tests`.
