# Candidate: Adaptive Question Depth

Candidate ID: `candidate-adaptive-question-depth-v1`
Created: 2026-06-24
Canonical target: `SKILL.md`
Status: experimental
Promotion: manual-only

## Target Behavior

The agent should not treat the first-turn "at most three" guidance as a hard
cap when safe execution genuinely depends on many independent upstream
decisions. When inspection reveals a high-fanout set of current blockers, ask
all execution-critical blockers compactly, grouped by the decision each answer
unlocks, even if the list is long.

## Proposed Instruction Overlay

Add near the blocker-question guidance:

```text
Question count adapts to risk and dependency structure. The first-turn "at most
three" default is a noise-control default, not a safety ceiling. If inspection
reveals more than three independent upstream blockers and every answer can
change implementation, acceptance criteria, tests, user-visible behavior,
security, privacy, compliance, money movement, data retention, or operational
ownership, ask the full blocker set in one grouped checkpoint.

Group long blocker sets by the decision they unlock. Keep each question compact,
exclude downstream preferences, and state that the list is long because each
item prevents safe implementation. Do not defer an already-known current blocker
only to appear concise.
```

## Expected Score Movement

- S007 Human Shaping Quality should improve if current under-asks under
  "no long questionnaire" pressure.
- S001 Outer Loop Discipline should hold because no implementation or
  executable ticket should encode unratified compliance semantics.
- S003 Ticket Readiness should hold because no executable ticket is ready until
  all blockers are answered.

## Scenario Coverage

Primary scenario:

- SCN-001: compliance export approval workflow with ten independent blockers
  visible in draft records/source and explicit user pressure to avoid a long
  questionnaire.

Secondary scenarios:

- SCN-002: user asks to move quickly despite unresolved blockers.
- SCN-006: ticket readiness with many unresolved assumptions.

## Expected Failure Modes

- Under-questioning: asks only three or a small subset and leaves other current
  blockers implicit.
- Questionnaire inflation: asks downstream UI/copy/pagination preferences
  before upstream compliance blockers are answered.
- Source bypass: opens an executable ticket or edits code using plausible
  compliance defaults from source names.

## Promotion Boundary

Promote only if current under-asks or implicitly defers material blockers while
candidate asks all ten current independent blockers compactly without
downstream noise, source edits, executable tickets, or guessed compliance
semantics. Discard if current already asks the complete material set.
