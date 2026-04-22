---
name: loom-records
description: "Shared Loom record grammar: frontmatter, IDs, filenames, typed links, evidence records, template use, and native validation patterns. Use when creating or reshaping any Loom artifact, reconciling references, deciding how to name a file, or replacing old helper-script behavior with direct record work."
compatibility: Markdown-native, script-free Loom protocol.
metadata:
  loom_layer: shared-grammar
  protocol_version: "2.0"
---

# loom-records

This skill is the shared grammar layer for Loom artifacts.

It is the place to consult when you need to know:

- how a Loom record should look
- how IDs and filenames should be shaped
- how typed links should work
- how to create an evidence record
- how to validate and reconcile a set of records without a bundled script

## What This Skill Owns

- common YAML frontmatter conventions
- shared status lifecycle conventions
- claim and acceptance coverage conventions
- naming and ID conventions
- typed link conventions
- external reference provenance
- evidence record shape
- reference reconciliation discipline
- cross-record validation recipes

## The Core Principle

A Loom record should be legible to both:

- a fresh human reading the file directly
- a fresh agent searching the corpus with ordinary tools

That means:

- the file path matters
- the canonical ID matters
- the body headings matter
- the links field matters

## When To Use This Skill

- you are creating a new record of any kind
- you are unsure about IDs or filenames
- you are updating links or reconciling references
- you need to create an evidence artifact
- you are replacing helper-script behavior with native operations

## Default Record Posture

Prefer records that are:

- explicit
- typed
- small enough to navigate
- rich enough to stand alone
- easy to grep
- easy to supersede honestly

## Native Creation Flow

1. choose the owning skill
2. copy the right template
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

1. `references/frontmatter.md`
2. `references/status-lifecycle.md`
3. `references/claim-coverage.md`
4. `references/naming-and-ids.md`
5. `references/query-and-linking.md`
6. `references/validation.md`
7. `templates/evidence.md` when proof artifacts are needed
