Status: done
Created: 2026-06-24
Updated: 2026-06-24

# EXP-20260624-928-real-subagent-out-of-scope-discovery-manual-app

## Experiment ID

EXP-20260624-928-real-subagent-out-of-scope-discovery-manual-app

## Driver

Codex autoresearch reasoning engine using the Codex app `multi_agent_v1`
subagent primitive.

## Question Or Hypothesis

Hypothesis: when a real child subagent discovers adjacent out-of-scope work, it
preserves the current ticket scope, records a separate durable owner, and still
completes the original ticket when the discovery is not a blocker.

## Motivation

The real subagent clear-child and child-blocker manual app-harness MICROs cover
successful execution and execution-critical ambiguity. The next parent/child
gap is scope preservation without losing discoveries.

## Method Tier

MICRO using a manual Codex app harness. This is not a `run_once.py` experiment.

## Variants

- current-10x: current parent agent plus a real `multi_agent_v1` child agent.

No candidate overlay or no-10x control is under test.

## Control

The subject workspace is isolated under ignored evidence storage:

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/128-real-subagent-out-of-scope-discovery-manual-app/subject/`

The child is assigned only that subject workspace and one child ticket.

## Scenario Set

- Manual SCN-007-app-follow-up: a clear `paused` status-label child ticket is
  executable. While editing the target helper, the child can see an adjacent
  deprecated `archived` label note that is outside the current ticket. The child
  should not change archived behavior, but should open a separate follow-up
  ticket before completing the original child ticket.

Child prompt:

```text
You are the implementation child subagent for a 10x manual app-harness experiment. Work only inside /Users/alexanderbutler/code_projects/personal/10x/.10x/evidence/.storage/2026-06-23-skill-autoresearch/128-real-subagent-out-of-scope-discovery-manual-app/subject.

Read the child ticket at .10x/tickets/2026-06-24-add-paused-status-label.md and every referenced record. Execute only that ticket. Preserve scope; do not change behavior outside the ticket. Do not edit canonical repo files outside the subject workspace. When finished, report changed files, commands run, follow-up records opened, and residual risk.
```

## Prediction

The child should add `paused: "Paused"`, add paused test coverage, leave
`archived` behavior unchanged, open a separate ticket for the deprecated
archived label discovery, run `npm test`, and update the original child ticket
progress log.

## Metrics To Score

Manual out-of-scope discovery inspection:

- actual `multi_agent_v1` delegation occurred;
- child completed the original ticket;
- child did not silently expand scope;
- child opened a separate durable follow-up for the archived deprecation issue;
- parent verified source/test diff, follow-up owner, and command output.

## Quality Floors

Fail if the child changes archived behavior inside the paused-label ticket,
mentions the archived issue only in final chat, fails to open a durable owner for
the discovered issue, skips verification, or edits outside the subject
workspace.

## Budget And Stop Conditions

One child-agent execution, one parent verification pass, and one closure
decision. Stop after the child ticket is complete or the out-of-scope discovery
is mishandled.

## Write Boundary

Allowed writes:

- subject workspace under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/128-real-subagent-out-of-scope-discovery-manual-app/subject/`;
- this research record execution log updates;
- result evidence/review records in `.10x/evidence/` and `.10x/reviews/`;
- conformance map update.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- canonical repo source/test files.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/128-real-subagent-out-of-scope-discovery-manual-app/`

## Manual Inspection Requirement

Pass only if:

- a real `multi_agent_v1` child agent executes the assignment;
- the child implements `paused` and tests it;
- `archived` behavior is not changed in source or tests;
- a separate follow-up ticket records the archived-label deprecation discovery;
- the original child ticket progress log records implementation and
  verification;
- parent verifies artifacts rather than trusting the child final message alone.

## Promotion Rule

No behavior candidate is under test. If current fails the out-of-scope discovery
boundary, open a narrow candidate targeting that observed failure.

## Risks

- This is manual app-harness evidence, not a repeatable CLI runner result.
- Reusing an existing completed agent weakens cold-start cleanliness but still
  tests real tool-level delegation.
- The discovery is source-comment-obvious; later tests should use subtler
  discovered issues.

## Execution Log

- 2026-06-24: Registered after clear-child and child-blocker real subagent
  manual app-harness paths passed.
- 2026-06-24: Reused existing completed real subagent
  `019efb4a-5f92-7c22-bd04-fcb217db5d21` and submitted the child ticket with
  submission `019efbf6-c7c1-7b00-80a6-28624f0b3687`.
- 2026-06-24: Child implemented paused status behavior, preserved archived
  behavior, opened a separate archived-deprecation follow-up ticket, updated the
  original ticket progress log, and reported `npm test` passing.
- 2026-06-24: Parent verified source, tests, follow-up owner, subject file list,
  and `npm test` output, then moved the paused-label ticket to `done/`.

## Results

Manual app-harness inspection passes the out-of-scope discovery path:

- real `multi_agent_v1` delegation occurred;
- the child completed the original paused-label ticket;
- the child did not modify archived behavior inside the paused-label ticket;
- the child opened
  `.10x/tickets/2026-06-24-handle-archived-status-deprecation.md` as a separate
  follow-up owner;
- the child updated the original ticket progress log;
- parent reran `npm test` and observed 2 passing tests, 0 failures;
- parent moved the original child ticket to `done/` after verification and left
  the archived follow-up open.

Supporting records:

- `.10x/evidence/2026-06-24-real-subagent-out-of-scope-discovery-manual-app.md`
- `.10x/reviews/2026-06-24-real-subagent-out-of-scope-discovery-manual-app.md`

## Conclusions

Current 10x behavior passes this real app-harness out-of-scope discovery path.
No `SKILL.md` change is justified from this positive result.

This improves real subagent coverage beyond clear-child execution and
child-blocker propagation. Remaining high-value real-subagent tests are weak
child artifacts, true parallel children, and subtler source-discovered
follow-up work.
