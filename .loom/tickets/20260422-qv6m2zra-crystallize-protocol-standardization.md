---
id: ticket:qv6m2zra
kind: ticket
status: complete_pending_acceptance
change_class: protocol-authority
created_at: 2026-04-22T19:15:21Z
updated_at: 2026-04-22T20:30:58Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  evidence:
    - evidence:protocol-standardization-validation
  critique:
    - critique:protocol-standardization-review
external_refs: {}
depends_on:
  - ticket:ctx9p2ma
---

# Summary

Crystallize the next Loom standardization pass from the latest full-protocol
review.

# Context

The previous hardening pass made Loom more regular through implementation
reality, change classes, workspace scope aliases, stricter examples, and
stronger packet/evidence boundaries. The latest review identified remaining
precision gaps before the protocol surface should be considered stable.

# Why Now

Loom is now strong enough that loose examples, vague lifecycle states,
command-owned wiki behavior, or adapter drift would teach the wrong lessons.
This pass should reduce ambiguity without adding a runtime or new canonical
layers.

# Scope

- add successful completion lifecycle states for strategic records
- formalize claim matrix status vocabulary
- define acceptance dossier and optional strict-mode acceptance provenance
- move wiki write-mode behavior into a skill-owned reference
- add semantic link usage guidance
- clarify core persisted layers versus compositional workflows
- add adapter fixture expectations
- harden examples, including constitution stubs and high-risk evidence
- add a first proof-carrying PR example
- update docs, templates, and dogfood records to match

# Non-goals

- do not add a runtime, validator, dashboard, or required installer test suite
- do not make adapters own protocol semantics
- do not turn `links:` into a complex schema
- do not add new canonical owner layers

# Acceptance Criteria

- initiatives, plans, and roadmaps can complete without being marked retired
- claim matrix statuses have a documented vocabulary used by templates and examples
- `/loom-wiki` write mode routes to a skill-owned reference
- semantic link usage explains when to use links, depends_on, coverage,
  evidence support, critique challenges, and external refs
- docs distinguish compositional workflows from persisted owner layers
- acceptance gate names the acceptance dossier and optional strict-mode human
  decision fields
- examples are minimal and internally consistent, including constitution stubs or explicit
  partial-slice handling
- high-risk protocol-change example includes evidence
- adapter fixture expectations exist and are non-semantic
- proof-carrying PR example exists
- validation evidence and critique are recorded

# Coverage

Covers:
- ticket:qv6m2zra#CLAIM-001

# Local Claims

- CLAIM-001: The standardization pass clarifies lifecycle, acceptance,
  examples, and adapter boundaries without expanding Loom's
  ontology.

# Claim Matrix

| Claim | Evidence | Critique | Status |
| --- | --- | --- | --- |
| ticket:qv6m2zra#CLAIM-001 | evidence:protocol-standardization-validation | critique:protocol-standardization-review no blocking findings | supported |

# Execution Notes

Implement directly in the Markdown corpus. Keep command wrappers derivative
and keep examples small.

# Evidence

- evidence:protocol-standardization-validation

# Critique Disposition

Risk class: high

Required critique profiles:
- protocol-change
- operator-clarity

Findings:
- none

Status: completed

# Wiki Disposition

Top-level protocol docs and references should carry the durable explanation.
Dedicated wiki promotion is not required in this pass unless validation shows
the product source lacks the accepted explanation.

# Dependencies

Depends on `ticket:ctx9p2ma`, which introduced the prior precision hardening
surfaces this pass refines.

# Journal

- 2026-04-22T19:15:21Z: Created ticket and began implementation.
- 2026-04-22T19:53:00Z: Completed standardization pass, removed over-explicit
  taxonomy language from protocol surfaces, recorded validation evidence, and
  completed critique. Status moved to `complete_pending_acceptance`.
- 2026-04-22T20:30:58Z: Removed version and checklist guidance surfaces,
  including workspace declarations, skill metadata version fields, and deleted
  reference files. Re-ran structural and leakage scans.
