---
name: loom-docs
description: Authoritative Loom documentation skill for durable explanatory records, documentation updates, operator guides, workflow guides, and architecture explanations grounded in evidence. Use when accepted system reality, workflows, or architecture need durable explanation for future operators or maintainers. Not for unsettled proposals, live execution journaling, or speculative future state.
compatibility: Designed for this Markdown-first Loom repository. Assumes repository-local scripts, canonical Markdown records, and harness-agnostic child launches resolved through `.loom/harness.md` profiles, harness self-discovery, or operator guidance.
metadata:
  author: agent-loom
  version: "0.1"
  loom-layer: documentation
---

# loom-docs

Documentation is the authoritative explanatory Loom layer.

Use this skill to write or update durable explanation after the accepted system shape is known well enough to describe truthfully.

If something materially changes how the system should be understood, it belongs in durable docs rather than in chat, PR prose, or one-off notes.

## Use This Skill When

- accepted reality changed and future operators need durable explanation
- a workflow, architecture, or concept now deserves a governed document
- another agent should be able to enter cold and understand the accepted system shape

## Do Not Use This Skill When

- the behavior is still unsettled or disputed
- the work is really a ticket journal, plan update, or review packet
- you only have proposed future state rather than accepted current truth

## What This Skill Governs

- documentation records
- documentation packet artifacts
- docs-update runs and their reconciliation back into the target doc

## Docs Are Distinct From Neighboring Loom Layers

- constitution is the durable project-policy layer
- research is the evidence and discovery layer
- initiatives provide strategic context
- specs provide declarative behavior contracts
- plans provide execution strategy
- tickets provide execution history and current work state
- critique provides adversarial review context
- docs explain accepted system reality and why it matters

## Default Docs Posture

- inspect existing docs before creating a new one
- prefer updating or superseding a governed explanation over fragmenting the docs surface
- keep the document high-level, explanatory, and dense with rationale, examples, boundaries, and verification context
- write for future human and AI readers who were not present during the implementation
- describe accepted or completed reality rather than plans that have not landed

## Before You Write

1. inspect the current docs surface first so you update the right document
2. confirm the audience and the exact accepted truth that needs explanation
3. gather the truth sources and verification basis before drafting
4. resolve scope if ownership across repositories or worktrees is unclear

## Execution Playbook

1. create a new doc only when no existing governed doc should own the explanation
2. if you create one, populate the body immediately; a new doc shell is not operator-ready
3. update or supersede existing docs instead of fragmenting the surface whenever possible
4. link truth sources and verification refs after the explanation is grounded in accepted evidence
5. compile a docs packet only when a fresh docs-maintainer run is the right next step
6. create verification records for docs-supporting evidence when those should enter the durable graph
7. validate the doc and check link integrity before treating the explanation as citeable

If a docs-maintainer pass completes without a durable docs revision or leaves a thin recap that cannot stand on its own, treat that as failed documentation work.

## How To Use The Scripts

Read `references/scripts.md` for the bundled CLI surface, including argument meanings and example invocations.

- `scripts/docs.py create`: use when a new governed explanation is needed in `.loom/docs/`
- `scripts/docs.py create`: after running it, populate the body immediately; the command only creates the shell
- `scripts/docs.py packet`: use when you want a packet scaffold under `.loom/runs/docs/` for a fresh-context docs pass
- `scripts/docs.py link`: use to add or remove truth-source and verification refs after the explanation is grounded
- `scripts/docs.py verify`: use when docs work or its supporting checks produce durable evidence

## What Good Looks Like

- a future reader can understand the accepted system shape without hidden context
- the audience is obvious from the prose
- the explanation is grounded in accepted truth and linked evidence
- examples, rationale, and boundaries are concrete enough to be useful
- the docs surface becomes clearer rather than more fragmented

## Failure Conditions

Treat docs work as failed or incomplete when:

- the child leaves no durable docs revision
- the resulting doc overclaims what the evidence supports
- the update fragments the docs surface instead of updating the governed explanation
- the document reads like a recap for people already present rather than a self-contained explanation for future readers

## Done Means

- the right governed doc owns the accepted explanation
- the prose is grounded in accepted truth and linked evidence
- the docs surface is clearer rather than more fragmented
- frontmatter and downstream links are explicit enough for later workspace validation

## Read In This Order

1. `references/schema-docs.md`
2. `references/scripts.md`
3. `references/docs-invocation.md`
4. `references/examples.md`

## References

- `references/schema-docs.md`
- `references/scripts.md`
- `references/docs-invocation.md`
- `references/examples.md`
