---
id: ticket:1ypcbj0m
kind: ticket
status: closed
created_at: 2026-04-04T23:57:49Z
updated_at: 2026-04-19T23:34:12Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  initiative:
    - initiative:prove-core-loom-workflow
  plan:
    - plan:bootstrap-core-workflow-backlog
  spec:
    - spec:minimum-proven-core-workflow-surface
depends_on: []
---

# Summary

Exercise one bounded root-repository proof slice that goes through Ralph-style
execution, critique, wiki disposition, and ticket reconciliation so Loom's core
workflow is proven on a real shipped change rather than described only in prose.

# Context

`constitution:main` now explicitly calls for exercising real Ralph, critique,
and wiki packet flows using the rewrite's template-first, native-tool posture.

The repository has a strategic record chain for this work, but it still has no
real end-to-end proof slice. The best next step is to run one small change
through the full workflow and let later wrapper and validation work respond to
what that proof reveals.

# Why Now

This is the highest-value next ticket because it validates the protocol where
the repository is still relying mostly on doctrine, templates, and structure.
Without one real proof run, later wrapper and validation work would still be
guessing at the most important operator path.

# Scope

- choose one small root-repository target that benefits the shipped Loom bundle
- author one explicit bounded execution packet from the shipped packet template
  with clear scope, trust boundary, and allowed writes
- run one fresh execution child against that packet; the agent launches a fresh
  worker with the packet as context and does not rely on a custom orchestration
  script
- run one critique pass on the result, again agent-driven with normal tools
- either land wiki follow-through or record a truthful wiki-not-required
  outcome
- reconcile the resulting truth into the ticket ledger and any linked packet,
  critique, wiki, or evidence artifacts

# Non-goals

- do not try to prove every workflow family at once
- do not redesign packet architecture wholesale
- do not widen scope beyond `repo:root`
- do not claim success based only on a child assertion without durable evidence
- do not reintroduce helper-script assumptions into the proof flow

# Acceptance Criteria

- one small proof target is chosen and kept bounded
- one execution packet is authored with explicit scope, trust boundary, output
  contract, and allowed write set
- one fresh execution run lands or blocks explicitly without widening scope
- one critique pass and one wiki decision are recorded and linked back to the
  ticket
- the ticket's evidence, critique disposition, wiki disposition, and journal
  tell the truth about the outcome

# Execution Notes

1. Choose the smallest useful shipped change that can still exercise the full
   workflow.
2. Author the execution packet from the current Ralph packet template.
3. Run one bounded fresh child execution step using that packet as the contract.
4. Run critique on the resulting change.
5. Land wiki follow-through or record why wiki was unnecessary.
6. Reconcile the outcome into the ticket and linked artifacts using normal
   tools; perform the smallest honest validation needed for the changed
   surfaces.

# Evidence

No execution evidence exists yet.

Expected proof evidence for this ticket includes, as relevant to the chosen
target:

- a bounded packet under `.loom/packets/`
- a linked critique record under `.loom/critique/`
- a wiki page under `.loom/wiki/` or an explicit wiki-not-required decision in
  the ticket
- any supporting evidence artifacts under `.loom/evidence/`
- manual inspection of the changed records and any shipped product surfaces the
  proof target touches

# Critique Disposition

One critique pass is expected as part of this proof slice.

If the proof target somehow remains too trivial to justify critique, the ticket
must record that decision explicitly rather than implying critique happened.

# Wiki Disposition

Wiki follow-through is expected if the chosen target changes operator-facing
workflow understanding or leaves behind a reusable explanation another agent
would benefit from reading.

If the target ends up not requiring wiki follow-through, record that decision
explicitly instead of implying it.

# Dependencies

- `initiative:prove-core-loom-workflow`
- `spec:minimum-proven-core-workflow-surface`
- `plan:bootstrap-core-workflow-backlog`
- the existing Ralph, critique, wiki, workspace, and records skill surfaces

# Journal

- 2026-04-04: created `ticket:1ypcbj0m` as the first ready execution slice for
  the new core-workflow initiative.
- 2026-04-17: reconciled the ticket to the rewrite-era model: template-authored
  packets, YAML frontmatter, and `wiki`/`packets`/`evidence` vocabulary instead
  of the old `docs`/`runs`/`verification` and helper-script assumptions.
- 2026-04-19: closed per user confirmation that this ticket is completed.
