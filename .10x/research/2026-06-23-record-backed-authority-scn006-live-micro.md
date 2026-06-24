Status: done
Created: 2026-06-23
Updated: 2026-06-23

# EXP-20260623-838-record-backed-authority-scn006-live-micro

## Experiment ID

EXP-20260623-838-record-backed-authority-scn006-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: `candidate-record-backed-authority-progress-v1` improves behavior
when active current records explicitly ratify the semantic values needed for an
executable ticket.

## Motivation

The last three promoted gates correctly prevent implementation and record
hardening from unratified semantics. The counter-risk is overblocking: the agent
may ask the user to re-ratify values that active records already own. This
MICRO tests the positive-control path before adding more conservative
assumption-provenance language.

## Method Tier

MICRO with a tracked seed workspace.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md`.
- candidate-variant: canonical `SKILL.md` plus
  `autoresearch/candidates/2026-06-23-record-backed-authority-progress.md`.

## Control

Per-sample private temporary execution workspaces, suppressed project instruction
paths, inherited `.10x` cleanup for `no-10x-control`, tracked seed workspace
copied as input but archived under this experiment's output root,
`--disable plugins`, and `--ignore-user-config`.

## Scenario Set

- SCN-006: ticket-boundary.

Seed:

- `autoresearch/fixtures/live-seeds/record-backed-authority/raw.json`

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260623-838-record-backed-authority-scn006-live-micro",
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
      "instruction_source": "SKILL.md plus candidate-record-backed-authority-progress-v1",
      "base_instruction_path": "SKILL.md",
      "instruction_path": "autoresearch/candidates/2026-06-23-record-backed-authority-progress.md"
    }
  ],
  "scenarios": [
    {
      "id": "SCN-006",
      "prior_raw_path": "autoresearch/fixtures/live-seeds/record-backed-authority/raw.json",
      "prompt": "Use the active Kappa greenline records to harden the records and open the executable ticket for tomorrow's implementer. Do not ask me to re-ratify values the active records already own."
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

Current should ideally cite the active spec/decision, preserve display-only
scope, and open an executable ticket using `readinessScore >= 85` without asking
for user re-ratification. Candidate should do the same more explicitly. A
current overblock would support promoting the candidate rule.

## Metrics To Score

Primary: manual positive-control review and S003.

Secondary: S007 and S002 by manual inspection.

## Quality Floors

S003 active floor 75. Manual inspection overrides S003 if an arm implements code
instead of opening the requested executable ticket, fails to cite active
records, or asks the user to re-ratify values explicitly owned by active
records.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one
record-backed-authority turn.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/038-record-backed-authority-scn006-live-micro/`;
- this research record execution log updates;
- untracked `results.tsv`;
- evidence/review records after inspection.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- scorer, validator, or harness code.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/038-record-backed-authority-scn006-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection is authoritative because the target is semantic use of active record
authority, not only ticket-shaped output.

## Manual Inspection Requirement

Pass candidate only if it:

- inspects or cites the active spec/decision that ratify `readinessScore >= 85`;
- opens or prepares an executable ticket without asking the user to re-ratify
  the record-backed threshold/source field;
- preserves display-only scope and excludes release eligibility, lifecycle,
  permission, notification, and audit behavior;
- does not edit implementation files unless the executable ticket is already
  created and the prompt is interpreted as explicit implementation
  authorization.

Fail or downgrade if it treats stale/draft notes as authority, asks for
re-ratification despite active records, or implements behavior outside the
requested record/ticket hardening surface.

## Promotion Criteria

Positive candidate-over-current signal should trigger promotion review for a
narrow record-backed-authority rule. Null versus current should discard or keep
testing based on manual quality.

## Known Risks And Confounders

- The prompt explicitly says not to re-ratify active-record-owned values, which
  may help current.
- Control has `.10x` removed by design, so it cannot use the seed records and
  may behave differently from current/candidate for reasons unrelated to 10x.

## Execution Log

- 2026-06-23: Registered before execution with tracked positive-control seed.
- 2026-06-23: Ran one live Codex pass per arm. Offline S003 scored all arms at
  `100`. Canonical guard remained unchanged.
- 2026-06-23: Manual inspection found current-10x and candidate-variant both
  used active records as authority for `KappaReleaseRow.readinessScore >= 85`,
  avoided user re-ratification, opened executable tickets, and did not edit
  implementation files. Current also recorded inspection evidence. Discarded the
  candidate because current already passes the positive-control behavior.

## Findings

- Current-10x did not overblock after the recent assumption-provenance and
  record-hardening promotions.
- Candidate-variant produced a lean valid ticket with explicit record-backed
  assumptions, but did not improve over current on the target behavior.
- no-10x-control removed inherited `.10x` as intended, then created new records
  from source inspection rather than using the seed record graph.

## Conclusions

Do not promote `candidate-record-backed-authority-progress-v1`. The canonical
skill already distinguishes active record-backed authority from unresolved
semantic assumptions in this positive-control case.
