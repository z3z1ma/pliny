---
id: ticket:ctx9p2ma
kind: ticket
status: complete_pending_acceptance
created_at: 2026-04-22T17:04:49Z
updated_at: 2026-04-22T17:25:00Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  critique:
    - critique:protocol-hardening-review
    - critique:final-protocol-precision-review
  evidence:
    - evidence:final-protocol-precision-validation
external_refs: {}
depends_on:
  - ticket:vairivh8
---

# Summary

Close the remaining protocol precision gaps found after the broad Loom
regularity pass.

# Context

The prior hardening pass established lifecycle, claim coverage, packet
freshness, context budgets, critique findings, command canonicality, and
golden fixtures. A follow-up review found smaller but important gaps in query
recipes, stale references, example rigor, workspace scoping, and software
implementation doctrine.

# Why Now

These gaps are mostly small, but Loom teaches future agents through its own
source corpus. Precision bugs and loose examples would become confusing
precedent in downstream repositories.

# Scope

- fix incorrect native query recipes and stale skill references
- make problem shaping discoverable without command wrappers
- clarify lazy `.loom/` tree materialization
- add implementation reality and change class guidance
- add a minimal workspace scope registry pattern
- harden examples into minimal consistent golden fixtures
- quarantine stale local draft material from current protocol truth
- normalize legacy dogfood JSON frontmatter in canonical owner records
- update related templates, rules, README, architecture notes, and dogfood
  records where needed

# Non-goals

- do not add a runtime, validator, dashboard, database, or mandatory helper
- do not add a new canonical layer for workspace scoping, examples, debug, or
  shipping
- do not copy review prose into product rules or skills

# Acceptance Criteria

- native recipes use correct ripgrep flags
- no product source reference points to the retired acceptance skill name
- fuzzy-request shaping is owned by a skill/reference, not only a command
- examples are described and shaped as golden protocol fixtures and traces
- example fixture links resolve or are explicitly non-links / stale
- evidence and packet examples satisfy the current minimal templates
- `.local/CONSTITUTION.md` is visibly archived and non-authoritative
- `.gitignore` uses the singular `.loom/memory` path
- legacy dogfood records in canonical owner directories use current YAML
  frontmatter
- records explain that source code owns implementation reality while specs own
  intended behavior
- tickets and packets can declare `change_class`
- workspace checks stay lightweight and human-readable
- workspace scope aliases are documented without becoming product truth

# Coverage

Covers:
- ticket:ctx9p2ma#CLAIM-001

# Local Claims

- CLAIM-001: The final hardening pass removes stale protocol ambiguity without
  expanding Loom into a runtime or adding new truth-owner layers.

# Execution Notes

Implement directly in the Markdown corpus and fixtures. Keep product text
self-contained and cold-agent oriented.

# Evidence

- evidence:final-protocol-precision-validation

# Critique Disposition

Risk class: medium

Required critique profiles:
- protocol-change
- operator-clarity

Findings:
- none

Status: completed

# Wiki Disposition

Update architecture and README summaries as needed. Dedicated wiki promotion is
not required unless a new accepted explanation is introduced beyond product
source.

# Dependencies

Depends on the prior regularity ticket because this pass tightens its
interfaces rather than replacing its direction.

# Journal

- 2026-04-22T17:04:49Z: Created ticket and began implementation.
- 2026-04-22T17:25:00Z: Implemented precision fixes, added missing doctrine
  and scope registry guidance, hardened examples, normalized legacy dogfood
  frontmatter, recorded validation evidence, and completed critique. Status is
  `complete_pending_acceptance`.
