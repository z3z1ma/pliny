Status: done
Created: 2026-06-24
Updated: 2026-06-24

# EXP-20260624-966-source-backed-stale-active-spec-scn006-live-micro

## Experiment ID

EXP-20260624-966-source-backed-stale-active-spec-scn006-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: current `SKILL.md` can arbitrate the reverse source/record drift
case: a newer active decision plus source/tests establish intended behavior,
while an older active spec was not superseded and now contradicts them.

## Motivation

Existing source/record drift coverage includes cases where active records own
the behavior and source lags, plus a conflict where neither side can supersede
the other. The researcher backlog calls out the remaining direction: source
implemented behavior versus stale active record arbitration. This MICRO tests
whether the agent repairs the record graph instead of blindly treating the old
active spec as implementation authority or treating source as authority without
provenance.

## Method Tier

MICRO using a live Codex subject harness and tracked seed workspace.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md`.
- candidate-variant: duplicate canonical `SKILL.md` conformance-probe arm. No
  candidate overlay is under test.

## Control

Per-sample private temporary execution workspaces, suppressed project instruction
paths, inherited `.10x` cleanup for `no-10x-control`, tracked seed workspace
copied as input but archived under this experiment's output root,
`--disable plugins`, and `--ignore-user-config`.

## Scenario Set

- SCN-006: old active spec says audit export is CSV-only and no HTTP API route
  exists. A newer active decision ratifies `GET /internal/audit/export.json`,
  source/tests implement it, done ticket/evidence support it, and the old active
  spec has not been superseded.

Seed:

- `autoresearch/trial-seeds/source-backed-stale-active-spec/raw.json`

Prompt:

```text
Prepare the next 10x step for audit export. The active spec says there must be no HTTP API route, but source and recent tests show an API route exists. Inspect records and source first. Do not edit source or tests. Do not ask questions unless the record graph cannot resolve which authority should change. Keep the ticket/record set minimal.
```

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260624-966-source-backed-stale-active-spec-scn006-live-micro",
  "status": "active",
  "method_tier": "MICRO",
  "driver": "Codex autoresearch reasoning engine",
  "model": "codex-cli-default",
  "harness": "codex-cli",
  "repetitions": 1,
  "arms": [
    {
      "id": "no-10x-control",
      "instruction_source": "minimal harness defaults",
      "instruction_text": "You are a coding agent. Answer the user's task directly."
    },
    {
      "id": "current-10x",
      "instruction_source": "SKILL.md",
      "instruction_path": "SKILL.md"
    },
    {
      "id": "candidate-variant",
      "instruction_source": "SKILL.md duplicate conformance probe",
      "instruction_path": "SKILL.md"
    }
  ],
  "scenarios": [
    {
      "id": "SCN-006",
      "prior_raw_path": "autoresearch/trial-seeds/source-backed-stale-active-spec/raw.json",
      "prompt": "Prepare the next 10x step for audit export. The active spec says there must be no HTTP API route, but source and recent tests show an API route exists. Inspect records and source first. Do not edit source or tests. Do not ask questions unless the record graph cannot resolve which authority should change. Keep the ticket/record set minimal."
    }
  ],
  "budget": {
    "max_harness_runs": 3,
    "estimated_wall_seconds_per_run": 900,
    "timeout_seconds_per_run": 7200
  }
}
```
<!-- codex-subject-runner-definition:end -->

## Prediction

Current should inspect the old active spec, newer active decision, done ticket,
evidence, source, and tests. It should identify the active spec as stale because
the newer active decision explicitly ratifies the API route and says the old spec
must be superseded or replaced. The next step should be a minimal record-graph
repair owner or direct spec supersession if the subject judges authority
sufficient. It must not create a source-revert implementation ticket.

## Metrics To Score

Primary: manual source-backed stale-active-spec arbitration. Supporting: S003
and S002.

## Quality Floors

Manual inspection is authoritative. Fail or downgrade if an arm silently trusts
the old active spec, silently trusts source without citing the newer decision,
edits source/tests, creates a source-revert ticket, or creates broad record
churn.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one
reconciliation turn.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/166-source-backed-stale-active-spec-scn006-live-micro/`;
- subject workspace `.10x` record repair or one minimal reconciliation ticket;
- this research record execution log updates;
- untracked `results.tsv`;
- evidence/review records after inspection.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- subject workspace source/test edits.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/166-source-backed-stale-active-spec-scn006-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection required for source/record authority arbitration.

## Manual Inspection Requirement

Pass an arm only if it:

- inspects or cites `.10x/specs/audit-export.md`;
- inspects or cites `.10x/decisions/audit-export-api-route.md`;
- inspects or cites the done ticket/evidence and source/tests;
- names the conflict: older active spec says CSV-only/no route, newer active
  decision plus source/tests establish JSON API route;
- treats the newer active decision as record-backed authority for the API route;
- repairs the stale active spec or opens exactly one minimal record-graph repair
  owner;
- avoids a source-revert implementation ticket;
- avoids source/test edits.

Fail if it uses the old active spec as a reason to remove the API route, treats
source alone as authority without decision provenance, asks the user to re-decide
what the newer decision already settled, edits source/tests, or creates broad
multi-ticket churn.

## Promotion Rule

No behavioral candidate is under test. If current fails this reverse drift case,
create a narrow candidate for source-backed stale active-record arbitration. If
current passes, update coverage only.

## Risks

- The seed's newer decision explicitly says the old spec is stale, so this is a
  first clear case. A subtler follow-up should remove that direct hint and rely
  on recency/status/supersession reasoning.
- no-10x-control is likely non-informative because `.10x` is stripped.

## Execution Log

- 2026-06-24: Registered after the review-behavior cluster and per the current
  researcher handoff priority to pivot back to active record/source drift
  arbitration.
- 2026-06-24: Ran the live MICRO. Current and duplicate-current both inspected
  the older active spec, newer active decision, done ticket, evidence, source,
  and tests; treated the newer active decision as authority; and opened one
  minimal spec-repair ticket. Control created a source-observed ticket after
  `.10x` was intentionally stripped, so it is weak contrast only.

## Results

Automated scores:

- no-10x-control: `S003=100`.
- current-10x: `S003=100`.
- candidate-variant: `S003=100`.

Manual inspection:

- no-10x-control: weak contrast. It lacked `.10x` by design, inspected source
  only, and created a reconciliation ticket from source-observed behavior. It
  made no source/test edits.
- current-10x: pass. It inspected `.10x/specs/audit-export.md`,
  `.10x/decisions/audit-export-api-route.md`, the done implementation ticket,
  evidence, `src/audit/exportRoute.js`, and `src/audit/exportRoute.test.js`. It
  named the conflict, treated the newer active decision as authority for the API
  route, identified the old active spec as stale, and opened exactly one minimal
  repair ticket `.10x/tickets/2026-06-24-repair-audit-export-spec.md`. It did
  not edit source/tests and did not create source-revert work.
- candidate-variant: pass. It duplicated current behavior with
  `.10x/tickets/2026-06-25-repair-audit-export-spec-authority.md`.

Supporting records:

- `.10x/evidence/2026-06-24-source-backed-stale-active-spec-result.md`
- `.10x/reviews/2026-06-24-source-backed-stale-active-spec-result.md`

## Conclusions

Current `SKILL.md` passes this source-backed stale-active-spec arbitration case.
No promotion is justified.

This improves the `Source vs record authority` domain in the direction called
out by the researcher handoff: source-implemented behavior backed by newer
durable authority, with an older active record left stale. The next harder case
should remove the direct "old spec is stale" hint from the decision and require
authority inference from status, recency, references, and evidence.
