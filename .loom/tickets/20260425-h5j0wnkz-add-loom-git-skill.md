---
id: ticket:h5j0wnkz
kind: ticket
status: closed
change_class: protocol-authority
created_at: 2026-04-25T07:36:33Z
updated_at: 2026-04-28T18:47:27Z
scope:
  kind: repository
  repositories:
    - repo:root
links: {}
external_refs: {}
depends_on: []
---

# Summary

Add a `loom-git` skill that teaches Git branch, worktree, remote-ref, and diff
hygiene as an operational support workflow for Loom, especially Ralph.

# Context

The operator asked for more discipline around using Git with Loom so many
different repository shapes, multiple repos, and parallel Ralph workers can make
progress without stepping on one another. Existing Loom guidance already names
child write scope and packet execution context, but it does not yet teach how to
discover an integration baseline or prepare isolated branches and worktrees from
that baseline.

# Why Now

The current protocol direction emphasizes hardening transaction boundaries,
packet freshness, execution waves, and multi-worktree scope resolution. Git is
the practical implementation isolation surface for that work, but it must remain
subordinate to Loom owner records rather than becoming a shadow ledger.

# Scope

- Create `skills/loom-git/` as a flat, self-contained skill.
- Teach integration-baseline discovery, remote ref refresh when relevant, branch
  base hygiene, worktree lifecycle discipline, parallel Ralph isolation, and
  diff/commit/merge hygiene.
- Update Ralph guidance so packetized implementation work knows when to consult
  `loom-git`.
- Update the optional `/loom-work` wrapper only where it helps route execution
  into the new skill.
- Keep Git as an operational support workflow, not a new canonical owner layer.

# Non-goals

- Add a required Git helper script or CLI.
- Add a new Loom record kind or canonical layer.
- Define one global branch naming policy for every organization.
- Create a `/loom-git` command wrapper unless later usage proves it is needed.
- Change installer behavior beyond the existing skill-directory copy behavior.

# Acceptance Criteria

- `skills/loom-git/SKILL.md` has discoverable frontmatter and a practical main
  procedure.
- The skill includes references deep enough to guide branch, worktree, parallel
  Ralph, and diff/merge decisions without bloating the main skill file.
- `skills/loom-ralph/SKILL.md` directly mentions `loom-git` for Git isolation and
  packet execution context.
- Ralph packet contract/template guidance can record integration ref,
  integration commit, branch, and worktree provenance.
- Optional `/loom-work` routing mentions `loom-git` where a command wrapper would
  otherwise hide the new skill.
- Validation evidence records structural and reference checks.
- Critique is performed or explicitly recorded before acceptance.

# Coverage

Covers:
- ticket:h5j0wnkz#ACC-001

# Claim Matrix

| Claim | Evidence | Critique | Status |
| --- | --- | --- | --- |
| ticket:h5j0wnkz#ACC-001 | evidence:loom-git-skill-validation | critique:loom-git-skill-review | supported |

# Execution Notes

Create the skill as a protocol workflow/support skill with no templates. Git may
carry branch, worktree, diff, and commit provenance, but ticket, packet,
evidence, critique, and wiki remain the owner layers for Loom truth.

# Evidence

Expected:
- diff inspection
- `git diff --check`
- targeted search for `loom-git` references
- structural inspection of the new skill files

Recorded:
- evidence:loom-git-skill-validation

# Critique Disposition

Risk class: high

Required critique profiles:
- protocol-change
- operator-clarity

Findings:
- critique:loom-git-skill-review#FIND-001 - resolved
- critique:loom-git-skill-review#FIND-002 - resolved
- critique:loom-git-skill-review#FIND-003 - resolved
- critique:loom-git-skill-review#FIND-004 - resolved
- critique:loom-git-skill-review#FIND-005 - resolved
- critique:loom-git-skill-review#FIND-006 - resolved

Status: completed

# Wiki Disposition

No wiki page required for this ticket. The durable operator guidance belongs in
the shipped skill and references; a wiki page would duplicate product surface.

# Acceptance Decision

Accepted by: operator
Accepted at: 2026-04-28T18:47:27Z
Basis: Operator accepted the shipped `loom-git` skill after validation evidence and required critique showed all findings resolved.
Residual risks: None recorded for this closure.

# Dependencies

No hard upstream ticket dependency found.

# Journal

- 2026-04-25T07:36:33Z: Ticket opened and moved to `active` for the requested
  `loom-git` skill authoring pass.
- 2026-04-25T07:42:40Z: Added `loom-git`, revised Ralph and package framing,
  resolved critique findings about Git topology generality and parallel
  worktree metadata contention, and moved the ticket to
  `complete_pending_acceptance` pending operator acceptance.
- 2026-04-25T07:48:03Z: Finalized validation evidence after trailing-whitespace
  and stale-assumption checks.
- 2026-04-25T07:48:46Z: Removed the last hosted-Git-specific wording from the
  Git reference and re-ran targeted checks.
- 2026-04-28T18:47:27Z: Operator accepted the completed work and closed the ticket.
