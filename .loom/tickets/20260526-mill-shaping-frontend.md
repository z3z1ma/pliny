# Frontend Shaping Session UI

ID: ticket:20260526-mill-shaping-frontend
Type: Ticket
Status: closed
Created: 2026-05-26
Updated: 2026-05-26
Risk: high - novel interaction design with no prior art to copy; visual quality and interaction feel determine whether the feature succeeds
Depends On: ticket:20260526-mill-shaping-foundation

## Summary

Build the full interactive frontend for shaping sessions: the "New" button entry
point, the third Design Room mode, the vertical timeline of typed interaction
blocks, the staging sidebar, operator input affordances, exploration indicators,
proposal cards, branch tab UI, and commit flow.

This is where the novel UX lives. The timeline IS the staging area—records
materialize inline as the session progresses. The interaction stream builds the
subgraph progressively. It should feel like watching a design emerge through
collaboration, not like using a tool.

Closure claim: The operator can start a shaping session via "New", see the
interactive timeline building up, answer questions, edit proposals, switch branches,
and commit the result.

## Related Records

- `plan:20260526-mill-shaping-sessions` - parent plan
- `spec:mill-shaping-sessions` - full behavioral contract (interaction model section)
- `ticket:20260526-mill-shaping-foundation` - backend session API and events
- `loom-mill/frontend/src/lib/design/DesignRoom.svelte` - Design Room container to extend

## Scope

Write:
- `loom-mill/frontend/src/lib/design/ShapingSession.svelte` (new) — the session workspace
- `loom-mill/frontend/src/lib/design/ShapingTimeline.svelte` (new) — vertical block timeline
- `loom-mill/frontend/src/lib/design/ShapingBlock.svelte` (new) — renders a single typed block
- `loom-mill/frontend/src/lib/design/StagingPanel.svelte` (new) — sidebar with aggregate + mini-graph + commit
- `loom-mill/frontend/src/lib/design/ProposalCard.svelte` (new) — inline-editable record proposal
- `loom-mill/frontend/src/lib/design/DesignRoom.svelte` — add third mode, wire "New" to shaping
- `loom-mill/frontend/src/lib/design/GraphSidebar.svelte` — "New" button starts shaping session
- `loom-mill/frontend/src/lib/ws.svelte.ts` — add shaping session state + event handlers

Read:
- All backend shaping API endpoints
- `spec:mill-shaping-sessions` (interaction model section especially)

Non-goals:
- Do NOT implement the backend engine logic (tickets 1-4 handle that)
- Do NOT implement real-time collaboration between multiple operators
- Do NOT add session templates/presets
- Do NOT add session history/replay (future feature)

## Detailed Design

### Design Room Mode Switching

`DesignRoom.svelte` currently has two center-panel modes: Editor and Graph.
Add a third: Shaping.

```svelte
let centerMode = $state<'editor' | 'graph' | 'shaping'>('editor');
let shapingSessionId = $state<string | null>(null);

// "New" button in GraphSidebar starts shaping
function handleStartShaping() {
  centerMode = 'shaping';
  shapingSessionId = null;  // Will be set after session creation
}
```

Render:
```svelte
{#if centerMode === 'shaping'}
  <ShapingSession bind:sessionId={shapingSessionId} onExit={() => centerMode = 'editor'} />
{:else if centerMode === 'graph'}
  <GraphView ... />
{:else}
  <DocumentEditor ... />
{/if}
```

### ShapingSession.svelte — Container

The session workspace is a two-column layout:
- **Left (75%)**: The vertical timeline (ShapingTimeline)
- **Right (25%)**: The staging panel (StagingPanel)

On entry:
1. If `sessionId` is null, show a seed input area: large textarea with placeholder
   "Dump your thoughts here. What do you want to shape?" and a "Begin" button.
2. After "Begin": POST /shaping/sessions with the input, get session_id back,
   then call POST /shaping/sessions/{id}/advance to start the conversation.
3. If `sessionId` is set (resume): fetch session state, render existing blocks.

```svelte
<div class="flex h-full w-full">
  {#if !sessionId}
    <!-- Seed input -->
    <div class="flex-1 flex items-center justify-center p-8">
      <div class="w-full max-w-2xl flex flex-col gap-4">
        <h2 class="text-lg font-semibold text-text-primary">Start Shaping</h2>
        <p class="text-[12px] text-text-tertiary">
          Dump your raw thoughts. The agent will explore, ask questions, and
          propose records as the session develops.
        </p>
        <textarea
          bind:value={seedInput}
          class="w-full h-48 p-4 rounded border border-border-default bg-bg-surface
            text-[13px] text-text-primary font-mono resize-none focus:outline-none
            focus:border-accent-primary"
          placeholder="What do you want to shape? Be as raw and unstructured as you want..."
        ></textarea>
        <button
          onclick={startSession}
          disabled={!seedInput.trim() || starting}
          class="self-end px-4 py-2 rounded bg-accent-primary text-white text-[12px]
            font-medium hover:bg-accent-primary/90 disabled:opacity-50 transition-colors"
        >
          {starting ? 'Starting...' : 'Begin Shaping'}
        </button>
      </div>
    </div>
  {:else}
    <!-- Active session -->
    <div class="flex-1 min-w-0 flex flex-col overflow-hidden">
      <ShapingTimeline {sessionId} blocks={session.blocks} onRespond={handleRespond} />
    </div>
    <div class="w-72 shrink-0 border-l border-border-default overflow-y-auto">
      <StagingPanel {sessionId} records={session.stagedRecords} branches={session.branches} activeBranch={session.activeBranch} onCommit={handleCommit} />
    </div>
  {/if}
</div>
```

### ShapingTimeline.svelte — Vertical Block Timeline

A scrollable vertical timeline of interaction blocks. Each block has:
- Type icon on the left (in a subtle timeline gutter)
- Block content rendered by ShapingBlock
- Timestamp on the right

```svelte
<div class="flex flex-col gap-0 overflow-y-auto p-6">
  {#each blocks as block (block.id)}
    <div class="flex gap-3 py-3 border-b border-border-subtle/30">
      <!-- Timeline gutter -->
      <div class="w-6 flex flex-col items-center pt-1">
        <div class="w-2 h-2 rounded-full {blockColor(block.type)}"></div>
        <div class="flex-1 w-px bg-border-subtle mt-1"></div>
      </div>
      <!-- Block content -->
      <div class="flex-1 min-w-0">
        <ShapingBlock {block} onRespond />
      </div>
    </div>
  {/each}
  
  <!-- Active exploration indicators -->
  {#each activeExplorations as exp}
    <div class="flex gap-3 py-3 animate-pulse">
      <div class="w-6 flex items-center justify-center">
        <div class="w-2 h-2 rounded-full bg-accent-primary animate-ping"></div>
      </div>
      <div class="text-[11px] text-text-tertiary">
        Exploring: {exp.goal}
        <button class="ml-2 text-status-error-text" onclick={() => cancelExploration(exp.id)}>Cancel</button>
      </div>
    </div>
  {/each}
  
  <!-- Operator input area (after questions) -->
  {#if awaitingInput}
    <div class="flex gap-3 py-3">
      <div class="w-6"></div>
      <div class="flex-1">
        <textarea ... ></textarea>
        <button onclick={submitResponse}>Send</button>
      </div>
    </div>
  {/if}
</div>
```

### ShapingBlock.svelte — Typed Block Renderer

Renders a single block based on its type:

- **OPERATOR_INPUT**: Plain text in a subtle background box. Mono font.
- **AGENT_QUESTION**: Question text + optional choice buttons or text input.
  Rendered as a card with a "?" icon. If unanswered, shows response affordance.
- **AGENT_OBSERVATION**: Observation text + evidence list (file paths, code).
  Rendered as a note card with "eye" icon. May contain expandable code snippets.
- **AGENT_PROPOSAL**: Full record preview card (ProposalCard component).
  Shows title, surface badge, first few lines of content. Expandable.
  Action buttons: Accept / Reject / Edit.
- **EXPLORATION_START/COMPLETE**: Compact indicator line showing what was explored
  and what was learned. Expandable to show full output (opt-in streaming).
- **BRANCH_POINT**: Tab selector showing branch options with descriptions.
  Operator clicks one to continue on that branch.
- **SYSTEM**: Minimal gray text for lifecycle events.

### ProposalCard.svelte — Inline-Editable Record

A rich card showing a proposed record:

```
┌─────────────────────────────────────────────────────────┐
│ 🎫 ticket   ┊  Auth Permission Refactor                 │
├─────────────────────────────────────────────────────────┤
│ ID: temp:ticket:auth-permission-refactor                │
│ Status: open                                            │
│ Risk: medium - touches auth boundaries...               │
│                                                         │
│ ## Summary                                              │
│ Refactor the permission checking to use...              │
│ ...                                                     │
│                                                    ▾    │
├─────────────────────────────────────────────────────────┤
│ [✓ Accept]    [✗ Reject]    [✎ Edit]               │
└─────────────────────────────────────────────────────────┘
```

- Surface badge colored by type
- Content preview (first 8 lines, expandable)
- Edit opens inline CodeMirror editor for the full content
- Accept/Reject call staging API
- References to other staged records render as clickable links

### StagingPanel.svelte — Persistent Sidebar

Shows the aggregate state of all staged records:

```
┌───────────────────────────────┐
│ Staged Records          3 / 5 │  (accepted / total)
├───────────────────────────────┤
│ 📋 Plan                    1  │
│ 🎫 Tickets                 3  │
│ 📐 Specs                   1  │
├───────────────────────────────┤
│     ┌──┐                      │
│     │Pl│→┌──┐                 │
│     └──┘ │T1│                 │
│           └──┘→┌──┐           │
│     ┌──┐      │T2│           │
│     │Sp│→┌──┐ └──┘           │
│     └──┘ │T3│                 │
│           └──┘                 │
│     (mini graph)              │
├───────────────────────────────┤
│ Branch: main ▾                │
│ [✓ Commit (3 accepted)]      │
└───────────────────────────────┘
```

- Record count by surface type
- Mini force-directed graph of staged record relationships
- Branch selector (if branches exist)
- Commit button (enabled when at least 1 record accepted)
- Click any record in the list → scroll to its proposal in timeline

### Branch Tab UI

When a BRANCH_POINT block appears in the timeline, render tabs:

```
┌─ Branch A: Single permission service ─┬─ Branch B: Distributed checks ─┐
│ ▼ Timeline continues on this branch... │                                 │
└────────────────────────────────────────┴─────────────────────────────────┘
```

Clicking a tab filters the timeline to show only that branch's blocks below the
branch point. The staging panel updates to show only that branch's records.

### WebSocket State

In `ws.svelte.ts`, add shaping session state that updates on `shaping:*` events:

```typescript
shapingSession = $state<{
  id: string | null;
  phase: string;
  blocks: InteractionBlock[];
  stagedRecords: StagedRecord[];
  activeBranch: string;
  branches: string[];
  activeExplorations: Array<{ id: string; goal: string }>;
} | null>(null);
```

### Color Palette for Block Types

- Operator input: `bg-bg-surface-active` (neutral, quiet)
- Agent question: `border-accent-primary/30` (purple tint, draws attention)
- Agent observation: `border-status-success-border/30` (green tint, informational)
- Agent proposal: `border-accent-secondary/30` (blue tint, actionable)
- Exploration: `text-text-tertiary` (gray, background activity)
- Branch point: `bg-status-warning-bg/20` (amber, decision needed)
- System: `text-text-tertiary italic` (minimal)

### Animation & Polish

- New blocks animate in with a subtle slide-up + fade
- Exploration indicators pulse gently
- Proposal cards expand/collapse smoothly
- Timeline auto-scrolls to latest block (with auto-scroll toggle like LogViewer)
- Branch tabs slide transition
- Commit triggers a satisfying "materialization" animation before exiting

## Acceptance

- ACC-001: "New" button in GraphSidebar enters shaping mode with seed input area.
  - Evidence: Playwright: click New, verify seed input renders.

- ACC-002: After entering seed text and clicking Begin, session is created and
  first blocks appear in the timeline.
  - Evidence: Playwright: enter text, click Begin, verify blocks render.

- ACC-003: All block types render correctly with appropriate visual treatment.
  - Evidence: Screenshots of each block type (may use mock data).

- ACC-004: Proposal cards show Accept/Reject/Edit actions; Edit opens inline editor.
  - Evidence: Playwright: interact with proposal card, verify actions work.

- ACC-005: Staging panel shows correct aggregate counts and updates live as
  proposals are added/accepted/rejected.
  - Evidence: Playwright: accept a proposal, verify staging panel count updates.

- ACC-006: Commit flow writes records and returns to editor mode.
  - Evidence: Playwright: commit, verify records appear in sidebar, mode exits.

- ACC-007: `npm --prefix loom-mill/frontend run build` passes.
  - Evidence: Build output.

## Current State

Ready to start after ticket:20260526-mill-shaping-foundation provides the API
surface and event types. Can begin with mock/stub data for the timeline and
proposal cards before the full backend engine is ready.

The frontend-expert should own this ticket for visual quality and interaction feel.

## Journal

- 2026-05-26: Created ticket. Fifth in the shaping sessions plan. This is where
  the novel UX lives—the timeline, staging, proposals, and commit flow.
- 2026-05-27: Implemented the frontend shaping session UI. Verified with Playwright. Closed ticket.
