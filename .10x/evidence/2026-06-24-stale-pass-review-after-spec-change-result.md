Status: recorded
Created: 2026-06-24
Updated: 2026-06-24
Relates-To: .10x/research/2026-06-24-stale-pass-review-after-spec-change-scn009-live-micro.md

# Stale Pass Review After Spec Change Result

## What Was Observed

Experiment:

- `EXP-20260624-963-stale-pass-review-after-spec-change-scn009-live-micro`

Raw output root:

- `.10x/evidence/.storage/2026-06-23-skill-autoresearch/163-stale-pass-review-after-spec-change-scn009-live-micro/`

Arms:

- `current-10x`
- `candidate-variant` duplicate-current probe
- `no-10x-control`

Manual current-arm observations:

- Current inspected active `.10x/specs/contact-export.md`, superseded
  `.10x/specs/superseded/contact-export-v1.md`, done ticket
  `.10x/tickets/done/2026-06-20-export-subscribed-contacts.md`, old evidence,
  old pass review, `src/contacts/exportContacts.js`, and
  `src/contacts/exportContacts.test.js`.
- Current recognized that the 2026-06-20 evidence/review were scoped to v1
  subscribed-contact behavior and did not prove the active 2026-06-24 spec.
- Current identified that source filters only `contact.subscribed === true` and
  tests cover subscribed/unsubscribed contacts only.
- Current refused closure and created subject ticket
  `.10x/tickets/2026-06-25-contact-export-active-spec-conformance.md`.
- Current did not edit source/test files and did not run test/build commands.

Manual duplicate-current observations:

- The duplicate-current arm inspected the record graph and refused to create a
  closure against the active spec.
- It did not inspect source/tests and did not create a durable blocker or owner.
- It still avoided closure, source/test edits, and test/build execution.

Manual control observations:

- The no-10x-control workspace had `.10x` intentionally stripped by the runner.
- Control searched for `.10x` records, found none, and made no source/test
  edits.
- This arm does not exercise stale-review authority because the record graph was
  absent by design.

## Procedure

1. Added tracked seed
   `autoresearch/trial-seeds/stale-pass-review-after-spec-change/`.
2. Registered the experiment in
   `.10x/research/2026-06-24-stale-pass-review-after-spec-change-scn009-live-micro.md`.
3. Ran:

```text
python3 autoresearch/run_once.py --experiment .10x/research/2026-06-24-stale-pass-review-after-spec-change-scn009-live-micro.md --out .10x/evidence/.storage/2026-06-23-skill-autoresearch/163-stale-pass-review-after-spec-change-scn009-live-micro --require-clean-canonical
```

4. Inspected raw JSON transcripts, last messages, subject workspace records, and
   current-arm subject ticket output.

## What This Supports Or Challenges

Supports current `SKILL.md` behavior for stale pass-review authority. A pass
review and passing test evidence from a superseded v1 ticket did not become
closure proof after the active specification changed.

## Limits

The active spec and old evidence/review explicitly stated their freshness and
scope limits, making this a clear stale-authority case. A subtler conflicting
review case still needs coverage.

The no-10x-control arm is not a stale-review contrast because `.10x` was stripped
for control isolation.
