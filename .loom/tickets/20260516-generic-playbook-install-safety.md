# Generic Playbook Install Safety

ID: ticket:20260516-generic-playbook-install-safety
Type: Ticket
Status: closed
Created: 2026-05-16
Updated: 2026-05-16
Risk: medium - changes install guidance around Playbook exposure and could affect users of generic skill-directory setups.
Priority: high - prevents reintroducing implicit Playbook activation through raw skill-tree instructions.

## Summary

Tighten generic install guidance so users are not told to expose the raw Playbook
skill tree as ordinary model-invoked skills unless the harness respects explicit-only
metadata or the user is deliberately invoking Playbooks. The single closure claim is
that generic docs preserve Core-first natural routing and make raw Playbook exposure
safe or clearly qualified.

## Related Records

- `research:20260516-product-surface-scan` - identified the generic install sharp edge.
- `spec:playbook-explicit-macros` - defines Playbooks as explicit macros or explicit-only skills.
- `knowledge:playbook-activation-tests-procedure` - explains why natural prompts should fail on any Playbook invocation.
- `CLAUDE.md` - contributor-facing integration acceptance guidance for Core-first natural prompts.

## Scope

May change:

- `INSTALL.md`
- root and package READMEs where they describe generic Playbook exposure
- harness-specific fallback wording that mentions exposing `loom-playbooks/playbooks`
- this ticket, evidence, and audit records as needed

Must not change:

- package entrypoints or native manifests
- Playbook source behavior or command generation
- Core skill activation doctrine
- harness-specific install instructions that are already explicit command or explicit-only skill surfaces, except for narrow clarifying wording

Durable execution context for the first Ralph run: read this ticket,
`spec:playbook-explicit-macros`, `INSTALL.md`, root/package READMEs, and any docs
that mention `loom-playbooks/playbooks`. Keep changes to documentation wording unless
source inspection reveals a direct stale reference in a test or fixture.

## Acceptance

- ACC-001: Generic local setup no longer presents `loom-playbooks/playbooks` as a
  raw ordinary skill path without a safety qualifier. It should state that raw
  Playbook exposure is appropriate only for harnesses that honor explicit-only
  metadata or when Playbooks are deliberately invoked as explicit workflow lenses.
  - Evidence: source inspection of `INSTALL.md` Generic Local Setup and targeted
    grep for `loom-playbooks/playbooks` in docs.
  - Audit: review should challenge whether the wording still lets users recreate
    implicit Playbook autoactivation.

- ACC-002: Harness fallback wording that still names `loom-playbooks/playbooks`
  preserves Core-first natural routing and does not suggest Playbooks should
  auto-load from ordinary prompts.
  - Evidence: source inspection of Cursor/generic fallback sections and package
    READMEs after edits.
  - Audit: same review lens as ACC-001.

- ACC-003: Docs continue to describe supported explicit Playbook surfaces for
  OpenCode, Gemini, Claude, Cursor, and Codex accurately without claiming a uniform
  command syntax across harnesses.
  - Evidence: source inspection against `spec:playbook-explicit-macros` and relevant
    install sections.
  - Audit: review should challenge unsupported harness claims if any wording changes.

- ACC-004: Documentation formatting checks pass.
  - Evidence: `git diff --check`; package smoke/pack checks only if implementation
    changes package files or generated command surfaces.
  - Audit: separate audit may be waived if the diff is docs-only and acceptance is
    supported by source inspection.

## Current State

Closed. The first Ralph worker run updated `INSTALL.md` and
`loom-playbooks/README.md` so generic raw Playbook exposure is qualified: expose
`loom-playbooks/playbooks` only when the harness honors explicit-only metadata or
when the user will deliberately invoke Playbooks. Cursor fallback wording now keeps
Core as the natural prompt route and treats raw Playbook exposure as explicit-only
or deliberate-invocation setup.

Validation completed: searched Markdown docs for `loom-playbooks/playbooks` and
natural autoactivation phrasing (`auto-load`, `auto-trigger`, `natural prompt`,
`natural-language`, `autoactivation`, `auto-activation`), inspected remaining
occurrences in scoped docs plus `ARCHITECTURE.md`, and ran `git diff --check`
successfully. Remaining occurrences are intentional package-shape references or
now have explicit safety qualifiers. Validation is preserved in
`evidence:20260516-product-surface-ticket-validation`. Ralph review
`audit:20260516-product-surface-ticket-review` found this ticket closeable; it
noted residual risk that external harness behavior is not proven, but the docs now
qualify that risk rather than overclaiming it.

## Journal

- 2026-05-16: Created ticket from operator disposition of `research:20260516-product-surface-scan` recommendation 3.
- 2026-05-16: Set Status `active` before launching the first ticket-owned Ralph worker run.
- 2026-05-16: Ralph worker updated generic install and package README wording for raw Playbook exposure safety, verified remaining `loom-playbooks/playbooks` and natural autoactivation phrasing, ran `git diff --check` successfully, and moved the ticket to `review` for closure/audit disposition.
- 2026-05-16: Recorded validation dossier
  `evidence:20260516-product-surface-ticket-validation` and Ralph review
  `audit:20260516-product-surface-ticket-review`; audit found this ticket
  closeable with residual external-harness risk already qualified by the docs.
  Closed with ACC-001 through ACC-004 satisfied and no follow-up.
