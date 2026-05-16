# Playbook Command Descriptions Use Source Descriptions

ID: ticket:20260516-playbook-command-descriptions-source
Type: Ticket
Status: closed
Created: 2026-05-16
Updated: 2026-05-16
Risk: medium - changes generated command metadata and smoke expectations around explicit Playbook macro surfaces.
Priority: high - operator explicitly rejected the generated explicitness prefix.

## Summary

Update Playbook command generation so generated command descriptions use each
Playbook's existing frontmatter description instead of adding an `Explicit optional
workflow macro for` prefix. The single closure claim is that OpenCode/Gemini
Playbook command metadata preserves the source descriptions verbatim while
Playbooks remain explicit invocation surfaces.

## Related Records

- `spec:playbook-explicit-macros#REQ-013` - defines the intended command-description behavior.
- `research:20260516-product-surface-scan` - identified the generated description polish issue.
- `spec:playbook-explicit-macros` - preserves the broader explicit macro behavior and no-autoactivation contract.
- `ticket:20260515-playbook-explicit-macro-docs-tests` - prior docs/tests ticket for explicit Playbook behavior.

## Scope

May change:

- `loom-playbooks/loom-playbooks.mjs`
- generated command TOML under `loom-playbooks/commands/*.toml`
- Playbooks smoke expectations if they currently require the generated explicitness prefix
- docs or test assertions only when they directly reference generated command descriptions
- this ticket, evidence, and audit records as needed

Must not change:

- Playbook source `description` frontmatter text unless a separate content-quality ticket owns that edit
- Playbook implicit/explicit invocation mechanics
- Core skill activation doctrine
- the safety framing inside macro prompt bodies unless implementation discovers a direct conflict and returns to spec/ticket shaping first
- unrelated Playbook workflow content

Durable execution context for the first Ralph run: read this ticket,
`spec:playbook-explicit-macros`, `loom-playbooks/loom-playbooks.mjs`, and a sample
generated command. Change only the command-description generation path and the
derived command files needed to make generated metadata align.

## Acceptance

- ACC-001: `readPlaybookMacroCatalog` or its description helper emits each macro
  description from the source Playbook frontmatter `description` without stripping
  `Use when` and without adding `Explicit optional workflow macro for`.
  - Evidence: source inspection of `loom-playbooks/loom-playbooks.mjs`.
  - Audit: review should challenge whether the metadata change accidentally
    reintroduces implicit Playbook activation or only changes explicit command
    descriptions.

- ACC-002: Regenerated `loom-playbooks/commands/*.toml` descriptions match their
  source Playbook descriptions and no generated command description contains the
  `Explicit optional workflow macro for` prefix.
  - Evidence: generated command diff plus targeted grep over `loom-playbooks/commands`.
  - Audit: same review lens as ACC-001.

- ACC-003: Playbooks remain explicit macros or explicit-only skills after the
  description change; command registration still avoids `config.skills.paths` for
  Playbooks.
  - Evidence: `npm --prefix loom-playbooks run smoke`,
    `npm --prefix loom-playbooks run pack:check`, and source inspection of smoke
    output or `inspectLoomPlaybooksBundle` behavior.
  - Audit: audit should inspect smoke output if any package behavior changes.

- ACC-004: Markdown and generated-file formatting checks pass.
  - Evidence: `git diff --check`.
  - Audit: included in any closure review; a separate audit may be waived if the
    diff is limited and smoke/pack checks pass.

## Current State

Closed. `loom-playbooks/loom-playbooks.mjs`
now returns source Playbook frontmatter descriptions verbatim from
`macroDescription`, and the smoke inspection now checks for the forbidden
`Explicit optional workflow macro for` generated prefix instead of treating
preserved `Use when` text as a failure. All 25 `loom-playbooks/commands/*.toml`
files were regenerated from source Playbook descriptions.

Validation run during the Ralph worker pass:

- `node loom-playbooks.mjs --write-gemini-commands` from `loom-playbooks`: wrote
  25 command files.
- `npm --prefix loom-playbooks run smoke`: passed; `registeredPlaybookSkillPaths`
  remained empty and `explicitDescriptionPrefixFailures` was empty.
- `npm --prefix loom-playbooks run pack:check`: passed; dry-run pack completed.
- Targeted generated-description grep over `loom-playbooks/commands/*.toml`: no
  command description contained `Explicit optional workflow macro for`.
- Targeted Node comparison over all 25 Playbook `SKILL.md` frontmatter
  descriptions and command TOML descriptions: passed.
- `git diff --check`: passed.

Validation is preserved in `evidence:20260516-product-surface-ticket-validation`.
Ralph review `audit:20260516-product-surface-ticket-review` found this ticket
closeable and did not identify command-description or explicitness-semantic drift.
Residual risk is limited to future source/command generation drift if commands are
edited by hand.

## Journal

- 2026-05-16: Created ticket from operator disposition of `research:20260516-product-surface-scan` recommendation 2; operator wants existing Playbook descriptions without the generated explicitness prefix.
- 2026-05-16: Set Status `active` before launching the first ticket-owned Ralph worker run.
- 2026-05-16: Ralph worker changed `macroDescription` to preserve source
  descriptions verbatim, updated smoke inspection to flag only the forbidden
  generated explicitness prefix, regenerated all 25 command TOML files, and
  validated with command regeneration, Playbooks smoke, Playbooks pack dry-run,
  targeted prefix grep, targeted source-vs-command description comparison, and
  `git diff --check`. Moved ticket to `review` because acceptance evidence is in
  place and audit/closure review is the remaining step.
- 2026-05-16: Recorded validation dossier
  `evidence:20260516-product-surface-ticket-validation` and Ralph review
  `audit:20260516-product-surface-ticket-review`; audit found this ticket
  closeable. Closed with ACC-001 through ACC-004 satisfied and no follow-up.
