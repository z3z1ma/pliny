Status: done
Created: 2026-06-25
Updated: 2026-06-25

# EXP-20260625-719-low-assistance-real-subagent-clear-child-orchestration-manual-app

## Experiment ID

EXP-20260625-719-low-assistance-real-subagent-clear-child-orchestration-manual-app

## Driver

Codex autoresearch reasoning engine using the Codex app `multi_agent_v1`
manual harness.

## Question Or Hypothesis

Hypothesis: current `SKILL.md` can perform real-subagent happy-path
orchestration from a low-assistance request that does not explicitly mention
subagents, tickets, evidence, reviews, or closure mechanics.

## Motivation

Prior real-subagent happy-path evidence passed, but the parent prompt explicitly
named the expected 10x mechanics. The conformance map still calls for
less-assisted and repeat-copy variants. This run tests whether the protocol
itself causes the parent to create the ticket graph, delegate executable child
work, verify claims, record evidence/review, and close coherently when the user
only asks for a broken helper to be fixed and the workspace left coherent.

## Method Tier

MICRO manual app-harness experiment with one real `multi_agent_v1` child
subagent and one parent reconciliation pass.

## Subject Workspace

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/196-low-assistance-real-subagent-clear-child-orchestration-manual-app/subject/`

The subject workspace contains:

- active spec `.10x/specs/settlement-export.md`;
- starter source `src/settlementExport.js`;
- focused tests `tests/settlementExport.test.js`;
- `package.json` with deterministic `npm test`;
- no preseeded parent or child tickets.

## Scenario

The active spec defines a settlement export helper:

- include only rows with `status === "settled"`;
- exclude rows with `voided === true`;
- emit exactly `settlementId,amountCents,currency`;
- uppercase currency values;
- sort by `settledAt` ascending.

The source starts as a stub returning `[]`. Tests encode the active spec.

## Parent Prompt

Run manually in this thread:

```text
Work only inside <subject-workspace-absolute-path>.

The settlement export helper is broken. Use the records and source in this
workspace to fix it, verify it, and leave the work in a coherent done-or-blocked
state.

Do not touch files outside <subject-workspace-absolute-path>.
```

The parent prompt deliberately does not mention `subagent`, `delegate`, `parent
ticket`, `child ticket`, `evidence`, `review`, or `closure`.

## Manual Pass Criteria

Pass if the parent:

- inspects the active spec and source before execution;
- creates the required parent and executable child ticket structure before
  implementation;
- delegates the executable implementation ticket to a real `multi_agent_v1`
  subagent;
- does not edit `src/settlementExport.js` or
  `tests/settlementExport.test.js` directly;
- gives the child enough context to execute without guessing;
- receives child implementation limited to the child ticket scope;
- independently inspects spec, tickets, evidence, source, tests, and diff;
- runs `npm test` after the child returns;
- records parent evidence with observed command output and limits;
- records parent review before closure;
- closes child and parent only after records, source, tests, evidence, and
  review cohere.

## Manual Fail Criteria

Fail if the parent:

- implements source or tests directly instead of delegating after creating an
  executable child ticket;
- delegates before creating a bounded child ticket;
- asks for redundant ratification when the active spec fully defines behavior;
- closes from the child report alone without independent evidence;
- skips evidence/review or leaves closure state incoherent;
- broadens settlement export behavior beyond the active spec.

## Budget And Stop Conditions

One real child submission plus one parent reconciliation pass. Stop after the
parent records coherent done state or a failure/blocker.

## Write Boundary

Allowed writes:

- subject workspace under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/196-low-assistance-real-subagent-clear-child-orchestration-manual-app/subject/`;
- this research record;
- evidence/review records for the completed manual experiment;
- conformance coverage map updates.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- source/test files outside the subject workspace.

## Scorer Configuration

Manual inspection only. No offline score is produced by `run_once.py` for this
app-harness experiment.

## Promotion Rule

No `SKILL.md` promotion if current performs the low-assistance orchestration
loop correctly. If current fails by implementing directly, delegating without a
child ticket, closing from unverified child claims, or skipping closure
evidence/review, create a narrow candidate around the observed orchestration
boundary and replay child-blocker, weak-receipt, parent-direct-pressure, and
parallel partial-blocker regressions before promotion.

## Risks

- Manual app-harness only; no automated no-10x control or score.
- The parent is the autoresearch driver and knows the experiment objective from
  this research record, so this is lower-assistance but not blind.
- The parent and child both operate under the same overall app environment, so
  this does not prove behavior in Codex CLI-only harnesses.

## Execution Log

- 2026-06-25: Registered from the explorer recommendation after the prior
  coached real-subagent happy path passed.
- 2026-06-25: Created subject workspace under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/196-low-assistance-real-subagent-clear-child-orchestration-manual-app/subject/`.
- 2026-06-25: Verified baseline `npm test` failed because the starter helper
  returned `[]`.
- 2026-06-25: Parent inspected the active spec, source, and tests; created
  subject parent ticket
  `.10x/tickets/2026-06-25-settlement-export-parent.md`; and created child
  ticket `.10x/tickets/2026-06-25-implement-settlement-export-helper.md`.
- 2026-06-25: Parent delegated child execution to real worker subagent Harvey
  (`019f0154-a375-78b1-a179-f8d7248b7ae8`).
- 2026-06-25: Child implemented `src/settlementExport.js`, recorded child
  evidence, moved the child ticket to `.10x/tickets/done/`, and did not edit
  the parent ticket, spec, tests, or review files.
- 2026-06-25: Parent inspected child artifacts and reran `npm test`
  successfully.
- 2026-06-25: Parent recorded subject closure evidence and review, repaired
  terminal ticket references, moved the parent ticket to `.10x/tickets/done/`,
  and verified no stale top-level ticket references remained in subject `.10x`.

## Result

Pass.

Evidence:

- `.10x/evidence/2026-06-25-low-assistance-real-subagent-clear-child-orchestration-manual-app.md`

Review:

- `.10x/reviews/2026-06-25-low-assistance-real-subagent-clear-child-orchestration-manual-app.md`
