# Bounded Harness Orchestration for Shaping Sessions

ID: ticket:20260526-mill-shaping-harness
Type: Ticket
Status: review
Created: 2026-05-26
Updated: 2026-05-26
Risk: medium - parallel subprocess management with shared mutable state (context doc); race conditions possible
Depends On: ticket:20260526-mill-shaping-foundation

## Summary

Add the ability for a shaping session to launch bounded harness invocations—deep
agent subprocesses (opencode, claude, codex) with filesystem access that explore
the codebase and produce meaningful context. Multiple invocations can run in
parallel with different goals. Results merge into the session's internal context
document.

This is the "exploration muscle" of the shaping engine. After this ticket, the
engine can send agents out to gather information, and the results accumulate in a
shared corpus that prevents redundant re-exploration.

Closure claim: The shaping engine can launch multiple bounded harness invocations
in parallel, stream their output as events, merge results into the context doc,
and support cancellation.

## Related Records

- `plan:20260526-mill-shaping-sessions` - parent plan
- `ticket:20260526-mill-shaping-foundation` - builds on session foundation
- `spec:mill-shaping-sessions` - behavioral contract (harness invocation section)
- `loom-mill/src/loom_mill/chat/harness.py` - existing single-subprocess harness
- `loom-mill/src/loom_mill/workstation/engine.py` - existing process lifecycle with capture tasks

## Scope

Write:
- `loom-mill/src/loom_mill/shaping/harness.py` — bounded invocation runner
- `loom-mill/src/loom_mill/shaping/orchestrator.py` — parallel invocation management
- `loom-mill/src/loom_mill/shaping/session.py` — extend with exploration methods
- `loom-mill/src/loom_mill/api/shaping.py` — add exploration trigger endpoint
- `loom-mill/tests/test_shaping_harness.py` — test coverage

Read:
- `loom-mill/src/loom_mill/chat/harness.py` — single-invocation pattern
- `loom-mill/src/loom_mill/workstation/engine.py` — process lifecycle, capture streams

Non-goals:
- Do NOT implement the "agent reasoning" that decides WHAT to explore (ticket 3)
- Do NOT implement staged record proposals (ticket 4)
- Do NOT build the frontend exploration indicator (ticket 5)
- Do NOT add exploration scheduling/prioritization (future optimization)

## Detailed Design

### Invocation Model

A **bounded invocation** is a single harness subprocess that:
- Receives a **goal** (what it should explore or produce)
- Receives **context** (relevant excerpts from the session context document)
- Has filesystem access (bash, read/write)
- Produces **output** (text streamed via stdout)
- Has a **timeout** (default 120s, configurable)
- Returns **exit code + full output** when done

```python
# loom_mill/shaping/harness.py

@dataclass
class InvocationConfig:
    goal: str                    # what this invocation should accomplish
    context_excerpt: str         # relevant context doc section (not full doc every time)
    command: str                 # harness command (e.g., "opencode")
    args: list[str] = field(default_factory=list)
    env: dict[str, str] = field(default_factory=dict)
    cwd: str | None = None
    timeout_seconds: float = 120.0

@dataclass
class InvocationResult:
    invocation_id: str
    goal: str
    exit_code: int
    output: str                  # full stdout
    stderr: str                  # full stderr (for debugging)
    duration_seconds: float
    context_summary: str         # agent-generated summary of what was learned
    # The context_summary is extracted from the output (last section or explicit marker)

async def run_bounded_invocation(
    config: InvocationConfig,
    invocation_id: str,
    on_stream: Callable[[str], None] | None = None,
) -> InvocationResult:
    """
    Launch a bounded harness invocation.
    
    Constructs a prompt that includes:
    1. The goal statement
    2. Relevant context excerpt
    3. Instructions to produce a structured output ending with "## Summary"
    
    Streams output line-by-line via on_stream callback.
    Returns the full result when done.
    """
    ...
```

### Prompt Construction for Invocations

Each invocation receives a prompt piped to stdin that structures what the agent
should do:

```markdown
# Exploration Goal

{config.goal}

# Session Context (relevant excerpt)

{config.context_excerpt}

# Instructions

Explore the goal above. You have full filesystem access. Use bash, read files,
inspect code.

When you're done, end your output with a section:

## Summary

Provide a concise summary (3-10 lines) of what you discovered that's relevant
to the shaping session. This summary will be added to the session's context
document for future reference.
```

### Orchestrator

```python
# loom_mill/shaping/orchestrator.py

class ShapingOrchestrator:
    """Manages parallel bounded invocations for a shaping session."""
    
    def __init__(self, session: ShapingSession, store: MillStateStore, harness_config: HarnessConfig):
        self.session = session
        self.store = store
        self.harness_config = harness_config
        self._active: dict[str, asyncio.Task] = {}
        self._results: dict[str, InvocationResult] = {}
    
    async def launch(self, goal: str, context_excerpt: str | None = None) -> str:
        """
        Launch a bounded invocation. Returns invocation_id.
        
        - Generates invocation_id
        - Adds EXPLORATION_START block to session
        - Publishes shaping:exploration_start event
        - Starts background task that runs the invocation
        - When done: adds EXPLORATION_COMPLETE block, merges context, publishes event
        """
        invocation_id = str(uuid4())
        
        # If no excerpt provided, use last N bytes of context doc
        if context_excerpt is None:
            full_context = self.session.read_context()
            context_excerpt = full_context[-4000:]  # Last 4K as default excerpt
        
        config = InvocationConfig(
            goal=goal,
            context_excerpt=context_excerpt,
            command=self.harness_config.command,
            args=self.harness_config.args,
            env=self.harness_config.env or {},
            cwd=self.harness_config.cwd,
        )
        
        # Record start
        self.session.add_block(InteractionBlock(
            id=str(uuid4()),
            type=BlockType.EXPLORATION_START,
            timestamp=utc_now(),
            content={"invocation_id": invocation_id, "goal": goal, "command": config.command}
        ))
        self.store.publish(ShapingEvent(
            session_id=self.session.session_id,
            event="exploration_start",
            data={"invocation_id": invocation_id, "goal": goal}
        ))
        
        # Launch background task
        task = asyncio.create_task(self._run(invocation_id, config))
        self._active[invocation_id] = task
        self.session.state.active_explorations.append(invocation_id)
        
        return invocation_id
    
    async def cancel(self, invocation_id: str) -> bool:
        """Cancel an in-flight invocation."""
        task = self._active.get(invocation_id)
        if task and not task.done():
            task.cancel()
            return True
        return False
    
    async def _run(self, invocation_id: str, config: InvocationConfig) -> None:
        """Background task for a single invocation."""
        try:
            def on_stream(line: str):
                # Publish streaming event (opt-in detail for frontend)
                self.store.publish(ShapingEvent(
                    session_id=self.session.session_id,
                    event="exploration_stream",
                    data={"invocation_id": invocation_id, "delta": line}
                ))
            
            result = await run_bounded_invocation(config, invocation_id, on_stream=on_stream)
            self._results[invocation_id] = result
            
            # Merge summary into context document
            self.session.append_context(
                f"## Exploration: {config.goal}",
                result.context_summary or result.output[-2000:]
            )
            
            # Record completion
            context_size = len(self.session.read_context())
            self.session.add_block(InteractionBlock(
                id=str(uuid4()),
                type=BlockType.EXPLORATION_COMPLETE,
                timestamp=utc_now(),
                content={
                    "invocation_id": invocation_id,
                    "summary": result.context_summary or "(no summary produced)",
                    "context_added": len(result.context_summary or ""),
                    "exit_code": result.exit_code,
                    "duration_seconds": result.duration_seconds,
                }
            ))
            self.store.publish(ShapingEvent(
                session_id=self.session.session_id,
                event="exploration_complete",
                data={
                    "invocation_id": invocation_id,
                    "summary": result.context_summary or "(no summary produced)",
                    "exit_code": result.exit_code,
                }
            ))
        except asyncio.CancelledError:
            self.session.add_block(InteractionBlock(
                id=str(uuid4()),
                type=BlockType.SYSTEM,
                timestamp=utc_now(),
                content={"message": f"Exploration cancelled: {config.goal}"}
            ))
        finally:
            self._active.pop(invocation_id, None)
            if invocation_id in self.session.state.active_explorations:
                self.session.state.active_explorations.remove(invocation_id)
            self.session._persist_state()
    
    @property
    def active_count(self) -> int:
        return len(self._active)
    
    def get_result(self, invocation_id: str) -> InvocationResult | None:
        return self._results.get(invocation_id)
```

### API Endpoints (additions)

```python
# POST /shaping/sessions/{session_id}/explore
# Body: {"goal": "Explore the auth module and identify existing permission patterns"}
# Returns: {"invocation_id": "...", "goal": "..."}
# Launches a bounded invocation.

# POST /shaping/sessions/{session_id}/explore/{invocation_id}/cancel
# Returns: {"cancelled": true|false}
# Cancels an in-flight invocation.

# GET /shaping/sessions/{session_id}/explorations
# Returns: [{"invocation_id": "...", "goal": "...", "status": "running"|"complete"|"cancelled", "summary": "..."}]
# Lists all explorations for the session.
```

### Context Document Growth Pattern

The context document grows as a series of sections:

```markdown
# Shaping Session

## Operator Input

I want to add graph visualization to the Design Room...

## Exploration: Examine existing record reference parsing

Found that records already have `references` and `depends_on` fields parsed
in `loom_mill/parser/parse.py`. The frontend receives these via WebSocket
snapshot. No backend graph API exists but the data is available client-side...

## Exploration: Check existing Design Room layout structure

DesignRoom.svelte uses a three-panel layout with GraphSidebar, DocumentEditor,
and ChatPanel. The center panel already supports mode switching between editor
and graph views...

## Operator Response

I want both a force-directed view and a DAG view. The DAG should use the
Loom ontology hierarchy...
```

### Concurrency Safety

Multiple invocations may try to append to the context document simultaneously.
Use a file lock or asyncio Lock to serialize writes:

```python
class ShapingSession:
    def __init__(self, ...):
        ...
        self._context_lock = asyncio.Lock()
    
    async def append_context(self, heading: str, content: str) -> int:
        async with self._context_lock:
            existing = self._context_path.read_text(encoding="utf-8")
            new_content = existing + f"\n{heading}\n\n{content}\n"
            self._context_path.write_text(new_content, encoding="utf-8")
            return len(new_content)
```

## Acceptance

- ACC-001: `POST /shaping/sessions/{id}/explore` launches a bounded harness
  subprocess that runs the configured command with the goal as a prompt.
  - Evidence: Test launches exploration with echo harness, verifies subprocess runs and returns output.
  - Audit: Verify timeout, proper cleanup on exit.

- ACC-002: Multiple explorations can run in parallel within the same session.
  - Evidence: Launch 3 explorations simultaneously, verify all complete, context doc has 3 sections.
  - Audit: Verify no race conditions in context doc writes.

- ACC-003: Exploration results are merged into the context document under a heading.
  - Evidence: After exploration, read context doc, verify new section appended with summary.
  - Audit: Verify context doc is valid Markdown, sections are ordered chronologically.

- ACC-004: WebSocket events are streamed: `shaping:exploration_start`,
  `shaping:exploration_stream` (opt-in), `shaping:exploration_complete`.
  - Evidence: Test uses WebSocket client, launches exploration, verifies event sequence.

- ACC-005: `POST .../cancel` stops an in-flight invocation and records cancellation.
  - Evidence: Launch slow exploration, cancel it, verify task is cancelled, block is added.

- ACC-006: Backend tests pass. Frontend builds.
  - Evidence: Test output.

## Current State

Implementation is complete and ready for review. Added the bounded harness runner,
parallel shaping orchestrator, exploration API endpoints, route registration, and
focused backend tests. Verification passed for the focused harness suite, the full
backend suite, and the frontend build. `git diff --check` is blocked by pre-existing
trailing whitespace in `loom-mill/frontend/src/lib/design/GraphSidebar.svelte`,
which is outside this ticket's write scope.

## Journal

- 2026-05-26: Implemented bounded harness orchestration and moved to review.
  Evidence: `uv run --extra dev python -m pytest tests/test_shaping_harness.py -x`
  passed 6 tests; `uv run --extra dev python -m pytest tests/ -x` passed 75 tests;
  `npm --prefix loom-mill/frontend run build` succeeded with existing Svelte/a11y
  warnings. `git diff --check` reports unrelated trailing whitespace in
  `GraphSidebar.svelte` lines 3 and 150.
- 2026-05-26: Marked active and began implementation from the ticket boundary.
- 2026-05-26: Created ticket. Second in the shaping sessions plan. Adds the
  exploration capability that feeds the context document.
