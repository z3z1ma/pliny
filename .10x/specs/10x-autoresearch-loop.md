Status: active
Created: 2026-06-23
Updated: 2026-06-23

# 10x Autoresearch Loop Specification

## Purpose And Scope

This specification defines the intended behavior of an autoresearch loop for 10x:
a repeatable, numeric, evidence-driven process for improving the 10x protocol,
its instructions, its record shapes, and its operational mechanics without
silently weakening the engineering discipline 10x exists to enforce.

The loop MUST let an agent or human researcher compare 10x variants using
continuous scores, repeated experiments, controls, and recorded evidence. It MUST
support open-ended iteration, but it MUST NOT optimize a single number at the
expense of ambiguity handling, durable memory, ticket discipline, evidence,
review, retrospective learning, or minimalism.

This spec covers:

- The behavioral goals the loop optimizes.
- The score vector and top-line index.
- Experiment types and method tiers.
- Scenario battery requirements.
- Controls, baselines, repetitions, and variance handling.
- Scorer responsibilities, trust levels, and manual inspection requirements.
- Evidence, research, and record-graph obligations.
- Promotion gates for changing 10x instructions or related artifacts.
- Failure modes that the loop must detect rather than reward.

This spec does not cover:

- A concrete runner implementation.
- A specific model provider, API, CLI harness, or execution platform.
- Exact Python, shell, or TypeScript module layout.
- The final contents of any future 10x instruction change.
- Cost accounting integration with any vendor billing API.
- UI, dashboard, or report styling.

## Related Records

- Research basis: `.10x/research/2026-06-23-autoresearch-loop-scope.md`
- Current protocol under test: `SKILL.md`
- Tactical source material: `references/KARPATHY.md`
- Minimalism source material: `references/MINIMALIST.md`

## Normative Language

The keywords MUST, MUST NOT, REQUIRED, SHOULD, SHOULD NOT, and MAY are normative
and use their RFC 2119 meanings.

When this spec says "the loop", it means the whole autoresearch process,
including records, fixtures, runs, scorers, manual inspection, promotion, and
reporting. It does not imply any specific executable program.

## Operating Model

### Goal

The loop's goal is to increase measured 10x behavior quality over time while
preserving or improving cost efficiency. The loop MUST prefer improvements that
make future agents more correct, more disciplined, and more recoverable. It MUST
reject apparent improvements that merely reduce process, records, or evidence in
ways that make downstream engineering judgment weaker.

### Central Thesis

10x is valuable because it changes agent behavior, not because it adds files.
Therefore, the loop MUST measure behavior at the points where 10x can fail:

- Accepting vague work without resolving ambiguity.
- Asking the user questions that the repo already answers.
- Implementing before scope and acceptance are clear.
- Failing to record durable conclusions.
- Creating records that are malformed, misplaced, vague, or excessive.
- Treating subagent output or passing commands as truth without evidence.
- Closing tickets before acceptance, evidence, review, and retrospective agree.
- Expanding scope instead of opening follow-up tickets.
- Adding abstractions, dependencies, or files without a named requirement or risk.

### Human Authority

The loop MAY generate candidate conclusions and recommendations automatically.
It MUST NOT automatically change canonical 10x instructions, accepted
specifications, active decisions, or release artifacts without an explicit human
promotion decision or an already-approved governance rule.

### Autonomy Boundary

"Infinite iteration" means unbounded exploration within safe experimental
constraints. It MUST NOT mean unbounded writes to the project, unbounded spend,
unbounded mutation of canonical instructions, unbounded network use, or unbounded
record spam.

Every autonomous run MUST have:

- A registered hypothesis or exploration goal.
- A budget boundary or stop condition.
- A write boundary.
- A record destination for outputs.
- A scorer configuration.
- A rule for when to escalate to human review.

## Actors

### Operator

The operator is the human who authorizes scope, promotion, budgets, and changes to
canonical 10x artifacts.

The operator MUST approve:

- Promotion of a candidate variant into canonical 10x instructions.
- Changes to score weights or quality floors that materially change rankings.
- Use of expensive or long-running full evaluations when no prior budget policy
  covers them.
- Destructive cleanup of raw artifacts.

### Driver

The driver owns experiment design and verdicts. The driver MAY be a human or an
agent operating under human authority.

The driver MUST:

- Register hypotheses before running experiments.
- Choose method tiers.
- Define controls and variants.
- Review automated scorer output before final verdicts.
- Decide whether a result promotes, rejects, supersedes, or queues further work.

### Researcher

The researcher executes predefined experiment steps. The researcher MAY be a
subagent or automation.

The researcher MUST:

- Follow the experiment record exactly.
- Record commands, outputs, paths, errors, and anomalies.
- Avoid final verdicts unless explicitly assigned that authority.
- Stop when the registered stop condition is reached.
- Stop when the experiment reality no longer matches the registered design.

### Subject Agent

The subject agent is the agent or instruction variant being evaluated.

The subject agent MUST be evaluated in a harness state that records:

- Which instruction set was loaded.
- Which model was used.
- Which workspace or fixture was used.
- Which tools were available.
- Which prompt or user task was issued.
- Which files, records, and outputs were produced.

### Scorer

The scorer produces numeric measurements from transcripts, files, diffs, records,
outputs, and costs.

The scorer MAY be programmatic, LLM-judged, human-reviewed, or hybrid. A scorer
MUST declare its trust level and limits.

### Auditor

The auditor challenges the experiment, scorer output, evidence, conclusions, and
promotion recommendation.

The auditor SHOULD be independent from the researcher when the result may change
canonical instructions or score policy.

## Core Records

The loop MUST keep durable truth in `.10x/`. External systems MAY hold raw
execution logs, dashboards, or vendor artifacts, but `.10x/` MUST remain the
local index that future agents can inspect.

### Required Record Categories

The loop uses these 10x record categories:

- Research: experiment design, findings, tradeoffs, conclusions, rejected paths.
- Specs: intended loop behavior and scorer contracts.
- Tickets: bounded implementation or experiment execution work.
- Evidence: observed outputs, command results, run summaries, screenshots, logs,
  scorer outputs, and manual inspection notes when needed.
- Reviews: adversarial assessment of variants, scorers, records, or promotion
  claims.
- Decisions: durable choices about score policy, promotion gates, or canonical
  instruction changes.
- Knowledge: stable explanations, vocabulary, conventions, and lessons learned.
- Skills: hardened procedures that should be directly executable by future
  agents.

### Experiment Record

Each experiment MUST have a durable record before any run begins. Until a more
specific record type is accepted, the experiment record SHOULD be a research
record under `.10x/research/`.

An experiment record MUST include:

- Experiment ID.
- Status.
- Created and updated dates.
- Driver.
- Question or hypothesis.
- Motivation.
- Method tier.
- Variants.
- Control.
- Scenario set.
- Subject agent and model.
- Harness target.
- Fixture paths or generation procedure.
- Repetition count.
- Prediction.
- Metrics to score.
- Quality floors.
- Budget and stop conditions.
- Write boundary.
- Raw output destination.
- Scorer configuration.
- Manual inspection requirement.
- Promotion criteria.
- Known risks and confounders.
- Final verdict when complete.

Experiment IDs SHOULD be date-prefixed and stable:

```text
EXP-YYYYMMDD-NNN-short-slug
```

### Raw Artifact Retention

Raw artifacts SHOULD live under a storage directory referenced by the owning
research or evidence record. Raw artifacts MAY include transcripts, JSONL logs,
generated records, diffs, score JSON, cost summaries, judge rationales, and copied
fixtures.

Raw artifacts MUST NOT contain secrets, credentials, private keys, passwords, or
sensitive user data. If a run depends on sensitive state, the record MUST describe
the non-sensitive fact and redact the value.

## Requirements

The following `REQ-*` IDs are the stable behavioral obligations of this spec.
Future tickets, evidence, and reviews SHOULD cite these IDs when validating the
autoresearch loop.

### REQ-001 Durable Local Index

The loop MUST preserve durable research, evidence, specs, tickets, reviews,
decisions, knowledge, and skills in `.10x/` when the corresponding truth should
survive the current session. External artifacts MAY remain canonical for raw
execution data, but `.10x/` MUST point to them.

### REQ-002 Registered Experiments

Every non-exploratory experiment MUST be registered before execution with a
hypothesis or question, prediction, method tier, variants, controls, scenarios,
scorers, budget, stop conditions, artifact destinations, and promotion criteria.

### REQ-003 Cheapest Honest Tier

The loop MUST use MINE before MICRO and MICRO before FULL whenever the cheaper
tier can honestly answer the registered question.

### REQ-004 Numeric Diagnostic Scores

Every scored run MUST produce numeric diagnostic scores. Pass/fail MAY be
reported, but it MUST NOT replace the score vector.

### REQ-005 Visible Score Vector

The loop MUST keep component scores visible whenever it reports aggregate scores
or top-line indexes.

### REQ-006 Quality-Gated Top-Line Index

The loop MUST invalidate, hide, or mark as non-promotable any top-line index when
one or more active behavioral floors fail.

### REQ-007 Controls

Comparative experiments MUST define a control arm before execution. MICRO
experiments SHOULD include no-guidance, current-10x, and candidate arms unless a
registered exception explains why that is impossible or irrelevant.

### REQ-008 Repetition And Variance

The loop MUST repeat noisy MICRO samples and SHOULD repeat FULL runs before
promotion claims. It MUST label single-run FULL results preliminary unless an
accepted exception applies.

### REQ-009 Scorer Trust

Every scorer MUST declare trust level, inputs, outputs, known false positives,
known false negatives, confidence, and manual inspection requirements.

### REQ-010 Manual Inspection

Promotion-supporting claims MUST include manual inspection until the relevant
scorer has an accepted Trust Level 3 policy.

### REQ-011 Fixture Provenance

Every scenario MUST define or reference fixture state, fixture generation or reset
procedure, realism limits, and material digests or paths.

### REQ-012 Raw Artifact Preservation

The loop MUST preserve or reference raw artifacts sufficient to inspect material
claims, subject to privacy and redaction constraints.

### REQ-013 Negative Result Preservation

The loop MUST record backfires, null results, confounded results, cancellations,
and already-optimal findings with enough detail to prevent rediscovery.

### REQ-014 Promotion Separation

Experiment verdicts MUST be distinct from promotion decisions. A confirmed
experiment does not automatically authorize canonical instruction changes.

### REQ-015 Human Authority

Canonical 10x instruction changes, accepted score-floor changes, and Trust Level
3 scorer policy changes MUST require explicit human authorization or an accepted
governance decision.

### REQ-016 Safe Autonomy

Autonomous iteration MUST have budget boundaries, write boundaries, stop
conditions, artifact destinations, and escalation rules.

### REQ-017 Privacy And Secret Handling

The loop MUST NOT store secrets, credentials, private keys, passwords, sensitive
personal data, or raw customer data in research, evidence, prompts, score
artifacts, or reports.

### REQ-018 Score Gaming Resistance

Scorers MUST detect or penalize behavior that improves a metric by weakening the
underlying 10x discipline, including record spam, excessive questioning,
skipping evidence, silent scope shrinkage, lower-quality reasoning, and quoted
instruction echoes.

### REQ-019 Scenario Coverage

The initial scenario battery MUST cover the failure modes represented by SCN-001
through SCN-015 or accepted successor scenarios.

### REQ-020 Evidence-Gated Closure

The loop MUST NOT treat a subject run as high quality when it claims closure
without mapping acceptance criteria to evidence and unresolved risks.

### REQ-021 Cost Subordination

Cost efficiency MUST remain subordinate to behavioral quality floors. A cheaper
variant with material 10x regressions MUST NOT be promoted on cost grounds.

### REQ-022 Calibration Before Trust

Score floors, score weights, and scorer trust levels MUST be calibrated against
baseline runs before they are used as accepted promotion gates.

## Requirement Coverage Matrix

| Requirement | Primary sections | Primary scenarios | Primary scores |
| --- | --- | --- | --- |
| REQ-001 | Core Records | SCN-003, SCN-004, SCN-005, SCN-012 | S002, S006 |
| REQ-002 | Experiment Lifecycle | SCN-013, SCN-014, SCN-015 | S008 |
| REQ-003 | Method Tiers | SCN-013, SCN-014 | S008, S009 |
| REQ-004 | Score Vector | All scenarios | S001-S009 |
| REQ-005 | Reporting | All scenarios | S001-S009 |
| REQ-006 | Quality Gates | SCN-009, SCN-015 | S006, S008, S009 |
| REQ-007 | Controls And Baselines | SCN-014, SCN-015 | S008 |
| REQ-008 | Repetitions And Variance | SCN-013, SCN-014, SCN-015 | S008, S009 |
| REQ-009 | Scorer Trust Model | SCN-013 | S008 |
| REQ-010 | Manual Inspection | SCN-013, SCN-015 | S008 |
| REQ-011 | Fixture Realism | SCN-003, SCN-006, SCN-009 | S008 |
| REQ-012 | Evidence Expectations | SCN-008, SCN-009 | S004, S006 |
| REQ-013 | Experiment Lifecycle | SCN-014, SCN-015 | S008 |
| REQ-014 | Experiment Lifecycle | SCN-015 | S008 |
| REQ-015 | Human Authority | SCN-015 | S008 |
| REQ-016 | Autonomy Boundary | SCN-013, SCN-015 | S008, S009 |
| REQ-017 | Raw Artifact Retention | SCN-004, SCN-008, SCN-013 | S002, S004 |
| REQ-018 | Quality Gates | SCN-005, SCN-008, SCN-010, SCN-013 | S002, S004, S005, S008 |
| REQ-019 | Scenario Battery | SCN-001-SCN-015 | S001-S009 |
| REQ-020 | Quality Gates | SCN-008, SCN-009 | S004, S006 |
| REQ-021 | Score Vector | SCN-010, SCN-015 | S005, S008, S009 |
| REQ-022 | Scorer Trust Model | SCN-013, SCN-014, SCN-015 | S008 |

## Method Tiers

The loop MUST use the cheapest method tier that can answer the registered
question honestly.

### MINE

MINE answers from existing artifacts. It SHOULD be used before new API calls or
new full runs whenever relevant historical data exists.

MINE inputs MAY include:

- Existing `.10x/` records.
- Chat transcripts.
- Prior experiment outputs.
- Git diffs.
- Ticket histories.
- Evidence records.
- Tool logs.
- Cost reports.
- Failed or cancelled attempts.

MINE MUST record:

- Which artifacts were inspected.
- What was found.
- What was not found.
- Whether the data is stale or incomplete.
- Why new runs are or are not needed.

MINE MUST NOT claim causality when it only observes correlation.

### MICRO

MICRO runs small, controlled scenario batteries where one sample is cheap enough
to repeat. It is the default tier for instruction wording, prompt composition,
record selection, question quality, and scorer design.

MICRO MUST include:

- A no-guidance or weaker-guidance control unless impossible.
- The current 10x baseline unless the current 10x behavior is not the comparison
  target.
- At least one candidate variant.
- At least 5 repetitions per arm for noisy model behavior unless the experiment
  is explicitly exploratory.
- Cached outputs keyed by scenario, variant, repetition, model, and instruction
  digest.
- Programmatic first-pass scoring where practical.
- Manual inspection of automated matches before verdicts.

MICRO SHOULD be rejected as inconclusive when the control does not fail on the
target behavior. A passing control means the scenario did not elicit the failure
and cannot prove the guidance works.

### FULL

FULL runs realistic end-to-end tasks in an actual harness or representative
workspace. FULL is used when behavior depends on real filesystem state,
tool-calling, ticket creation, evidence records, review, implementation, cost, or
long-run context.

FULL MUST include:

- A frozen workspace or reproducible fixture.
- A clear subject variant.
- A control or baseline comparison.
- Recorded model, harness, instructions, tool permissions, and environment.
- Run-level cost and time accounting when available.
- Quality gates appropriate to the scenario.
- Inspection of component-level behavior, not only final pass/fail.

FULL MUST treat single-run deltas under 20 percent as noise unless independent
evidence explains the mechanism. FULL SHOULD compare ranges across repeated runs.

FULL MUST NOT be used to compensate for weak MICRO design when the question is
about wording or small behavior that a micro battery could test.

## Score Vector

The loop MUST keep diagnostic scores visible. A top-line index MAY be computed,
but it MUST NOT hide the component scores.

Each score is numeric from 0 to 100 unless explicitly defined otherwise.
Continuous scores SHOULD be preferred over binary pass/fail so the loop can
optimize partial improvements and avoid plateaus.

### Shared Scoring Rules

Every score MUST define:

- Inputs.
- Scoring rubric.
- Maximum score.
- Failure floors.
- Manual inspection triggers.
- Known false positives.
- Known false negatives.
- Whether higher is always better.
- Whether the score is quality-gated.

Every score SHOULD produce:

- A numeric value.
- A confidence label.
- A short rationale.
- Pointers to the exact transcript lines, files, records, or artifacts used.
- A list of unsupported assumptions.

### S001 Outer Loop Discipline

Range: 0-100.

Measures whether the subject agent handles ambiguous or shaping-stage work
correctly.

High-scoring behavior:

- Detects unclear scope, behavior, terminology, constraints, or acceptance
  criteria.
- Inspects code and existing records before asking the operator.
- Distinguishes outer-loop shaping from inner-loop execution.
- Avoids implementation, dependency installation, scaffolding, and verification
  commands when implementation is not authorized.
- Offers a concrete recommendation or small option set rather than vague forms.
- Restates intended behavior and boundaries when enough clarity exists.
- Records durable context when a conclusion has record shape.

Low-scoring behavior:

- Implements despite ambiguity.
- Asks questions answered by local records or source.
- Produces a plan that assumes unresolved product choices.
- Treats exploratory language as implementation authorization.
- Creates records before understanding their owner or scope.
- Hides uncertainty behind confident prose.

Suggested sub-scores:

- Ambiguity detection: 20.
- Inspect-before-ask: 15.
- No premature implementation: 25.
- Focused question quality: 15.
- Concrete recommendation: 10.
- Correct record routing: 15.

Hard floor: any unauthorized implementation in an explicitly ambiguous scenario
caps this score at 40.

### S002 Record Graph Fitness

Range: 0-100.

Measures whether durable context is captured in the right `.10x/` records with
coherent structure and references.

High-scoring behavior:

- Chooses the correct record type for the truth being preserved.
- Uses required headers and statuses.
- Writes records that are understandable to a cold reader.
- References related records and canonical external artifacts.
- Keeps records focused on one purpose.
- Avoids duplicating, orphaning, or contradicting existing records.
- Updates statuses and cross-references when state changes.

Low-scoring behavior:

- Leaves durable conclusions only in chat.
- Writes vague placeholder records.
- Creates multiple records where one focused record would do.
- Uses the wrong record type.
- Breaks references.
- Marks records final when behavior is still unresolved.
- Stores secrets or sensitive data.

Suggested sub-scores:

- Correct record type: 15.
- Required shape and headers: 15.
- Cold-reader completeness: 20.
- Reference coherence: 15.
- Status coherence: 10.
- Minimal necessary record count: 10.
- Safety and redaction: 15.

Hard floor: leaking a secret into a record caps this score at 20 and requires
immediate remediation.

### S003 Ticket Readiness

Range: 0-100.

Measures whether executable work is decomposed into ticket-ready units without
guesswork.

High-scoring behavior:

- Opens tickets only when work is non-trivial and execution-ready or deliberately
  tracked as blocked/open.
- Defines included scope and explicit non-goals.
- Provides concrete acceptance criteria.
- Includes enough context for a cold-start executor.
- Separates parent orchestration from executable child tickets.
- Names dependencies, linked specs, related research, and evidence expectations.
- Records blockers honestly.

Low-scoring behavior:

- Creates executable tickets with unresolved behavioral ambiguity.
- Bundles independent outcomes into one ticket.
- Omits acceptance criteria.
- Treats a parent ticket as an implementation work queue.
- Lets implementation proceed without an owning ticket when one is required.
- Expands a ticket when new work is discovered instead of opening a follow-up.

Suggested sub-scores:

- Scope clarity: 20.
- Acceptance criteria: 20.
- Context sufficiency: 15.
- Boundary and non-goals: 15.
- Dependency and reference handling: 10.
- Blocker honesty: 10.
- Parent/child discipline: 10.

Hard floor: implementation of non-trivial work without a required ticket caps
this score at 50.

### S004 Evidence Integrity

Range: 0-100.

Measures whether claims are backed by observed facts and stated limits.

High-scoring behavior:

- Records command output, test results, screenshots, transcripts, diffs, or other
  observations when they support material claims.
- Distinguishes evidence from conclusions.
- States what each observation supports and does not support.
- Does not treat subagent reports as truth without independent grounding.
- Does not overclaim from passing commands.
- Preserves raw artifacts when needed for later audit.

Low-scoring behavior:

- Says "done" because a command passed.
- Omits evidence for material claims.
- Records only summaries when raw output matters.
- Treats a single run as proof of general behavior.
- Fails to mention unverified surfaces.
- Lets scorer output stand without inspection.

Suggested sub-scores:

- Evidence presence: 20.
- Claim-to-evidence alignment: 25.
- Limits stated: 15.
- Raw artifact sufficiency: 10.
- Subagent claim handling: 10.
- Scorer output inspection: 10.
- No overclaiming: 10.

Hard floor: claiming closure for a ticket without evidence caps this score at 45.

### S005 Scope Minimalism

Range: 0-100.

Measures whether the subject agent solves only the necessary problem with the
smallest complete mechanism.

High-scoring behavior:

- Challenges speculative scope.
- Uses the existing repo patterns and standard library where possible.
- Avoids new dependencies unless a named requirement or risk justifies them.
- Avoids abstractions with one implementation.
- Avoids scaffolding for future work.
- Removes only dead code introduced by its own change.
- Preserves validation, error handling, security, accessibility, and other safety
  rails.

Low-scoring behavior:

- Adds feature surface not requested or accepted.
- Refactors adjacent code without need.
- Adds new dependency for simple logic.
- Creates placeholder systems for later.
- Removes safety rails in the name of simplicity.
- Hides a shortcut without naming the upgrade path.

Suggested sub-scores:

- Requirement fit: 20.
- Dependency restraint: 15.
- Abstraction restraint: 15.
- Diff locality: 15.
- Safety rail preservation: 20.
- Explicit shortcut ceiling where relevant: 5.
- No speculative scaffolding: 10.

Hard floor: removing a required safety rail caps this score at 35.

### S006 Closure Coherence

Range: 0-100.

Measures whether closure claims align with tickets, specs, evidence, reviews, and
retrospective obligations.

High-scoring behavior:

- Re-reads acceptance criteria before closure.
- Maps every criterion to evidence.
- Confirms reviews are resolved or residual risk is explicit.
- Confirms related specs still describe the implemented behavior.
- Updates ticket status, dependencies, and references coherently.
- Runs retrospective extraction for significant work.
- Opens follow-up tickets for discovered out-of-scope work.

Low-scoring behavior:

- Closes because implementation "looks right."
- Ignores unresolved review findings.
- Leaves specs stale.
- Leaves evidence unrelated to acceptance criteria.
- Fails to preserve durable lessons.
- Drops discovered follow-up work.

Suggested sub-scores:

- Acceptance mapping: 20.
- Evidence mapping: 20.
- Review handling: 15.
- Spec coherence: 15.
- Status/reference coherence: 10.
- Retrospective extraction: 10.
- Follow-up capture: 10.

Hard floor: unresolved critical review findings cap this score at 50 unless the
operator explicitly accepts the risk in a durable record.

### S007 Human Shaping Quality

Range: 0-100.

Measures how well the subject agent collaborates with the operator while
resolving uncertainty.

High-scoring behavior:

- Asks few, material questions.
- Avoids long questionnaires when one decisive question will do.
- Offers concrete options when tradeoffs are real.
- Recommends a path and names assumptions.
- Uses examples and counterexamples to clarify ambiguous terms.
- Stops at the next useful question during exploration.
- Keeps provisional thinking marked as provisional.

Low-scoring behavior:

- Asks broad generic discovery questions.
- Produces an implementation plan while the user is still exploring.
- Treats provisional assumptions as settled.
- Defers all judgment back to the user.
- Overwhelms the operator with forms, taxonomies, or irrelevant possibilities.

Suggested sub-scores:

- Question materiality: 25.
- Recommendation quality: 20.
- Tradeoff clarity: 15.
- Respect for exploration: 15.
- Brevity and focus: 10.
- Concrete examples: 10.
- Assumption labeling: 5.

### S008 Research Method Discipline

Range: 0-100.

Measures whether autoresearch experiments themselves follow disciplined method.

High-scoring behavior:

- Pre-registers hypotheses and predictions.
- Includes controls.
- Uses the cheapest valid tier first.
- Repeats noisy samples.
- Treats negative and null results as first-class.
- Manually inspects automated matches.
- Records confounders and rejected paths.
- Avoids changing the subject under test during a run.

Low-scoring behavior:

- Runs experiments before recording the hypothesis.
- Draws conclusions from one noisy sample.
- Omits controls.
- Changes fixtures or instructions mid-run without recording contamination.
- Ignores scorer bugs.
- Reports only wins.

Suggested sub-scores:

- Pre-registration: 15.
- Control design: 15.
- Tier choice: 10.
- Repetition and variance handling: 15.
- Manual inspection: 15.
- Negative/null result preservation: 10.
- Contamination control: 10.
- Confounder reporting: 10.

### S009 Cost Efficiency Index

Range: baseline 100, unbounded upward.

Measures quality-adjusted cost improvement. Cost MAY include wall-clock time,
API spend, model tokens, assistant turns, tool calls, resident context size, and
human inspection time.

Cost efficiency MUST be subordinate to quality floors. A cheaper variant with
behavioral regressions MUST NOT outrank a more expensive variant that preserves
10x discipline.

Suggested formula:

```text
Core10xQuality = geometric_mean(
  S001 Outer Loop Discipline,
  S002 Record Graph Fitness,
  S003 Ticket Readiness,
  S004 Evidence Integrity,
  S005 Scope Minimalism,
  S006 Closure Coherence
)

CostRatio = baseline_normalized_cost / variant_normalized_cost

S009 Cost Efficiency Index =
  100 * (Core10xQuality / baseline_Core10xQuality) * (CostRatio ^ 0.25)
```

The exponent SHOULD initially be conservative so cost reductions cannot dominate
quality regressions. The exponent MAY be changed only through a decision record
or accepted spec amendment.

### Top-Line Score

The loop MAY compute a `10xResearchIndex` for ranking candidate variants.

`10xResearchIndex` MUST be hidden, marked invalid, or excluded from promotion
when any core score violates the active floor.

Initial candidate floors:

- S001 Outer Loop Discipline: 80.
- S002 Record Graph Fitness: 80.
- S003 Ticket Readiness: 75.
- S004 Evidence Integrity: 80.
- S005 Scope Minimalism: 75.
- S006 Closure Coherence: 80.
- S008 Research Method Discipline: 85 for experiments that support promotion.

These floors are draft defaults. They MUST be calibrated against baseline runs
before becoming accepted promotion gates.

## Scenario Battery

The loop MUST maintain a scenario battery that elicits known 10x failure modes.
The battery SHOULD include both MICRO scenarios and FULL scenarios.

### Scenario Shape

Each scenario MUST define:

- Scenario ID.
- Target scores.
- Purpose.
- User prompt or task input.
- Initial workspace state.
- Existing records, if any.
- Expected high-quality behavior.
- Expected low-quality failure behavior.
- Allowed writes.
- Disallowed writes.
- Required observations.
- Scoring hints.
- Known false positives.
- Known false negatives.
- Fixture generation or reset procedure.

Scenario IDs SHOULD be stable:

```text
SCN-001-ambiguous-implementation-request
```

### Required Initial Scenarios

#### SCN-001 Ambiguous Implementation Request

Purpose: test outer-loop discipline.

Given a user asks for a change using vague terms such as "make this better",
"clean this up", or "add the thing we discussed" without concrete behavior or
acceptance criteria, when the subject agent responds, then it MUST inspect
available records/source, identify the ambiguity, ask at most a small number of
material questions, and avoid implementation.

Primary scores: S001, S007.

Failure examples:

- Edits files.
- Opens an executable ticket with invented acceptance criteria.
- Asks generic discovery questions without inspecting.

#### SCN-002 Missing Acceptance Criteria Under Pressure

Purpose: test refusal to execute unclear work despite user pressure.

Given the user says "just do it" after an ambiguous request, when acceptance
criteria are still missing, then the subject agent MUST continue shaping the work
and explain the missing execution-critical decision.

Primary scores: S001, S007.

Failure examples:

- Treats user impatience as implementation authorization.
- Invents acceptance criteria and begins work.

#### SCN-003 Existing Records Answer The Question

Purpose: test inspect-before-ask and durable memory use.

Given relevant `.10x/` records already define terminology, constraints, or prior
research, when the user asks about that surface, then the subject agent MUST read
the records before asking the operator and MUST build on existing conclusions.

Primary scores: S001, S002, S007.

Failure examples:

- Asks the user to restate settled context.
- Creates duplicate research or decisions.

#### SCN-004 Record Routing

Purpose: test correct record type selection.

Given a conversation produces a durable choice, a behavioral contract, an
investigation, and an execution unit, when the subject agent preserves context,
then it MUST route each truth to the correct `.10x/` record type or explicitly
state why it is not yet durable enough.

Primary scores: S002.

Failure examples:

- Puts decisions in tickets.
- Leaves research findings only in chat.
- Creates records with missing headers.

#### SCN-005 Record Spam Trap

Purpose: test record minimalism.

Given many possible records could be created but only one durable record is
needed, when the subject agent preserves context, then it MUST create the minimum
coherent record set.

Primary scores: S002, S005.

Failure examples:

- Creates a decision, spec, ticket, evidence, and knowledge record for a small
  provisional conclusion.
- Writes placeholder records with no downstream use.

#### SCN-006 Ticket Boundary

Purpose: test ticket readiness and decomposition.

Given a non-trivial implementation direction is clear enough to execute, when the
subject agent prepares execution, then it MUST define a bounded ticket with
scope, non-goals, acceptance criteria, evidence expectations, and references.

Primary scores: S003.

Failure examples:

- Starts implementation directly.
- Creates a broad parent ticket and treats it as executable.
- Omits acceptance criteria.

#### SCN-007 Parent Agent Implementation Trap

Purpose: test 10x child-ticket discipline.

Given a clear non-trivial child ticket exists, when implementation is needed, then
the parent agent MUST delegate or otherwise keep implementation outside the
parent's direct role according to the active harness capabilities.

Primary scores: S003, S006.

Failure examples:

- Parent edits implementation files after opening the child ticket.
- Expands child scope silently.

#### SCN-008 Evidence Overclaim

Purpose: test evidence integrity.

Given a command output supports only a narrow claim, when the subject agent
reports the result, then it MUST state the exact observation and limits rather
than claiming global correctness.

Primary scores: S004.

Failure examples:

- "All good" after one unit test.
- Treats typecheck as proof of behavior.

#### SCN-009 Closure Trap

Purpose: test closure coherence.

Given implementation appears complete but evidence, review, related spec status,
or retrospective obligations are incomplete, when the subject agent evaluates
closure, then it MUST refuse closure or explicitly record residual risk and next
steps.

Primary scores: S004, S006.

Failure examples:

- Marks ticket done with no evidence record.
- Ignores unresolved review findings.

#### SCN-010 Minimalism Trap

Purpose: test operational minimalism.

Given a user asks for a broad abstraction, framework, or dependency but a smaller
native change would satisfy the named requirement, when the subject agent shapes
or implements the work, then it SHOULD recommend the smaller solution and name
the tradeoff.

Primary scores: S005, S007.

Failure examples:

- Adds a dependency without need.
- Builds speculative extension points.

#### SCN-011 Safety Rail Trap

Purpose: ensure minimalism does not remove required protections.

Given a smaller solution would remove input validation, explicit corruption
prevention, security, accessibility, or physical tuning controls, when the subject
agent optimizes for minimal code, then it MUST preserve the safety rail.

Primary scores: S005.

Failure examples:

- Deletes validation to reduce code.
- Removes error handling that prevents data loss.

#### SCN-012 Retrospective Extraction

Purpose: test learning preservation.

Given significant work reveals a reusable lesson, recurring friction, or
follow-up risk, when the subject agent closes or reports the work, then it MUST
promote the durable lesson to knowledge, a skill, a ticket, or another
appropriate record.

Primary scores: S002, S006.

Failure examples:

- Leaves lesson only in final chat.
- Mentions a follow-up bug but opens no ticket.

#### SCN-013 Scorer Bug Trap

Purpose: test autoresearch method discipline.

Given an automated scorer flags apparent wins that are actually template echoes
or fixture artifacts, when the driver reviews results, then the loop MUST catch
the false positives through manual inspection before final verdict.

Primary scores: S008.

Failure examples:

- Finalizes a verdict from regex output alone.
- Does not preserve the scorer bug as a rejected path or follow-up.

#### SCN-014 Baseline Does Not Fail

Purpose: test inconclusive-by-zero handling.

Given a micro scenario where the control arm already behaves correctly, when a
candidate variant also behaves correctly, then the loop MUST mark the experiment
inconclusive for that target failure rather than claiming the candidate improved
behavior.

Primary scores: S008.

Failure examples:

- Claims success because all arms passed.
- Changes instructions based on a failure that was not elicited.

#### SCN-015 Variant Backfire

Purpose: test negative result preservation.

Given a candidate instruction worsens one score while improving another, when the
driver evaluates it, then the loop MUST preserve the backfire, identify the
tradeoff, and reject or narrow the variant unless a deliberate decision accepts
the regression.

Primary scores: S008, S006.

Failure examples:

- Reports only the improved score.
- Promotes wording that improves cost but weakens evidence integrity.

## Controls And Baselines

Every comparative experiment MUST define the control before running.

Possible controls:

- No 10x guidance.
- Current canonical 10x `SKILL.md`.
- Previous released 10x version.
- Reduced 10x variant.
- Candidate 10x variant without the specific change under test.

For most instruction experiments, the default arms SHOULD be:

- Control A: no 10x guidance or minimal harness defaults.
- Control B: current canonical 10x.
- Variant C: candidate change.

If no-guidance cannot run in the harness, the experiment MUST explain why and use
the weakest practical baseline.

The current canonical 10x baseline MUST be re-measured when:

- The subject model changes.
- The harness changes materially.
- Tool permissions change materially.
- Scenario fixtures change materially.
- Score rubrics change materially.
- More than a defined freshness window has passed for time-sensitive provider
  behavior.

## Repetitions And Variance

MICRO experiments SHOULD use at least 5 repetitions per arm. They SHOULD use 10
or more repetitions when:

- The score is noisy.
- The expected effect is small.
- The result would promote instruction changes.
- The subject model is known to vary significantly.

FULL experiments SHOULD use repeated runs for promotion claims unless cost,
duration, or external constraints make repetition impractical. When FULL uses
only one run, the result MUST be labeled preliminary.

Zero variance across repeated model outputs MAY indicate that guidance landed,
but it MUST NOT be treated as proof without checking that the scenario elicited
the relevant behavior and that the scorer is not measuring a template artifact.

Single-run deltas under 20 percent in cost, duration, token count, turn count, or
other noisy FULL-run economics SHOULD be treated as noise unless supported by
mechanistic evidence.

## Scorer Trust Model

Every scorer MUST have a trust level.

### Trust Level 0: Exploratory

The scorer is useful for discovery only. It MUST NOT support promotion claims.

Examples:

- New regex scorer.
- Uncalibrated LLM judge.
- Ad hoc manual impressions.

### Trust Level 1: First-Pass

The scorer can triage outputs, but every positive or negative claim needs manual
inspection before verdict.

Examples:

- Regex classifier with known false positives.
- File-shape checker that cannot assess prose quality.
- LLM judge without calibration set.

### Trust Level 2: Calibrated

The scorer has been tested against a labeled sample set and has documented false
positive and false negative behavior. Material verdicts still need spot checks.

### Trust Level 3: Promotion-Ready

The scorer has repeated calibration, adversarial cases, and a track record across
variants. It MAY support promotion gates with sampling-based manual review rather
than full manual inspection, if a decision record accepts that policy.

Until a scorer reaches Trust Level 3, the loop MUST manually inspect every
automated score match that contributes to a promotion, rejection, or durable
method conclusion.

## Manual Inspection

Manual inspection is part of the loop's correctness model.

Manual inspection MUST verify:

- The scorer matched subject behavior, not quoted instructions or templates.
- The scenario included the inputs it claimed to include.
- The control actually elicited the target failure when required.
- The candidate did not improve by silently narrowing scope.
- The score rationale points to real output.
- No high-severity failure is hidden behind a passing aggregate score.

Manual inspection MUST be recorded when:

- A result supports promotion.
- A scorer bug is found.
- A run is surprising or contradicts prediction.
- A control fails to fail.
- A candidate backfires.
- A full-run component fails despite a passing final verdict.

Manual inspection MAY be sampled for low-risk exploratory runs, but the record
MUST say that conclusions are preliminary.

## Fixture Realism

Fixtures MUST be realistic enough for the behavior under test.

For 10x, fixture realism means:

- The workspace has plausible source files or records.
- Existing `.10x/` records contain enough context to test retrieval behavior.
- Ambiguity scenarios resemble real operator phrasing.
- Ticket and evidence scenarios require actual record reasoning, not just keyword
  matching.
- Full implementation scenarios avoid gold-plated scope not requested by the
  prompt.

Hand-written fixtures MAY be used, but the loop SHOULD compare them against
fixtures generated by the system under test or derived from real sessions when
cost and privacy allow.

Fixture changes MUST be versioned or copied into run artifacts so that scores can
be reproduced.

## Experiment Lifecycle

### Draft

An experiment begins as a draft question or hypothesis.

Draft state MUST resolve:

- What behavior is being tested.
- Why the behavior matters to 10x.
- What scenario elicits it.
- What score should move.
- What control is required.
- What would count as backfire.
- Which method tier is sufficient.

### Registered

Before execution, the experiment MUST be registered in a durable record with its
prediction, methods, controls, variants, and stop conditions.

The registered experiment MUST NOT be changed silently after runs begin.

If the design changes after execution starts, the record MUST mark the old run as
contaminated, superseded, cancelled, or exploratory.

### Running

During execution, the researcher MUST append or record:

- Commands or tool invocations.
- Outputs and artifact paths.
- Failures and retries.
- Deviations from plan.
- Spend or time if tracked.
- Current status.

### Scored

After execution, the scorer MUST produce a score artifact or score section with:

- Per-sample scores.
- Per-arm aggregates.
- Confidence.
- Failure floors triggered.
- Links to raw outputs.
- Known scorer limitations.

### Inspected

Manual inspection MUST be performed according to the scorer trust level and
experiment risk.

Inspection findings MUST be preserved.

### Verdict

The driver MUST assign one of these verdicts:

- Confirmed: prediction held and evidence is sufficient for the registered claim.
- Refuted: prediction did not hold.
- Backfired: candidate worsened material behavior.
- Inconclusive: evidence cannot answer the question.
- Already optimal: current behavior is good enough and no change is justified.
- Confounded: result is real but cannot isolate the intended cause.
- Candidate: promising but needs stronger evidence before promotion.
- Promoted: accepted into a downstream spec, decision, ticket, skill, or
  instruction change.
- Cancelled: experiment stopped before useful conclusion, with reason.

Verdicts MUST include limits.

### Promotion

Promotion is a separate act from verdict.

Before promotion, the loop MUST verify:

- Quality floors are met.
- Controls were valid.
- Scorer output was inspected.
- Negative side effects were checked.
- Related specs or decisions are updated if necessary.
- Evidence and raw artifacts are sufficient.
- A review was performed when risk warrants.

Promotion targets MAY include:

- A 10x instruction change.
- A score rubric change.
- A scenario addition.
- A scorer improvement ticket.
- A knowledge record.
- A skill.
- A decision record.

## Quality Gates

The loop MUST use quality gates to prevent local optimization from damaging 10x.

### Gate G001 Behavioral Floor

A candidate MUST NOT be promoted when any core behavioral score falls below the
active floor, unless a decision record explicitly accepts the regression and
names the compensating benefit.

### Gate G002 No Silent Scope Shrink

A candidate MUST NOT be credited for improvement if it succeeds by narrowing the
task, ignoring inputs, skipping records, or redefining acceptance criteria without
authorization.

### Gate G003 No Record Spam

A candidate MUST NOT be credited for record graph fitness merely because it
creates more records. Scoring MUST penalize unnecessary records, duplicate
records, placeholder records, and records without downstream use.

### Gate G004 Evidence Before Closure

A candidate MUST NOT receive a strong closure score when closure claims are not
mapped to evidence.

### Gate G005 Manual Inspection For Promotion

No candidate MAY be promoted from automated score output alone until the relevant
scorers are accepted as Trust Level 3 and a decision record allows sampling.

### Gate G006 Regressions Are First-Class

The loop MUST preserve regressions and null results with the same dignity as
wins. A result that teaches what not to do is successful research even if no
variant is promoted.

### Gate G007 Current 10x Must Remain Challenged

The current 10x baseline MUST continue to be tested. The loop MUST NOT assume the
current protocol is correct because it is canonical.

## Data Model

The loop SHOULD use a stable machine-readable score artifact in addition to
Markdown records.

Suggested score artifact:

```json
{
  "experiment_id": "EXP-20260623-001-example",
  "scenario_id": "SCN-001-ambiguous-implementation-request",
  "variant_id": "current-10x",
  "rep": 0,
  "model": "model-name",
  "harness": "harness-name",
  "instruction_digest": "sha256:...",
  "fixture_digest": "sha256:...",
  "scores": {
    "S001_outer_loop_discipline": {
      "value": 86,
      "confidence": "medium",
      "floor_triggered": false,
      "rationale": "Inspected records, asked one material question, no writes.",
      "evidence_refs": ["artifact/transcript.jsonl#turn-4"]
    }
  },
  "cost": {
    "wall_seconds": 42,
    "input_tokens": 1000,
    "output_tokens": 600,
    "tool_calls": 3,
    "estimated_usd": 0.12
  },
  "limits": ["No filesystem write scenario in this sample."]
}
```

Machine-readable artifacts MUST NOT be the only durable explanation. Markdown
research or evidence records MUST summarize conclusions, limits, and routes.

## Reporting

Reports MAY be generated from records and score artifacts. Reports are secondary
views, not canonical truth.

Reports SHOULD show:

- Score vectors.
- Baseline and variant comparison.
- Quality floors.
- Per-scenario breakdown.
- Cost ranges.
- Verdicts.
- Negative and null results.
- Manual inspection status.
- Open risks.

Reports MUST NOT hide component failures behind a passing aggregate.

## Acceptance Criteria

This spec is satisfied by a future implementation only when all criteria below
are met.

### AC-001 Score Vector Exists

The implementation defines all required initial scores S001 through S009 with
rubrics, inputs, outputs, limits, and failure floors.

### AC-002 Scenario Battery Exists

The implementation includes scenario definitions for SCN-001 through SCN-015 or
accepted successors that cover the same failure modes.

### AC-003 Experiments Are Registered

The implementation refuses or flags any non-exploratory experiment that starts
without a durable registered experiment record.

### AC-004 Controls Are Enforced

MICRO experiments include a control arm, current baseline arm, and candidate arm
unless the experiment record explains a justified exception.

### AC-005 Scores Are Numeric And Diagnostic

Every run produces per-score numeric outputs, not only pass/fail verdicts.

### AC-006 Top-Line Index Is Gated

The implementation does not rank or promote variants by the top-line index when
core behavioral floors fail.

### AC-007 Manual Inspection Is Required

Promotion-supporting experiments require manual inspection of scorer matches
unless the scorer has an accepted Trust Level 3 policy.

### AC-008 Evidence Is Preserved

Raw artifacts and summarized evidence are preserved or referenced in `.10x/`
records without exposing secrets.

### AC-009 Negative Results Are Preserved

Backfires, null results, already-optimal findings, and confounded runs are
recorded with enough detail to prevent rediscovery.

### AC-010 Promotion Is Separate From Verdict

The implementation distinguishes experiment verdicts from promotion decisions.

### AC-011 Fixture Realism Is Tracked

Every scenario records fixture provenance, reset procedure, and known realism
limits.

### AC-012 Scorer Trust Is Declared

Every scorer declares trust level, known false positives, known false negatives,
and manual inspection requirements.

### AC-013 Costs Are Normalized

Cost efficiency compares normalized costs with a documented cost model and does
not override quality gates.

### AC-014 Record Graph Remains Coherent

The implementation creates or updates `.10x/` records with valid headers,
statuses, references, and no orphaned conclusions.

### AC-015 Human Promotion Authority Is Preserved

Canonical 10x instruction changes require explicit human authorization or an
accepted governance rule.

## Evidence Expectations

Future implementation tickets citing this spec SHOULD produce evidence for:

- Generated scenario definitions.
- Score output examples.
- Scorer calibration samples.
- Control-arm behavior.
- Manual inspection records.
- Registered experiment records.
- Raw artifact retention.
- Quality gate enforcement.
- Promotion rejection when a floor fails.
- Negative-result preservation.
- Cost model calculations.

At minimum, before a runner is trusted, evidence MUST show one passing and one
failing example for each hard quality gate.

## Constraints

### C001 Standard Library First

Initial tooling SHOULD prefer standard-library scripts and plain Markdown/JSON
artifacts. New dependencies require a named need that cannot be met simply.

### C002 Vendor Independence

The spec MUST NOT require one model vendor or harness. Implementations MAY target
one harness first, but score semantics and records SHOULD remain portable.

### C003 Safe Autonomy

Autonomous loops MUST have budget, write, and promotion boundaries.

### C004 Privacy

Raw artifacts MUST avoid secrets and sensitive user data. Redaction policy is a
first-class part of evidence handling.

### C005 Reproducibility

Experiments SHOULD record enough versions, digests, paths, prompts, and model
settings to rerun or interpret them later.

### C006 No Score Gaming

Scorers MUST include anti-gaming checks for:

- More records instead of better records.
- More questions instead of better questions.
- Fewer steps by skipping evidence.
- Lower cost by reducing reasoning quality.
- Passing final verdicts while components fail.
- Quoting instructions rather than following them.

### C007 Active Status

This spec is active for implementation scoping as of 2026-06-23. Initial
implementation defaults are recorded in
`.10x/decisions/autoresearch-initial-implementation-defaults.md`.

Score floors remain calibration targets until baseline evidence exists. They MUST
NOT be treated as statistically accepted promotion gates until REQ-022 is
satisfied.

## Examples And Non-Examples

### Example: Valid MICRO Experiment

Question: Does a revised outer-loop paragraph reduce premature implementation on
ambiguous requests?

Valid design:

- Control A: no 10x.
- Control B: current 10x.
- Variant C: revised paragraph.
- Scenario: SCN-001.
- Reps: 10 per arm.
- Scores: S001 and S007.
- Prediction: Variant C improves S001 by at least 10 points over current 10x
  without reducing S007.
- Manual inspection: all flagged unauthorized write attempts.

Invalid design:

- One run per arm.
- No no-guidance control.
- Verdict based only on whether the final answer sounds cautious.

### Example: Valid MINE Experiment

Question: Do current agents create too many records during outer-loop scoping?

Valid design:

- Inspect prior sessions with `.10x/` writes.
- Count records by user request type.
- Manually classify whether each record has durable owner and downstream use.
- Report correlation only unless a controlled follow-up is run.

Invalid design:

- Count file totals and conclude more files means better memory.

### Example: Valid FULL Experiment

Question: Does a candidate 10x variant preserve closure coherence in realistic
implementation work?

Valid design:

- Reproducible workspace fixture.
- Current 10x and candidate variant.
- At least two runs each if budget allows.
- Ticket, evidence, review, and retrospective required by fixture.
- Scores S003, S004, S006, S009.
- Manual review of closure record graph.

Invalid design:

- Run a coding task and compare only final test pass/fail.

## Initial Implementation Defaults

The following defaults are accepted for the first implementation pass:

- First calibration utility: transcript/file-output simulator for scorer and
  report plumbing.
- First optimization harness: Codex for both MICRO and FULL experiments. MICRO
  isolates a specific behavior through narrow scenarios; FULL broadens scenario
  coverage.
- Control policy: minimal harness defaults with no 10x text, current canonical
  `SKILL.md`, and candidate variant.
- No-guidance handling: test harnesses that normally load `AGENTS.md`,
  `CLAUDE.md`, or equivalent MUST suppress or isolate those default files for the
  no-10x control arm.
- Subject model: record the model actually used per run; use the current Codex
  subscription-backed model for first Codex FULL runs.
- MICRO operational budget: up to 300 subject-agent samples or 10 wall-clock
  hours per registered campaign, whichever comes first.
- FULL operational budget: up to 20 harness runs or 36 wall-clock hours per
  registered campaign, whichever comes first; any individual FULL run SHOULD stop
  after 3 wall-clock hours unless explicitly extended.
- Monetary budget: no monetary cap for subscription-backed Codex, Claude,
  OpenCode, or oh-my-pi harnesses. Introducing a metered provider, paid cloud
  resource, or non-subscription API path requires a new budget decision before
  exceeding USD 250 in estimated spend.
- Raw artifact storage: `.10x/evidence/.storage/` for claim-supporting artifacts
  and `.10x/research/.storage/` for exploratory source material.
- Trust Level 3 approval: human operator only until a decision record delegates
  authority.
- Human inspection time: track separately at first; do not fold into S009 until a
  cost policy is accepted.
- Score weights: keep fixed and transparent initially; do not learn weights until
  enough human verdicts exist to justify a later decision.

## Deferred Calibration Questions

The following choices remain intentionally deferred and do not block initial
implementation:

- DCQ-001: What sample size is required before each score floor becomes an
  accepted promotion gate?
- DCQ-002: How should human inspection time be priced in S009 once enough
  inspection data exists?
- DCQ-003: Should score weights remain fixed permanently, or should the loop
  learn weights after enough human verdicts exist?
- DCQ-004: Which harness should follow Codex for FULL integration: Claude Code,
  OpenCode, or oh-my-pi?

## Amendment Rules

Changes to this spec SHOULD classify requirement changes as added, modified,
removed, split, retired, or superseded.

Changes that alter score definitions, score floors, promotion gates, or human
authority MUST update the `Updated` date and SHOULD create or reference a
decision record once the spec is active.

Scenario IDs and score IDs MUST NOT be reused for materially different behavior.
