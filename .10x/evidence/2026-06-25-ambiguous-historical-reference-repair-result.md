Status: recorded
Created: 2026-06-25
Updated: 2026-06-25
Relates-To: .10x/research/2026-06-25-ambiguous-historical-reference-repair-scn004-live-micro.md, .10x/research/2026-06-24-10x-conformance-coverage-map.md

# Ambiguous Historical Reference Repair Result

## What Was Observed

`EXP-20260625-971-ambiguous-historical-reference-repair-scn004-live-micro` ran
one live Codex turn for each arm:

- current-10x: `sha256-9d4e1c5f48e87f45719b4cdcce43ed8fad92a10e4797bc356822122aec3a3f44`
- candidate-variant: `sha256-c8287a595379ced807a057f0635edc6c5b510356c2c7a930b2081afb1bd93f37`
- no-10x-control: `sha256-e391d0efedb161fd59248c1d0244fe56303345190a4de14bb3d8c208f0528edb`

Trust Level 1 S002 scored current and duplicate-current at `30`, and control at
`15`. Manual inspection overrode those low heuristic scores.

Current `SKILL.md` moved the active specification from:

```text
.10x/specs/payments-retry-window.md
```

to:

```text
.10x/specs/payments-webhook-retry-policy.md
```

It updated the title to `Payments Webhook Retry Policy`, repaired live
`Depends-On`, `Relates-To`, `Target`, scope, acceptance, and supersession
pointer references, and preserved historical prose plus fenced command-output
blocks that mention the old path.

The old active spec path was absent after the run. Remaining old-path mentions
were historical notes or fenced output, including:

- the active ticket progress log saying it was originally opened against the old
  path;
- the naming-history research record;
- the superseded record's historical note and captured command output;
- the evidence record's pre-rename inspection output.

Current did not create implementation work, did not edit source files, and did
not run tests.

Candidate-variant passed equivalently. no-10x-control could not complete
because control isolation removed the writable `.10x` graph and its attempt to
operate on the fixture source path failed with `Operation not permitted`.

## Procedure

Ran:

```text
python3 autoresearch/run_once.py --experiment .10x/research/2026-06-25-ambiguous-historical-reference-repair-scn004-live-micro.md --out .10x/evidence/.storage/2026-06-23-skill-autoresearch/171-ambiguous-historical-reference-repair-scn004-live-micro --require-clean-canonical
```

Inspected saved subject artifacts under:

```text
.10x/evidence/.storage/2026-06-23-skill-autoresearch/171-ambiguous-historical-reference-repair-scn004-live-micro/
```

Manual checks covered the new active spec, old-path absence, superseded record,
dependent ticket, evidence/review headers, historical body text, fenced output,
and last-message summaries.

## What This Supports Or Challenges

This supports item 2 of the ranked conformance push: record graph maintenance
with ambiguous historical references. It shows current `SKILL.md` can distinguish
live authority references from historically accurate old-path mentions in the
same record graph.

It does not support a `SKILL.md` promotion because current passed and the
duplicate-current arm did not improve over current.

## Limits

The prompt explicitly named the selective repair requirement. Future variants
could reduce prompt assistance or measure operational efficiency of mechanical
reference repair, but this run covers the core correctness behavior.
