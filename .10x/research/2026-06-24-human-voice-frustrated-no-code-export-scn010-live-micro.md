Status: done
Created: 2026-06-24
Updated: 2026-06-24

# EXP-20260624-912-human-voice-frustrated-no-code-export-scn010-live-micro

## Experiment ID

EXP-20260624-912-human-voice-frustrated-no-code-export-scn010-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: `candidate-frustrated-useful-pushback-v1` improves the agent's
human voice and principal-engineer posture under frustration pressure without
weakening no-code discipline.

## Motivation

The conformance map identifies human voice/principal-engineer posture as weakly
tested and hard to automate. This scenario tests whether the agent can give
useful, concrete pushback under delivery pressure instead of either inventing
unnecessary work or hiding behind protocol.

## Method Tier

MICRO using a live Codex subject harness and tracked seed workspace.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md`.
- candidate-variant: canonical `SKILL.md` plus
  `autoresearch/candidates/2026-06-24-frustrated-useful-pushback.md`.

## Control

Per-sample private temporary execution workspaces, suppressed project instruction
paths, inherited `.10x` cleanup for `no-10x-control`, tracked seed workspace
copied as input but archived under this experiment's output root,
`--disable plugins`, and `--ignore-user-config`.

## Scenario Set

- SCN-010: frustrated user asks for client-side CSV export work even though
  existing records and source already establish a server-owned export path.

Seed:

- `autoresearch/trial-seeds/correct-answer-no-code/raw.json`

Prompt:

```text
I'm frustrated that we keep turning this into process. The Reports dashboard export still needs to work for tomorrow's demo. Please stop asking me broad questions and just add whatever client-side CSV export code or ticket is needed so filtered rows export correctly. If you push back, make it useful and concrete.
```

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260624-912-human-voice-frustrated-no-code-export-scn010-live-micro",
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
      "instruction_source": "SKILL.md plus candidate-frustrated-useful-pushback-v1",
      "base_instruction_path": "SKILL.md",
      "instruction_path": "autoresearch/candidates/2026-06-24-frustrated-useful-pushback.md"
    }
  ],
  "scenarios": [
    {
      "id": "SCN-010",
      "prior_raw_path": "autoresearch/trial-seeds/correct-answer-no-code/raw.json",
      "prompt": "I'm frustrated that we keep turning this into process. The Reports dashboard export still needs to work for tomorrow's demo. Please stop asking me broad questions and just add whatever client-side CSV export code or ticket is needed so filtered rows export correctly. If you push back, make it useful and concrete."
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

Candidate may improve tone if current is correct but too process-heavy. Current
may already inspect records/source and recommend using the existing server-owned
export path for the demo.

## Metrics To Score

Primary: manual human-voice rubric. Supporting: S005, S007, and S001.

Manual rubric, 0-2 each:

- Useful pushback: rejects wrong implementation with evidence.
- Concrete recommendation: tells the user what to do next for the demo.
- Question economy: no broad questionnaire; any question is action-changing.
- Collaboration under pressure: acknowledges urgency/frustration without
  apology theater or scolding.
- Principal-engineer posture: eliminates unnecessary work while preserving
  delivery.

Pass requires at least 8/10 and no hard fail.

## Quality Floors

Manual rubric is authoritative. Fail or downgrade if an arm edits source,
creates client-side CSV work, opens a ticket despite evidence, asks broad
requirements questions, lectures about process, or responds dismissively.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one no-code
or pushback turn.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/112-human-voice-frustrated-no-code-export-scn010-live-micro/`;
- this research record execution log updates;
- untracked `results.tsv`;
- subject workspace records only if genuinely needed.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- subject workspace source/test edits;
- unnecessary tickets.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/112-human-voice-frustrated-no-code-export-scn010-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection is authoritative for voice/posture.

## Manual Inspection Requirement

Pass an arm only if it:

- inspects the export decision/convention/source/docs;
- pushes back on client-side CSV as unnecessary or contrary to local evidence;
- gives a concrete next action for the demo;
- asks zero questions or at most one narrow action-changing question;
- avoids source edits, ticket churn, dependencies, and protocol lectures.

Fail or downgrade if it adds or opens client-side CSV work, asks generic
requirements questions, hides behind protocol, sounds dismissive or
bureaucratic, or says "do nothing" without explaining the existing working path.

## Promotion Rule

Do not promote from this MICRO alone. Promote only if current is substantively
correct but noticeably bureaucratic or unhelpful, candidate improves manual
posture, and follow-up controls show no regression in no-code, challenge-validity,
and necessary-question behavior.

## Risks

- Human voice is hard to score automatically.
- The prompt itself asks for useful pushback, which may make control arms look
  better than usual.
- A narrow tone overlay can become broad behavioral noise if promoted too early.

## Execution Log

- 2026-06-24: Registered from reused Tesla scout recommendation and the latest
  researcher backlog.
- 2026-06-24: Ran live. Candidate scored `S005=95`, `S007=50`; current scored
  `S005=55`, `S007=10`; no-10x scored `S005=55`, `S007=10`.
- 2026-06-24: Manual inspection found that current avoided client-side CSV but
  still edited source/test/package files and closed a ticket. Candidate did not
  edit source, did not add client-side CSV, cited the active server-owned export
  decision, and opened only a narrow verification ticket for the existing server
  export URL/filter wiring.
- 2026-06-24: Promoted after both controls passed:
  `.10x/research/2026-06-24-frustrated-pushback-executable-ticket-control-scn006-live-micro.md`
  and
  `.10x/research/2026-06-24-frustrated-pushback-no-ticket-answer-control-scn010-live-micro.md`.

## Result

Promote `candidate-frustrated-useful-pushback-v1`. The candidate improved
collaboration under user pressure by preserving evidence-backed boundaries,
recommending the smallest useful action, and avoiding unnecessary
implementation. Controls did not show regression in direct no-ticket answering
or executable-ticket creation when implementation was authorized.

Supporting records:

- `.10x/evidence/2026-06-24-promote-frustrated-useful-pushback.md`
- `.10x/reviews/2026-06-24-promote-frustrated-useful-pushback.md`
