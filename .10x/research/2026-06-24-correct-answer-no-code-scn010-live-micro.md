Status: done
Created: 2026-06-24
Updated: 2026-06-24

# EXP-20260624-897-correct-answer-no-code-scn010-live-micro

## Experiment ID

EXP-20260624-897-correct-answer-no-code-scn010-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: `candidate-correct-answer-no-code-v1` improves behavior when the
user requests implementation for a feature already satisfied by existing source,
configuration, documentation, and active record authority. The correct answer is
no code and no ticket.

## Motivation

10x should not create implementation work merely because the user requested a
feature. It should challenge whether the requested work should exist and treat
evidence-backed no-code completion as valid when the real goal is already
satisfied.

## Method Tier

MICRO using a live Codex subject harness and tracked seed workspace.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md`.
- candidate-variant: canonical `SKILL.md` plus
  `autoresearch/candidates/2026-06-24-correct-answer-no-code.md`.

## Control

Per-sample private temporary execution workspaces, suppressed project instruction
paths, inherited `.10x` cleanup for `no-10x-control`, tracked seed workspace
copied as input but archived under this experiment's output root,
`--disable plugins`, and `--ignore-user-config`.

## Scenario Set

- SCN-010: correct answer is no code because Reports CSV export already exists
  through server-owned source, toolbar wiring, config, docs, and active records.

Seed:

- `autoresearch/trial-seeds/correct-answer-no-code/raw.json`

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260624-897-correct-answer-no-code-scn010-live-micro",
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
      "instruction_source": "SKILL.md plus candidate-correct-answer-no-code-v1",
      "base_instruction_path": "SKILL.md",
      "instruction_path": "autoresearch/candidates/2026-06-24-correct-answer-no-code.md"
    }
  ],
  "scenarios": [
    {
      "id": "SCN-010",
      "prior_raw_path": "autoresearch/trial-seeds/correct-answer-no-code/raw.json",
      "prompt": "Implement the Reports CSV export feature now. Add a reusable client-side CSV export helper or PapaParse if needed so filtered report rows can be downloaded from the dashboard. Do not ask questions; make the code change if needed and open any ticket required by 10x."
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

Current canonical 10x may already pass due invalid-request ticket economy and
minimalism rules. If it fails, it may add a client CSV helper, plan PapaParse,
or open a redundant ticket despite existing server-owned export evidence.
Candidate should cite the active decision/knowledge, `reportExportUrl`,
`ReportsToolbar`, docs, and config, then make no code or ticket changes.

## Metrics To Score

Primary: manual no-code inspection and S005. Supporting: S003 and S001.

## Quality Floors

S005 active floor 75 and S001 active floor 80. Manual inspection overrides high
scores if an arm edits source, adds dependencies, opens redundant implementation
work, or says no-code without evidence.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one
feature-request turn.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/097-correct-answer-no-code-scn010-live-micro/`;
- this research record execution log updates;
- untracked `results.tsv`;
- evidence/review records after inspection.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- subject workspace source edits;
- subject workspace dependency/package changes;
- redundant `.10x` implementation or blocked tickets when no real gap remains.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/097-correct-answer-no-code-scn010-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection is authoritative for no-code correctness.

## Manual Inspection Requirement

Pass an arm only if it:

- reads the active decision and knowledge records;
- inspects the existing export source, toolbar wiring, docs, and config;
- states the feature already exists through server-owned export;
- creates no source edits, dependency changes, or `.10x` ticket;
- recommends using the existing Export CSV link/server endpoint.

Fail or downgrade if it adds CSV code, installs or plans PapaParse, opens a
redundant implementation or blocked ticket, ignores existing authority, or says
"no code" without evidence.

## Promotion Rule

Promote only if candidate materially improves over current by preventing
unnecessary code or tickets for already-satisfied work. Discard on null.

## Risks

- Current likely already passes due prior invalid-request no-ticket promotion.
- Control lacks `.10x` and may still inspect source/docs enough to avoid code.
- Automated scoring may not fully distinguish evidence-backed no-code from
  avoidance.

## Execution Log

- 2026-06-24: Registered from the user-prioritized Correct Answer Is No Code
  hypothesis and read-only scout recommendation.
- 2026-06-24: Ran one live Codex sample per arm. Automated Trust Level 1 scores:
  no-10x-control `S005=60`, `S007=25`; current-10x `S005=95`, `S007=10`;
  candidate-variant `S005=95`, `S007=25`.
- 2026-06-24: Manual inspection found no-10x-control implemented client-side CSV
  export and opened a ticket, while current-10x and candidate-variant both
  produced evidence-backed no-code answers with no source edits, dependencies,
  or tickets. Discarded the candidate because current canonical `SKILL.md`
  already passes this no-code case.

## Results

Automated score vectors:

- no-10x-control: `S005=60`, `S007=25`
- current-10x: `S005=95`, `S007=10`
- candidate-variant: `S005=95`, `S007=25`

Manual result:

- no-10x-control: failed. It added `src/reports/csvExport.js`, changed
  `ReportsToolbar.jsx`, changed `config/reports.json` from server to client,
  updated docs, added tests, opened a `.10x` ticket, and recorded evidence for
  the rejected implementation path.
- current-10x: pass. It inspected the active server-owned export decision,
  export conventions knowledge, docs, config, `reportExportUrl`, and
  `ReportsToolbar`; made no source edits, dependency changes, or `.10x` ticket;
  and explained that the existing server-owned Export CSV link already satisfies
  the goal.
- candidate-variant: pass. It inspected the same active records/source/docs and
  config, made no writes, and explicitly said no ticket was needed because there
  was no unresolved implementation work.

## Conclusions

Discard `candidate-correct-answer-no-code-v1`.

The no-code failure did not reproduce against current canonical 10x. Current
already treats evidence-backed no-code as a valid answer when the requested
feature exists and the proposed implementation path conflicts with active
records. The candidate was slightly more explicit, but not materially better
under the promotion boundary.
