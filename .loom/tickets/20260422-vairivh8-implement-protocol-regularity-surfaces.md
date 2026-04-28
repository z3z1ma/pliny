---
id: ticket:vairivh8
kind: ticket
status: closed
created_at: 2026-04-22T07:07:00Z
updated_at: 2026-04-28T18:47:27Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  roadmap:
    - roadmap:bootstrap-the-markdown-first-protocol-corpus
  critique:
    - critique:protocol-hardening-review
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
- move command-owned behavior into skill-owned references
- quarantine non-protocol utility skills from the default protocol skill set
- tighten ticket readiness defaults, claim namespacing, packet transaction
  boundaries, critique findings, evidence validity, packet lifecycle, and
  structural protocol checks

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
- critique guidance clearly covers code review as well as Loom artifact review
- critique guidance distinguishes direct artifact critique from packetized
  implementation review
- map/debug/spike/sketch/ship workflows are discoverable through skills and
  commands
- retrospective prevention routing is explicit
- `.loom/memory` is the dogfood memory path
- examples cover representative protocol routes
- always-on rules do not copy product-analysis prose into reusable agent
  instruction text
- deleting `commands/` no longer removes the canonical repair, status,
  acceptance, review pass-splitting, wiki audit, or problem-shaping procedures
- default ticket template starts as `proposed`
- cross-record claim references are namespaced
- Ralph packets distinguish child write scope from parent merge scope
- critique findings have stable IDs and disposition vocabulary
- evidence records capture environment, validity, limitations, supported
  claims, and challenged claims
- structural protocol check guidance exists
- local prose utility skills are outside the default protocol `skills/` tree
- at least one example includes before/after fixture slices

# Coverage

Covers:
- CLAIM-001

# Local Claims

- CLAIM-001: The protocol regularity surfaces are installed and tightened
  without turning commands, utilities, or workflow conveniences into new truth
  owners.

# Execution Notes

Implemented directly as source-corpus edits. No helper runtime or generated
schema was introduced.

# Evidence

- `git diff --check` passed.
- `git diff --cached --check` passed.
- `bash -n scripts/install-loom.sh` passed.
- Search for the old plural memory path returned no matches after the rename.
- Search for product-analysis leakage phrases in `rules/` returned no matches.
- Search for operator-language leakage in changed rules, skills, and commands
  returned no matches.
- `find skills -maxdepth 2 -name SKILL.md | sort` shows 17 default protocol
  skill surfaces after utility quarantine.
- `find commands -maxdepth 1 -type f -name '*.md' | sort` shows 19 command
  wrappers.
- `find examples -mindepth 2 -maxdepth 2 -name README.md | sort | wc -l`
  returned 5 protocol examples.

# Critique Disposition

Risk class: high

Required critique profiles:
- protocol-change
- operator-clarity

Findings:
- critique:protocol-hardening-review#FIND-001 — resolved
- critique:protocol-hardening-review#FIND-002 — resolved

Status: completed

# Wiki Disposition

Deferred from this ticket. Critique accepted the shape and findings were resolved;
the product source and examples carry the accepted explanation for closure. A
future wiki pass may document the regularized workflow map separately.

# Acceptance Decision

Accepted by: operator
Accepted at: 2026-04-28T18:47:27Z
Basis: Operator accepted the completed regularity pass after validation evidence and required critique showed all findings resolved.
Residual risks: Future wiki synthesis may still be useful, but it is not required for this ticket's closure.

# Dependencies

None.

# Journal

- 2026-04-22T07:07:00Z: Created after implementation to restore ticket-ledger
  truth for this broad protocol mutation. Status is `review_required` because
  high-risk protocol-surface changes need critique before acceptance.
- 2026-04-22T07:32:15Z: Clarified critique surfaces so code changes, behavior
  changes, and Loom artifacts are all explicit review targets. Kept always-on
  rule wording concise and operational.
- 2026-04-22T07:40:52Z: Clarified that critique packets are primarily for
  implementation/code review anchored by a ticket, governing context, and git
  diff. Direct critique of Loom artifacts does not require a packet by default.
- 2026-04-22T08:42:44Z: Added semantic hardening: skill-owned command
  procedures, proposed-by-default tickets, namespaced claim references,
  child/parent packet scopes, execution context, packet lifecycle, critique
  finding IDs, stronger evidence metadata, structural check guidance,
  optional utility quarantine, and one before/after fixture example.
- 2026-04-22T09:10:31Z: Ran packetized implementation critique and recorded
  `critique:protocol-hardening-review`. Follow-up tickets created for legacy
  dogfood directory reconciliation and fuller example fixtures.
- 2026-04-22T15:50:04Z: Re-reviewed command canonicality and thinned the
  remaining workflow wrappers (`map`, `debug`, `spike`, `sketch`, `ship`, and
  `work`) so they route to skill-owned procedures. Added
  `skills/loom-ralph/references/work-driver.md`.
- 2026-04-22T15:59:16Z: Reworked default skill `Read In This Order` sections
  to distinguish immediate baseline references from conditional references,
  preserving progressive disclosure with judgment instead of flat indexes.
- 2026-04-22T16:09:59Z: Resolved both critique findings: removed empty legacy
  dogfood directories and expanded every protocol example into fixture form.
  Moved ticket to `complete_pending_acceptance` pending final human acceptance.
- 2026-04-28T18:47:27Z: Operator accepted the completed work, deferred non-blocking
  wiki synthesis, and closed the ticket.
