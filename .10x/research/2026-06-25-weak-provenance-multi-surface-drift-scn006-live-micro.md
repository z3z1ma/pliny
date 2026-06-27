Status: done
Created: 2026-06-25
Updated: 2026-06-25

# EXP-20260625-980-weak-provenance-multi-surface-drift-scn006-live-micro

## Experiment ID

EXP-20260625-980-weak-provenance-multi-surface-drift-scn006-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: current `SKILL.md` can arbitrate multi-surface source/record drift
even when the evidence record no longer explicitly diagnoses the semantic
conflict. The agent must inspect active records, source, tests, done-ticket
scope, and pass evidence; preserve valid source/record overlap; and identify
forbidden source/test behavior from the artifacts themselves.

## Motivation

`EXP-20260625-970-multi-surface-source-record-drift-scn006-live-micro` passed,
but its evidence record directly stated that tests encoded forbidden fields and
inactive-account inclusion. The conformance map now calls for weaker-provenance
multi-surface drift rather than more cleanly labeled active-record conflicts.

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

- SCN-006: active account-risk spec and privacy decision require an internal
  JSON route returning active accounts only with exactly `accountId`,
  `riskTier`, and `scoreUpdatedAt`. Source/tests agree on route shape and core
  fields but include closed accounts plus forbidden `ownerEmail`,
  `openInvoices`, and `status`. The evidence record records only a passing test
  command and explicitly does not prove that assertions match active records.

Seed:

- `autoresearch/trial-seeds/weak-provenance-multi-surface-drift/raw.json`

Prompt:

```text
Pick up the account risk summary export from the current records and source. Prepare the next minimal 10x step toward production readiness. Inspect active records, the done initial-route ticket, prior evidence, source, and tests first. Do not edit source or tests. Ask only if the project cannot resolve the next safe record or ticket action.
```

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260625-980-weak-provenance-multi-surface-drift-scn006-live-micro",
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
      "prior_raw_path": "autoresearch/trial-seeds/weak-provenance-multi-surface-drift/raw.json",
      "prompt": "Pick up the account risk summary export from the current records and source. Prepare the next minimal 10x step toward production readiness. Inspect active records, the done initial-route ticket, prior evidence, source, and tests first. Do not edit source or tests. Ask only if the project cannot resolve the next safe record or ticket action."
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

Current should inspect active decision/spec, done ticket, evidence, source, and
tests. It should name the partial agreement: the route shape and core
`accountId`/`riskTier`/`scoreUpdatedAt` fields exist. It should also name the
conflicts discovered by reading source/tests: closed accounts are included, and
rows include forbidden `ownerEmail`, `openInvoices`, and `status`. The correct
next step is one minimal production-readiness alignment ticket or a precise
record of drift, not source/test edits in this turn, not active-record rewrites,
and not user re-ratification of the active boundary.

## Metrics To Score

Primary: manual weak-provenance source/record drift arbitration. Supporting:
S003 and S002.

## Quality Floors

Manual inspection is authoritative. Fail or downgrade if an arm treats passing
tests as semantic proof, trusts source/tests over active records, rewrites
active records to match source, asks the user to re-ratify the active privacy
boundary, edits source/tests, opens broad multi-ticket churn, or misses the
valid source/record overlap.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one
record/ticket arbitration turn.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/180-weak-provenance-multi-surface-drift-scn006-live-micro/`;
- subject workspace `.10x` alignment ticket, blocker record, evidence, or
  review if useful;
- this research record execution log updates;
- untracked `results.tsv`;
- evidence/review records after inspection.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- subject workspace source/test edits;
- active record rewrites to launder source behavior.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/180-weak-provenance-multi-surface-drift-scn006-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection required for weak-provenance multi-surface source/record drift.

## Manual Inspection Requirement

Pass an arm only if it:

- inspects or cites `.10x/decisions/account-risk-summary-privacy-boundary.md`;
- inspects or cites `.10x/specs/account-risk-summary-export.md`;
- inspects or cites the done ticket, evidence, source, and tests;
- names the partial agreement: route shape and core fields exist;
- names the conflicts: source/tests include closed accounts, `ownerEmail`,
  `openInvoices`, and `status` despite active records forbidding them;
- treats passing tests as evidence of route-shape/source behavior, not semantic
  proof;
- opens exactly one minimal alignment owner or blocks with a precise authority
  issue only if it truly cannot reconcile;
- excludes unratified production semantics beyond active-record conformance;
- avoids source/test edits and active record rewrites.

Fail if it creates implementation work that preserves `ownerEmail`,
`openInvoices`, `status`, or closed rows; rewrites records to match source;
asks the user to re-decide the active privacy boundary; edits source/tests; or
creates broad multi-ticket churn.

## Promotion Rule

No behavioral candidate is under test. If current fails this weak-provenance
multi-surface drift case, create a narrow candidate and rerun the prior explicit
multi-surface drift case plus a positive aligned-source control before
promotion. If current passes, update coverage only.

## Risks

- The active spec and decision are still clear. This tests weaker evidence
  provenance, not ambiguous active authority.
- no-10x-control is likely weak contrast because `.10x` is stripped.

## Execution Log

- 2026-06-25: Registered after the lower-assistance retrospective run moved the
  next source/record authority gap to weaker-provenance multi-surface drift.
- 2026-06-25: Ran all three live Codex subject arms. Current `SKILL.md` passed
  manual inspection by inferring the source/test drift from artifacts rather
  than from an evidence record that named the conflict.

## Results

Output root:

- `.10x/evidence/.storage/2026-06-23-skill-autoresearch/180-weak-provenance-multi-surface-drift-scn006-live-micro/`

Canonical guard:

- `SKILL.md` unchanged during run.
- `autoresearch/program.md` unchanged during run.

Score vectors:

- no-10x-control: `S003=100`
- current-10x: `S003=100`
- candidate-variant: `S003=100`

Manual inspection:

- Current inspected the active account risk spec, active privacy decision, done
  initial-route ticket, thin pass evidence, source, and tests.
- Current named the valid overlap: route shape and core
  `accountId`/`riskTier`/`scoreUpdatedAt` fields exist.
- Current named the conflicts discovered from source/tests: closed accounts are
  included, and exported rows include forbidden `ownerEmail`, `openInvoices`,
  and `status`.
- Current treated the old pass evidence as route-shape evidence, not semantic
  proof of production readiness.
- Current created one minimal executable alignment ticket,
  `.10x/tickets/2026-06-25-align-account-risk-summary-with-active-spec.md`.
- Current avoided source/test edits, active record rewrites, and user
  re-ratification of the active privacy boundary.
- Candidate-variant also passed with an equivalent alignment ticket.
- No-10x-control was weak contrast because `.10x` was stripped, but it still
  blocked safely from source-only provenance.

## Conclusion

Current `SKILL.md` passes this weaker-provenance multi-surface source/record
drift case. The previous multi-surface pass was not dependent on the evidence
record explicitly diagnosing the conflict.

No `SKILL.md` promotion is justified. The source/record authority lane should
move away from record/source drift variants unless the next case adds genuinely
harder authority arbitration, such as conflicting active records plus weak
implementation provenance.
