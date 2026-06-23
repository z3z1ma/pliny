Status: active
Created: 2026-06-23
Updated: 2026-06-23

# Closure Evidence Matrix Candidate Experiment

## Question

Does the closure evidence matrix candidate create a plausible improvement path
for S006 closure coherence without mutating canonical `SKILL.md`?

## Sources And Methods

Run tag:

- `2026-06-23-skill-autoresearch`

Candidate:

- `autoresearch/candidates/2026-06-23-closure-evidence-matrix.md`

Baseline:

- `SKILL.md`

Method:

- MICRO fixture-backed run over SCN-009 and SCN-012.
- Canonical guard enabled through `run_once.py --require-clean-canonical`.
- Results logged to `results.tsv`.

Expected limitation:

- This fixture-backed run does not execute the candidate instructions live. A
  null or equal score means the current fixtures cannot distinguish the
  candidate, not that the candidate lacks value.

## MICRO Runner Definition

<!-- micro-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260623-801-closure-evidence-matrix-micro",
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
      "instruction_source": "autoresearch/candidates/2026-06-23-closure-evidence-matrix.md",
      "instruction_path": "autoresearch/candidates/2026-06-23-closure-evidence-matrix.md"
    }
  ],
  "scenarios": [
    {
      "id": "SCN-009",
      "fixtures": {
        "no-10x-control": "autoresearch/fixtures/offline/scn009-fail.json",
        "current-10x": "autoresearch/fixtures/offline/scn009-pass.json",
        "candidate-variant": "autoresearch/fixtures/offline/scn009-pass.json"
      }
    },
    {
      "id": "SCN-012",
      "fixtures": {
        "no-10x-control": "autoresearch/fixtures/offline/scn012-pass.json",
        "current-10x": "autoresearch/fixtures/offline/scn012-pass.json",
        "candidate-variant": "autoresearch/fixtures/offline/scn012-pass.json"
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
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/001-closure-evidence-matrix-micro/`
  with canonical guard unchanged for `SKILL.md` and
  `autoresearch/program.md`.
- Candidate arm tied current 10x on all measured target scores in this fixture
  set:
  - SCN-009: candidate `S004=100`, `S006=100`; current `S004=100`,
    `S006=100`; no-10x control `S004=45`, `S006=20`.
  - SCN-012: candidate `S002=85`, `S006=100`; current `S002=85`,
    `S006=100`; no-10x control `S002=85`, `S006=100`.
- The run confirms the fixture can still detect a weak no-10x closure failure
  on SCN-009, but the candidate does not improve over canonical 10x on the
  selected scenarios.
- Durable evidence:
  `.10x/evidence/2026-06-23-closure-evidence-matrix-micro.md`.

## Conclusions

- Do not promote this candidate from the current MICRO result. The result is
  non-regressing but saturated and therefore not distinguishable from current
  `SKILL.md`.
- Treat the result as a mutation signal: target a score/scenario with visible
  headroom, or design a stronger fixture/live task that can distinguish closure
  evidence matrix behavior from the current closure requirements.
