Status: done
Created: 2026-06-25
Updated: 2026-06-25

# EXP-20260625-963-active-skill-forward-use-scn012-live-micro

## Experiment ID

EXP-20260625-963-active-skill-forward-use-scn012-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: `candidate-active-skill-forward-use-v1` improves downstream use of
already-authored operational skills by making skill discovery and execution
salient before an agent re-derives a known procedure.

## Motivation

Recent runs proved current `SKILL.md` can author, mirror, name, and repair
skills. The next uncovered behavior is forward use: a later agent should
recognize that an active skill already owns a repeatable procedure and should
execute that skill's validation rather than inventing an adjacent workflow.

## Method Tier

MICRO using a live Codex subject harness, tracked seed workspace, and five
repetitions per arm.

## Variants

- no-10x-control: minimal Codex instruction. This arm is a required runner
  comparator but is not promotion authority.
- current-10x: canonical `SKILL.md`.
- candidate-variant: canonical `SKILL.md` plus
  `candidate-active-skill-forward-use-v1`.

## Control

Per-sample private temporary execution workspaces, suppressed project
instruction paths, inherited `.10x` cleanup for `no-10x-control`, tracked seed
workspace copied as input but archived under this experiment's output root,
`--disable plugins`, `--ignore-user-config`, and a scoped writable add dir for
the existing native skill root:

- `--add-dir <subject-workspace>/.agents/skills`

## Scenario Set

- SCN-012: subject workspace contains an already-authored Ledger import fixture
  replay skill at `.10x/skills/ledger-import-fixture-replay/SKILL.md`, an
  equivalent `.agents/skills/ledger-import-fixture-replay/SKILL.md` exposure
  copy, active Ledger import vocabulary and preview spec records, an open
  verification ticket, a deterministic preview script, tracked CSV fixture
  data, and a stale historical note that names inline CSV/current-date/
  `externalId` behavior.

Seed:

- `autoresearch/trial-seeds/skill-forward-use-ledger-replay/raw.json`

Prompt:

```text
Verify the Ledger import preview using the existing tracked fixture procedure and record evidence against the open ticket. Use the project's existing operational memory if it already contains an applicable procedure. Do not edit implementation files.
```

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260625-963-active-skill-forward-use-scn012-live-micro",
  "status": "active",
  "method_tier": "MICRO",
  "driver": "Codex autoresearch reasoning engine",
  "model": "codex-cli-default",
  "harness": "codex-cli",
  "repetitions": 5,
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
      "instruction_source": "SKILL.md plus candidate-active-skill-forward-use-v1",
      "base_instruction_path": "SKILL.md",
      "instruction_path": "autoresearch/candidates/2026-06-25-active-skill-forward-use.md"
    }
  ],
  "scenarios": [
    {
      "id": "SCN-012",
      "prior_raw_path": "autoresearch/trial-seeds/skill-forward-use-ledger-replay/raw.json",
      "prompt": "Verify the Ledger import preview using the existing tracked fixture procedure and record evidence against the open ticket. Use the project's existing operational memory if it already contains an applicable procedure. Do not edit implementation files."
    }
  ],
  "budget": {
    "max_harness_runs": 15,
    "estimated_wall_seconds_per_run": 900,
    "timeout_seconds_per_run": 7200
  }
}
```
<!-- codex-subject-runner-definition:end -->

## Prediction

Candidate should improve the probability that the subject:

- inspects `.10x/skills/ledger-import-fixture-replay/SKILL.md` or the
  equivalent `.agents` exposure copy;
- runs `python3 scripts/ledger_preview.py --fixture testdata/ledger/import-preview.csv --posting-date 2026-01-15`;
- records evidence with the command and JSON output;
- validates `sourceRef` values `LEDGER-001` and `LEDGER-002`;
- validates `amountCents` values `12345` and `-678`;
- validates posting date `2026-01-15`;
- avoids inline CSV, wall-clock date dependence, and `externalId`;
- avoids implementation edits.

## Metrics To Score

Primary: manual skill forward-use and evidence inspection. Supporting: S002,
S006, and S008.

## Quality Floors

Manual inspection is authoritative. Candidate is promising only if every
candidate repetition:

- inspects or cites the active skill as the operational procedure owner;
- runs the exact fixture replay command or a behaviorally equivalent command
  using `testdata/ledger/import-preview.csv` and posting date `2026-01-15`;
- creates or updates a `.10x/evidence/` record with the observed command,
  output, validation, and limits;
- records `LEDGER-001`, `LEDGER-002`, `12345`, `-678`, and `2026-01-15`;
- avoids inline CSV construction, wall-clock date dependence, and `externalId`;
- avoids implementation file, fixture, script, and skill edits.

Current is the baseline. Promote only if candidate improves skill forward-use
without weakening record authority or evidence integrity.

## Budget And Stop Conditions

Maximum 15 live Codex calls. Timeout 7200 seconds per run. Stop after five
repetitions per arm.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/211-active-skill-forward-use-scn012-live-micro/`

## Promotion Rule

If candidate improves forward-use in the primary run, run at least three
regression controls before promotion: skill-vs-knowledge routing, divergent
mirror repair, and a source/record drift case where a stale skill-like
procedure must not override active authority. Discard as null if current already
uses the skill consistently.

## Execution Log

- 2026-06-25: Registered after EXP-962 discarded terminal-record hygiene as a
  null result and the coverage map identified forward-use validation of
  generated skills as the next CLI-runnable gap.
- 2026-06-25: Ran 15 live Codex subject samples, five each for no-10x-control,
  current-10x, and candidate-variant. Raw artifacts are under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/211-active-skill-forward-use-scn012-live-micro/`.
- 2026-06-25: Manual inspection found current and candidate both clean on the
  targeted active-skill forward-use floor. Candidate discarded as null; no
  `SKILL.md` promotion.

## Results

All samples completed without timeout. `canonical_guard.json` reported
`SKILL.md` and `autoresearch/program.md` unchanged during the run.

Trust Level 1 telemetry:

- candidate-variant: `S002=45` average, `S006=45` average;
- current-10x: `S002=45` average, `S006=45` average;
- no-10x-control: `S002=45` average, `S006=30` average.

Manual inspection found all five current repetitions and all five candidate
repetitions:

- created one `.10x/evidence/` record for fixture replay;
- used the existing active skill or existing tracked fixture procedure;
- ran the fixture replay command with `testdata/ledger/import-preview.csv` and
  posting date `2026-01-15`;
- recorded `LEDGER-001`, `LEDGER-002`, `12345`, `-678`, and `2026-01-15`;
- updated the verification ticket or moved it to `tickets/done/`;
- avoided `externalId` in changed evidence/ticket files;
- edited no implementation, fixture, script, or skill files.

The no-10x-control arm also used the `.agents` skill exposure and recorded
evidence, but because the runner removed `.10x` for control, it lacked the
existing verification ticket and source `.10x` skill context. It is therefore a
useful harness-shape observation but not promotion authority.

One candidate repetition moved the verification ticket to `tickets/done/`. All
other current and candidate repetitions left the ticket open with progress
evidence. The prompt asked to verify and record evidence against the open
ticket, not explicitly to close it, so this difference is not treated as a
candidate win.

## Conclusion

`candidate-active-skill-forward-use-v1` is a null result. Current canonical
`SKILL.md` already supports forward use of an active operational skill in this
subject workspace. Adding an explicit skill-use paragraph would increase prompt
surface without measured reliability gain.

Supporting records:

- `.10x/evidence/2026-06-25-active-skill-forward-use-result.md`
- `.10x/reviews/2026-06-25-active-skill-forward-use-result.md`
