# Product Discovery Loop

Use this reference when `loom-product-discovery` is active. It adapts divergent
and convergent ideation into Loom owner records rather than a separate idea file
system.

## Philosophy

- Start with user/operator experience and work backward to technology.
- Push toward the simplest version that solves the real problem.
- Focus means saying no to good ideas, not only bad ideas.
- Challenge assumptions with specificity, not hostility.
- Ground ideas in the codebase when inside a repository.
- Produce owner-record truth, not a polished one-pager that becomes a shadow spec.

## Phase 1: Understand And Expand

Goal: open the idea before narrowing it.

1. Restate the idea as a crisp "How might we" problem statement.
2. Ask only the material questions needed before expansion:
   - Who is this for, specifically?
   - What does success look like?
   - What current pain, workaround, or baseline proves the need?
   - What constraints matter: time, technology, policy, privacy, cost, support?
   - What has already been tried?
   - Why now?
3. If inside a codebase, inspect existing architecture, patterns, specs, tickets,
   analytics/evidence, docs, and prior attempts before inventing directions.
4. Generate five to eight variations using selected lenses:
   - inversion: what if we did the opposite?
   - constraint removal: what changes if time, budget, or tech limits vanished?
   - audience shift: what if this served a different user or operator?
   - combination: what adjacent workflow could this merge with?
   - simplification: what is the version ten times simpler?
   - scale: what breaks or becomes powerful at much larger scale?
   - expert lens: what would domain experts find obvious?

Do not generate 20 shallow ideas. The point is a small set of materially different
directions.

## Phase 2: Evaluate And Converge

Cluster promising variations into two or three directions. Stress-test each:

- User value: who benefits, by how much, and is it painkiller or vitamin?
- Feasibility: what is the hardest technical, operational, or organizational part?
- Differentiation: why would someone switch from current behavior?
- Evidence: what observed fact supports this direction?
- Risk: what could make this direction wrong, unsafe, too expensive, or stale?
- Maintenance: what ongoing burden does it create?
- Loom fit: which owner records would need to change?

Surface hidden assumptions:

- what must be true for this to work
- what could kill the idea
- what the team is choosing to ignore for now
- which assumption can be tested by spike, research, evidence, or user input

Be honest. If a direction is weak, say why and route it to rejected options rather
than preserving it as false balance.

## Phase 3: Sharpen And Route

Produce the durable output in owner records:

- initiative: durable objective, beneficiary, success metrics, autonomy boundaries
- research: variations, assumptions, rejected paths, evidence synthesis
- spec: intended behavior, requirements, scenarios, acceptance
- plan: decomposition, sequencing, dependencies, rollout
- ticket: bounded execution when behavior and scope are clear enough
- evidence/research: experiment, sketch, prototype, or feasibility probe results;
  use `loom-spike` as the workflow route when a bounded experiment is the next step
- wiki: accepted explanation after truth settles

A compact discovery summary is useful only if its claims land in the right owner
records. It should include:

- problem statement
- recommended direction and why
- assumptions to validate
- smallest valuable scope
- not-doing list
- open questions and whether they block downstream work

## Not-Doing List

The not-doing list is often the most valuable artifact. It should name attractive
excluded ideas and the reason they are excluded:

- out of scope for this user or objective
- too much implementation cost for current evidence
- creates migration or support burden
- requires policy/security decision first
- should wait for a spike or usage signal
- belongs to a later ticket or initiative

Do not bury tradeoffs in enthusiastic prose.

## Codebase-Grounded Discovery

When ideating inside a repository, look for:

- existing user flows, API surfaces, data models, and module seams
- prior specs/plans/tickets and open blockers
- current design-system or UX patterns
- constraints from package architecture, harnesses, or public docs
- test and evidence surfaces that could validate the idea
- abandoned or rejected attempts in research or critique

Grounded discovery does not mean implementation planning. It means options are
aware of reality before they become specs or tickets.

## Anti-Patterns

- yes-machining a weak idea
- skipping the target user/operator
- treating the requested solution as the problem statement
- producing a plan before assumptions are surfaced
- generating too many shallow options
- ignoring existing codebase constraints
- storing the real PRD outside Loom owner records
- asking for approval after every reversible step instead of recording delegated authority

## Verification

- a crisp problem statement exists
- target user/operator and success criteria are named
- several materially different directions were explored
- hidden assumptions and validation paths are explicit
- not-doing list captures real tradeoffs
- open questions are marked blocking or non-blocking
- downstream owner records now carry the durable truth
