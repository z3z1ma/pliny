Status: done
Created: 2026-06-23
Updated: 2026-06-23

# EXP-20260623-850-retrospective-extraction-type-gate-scn012-live-micro

## Experiment ID

EXP-20260623-850-retrospective-extraction-type-gate-scn012-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: `candidate-retrospective-extraction-type-gate-v1` improves closure
retrospectives by routing each durable learning item to the correct record type
instead of satisfying the retrospective with a generic follow-up ticket or final
answer prose.

## Motivation

Recent closure experiments strengthened semantic blockers and follow-up owners.
The next likely failure is a narrower retrospective problem: an agent may open a
single follow-up ticket for unfinished work and still lose reusable procedures,
conventions, or instruction gaps that should become knowledge, skills, or
instruction updates. 10x should compound learning in the form future agents need.

## Method Tier

MICRO using a tracked Ledger import retrospective seed.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md`.
- candidate-variant: canonical `SKILL.md` plus
  `autoresearch/candidates/2026-06-23-retrospective-extraction-type-gate.md`.

## Control

Per-sample private temporary execution workspaces, suppressed project instruction
paths, inherited `.10x` cleanup for `no-10x-control`, tracked seed workspace
copied as input but archived under this experiment's output root,
`--disable plugins`, and `--ignore-user-config`.

## Scenario Set

- SCN-012: retrospective extraction from ready-to-close work with one follow-up
  risk, one reusable test procedure, and one settled naming convention.

Seed:

- `autoresearch/fixtures/live-seeds/retrospective-extraction/raw.json`

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260623-850-retrospective-extraction-type-gate-scn012-live-micro",
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
      "instruction_source": "SKILL.md plus candidate-retrospective-extraction-type-gate-v1",
      "base_instruction_path": "SKILL.md",
      "instruction_path": "autoresearch/candidates/2026-06-23-retrospective-extraction-type-gate.md"
    }
  ],
  "scenarios": [
    {
      "id": "SCN-012",
      "prior_raw_path": "autoresearch/fixtures/live-seeds/retrospective-extraction/raw.json",
      "prompt": "All Ledger import preview acceptance criteria now have recorded evidence and the review is pass. Close the child and parent. During the retrospective, preserve these three items correctly: stable Ledger import tests require tracked CSV fixtures under testdata/ledger/ plus frozen posting date 2026-01-15 after two failed inline fixture/system-date attempts; the settled domain name is sourceRef, not externalId; archive import still lacks malformed-currency coverage and is outside this ticket. Do not edit implementation files."
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

Candidate should open a bounded archive malformed-currency follow-up ticket,
preserve the `sourceRef` naming convention as knowledge, preserve the Ledger
import fixture setup as a skill or equivalent procedure record, then close the
child and parent only if evidence, review, and retrospective obligations are
coherent.

Current may already pass because canonical `SKILL.md` says retrospective
extraction elevates knowledge, distills skills, and opens follow-up tickets.

## Metrics To Score

Primary: manual retrospective type-routing review, S002, and S006.

Secondary: S008 by manual inspection because Trust Level 1 scoring does not yet
distinguish skills from generic tickets.

## Quality Floors

S002 active floor 80 and S006 active floor 80. Manual inspection overrides high
scores if an arm leaves durable learning only in chat or records procedure and
convention lessons as generic follow-up tickets.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one closure
turn.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/050-retrospective-extraction-type-gate-scn012-live-micro/`;
- this research record execution log updates;
- untracked `results.tsv`;
- evidence/review records after inspection.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- scorer, validator, or harness code.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/050-retrospective-extraction-type-gate-scn012-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection is authoritative because the target behavior is typed retrospective
record routing, not generic presence of "retrospective" wording.

## Manual Inspection Requirement

Pass an arm only if it:

- does not edit implementation files;
- maps child acceptance criteria to recorded evidence and preserves review pass;
- opens a bounded follow-up owner for archive malformed-currency coverage, or
  blocks closure because that risk remains unowned;
- records the `sourceRef` naming convention as durable knowledge or an
  equivalent cold-reader record;
- records the Ledger fixture setup as a skill or equivalent operational
  procedure record;
- closes child and parent tickets only after retrospective obligations have
  durable owners.

Fail or downgrade if it leaves any retrospective item only in final prose,
creates only a generic catch-all ticket, or records one-off noise as a bloated
knowledge/skill record.

## Promotion Criteria

Positive candidate-over-current signal should trigger promotion review for a
narrow retrospective extraction type gate. Null versus current should discard.

## Known Risks And Confounders

- The seed explicitly names the expected retrospective items, so current may
  pass by following existing Retrospective Protocol language.
- The Trust Level 1 SCN-012 scorer rewards knowledge and tickets but does not
  currently check for skills or distinguish generic tickets from typed learning.
- The no-10x control has `.10x` removed and cannot preserve the seed record
  graph.

## Execution Log

- 2026-06-23: Registered after discarding the subagent-claim reconciliation
  candidate as null to weaker versus current. This tests whether closure
  retrospectives route procedure, convention, and unfinished-work learning into
  different durable record types.
- 2026-06-23: Ran one live Codex sample for each arm. Automated Trust Level 1
  scores: current-10x `S002=85,S006=85`, candidate-variant
  `S002=70,S006=85`, no-10x-control `S002=85,S006=50`.
- 2026-06-23: Manual inspection found current-10x closed child and parent,
  opened the archive malformed-currency follow-up, and captured both the
  repeatable fixture procedure and `sourceRef` convention in one knowledge
  record. It did not create a skill for the repeatable procedure.
- 2026-06-23: Manual inspection found candidate-variant closed child and parent,
  created `.10x/skills/ledger-import-test-fixtures/SKILL.md`, mirrored it to
  `.claude/skills/ledger-import-test-fixtures/SKILL.md`, created
  `.10x/knowledge/ledger-import-source-reference.md`, and opened
  `.10x/tickets/2026-06-23-add-archive-import-malformed-currency-coverage.md`.
  It did not edit implementation files.
- 2026-06-23: Promoted `candidate-retrospective-extraction-type-gate-v1` into
  `SKILL.md`. Opened a follow-up ticket for the SCN-012 scorer false negative
  on skill records.

## Results

Automated score vectors:

- current-10x: `S002=85`, `S006=85`
- candidate-variant: `S002=70`, `S006=85`
- no-10x-control: `S002=85`, `S006=50`

Manual result:

- no-10x-control: not promotion-relevant. It created a new record graph from the
  prompt and did not preserve the seeded ticket/spec graph.
- current-10x: safe but incomplete. It preserved closure coherence, opened the
  archive coverage follow-up, and recorded the fixture/date convention plus
  `sourceRef` naming in knowledge. It did not route the repeatable operational
  procedure to a skill.
- candidate-variant: pass. It routed the three retrospective observations by
  type: fixture setup procedure to skill, `sourceRef` naming to knowledge, and
  archive malformed-currency gap to a follow-up ticket. It closed only after the
  retrospective obligations had durable owners and did not edit implementation
  files.

## Conclusions

Promote `candidate-retrospective-extraction-type-gate-v1`. The promoted rule
sharpens the existing Retrospective Protocol by requiring classification by
record type before closure and by forbidding generic follow-up tickets as a
substitute for procedure, convention, or instruction-gap learning.

The run also exposes an autoresearch scorer gap: SCN-012 S002 rewards common
headers and knowledge/ticket records but does not model skills, causing a false
negative for the candidate's best behavior.
