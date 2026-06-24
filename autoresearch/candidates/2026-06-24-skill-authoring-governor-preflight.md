# Candidate: Skill Authoring Governor Preflight

Candidate ID: `candidate-skill-authoring-governor-preflight-v1`
Created: 2026-06-24
Canonical target: `SKILL.md`
Status: experimental

## Target Behavior

Before creating or updating a `.10x/skills/<slug>/SKILL.md` record, the agent
should search the subject workspace for an existing skill-writing governor,
read it, and apply it while keeping the authored skill self-contained and
mirrored to the harness-native directory when present.

## Proposed Instruction Overlay

Add near the Skills record section:

```text
Before creating or updating `.10x/skills/<slug>/SKILL.md`, run a
skill-authoring preflight in the subject workspace: search existing
harness-native skill directories and `.10x/skills` for a governing
skill-writing skill or instruction, read it, and apply it.

A 10x skill must live at `.10x/skills/<skill-slug>/SKILL.md`, use the required
YAML frontmatter, and contain self-contained Objective, Prerequisites,
Procedure, and Validation sections. It must not reference tickets, evidence,
reviews, research, specs, or decisions. The only allowed `.10x` reference is a
knowledge record used for shared vocabulary.

When a harness-native skills directory already exists, mirror, copy, sync, or
symlink the active skill there and keep the exposed content equivalent to the
source skill. Autoresearch promotion must never create or promote product
behavior into this repository's own `.10x/skills`; only subject workspace
outputs count.
```

## Expected Score Movement

- S008 Retrospective Capture should improve when reusable procedure learning is
  distilled through the local skill-writing governor.
- S002 Record Graph Fitness should improve if source/mirror skill records are
  valid and equivalent.
- S006 Closure Coherence should improve when closure waits for governed skill
  extraction and exposure.

## Scenario Coverage

Primary scenario:

- SCN-012 Ledger import fixture replay procedure with seeded
  `.claude/skills/skill-writing-governor/SKILL.md`.

Secondary scenarios:

- SCN-009 closure coherence with skill retrospective obligations.
- SCN-004 record routing for skills versus knowledge.

## Expected Failure Modes

- Current may already scan for the governing skill because `SKILL.md` says to
  inspect existing skill-writing governance.
- Candidate may create a skill that references ticket/evidence records and is
  not self-contained.
- Candidate may create speculative mirrors for absent harnesses.

## Promotion Boundary

Promote only if current fails at least one target behavior while candidate
passes: governor scan, valid `.10x/skills/<slug>/SKILL.md`, self-contained
content, allowed references only, and equivalent `.claude/skills` mirror. Discard
as null if current already passes.
