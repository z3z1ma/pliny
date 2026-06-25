# Candidate: Active Skill Forward Use

Candidate ID: `candidate-active-skill-forward-use-v1`
Created: 2026-06-25
Canonical target: `SKILL.md`
Status: discarded-null

## Target Behavior

When a task asks the agent to perform a non-trivial operational procedure, the
agent should inspect active `.10x/skills/` records and present harness-native
skill roots for an applicable skill before inventing or re-deriving the
procedure.

## Motivation

Recent skill-authoring experiments prove current `SKILL.md` can create,
identify, mirror, and repair skills. They do not prove that a later agent
actually uses the generated skill when performing the procedure. A skill that is
authored but not used does not compound operational memory.

## Proposed Instruction Overlay

Add near the Skills record section:

```text
Use active skills, not only author them. Before performing a non-trivial
operational procedure, search `.10x/skills/` and any present harness-native
skill roots such as `.claude/skills/`, `.agents/skills/`, and
`.opencode/skills/` for an active skill whose description, objective, or
procedure matches the requested work. When a skill matches, execute its
procedure and validation instead of inventing a nearby workflow. Treat skills as
operational procedure guidance, not semantic authority over active
specifications or decisions; if a skill conflicts with active records or
source, stop and reconcile the conflict before proceeding.
```

## Expected Score Movement

- S008 should improve when existing skills are reused rather than ignored.
- S002 should improve if evidence and tickets reference the durable operational
  owner instead of creating duplicate procedure notes.
- S006 should improve if closure evidence follows the skill validation.

## Scenario Coverage

Primary scenario:

- SCN-012 forward-use Ledger import fixture replay, where the procedure already
  exists as a `.10x` source skill and `.agents` exposure copy before the agent
  is asked to run the verification.

Required regression controls before promotion if promising:

- Skill-vs-knowledge routing, to avoid overusing skills for conceptual facts.
- Divergent mirror repair, to ensure active source skill remains canonical.
- Source/record drift, to ensure a stale skill does not override active specs or
  decisions.

## Expected Failure Modes

- Candidate may over-search skills for trivial work.
- Candidate may treat stale skills as semantic truth even when active specs or
  decisions conflict.
- Candidate may cite a skill without executing its validation.
- Candidate may over-record generic skill-use evidence with no observed output.

## Promotion Boundary

Promote only if current ignores or underuses an applicable active skill and the
candidate reliably executes the skill's procedure and validation without
weakening active-record authority, evidence integrity, or minimalism. Discard as
null if current already finds and uses the active skill.

## Result

`EXP-20260625-963-active-skill-forward-use-scn012-live-micro` discarded this
candidate as null.

Current `SKILL.md` already passed the forward-use floor in all five
repetitions:

- used the existing Ledger import fixture replay skill or existing tracked
  fixture procedure;
- ran the fixture replay command with `testdata/ledger/import-preview.csv` and
  posting date `2026-01-15`;
- recorded evidence containing the observed command/output and limits;
- validated `LEDGER-001`, `LEDGER-002`, `12345`, `-678`, and `2026-01-15`;
- updated the open verification ticket;
- avoided `externalId`, inline CSV construction, wall-clock date dependence,
  and implementation/fixture/script/skill edits.

Candidate also passed all five repetitions but did not improve the target
behavior. One candidate repetition moved the ticket to `tickets/done/`, while
the other four candidate repetitions and all five current repetitions left the
ticket open with progress evidence. That closure variance is not evidence for
this forward-use overlay.

No `SKILL.md` promotion is justified.

Supporting records:

- `.10x/evidence/2026-06-25-active-skill-forward-use-result.md`
- `.10x/reviews/2026-06-25-active-skill-forward-use-result.md`
