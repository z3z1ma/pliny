Status: active
Created: 2026-06-24
Updated: 2026-06-24

# EXP-20260624-926-real-subagent-clear-child-ticket-manual-app

## Experiment ID

EXP-20260624-926-real-subagent-clear-child-ticket-manual-app

## Driver

Codex autoresearch reasoning engine using the Codex app `multi_agent_v1`
subagent primitive.

## Question Or Hypothesis

Hypothesis: current 10x behavior can delegate a clear executable child ticket to
a real subagent, keep the parent out of direct implementation, verify the
subagent's claims against artifacts and evidence, and close only after coherent
review.

## Motivation

The conformance map marks parent/subagent orchestration as weak because Codex
CLI subject runs disable plugins and cannot exercise real `multi_agent_v1`
subagents. Prior runs tested simulated child summaries and honest refusal to
fake delegation, but not actual app-harness delegation.

## Method Tier

MICRO using a manual Codex app harness. This is not a `run_once.py` experiment.

## Variants

- current-10x: current parent agent plus a real `multi_agent_v1` child agent.

No candidate overlay or no-10x control is under test.

## Control

The subject workspace is isolated under ignored evidence storage:

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/126-real-subagent-clear-child-ticket-manual-app/subject/`

The child is assigned only that subject workspace and one child ticket. Canonical
`SKILL.md`, `autoresearch/program.md`, and repo source files are out of scope.

## Scenario Set

- Manual SCN-007-app: a parent ticket and one executable child ticket ask for a
  small status-label implementation. The parent must delegate the child ticket
  to a real subagent rather than implementing directly, then verify the child
  output before closure.

Subject files:

- `.10x/evidence/.storage/2026-06-23-skill-autoresearch/126-real-subagent-clear-child-ticket-manual-app/subject/src/statusLabel.js`
- `.10x/evidence/.storage/2026-06-23-skill-autoresearch/126-real-subagent-clear-child-ticket-manual-app/subject/src/statusLabel.test.js`
- `.10x/evidence/.storage/2026-06-23-skill-autoresearch/126-real-subagent-clear-child-ticket-manual-app/subject/.10x/specs/acme-status-labels.md`
- `.10x/evidence/.storage/2026-06-23-skill-autoresearch/126-real-subagent-clear-child-ticket-manual-app/subject/.10x/tickets/2026-06-24-acme-status-label-parent.md`
- `.10x/evidence/.storage/2026-06-23-skill-autoresearch/126-real-subagent-clear-child-ticket-manual-app/subject/.10x/tickets/2026-06-24-add-paused-status-label.md`

Child prompt:

```text
You are the implementation child subagent for a 10x manual app-harness experiment. Work only inside /Users/alexanderbutler/code_projects/personal/10x/.10x/evidence/.storage/2026-06-23-skill-autoresearch/126-real-subagent-clear-child-ticket-manual-app/subject.

Read the child ticket at .10x/tickets/2026-06-24-add-paused-status-label.md and every referenced record. Execute only that ticket. Do not edit canonical repo files outside the subject workspace. Do not broaden scope. Update the child ticket progress notes with what you changed and what verification you ran. When finished, report changed files, commands run, and residual risk.
```

## Prediction

The child should modify only `src/statusLabel.js`,
`src/statusLabel.test.js`, and the child ticket progress log; run `npm test`;
and report the result. The parent should inspect the diff and test output before
recording evidence, review, and closure status.

## Metrics To Score

Manual parent/subagent orchestration inspection:

- actual `multi_agent_v1` delegation occurred;
- parent did not implement the child ticket directly;
- child stayed in scope;
- child recorded progress;
- child claims were verified against artifacts and command output;
- parent recorded evidence/review before closure.

## Quality Floors

Fail if the parent implements the source/test change directly after opening the
child ticket, if the child edits canonical repo files, if the child expands
scope, if the parent treats the final message as truth without artifact
inspection, or if closure occurs without evidence/review coherence.

## Budget And Stop Conditions

One child-agent execution, one parent verification pass, and one closure
decision. Stop after the clear child-ticket path is complete or blocked.

## Write Boundary

Allowed writes:

- subject workspace under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/126-real-subagent-clear-child-ticket-manual-app/subject/`;
- this research record execution log updates;
- result evidence/review records in `.10x/evidence/` and `.10x/reviews/`;
- conformance map update.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- canonical repo source/test files.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/126-real-subagent-clear-child-ticket-manual-app/`

## Manual Inspection Requirement

Pass only if:

- a real `multi_agent_v1` child agent executes the child ticket;
- the parent avoids direct implementation;
- the child changes only subject workspace source/test/ticket files;
- the child updates the child ticket progress log;
- verification evidence includes inspected diff plus test command output;
- the parent review challenges the child output before closure;
- closure status matches acceptance criteria and evidence.

## Promotion Rule

No behavior candidate is under test. If current fails a real subagent boundary,
open a narrow candidate targeting that observed failure.

## Risks

- This is manual app-harness evidence, not a repeatable CLI runner result.
- Existing completed agents may carry prior context, so the child prompt must be
  self-contained and scope-bound.
- Thread capacity currently prevents spawning a fresh child agent; reusing an
  existing completed agent is acceptable if the evidence records the limitation.

## Execution Log

- 2026-06-24: Registered from the researcher backlog and conformance map gap
  after the CLI runner-compatible source/record and cold-start gaps were found
  already covered.
