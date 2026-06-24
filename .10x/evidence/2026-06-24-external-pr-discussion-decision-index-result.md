Status: recorded
Created: 2026-06-24
Updated: 2026-06-24
Relates-To: .10x/research/2026-06-24-external-pr-discussion-decision-index-scn004-live-micro.md

# External PR Discussion Decision Index Result

## What Was Observed

Ran `EXP-20260624-929-external-pr-discussion-decision-index-scn004-live-micro`
with three live Codex subject arms.

Automated Trust Level 1 scores:

- no-10x-control: `S002=60`
- current-10x: `S002=60`
- candidate-variant: `S002=60`

Manual inspection found all three arms created one decision-class local record:

- `.10x/decisions/acme-webhook-idempotency-key.md`

Current `SKILL.md` satisfied these criteria:

- read the exported PR discussion;
- created a `.10x/decisions/` record;
- used `Status`, `Created`, and `Updated` headers;
- named the accepted decision: ACME webhook idempotency uses
  `provider_delivery_id`, not `event_id`;
- included context, decision, alternatives, and consequences;
- stated the PR discussion remains the canonical review artifact;
- avoided copying the whole PR discussion;
- avoided source/test edits and implementation tickets.

Manual concern: the current arm under-specified external provenance. The seed
artifact exposed a canonical URL, repository, PR status, and thread id. Current
recorded the local export path and PR number, but omitted:

- canonical URL `https://github.example/acme/payments/pull/482#discussion_r918273645`;
- thread id `discussion_r918273645`;
- observed PR status `merged`;
- export timestamp `2026-06-24T15:10:00Z`.

The duplicate-current arm included the canonical URL but still omitted the PR
status and thread id as explicit provenance fields. The no-10x-control arm also
created a compact decision record because the prompt directly named `.10x`.

The canonical guard reported unchanged `SKILL.md` and
`autoresearch/program.md` hashes during the run.

Raw artifact root:

- `.10x/evidence/.storage/2026-06-23-skill-autoresearch/129-external-pr-discussion-decision-index-scn004-live-micro/`

## Procedure

1. Registered the seed workspace and research record in commit `d6bab28b`.
2. Ran:

```text
python3 autoresearch/run_once.py --experiment .10x/research/2026-06-24-external-pr-discussion-decision-index-scn004-live-micro.md --out .10x/evidence/.storage/2026-06-23-skill-autoresearch/129-external-pr-discussion-decision-index-scn004-live-micro --require-clean-canonical
```

3. Read `report.md`, `summary.json`, canonical guard, archived workspace file
   lists, final messages, and the decision record in each archived workspace.

## What This Supports Or Challenges

Supports current `SKILL.md` handling external PR discussions as decision-shaped
durable context rather than copying threads or opening implementation work.

Challenges the current "durable pointer" language: for non-document external
artifacts, current may create the right record type while omitting available
canonical URL, external id, status, or revision/export metadata.

## Limits

This run used one synthetic exported PR discussion and one repetition. The
prompt directly named `.10x`, so the no-10x-control arm is not a meaningful
process comparator.

This was not a real candidate comparison; `candidate-variant` duplicated current
`SKILL.md`.
