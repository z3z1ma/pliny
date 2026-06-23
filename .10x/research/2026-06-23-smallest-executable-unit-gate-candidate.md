Status: active
Created: 2026-06-23
Updated: 2026-06-23

# Smallest Executable Unit Gate Candidate Experiment

## Question

Does the smallest executable unit gate create a plausible improvement path for
S003 ticket readiness and S005 scope minimalism without mutating canonical
`SKILL.md`?

## Sources And Methods

Run tag:

- `2026-06-23-skill-autoresearch`

Candidate:

- `autoresearch/candidates/2026-06-23-smallest-executable-unit-gate.md`

Baseline:

- `SKILL.md`

Method:

- MICRO fixture-backed run over SCN-006, SCN-010, and SCN-011.
- Canonical guard enabled through `run_once.py --require-clean-canonical`.
- Results logged to `results.tsv`.

Expected limitation:

- This fixture-backed run does not execute the candidate instructions live. It
  can only verify that the candidate does not regress known fixture traps and
  that the control arm still exposes failures where negative fixtures exist.

## MICRO Runner Definition

<!-- micro-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260623-802-smallest-executable-unit-gate-micro",
  "status": "active",
  "method_tier": "MICRO",
  "driver": "autoresearch program loop",
  "model": "fixture-model",
  "harness": "micro-fixture",
  "repetitions": 1,
  "arms": [
    {
      "id": "no-10x-control",
      "instruction_source": "minimal harness defaults",
      "instruction_digest": "sha256:no10x-placeholder"
    },
    {
      "id": "current-10x",
      "instruction_source": "SKILL.md",
      "instruction_path": "SKILL.md"
    },
    {
      "id": "candidate-variant",
      "instruction_source": "autoresearch/candidates/2026-06-23-smallest-executable-unit-gate.md",
      "instruction_path": "autoresearch/candidates/2026-06-23-smallest-executable-unit-gate.md"
    }
  ],
  "scenarios": [
    {
      "id": "SCN-006",
      "fixtures": {
        "no-10x-control": "autoresearch/fixtures/offline/scn006-fail.json",
        "current-10x": "autoresearch/fixtures/offline/scn006-pass.json",
        "candidate-variant": "autoresearch/fixtures/offline/scn006-pass.json"
      }
    },
    {
      "id": "SCN-010",
      "fixtures": {
        "no-10x-control": "autoresearch/fixtures/offline/scn010-fail.json",
        "current-10x": "autoresearch/fixtures/offline/scn010-pass.json",
        "candidate-variant": "autoresearch/fixtures/offline/scn010-pass.json"
      }
    },
    {
      "id": "SCN-011",
      "fixtures": {
        "no-10x-control": "autoresearch/fixtures/offline/scn011-pass.json",
        "current-10x": "autoresearch/fixtures/offline/scn011-pass.json",
        "candidate-variant": "autoresearch/fixtures/offline/scn011-pass.json"
      }
    }
  ],
  "budget": {
    "estimated_wall_seconds_per_sample": 0
  }
}
```
<!-- micro-runner-definition:end -->

## Findings

- 2026-06-23: MICRO run completed at
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/002-smallest-executable-unit-gate-micro/`
  with canonical guard unchanged for `SKILL.md` and
  `autoresearch/program.md`.
- Candidate arm tied current 10x on all measured target scores:
  - SCN-006: candidate `S003=100`; current `S003=100`; no-10x control
    `S003=10`.
  - SCN-010: candidate `S005=100`, `S007=75`; current `S005=100`,
    `S007=75`; no-10x control `S005=35`, `S007=10`.
  - SCN-011: candidate `S005=100`; current `S005=100`; no-10x control
    `S005=100`.
- The run confirms control discrimination on SCN-006 and SCN-010, but SCN-011
  does not distinguish the no-10x control because only a passing fixture exists.
- Durable evidence:
  `.10x/evidence/2026-06-23-smallest-executable-unit-gate-micro.md`.

## Conclusions

- Do not promote this candidate from the current MICRO result. It passed the
  known guardrail fixtures but did not distinguish itself from current
  `SKILL.md`.
- Treat the result as a mutation signal. The next research move should add a
  live or manually inspected evaluation surface that executes candidate
  instruction text, or it should create a narrower discriminating scenario
  before producing more candidate overlays.
