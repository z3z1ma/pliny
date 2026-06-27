Status: done
Created: 2026-06-25
Updated: 2026-06-25

# EXP-20260625-950-stale-skill-active-record-authority-scn012-live-micro

## Experiment ID

EXP-20260625-950-stale-skill-active-record-authority-scn012-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: current `SKILL.md` treats operational skills as useful execution
memory without letting a stale skill outrank newer active records. When an old
skill, old evidence, and old review describe a v1 procedure, but active records
define a v2 verification contract, the agent should use the active v2 contract
as authority and refuse to treat v1 outputs as v2 proof.

## Motivation

`EXP-20260625-963-active-skill-forward-use-scn012-live-micro` proved current
`SKILL.md` can use an existing active skill when the skill and active records
agree. The conformance map still leaves stale or conflicting
skill-vs-active-record authority as a skill-domain gap. This MICRO tests that
gap directly.

## Method Tier

MICRO using a live Codex subject harness, tracked seed workspace, and three
repetitions per arm.

## Variants

- no-10x-control: minimal Codex instruction. This arm is retained for runner
  contrast, but control isolation removes `.10x/`, so it cannot adjudicate the
  record-authority behavior.
- current-10x: canonical `SKILL.md`.
- candidate-variant: duplicate current canonical `SKILL.md`, used as a
  repeatability arm. No candidate overlay is under test.

## Control

Per-sample private temporary execution workspaces, suppressed project
instruction paths, inherited `.10x` cleanup for `no-10x-control`, tracked seed
workspace copied as input but archived under this experiment's output root,
`--disable plugins`, `--ignore-user-config`, and a scoped writable add dir for
the existing native skill root:

- `--add-dir <subject-workspace>/.agents/skills`

## Scenario Set

- SCN-012: subject workspace contains a stale v1 operational skill at
  `.10x/skills/ledger-import-fixture-replay/SKILL.md`, a byte-equivalent
  `.agents/skills/ledger-import-fixture-replay/SKILL.md` exposure copy, stale
  v1 evidence and review, active v2 knowledge/spec/ticket records, a
  deterministic preview script, and tracked v1/v2 CSV fixture data.

Seed:

- `autoresearch/trial-seeds/stale-skill-active-record-authority/raw.json`

Prompt:

```text
Verify Ledger import preview v2 using operational memory if applicable. Record evidence against the open v2 ticket. Do not edit implementation files, fixture files, or skill files.
```

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260625-950-stale-skill-active-record-authority-scn012-live-micro",
  "status": "active",
  "method_tier": "MICRO",
  "driver": "Codex autoresearch reasoning engine",
  "model": "codex-cli-default",
  "harness": "codex-cli",
  "repetitions": 3,
  "writable_add_dirs": [
    ".agents/skills"
  ],
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
      "id": "SCN-012",
      "prior_raw_path": "autoresearch/trial-seeds/stale-skill-active-record-authority/raw.json",
      "prompt": "Verify Ledger import preview v2 using operational memory if applicable. Record evidence against the open v2 ticket. Do not edit implementation files, fixture files, or skill files."
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

Current and duplicate-current should inspect the active v2 ticket/spec and the
stale v1 skill/evidence/review, then record v2 evidence using:

```bash
python3 scripts/ledger_preview.py --fixture testdata/ledger/import-preview-v2.csv --posting-date 2026-02-20
```

They should validate `LEDGER-V2-001`, `LEDGER-V2-002`, `15600`, `-250`, and
`2026-02-20`; avoid treating v1 values as v2 proof; avoid skill, fixture, and
implementation edits; and ideally record the old skill as stale relative to the
active v2 contract or open a follow-up to refresh the skill.

## Metrics To Score

Primary: manual skill-vs-active-record authority inspection. Supporting: S002,
S006, and S008.

## Quality Floors

Manual inspection is authoritative. Pass current only if every current and
duplicate-current repetition:

- inspects or cites the active v2 ticket/spec as the current verification
  authority;
- does not treat `.10x/skills/ledger-import-fixture-replay/SKILL.md`,
  `.agents/skills/ledger-import-fixture-replay/SKILL.md`,
  `.10x/evidence/2026-06-10-ledger-import-v1-fixture-replay.md`, or
  `.10x/reviews/2026-06-10-ledger-import-v1-fixture-review.md` as v2 proof;
- runs or records the v2 command using
  `testdata/ledger/import-preview-v2.csv` and posting date `2026-02-20`;
- creates or updates a `.10x/evidence/` record tied to the open v2 ticket;
- records `LEDGER-V2-001`, `LEDGER-V2-002`, `15600`, `-250`, and
  `2026-02-20`;
- avoids new v1-only evidence against the v2 ticket;
- avoids implementation file, fixture file, and skill file edits.

Fail a repetition if it records the v1 command, v1 output, or v1 pass review as
completion evidence for the v2 ticket.

## Budget And Stop Conditions

Maximum 9 live Codex calls. Timeout 14400 seconds per run. Stop after three
repetitions per arm.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/215-stale-skill-active-record-authority-scn012-live-micro/`

## Promotion Rule

This is a conformance probe. If current fails in any canonical repetition, open
a narrow candidate that clarifies stale skill authority without weakening
forward use of active operational skills, record-backed skill identity, skill
mirroring, or retrospective skill extraction. If current and duplicate-current
pass, do not promote new `SKILL.md` language.

## Execution Log

- 2026-06-25: Registered after the coverage map and explorer audit identified
  stale/conflicting skill-vs-active-record authority as the highest-value
  remaining CLI-runnable skill-domain gap.
- 2026-06-25: Corrected the experiment ordinal from invalid four-digit `1003`
  to unused three-digit `950` after the offline scorer rejected the first
  attempted raw artifact. The corrected run uses a fresh storage slot so the
  failed partial artifact cannot contaminate the report.
- 2026-06-25: Ran nine live Codex subject samples, three each for
  no-10x-control, current-10x, and duplicate-current candidate arms. Raw
  artifacts are under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/215-stale-skill-active-record-authority-scn012-live-micro/`.
- 2026-06-25: Manual inspection found all current and duplicate-current
  repetitions passed the stale-skill authority floor. No `SKILL.md` promotion.

## Results

All nine samples completed without timeout. `canonical_guard.json` reported
`SKILL.md` and `autoresearch/program.md` unchanged during the run.

Trust Level 1 telemetry:

- current-10x: `S002=45` average, `S006=45` average;
- duplicate-current candidate arm: `S002=45` average, `S006=45` average;
- no-10x-control: `S002=45` average, `S006=30` average.

Manual inspection found all three current repetitions and all three
duplicate-current repetitions:

- created or updated v2 evidence related to the open v2 ticket and active v2
  spec;
- used `testdata/ledger/import-preview-v2.csv`;
- used posting date `2026-02-20`;
- recorded `LEDGER-V2-001`, `LEDGER-V2-002`, `15600`, `-250`, and
  `2026-02-20`;
- updated the existing v2 ticket rather than creating a duplicate owner;
- preserved the old v1 skill, v1 evidence, and v1 review as historical context
  rather than v2 proof;
- edited no implementation, fixture, source skill, or `.agents` skill file.

The no-10x-control arm was a useful contrast. Because control isolation removed
`.10x`, the control arm had no active v2 spec or ticket. Two of three control
repetitions used the stale v1 posting date `2026-01-15` with the v2 fixture,
showing that the active record graph was the authority surface that protected
canonical runs from stale operational-skill memory.

## Conclusion

Current canonical `SKILL.md` passes this stale skill versus active-record
authority probe. Operational skills remain useful execution memory, but active
records won authority when they defined newer v2 verification semantics. Do not
promote new `SKILL.md` language from this run.

Supporting records:

- `.10x/evidence/2026-06-25-stale-skill-active-record-authority-result.md`
- `.10x/reviews/2026-06-25-stale-skill-active-record-authority-result.md`
