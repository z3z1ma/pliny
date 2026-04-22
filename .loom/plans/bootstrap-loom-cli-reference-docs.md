---
id: plan:bootstrap-cli-reference-docs
kind: plan
status: active
created_at: 2026-04-01T17:44:27Z
updated_at: 2026-04-22T17:20:00Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  roadmap:
    - roadmap:bootstrap-the-markdown-first-protocol-corpus
  ticket:
    - ticket:z8h0g58e
external_refs: {}
---

# Purpose / Big Picture

Produce package-local CLI references for Loom's exposed helper scripts so operators can see each script's arguments, flags, output shape, and invocation patterns without reconstructing behavior from scattered examples or parser code.

This plan intentionally starts by inventorying the shared helper family at the source level, but the shipped documentation surface belongs inside the skill bundles under `references/scripts.md` and must use package-local `scripts/...` paths.

# Progress

- 2026-04-01: created the first plan, research note, and execution ticket for the CLI reference work.
- 2026-04-01: scoped the first slice to the shared helper family instead of the full `create_<kind>.py` family so the first deliverable stays small and parser-truth-grounded.
- 2026-04-01: published skill-local `references/scripts.md` files across the ten subsystem skills and validated the new canonical records plus their links.
- The package-local script references are now in place; the main remaining follow-up is whether to extend or deepen coverage for the `create_<kind>.py` family and any future helper additions.

# Surprises & Discoveries

- The repository already has useful invocation examples, but they are split across `worked-example-flow.md` and individual skill references rather than one script-centered reference.
- The shared helper CLIs are intentionally small and mostly consistent, which made it practical to add precise script references to each affected skill without changing helper behavior.
- The important packaging boundary is not where the helper source lives, but where the bundle exposes it. Package-facing docs needed to stay on the skill surfaces rather than in a rule appendix that pointed at source-only paths.

# Decision Log

- 2026-04-01: use the shared helper parser definitions as implementation truth for the inventory, but publish the resulting operator docs only through skill-local `references/scripts.md` files.
- 2026-04-01: treat this first pass as documentation and research work, not as a CLI redesign or standardization spec.
- 2026-04-01: keep the broader `create_<kind>.py` family as follow-up work rather than widening this first slice.

# Outcomes & Retrospective

The first slice has landed: the repository now has one durable research note, one linked execution ticket, and skill-local script references across the subsystem skills that expose bundled mini-CLIs.

This plan should stay active until the team decides whether the next pass expands into the `create_<kind>.py` family or other operator-facing helper docs.

# Context and Orientation

`constitution:main` and the active roadmap both say the next Loom work should deepen canonical records, exercise real workflows, and improve helper/operator clarity only where it is grounded in visible rules and shipped behavior.

The user's highest-confidence next step was better documentation for the exposed scripts, especially their flags, positional arguments, and invocation examples across the different script-path surfaces. That request is aligned with the roadmap gap: the helper layer exists, but its discoverability still depends too much on source inspection.

# Milestones

1. Seed canonical execution context.
   Create one plan, one research note, and one execution ticket for the CLI reference work.

2. Inventory parser truth.
   Read the shared helper scripts, capture arguments, flags, defaults, output shapes, and exposure patterns.

3. Publish package-local script references.
   Add `references/scripts.md` files to the relevant skills so bundled script docs live on the same surfaces that ship to operators.

4. Validate and reconcile.
   Validate the canonical records, confirm link integrity, and update the ticket with the outcome and remaining follow-up scope.

# Plan of Work

The work should proceed from durable state to source docs rather than the other way around.

First, create the canonical records so the investigation and execution truth have a stable home. Next, inventory the parser surface directly from the helper definitions and existing examples. Then publish package-local script references under each relevant skill so bundled operators read `scripts/...` and `references/...` paths instead of repo-source-only build paths. Finally, validate the records and leave clear follow-up boundaries for the broader `create_<kind>.py` family.

# Concrete Steps

1. Create and link the plan, research note, and execution ticket.
2. Inspect each shared helper parser and note positional arguments, flags, defaults, and output forms.
3. Write `references/scripts.md` files for the affected skills with script-by-script usage notes and package-local examples.
4. Update each skill's read order and reference list so the script reference is discoverable.
5. Validate the new records and reconcile the ticket status.

# Validation and Acceptance

- `validate_record.py` should pass for the new plan, research note, and ticket.
- `check_links.py` should confirm that the new record graph resolves cleanly.
- The skill-local script references should match the actual argparse surfaces in the bundled scripts.
- Any uncovered remaining scope should be left as explicit follow-up rather than implied completion.

# Idempotence and Recovery

The first slice is easy to resume because the work is partitioned by script.

If the docs pass is interrupted, a later actor can resume by rereading the plan, the research note, and the skill-local script references, then checking which script sections are still missing or stale. No hidden runtime state is involved.

# Artifacts and Notes

- Governing roadmap: `roadmap:bootstrap-the-markdown-first-protocol-corpus`
- Research note: `research:shared-script-cli-inventory`
- Execution ticket: `ticket:z8h0g58e`
- Published script references: `src/skills/*/references/scripts.md`
- Shared helper scope: `compile_packet.py`, `list_records.py`, `validate_record.py`, `resolve_scope.py`, `show_status.py`, `diagnose_workspace.py`, `check_links.py`, `link_records.py`, `create_verification.py`

# Interfaces and Dependencies

The authoritative parser surface comes from `build/shared/scripts/*.py`.

The source bundle exposes script paths under `src/skills/*/scripts/`, and the assembled harness surface exposes matching paths under `.opencode/skills/*/scripts/`. Package-facing docs should describe the bundled `scripts/...` surfaces without teaching operators to invoke source-only build paths.

Existing examples in `src/skills/loom-workspace/references/examples.md`, `src/skills/loom-tickets/references/examples.md`, and `src/rules/appendices/worked-example-flow.md` provide useful invocation patterns, but the skill-local script references should remain grounded in the parser definitions when those examples are incomplete.

# Linked Tickets

- `ticket:z8h0g58e` owns the live execution truth for this first CLI inventory slice.

# Risks and Open Questions

- The broader `create_<kind>.py` family may still need deeper follow-up examples beyond the initial script references.
- If skill-local copies ever diverge, the relevant skill-local script reference will need to explain that divergence explicitly rather than assuming mirroring.
- If the first appendix reveals inconsistent argument naming or output conventions, that follow-up should be handled as spec or helper work rather than being silently normalized in prose.

# Revision Notes

- 2026-04-01: created the plan to bootstrap a shared helper CLI reference starting from the parser-truth inventory and one linked execution ticket.
- 2026-04-01: replaced the rule-level appendix approach with skill-local `references/scripts.md` docs so the shipped operator surface stays package-local.
