---
{
  "created_at": "2026-04-01T17:44:27Z",
  "id": "ticket:z8h0g58e",
  "kind": "ticket",
  "links": {
    "plan": [
      "plan:bootstrap-cli-reference-docs"
    ],
    "research": [
      "research:shared-script-cli-inventory"
    ]
  },
  "repository_scope": {
    "kind": "repository",
    "repository_id": "repo:root"
  },
  "schema_version": 1,
  "status": "closed",
  "updated_at": "2026-04-19T23:34:12Z"
}
---

# Summary

Produce the first parser-truth inventory for Loom's shared helper CLIs and publish package-local skill references that explain their arguments, flags, outputs, and invocation patterns.

# Context

The repository already exposes a set of standalone scripts that behave like mini-CLIs, but the usage guidance is fragmented across skill references, one worked flow, and the parser code itself.

The user explicitly called out the need for a breakdown of script flags, positional arguments, meanings, and invocation examples across the different script surfaces. This ticket owns the first bounded slice of that work.

# Why This Work Matters Now

This is one of the clearest next-step improvements because it strengthens operator usability without inventing new workflow behavior.

It also helps turn the repository from a strong static corpus into a more usable protocol pack by making the helper layer legible without transcript archaeology or direct source inspection.

# Scope

- create a durable research note for the shared helper CLI family
- inspect the shared helper parser surface so the bundled docs stay grounded in implementation truth
- publish `references/scripts.md` files for the skills that expose those bundled scripts
- keep repository scope at `repo:root`

# Non-goals

- do not redesign helper behavior
- do not document every `create_<kind>.py` script in this first ticket
- do not widen into packet policy or helper implementation changes unless the docs uncover a concrete inconsistency
- do not pretend that skill-local path variants are separate CLIs when they are shared copies

# Acceptance Criteria

- `research:shared-script-cli-inventory` exists with reusable parser-truth findings for the shared helper family
- skill-local `references/scripts.md` files exist for the subsystem skills and document their bundled scripts in a script-centered way
- the new references explain arguments, flags, and package-local invocation patterns without sending operators to source-only build paths
- structural validation passes for the new plan, research note, and ticket
- workspace link validation remains clean after the new records are linked

# Implementation Plan

- create and populate the canonical plan, research note, and ticket so the work has durable ownership
- inspect the shared helper parsers and extract real argument, flag, default, and output details
- write skill-local script references that document the bundled CLIs where operators actually encounter them
- validate the new records and reconcile the ticket with the outcome and remaining follow-up scope

# Dependencies

- `plan:bootstrap-cli-reference-docs` provides the durable sequencing context for this work
- `research:shared-script-cli-inventory` provides the evidence base for the appendix content
- existing source examples in the workspace and packet appendices provide supplemental invocation examples but do not replace parser inspection

# Risks / Edge Cases

- future divergence between helper source and skill-local copies could stale the references if the shared-copy assumption stops being true
- some users may expect the broader `create_<kind>.py` family to be covered immediately, so the bounded shared-helper scope must stay explicit
- parser inspection captures the interface surface, but not every behavioral nuance; the appendix should avoid overclaiming beyond the visible CLI contract

# Verification

This ticket's first verification gate was structural and linkage-oriented rather than behavioral.

Executed evidence for the completed slice:

- `validate_record.py` passes for `plan:bootstrap-cli-reference-docs`, `research:shared-script-cli-inventory`, and `ticket:z8h0g58e`
- `check_links.py` reports no unresolved link issues after the new records were linked
- skill-local `references/scripts.md` files were written from direct parser inspection of the bundled helper definitions and create-script entrypoints

# Documentation Disposition

This ticket directly produced operator-facing source documentation through skill-local `references/scripts.md` files across the subsystem skills.

Follow-up documentation is still expected for the broader `create_<kind>.py` family, but that is outside this ticket's bounded scope and should be handled by separate follow-up work.

# Journal

- 2026-04-01: created `ticket:z8h0g58e` to own the first bounded CLI inventory slice after identifying shared helper discoverability as a high-leverage next step.
- 2026-04-01: linked the ticket to `plan:bootstrap-cli-reference-docs` and `research:shared-script-cli-inventory` so the work has durable strategy and evidence context.
- 2026-04-01: replaced the rule-level appendix approach with skill-local `references/scripts.md` files so bundled script docs stay on the shipped package surfaces.
- 2026-04-01: validated `plan:bootstrap-cli-reference-docs`, `research:shared-script-cli-inventory`, and `ticket:z8h0g58e`, confirmed workspace link integrity, and moved the ticket to `complete_pending_acceptance` pending review of the documentation shape.
- 2026-04-19: closed per user confirmation that this ticket is completed.
