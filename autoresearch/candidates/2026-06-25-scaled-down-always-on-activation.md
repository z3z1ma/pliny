# Candidate: Scaled-Down Always-On Activation

Candidate ID: `candidate-scaled-down-always-on-activation-v1`
Created: 2026-06-25
Canonical target: `SKILL.md`
Status: promoted
Promotion: manual-only

## Target Behavior

The agent must not treat 10x as optional overhead for small or personal work.
For trivial edits, 10x should be nearly invisible. For non-trivial creation,
including small greenfield apps, 10x must still preserve the Outer Loop gate and
avoid inventing product semantics from conventional defaults.

## Motivation

`EXP-20260625-720-small-greenfield-app-activation-boundary-live-micro` reproduced
the user's external failure in a generic form. Current canonical 10x did not say
"10x is unnecessary," but it implemented immediately and backfilled records,
which is the same activation-boundary defect.

The fix should not mention to-do apps or bookmark apps. It should establish the
general scaling rule: small work reduces ceremony, not discipline.

## Proposed Instruction Overlay

Add near `## Execution Gate`, before the Outer Loop / Inner Loop boundary:

```text
## Protocol Activation And Scale

10x is always active. Do not decide that this protocol is unnecessary because a
task is small, personal, greenfield, low-stakes, or likely to fit in one file.
Small work changes the amount of visible ceremony; it does not disable the
Outer Loop, assumption provenance, write boundary, ticket discipline, evidence,
or closure rules when those rules apply.

Scale 10x down by asking fewer and sharper questions, creating the smallest
useful record, using the simplest mechanical workflow, and skipping durable
records only when the work is genuinely trivial and fully specified. Do not
scale it down by implementing non-trivial behavior from unratified defaults and
then backfilling records afterward.

Creating a new app, feature, workflow, data store, API, UI surface, persistence
behavior, or testable product behavior is non-trivial even when the user asks
for something "small" or says to "keep it simple." If the request does not
settle target workflow, storage/persistence, platform, acceptance behavior, and
verification path, stay in the Outer Loop. Inspect the workspace, recommend the
smallest simple shape, and ask a compact confirm-or-correct question before
implementation. A draft or shaping record may preserve the request and blockers;
do not create app files, dependency files, tests, servers, frontends, or data
files until Inner Loop entry.

Trivial work remains trivial: exact typo fixes, formatting-only changes,
single-line mechanical edits, or fully specified no-risk changes may be done
without creating records when no durable context would be useful. The exception
is narrow and does not apply to vague greenfield creation or product behavior.
```

## Expected Score Movement

- SCN-001 small greenfield app activation should improve by preventing direct
  implementation and semantic invention.
- S001 should improve for Outer Loop containment.
- S002/S003 should not regress because executable ticket creation remains
  allowed once behavior is ratified.
- S005 should hold because the text explicitly scales down ceremony and keeps
  trivial work trivial.

## Scenario Coverage

Primary:

- SCN-001 small greenfield app activation boundary.

Regressions:

- SCN-006 over-conservatism positive control: clear active records plus
  implementation authorization should still create an executable ticket.
- SCN-009 closure or child-ticket positive control: the candidate must not block
  coherent closure or child orchestration when requirements are settled.
- SCN-010 no-code/minimalism positive control: the candidate must not force
  records or implementation when elimination is the right answer.

## Expected Failure Modes

- Agent asks excessive questions for truly trivial edits.
- Agent refuses to create an executable ticket even when active records settle
  behavior.
- Agent over-records throwaway tasks.
- Agent treats every small app as blocked even after the user ratifies a simple
  shape.

## Promotion Boundary

Promote only if the candidate stops direct implementation on the small
greenfield activation scenario while holding decisive-entry and minimalism
regressions. Do not promote if it turns trivial edits into heavyweight process
or weakens the Inner Loop once scope is actually settled.
