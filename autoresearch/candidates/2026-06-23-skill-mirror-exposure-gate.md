# Candidate: Skill Mirror Exposure Gate

Candidate ID: `candidate-skill-mirror-exposure-gate-v1`
Created: 2026-06-23
Canonical target: `SKILL.md`
Status: discarded

## Target Behavior

When retrospective extraction creates an active skill, the agent must not leave
that skill only in `.10x/skills/` if the repository has a clear harness-native
skills directory. The skill should be exposed immediately to the execution
engine through the detected native directory, with no divergent stale copy.

## Proposed Instruction Overlay

Add this rule near the Retrospective Protocol or Skills section:

```text
When retrospective extraction creates or updates a `.10x/skills/<slug>/SKILL.md`
record, closure is incomplete until the skill is exposed to the execution
engine or a blocker/no-action rationale explains why no harness-native target is
known.

Before closing the ticket that produced the skill, verify:

- the `.10x/skills/<slug>/SKILL.md` source has valid skill frontmatter and the
  required Objective, Prerequisites, Procedure, and Validation sections;
- if the repository contains an existing harness-native skills directory such
  as `.claude/skills/` or `.agents/skills/`, the skill is mirrored, copied, or
  symlinked there under the same slug;
- the exposed skill is synchronized with the `.10x` source, or the sync
  mechanism is explicit;
- no speculative mirrors are created for harnesses not present in the
  workspace.
```

## Expected Score Movement

- S008 Retrospective Capture: should improve if current creates the durable
  skill but fails to expose it.
- S002 Record Graph Fitness: should improve if the source skill and native
  mirror are coherent rather than divergent.
- S006 Closure Coherence: should improve if closure waits for exposure or
  records a blocker.

## Scenario Coverage

Primary scenario:

- SCN-012: completed Ledger import preview closure with a repeated operational
  procedure that must become a skill, plus an existing `.claude/skills/`
  directory as the unambiguous harness-native target.

Secondary scenarios:

- SCN-009 closure coherence when retrospective obligations include skills.
- SCN-004 record routing for operational procedure lessons.

## Expected Failure Modes

- Duplicate drift: creating `.10x/skills` and `.claude/skills` files with
  different content.
- Speculative mirror spam: creating mirrors for every possible harness instead
  of the one present in the workspace.
- Overblocking: refusing closure even though the native directory is present
  and the mirror can be created directly.
- Under-recording: creating only the native skill and losing the `.10x` source.

## Promotion Boundary

Promote only if current creates a skill or says a skill is needed but fails to
expose a usable native mirror, while candidate creates a valid `.10x` skill,
exposes it under the present harness-native directory, keeps the copies
coherent, and closes only after the rest of the retrospective obligations have
owners.

Discard if current already creates both the `.10x` source and native mirror, or
if candidate creates divergent/speculative mirrors.

## Result

`EXP-20260623-853-skill-mirror-exposure-scn012-live-micro` discarded this
candidate as null versus current. Current 10x and the candidate both created a
valid `.10x/skills/ledger-import-test-fixtures/SKILL.md` source, exposed an
identical `.claude/skills/ledger-import-test-fixtures/SKILL.md` mirror, routed
`sourceRef` to knowledge, opened an archive malformed-currency follow-up ticket,
closed the parent and child tickets, and avoided source edits.

The candidate is safe but redundant because canonical `SKILL.md` already
contains and executed the skill exposure obligation in this seed.
