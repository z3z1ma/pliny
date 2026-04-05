---
{
  "created_at": "2026-04-04T23:57:49Z",
  "id": "ticket:0003",
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
    ]
  },
  "repository_scope": {
    "kind": "repository",
    "repository_id": "repo:root"
  },
  "schema_version": 1,
  "status": "ready",
  "updated_at": "2026-04-04T23:58:09Z"
}
---

# Summary

Exercise one bounded root-repository proof slice that goes through Ralph-style
execution, critique, docs disposition, and ticket reconciliation so Loom's core
workflow is proven on a real shipped change rather than described only in prose.

# Context

`constitution:main` explicitly calls for exercising real Ralph, critique, and
docs packet flows against the current helpers and records.

The repository now has a strategic record chain for this work, but it still has
no real end-to-end proof slice. The best next step is to run one small change
through the full workflow and let later command and validation additions respond
to what that proof reveals.

# Why This Work Matters Now

This is the highest-value next ticket because it validates the protocol at the
point where the repository is still relying mostly on doctrine and structure.
Without one real proof run, later command and validation work would still be
guessing at the most important operator path.

# Scope

- choose one small root-repository target that benefits the shipped bundle;
  preferred targets are a single new core slash command or another similarly
  small operator-facing workflow improvement
- compile an explicit bounded execution packet with clear scope and allowed
  writes using `compile_packet.py` for scaffolding; populate content with
  standard editing tools
- run one fresh execution child against that packet -- this means the agent
  launches a headless invocation of itself with the compiled packet as context;
  no custom orchestration script is needed
- run one critique pass on the result, again agent-driven with standard tools
- either land docs follow-through or record a truthful docs-not-required
  outcome
- reconcile the resulting truth into the ticket ledger and any linked evidence
- use Python scripts only for structural validation, link checks, frontmatter
  scaffolding, and frontmatter-aware querying; all record population, content
  editing, searching, and workflow orchestration is agent work with normal tools

# Non-goals

- do not try to prove every workflow family at once
- do not redesign packet architecture or helper behavior wholesale
- do not widen scope beyond `repo:root`
- do not claim success based only on a child assertion without durable evidence
- do not build custom Python orchestration for Ralph launch, critique, or docs
  steps; the agent handles these directly with standard tools

# Acceptance Criteria

- one small proof target is chosen and kept bounded
- one execution packet is compiled with explicit scope, trust boundary, output
  contract, and allowed write set
- one fresh execution run lands or blocks explicitly without widening scope
- one critique pass and one docs decision are recorded and linked back to the
  ticket
- the ticket's status, verification section, docs disposition, and journal tell
  the truth about the outcome

# Implementation Plan

1. Choose the smallest useful shipped change that can still exercise the full
   workflow.
2. Use `compile_packet.py` to scaffold the execution packet; populate it with
   the agent's normal editing tools.
3. Run one bounded fresh child execution step by launching a headless agent
   invocation with the compiled packet as context -- no custom script needed.
4. Run critique on the resulting change, again agent-driven.
5. Land docs follow-through or record why docs were unnecessary.
6. Reconcile the outcome into the ticket and linked artifacts using standard
   tools; run `validate_record.py` and `check_links.py` for structural proof.

# Dependencies

- `initiative:prove-core-loom-workflow`
- `spec:minimum-proven-core-workflow-surface`
- `plan:bootstrap-core-workflow-backlog`
- the existing Ralph, critique, docs, and verification helper surfaces already
  shipped in this repository

# Risks / Edge Cases

- the chosen target may be too large for one clean proof slice
- packet freshness or write-boundary issues may appear once the flow is used for
  real
- critique and docs expectations may still need sharpening after the first run
- the workflow could block for procedural reasons rather than implementation
  reasons, which still needs truthful ledgering

# Verification

No execution evidence exists yet.

Expected proof evidence for this ticket includes, as relevant to the changed
surfaces:

- `python3 build/assemble-skills.py`
- `uvx ruff check build/ src/`
- `python3 build/shared/scripts/validate_record.py`
- `python3 build/shared/scripts/check_links.py`
- durable links to the packet, critique, docs, and verification artifacts

There is no conventional test suite in this repository, so structural and
workflow evidence are the main gate.

# Documentation Disposition

Docs follow-through is expected as part of the proof slice.

If the chosen target changes operator-facing workflow behavior, land the needed
docs update. If the target ends up not requiring docs, record that decision
explicitly instead of implying it.

# Journal

- 2026-04-04: created `ticket:0003` as the first ready execution slice for the
  new core-workflow initiative, with the explicit goal of proving one bounded
  Ralph -> critique -> docs path in `repo:root`.
- 2026-04-04: updated scope, non-goals, and implementation plan to reflect the
  principle that Python scripts are justified only for structural validation,
  link checks, and frontmatter work; all workflow orchestration including Ralph
  launch is agent-driven with standard tools.
