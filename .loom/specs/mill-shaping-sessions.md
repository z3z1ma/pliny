# Design Room Shaping Sessions

ID: spec:mill-shaping-sessions
Type: Spec
Status: draft
Created: 2026-05-26
Updated: 2026-05-26

## Summary

The Design Room's highest-leverage feature is not the Markdown editor or the chat
panel. It is a distinct interaction surface for **shaping sessions**: sustained,
multi-turn collaborative processes between an operator and an AI agent that
progressively materialize a coherent subgraph of Loom records.

A shaping session is fundamentally different from:
- Chat (unbounded, unstructured, ephemeral, no staged output)
- Editing (single-document, mechanical, no collaborative discovery)
- Form-filling (rigid, no learning, no adaptation)

A shaping session is an evolving shared workspace where the agent and operator
explore intent, narrow scope, resolve ambiguity, and progressively materialize
records—all visible in a staging area before anything touches disk.

## Behavioral Intent

### What a shaping session IS

A 10-60 minute interactive process where:

1. The operator arrives with a text dump of thoughts—raw, unstructured intent
2. Deep agents (opencode, claude, etc.) with bash and filesystem access perform
   bounded explorations of the codebase, existing records, and domain context
3. These explorations feed into a growing **internal context document**—a monolithic
   Markdown corpus that accumulates everything the session knows, preventing
   redundant re-exploration of the same ground
4. From that context, the agent surfaces contradictions, ambiguities, missing
   pieces, and design questions back to the operator
5. As understanding develops, the agent proposes record drafts into a **staging
   area**: tickets, specs, plans, research notes
6. The operator sees the growing subgraph, can edit individual drafts, ask for
   changes, reject proposals, redirect, or explore branching directions
7. The agent maintains coherence across the staged records
8. When the operator is satisfied, they commit the staged subgraph to disk
9. A durable session record captures the reasoning path that led to the output

### What a shaping session is NOT

- A chatbot conversation with side effects
- A wizard/form with sequential steps
- An auto-generator that dumps 20 tickets without collaboration
- A simple command ("make tickets for this")
- A thin wrapper over chat with a staging panel added

### Resolved Design Decisions

**Input model**: No templates or presets. The operator provides initial input as a
raw text dump of thoughts. This is the seed. Everything else emerges from
exploration and interaction.

**Context acquisition**: Deep agents with bash/filesystem access (the same harnesses
used by workstations—opencode, claude, codex, etc.) perform bounded exploration
runs. All reasoning comes from model invocations, not from static templates or
canned questions.

**Internal context document**: A growing Markdown document internal to the session
that accumulates context across harness invocations. This prevents re-exploring the
whole codebase on each turn. Agents make bounded iterations against this shared
corpus, surfacing contradictions, ambiguities, and questions. This is the session's
"memory" and reasoning substrate.

**Parallel harness invocations**: The engine may launch multiple bounded harness
runs in parallel with different goals (e.g., one exploring the auth code while
another examines the existing spec). Results merge into the internal context document.

**Branching**: Supported. The operator can explore two different directions before
committing one. The staging area shows branches as distinct subgraphs.

**Durable session records**: Yes. Committed sessions produce a durable record
(research note or knowledge record) that captures the reasoning path, decisions
made, and context gathered—not just the output records.

**Interaction engine**: New, purpose-built. Not chat with extras. Not the existing
harness subprocess piping. A new backend service that orchestrates bounded agent
invocations, manages the internal context document, tracks session state, and
streams structured interaction elements to the frontend.

### The interaction texture

The experience should feel like working with a skilled engineering lead who:
- Asks "what should this explicitly NOT become?" before writing scope
- Notices when two proposed tickets would fight over the same code
- Points out "you said X here but Y there—which is true?"
- Offers concrete options ("I see three ways to slice this—here's the tradeoff")
- Admits uncertainty ("I'm not sure whether this should be one ticket or two—
  what's your intuition on the complexity?")
- Adapts the question style based on what's already clear vs. what's still fuzzy

## Requirements

### REQ-001: Session lifecycle

A shaping session has explicit lifecycle states:
- **exploring**: gathering context, asking broad questions
- **narrowing**: focused questions on specific ambiguities
- **proposing**: actively drafting records into the staging area
- **refining**: iterating on staged records based on feedback
- **ready**: operator has reviewed staged records and is ready to commit

Transitions are fluid. The agent can return to earlier phases when new information
changes the picture. The operator can force any transition.

### REQ-002: Staging area

Staged records exist in memory (and optionally persisted to `.mill/shaping-sessions/`)
but are NOT written to `.loom/` until explicit commit. The staging area:
- Shows each proposed record with its type, title, and status
- Shows relationships between staged records (visual graph)
- Allows inline editing of any staged record
- Allows deletion/rejection of any staged record
- Shows diffs when the agent proposes changes to existing records
- Shows the aggregate: "This session will create 4 tickets, 1 plan, modify 1 spec"

### REQ-003: Agent interaction model

The agent drives the conversation through structured interaction, not free-form
chat. Interaction primitives include:
- **Questions**: focused prompts that narrow the design space (presented as cards
  the operator can answer, skip, or redirect)
- **Proposals**: draft records or record modifications the agent materializes into
  the staging area
- **Observations**: things the agent noticed from inspecting the codebase, existing
  records, or operator answers
- **Options**: when multiple valid directions exist, presented as selectable paths
  with tradeoffs named
- **Challenges**: when the agent notices inconsistency, scope creep, or missing
  pieces

These are not chat messages. They are typed interaction elements with their own
rendering and response affordances.

### REQ-004: Session persistence

Sessions survive page refresh and can be resumed. Session state includes:
- Conversation history (agent questions + operator responses)
- Staged records (current drafts)
- Context gathered (files inspected, records read, decisions made)
- Current phase

### REQ-005: Commit flow

When the operator commits the staged subgraph:
- All staged records are written atomically to their `.loom` directories
- References between them are correct (using actual IDs)
- A commit is created with a meaningful message
- The session is archived (can be reviewed later but not resumed)
- The Design Room navigates to the plan or first record

### REQ-006: Subgraph isolation

During shaping, the staged records are visually distinct from existing records.
The operator can:
- See only their staged records (isolated view)
- See staged records in context of existing records (contextual view)
- Toggle between these views

### REQ-007: Coherence maintenance

The agent is responsible for cross-record coherence:
- No duplicate scope between tickets
- References between staged records use correct IDs
- Acceptance criteria don't contradict other tickets
- Plan execution units match their child tickets
- Dependencies are correctly modeled

When the operator edits a staged record in a way that breaks coherence, the agent
should surface the issue (not silently fix it or ignore it).

## Scenarios

### SCN-001: Operator shapes a complex feature

Operator opens a new shaping session and says "I want to add graph visualization
to the Design Room."

Agent inspects existing specs and code, then asks:
- "What records should appear as nodes? All types, or specific surfaces?"
- "Is this for understanding relationships between records, or for navigation?"
- "Should it replace the sidebar, augment it, or be a separate view?"

As answers come in, the agent proposes records: a spec for graph behavior, a plan
with execution units, child tickets for rendering, data, and interaction. Each
appears in the staging area as it's proposed. The operator reviews, asks for changes
to one ticket's scope, and the agent adjusts related tickets' non-goals accordingly.

After 20 minutes, the operator commits 1 spec + 1 plan + 4 tickets.

### SCN-002: Operator shapes a bug investigation

Operator opens a session: "Notifications show undefined."

Agent inspects the notification code, finds the root cause, and proposes a single
ticket with detailed scope, related records, and acceptance. Session is short (2
minutes) because the work is obvious. One ticket staged and committed.

### SCN-003: Operator mid-session realizes scope should split

During shaping, the operator says "actually, the auth changes and the permission
changes should be separate work."

The agent splits its staged ticket into two tickets, updates the plan's execution
units, and adjusts references. Both appear in the staging area showing the split.

### SCN-004: Session resume

Operator shaped 15 tickets yesterday but didn't commit. Today they open the
session, see the staged subgraph, and resume from where they left off. The agent
remembers context and can continue asking questions or accept commit.

## Boundaries

### What this spec does NOT cover
- The implementation of the AI agent's reasoning/prompting strategy
- The specific harness or model used for the agent's responses
- The Markdown editor (separate existing component)
- The existing chat panel (remains available as a simpler alternative)
- Real-time collaboration between multiple humans

### Open Questions

- **OQ-007**: What is the exact interaction rendering model? The operator rejected
  structured-chat-as-MVP and wants a fully novel experience. What visual primitives
  compose the interaction stream? Cards? Inline-editable blocks? A conversation
  that embeds structured elements? Something else?

- **OQ-008**: How does the operator steer branching? Does the agent propose a fork
  ("I see two directions—A or B"), and the operator picks? Or can the operator
  explicitly say "explore both and show me"? How is the unchosen branch represented?

- **OQ-009**: How does the internal context document relate to the staging area?
  Is the context document visible to the operator, or is it purely agent-internal?
  Can the operator see "what the agent knows so far"?

- **OQ-010**: What are the boundaries of bounded parallel harness invocations? How
  many can run simultaneously? How is the operator notified when they complete? Can
  the operator interrupt/cancel an in-flight exploration?

- **OQ-011**: How do sessions compose with existing Design Room state? If the
  operator already has a document open in the editor, does starting a shaping
  session replace the editor panel, or does it become a new mode alongside it?

## Evidence Expectations

- A shaping session that produces multiple records with correct cross-references
- Session resume working across page refreshes
- Staging area showing records before they're committed to disk
- Agent asking questions that adapt based on previous answers
- Conflict detection when operator edits break coherence

## Related Records

- `spec:mill-design-room` - Design Room behavior contract
- `loom-mill/frontend/src/lib/design/ChatPanel.svelte` - existing chat (simpler interface)
- `loom-mill/frontend/src/lib/design/DesignRoom.svelte` - Design Room container
- `.loom/plans/` - example of multi-record shaped output
