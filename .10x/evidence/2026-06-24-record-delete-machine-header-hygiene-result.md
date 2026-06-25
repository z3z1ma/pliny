Status: recorded
Created: 2026-06-24
Updated: 2026-06-24
Relates-To: .10x/research/2026-06-24-record-delete-machine-header-hygiene-scn004-live-micro.md

# Record Delete Machine Header Hygiene Result

## What Was Observed

Ran `EXP-20260624-938-record-delete-machine-header-hygiene-scn004-live-micro`
with three live Codex subject arms.

Automated Trust Level 1 scores:

- no-10x-control: `S002=15`
- current-10x: `S002=30`
- candidate-variant: `S002=30`

Manual inspection overrides the heuristic score. Current `SKILL.md` and the
duplicate-current arm passed the stricter deleted-path header-hygiene criteria:

- deleted `.10x/specs/zeus-webhook-retry.md`;
- cancelled and moved the dependent ticket to
  `.10x/tickets/cancelled/2026-06-24-implement-zeus-webhook-retry.md`;
- cleared the deleted path from live `Depends-On`, `Relates-To`, `Target`, and
  `Parent` headers;
- changed the review header to `Target: deleted Zeus webhook retry draft specification`;
- changed evidence `Relates-To` to the cancelled ticket, review, and/or current
  supporting records without pointing at the deleted spec;
- preserved deleted-path mentions only in historical body prose or fenced
  command-output blocks;
- recorded repair evidence in the subject workspace;
- edited no source files and ran no tests.

The manual live-header search returned no matches for both current and
duplicate-current:

```bash
rg -n '^(Depends-On|Relates-To|Target|Parent):.*\.10x/specs/zeus-webhook-retry\.md' .10x
```

Raw artifact root:

- `.10x/evidence/.storage/2026-06-23-skill-autoresearch/138-record-delete-machine-header-hygiene-scn004-live-micro/`

## Procedure

1. Registered the stricter header-hygiene research record.
2. Ran:

```bash
python3 autoresearch/run_once.py --experiment .10x/research/2026-06-24-record-delete-machine-header-hygiene-scn004-live-micro.md --out .10x/evidence/.storage/2026-06-23-skill-autoresearch/138-record-delete-machine-header-hygiene-scn004-live-micro --require-clean-canonical
```

3. Read `report.md`, raw artifacts, score artifacts, workspace manifests, final
   messages, and changed subject records.
4. Ran manual path-existence and live-header checks over the archived
   workspaces.

## What This Supports Or Challenges

Supports marking current `SKILL.md` as passing deleted-path live-header hygiene
under direct pressure. This strengthens record graph lifecycle conformance and
removes the residual risk from the earlier invalid-draft deletion run.

Challenges the current offline S002 scorer, which scored current and
duplicate-current at `30` despite successful deletion, cancellation, reference
repair, evidence creation, and no source/test edits.

## Limits

The prompt explicitly named the live headers, so this proves behavior under
direct header-hygiene pressure more than spontaneous cleanup in weaker prompts.

This was not a behavioral candidate comparison; `candidate-variant` duplicated
current `SKILL.md`.

The no-10x-control arm is not a meaningful contrast because control isolation
removed `.10x` before execution.
