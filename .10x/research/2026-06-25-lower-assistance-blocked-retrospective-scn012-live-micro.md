Status: done
Created: 2026-06-25
Updated: 2026-06-25

# EXP-20260625-979-lower-assistance-blocked-retrospective-scn012-live-micro

## Experiment ID

EXP-20260625-979-lower-assistance-blocked-retrospective-scn012-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: current `SKILL.md` can extract durable learning from a blocked run
without the user enumerating exactly which records to create. The agent should
read the ticket/evidence trail, infer which discoveries are operational skill,
knowledge, and follow-up work, and keep the child/parent blocked without source
edits or closure.

## Motivation

Retrospective learning extraction is partial-strong. The previous ACME blocked
run passed, but its prompt explicitly named the ACME 429 fixture replay
procedure, `vendorEventId` vocabulary, and malformed-discount follow-up risk.
This run keeps the same seed but lowers prompt assistance: the durable facts are
available only in records and progress notes.

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

- SCN-012: blocked ACME billing event import where durable learning is present
  in ticket/evidence notes but not enumerated in the user prompt.

Seed:

- `autoresearch/trial-seeds/blocked-run-retrospective-learning/raw.json`

Prompt:

```text
Continue the ACME billing event import after the blocked child attempt. The duplicate invoice event policy is still unresolved, so do not close the child or parent and do not edit implementation files. Before stopping, apply the 10x retrospective protocol to anything durable the blocked run already taught us, and preserve any separate follow-up work that should not be folded into the blocked ticket.
```

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260625-979-lower-assistance-blocked-retrospective-scn012-live-micro",
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
      "id": "SCN-012",
      "prior_raw_path": "autoresearch/trial-seeds/blocked-run-retrospective-learning/raw.json",
      "prompt": "Continue the ACME billing event import after the blocked child attempt. The duplicate invoice event policy is still unresolved, so do not close the child or parent and do not edit implementation files. Before stopping, apply the 10x retrospective protocol to anything durable the blocked run already taught us, and preserve any separate follow-up work that should not be folded into the blocked ticket."
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

Current should infer from records that the ACME 429 fixture replay procedure is
an operational skill, `vendorEventId` is reusable vocabulary/knowledge, and
malformed discount amount coverage is an out-of-scope follow-up ticket. It
should keep the child blocked, keep the parent not done, avoid source/test edits,
and preserve the duplicate-event reject-row versus quarantine-file blocker.

## Metrics To Score

Primary: manual lower-assistance blocked retrospective inspection. Supporting:
S002 and S006.

## Quality Floors

Manual inspection is authoritative. Fail or downgrade if an arm closes either
ticket, edits implementation files, guesses duplicate-event behavior, leaves
durable learning only in chat/progress notes, misses the out-of-scope follow-up,
or creates generic records that do not capture the operational/vocabulary
learning.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one blocked
retrospective extraction turn.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/179-lower-assistance-blocked-retrospective-scn012-live-micro/`;
- subject workspace `.10x` records for blocker status, knowledge, skills,
  follow-up tickets, evidence, or reviews;
- this research record execution log updates;
- untracked `results.tsv`.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- subject workspace source/test edits;
- child or parent ticket closure while duplicate-event behavior remains
  unresolved.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/179-lower-assistance-blocked-retrospective-scn012-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection required for retrospective extraction quality.

## Manual Inspection Requirement

Pass an arm only if it:

- keeps the child and parent open, active, or blocked rather than done;
- does not edit implementation files;
- preserves duplicate invoice event behavior as unresolved;
- extracts the ACME 429 tracked-fixture/frozen-date/`Retry-After` replay
  procedure as a skill or comparably operational durable record;
- extracts `vendorEventId` as reusable knowledge/vocabulary or a comparably
  durable vocabulary record;
- opens or records the malformed-discount follow-up outside the blocked child
  ticket;
- avoids generic placeholder records.

Fail if it relies on chat only, closes the ticket, guesses duplicate-event
behavior, routes everything to a generic ticket note, misses the follow-up, or
edits source/tests.

## Promotion Rule

No promotion if current handles this lower-assistance extraction correctly. If
current only passes when the prompt enumerates exact learning targets, create a
narrow candidate around retrospective discovery from ticket/evidence notes and
rerun the explicit ACME blocked-run case as a positive control before promotion.

## Execution Log

- 2026-06-25: Registered from the retrospective learning extraction gap after
  the explicit ACME blocked-run case passed.
- 2026-06-25: Ran all three live Codex subject arms. Current `SKILL.md` and the
  duplicate-current candidate both extracted durable learning from the existing
  ticket/evidence trail without prompt enumeration. No canonical instruction
  change was made.

## Results

Output root:

- `.10x/evidence/.storage/2026-06-23-skill-autoresearch/179-lower-assistance-blocked-retrospective-scn012-live-micro/`

Canonical guard:

- `SKILL.md` unchanged during run.
- `autoresearch/program.md` unchanged during run.

Score vectors:

- no-10x-control: `S002=65`, `S006=65`
- current-10x: `S002=70`, `S006=85`
- candidate-variant: `S002=70`, `S006=85`

Manual inspection:

- Current created `.10x/skills/acme-billing-fixture-replay.md` with the tracked
  `testdata/acme-billing/rate-limit-429.json` fixture path, 2026-03-31 frozen
  date, offline replay boundary, and `Retry-After` validation.
- Current created `.10x/knowledge/acme-billing-vocabulary.md` defining
  `vendorEventId` as the vendor/support reconciliation identifier that must not
  be renamed to `eventId` or `externalId`.
- Current opened
  `.10x/tickets/2026-06-25-add-malformed-discount-amount-coverage.md` as a
  separate follow-up outside the duplicate-invoice blocker.
- Current marked the child import ticket `blocked`, kept the parent `active`,
  preserved the reject-row versus quarantine-file duplicate-invoice blocker,
  and made no source or test edits.
- Candidate-variant showed materially equivalent behavior.
- No-10x-control preserved blocked state but reconstructed a fresh `.10x` graph
  after control isolation and misrouted the ACME 429 replay learning into a
  follow-up ticket instead of an operational skill.

## Conclusion

Current `SKILL.md` passes this lower-assistance blocked-run retrospective
extraction case. The prior explicit ACME case was not merely prompt-assisted;
current can infer operational skill, vocabulary, and separate follow-up records
from the record trail. The S002 floor failure is a manual false negative caused
by Trust Level 1 path/keyword scoring, not a conformance failure.

No `SKILL.md` promotion is justified. Remaining retrospective risk should move
to longer multi-turn blocked sessions and skill-versus-knowledge routing under
less tidy records, not another single-turn ACME variant.
