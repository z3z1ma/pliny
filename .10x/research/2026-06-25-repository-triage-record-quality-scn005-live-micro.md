Status: done
Created: 2026-06-25
Updated: 2026-06-25

# EXP-20260625-975-repository-triage-record-quality-scn005-live-micro

## Experiment ID

EXP-20260625-975-repository-triage-record-quality-scn005-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: current `SKILL.md` can perform broader repository record-quality
triage without record spam or lifecycle confusion. Given active, done,
cancelled, stale research, source, tests, and docs, it should reuse an existing
test-gap owner, open only the uncovered docs-gap ticket, update relevant parent
state, and avoid reviving historical or stale records.

## Motivation

Record ontology and record graph authority are strong for focused cases. The
remaining coverage-map gap is broader repeated-session or repository-scale
maintenance, where multiple surfaces create tempting but distinct routing
actions. This MICRO tests a small repository-triage version of that risk.

## Method Tier

MICRO using a live Codex subject harness and tracked seed workspace.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md`.
- candidate-variant: duplicate canonical `SKILL.md` conformance-probe arm. No
  candidate overlay is under test.

## Control

Per-sample private temporary execution workspaces, suppressed project
instruction paths, inherited `.10x` cleanup for `no-10x-control`, tracked seed
workspace copied as input but archived under this experiment's output root,
`--disable plugins`, and `--ignore-user-config`.

## Scenario Set

- SCN-005: account export repository triage. The workspace contains an active
  export spec, active parent ticket, existing active email-redaction test ticket,
  done visible-filter child, cancelled legacy adapter ticket, stale row-limit
  research, source/tests that satisfy visible filtering but lack explicit email
  redaction assertion, and operator docs that still list `email`.

Seed:

- `autoresearch/fixtures/live-seeds/repository-triage-record-quality/raw.json`

Prompt:

```text
Fresh session. Triage account export hardening from this workspace's `.10x` records, source, tests, and docs. Route only real gaps to durable owners. If an existing record already owns a gap, reuse or update it instead of opening a duplicate. If a real gap is uncovered, open the smallest bounded ticket for that gap. Keep done, cancelled, and stale research records historical unless current active records make them relevant. Do not edit source, tests, or docs. Do not ask for prior chat.
```

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260625-975-repository-triage-record-quality-scn005-live-micro",
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
      "id": "SCN-005",
      "prior_raw_path": "autoresearch/fixtures/live-seeds/repository-triage-record-quality/raw.json",
      "prompt": "Fresh session. Triage account export hardening from this workspace's `.10x` records, source, tests, and docs. Route only real gaps to durable owners. If an existing record already owns a gap, reuse or update it instead of opening a duplicate. If a real gap is uncovered, open the smallest bounded ticket for that gap. Keep done, cancelled, and stale research records historical unless current active records make them relevant. Do not edit source, tests, or docs. Do not ask for prior chat."
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

Current should inspect `.10x`, source, tests, and docs. It should identify:

- existing active ticket
  `.10x/tickets/2026-06-25-add-account-export-email-redaction-test.md` already
  owns the missing email-redaction test gap;
- `docs/account-export.md` still lists `email`, and no existing active ticket
  owns the docs correction;
- done visible-filter ticket/evidence are historical and already terminal;
- cancelled legacy adapter is not active authority;
- stale 2025 row-limit research should not create current row-limit work.

It should open exactly one new docs ticket, update the parent and/or existing
test ticket only as needed, and avoid source/test/docs edits.

## Metrics To Score

Primary: manual record-quality triage and record-economy inspection. Supporting:
S002 and S005.

## Quality Floors

Manual inspection is authoritative. Pass current only if it:

- inspects active spec, active parent, active test ticket, done child/evidence,
  cancelled ticket, stale research, source, tests, and docs;
- reuses the existing email-redaction test ticket rather than opening a
  duplicate;
- creates exactly one bounded operator-docs alignment ticket or updates a true
  existing docs owner if one exists;
- updates the parent ticket only for triage progress, dependencies, or blockers
  that remain true;
- treats done, cancelled, and stale research records as historical or stale
  rather than active implementation authority;
- does not edit source, tests, docs, implementation files, or stale research;
- does not create a broad catch-all parent, source implementation ticket,
  legacy adapter ticket, row-limit ticket, or duplicate visible-filter ticket.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one
repository-triage turn.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/175-repository-triage-record-quality-scn005-live-micro/`;
- subject workspace `.10x` ticket updates or one new docs ticket;
- this research record execution log updates;
- untracked `results.tsv`;
- evidence/review records after inspection.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- subject workspace source/test/docs edits;
- duplicate or catch-all `.10x` records.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/175-repository-triage-record-quality-scn005-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection required for record routing, duplicate-owner detection, and lifecycle
authority.

## Promotion Rule

No behavioral candidate is under test. If current fails this broader triage by
creating duplicate owners, reviving historical records, or editing source/docs,
create a narrow candidate around repository triage and lifecycle-aware record
economy. If current passes, update coverage only.

## Risks

- The prompt directly asks for record economy. Future variants can reduce
  assistance if current passes.
- There is more than one acceptable path for parent-ticket progress notes.
  Manual inspection should judge ownership and boundary correctness, not exact
  prose.

## Execution Log

- 2026-06-25: Registered after EXP-974 covered mechanical record maintenance
  and the coverage map still named broader repository triage as a record-quality
  gap.
- 2026-06-25: Ran one live Codex repetition for no-10x-control, current-10x,
  and duplicate-current candidate arms. Raw artifacts are stored under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/175-repository-triage-record-quality-scn005-live-micro/`.
- 2026-06-25: Manual inspection passed current `SKILL.md`. Current inspected
  the relevant active records, historical records, stale research, source,
  tests, and docs; reused the existing email-redaction test ticket; opened one
  bounded docs-alignment ticket; updated the parent with triage progress; and
  changed no source, tests, docs, `SKILL.md`, or `autoresearch/program.md`.
- 2026-06-25: Trust Level 1 S002 scored current and duplicate-current at 50
  for "record spam", but manual inspection classifies this as a false negative:
  the run created exactly one new durable owner and only updated two existing
  relevant owners.

## Results

Current `SKILL.md` passed the repository triage probe.

Current changed exactly three `.10x` ticket records in the subject workspace:

- updated existing parent ticket
  `.10x/tickets/2026-06-25-account-export-hardening-parent.md`;
- updated existing open test owner
  `.10x/tickets/2026-06-25-add-account-export-email-redaction-test.md`;
- created one new docs owner
  `.10x/tickets/2026-06-25-remove-account-export-email-from-docs.md`.

It did not edit source, tests, docs, package metadata, stale research, done
tickets, cancelled tickets, `SKILL.md`, or `autoresearch/program.md`.

Duplicate-current produced materially equivalent behavior. The no-10x-control
arm also opened a single docs ticket, but because the control workspace had its
inherited `.10x` removed, it did not exercise reuse of the existing parent and
test-ticket owners.

## Conclusions

No `SKILL.md` promotion is justified. Current already handles this broader
repository-scale record triage shape without duplicate owners, historical-record
revival, or implementation drift.

This closes the immediate coverage-map gap for repository-scale record-quality
triage. Remaining record-quality upside should come from longer repeated-session
maintenance, sharper lower-assistance lifecycle cases, or cross-harness/app
subagent behavior rather than another one-turn repository triage fixture.
