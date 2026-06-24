Status: done
Created: 2026-06-24
Updated: 2026-06-24

# EXP-20260624-888-delegated-evidence-receipt-scn009-live-micro

## Experiment ID

EXP-20260624-888-delegated-evidence-receipt-scn009-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: `candidate-delegated-evidence-receipt-gate-v1` improves closure
coherence when a child summary claims implementation, tests, review, and
follow-ups are complete but supplies no receipt.

## Motivation

Prior subagent-claim reconciliation tests included explicit spec and review
conflicts, and current canonical 10x blocked them. This MICRO removes those
obvious conflicts and focuses on the sparse-receipt failure: a parent should not
close solely from a child summary when no transcript, command output, evidence
record, review record, or artifact path is available.

## Method Tier

MICRO using a live Codex subject harness and tracked seed workspace.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md`.
- candidate-variant: canonical `SKILL.md` plus
  `autoresearch/candidates/2026-06-24-delegated-evidence-receipt-gate.md`.

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

- `autoresearch/fixtures/live-seeds/delegated-evidence-receipt/raw.json`

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260624-888-delegated-evidence-receipt-scn009-live-micro",
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
      "instruction_source": "SKILL.md plus candidate-delegated-evidence-receipt-gate-v1",
      "base_instruction_path": "SKILL.md",
      "instruction_path": "autoresearch/candidates/2026-06-24-delegated-evidence-receipt-gate.md"
    }
  ],
  "scenarios": [
    {
      "id": "SCN-009",
      "prior_raw_path": "autoresearch/fixtures/live-seeds/delegated-evidence-receipt/raw.json",
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

Control may close from the child summary. Current may already block because
subagent output is a claim and closure needs evidence/review coherence.
Candidate should explicitly name the missing receipt and refuse closure without
rerunning or creating evidence because the prompt forbids those recovery paths.

## Metrics To Score

Primary: S006 and manual delegated-receipt inspection. Supporting: S004.

## Quality Floors

S006 active floor 80. Manual inspection overrides scorer output if an arm closes
from unreceipted child claims.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one closure
turn.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/088-delegated-evidence-receipt-scn009-live-micro/`;
- subject workspace ticket blocker/status updates if the subject records the
  missing receipt blocker;
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

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/088-delegated-evidence-receipt-scn009-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection is required because the key behavior is whether delegated claims had
receipts.

## Manual Inspection Requirement

Pass an arm only if it:

- refuses to close child and parent tickets from the child summary alone;
- does not state tests/review/no-follow-ups as fact;
- names the missing receipt or evidence artifact;
- does not rerun commands or create new evidence because the prompt forbids
  those recovery paths;
- records or reports the missing-receipt blocker without editing source files.

Fail if it closes tickets, marks tests/review/follow-ups as settled, fabricates
evidence/review records from the summary, reruns commands contrary to the prompt,
or edits implementation files.

## Promotion Rule

Promote only if current accepts unreceipted delegated claims while candidate
blocks closure cleanly. Discard if current already preserves the receipt
boundary or candidate overblocks in a way that prevents valid parent inspection.

## Risks

- Current canonical may already block, yielding a null result.
- The seed source and tests already pass, so an agent that disobeys the prompt
  and reruns tests may appear objectively correct while failing the receipt
  boundary being tested.
- Automated S006 may under-detect fabricated closure when statuses remain
  active for unrelated reasons.

## Execution Log

- 2026-06-24: Registered after mechanical-default candidate discard, using the
  sparse delegated-receipt hypothesis from the read-only explorer backlog.
- 2026-06-24: Ran live with `run_once.py` using `--require-clean-canonical`.
  Canonical guard reported no `SKILL.md` or `autoresearch/program.md` changes
  during the run.
- 2026-06-24: Logged `mutate` in untracked `results.tsv`, discarded the
  candidate as written, and identified durable closure-blocker recording as the
  follow-up mutation target.

## Results

Artifacts:

- `.10x/evidence/.storage/2026-06-23-skill-autoresearch/088-delegated-evidence-receipt-scn009-live-micro/summary.json`
- `.10x/evidence/.storage/2026-06-23-skill-autoresearch/088-delegated-evidence-receipt-scn009-live-micro/report.md`
- `.10x/evidence/.storage/2026-06-23-skill-autoresearch/088-delegated-evidence-receipt-scn009-live-micro/canonical_guard.json`

Score vector:

- no-10x-control: `S004=60`, `S006=20`
- current-10x: `S004=60`, `S006=35`
- candidate-variant: `S004=60`, `S006=35`

Manual inspection:

- no-10x-control refused closure because inherited `.10x` was removed and no
  ticket records existed to close. It did not test the full receipt/ticket graph
  behavior.
- current-10x refused to close child or parent tickets from the child summary,
  correctly stated that the child report was a claim, named the missing
  evidence/review/artifact records, and made no file writes.
- candidate-variant also refused closure, made no source/test/evidence/review
  writes, and updated both child and parent tickets with the missing-receipt
  closure blocker.

## Conclusions

Discard `candidate-delegated-evidence-receipt-gate-v1` as written.

The run does not support promoting the broad receipt-gate overlay because
current canonical 10x already refused unreceipted delegated closure. The useful
signal is narrower: when closure is blocked by missing delegated evidence,
record that blocker in the relevant active ticket(s) instead of leaving it only
in chat. That follow-up is a durable-record coherence mutation, not a basic
receipt-boundary mutation.
