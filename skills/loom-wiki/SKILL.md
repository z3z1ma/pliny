---
name: loom-wiki
description: "Maintain the persistent, interlinked explanation layer for accepted understanding. Use when an answer, architecture concept, workflow, troubleshooting pattern, or operator reference should compound into durable knowledge rather than disappear into chat."
compatibility: Markdown-native, script-free Loom protocol.
metadata:
  skill_kind: owner-layer
  owns_layer: wiki
---

# loom-wiki

Wiki is Loom's accepted-explanation layer.

Use it when understanding should persist and compound.

## What This Skill Owns

- concept pages
- workflow pages
- reference pages
- codebase atlas pages for accepted repository or module structure
- inter-page linking
- wiki packets for synthesis passes
- page maintenance when accepted owner truth changes

Wiki explains settled understanding. It does not own policy, intended behavior,
live execution state, observed artifacts, or review verdicts.

Wiki packets use `kind: packet` with `packet_kind: wiki` under
`.loom/packets/wiki/`. They are wiki-owned synthesis contracts, not Ralph
implementation packets, and they do not use Ralph `verification_posture` unless
this skill later defines a wiki-specific field.

## What Makes Wiki Valuable

A good wiki page saves future agents from re-deriving the same understanding from scratch.

Wiki is where you promote:

- architecture explanations
- recurring answers
- workflow guides
- concepts worth naming
- troubleshooting knowledge
- references that summarize accepted patterns

## Use This Skill When

- another agent will likely need this explanation later
- the answer synthesizes several records
- a workflow changed materially
- the accepted architecture deserves a clear page
- critique or research produced durable understanding that should become easier to reuse
- a retrospective found accepted explanation that future agents should not have
  to re-derive

## Do Not Use This Skill When

- the truth is still unsettled
- the work belongs in the ticket or spec instead
- the page would be mere transcript residue
- you are trying to sneak policy or behavior-contract authority into a wiki page

## Wiki Page Families

This package ships templates for:

- concept pages
- workflow pages
- reference pages
- atlas pages

Those are enough to start.
You can add more page types if the project genuinely needs them.

## Wiki Procedure

1. choose the page family
2. gather the accepted source records and evidence
3. decide whether the work merits a wiki packet
4. write or update the page from accepted owner truth
5. add sources and related pages
6. link the page back into relevant tickets, critiques, or plans when useful

## Done Means

- accepted understanding now lives in a durable page
- the page cites the records or evidence that ground it
- the page links outward and inward where that helps navigation
- future agents can reuse the page instead of re-deriving it

## Read In This Order

Read immediately before creating or substantially changing wiki pages:

1. `references/wiki-philosophy.md` when deciding whether understanding belongs
   in wiki or another owner layer.
2. `references/page-types.md` when choosing concept, workflow, reference, or
   atlas shape.

Then read conditionally:

3. `references/wiki-write.md` when creating or substantially rewriting a wiki
   page from accepted owner truth.
4. `references/maintenance.md` when updating, staling, or superseding existing
   pages.
5. `references/wiki-audit.md` when auditing pages for staleness, duplication,
   broken sources, or misplaced authority.
6. `templates/index.md` only when creating or refreshing a wiki index.
7. The relevant page template only when writing that page type.
8. `templates/wiki-packet.md` only when a fresh synthesis pass is warranted.
