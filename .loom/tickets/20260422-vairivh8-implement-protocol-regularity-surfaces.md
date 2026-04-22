---
id: ticket:vairivh8
kind: ticket
status: review_required
created_at: 2026-04-22T07:07:00Z
updated_at: 2026-04-22T07:07:00Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  roadmap:
    - roadmap:bootstrap-the-markdown-first-protocol-corpus
external_refs: {}
depends_on: []
---

# Summary

Implement the first pass of Loom protocol regularity surfaces from the April
2026 product direction.

# Context

The user supplied a detailed opportunity map for sharpening Loom without
turning it into a runtime or external platform. The active roadmap already
owned this direction, but the source corpus needed concrete rule, skill,
template, command, example, and dogfood-record updates.

# Why Now

The repository had the strong Markdown-native core, but several repeated
workflow shapes were still implicit. Making lifecycle, coverage, packet
freshness, critique profiles, workflow routes, examples, and memory naming
explicit improves cold-agent recovery before deeper implementation work starts.

# Scope

- add shared lifecycle and claim coverage references
- update templates for coverage, evidence support, external references, packet
  freshness, context budget, execution waves, and critique disposition
- add map, debug, spike, sketch, and ship workflow skills and command wrappers
- add critique profiles and retrospective prevention routing
- add protocol examples
- rename dogfood memory storage to singular `.loom/memory`
- keep always-on rule changes concise and operational

# Non-goals

- do not add a runtime, daemon, CLI, MCP, dashboard, or hidden helper ontology
- do not rewrite every historical dogfood ticket, plan, or research record in
  this pass
- do not claim final acceptance before critique

# Acceptance Criteria

- shared lifecycle guidance exists for non-ticket records
- claim coverage can trace acceptance IDs through tickets, packets, evidence,
  and critique
- Ralph packets carry source fingerprint and context budget fields
- plans can express execution waves
- critique supports named risk profiles
- map/debug/spike/sketch/ship workflows are discoverable through skills and
  commands
- retrospective prevention routing is explicit
- `.loom/memory` is the dogfood memory path
- examples cover representative protocol routes
- always-on rules do not copy product-analysis prose into reusable agent
  instruction text

# Coverage

Covers:
- CLAIM-protocol-regularity-surfaces

# Execution Notes

Implemented directly as source-corpus edits. No helper runtime or generated
schema was introduced.

# Evidence

- `git diff --check` passed.
- Search for the old plural memory path returned no matches after the rename.
- Search for product-analysis leakage phrases in `rules/` returned no matches.
- `find skills -maxdepth 2 -name SKILL.md | sort` shows 19 skill surfaces.
- `find commands -maxdepth 1 -type f -name '*.md' | sort` shows 19 command
  wrappers.
- `find examples -mindepth 2 -maxdepth 2 -name README.md | sort | wc -l`
  returned 5 protocol examples.

# Critique Disposition

Risk class: high

Required critique profiles:
- protocol-change
- operator-clarity

Status: required

# Wiki Disposition

Deferred until critique accepts the shape. A later wiki pass should document
the regularized workflow map once review findings are resolved.

# Dependencies

None.

# Journal

- 2026-04-22T07:07:00Z: Created after implementation to restore ticket-ledger
  truth for this broad protocol mutation. Status is `review_required` because
  high-risk protocol-surface changes need critique before acceptance.
