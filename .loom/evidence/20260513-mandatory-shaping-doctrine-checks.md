# Mandatory Shaping Doctrine Checks

ID: evidence:20260513-mandatory-shaping-doctrine-checks
Type: Evidence Dossier
Status: recorded
Created: 2026-05-13
Updated: 2026-05-13
Observed: 2026-05-13

## Summary

Validation dossier for the outer-loop shaping doctrine change. Observations cover
the authoritative skill-directory wording, absence of new symptom-specific MVP
language in shipped skill directories, aligned docs, and package/Markdown checks.

## Observations

- Observation: targeted scan of Core and Playbooks skill directories found no new
  `MVP`, `first plausible`, `fully concrete`, or `completely concrete` wording.
  - Procedure/source: `grep` over `loom-core/skills` and `loom-playbooks/skills`
    for `MVP|first plausible|fully concrete|completely concrete`.
  - Actual result: no files found in either skill tree.

- Observation: targeted scan of Core and Playbooks skill directories found no
  direct metaphor wording or over-literal operator phrasing from the correction
  pass.
  - Procedure/source: `grep` over `loom-core/skills` and `loom-playbooks/skills`
    for `hard engineering|hard thinking|hard choices|build/omit|what to build|what
    to leave out|conceptual integrity|conceptual-integrity|design-integrity|factory`.
  - Actual result: no files found in either skill tree.

- Observation: targeted scan of Core and Playbooks skill directories confirmed
  `data model` / `data-model` language is present where it describes the actual
  engineering concept.
  - Procedure/source: `grep` over `loom-core/skills` and `loom-playbooks/skills`
    for `data model|data-model`.
  - Actual result: matches appeared in `using-loom`, `shaping-with-humans`,
    delegation guidance, ticket creation/shape, plan creation/shape/slicing, spec
    guidance, `loom-idea-refine`, `loom-incremental-implementation`, and
    `loom-prototype-and-spike`.

- Observation: targeted scan of Core skills found systemic outer-loop language in
  model-visible doctrine and record-surface guidance.
  - Procedure/source: `grep` over `loom-core/skills` for `scope`,
    `system-shape`, `state-model`, `state relationship`, `coherence`, and
    `Concrete Ask Gate`.
  - Actual result: matches appeared in `using-loom`, `shaping-with-humans`,
    `how-loom-thinks`, delegation guidance, ticket creation/shape, plan
    creation/shape/slicing, and spec guidance.

- Observation: targeted scan of Playbooks skills found execution guard language in
  workflow entry points that can otherwise route quickly into implementation.
  - Procedure/source: `grep` over `loom-playbooks/skills` for `scope`,
    `system-shape`, `state`, `coherence`, `unshaped asks`, and `domain model`.
  - Actual result: matches appeared in `loom-idea-refine`,
    `loom-incremental-implementation`, `loom-frontend-ui-engineering`,
    `loom-prototype-and-spike`, and `loom-api-and-interface-design`.

- Observation: targeted scan of the updated human-facing docs found no new
  symptom-specific wording after the correction.
  - Procedure/source: `grep` over `README.md`, `PROTOCOL.md`, `ARCHITECTURE.md`,
    `loom-core/README.md`, and `loom-playbooks/README.md` for `MVP`,
    `first plausible`, `fully concrete`, and `completely concrete`.
  - Actual result: no files found.

- Observation: Markdown diff whitespace check passed after the latest wording
  revision.
  - Procedure/source: `git diff --check` from repository root.
  - Actual result: command exited successfully with no output.

- Observation: Core package smoke and pack checks passed after the latest wording
  revision.
  - Procedure/source: `npm --prefix loom-core run smoke` and
    `npm --prefix loom-core run pack:check` from repository root.
  - Actual result: smoke returned `ok: true`, registered seven ordered
    `using-loom` instruction files, exposed 11 Core skills, and pack dry-run
    completed with 65 files.

- Observation: Playbooks package smoke and pack checks passed after the latest
  wording revision.
  - Procedure/source: `npm --prefix loom-playbooks run smoke` and
    `npm --prefix loom-playbooks run pack:check` from repository root.
  - Actual result: smoke returned `ok: true`, confirmed Playbooks does not preload
    Core doctrine, exposed 25 Playbooks skills, and pack dry-run completed with 28
    files.

## Artifacts

- Tool outputs from the current session - command output showed passing
  `git diff --check`, smoke, and pack checks.

## What This Shows

- `ticket:20260513-mandatory-shaping-doctrine#ACC-001` - supports -
  authoritative `using-loom` skill prose now says ambiguity defaults to shaping,
  not implementation, and names scope, system-shape, state, and coherence choices
  as execution blockers when unresolved.

- `ticket:20260513-mandatory-shaping-doctrine#ACC-002` - supports -
  `shaping-with-humans` now defines a concrete-ask gate and mandatory shaping
  actions for unresolved design, scope, system-shape, state, evidence, and surface
  choices.

- `ticket:20260513-mandatory-shaping-doctrine#ACC-003` - supports - ticket,
  plan, spec, delegation, and implementation-playbook guidance now prevent fuzzy
  asks from becoming executable work before direction-setting choices are settled
  or owned by linked records.

- `ticket:20260513-mandatory-shaping-doctrine#ACC-004` - supports - updated docs
  restate the same mandatory shaping gate without adding symptom-specific MVP
  language.

- `ticket:20260513-mandatory-shaping-doctrine#ACC-005` - supports - repository
  Markdown/package checks passed after the skill and docs edits.

## What This Does Not Show

This evidence does not show improved behavior in a live eval run, only that the
shipped skill corpus now contains the mandatory systemic language and that package
checks still pass after revision. No adapter manifest validation was run because
no adapter manifest, hook, or bootstrap load-order files changed.

## Related Records

- `ticket:20260513-mandatory-shaping-doctrine` - scoped the doctrine change and
  acceptance claims.
