# Candidate: Skill Record-Backed Identity

Candidate ID: `candidate-skill-record-backed-identity-v1`
Created: 2026-06-25
Canonical target: `SKILL.md`
Status: active

## Target Behavior

When authoring or updating a 10x source skill, the agent should preserve the
skill identity already established by the record graph or workstream instead of
coining a near-synonym slug.

## Motivation

`candidate-skill-source-path-shape-v1` fixed flat source-skill files but
explicitly did not solve weak-request slug stability. Later conformance runs
showed canonical `SKILL.md` can still drift among semantically similar skill
slugs:

- `replay-ledger-import-fixtures`
- `ledger-fixture-replay`
- `ledger-import-fixture-replay`

The behavioral gap is not directory shape. It is failure to treat an existing
durable workstream's skill name/path as authority when naming the skill.

## Proposed Instruction Overlay

Add immediately after the source skill path sentence in the Skills record
section:

```text
Preserve record-backed skill identity. If an existing ticket, specification,
knowledge record, evidence record, review, prior skill, or parent workstream
names a skill slug, skill path, or intended skill identity, use that identity
exactly for the source skill and any harness-native exposure copy. Do not coin a
near-synonym slug merely because it sounds clearer.
```

## Expected Score Movement

- S002 should improve on skill-authoring scenarios by reducing duplicate or
  near-duplicate skill owners.
- S006 should improve when parent closure can reference one stable skill path.
- S008 should hold because the candidate preserves self-contained skill shape
  without adding record references inside the skill.

## Scenario Coverage

Primary scenario:

- SCN-012 skill closure completeness, where current and duplicate-current
  created closure evidence but sometimes used near-synonym skill slugs.

Required regression controls before promotion:

- Weak-request slug stability.
- No-native-dir source skill behavior.
- `.agents` writable mirror.
- `.opencode` mirror.
- `.claude` mirror.

## Expected Failure Modes

- Candidate may overfit to exact prompt wording instead of records.
- Candidate may preserve a bad historical slug when the workstream clearly
  superseded it.
- Candidate may treat descriptive prose as a slug even when no identity is
  established.
- Candidate may improve source skill identity but forget harness-native mirror
  identity.

## Promotion Boundary

Promote only if candidate materially improves slug stability versus current on
the closure-completeness run and passes mirror/source-path regressions. Discard
if current already becomes stable on rerun, if candidate creates duplicate skill
owners, or if candidate weakens self-contained skill quality.

## Result

`EXP-20260625-997-skill-record-backed-identity-scn012-live-micro` is promising
but not promotable yet.

Manual inspection found candidate created
`.10x/skills/ledger-import-fixture-replay/SKILL.md` in all three repetitions.
Current created the expected skill in two repetitions and drifted to
`.10x/skills/ledger-fixture-replay/SKILL.md` in one repetition. Candidate also
preserved parent closure evidence, avoided speculative mirror directories, and
kept generated skills free of forbidden `.10x` record references.

Required before promotion:

- weak-request slug-stability regression;
- no-native source-path regression;
- `.agents` writable mirror regression;
- `.opencode` mirror regression;
- `.claude` mirror regression.

Supporting records:

- `.10x/evidence/2026-06-25-skill-record-backed-identity-result.md`
- `.10x/reviews/2026-06-25-skill-record-backed-identity-result.md`

`EXP-20260625-998-skill-record-backed-identity-weak-request-regression-scn012-live-micro`
passed the weak-request identity regression. Candidate and current both created
the exact `.10x/skills/ledger-import-fixture-replay/SKILL.md` source skill in
all three repetitions, while no-10x-control created flat or near-synonym skill
files. Candidate created no speculative native mirrors, no alternate skill
owners, no forbidden `.10x` references inside generated skills, and no
implementation edits.

This run is non-regression clearance rather than additional improvement proof,
because current also passed. It also surfaced residual lifecycle risk: candidate
left done-status tickets at top-level in two repetitions, while current moved
completed tickets into `done/` in all three repetitions. Treat that as a
separate closure-maintenance concern, not as a failure of the identity overlay.

Still required before promotion:

- no-native source-path regression;
- `.agents` writable mirror regression;
- `.opencode` mirror regression;
- `.claude` mirror regression.

Additional supporting records:

- `.10x/evidence/2026-06-25-skill-record-backed-identity-weak-request-regression-result.md`
- `.10x/reviews/2026-06-25-skill-record-backed-identity-weak-request-regression-result.md`
