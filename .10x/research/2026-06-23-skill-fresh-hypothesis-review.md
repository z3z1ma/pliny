Status: active
Created: 2026-06-23
Updated: 2026-06-23

# SKILL.md Fresh Hypothesis Review

## Question

After reading canonical `SKILL.md` fresh, what hypotheses are worth pursuing to
amplify 10x behavior and reduce obviously bad agent behavior?

## Sources And Methods

Sources inspected:

- `SKILL.md`
- `.10x/research/2026-06-23-skill-autoresearch-run.md`
- `.10x/evidence/2026-06-23-one-decisive-question-live-micro-rerun.md`
- `autoresearch/catalogs/scores.json`
- `autoresearch/catalogs/scenarios.json`

Method:

- Re-read `SKILL.md` end to end.
- Separated the skill's core premise from the narrow question-count candidate
  previously tested.
- Compared the premise against observed live-run failure modes.
- Identified candidate hypotheses that preserve the skill's discipline rather
  than optimizing superficial transcript style.

## Findings

The core premise of `SKILL.md` is a state machine for disciplined engineering:

- ambiguous work stays in the Outer Loop;
- clear work enters the Inner Loop only through an owning ticket;
- project memory is externalized into `.10x/`;
- records, evidence, reviews, and retrospectives make claims durable and
  inspectable;
- minimal implementation is subordinate to correctness, safety, and clarity;
- closure is not a claim until evidence, records, and residual risks cohere.

The skill does not need fewer questions. It needs better ambiguity economics:
extract as much execution-critical information as needed, in dependency order,
without asking what the repo already answers and without converting uncertainty
into implementation.

The one-question candidate was a bad optimization target. Complex software work
can require a long interview, and that interview is cheap compared with days of
incorrect implementation and rework. The right objective is not minimizing
question count; it is maximizing information gain per interaction while
continuing until execution-critical uncertainty is gone.

Current high-value behavioral surfaces:

- Outer Loop interrogation can become performative if it asks generic questions
  or prematurely narrows to one question.
- Record discipline can become process theater if agents create records because
  records are available, not because durable context crystallized.
- Ticket discipline can become heavy or brittle if the agent opens a ticket
  before the work is truly executable, or treats a parent ticket as a work
  queue.
- Minimalism can be misread as "do the smallest visible thing" instead of "spend
  the least complexity that fully satisfies the real contract."
- Subagent discipline may be over-applied in harnesses where no subagent exists,
  causing paralysis or fake delegation.
- Closure discipline is a major source of value, but agents may still overclaim
  because closure checks are distributed across several sections.

## Hypotheses Worth Pursuing

### H1: Information-Gain Interrogation

Candidate direction:

Add a clarification rule that says to ask as many questions as needed, but each
question must name the execution decision it resolves and why the answer changes
implementation, sequencing, constraints, or acceptance criteria.

Expected improvement:

- Improves S001 and S007 without suppressing legitimate interviews.
- Reduces generic question spam and bad one-question underfitting.

Failure mode to watch:

- Agents may produce verbose "question rationale" prose that burdens the user.

Best MICRO:

- SCN-001 plus a custom continuation where the first answer reveals another
  material ambiguity.

### H2: Ambiguity Ledger

Candidate direction:

For complex Outer Loop work, require a compact ambiguity ledger with columns:
`known`, `unknown`, `why it matters`, `source checked`, `status`. The ledger can
live in chat or a draft record while shaping. It becomes durable only when it has
record force.

Expected improvement:

- Helps agents interview relentlessly without losing track.
- Makes it clear why repeated questions are justified.
- Reduces premature specs/tickets because unresolved unknowns remain visible.

Failure mode to watch:

- Can become table theater or record spam if used for trivial work.

Best MICRO:

- A multi-turn ambiguous feature request where the user provides partial answers
  and new constraints over several turns.

### H3: Outer Loop Exit Checklist

Candidate direction:

Strengthen the exit condition into a short checklist the agent must satisfy
before creating an executable ticket or implementation plan:

- behavior known;
- scope and non-goals known;
- acceptance criteria known;
- constraints and safety rails known;
- dependencies/context inspected;
- user authorization explicit.

Expected improvement:

- Improves S001 and S003 by preventing half-shaped work from entering the Inner
  Loop.
- More aligned with the skill's premise than optimizing wording style.

Failure mode to watch:

- Agents may paste the checklist ritualistically without actually verifying it.

Best MICRO:

- SCN-006 ticket-boundary and SCN-002 pressure-to-proceed.

### H4: Record Creation Economy

Candidate direction:

Clarify that "durable context must reach disk" does not mean every useful
thought becomes a record immediately. Add a decision rule: create, update,
defer, or decline a record based on durability, ownership, and downstream reuse.

Expected improvement:

- Improves S002 and S005 by reducing record spam.
- Preserves the core durable-memory premise.

Failure mode to watch:

- Agents may defer records too often and lose context.

Best MICRO:

- SCN-005 record-spam-trap with current and candidate live runs.

### H5: Minimalism Means Complete Contract, Not Smallest Visible Action

Candidate direction:

Add a warning that minimalism is invalid if it removes behavior required by the
contract, skips safety rails, avoids necessary questions, or narrows scope
without user agreement.

Expected improvement:

- Improves S005 while preventing the "one question" style of false minimalism.
- Reinforces the interaction between minimalism and Outer Loop discipline.

Failure mode to watch:

- Agents may over-explain why every check is "necessary."

Best MICRO:

- SCN-010 minimalism-trap and SCN-011 safety-rail-trap.

### H6: No Fake Delegation

Candidate direction:

Clarify how parent/child/subagent discipline behaves when a harness lacks a real
subagent primitive: create the executable child ticket, then either invoke an
actual subagent when available or state that the current agent is operating as
the executor for that single child ticket under explicit role separation.

Expected improvement:

- Reduces paralysis and dishonest "assigned to subagent" claims.
- Improves S003/S006 coherence in harnesses that cannot spawn child agents.

Failure mode to watch:

- Could weaken the intended parent-does-not-implement invariant if phrased too
  loosely.

Best MICRO:

- SCN-007 parent-agent-implementation-trap.

### H7: Closure Evidence Matrix, But Only For Non-Trivial Tickets

Candidate direction:

Revive the closure evidence matrix idea with a scope limiter: use it only for
non-trivial tickets or major work. It should map each acceptance criterion to
evidence and residual limits.

Expected improvement:

- Improves S006 and S004 without forcing table overhead on tiny changes.

Failure mode to watch:

- Matrix theater or overuse on trivial work.

Best MICRO:

- SCN-009 closure-trap and SCN-012 retrospective-gap.

## Conclusions

The most promising next hypothesis is H1: Information-Gain Interrogation. It
directly addresses the operator concern: the agent should interview as deeply as
needed, even for an hour, when that prevents six hours of wrong execution. The
candidate should reject question-count optimization and instead require every
question to earn its place by naming what decision it resolves.

The second-best near-term hypothesis is H3: Outer Loop Exit Checklist. It
protects the Outer/Inner boundary in a measurable way and should pair well with
H1 after H1 proves useful.

Do not pursue one-question discipline further. The useful residue from that
probe is "avoid generic questionnaires," not "ask fewer questions."
