# Interaction Block Engine

ID: ticket:20260526-mill-shaping-blocks
Type: Ticket
Status: review
Created: 2026-05-26
Updated: 2026-06-09
Risk: high - core novelty of the feature; agent reasoning quality directly determines UX quality; prompt engineering intensive
Depends On: ticket:20260526-mill-shaping-harness

## Summary

The interaction block engine is the brain of the shaping session. It reads the
operator's input and the accumulated context document, then decides what to do
next: ask a question, make an observation, propose a record, suggest a branch
point, or launch more exploration.

It produces these decisions by invoking the harness (the same deep agents used for
exploration) with a carefully structured prompt that includes the current context,
the session history, and instructions for what kind of output to produce.

This is the hardest and most important ticket. The quality of the agent's questions,
observations, and proposals determines whether the shaping experience feels like
working with a brilliant collaborator or a mediocre chatbot.

Closure claim: Given operator input and accumulated context, the engine produces
meaningful structured interaction blocks that advance the shaping conversation
toward materialized records.

## Related Records

- `plan:20260526-mill-shaping-sessions` - parent plan
- `ticket:20260526-mill-shaping-harness` - provides bounded invocations
- `spec:mill-shaping-sessions` - interaction texture description
- `loom-mill/src/loom_mill/shaping/orchestrator.py` - invocation infrastructure

## Scope

Write:
- `loom-mill/src/loom_mill/shaping/engine.py` — the core reasoning loop
- `loom-mill/src/loom_mill/shaping/prompts.py` — prompt templates for each reasoning mode
- `loom-mill/src/loom_mill/shaping/parser.py` — parse agent output into typed blocks
- `loom-mill/src/loom_mill/api/shaping.py` — extend with "advance" endpoint
- `loom-mill/tests/test_shaping_engine.py` — test coverage

Read:
- `loom-mill/src/loom_mill/shaping/session.py` — session state
- `loom-mill/src/loom_mill/shaping/orchestrator.py` — invocation launching

Non-goals:
- Do NOT implement the staging area CRUD or commit (ticket 4)
- Do NOT build the frontend (ticket 5)
- Do NOT optimize prompt size or caching (future optimization)
- Do NOT add fine-grained prompt configuration (ship one good default)

## Detailed Design

### Core Loop

The engine operates on a simple loop:

```
1. Operator provides input (or session just started)
2. Engine reads: context doc + recent blocks + session phase
3. Engine decides: what type of block to produce next
4. Engine invokes harness with structured prompt for that block type
5. Engine parses harness output into typed InteractionBlock(s)
6. Blocks are added to session state + streamed to frontend
7. If the block is a question, wait for operator response → goto 1
8. If the block is a proposal, add to staging → continue to next block
9. If the engine decides more exploration is needed → launch exploration → wait → goto 2
```

### Engine Class

```python
# loom_mill/shaping/engine.py

class ShapingEngine:
    """Drives the shaping conversation by producing interaction blocks."""
    
    def __init__(self, session: ShapingSession, orchestrator: ShapingOrchestrator, store: MillStateStore):
        self.session = session
        self.orchestrator = orchestrator
        self.store = store
    
    async def advance(self) -> list[InteractionBlock]:
        """
        Produce the next interaction block(s) based on current state.
        
        Called after:
        - Session creation (initial exploration + first question)
        - Operator input (response to a question or new direction)
        - Exploration completion (now have more context to reason from)
        
        Returns the blocks produced (may be 1 or several in sequence).
        """
        context = self.session.read_context()
        recent_blocks = self.session.state.blocks[-20:]  # Last 20 blocks for recency
        phase = self.session.state.phase
        
        # Decide what to do next
        decision = await self._decide_next_action(context, recent_blocks, phase)
        
        blocks = []
        if decision.action == "explore":
            # Need more context before we can shape
            invocation_id = await self.orchestrator.launch(
                goal=decision.goal,
                context_excerpt=decision.context_excerpt
            )
            # Exploration blocks are added by the orchestrator
            # After exploration completes, advance() will be called again
            
        elif decision.action == "question":
            block = InteractionBlock(
                id=str(uuid4()),
                type=BlockType.AGENT_QUESTION,
                timestamp=utc_now(),
                content={
                    "question": decision.question,
                    "options": decision.options,  # None for open-ended
                    "context_ref": decision.context_ref,
                }
            )
            self.session.add_block(block)
            self._publish_block(block)
            blocks.append(block)
            
        elif decision.action == "observation":
            block = InteractionBlock(
                id=str(uuid4()),
                type=BlockType.AGENT_OBSERVATION,
                timestamp=utc_now(),
                content={
                    "observation": decision.observation,
                    "evidence": decision.evidence,
                }
            )
            self.session.add_block(block)
            self._publish_block(block)
            blocks.append(block)
            # After observation, continue reasoning (may produce more blocks)
            
        elif decision.action == "propose":
            block = InteractionBlock(
                id=str(uuid4()),
                type=BlockType.AGENT_PROPOSAL,
                timestamp=utc_now(),
                content={
                    "temp_id": decision.record_temp_id,
                    "surface": decision.record_surface,
                    "title": decision.record_title,
                    "content": decision.record_content,
                }
            )
            self.session.add_block(block)
            self._publish_block(block)
            blocks.append(block)
            # Staging area addition handled by ticket 4
            
        elif decision.action == "branch":
            block = InteractionBlock(
                id=str(uuid4()),
                type=BlockType.BRANCH_POINT,
                timestamp=utc_now(),
                content={
                    "branches": decision.branches,
                    "reasoning": decision.reasoning,
                }
            )
            self.session.add_block(block)
            self._publish_block(block)
            blocks.append(block)
        
        return blocks
    
    async def _decide_next_action(self, context: str, recent_blocks: list, phase: SessionPhase) -> Decision:
        """
        Use a harness invocation to reason about what to do next.
        
        This is the critical prompt. It receives:
        - The full context document (or truncated if too large)
        - Recent interaction blocks (formatted as history)
        - The current phase
        - Instructions for what kind of output to produce
        
        The harness output is parsed into a Decision object.
        """
        prompt = build_decision_prompt(context, recent_blocks, phase)
        result = await run_bounded_invocation(
            InvocationConfig(
                goal="Decide next shaping action",
                context_excerpt="",  # context is embedded in prompt
                command=self.orchestrator.harness_config.command,
                args=self.orchestrator.harness_config.args,
                timeout_seconds=60.0,
            ),
            invocation_id=f"decision-{uuid4().hex[:8]}",
            on_stream=None,  # Don't stream decision reasoning to user
            prompt_override=prompt,  # Use custom prompt instead of goal-based template
        )
        return parse_decision(result.output)
    
    def _publish_block(self, block: InteractionBlock):
        self.store.publish(ShapingEvent(
            session_id=self.session.session_id,
            event="block_added",
            data={"block": asdict(block)}
        ))
```

### Decision Prompt

The decision prompt is the soul of the interaction quality. It must:

1. Convey the operator's raw intent clearly
2. Show what context has already been gathered
3. Show what questions have already been asked/answered
4. Indicate the current phase and what's expected
5. Request a structured output that can be parsed

```python
# loom_mill/shaping/prompts.py

def build_decision_prompt(context: str, recent_blocks: list, phase: SessionPhase) -> str:
    history = format_block_history(recent_blocks)
    
    return f"""You are a shaping agent in a Loom session. Your job is to help the operator
shape their fuzzy intent into concrete Loom records (tickets, specs, plans, research).

## Current Phase: {phase.value}

## Internal Context Document (what we know so far)

{context[-8000:]}

## Recent Interaction History

{history}

## Your Task

Based on the context and history above, decide your SINGLE next action.
Output EXACTLY ONE of these structured blocks:

### If you need more information from the codebase:
```action
type: explore
goal: <what to explore and why>
```

### If you need to ask the operator a question:
```action
type: question
question: <the question>
options: <comma-separated options, or "open" for free-text>
context_ref: <what part of the context this relates to>
```

### If you discovered something the operator should know:
```action
type: observation
observation: <what you noticed>
evidence: <file paths, code snippets, or record refs that support this>
```

### If you're ready to propose a record:
```action
type: propose
surface: <tickets|specs|plans|research>
title: <record title>
content: <full Markdown content of the proposed record>
```

### If you see multiple valid directions:
```action
type: branch
branches: <branch_a_label> | <branch_b_label>
reasoning: <why these are materially different paths>
```

## Guidelines

- Ask ONE focused question at a time, not a list
- Questions should narrow the design space, not gather information you could find yourself
- Before proposing, verify you have enough context from exploration
- Proposals should be detailed, complete records (not stubs)
- Observe contradictions, missing pieces, scope creep, and incoherence
- If the operator gave a clear enough direction, propose records rather than asking more
- Move toward proposing records as quickly as the certainty allows
"""
```

### Output Parser

```python
# loom_mill/shaping/parser.py

@dataclass
class Decision:
    action: str                  # "explore" | "question" | "observation" | "propose" | "branch"
    # Action-specific fields:
    goal: str | None = None
    context_excerpt: str | None = None
    question: str | None = None
    options: list[str] | None = None
    context_ref: str | None = None
    observation: str | None = None
    evidence: list[str] | None = None
    record_temp_id: str | None = None
    record_surface: str | None = None
    record_title: str | None = None
    record_content: str | None = None
    branches: list[dict] | None = None
    reasoning: str | None = None

def parse_decision(output: str) -> Decision:
    """
    Parse the harness output into a typed Decision.
    
    Looks for ```action ... ``` blocks and extracts key-value pairs.
    Falls back to treating the entire output as an observation if parsing fails.
    """
    ...
```

### API Endpoint

```python
# POST /shaping/sessions/{session_id}/advance
# Body: {} (empty - just triggers the engine to produce next block)
# Returns: {"blocks": [...]} — the blocks produced
#
# Called after:
# - Session creation (to start the conversation)
# - Operator input (to continue after answering)
# - Exploration completion (to reason with new context)
#
# May trigger further explorations internally before returning blocks.
# Long-running: may take 30-60s for complex reasoning chains.
# Consider making this a streaming endpoint or using WebSocket events for results.
```

### Phase Transitions

The engine automatically transitions phases based on conversation progress:

- `exploring` → `narrowing`: when initial explorations complete and first question asked
- `narrowing` → `proposing`: when enough questions answered to start drafting records
- `proposing` → `refining`: when operator edits/rejects a proposal
- `refining` → `ready`: when operator accepts all proposals (detected by staging area state)

## Acceptance

- ACC-001: After operator provides initial input and `advance()` is called, the
  engine produces at least one meaningful block (exploration, question, or observation).
  - Evidence: Test with real or echo harness, verify block is produced and makes sense given input.
  - Audit: Verify prompt includes operator input and context.

- ACC-002: After exploration completes and `advance()` is called, the engine uses
  the new context to produce a more informed block.
  - Evidence: Seed context with codebase info, advance, verify block references discovered info.

- ACC-003: After operator answers a question, `advance()` incorporates the answer
  into its reasoning and moves toward proposals.
  - Evidence: Multi-turn test: input → question → answer → proposal (or next question).

- ACC-004: The engine can produce `AGENT_PROPOSAL` blocks with complete, well-formed
  Markdown record content.
  - Evidence: Advance until proposal, verify content is valid Loom record Markdown.
  - Audit: Verify proposed records have correct structure (ID, Type, Status, etc.).

- ACC-005: Decision parsing handles malformed harness output gracefully (fallback
  to observation block, not crash).
  - Evidence: Test with intentionally garbled output, verify graceful degradation.

- ACC-006: Backend tests pass.
  - Evidence: Test output.

## Evidence

- `evidence:20260526-mill-shaping-blocks-engine-validation` - focused engine tests,
  full backend tests, frontend build, and whitespace checks for touched files.

## Current State

Implementation is complete and ready for review/audit. The engine, parser, prompt
templates, advance API endpoint, and tests are in place. Validation passed for the
focused engine suite, full backend suite, and frontend build. A separate audit pass
is still needed before closure because this is high-risk core reasoning behavior.

Current follow-up review found engine/parser issues that affect this ticket's
acceptance: invalid continue/revise paths must fail closed, revise must stale the
full affected branch rather than only direct children, and parser op tags embedded
inside record Markdown must not execute. Those fixes have been implemented,
adversarially reviewed, and covered by focused verification; this ticket remains
in review until acceptance disposition is reconciled.

## Journal

- 2026-06-09: Reconciled stale ledger state after the current implementation
  review. Three of the nine follow-up findings touch this ticket's engine/parser
  behavior; fixes are implemented and covered by focused backend tests.
- 2026-05-26: Started implementation in the current session. Read the ticket,
  related plan/spec, and shaping session/harness/orchestrator/API seams. Small
  harness prompt override is needed so the engine can reuse bounded invocations
  for internal decision prompts without streaming reasoning to the user.
- 2026-05-26: Implemented the decision parser, prompt templates, shaping engine,
  advance API endpoint, and focused tests. Validation evidence recorded in
  `evidence:20260526-mill-shaping-blocks-engine-validation`; moved ticket to
  review pending audit.
- 2026-05-26: Created ticket. Third in the shaping sessions plan. This is the
  core novelty—the agent reasoning that drives meaningful shaping conversations.
