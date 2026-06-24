# Candidate: Mechanical Default Action Gate

Candidate ID: `candidate-mechanical-default-action-gate-v1`
Created: 2026-06-24
Canonical target: `SKILL.md`
Status: discarded
Promotion: manual-only

## Target Behavior

When all execution-critical semantics are record-backed or user-ratified and
the only remaining unknowns are mechanical artifact choices, the agent should
choose the smallest repo-conventional default and proceed. It should not ask the
user, open a blocked ticket, or stall on filenames, slugs, record titles, draft
placement, or evidence paths.

## Proposed Instruction Overlay

Add near the semantic-default guidance or ticket-readiness gate:

```text
Mechanical defaults are action triggers, not blockers. After inspecting records
and source, if behavior, scope, constraints, acceptance criteria, and
verification are settled, choose local conventions for mechanical artifact
details such as ticket filename, record title, slug, draft placement, evidence
path, or temporary section ordering. Proceed with the smallest conventional
artifact and state that no semantic default was chosen.

Do not ask the user to decide mechanical details that existing repository
patterns answer. Do not open a blocked ticket for mechanical naming or placement
when the executable behavior is otherwise ready.

This does not apply to semantic defaults. If the remaining choice affects
user-visible behavior, business rules, data meaning, permissions, lifecycle
state, failure handling, notifications, money, security, privacy, operations, or
acceptance criteria, it remains a semantic blocker.
```

## Expected Score Movement

- S003 Ticket Fitness should improve when current stalls on mechanical ticket
  naming or creates a blocked mailbox despite settled behavior.
- S005 Scope Minimalism should improve by avoiding unnecessary question/record
  churn for reversible artifact details.
- S007 Human Shaping Quality should improve if the agent explains that the
  remaining default is mechanical, not semantic.

## Scenario Coverage

Primary scenario:

- SCN-006: active billing CSV export decision/spec/source establish behavior,
  scope, acceptance criteria, non-goals, and verification. The user asks for the
  executable ticket but leaves filename/title to the agent.

Secondary scenarios:

- SCN-005: record minimalism when only record naming/placement remains.
- SCN-010: minimal implementation when local convention answers artifact shape.

## Expected Failure Modes

- Null result because current `SKILL.md` already creates the ticket from the
  ticket-readiness gate.
- Candidate accidentally treats a semantic value as mechanical and proceeds.
- Candidate creates an under-specified ticket because it over-focuses on action.

## Promotion Boundary

Promote only if current asks about mechanical naming/placement or creates a
blocked/mechanical placeholder while candidate creates the correct bounded
ticket without semantic invention. Discard if current already proceeds with
comparable ticket quality, or if candidate defaults any product behavior.

## Result

Kept for follow-up after
`EXP-20260624-886-mechanical-default-action-gate-scn006-live-micro`.

Automated first-pass scoring:

- candidate: `S003=100`
- current: `S003=85`
- control: `S003=100`

Manual inspection found current and candidate both created one high-quality
executable child ticket, made no implementation edits, preserved active
decision/spec dependencies, included exclusions and evidence expectations, and
asked no naming or placement questions. Candidate's distinct advantage was
explicitly recording that filename/title were mechanical defaults; the automated
`S003=100` versus current `S003=85` appears partly driven by wording and ticket
shape rather than a major behavioral difference.

Do not promote from this result alone. The prompt explicitly told the subject
that filename/title were mechanical, so the candidate needs a subtler follow-up
or ablation before canonical `SKILL.md` absorbs the paragraph.

`EXP-20260624-887-mechanical-default-action-gate-subtle-scn006-live-micro`
discarded the candidate. Automated first-pass scoring regressed:

- candidate: `S003=65`
- current: `S003=85`
- control: `S003=100`

Manual inspection found candidate still created a usable ticket and named the
mechanical filename/title default, but current produced the stronger ticket
overall: fuller source context, verification expectations, and assumption
provenance. The overlay is not worth its token cost and should not be promoted.
