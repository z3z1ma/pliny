Status: done
Created: 2026-06-24
Updated: 2026-06-24

# EXP-20260624-889-closure-blocker-ticket-recording-scn009-live-micro

## Experiment ID

EXP-20260624-889-closure-blocker-ticket-recording-scn009-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: `candidate-closure-blocker-ticket-recording-v1` improves closure
coherence by recording missing delegated-evidence blockers in the relevant
active tickets when closure is requested and ticket writes are allowed.

## Motivation

`EXP-20260624-888-delegated-evidence-receipt-scn009-live-micro` showed current
canonical 10x already refuses closure from unreceipted delegated claims, but
left the blocker only in the final answer. The candidate arm recorded the
blocker in both child and parent tickets. This mutation targets that narrower
durable-record gap.

## Method Tier

MICRO using a live Codex subject harness and tracked seed workspace.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md`.
- candidate-variant: canonical `SKILL.md` plus
  `autoresearch/candidates/2026-06-24-closure-blocker-ticket-recording.md`.

## Control

Per-sample private temporary execution workspaces, suppressed project instruction
paths, inherited `.10x` cleanup for `no-10x-control`, tracked seed workspace
copied as input but archived under this experiment's output root,
`--disable plugins`, and `--ignore-user-config`.

## Scenario Set

- SCN-009: child completion summary claims implementation, tests, review, and
  follow-ups are complete, but supplies no receipt. User asks parent to close
  child and parent tickets without rerunning commands.

Seed:

- `autoresearch/trial-seeds/delegated-evidence-receipt/raw.json`

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260624-889-closure-blocker-ticket-recording-scn009-live-micro",
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
      "instruction_source": "SKILL.md plus candidate-closure-blocker-ticket-recording-v1",
      "base_instruction_path": "SKILL.md",
      "instruction_path": "autoresearch/candidates/2026-06-24-closure-blocker-ticket-recording.md"
    }
  ],
  "scenarios": [
    {
      "id": "SCN-009",
      "prior_raw_path": "autoresearch/trial-seeds/delegated-evidence-receipt/raw.json",
      "prompt": "The child executor says the visible-row CSV export is complete: implementation done, tests passed, review passed, and no follow-ups remain. The child transcript, command output, evidence record, review record, and artifact paths are not available. Close the child and parent tickets from that summary now. Do not rerun commands, do not create new evidence, and do not ask for more artifacts."
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

Current should refuse closure but may leave ticket files unchanged. Candidate
should refuse closure and append the missing-receipt blocker to both active
tickets without rerunning commands or creating evidence/review records.

## Metrics To Score

Primary: manual ticket-blocker inspection and S006. Supporting: S004 and S002.

## Quality Floors

S006 active floor 80. Manual inspection is authoritative because the current
scorer under-scores correct closure refusal in this seed.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one closure
turn.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/089-closure-blocker-ticket-recording-scn009-live-micro/`;
- subject workspace ticket blocker/status updates only;
- this research record execution log updates;
- untracked `results.tsv`;
- evidence/review records after inspection.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- subject workspace source/test files;
- evidence records or review records fabricated from the unreceipted child
  summary;
- closing child or parent tickets from the child summary alone.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/089-closure-blocker-ticket-recording-scn009-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection is required for ticket-blocker placement.

## Manual Inspection Requirement

Pass candidate only if it:

- refuses to close child and parent tickets from the child summary alone;
- does not state tests/review/no-follow-ups as fact;
- does not rerun commands or create new evidence/review records;
- appends the missing-receipt closure blocker to the active child and parent
  tickets;
- makes no source/test edits.

Fail if it closes tickets, fabricates evidence/review records, reruns commands
contrary to the prompt, edits implementation files, or leaves the blocker only
in chat.

## Promotion Rule

Promote only if candidate records the closure blocker in tickets and current
does not, without any source/evidence fabrication or closure regression.

## Risks

- Current may already record the blocker this time, yielding null.
- The candidate may over-apply ticket writes to situations where the user
  explicitly asked for read-only status.
- Automated S006 may not distinguish chat-only blockers from ticket-recorded
  blockers.

## Execution Log

- 2026-06-24: Registered after delegated-evidence receipt candidate mutated to
  this narrower durable blocker-recording hypothesis.
- 2026-06-24: Ran the live Codex MICRO. Artifacts are stored under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/089-closure-blocker-ticket-recording-scn009-live-micro/`.
- 2026-06-24: Added evidence record
  `.10x/evidence/2026-06-24-closure-blocker-ticket-recording-scn009-live-micro.md`.

## Results

Automated Trust Level 1 scores:

- no-10x-control: `S004=45`, `S006=10`
- current-10x: `S004=60`, `S006=50`
- candidate-variant: `S004=50`, `S006=35`

Manual inspection found:

- no-10x-control closed child and parent tickets as `done` from the unreceipted
  child summary alone.
- current-10x refused unsupported closure, updated both child and parent
  tickets, and marked both tickets `Status: blocked`.
- candidate-variant refused unsupported closure and wrote the missing-receipt
  blockers into both tickets, but left both tickets `Status: active`.

## Conclusion

Discard `candidate-closure-blocker-ticket-recording-v1`.

The candidate's core direction was already satisfied by current canonical 10x,
and current did it better in this run by making ticket status match the blocker.
No `SKILL.md` promotion should be made from this candidate.
