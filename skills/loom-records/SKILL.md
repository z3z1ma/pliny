---
name: loom-records
description: "Shared Loom record grammar: frontmatter, IDs, filenames, typed links, status lifecycles, claim coverage syntax, template use, and native validation patterns. Use when creating or reshaping any Loom artifact, reconciling references, deciding how to name a file, or validating records directly."
compatibility: Markdown-native, script-free Loom protocol.
metadata:
  skill_kind: shared-grammar
---

# loom-records

This skill is the shared grammar layer for Loom artifacts.

It is the place to consult when you need to know:

- how a Loom record should look
- how IDs and filenames should be shaped
- how typed links should work
- how evidence, critique, coverage, and external references should link without
  changing owner-layer authority
- how to validate and reconcile a set of records without a bundled script

## What This Skill Owns

- common YAML frontmatter conventions
- shared packet frontmatter conventions
- shared status lifecycle conventions
- claim and acceptance coverage conventions
- naming and ID conventions
- typed link conventions
- semantic link usage and relationship routing
- external reference provenance
- route vocabulary for checkpoint, resume, handoff, and route-readiness fields
- implementation reality boundaries for software work
- change class taxonomy for routing evidence and critique
- reference reconciliation discipline
- cross-record validation recipes
- repair and drift taxonomy

## The Core Principle

A Loom record should be legible to both:

- a fresh human reading the file directly
- a fresh agent searching the corpus with ordinary tools

That means:

- the file path matters
- the canonical ID matters
- the body headings matter
- the links field matters

## Use This Skill When

- you are creating a new record of any kind
- you are unsure about IDs or filenames
- you are updating links or reconciling references
- you need shared grammar for claim coverage, status, links, or validation
- you need to express record behavior directly in visible Markdown files

## Do Not Use This Skill When

- the next truth change belongs to a specific owner skill such as ticket,
  evidence, critique, wiki, spec, plan, research, initiative, or constitution
- you are trying to use grammar guidance as a substitute for owner-layer review
- you need an observed evidence artifact; use `loom-evidence` for the evidence record and
  return here only for shared naming, linking, or validation grammar

## Default Record Posture

Prefer records that are:

- explicit
- typed
- small enough to navigate
- rich enough to stand alone
- easy to grep
- easy to supersede honestly

## Native Creation Flow

1. choose the owning skill for the record kind
2. copy the appropriate template from that owner skill's `templates/` directory, when one exists
3. fill in frontmatter truthfully
4. fill in the required body sections
5. add typed links for real relationships
6. search for inbound and outbound references if this changes the graph

## Done Means

- the record has a stable canonical ID
- the filename agrees with the naming rule
- frontmatter and body both tell the truth
- typed links exist where they materially help graph navigation
- direct references remain reconciled

## Read In This Order

Read immediately for any non-trivial record creation or repair:

1. `references/frontmatter.md` when creating or repairing record metadata.
2. `references/packet-frontmatter.md` when creating or repairing packet
   frontmatter for Ralph, critique, or wiki packet support artifacts.
3. `references/naming-and-ids.md` when choosing IDs, filenames, or reference
   shapes.

Then read conditionally:

4. `references/status-lifecycle.md` when setting or auditing non-ticket
   statuses.
5. `references/claim-coverage.md` when requirements, acceptance, evidence, or
   critique need traceable claim IDs.
6. `references/query-and-linking.md` when searching graph edges or reconciling
   references.
7. `references/semantic-link-usage.md` when deciding whether a relationship
   belongs in `links:`, `depends_on`, coverage, evidence, critique, or
   external refs.
8. `references/implementation-reality.md` when code, tests, specs, and
   evidence need their truth boundaries separated.
9. `references/change-class.md` when tickets or packets need evidence,
   critique, or verification defaults.
10. `references/validation.md` when checking structural record health.
11. `references/repair-and-drift.md` when graph drift needs classification or
    safe repair.
12. `references/route-vocabulary.md` when checkpoint, resume, handoff, or
    route-readiness examples need shared route tokens.
13. `references/retrospective.md` when assimilating durable learning into owner
    layers.
14. `skills/loom-evidence/SKILL.md` when creating or validating evidence artifacts.
