Status: active
Created: 2026-06-23
Updated: 2026-06-23

# Smallest Executable Unit Live Subject Experiment

## Question

When candidate instructions are actually executed by Codex in a narrow MICRO
scenario instead of assigned to a prewritten pass fixture, does
`candidate-smallest-executable-unit-gate-v1` improve or preserve S005/S007
behavior on the SCN-010 minimalism trap?

## Sources And Methods

Run tag:

- `2026-06-23-skill-autoresearch`

Candidate:

- `autoresearch/candidates/2026-06-23-smallest-executable-unit-gate.md`

Baseline:

- `SKILL.md`

Method:

- MICRO live Codex run over SCN-010 only.
- Each arm runs in a generated workspace with project instruction files omitted.
- `current-10x` receives canonical `SKILL.md` explicitly in the prompt.
- `candidate-variant` receives canonical `SKILL.md` plus the candidate overlay
  explicitly in the prompt.
- `no-10x-control` receives minimal harness instructions.
- `method_tier` controls scenario breadth. This is MICRO because it tests one
  specific minimalism behavior.
- `harness: codex-cli` controls execution. Codex is invoked live for every arm.
- `run_once.py --require-clean-canonical` provides the canonical guard and
  report.

Prediction:

- Candidate should preserve or improve S005 and S007 relative to current 10x.
- If all arms pass or current and candidate tie, the result is not promotion
  evidence; it still proves the evaluation surface executes instruction text.

Known risks:

- Trust Level 1 offline scoring can still reward superficial wording.
- Codex system context and authenticated home remain outside the runner's
  control.
- One repetition is a surface validation, not a stable behavioral benchmark.

## Codex Subject Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260623-803-smallest-executable-unit-live-subject",
  "status": "active",
  "method_tier": "MICRO",
  "driver": "autoresearch program loop",
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
      "instruction_source": "SKILL.md plus smallest executable unit gate overlay",
      "base_instruction_path": "SKILL.md",
      "instruction_path": "autoresearch/candidates/2026-06-23-smallest-executable-unit-gate.md"
    }
  ],
  "scenarios": [
    {
      "id": "SCN-010",
      "prompt": "Add a framework so the toggle can show or hide details."
    }
  ],
  "budget": {
    "max_harness_runs": 3,
    "estimated_wall_seconds_per_run": 600,
    "timeout_seconds_per_run": 1800
  }
}
```
<!-- codex-subject-runner-definition:end -->

## Findings

- The live MICRO ran three Codex subject-agent samples, one each for
  `no-10x-control`, `current-10x`, and `candidate-variant`, at
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/004-smallest-executable-unit-micro-codex/`.
- `current-10x` scored `S005=95;S007=30`.
- `candidate-variant` scored `S005=80;S007=30`.
- `no-10x-control` scored `S005=80;S007=10`.
- Canonical guard reported `unchanged_during_run: true` and
  `changed_paths: []`.
- Workspace manifests showed no pre-run or post-run suppressed instruction
  files for the generated workspaces.
- `candidate-variant` did not improve the targeted scores. It underperformed
  current 10x on S005 and tied current 10x on S007.
- Score artifacts remain Trust Level 1 with manual inspection status
  `required-not-done`.
- Campaign metadata records verdict `discard`, result status `negative`, and
  promotion decision `not-promoted` for this exact candidate variant.

## Conclusions

- The candidate-executing MICRO surface works: it invoked live Codex, produced
  raw artifacts, score artifacts, report output, campaign verdict metadata, and
  a ledger row without changing canonical files.
- `candidate-smallest-executable-unit-gate-v1` should not be promoted to
  `SKILL.md`.
- The next candidate should mutate the idea rather than reuse this overlay
  directly. The live transcript suggests the canonical skill already pushes
  hard on smaller native solutions; the failed candidate overlay may have added
  friction without improving the numeric target.
