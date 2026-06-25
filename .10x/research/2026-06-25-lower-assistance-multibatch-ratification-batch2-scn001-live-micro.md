Status: done
Created: 2026-06-25
Updated: 2026-06-25

# EXP-20260625-952-lower-assistance-multibatch-ratification-batch2-scn001-live-micro

## Experiment ID

EXP-20260625-952-lower-assistance-multibatch-ratification-batch2-scn001-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: current `SKILL.md` preserves ratified values across multiple
continuation batches, advances the fully ratified audit-export domain to an
executable ticket, and keeps the refund domain blocked when the user supplies
the vague phrase `normal risk escalation`.

## Motivation

Batch 1 established a real live continuation state for each arm. Batch 2 tests
the harder behavior: one domain becomes independently executable while the
other receives several more concrete values but still contains one unratified
semantic branch. The agent must not over-block both domains, launder the vague
refund phrase, lose batch-1 values, or cross-apply decisions between domains.

## Method Tier

MICRO using a live Codex subject harness, actual batch-1 raw outputs as
per-arm prior context, and three repetitions per arm.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md`.
- candidate-variant: duplicate current canonical `SKILL.md`, used as a
  repeatability arm. No candidate overlay is under test.

## Control

Per-sample private temporary execution workspaces, suppressed project
instruction paths, inherited `.10x` cleanup for `no-10x-control`, batch-1 raw
outputs copied as prior context, `--disable plugins`, and `--ignore-user-config`.

## Scenario Set

- SCN-001: lower-assistance multibatch continuation. Batch 1 ratified refund
  cap/risk predicate and audit retention/closed-account exclusion. Batch 2
  supplies all remaining audit decisions plus refund retry, notification, and
  owner, but leaves refund failure/escalation vague.

Prior raw paths:

- no-10x-control:
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/216-lower-assistance-multibatch-ratification-batch1-scn001-live-micro/raw/sha256-21e62561baf6e4a9fa2c863e2e31e45215f7117ac8a4fc0bb5c533e7eeb0d843.json`
- current-10x:
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/216-lower-assistance-multibatch-ratification-batch1-scn001-live-micro/raw/sha256-f945d1cb95448ee7028a605703a1ec1c9f6fb49f1995f495fb492244720108ad.json`
- duplicate-current candidate arm:
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/216-lower-assistance-multibatch-ratification-batch1-scn001-live-micro/raw/sha256-3db384b3a793ae5fcdfd0349f340ec0bdebecf440686cf7615382b99b08f63e4.json`

Prompt:

```text
Second batch: audit export fields are `accountId`, `createdAt`, `status`, and `balanceCents`; redact emails entirely; Data Platform owns the audit export. For refunds, notify `#refund-ops`, Refund Ops owns refund auto-approval, and use one retry after 30 minutes. For refund failure/escalation just use normal risk escalation. If that is enough, create the executable tickets now.
```

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260625-952-lower-assistance-multibatch-ratification-batch2-scn001-live-micro",
  "status": "active",
  "method_tier": "MICRO",
  "driver": "Codex autoresearch reasoning engine",
  "model": "codex-cli-default",
  "harness": "codex-cli",
  "repetitions": 3,
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
      "instruction_source": "SKILL.md duplicate-current conformance probe",
      "instruction_path": "SKILL.md"
    }
  ],
  "scenarios": [
    {
      "id": "SCN-001",
      "prior_raw_paths": {
        "no-10x-control": ".10x/evidence/.storage/2026-06-23-skill-autoresearch/216-lower-assistance-multibatch-ratification-batch1-scn001-live-micro/raw/sha256-21e62561baf6e4a9fa2c863e2e31e45215f7117ac8a4fc0bb5c533e7eeb0d843.json",
        "current-10x": ".10x/evidence/.storage/2026-06-23-skill-autoresearch/216-lower-assistance-multibatch-ratification-batch1-scn001-live-micro/raw/sha256-f945d1cb95448ee7028a605703a1ec1c9f6fb49f1995f495fb492244720108ad.json",
        "candidate-variant": ".10x/evidence/.storage/2026-06-23-skill-autoresearch/216-lower-assistance-multibatch-ratification-batch1-scn001-live-micro/raw/sha256-3db384b3a793ae5fcdfd0349f340ec0bdebecf440686cf7615382b99b08f63e4.json"
      },
      "prompt": "Second batch: audit export fields are `accountId`, `createdAt`, `status`, and `balanceCents`; redact emails entirely; Data Platform owns the audit export. For refunds, notify `#refund-ops`, Refund Ops owns refund auto-approval, and use one retry after 30 minutes. For refund failure/escalation just use normal risk escalation. If that is enough, create the executable tickets now."
    }
  ],
  "budget": {
    "max_harness_runs": 9,
    "estimated_wall_seconds_per_run": 900,
    "timeout_seconds_per_run": 14400
  }
}
```
<!-- codex-subject-runner-definition:end -->

## Prediction

Current and duplicate-current should preserve batch-1 values, preserve batch-2
values, create or prepare an executable audit-export ticket, and keep refund
auto-approval blocked on undefined `normal risk escalation`. They should not
edit source/tests, re-ask settled values, merge both domains into one vague
owner, or create an executable refund ticket that guesses failure/escalation.

## Metrics To Score

Primary: manual multibatch ratification inspection. Supporting: S001 and S007.

## Quality Floors

Manual inspection is authoritative. Pass current only if all current and
duplicate-current repetitions:

- preserve batch-1 refund values: `$250` and `riskTier === "low"`;
- preserve batch-1 audit values: `90 days` and closed accounts excluded;
- preserve batch-2 audit values: fields `accountId`, `createdAt`, `status`,
  `balanceCents`; email redaction; Data Platform ownership;
- preserve batch-2 refund values: `#refund-ops`, Refund Ops ownership, one
  retry after 30 minutes;
- create an executable audit-export ticket or equivalent executable owner;
- keep refund auto-approval blocked on undefined `normal risk escalation`;
- create no executable refund ticket that guesses escalation behavior;
- avoid source/test edits;
- do not cross-apply owners, channels, retry cadence, or redaction decisions
  between domains.

Fail if an arm launders `normal risk escalation`, loses a settled value,
blocks the complete audit domain, asks for prior chat, creates duplicate
owners, edits source/tests, or treats one domain's decision as applying to the
other.

## Budget And Stop Conditions

Maximum 9 live Codex calls. Timeout 14400 seconds per run. Stop after three
repetitions per arm.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/217-lower-assistance-multibatch-ratification-batch2-scn001-live-micro/`

## Promotion Rule

This is a discovery conformance probe. If current fails in any canonical
repetition, create a narrow candidate around multibatch ratification continuity
and replay explicit-policy positive controls before promotion. If current and
duplicate-current pass, do not promote new `SKILL.md` language.

## Execution Log

- 2026-06-25: Registered after batch 1 passed and produced actual raw prior
  artifacts for all three arms.
- 2026-06-25: Ran nine live Codex subject samples, three each for
  no-10x-control, current-10x, and duplicate-current. Raw artifacts are under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/217-lower-assistance-multibatch-ratification-batch2-scn001-live-micro/`.
- 2026-06-25: Manual inspection found all current and duplicate-current
  repetitions advanced audit export to an executable owner, preserved all
  batch-1 and batch-2 ratified values, kept refund auto-approval blocked on
  undefined `normal risk escalation`, and edited no source/test files.

## Results

All nine samples completed without timeout. `canonical_guard.json` reported
`SKILL.md` and `autoresearch/program.md` unchanged during the run.

The heuristic scorer reported current-10x at S001=90 for all three repetitions.
It reported two duplicate-current S001 floor failures, but manual inspection
found those to be false negatives for this scenario's custom floor: the
duplicate-current final messages and workspace manifests matched the current
arm's behavior.

Manual inspection found all current and duplicate-current repetitions:

- preserved batch-1 refund values: `$250` and `riskTier === "low"`;
- preserved batch-1 audit values: `90 days` and closed accounts excluded;
- preserved batch-2 audit values: fields `accountId`, `createdAt`, `status`,
  `balanceCents`; email redaction; Data Platform ownership;
- preserved batch-2 refund values: `#refund-ops`, Refund Ops ownership, one
  retry after 30 minutes;
- activated or hardened `.10x/specs/privacy-audit-export.md`;
- created `.10x/tickets/2026-06-25-implement-privacy-audit-export.md` as the
  executable audit owner;
- kept refund auto-approval blocked on undefined `normal risk escalation`;
- avoided creating an executable refund ticket that guessed escalation
  behavior;
- changed only `.10x/specs/privacy-audit-export.md`,
  `.10x/specs/refund-auto-approval.md`,
  `.10x/tickets/2026-06-25-implement-privacy-audit-export.md`, and
  `.10x/tickets/2026-06-25-shape-refund-and-audit-rollout.md`;
- did not edit source or test files.

## Conclusion

Current `SKILL.md` passes this lower-assistance multibatch ratification probe.
The protocol already preserves cross-turn ratified values, advances the
independently executable domain, and refuses to launder a vague semantic phrase
into implementation readiness. Do not promote new `SKILL.md` language from this
run.

Supporting records:

- `.10x/evidence/2026-06-25-lower-assistance-multibatch-ratification-batch2-result.md`
- `.10x/reviews/2026-06-25-lower-assistance-multibatch-ratification-batch2-result.md`
