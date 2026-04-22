# Constitutional Record Families

The constitution subsystem owns three record families. They sit at the same layer of authority because each carries durable policy-grade truth that outlives any single ticket.

## `constitution:main`

Use for the enduring project frame:

- vision
- principles
- constraints
- strategic direction
- current focus

Usually one file per workspace. Link-light. Amended deliberately, not continuously.

## Decision records (ADRs)

Use when one architectural or policy choice should remain visible and citable.

Decision records are Loom's architectural decision records. They make precedent queryable. Future agents should be able to answer *"why did we choose X here?"* by reading the relevant decision record, not by archaeology.

A good decision record says:

- what was chosen
- why it was chosen
- what alternatives were rejected and why each was rejected
- what consequences follow
- what would cause this decision to be revisited

Keep the rejected alternatives section honest and specific. A decision record that only documents the winner is half a record.

Store decision records under `.loom/constitution/decisions/`. Use a numbered prefix (`decision-0001-...`, `decision-0002-...`) so precedent order is readable at a glance.

## Roadmap records

Use when the project needs durable strategic sequencing above the plan layer.

Roadmap is for themes and milestones — the strategic arc a future agent should inherit when scoping a new initiative. It is not for execution journaling and not for the live ticket queue.

A roadmap record answers:

- what themes is the project committing to over time
- what milestones mark meaningful advancement
- what the current chapter of work is
- what explicitly comes after the current chapter

Store roadmap records under `.loom/constitution/roadmap/`.

## Reach For This Subsystem When

- a choice should be citable later as precedent — write a decision record
- a constraint or principle needs to bind future work — amend `constitution:main`
- strategic sequencing should outlive the current plan — write a roadmap record

If the truth is live execution, it belongs in a ticket. If the truth is intended behavior, it belongs in a spec. If the truth is investigation, it belongs in research. The constitution subsystem exists for the policy-grade truths that shape all of the above.
