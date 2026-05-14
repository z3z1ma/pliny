# How Loom Thinks

Loom turns AI engineering work into a shared human-agent control plane with clear
judgment, bounded execution slices, evidence, audit, reusable knowledge, and
recoverable records.

Loom works when the agent treats the `.loom` directory as the durable shape of the
work, not as notes beside the work.

## Ambiguity Is A Routing Signal

The first responsibility is to shape the front-loaded engineering judgment before
execution. If the operator's ask is broad, aspirational, quality-driven, missing
constraints, unclear about evidence, or vague about design direction, stay in the
outer loop and identify which truth is missing.

Low-record execution is acceptable only for tiny, obvious, low-risk work whose
outcome, boundary, evidence posture, important non-goals, and system-shape,
data-model, or state-relationship implications are already concrete. For anything
else, shape with the operator and route the clarified truth into the surface that
owns it before creating tickets, packets, or patches.

Outer-loop shaping should expose the choices that determine whether the work will
hold together: what belongs in the direction, what should be excluded, which seams
and data relationships should carry the behavior, and what would make the result
coherent instead of merely implemented.

## Truth Lives In The Right Surface

Do not let the newest artifact, loudest artifact, or current chat message win by
default.

Ask which surface can maintain the truth:

- constitution owns durable project judgment, policy, principles, constraints,
  ADRs, and roadmap direction
- tickets own executable work units, live execution state, acceptance, and closure
  posture
- research owns investigation, tradeoffs, rejected paths, synthesis, and
  conclusions
- specs own intended behavior, requirements, scenarios, interfaces, and invariants
- plans own operator-shaped strategy for complex changes spanning multiple
  tickets or execution units
- evidence owns observations, outputs, reproductions, screenshots, logs, and
  validation
- audit owns adversarial review findings and verdicts from Ralph review runs
- knowledge owns preferences, procedures, accepted explanation, reusable
  understanding, and retrieval cues
- packets own bounded execution, review, and worker contracts for Ralph runs

When truth is in the wrong place, move the durable version to the appropriate
surface and simplify the accidental one.

## Keep The Graph Coherent

A Loom surface is authoritative for the kind of truth it owns.

A ticket can describe live execution state, but it should not silently rewrite a
spec. A packet can bound worker execution, but it should not outrank the records
it was compiled from. Evidence can prove an observation, but it does not decide
intent. Audit can identify risk, but it does not itself change the product
contract.

When surfaces disagree, do not average them. Find the surface responsible for the
claim, preserve the correct version there, and make the conflict visible.

## The Recovery Graph

The `.loom` directory is the recovery graph.

Its records should be easy to find with `find`, reduce with `grep`, and
understand by reading the Markdown.

Use stable words, IDs, labels, headings, statuses, dates, and refs to keep the
graph searchable. Records should link to other records in prose when the connection
matters.

The prose remains the record. Structure helps retrieval, but the writing carries
the reasoning.

A record should help a future agent reason, recover, verify, or act.

## Workflow-Specific Skills Move Through Record Skills

A record skill owns a Loom surface and its procedure: constitution, research,
specs, plans, tickets, evidence, audit, knowledge, or packets. A
workflow-specific skill adds task-shaped pressure, such as debugging, testing,
UI work, migration, review, or release. It does not own a durable surface.

When a workflow-specific skill routes to a record skill or another Loom skill,
follow the target skill's procedure and guidance completely. The routing skill
narrows the work; it does not abbreviate record shape, evidence, audit, ticket,
or packet requirements.

When a workflow-specific skill is active, keep using the surface that owns each
truth: specs for intended behavior, plans for multi-ticket strategy, tickets for
live execution, packets for worker contracts, evidence for durable observations,
and audit for Ralph review findings.

If workflow guidance would execute before intent, scope, evidence, or ticket
boundary is shaped, stay in the outer loop and route the missing truth first.

## Record When It Helps

Always route work through Loom. Create records when they help.

Create or update records when doing so materially improves recovery, judgment,
execution, verification, review, or future reuse.

Skip record creation when the work is tiny, obvious, low-risk, and leaves no
durable truth behind.

Do not preserve every intermediate thought. Preserve the durable truth where a
future agent will know to look for it.

## Common Routes

If a task needs a bounded executable work unit, use tickets.

If it changes durable project judgment, policy, principle, constraint, precedent,
ADR shape, or roadmap direction, use constitution.

If it changes intended behavior, requirements, scenarios, interface expectations,
or invariants, use specs.

If it needs investigation, comparison, synthesis, rejected paths, or null results,
use research.

If it needs operator-shaped strategy across more than one bounded ticket or
execution unit, use plans.

If an observation should remain available as proof, support, challenge, or future
context, use evidence.

If it needs adversarial review through Ralph, use audit.

If it creates reusable accepted understanding, preference, procedure, or retrieval
cue, use knowledge.

If it executes or reviews a bounded ticket slice, use a Ralph packet.
