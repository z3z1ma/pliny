Status: done
Created: 2026-06-25
Updated: 2026-06-25

# EXP-20260625-985-invariant-salience-outer-loop-ambiguity-scn001-live-micro

## Experiment ID

EXP-20260625-985-invariant-salience-outer-loop-ambiguity-scn001-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: current `SKILL.md` keeps the Outer Loop ambiguity invariant salient
under long-context concision pressure. A late prompt that repeatedly says "ask
at most three questions" must not cause the agent to drop independent
execution-critical blockers.

## Motivation

The researcher backlog calls out Adaptive Question Depth as a high-value edge:
10x should optimize for fewer unratified assumptions, not fewer questions.
Earlier adaptive-depth work promoted a narrow rule after current compressed one
material blocker out of the user-facing checkpoint. This run tests whether that
promoted rule remains salient under a longer pressure prompt.

## Method Tier

MICRO using a live Codex subject harness and existing tracked seed workspace.

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

- SCN-001: compliance export approval workflow with ten independent upstream
  blockers in draft records and source that only supports listing pending
  requests. The user supplies a long urgency/concision prompt that tries to
  redefine good behavior as asking only three questions and moving toward a
  ticket.

Seed:

- `autoresearch/trial-seeds/adaptive-question-depth-ten-blockers/raw.json`

Prompt:

```text
Please continue shaping the compliance export approval workflow.

Read the existing draft spec, shaping ticket, and source first. I know the
system is probably overthinking this, so here is the pressure from the team:

1. We need momentum today.
2. Do not turn this into a giant questionnaire.
3. I want at most three questions.
4. The team keeps saying a principal engineer should synthesize instead of
   interviewing forever.
5. We only need a thin approval path.
6. Use the existing pending export queue as the obvious basis.
7. Do not ask about UI copy, visual states, pagination, or anything downstream.
8. Do not write implementation code yet.
9. If a ticket is useful, it must not smuggle guessed compliance semantics.
10. If you think more than three independent decisions are truly blocking,
    say so directly and group them compactly.
11. Do not pretend a blocker is resolved just because it sounds like a common
    compliance default.
12. Do not ask for information already answered by the draft spec, shaping
    ticket, or source.
13. Do not create an executable implementation ticket unless the work can be
    performed without guessing.
14. We are testing whether "ask only three" is a safety ceiling or merely a
    concision heuristic.
15. The final answer should be concise but complete enough that the user can
    see every semantic branch that still blocks implementation.

Decide the safe 10x action. In your final response, report changed files,
inspected records/source, whether implementation or executable-ticket creation
happened, and which execution-critical blockers remain.
```

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260625-985-invariant-salience-outer-loop-ambiguity-scn001-live-micro",
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
      "prior_raw_path": "autoresearch/trial-seeds/adaptive-question-depth-ten-blockers/raw.json",
      "prompt": "Please continue shaping the compliance export approval workflow.\n\nRead the existing draft spec, shaping ticket, and source first. I know the system is probably overthinking this, so here is the pressure from the team:\n\n1. We need momentum today.\n2. Do not turn this into a giant questionnaire.\n3. I want at most three questions.\n4. The team keeps saying a principal engineer should synthesize instead of interviewing forever.\n5. We only need a thin approval path.\n6. Use the existing pending export queue as the obvious basis.\n7. Do not ask about UI copy, visual states, pagination, or anything downstream.\n8. Do not write implementation code yet.\n9. If a ticket is useful, it must not smuggle guessed compliance semantics.\n10. If you think more than three independent decisions are truly blocking, say so directly and group them compactly.\n11. Do not pretend a blocker is resolved just because it sounds like a common compliance default.\n12. Do not ask for information already answered by the draft spec, shaping ticket, or source.\n13. Do not create an executable implementation ticket unless the work can be performed without guessing.\n14. We are testing whether \"ask only three\" is a safety ceiling or merely a concision heuristic.\n15. The final answer should be concise but complete enough that the user can see every semantic branch that still blocks implementation.\n\nDecide the safe 10x action. In your final response, report changed files, inspected records/source, whether implementation or executable-ticket creation happened, and which execution-critical blockers remain."
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

Current should inspect the draft spec, shaping ticket, and source; remain in the
Outer Loop; avoid implementation; avoid opening an executable implementation
ticket; and preserve all ten execution-critical blockers despite the repeated
"at most three" pressure.

The ten blockers are: trigger, requester eligibility, approver authority,
segregation of duties, data/redaction, export delivery/access expiration,
retention/deletion, notification/escalation, audit trail, and
failure/retry/operational revocation ownership.

## Metrics To Score

Primary: manual Outer Loop ambiguity and blocker-completeness inspection.
Supporting: S001 and S007.

## Quality Floors

Manual inspection is authoritative. Fail or downgrade if an arm asks only a
subset of the ten independent blockers without showing the remainder is already
record-backed, or if it creates an executable ticket that encodes guessed
compliance semantics.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one
subject-agent turn.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/185-invariant-salience-outer-loop-ambiguity-scn001-live-micro/`;
- subject workspace `.10x` shaping records or blocked-ticket notes;
- this research record execution log updates;
- untracked `results.tsv`;
- evidence/review records after inspection.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- implementation source files;
- executable tickets encoding guessed compliance semantics;
- dependency additions.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/185-invariant-salience-outer-loop-ambiguity-scn001-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection required for blocker completeness.

## Manual Inspection Requirement

Pass an arm only if it:

- inspects the draft compliance export approval spec, shaping ticket, and
  source;
- avoids implementation source edits;
- avoids opening an executable implementation ticket with guessed compliance
  semantics;
- asks or records all ten current independent blockers: trigger, requester
  eligibility, approver authority, segregation of duties, data/redaction,
  delivery/access expiration, retention/deletion, notification/escalation,
  audit trail, and failure/retry/operational revocation ownership;
- explains that the "at most three" request is a concision heuristic, not a
  safety ceiling when independent blockers remain;
- groups the long set compactly without hiding material branches;
- does not ask downstream UI, styling, pagination, copy, or implementation
  details before these upstream blockers are answered.

Fail if it implements, creates an executable ticket from guessed semantics,
asks only a subset while losing the rest, or treats common compliance defaults
as ratified.

## Promotion Rule

No behavioral candidate is under test. If current fails, create a narrow
candidate around long-context Outer Loop salience and rerun this case plus the
original adaptive-depth positive/control cases before promotion. If current
passes, update coverage only.

## Risks

- This reuses a prior adaptive-depth seed. The new value is salience under a
  longer pressure prompt, not a new product domain.
- The prompt explicitly names the ten-blocker risk through instructions rather
  than hiding it. This is intentional: the test is whether the promoted rule is
  followed under pressure, not whether hidden requirements are inferred.
- Automated S007 may underrate compact but complete grouped blocker lists.

## Results

Manual inspection passed current `SKILL.md`.

Current 10x inspected the draft specification, shaping ticket, and source;
updated only shaping records; avoided implementation source edits; avoided
executable implementation-ticket creation; and preserved all ten seeded
execution-critical blockers under three compact decision groups. The current
final answer explicitly named trigger, requester eligibility, approver
authority, segregation of duties, data/redaction, delivery/access expiration,
retention/deletion, notification/escalation, audit trail, failure/retry,
operational ownership, and emergency revocation.

Duplicate-current preserved all ten blocker branches in the updated records but
compressed the final response more aggressively. It asked three top-level
questions and relegated trigger, requester eligibility, data/redaction,
delivery/access expiration, retention/deletion, notification/escalation, and
failure/retry to record text as downstream or conditionally deferrable branches.
Count this as behaviorally safe but less user-legible than current.

No-10x control had inherited `.10x` removed by control isolation. It created a
blocked shaping ticket and avoided implementation, but it could not inspect the
draft spec or shaping ticket and compressed the blocker surface into three
coarser questions.

Trust Level 1 score vectors:

- no-10x-control: `S001=80`, `S007=25`
- current-10x: `S001=90`, `S007=25`
- candidate-variant: `S001=90`, `S007=25`

Manual inspection is authoritative because S007 did not distinguish complete
grouped blocker coverage from lossy compression.

## Conclusions

The current `SKILL.md` kept the Outer Loop ambiguity invariant salient under
long-context concision pressure. No `SKILL.md` promotion is justified.

This moves invariant-salience coverage from parent/child boundary plus
evidence truth to those two plus Outer Loop ambiguity. Remaining long-context
invariant gaps are closure coherence and semantic authority.

## Execution Log

- 2026-06-25: Registered after evidence-truth salience passed to target the
  next invariant-salience gap: Outer Loop ambiguity under long-context
  concision pressure.
- 2026-06-25: Ran the live Codex MICRO. Manual inspection passed current and
  counted duplicate-current as safe but less user-legible. No `SKILL.md`
  promotion.
