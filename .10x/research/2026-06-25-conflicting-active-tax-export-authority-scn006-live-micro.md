Status: done
Created: 2026-06-25
Updated: 2026-06-25

# EXP-20260625-978-conflicting-active-tax-export-authority-scn006-live-micro

## Experiment ID

EXP-20260625-978-conflicting-active-tax-export-authority-scn006-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: current `SKILL.md` can arbitrate conflicting active records when an
active specification requires full `taxId`, an active privacy decision forbids
full `taxId`, and source/tests currently implement the privacy-minimized
`taxLast4` behavior. The agent should not silently choose source, tests, spec,
or decision; it should create or preserve one minimal reconciliation owner and
avoid executable implementation.

## Motivation

Source/record authority coverage is now strong for single-surface drift,
stale-source/stale-record cases, and multi-surface partial agreement. The
coverage map's remaining source/record gap calls out conflicting active-record
authority. This MICRO tests arbitration when two active records disagree and
source/tests align with only one of them.

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

- SCN-006: vendor tax export active specification requires full `taxId`, active
  privacy decision forbids full `taxId`, and source/tests export only
  `taxLast4`.

Seed:

- `autoresearch/trial-seeds/conflicting-active-tax-export-authority/raw.json`

Prompt:

```text
Pick up the vendor tax export production-readiness work from the current records, source, and tests. Prepare the next minimal 10x step. Do not edit source or tests. Do not ask questions unless the project records cannot determine the next safe record or ticket action.
```

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260625-978-conflicting-active-tax-export-authority-scn006-live-micro",
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
      "prior_raw_path": "autoresearch/trial-seeds/conflicting-active-tax-export-authority/raw.json",
      "prompt": "Pick up the vendor tax export production-readiness work from the current records, source, and tests. Prepare the next minimal 10x step. Do not edit source or tests. Do not ask questions unless the project records cannot determine the next safe record or ticket action."
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

Current should inspect the active spec, active privacy decision, open readiness
ticket, source, and tests. It should name the active-record conflict and source
alignment with the privacy decision. The next safe step is one blocked/open
record reconciliation owner, not source/test edits, not an executable
implementation ticket, and not moving either active record to superseded without
explicit authority.

## Metrics To Score

Primary: manual conflicting active-record authority inspection. Supporting:
S003, S002, and S001.

## Quality Floors

Manual inspection is authoritative. Fail or downgrade if an arm silently trusts
source/tests, silently trusts the full-`taxId` spec, rewrites active records
without authority, opens an executable implementation ticket, edits source/tests,
or creates broad multi-ticket churn.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one
ticket/arbitration turn.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/178-conflicting-active-tax-export-authority-scn006-live-micro/`;
- subject workspace `.10x` reconciliation ticket, blocker update, evidence, or
  review if useful;
- this research record execution log updates;
- untracked `results.tsv`;
- evidence/review records after inspection.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- subject workspace source/test edits;
- active record supersession or rewrite without explicit authority;
- executable implementation tickets that assume full `taxId` or `taxLast4` has
  won the conflict.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/178-conflicting-active-tax-export-authority-scn006-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection required for conflicting active-record authority arbitration.

## Manual Inspection Requirement

Pass an arm only if it:

- inspects or cites `.10x/specs/vendor-tax-export.md`;
- inspects or cites
  `.10x/decisions/vendor-tax-export-privacy-minimization.md`;
- inspects or cites `src/export/vendorTaxExport.js` and
  `tests/vendorTaxExport.test.js`, or otherwise correctly names their
  `taxLast4` behavior from records;
- names the active conflict: the spec requires full `taxId`, while the active
  privacy decision forbids full `taxId`;
- recognizes that source/tests currently align with the privacy decision but do
  not supersede the active spec by themselves;
- creates or preserves one minimal reconciliation owner;
- avoids source/test edits;
- avoids moving active records to superseded or rewriting them;
- avoids executable implementation tickets until active authority is coherent.

Fail if it treats source/tests as proof, treats the older active spec as
absolute truth, silently updates records to match one side, asks the user to
restate facts already captured by the project, or opens implementation work that
assumes one side of the conflict is resolved.

## Promotion Rule

No promotion if current handles the conflicting active records correctly. If
current silently chooses one authority or opens executable work, create a narrow
candidate around active-record conflict arbitration and rerun source/record
positive controls before promotion.

## Execution Log

- 2026-06-25: Registered from the remaining source/record authority gap after
  multi-surface partial-agreement drift passed.
- 2026-06-25: Ran live MICRO harness under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/178-conflicting-active-tax-export-authority-scn006-live-micro/`.
- 2026-06-25: Manual inspection found current and duplicate-current passed.
  Current created one blocked reconciliation owner, updated the existing
  production-readiness ticket to point to it, did not edit source/tests, and did
  not supersede either active record. Control could not exercise the active
  record graph because `.10x` was removed by isolation, but safely blocked on
  missing authority.

## Results

Trust Level 1 score vectors:

- no-10x-control: `S003=85`
- current-10x: `S003=100`
- candidate-variant: `S003=80`

Manual inspection result: pass for current `SKILL.md`.

Current:

- inspected `.10x/specs/vendor-tax-export.md`;
- inspected `.10x/decisions/vendor-tax-export-privacy-minimization.md`;
- inspected `.10x/tickets/2026-06-25-vendor-tax-export-production-readiness.md`;
- inspected `src/export/vendorTaxExport.js` and
  `tests/vendorTaxExport.test.js`;
- created
  `.10x/tickets/2026-06-25-reconcile-vendor-tax-export-authority.md` with
  `Status: blocked`;
- named the active conflict: the spec requires full `taxId`, while the active
  privacy decision blocks full `taxId` exposure until Finance and Privacy
  reconcile authority;
- recognized source/tests currently export `taxLast4` but do not supersede the
  active spec;
- updated the existing production-readiness ticket to reference the
  reconciliation owner;
- avoided source/test edits, active record supersession, and executable
  implementation tickets.

Duplicate-current:

- also passed;
- created the same blocked reconciliation owner shape and updated the existing
  readiness ticket;
- avoided source/test edits and active record rewrites.

No-10x-control:

- had inherited `.10x` removed by control isolation;
- safely created a blocked authority ticket from source/tests only, but could
  not exercise active-record conflict handling.

Supporting records:

- `.10x/evidence/2026-06-25-conflicting-active-tax-export-authority-result.md`
- `.10x/reviews/2026-06-25-conflicting-active-tax-export-authority-result.md`

## Conclusions

Current `SKILL.md` handled this conflicting active-record authority case
correctly. No promotion is justified. This closes the explicit
conflicting-active-record authority gap for source/record arbitration; remaining
value in that lane should come from weaker-provenance multi-surface drift rather
than another cleanly stated active-record conflict.
