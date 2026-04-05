---
{
  "created_at": "2026-04-04T23:57:49Z",
  "id": "ticket:0005",
  "kind": "ticket",
  "links": {
    "initiative": [
      "initiative:prove-core-loom-workflow"
    ],
    "plan": [
      "plan:bootstrap-core-workflow-backlog"
    ],
    "spec": [
      "spec:minimum-proven-core-workflow-surface"
    ],
    "ticket": [
      "ticket:0003"
    ]
  },
  "repository_scope": {
    "kind": "repository",
    "repository_id": "repo:root"
  },
  "schema_version": 1,
  "status": "proposed",
  "updated_at": "2026-04-04T23:58:09Z"
}
---

# Summary

Tighten structural validation and workspace diagnostics around packet shape,
scope, and canonical link integrity based on the concrete failures or
ambiguities exposed by the proved workflow path.

# Context

This repository has no conventional test suite. Structural validation,
diagnostics, and record integrity checks are the main guardrails.

The doctrine already defines fail-closed scope behavior, required packet fields,
and a minimum verification gate. The right next validation work is to mechanize
those published requirements more sharply where `ticket:0003` reveals real gaps.

# Why This Work Matters Now

Validation is most useful after one real workflow slice has been exercised.
Without that proof, helper changes would risk hardening the wrong abstractions.
With it, the repository can tighten the exact structural failures that most
threaten truthful bounded execution.

# Scope

- review packet, scope, and workspace validation behavior against the exercised
  proof flow
- add deterministic checks for existing doctrine requirements only
- improve diagnostics where current failures are hard to interpret
- keep changes in the shared helper layer and affected distributed scripts only
  as necessary
- new validation work must stay within the principle that Python scripts are
  justified only for structural integrity checks, frontmatter parsing, link
  resolution, and record scaffolding; any work that the agent can handle with
  standard tools should not become a new script

# Non-goals

- do not invent hidden ontology or acceptance scoring
- do not widen scope-resolution heuristics past fail-closed behavior
- do not fold unrelated helper cleanup into this ticket
- do not turn validation into a monolithic test runner
- do not add scripts for tasks the agent can already do with standard tools;
  validation scripts earn their place only through deterministic structural
  checks that benefit from reproducibility

# Acceptance Criteria

- execution-packet validation catches missing doctrine-required scope or
  write-boundary data when relevant
- workspace diagnostics and/or scope resolution make ambiguous ownership failures
  clearer
- canonical record and link validation remain clean for the backlog chain and any
  proof-flow artifacts
- any stricter checks that affect operator expectations are reflected in the
  visible docs or references that own those expectations

# Implementation Plan

1. Review the proof-flow evidence from `ticket:0003` and note structural
   failure modes or ambiguities.
2. Map each candidate validation change back to existing doctrine.
3. Implement the smallest checks and error-message improvements that close those
   gaps.
4. Rebuild distributed skill surfaces if shared helpers changed.
5. Re-run structural verification and reconcile the ticket truthfully.

# Dependencies

- `ticket:0003` should provide the main evidence for what to harden
- `ticket:0004` may reveal additional operator-facing failure modes if command
  entry points land first
- the shared helper layer under `build/shared/_loom_lib/` and
  `build/shared/scripts/`

# Risks / Edge Cases

- false positives if checks are stricter than the published rules
- hidden policy drift if helper logic starts deciding more than doctrine states
- scope creep across several helper files without one clear validation target

# Verification

Expected verification for this ticket includes:

- `uvx ruff check build/ src/`
- `python3 build/assemble-skills.py`
- `python3 build/shared/scripts/validate_record.py`
- `python3 build/shared/scripts/check_links.py`
- `python3 build/shared/scripts/diagnose_workspace.py`
- targeted manual reproduction of the specific failure modes this ticket claims
  to harden

# Documentation Disposition

Documentation follow-up is expected if this ticket materially changes operator
expectations for diagnostics, validation failures, or required packet fields.

If the work is limited to clearer messaging with no change in expected workflow,
skill references may be sufficient and a separate canonical docs record may not
be necessary.

# Journal

- 2026-04-04: created `ticket:0005` as the proposed hardening slice for packet,
  scope, and workspace validation after the first real workflow proof run.
- 2026-04-04: updated scope and non-goals to reinforce that new scripts are
  justified only for deterministic structural checks; the agent handles all
  other workflow tasks with standard tools.
