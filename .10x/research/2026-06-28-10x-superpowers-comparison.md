Status: done
Created: 2026-06-28
Updated: 2026-06-28

# 10x And Superpowers Holistic Mechanical Comparison

## Question

How does 10x differ mechanically and behaviorally from the Superpowers GitHub
repository, and where is 10x stronger as a method for producing durable,
higher-quality agent outcomes?

## Sources And Methods

Inspected 10x local repository at commit
`9bf1cde5e6a332235816e74920142052d96717e7`:

- `README.md`
- `SKILL.md`
- `autoresearch/README.md`
- `autoresearch/program.md`
- `.10x/specs/10x-autoresearch-loop.md`
- `.10x/decisions/autoresearch-live-trial-scientist-inspection.md`
- recent evidence/review records, including
  `.10x/evidence/2026-06-28-record-richness-hypothesis-batch.md`,
  `.10x/reviews/2026-06-28-record-richness-candidate-review.md`, and
  `.10x/reviews/2026-06-28-readme-public-launch-polish.md`

Cloned and inspected Superpowers from
`https://github.com/obra/Superpowers` at commit
`896224c4b1879920ab573417e68fd51d2ccc9072`:

- `README.md`
- `CLAUDE.md`
- `skills/using-superpowers/SKILL.md`
- `skills/brainstorming/SKILL.md`
- `skills/writing-plans/SKILL.md`
- `skills/executing-plans/SKILL.md`
- `skills/subagent-driven-development/SKILL.md`
- `skills/subagent-driven-development/implementer-prompt.md`
- `skills/subagent-driven-development/task-reviewer-prompt.md`
- `skills/test-driven-development/SKILL.md`
- `skills/systematic-debugging/SKILL.md`
- `skills/verification-before-completion/SKILL.md`
- `skills/requesting-code-review/SKILL.md`
- `skills/receiving-code-review/SKILL.md`
- `skills/using-git-worktrees/SKILL.md`
- `skills/finishing-a-development-branch/SKILL.md`
- `skills/writing-skills/SKILL.md`
- selected docs under `docs/superpowers/specs/`

No `evals/` directory or `.gitmodules` file was present in the cloned
Superpowers commit. Superpowers documentation points to an external
`superpowers-evals` / `evals/` setup and records eval findings in dated design
docs, but this comparison did not inspect that external eval repository.

## Findings

### Superpowers Core Shape

Superpowers is a multi-skill, multi-harness methodology. Its bootstrap skill
requires skill invocation before any action. Its primary development workflow is
roughly:

1. use `brainstorming` before creative or behavior-changing work;
2. write a design doc under `docs/superpowers/specs/`;
3. write a detailed implementation plan under `docs/superpowers/plans/`;
4. execute via subagent-driven development or inline plan execution;
5. enforce TDD during implementation;
6. run task review, final review, verification, and branch-finishing workflows.

It has strong concrete mechanics:

- mandatory skill dispatch;
- design approval before implementation;
- exact implementation plans with file paths, code, commands, and expected
  output;
- strict RED/GREEN/REFACTOR TDD;
- systematic root-cause debugging before fixes;
- subagent task briefs, report files, review packages, and a
  `.superpowers/sdd/progress.md` ledger for compaction recovery;
- reviewers instructed to distrust implementer reports and review task diffs
  against requirements and code quality;
- plugin/hook infrastructure for many harnesses.

### 10x Core Shape

10x is one portable instruction file plus a repo-local durable project context
system. The record graph is not the whole product; it is the substrate that
lets the agent behave differently. 10x teaches a universal operating method:

1. outer loop: inspect records/source, clarify ambiguity, classify assumptions,
   and record durable context;
2. inner loop: execute one bounded ticket only when behavior, constraints, and
   acceptance criteria are concrete enough;
3. evidence/review/closure: map acceptance criteria to observed evidence,
   review adversarially, handle spec drift, and extract durable learning.

Its key behavioral invention is an epistemic operating system: the agent is
trained to ask what kind of truth it is dealing with, what authority backs it,
what uncertainty remains, what action would be mutation, and what evidence
would prove the outcome. The typed `.10x/` graph gives that behavior durable
project context:

- decisions for durable choices and supersession;
- research for investigations and null results;
- specs for behavior contracts;
- tickets for bounded execution;
- evidence for reproducible observations;
- reviews for adversarial critique;
- knowledge for reusable context;
- skills for hardened procedures.

These records are separated truths, not a flat note pile. Decisions,
specifications, evidence, reviews, tickets, research, knowledge, and skills
have different authority, lifecycle, provenance, limits, and closure semantics.
The repo itself practices this method. At inspection time `.10x/` contained
active and historical records across these categories. The `autoresearch/`
system also evaluates the skill through registered live subject-agent trials
while keeping verdicts in durable `.10x/` records rather than runner-generated
scores.

### Behavioral Mechanics 10x Drives

10x changes how the agent asks questions. Superpowers brainstorming asks one
question at a time to refine a design. 10x first exhausts records, source, and
artifacts, then asks only current blockers whose answers change safe action. It
requires the agent to name what implementation would invent, classify prior
answers as answered/unresolved/superseded, give recommended contracts when
available, and avoid letting examples become requirements.

10x changes how the agent treats authority. Superpowers uses approved design
docs and plans as workflow inputs. 10x distinguishes active specs and decisions
from source-observed behavior, stale research, terminal tickets, examples,
tests, chat claims, external artifacts, and subagent reports. When these drift,
10x requires the conflict to be named rather than silently choosing whichever
artifact is convenient.

10x changes how the agent thinks before writing code. It does not merely say
"plan first." It defines implementation as any mutation later agents, builds,
runtime surfaces, project records, or services could depend on, and it bars
implementation while semantic assumptions remain unbacked. This includes
writing tests that encode guessed behavior. The result is less wrong-premise
code: the agent cannot make a passing test suite prove an unratified product
policy.

10x changes how the agent writes code once execution is valid. Inner-loop work
is ticket-scoped, spec-governed, acceptance-driven, and evidence-bound. The
agent reads the ticket and every referenced record before editing, executes only
that outcome, records blockers when ambiguity appears, and opens separate
owners for out-of-scope discoveries instead of widening the work silently.

10x changes review behavior. Superpowers uses task reviewers and final code
review packages. 10x makes review part of the project context graph: reviews
are adversarial records with target, verdict, findings, and residual risk. They
challenge work but do not close it. Closure requires reconciling reviews with
evidence, specs, statuses, dependencies, and retrospective obligations.

10x changes delegation. Superpowers protects subagents with task briefs,
reports, review packages, and progress ledgers. 10x can use subagents, but the
primary handoff is the project context graph: focused specs, executable
tickets, decisions, research, knowledge, prior evidence, and reviews. Those
records are not transient coordination files; they are the durable context a
future implementer and a future reviewer both share.

10x changes completion behavior. Superpowers verifies before completion. 10x
requires closure coherence: acceptance criteria mapped to evidence, spec drift
checked, review risk handled, statuses and references repaired, unresolved
follow-ups given durable owners, and learning extracted into the right record
type. "Done" becomes a graph state, not a final sentence.

### Where 10x Is Mechanically Stronger

10x is stronger at project context and authority. Superpowers preserves specs,
plans, and an SDD progress ledger, but those artifacts mostly support the
current implementation workflow. 10x makes layered project context the central
substrate: source of authority, provenance, status, record lifecycle,
supersession, evidence, review, and retrospective learning are all first-class
and typed.

10x is stronger at preventing wrong-premise implementation. Superpowers requires
brainstorming/spec approval and asks clarifying questions, but 10x explicitly
classifies every execution-relevant assumption as record-backed,
user-ratified, or blocked. It forbids tests, specs, tickets, and implementation
from laundering guessed semantics into truth.

10x is stronger across sessions because it does not preserve only progress; it
preserves the layered context needed to reason. Superpowers has a task progress
ledger for SDD resumption and docs/specs/plans, but 10x is built around
cold-start regeneration: future agents are expected to recover decisions,
constraints, acceptance criteria, evidence limits, unresolved blockers,
semantic authority, and learning from records without chat archaeology.

10x is stronger at closure coherence. Superpowers verifies before completion
and reviews changes, but 10x adds a closure-specific graph check: acceptance
criteria must map to evidence, review findings must be resolved or explicitly
accepted, specs must still match implementation, record references/statuses
must be coherent, and retrospective learning must be extracted before closure.

10x is stronger at evidence provenance. Superpowers requires verification and
uses reports/diffs/test evidence in SDD. 10x separates evidence from claims as a
record type, requires limits, preserves negative/null results, and treats
subagent reports, test passes, and runner outputs as claims until inspected.

10x is stronger at handling active-record/source drift. It distinguishes active
specs/decisions from current source implementation state and requires conflicts
to be named instead of silently resolved. Superpowers has strong spec/plan
alignment in the active workflow, but less generalized machinery for record
authority, supersession, stale records, terminal history, and external artifact
indexes.

10x is stronger as an institutional learning system. Superpowers skills are
tested and tuned, and its docs show serious eval thinking. 10x makes every
serious investigation, decision, evidence note, review, and lesson part of the
repo-local graph by default. The method is not just "use better skills"; it is
"make the project carry the context for why work was shaped, proven, accepted,
blocked, superseded, or rejected."

10x is stronger at shaping agent cognition. Superpowers gives the agent
procedures. 10x changes the default mental move: inspect before inventing,
classify truth before acting, ask only action-changing blockers, refuse semantic
defaults, keep examples as candidates until ratified, treat tests as claims,
and treat pressure as irrelevant to authority. These behaviors affect every
turn, not just named workflow stages.

### Where Superpowers Is Stronger Or More Complete

Superpowers is stronger as a packaged multi-harness product. It includes
plugins/hooks/manifests for many agents and a broader skill library.

Superpowers is stronger at strict TDD enforcement. 10x requires verification
and warns that tests can launder assumptions, but Superpowers has a much harder
"no production code without failing test first" rule.

Superpowers is stronger at detailed task execution choreography. Its SDD system
has precise mechanics for task briefs, implementer reports, review packages,
model selection, fix dispatches, final branch review, and branch finishing.

Superpowers is stronger for teams that want a concrete step-by-step delivery
pipeline and are willing to accept the ceremony of design-doc approval, exact
plans, commits per task, and TDD as the core work shape.

### Fundamental Difference

Superpowers primarily answers: "Which disciplined workflow skill should the
agent invoke, and how should it execute this branch right now?"

10x primarily answers: "How should an agent reason from layered project
context so it does not invent semantics, flatten provenance, over-trust claims,
lose decisions, or close work that is not actually proven?"

That difference changes outcomes. Superpowers can make a single session or
branch much more disciplined. 10x makes the project itself a richer reasoning
environment and changes the agent's behavior inside that environment.

## Conclusions

The strongest superiority claim for 10x is not that it has more process or only
that it has better records. It has a more complete behavioral and contextual
model. It turns ambiguity, ratification, assumptions, semantic authority,
evidence, review, closure, drift, supersession, and retrospective learning into
explicit mechanics with durable owners.

For long-lived projects, high-ambiguity product work, cross-session continuity,
regulated/high-impact semantics, and multi-agent execution where correctness
depends on not inventing business meaning, 10x should produce better outcomes
than Superpowers alone because it changes both what the agent knows and how the
agent is allowed to act on what it knows.

For short-to-medium feature implementation where the desired behavior is already
settled and the main risk is execution choreography, Superpowers' TDD and SDD
machinery may be equal or stronger. The two compose, but 10x should remain the
governing context layer: Superpowers can supply strict execution tactics, while
10x supplies the authority model, behavioral gates, project context graph, and
closure discipline.

## Limits

This comparison inspected the Superpowers repository at one commit and did not
inspect the external `superpowers-evals` repository. Claims about Superpowers
eval quality are therefore limited to the main repository's README,
contributor guidance, and dated design/spec records.
