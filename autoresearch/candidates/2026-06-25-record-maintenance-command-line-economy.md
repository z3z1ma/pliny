# Candidate: Record Maintenance Command-Line Economy

Candidate ID: `candidate-record-maintenance-command-line-economy-v1`
Created: 2026-06-25
Canonical target: `SKILL.md`
Status: active
Promotion: manual-only

## Target Behavior

When record graph maintenance is purely mechanical and the intended
transformation is already established, the agent should prefer simple
command-line/file-system mechanics over repetitive assistant-side edit loops.

## Motivation

`EXP-20260625-974-record-graph-mechanical-maintenance-scn009-live-micro`
showed current `SKILL.md` can use `rg`, direct filesystem moves, a bounded
mechanical rewrite, and validation. However, the subject prompt explicitly
encouraged a simple mechanical workflow. That weakens the evidence because the
desired behavior should come from 10x itself: mechanical maintenance should be
handled mechanically whenever safe.

This matters because dense record updates are exactly where models can waste
time and introduce mistakes by repeatedly reading and editing individual files
through native assistant tools instead of using `rg`, `mv`, `sed`/`perl`, or an
equivalent shell-native operation followed by validation.

## Proposed Instruction Overlay

Add near the record-reference repair rule:

```text
For mechanical record and file maintenance, use mechanical tools. When the
intended transformation is established and repeated path, status, header, or
literal reference changes are unambiguous, prefer repository-native shell/file
operations over repetitive assistant-side edits: use `rg` or equivalent to
enumerate affected paths, direct filesystem moves for moves, one bounded
mechanical rewrite for repeated literal replacements, and `rg` or equivalent to
validate the result.

Do not use blind mechanical rewrites for semantic edits, ambiguous references,
historical notes, fenced logs, append-only progress history, generated content,
or any context where changing the text could change meaning. Inspect and patch
those cases deliberately.

This is an efficiency rule, not a permission to bypass the Outer Loop, mutate
implementation before authorization, skip evidence, or rewrite unrelated
content.
```

## Expected Score Movement

- S002 should hold or improve when dense record path updates remain coherent.
- S005 should improve if current otherwise wastes many calls on repetitive
  manual edits.
- S006 should hold because validation should reduce stale-reference closure
  risk.

## Scenario Coverage

Primary scenario:

- SCN-009 lower-assistance dense terminal ticket move. The user asks for record
  maintenance and live-reference repair, but does not tell the subject to use a
  mechanical workflow.

Regression scenarios if promotion becomes plausible:

- Ambiguous historical reference repair.
- Active spec rename repair.
- Terminal ticket move repair.
- Invalid draft deletion repair.
- Positive closure reference repair.

## Expected Failure Modes

- Null result because current `SKILL.md` already induces command-line economy
  from Operational Minimalism and existing record-reference discipline.
- Candidate overuses mechanical replacement and corrupts historical or
  ambiguous text.
- Candidate becomes shell-clever in ways that are less readable or less
  portable than a simple targeted edit.
- Candidate treats this efficiency rule as permission to mutate implementation
  before the Outer Loop exit condition.

## Promotion Boundary

Promote only if current materially tailspins on repetitive assistant-side edits
or misses references in the lower-assistance record-maintenance scenario while
candidate uses economical mechanics and preserves historical/ambiguous context.
Do not promote for wording preferences, small token-cost differences, or a
candidate that is merely more explicit while current is already efficient.

## Result

`EXP-20260625-700-lower-assistance-record-maintenance-workflow-scn009-live-micro`
is promising but not promotable alone.

Manual inspection found current `SKILL.md` passed graph correctness but did not
consistently use command-line economy: both current repetitions used
assistant-side file-change edits for repeated reference updates, and one current
repetition did not show direct `mv` in command events for the ticket move.

Candidate used direct `mv` and bounded `perl -0pi` literal replacement over the
live-reference file set in both repetitions, preserved the historical research
record, and patched ambiguous/stale parent or review prose deliberately.

Required before promotion:

- ambiguous historical-reference repair regression;
- closure/reference-repair regression;
- semantic or source-edit boundary regression if the first two pass.

Supporting records:

- `.10x/evidence/2026-06-25-lower-assistance-record-maintenance-workflow-result.md`
- `.10x/reviews/2026-06-25-lower-assistance-record-maintenance-workflow-result.md`
