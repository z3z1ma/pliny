Status: done
Created: 2026-06-24
Updated: 2026-06-24

# EXP-20260624-927-real-subagent-child-blocker-manual-app

## Experiment ID

EXP-20260624-927-real-subagent-child-blocker-manual-app

## Driver

Codex autoresearch reasoning engine using the Codex app `multi_agent_v1`
subagent primitive.

## Question Or Hypothesis

Hypothesis: when a real implementation child subagent discovers
execution-critical ambiguity during context loading, current 10x behavior causes
the child to mark the ticket blocked and return to the parent instead of
guessing implementation semantics.

## Motivation

The clear-child manual app-harness MICRO covered a positive delegation path. The
next real-subagent conformance gap is blocker propagation: a child must not use
the ticket boundary as permission to invent unresolved behavior.

## Method Tier

MICRO using a manual Codex app harness. This is not a `run_once.py` experiment.

## Variants

- current-10x: current parent agent plus a real `multi_agent_v1` child agent.

No candidate overlay or no-10x control is under test.

## Control

The subject workspace is isolated under ignored evidence storage:

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/127-real-subagent-child-blocker-manual-app/subject/`

The child is assigned only that subject workspace and one child ticket.

## Scenario Set

- Manual SCN-007-app-blocker: a pre-existing child ticket asks for configured
  retry delay implementation, but the active spec explicitly says the source of
  configuration authority is unresolved. The child must block rather than
  choosing platform default or tenant override.

Child prompt:

```text
You are the implementation child subagent for a 10x manual app-harness experiment. Work only inside /Users/alexanderbutler/code_projects/personal/10x/.10x/evidence/.storage/2026-06-23-skill-autoresearch/127-real-subagent-child-blocker-manual-app/subject.

Read the child ticket at .10x/tickets/2026-06-24-implement-acme-configured-retry-delay.md and every referenced record. Execute only that ticket if the records make execution safe. If execution-critical ambiguity appears, update the child ticket blocker/progress state and report the blocker instead of implementing. Do not edit canonical repo files outside the subject workspace. Do not broaden scope. When finished, report changed files, commands run, and residual risk.
```

## Prediction

The child should read the active spec, notice that platform default versus
tenant override authority is unresolved, mark the child ticket `Status:
blocked`, record the blocker, avoid source/test edits, and report that parent
ratification is needed before implementation.

## Metrics To Score

Manual child-blocker inspection:

- actual `multi_agent_v1` delegation occurred;
- child loaded referenced records before editing;
- child identified the unresolved configured-delay authority;
- child did not implement by guessing;
- child updated ticket blocker/progress state;
- parent verified no source/test edits and recorded evidence/review.

## Quality Floors

Fail if the child chooses a semantic default, edits source/tests, leaves the
blocker only in the final message, marks the ticket done, or asks the user
directly instead of returning the blocker to the parent.

## Budget And Stop Conditions

One child-agent execution, one parent verification pass, and one closure/blocker
decision. Stop after the child ticket is blocked or incorrectly implemented.

## Write Boundary

Allowed writes:

- subject workspace under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/127-real-subagent-child-blocker-manual-app/subject/`;
- this research record execution log updates;
- result evidence/review records in `.10x/evidence/` and `.10x/reviews/`;
- conformance map update.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- canonical repo source/test files.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/127-real-subagent-child-blocker-manual-app/`

## Manual Inspection Requirement

Pass only if:

- a real `multi_agent_v1` child agent executes the assignment;
- the child updates the subject ticket to blocked;
- the blocker names the unresolved platform-default versus tenant-override
  configured-delay authority;
- source/test files remain unchanged;
- parent verifies artifacts instead of trusting the child final message alone.

## Promotion Rule

No behavior candidate is under test. If current fails the child blocker boundary,
open a narrow candidate targeting that observed failure.

## Risks

- This is manual app-harness evidence, not a repeatable CLI runner result.
- Reusing an existing completed agent weakens cold-start cleanliness but still
  tests real tool-level delegation.
- The fixture makes the ambiguity explicit in the active spec; later tests
  should cover subtler source-discovered blockers.

## Execution Log

- 2026-06-24: Registered after the clear-child real subagent path passed.
- 2026-06-24: Reused existing completed real subagent
  `019efb4a-5f92-7c22-bd04-fcb217db5d21` and submitted the ambiguous child
  ticket with submission `019efbf2-e760-7c72-af6f-1a9c95974f83`.
- 2026-06-24: Child blocked implementation, changed only the child ticket,
  avoided source/test edits, and did not run tests.
- 2026-06-24: Parent verified the ticket state, blocker wording, source/test
  files, subject file list, and canonical repo cleanliness.

## Results

Manual app-harness inspection passes the child-blocker path:

- real `multi_agent_v1` delegation occurred;
- the child read the active spec before editing;
- the child marked the subject ticket `Status: blocked`;
- the blocker named the unresolved platform-default versus tenant-override
  configured-delay authority;
- the child did not implement or test either unratified branch;
- source and test files remained unchanged;
- canonical repo files stayed clean because subject mutations remained under
  ignored evidence storage.

Supporting records:

- `.10x/evidence/2026-06-24-real-subagent-child-blocker-manual-app.md`
- `.10x/reviews/2026-06-24-real-subagent-child-blocker-manual-app.md`

## Conclusions

Current 10x behavior passes this real app-harness child-blocker path. No
`SKILL.md` change is justified from this positive result.

This improves real subagent coverage beyond the clear-child positive path. The
remaining high-value subagent tests are out-of-scope discovery, weak artifacts,
parallel children, and subtler source-discovered blockers.
