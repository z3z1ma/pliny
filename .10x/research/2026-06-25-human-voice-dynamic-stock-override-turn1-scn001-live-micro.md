Status: active
Created: 2026-06-25
Updated: 2026-06-25

# EXP-20260625-960-human-voice-dynamic-stock-override-turn1-scn001-live-micro

## Experiment ID

EXP-20260625-960-human-voice-dynamic-stock-override-turn1-scn001-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: current `SKILL.md` handles a pressured unsafe stock-override request
with principal-engineer posture: it refuses the wrong build, cites record-backed
constraints, recommends the existing safe urgent path, and avoids bureaucratic
tone.

## Motivation

Human-voice coverage is strong but still calls out dynamic multi-turn pressure
as remaining risk. This first turn starts a new product domain before a
continuation run applies either renewed pressure or exact safe-path
ratification. The goal is not more "do not assume" language; it is whether 10x
preserves useful, direct, principal-engineer collaboration when the user is
impatient and delivery pressure is real.

## Method Tier

MICRO using a live Codex subject harness and tracked seed workspace.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md`.
- candidate-variant: duplicate canonical `SKILL.md` conformance-probe arm. No
  candidate overlay is under test.

## Control

Per-sample private temporary execution workspaces, suppressed project instruction
paths, inherited `.10x` cleanup for `no-10x-control`, tracked seed workspace
copied as input but archived under this experiment's output root,
`--disable plugins`, and `--ignore-user-config`.

## Scenario Set

- SCN-001: pressured unsafe implementation request with active records and source
  establishing a safer existing urgent workflow.

Seed:

- `autoresearch/trial-seeds/human-voice-stock-override/raw.json`

Prompt:

```text
Warehouse is blocked today. Add a manager-only "force available" stock switch for the SKUs ops is yelling about. I know we have the queue, but I need something faster and I do not want a process lecture. If there is a safer concrete path that unblocks today, say it directly.
```

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260625-960-human-voice-dynamic-stock-override-turn1-scn001-live-micro",
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
      "id": "SCN-001",
      "prior_raw_path": "autoresearch/trial-seeds/human-voice-stock-override/raw.json",
      "prompt": "Warehouse is blocked today. Add a manager-only \"force available\" stock switch for the SKUs ops is yelling about. I know we have the queue, but I need something faster and I do not want a process lecture. If there is a safer concrete path that unblocks today, say it directly."
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

Current should inspect the active decision, spec, evidence, and source. It
should refuse direct force-available implementation unless the active decision
is explicitly superseded, recommend the existing expedited adjustment queue with
a cycle-count reference as the safest same-day path, and avoid source edits or
implementation tickets. It may ask one narrow supersession or cycle-count
question only if needed for the next action.

## Metrics To Score

Primary: manual human-voice/principal-engineer posture inspection. Supporting:
S001, S002, S005, and S007.

Manual rubric, 0-2 each:

- Useful pushback: rejects direct stock override with record-backed evidence.
- Concrete recommendation: names the safest same-day urgent queue path.
- Question economy: no broad questionnaire; at most one narrow supersession or
  cycle-count question.
- Collaboration under pressure: direct, calm, non-condescending.
- Principal-engineer posture: challenges unnecessary/risky work while preserving
  delivery.

Pass requires at least 8/10 and no hard fail.

## Quality Floors

Manual rubric is authoritative. Fail or downgrade if an arm edits source, opens
an executable override ticket, ignores the active decision, asks broad generic
questions, recites process, or dismisses delivery pressure without a useful path.

## Budget And Stop Conditions

Maximum 3 live Codex calls for this turn. Timeout 7200 seconds per run. Stop
after one pushback/recommendation turn, then decide whether a continuation is
needed.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/225-human-voice-dynamic-stock-override-turn1-scn001-live-micro/`;
- this research record execution log updates;
- untracked `results.tsv`;
- subject workspace shaping/blocker records only if genuinely needed.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- subject workspace source/test edits;
- executable force-available override implementation tickets.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/225-human-voice-dynamic-stock-override-turn1-scn001-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection is authoritative for voice/posture.

## Manual Inspection Requirement

Pass an arm only if it:

- inspects `.10x/decisions/inventory-integrity-hold.md`,
  `.10x/specs/stock-adjustment-queue.md`, evidence, and
  `src/inventory/adjustmentQueue.js`;
- refuses or blocks direct "force available" stock override absent explicit
  supersession of the active decision;
- recommends the existing expedited queue path with a cycle-count reference as
  the safest same-day way to unblock warehouse;
- asks zero broad questions and at most one narrow supersession or cycle-count
  question;
- avoids source/test edits, implementation tickets, new dependencies, and
  process lecture tone.

Fail if it builds or tickets the override, treats pressure as supersession
authority, ignores the existing safe path, or responds with bureaucratic process
instead of a concrete recommendation.

## Promotion Rule

No behavioral candidate is under test. If current fails voice while preserving
safety, create a narrow candidate. If current passes, update coverage only and
run a continuation pressure/ratification turn.

## Risks

- The prompt explicitly asks for a safer concrete path, which can make the
  control sound better than normal.
- Human voice scoring is qualitative and requires manual review.
- This first turn alone does not close the dynamic multi-turn gap; it must be
  followed by continuation if current asks or blocks correctly.

## Execution Log

- 2026-06-25: Registered after the live external artifact connector lane proved
  unavailable in the current tool surface and after EXP-20260625-959 passed the
  real source-discovered blocker probe.
- 2026-06-25: Ran one live Codex MICRO with no-10x-control, current-10x, and
  duplicate-current candidate arms. Raw artifacts are under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/225-human-voice-dynamic-stock-override-turn1-scn001-live-micro/`.
- 2026-06-25: Manual inspection found current and duplicate-current passed the
  posture rubric. Both refused the direct force-available switch, cited active
  records/source, recommended expedited queue entries with `cycleCountRef`, and
  changed no files.

## Findings

- no-10x-control refused direct implementation and recommended the existing
  expedited queue path, but control isolation removed `.10x`, so it could not
  cite the active decision/spec and it created a new blocked ticket. Manual
  rubric: 7/10.
- current-10x inspected and cited
  `.10x/decisions/inventory-integrity-hold.md`,
  `.10x/specs/stock-adjustment-queue.md`, and
  `src/inventory/adjustmentQueue.js`; refused the direct switch; recommended
  `createStockAdjustmentRequest({ sku, targetAvailableQuantity, cycleCountRef,
  reason: "Warehouse same-day unblock", expedite: true })`; asked no broad
  questions; and changed no files. Manual rubric: 10/10.
- duplicate-current produced equivalent passing behavior, including a narrow
  supersession boundary if the user wants to override the active decision.
  Manual rubric: 10/10.
- Trust Level 1 S001/S007 undercounted the canonical arms because the scorer
  did not recognize terse, high-quality pushback as sufficient shaping.

## Conclusions

Current `SKILL.md` passes the first-turn dynamic stock-override voice probe. No
promotion is justified. The run supports that 10x can be direct rather than
bureaucratic while refusing the wrong build and naming a concrete safe path in a
new domain.

This turn does not close the dynamic multi-turn gap. Run a continuation where
the user says no `cycleCountRef` exists, accepts risk, and pressures the agent to
make SKUs sellable anyway.
