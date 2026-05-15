# Rename Loom Driver Agent

ID: ticket:20260515-loom-driver-rename
Type: Ticket
Status: closed
Created: 2026-05-15
Updated: 2026-05-15
Risk: high - renames a model-visible agent interface, shipped adapter surfaces, and existing Loom graph records.
Priority: high - prevents the newly introduced agent surface from settling under the wrong name.

## Summary

Rename the inner-loop coordination agent to Loom Driver across product files, adapter manifests, docs, filenames, record IDs, and Loom record prose. Single closure claim: the repo and Loom graph use the Driver name consistently, with no remaining legacy predecessor-name filenames or text occurrences.

## Related Records

- `spec:loom-driver-agent` - behavior contract after the rename.
- `ticket:20260515-loom-driver-agent` - original implementation ticket after the rename.
- `ticket:20260515-loom-driver-orchestration-tightening` - recent coordination-tightening ticket after the rename.
- `evidence:20260515-loom-driver-orchestration-tightening-validation` - validation baseline to rename and supersede with fresh validation.
- `audit:20260515-loom-driver-orchestration-tightening-audit` - prior review baseline after the rename.
- `packet:20260515T070409Z-loom-driver-rename` - execution packet and worker output for the rename.
- `evidence:20260515-loom-driver-rename-validation` - validation observations after the rename.
- `packet:20260515T071315Z-loom-driver-rename-audit` - Ralph review packet for the rename audit.
- `audit:20260515-loom-driver-rename-audit` - fresh clear audit for this rename.

## Scope

May change:

- Filenames and IDs containing the prior agent slug.
- Product source files, adapter manifests, docs, and Loom records containing the prior agent display name, slug, or code identifiers.
- Smoke checks and exported helper names that refer to the renamed agent.
- New evidence, audit, and packet records for this rename.

Must not change:

- The agent behavior contract beyond terminology.
- Loom Weaver behavior.
- Runtime infrastructure, package shape, or helper tooling beyond name references.
- Compatibility aliases or legacy-name shims unless a later ticket explicitly chooses them.

## Acceptance

- ACC-001: All filenames and record IDs use the Driver slug/name consistently.
  - Evidence: file search shows no predecessor-name filenames remain.
  - Audit: challenge whether renamed records still link to each other.

- ACC-002: Product source, adapter manifests, docs, and Loom records contain no predecessor-name text occurrences.
  - Evidence: content search after the last material change returns no matches for the predecessor terms.
  - Audit: challenge whether the search scope included hidden Loom records and untracked files.

- ACC-003: Core smoke and package checks pass with the Driver agent surface.
  - Evidence: `npm --prefix loom-core run smoke`, `npm --prefix loom-core run pack:check`, and `git diff --check` after the rename.
  - Audit: challenge whether checks cover prompt/TOML parity and packed agent files.

- ACC-004: Adapter validations touched by the rename pass.
  - Evidence: Claude Core plugin validation after the manifest and agent filename rename.
  - Audit: challenge whether any touched manifest was missed.

- ACC-005: Fresh evidence records the rename validation and a Ralph-backed audit challenges closure.
  - Evidence: new evidence and audit records for this ticket.
  - Audit: separate Ralph review before closure.

## Current State

Closed. The repo and Loom graph use the Driver name consistently across renamed files, record IDs, source text, adapter manifests, docs, prompt surfaces, and validation references. `evidence:20260515-loom-driver-rename-validation` supports `ACC-001` through `ACC-004`, and `audit:20260515-loom-driver-rename-audit` satisfies `ACC-005` with a clear verdict and no material findings.

Residual limits remain explicit: VCS metadata under `.git/` was not rewritten, live harness invocation was not tested, and adapter runtime behavior beyond static manifest/package validation remains unproven.

## Journal

- 2026-05-15: Created and activated ticket from operator request to rename the inner-loop coordination agent consistently across filenames, text, and Loom records.
- 2026-05-15: Consumed `packet:20260515T070409Z-loom-driver-rename`; renamed source, docs, adapter surfaces, and Loom records to Driver. Recorded validation in `evidence:20260515-loom-driver-rename-validation` and moved status to review for audit.
- 2026-05-15: Consumed `packet:20260515T071315Z-loom-driver-rename-audit`; recorded `audit:20260515-loom-driver-rename-audit` with clear verdict and no material findings. Closed ticket with metadata and runtime-validation residual limits explicit.
