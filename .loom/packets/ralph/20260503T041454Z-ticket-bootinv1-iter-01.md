---
id: packet:ralph-ticket-bootinv1-20260503T041454Z
kind: packet
packet_kind: ralph
status: consumed
target: ticket:bootinv1
mode: execution
change_class: protocol-authority
risk_class: high
style: reference-first
verification_posture: observation-first
iteration: 1
created_at: 2026-05-03T04:14:54Z
updated_at: 2026-05-03T04:16:21Z
scope:
  kind: repository
  repositories:
    - repo:root
child_write_scope:
  records:
    - None - child returns output only; parent reconciles ticket, evidence, critique, and packet status.
  paths:
    - skills/loom-bootstrap/references/01-core-identity.md
parent_merge_scope:
  records:
    - ticket:bootinv1
  paths:
    - .loom/tickets/20260503-bootinv1-promote-bootstrap-invariant.md
    - .loom/evidence/20260503-bootstrap-invariant-validation.md
    - .loom/critique/bootstrap-invariant-review.md
    - .loom/packets/ralph/20260503T041454Z-ticket-bootinv1-iter-01.md
source_fingerprint:
  git_commit: 1d8ad24e974de8cc9532aa71e28cda9d71e2eef0
  integration_remote: origin
  integration_ref: origin/main
  integration_commit: 1d8ad24e974de8cc9532aa71e28cda9d71e2eef0
  git_status_summary: clean
  git_status_detail: clean working tree at packet compile time
  compiled_from:
    - ticket:bootinv1
    - plan:skills-corpus-context-integrity-hardening-pass
    - initiative:skills-corpus-context-integrity-hardening-pass
    - research:skills-corpus-context-integrity-hardening-review
execution_context:
  branch: main
  push_remote: origin
  worktree: /Users/alexanderbutler/code_projects/personal/agent-loom
  isolation: none
  git_shared_metadata_mutations: forbidden
  destructive_commands: forbidden
  network: forbidden
context_budget:
  posture: normal
  max_source_files: 6
  max_excerpt_lines_per_file: 120
  avoid_full_file_reads: true
sources:
  initiative:
    - initiative:skills-corpus-context-integrity-hardening-pass
  research:
    - research:skills-corpus-context-integrity-hardening-review
  plan:
    - plan:skills-corpus-context-integrity-hardening-pass
  ticket:
    - ticket:bootinv1
  files:
    - skills/loom-bootstrap/references/01-core-identity.md
    - README.md
links: {}
---

# Mission

Add minimal first-contact bootstrap orientation to
`skills/loom-bootstrap/references/01-core-identity.md` for `ticket:bootinv1`.

# Bound Context

Bootstrap is the first doctrine a model may see after discovering Loom. The user
explicitly constrained this ticket: do not leak internal framing, marketing, viral
positioning, or external article references. Add only what a never-seen-Loom model
needs to orient to Loom's operational worldview.

Keep existing boundaries intact:

- layer ownership decides truth placement;
- tickets are the live execution ledger;
- packets are bounded support contracts;
- evidence observes;
- critique reviews;
- wiki preserves accepted explanation;
- filesystem records are the recovery surface.

# Source Snapshot

At baseline `1d8ad24`, `01-core-identity.md` already says Loom is mandatory when
present, Markdown-native, layer-owned, and optimized for cold recovery. It does
not yet use the concise invariant language from the README such as placement over
recency or the disposable-session/compounding-graph framing.

# Verification Targets

- `initiative:skills-corpus-context-integrity-hardening-pass#OBJ-001`
- `ticket:bootinv1#ACC-001`
- `ticket:bootinv1#ACC-002`
- `ticket:bootinv1#ACC-003`
- `ticket:bootinv1#ACC-004`

# Task For This Iteration

Make the smallest correct edit to `01-core-identity.md`:

1. Add a short operational invariant near the top of the reference.
2. Include only minimal first-contact orientation: placement/owner truth,
   recoverable records, disposable sessions/workers, and the graph path from
   packet to evidence/critique/reconciliation.
3. Avoid marketing, external references, internal strategy, or product-positioning
   language.
4. Preserve all existing authority and ownership boundaries.

Do not update Loom tickets, evidence, critique, or this packet. The parent will
reconcile those.

# Verification Posture

Observation-first. Before and after editing, report targeted observations for:

- placement/recency wording;
- disposable session/worker wording;
- graph recovery wording;
- absence of marketing/internal framing/external article references;
- unchanged owner-boundary claims.

Run `git diff --check` after editing.

# Stop Conditions

Stop and report `blocked` or `escalate` if the edit would require changing the
layer model, adding a new bootstrap reference, adding product marketing, or
introducing runtime/tooling assumptions.

# Output Contract

Return outcome, changed files, records changed, before/after observations,
`git diff --check` result, self-review, blockers/residual risks, and recommended
ticket state/next route.

# Working Notes

Parent compiled from clean `main` at `1d8ad24`.

# Child Output

Outcome: stop - bounded edit completed.

Files changed:

- `skills/loom-bootstrap/references/01-core-identity.md`

Records changed: None.

Before observations:

- Placement/recency: owner-layer truth existed; explicit `not newest` wording was
  missing.
- Disposable sessions/workers: disposable context windows existed; disposable
  workers were not explicit near the top.
- Graph recovery: recovery via visible files/durable graph existed; packet ->
  evidence/critique/reconciliation path was not summarized near first contact.
- Marketing/internal/external references: none observed.
- Owner-boundary claims: tickets, packets, evidence, critique, wiki boundaries
  already present.

After observations:

- Added a short operational invariant near the top.
- Placement over recency is now explicit.
- Disposable context windows and workers are now explicit.
- Recovery path now names packet, evidence, critique, reconciliation, and
  ticket-owned ledger.
- No marketing, external references, viral language, or README-style positioning
  added.
- Existing owner-boundary claims preserved.

Validation: `git diff --check` passed with no output.

Self-review: edit is intentionally small and slightly repetitive with later
recovery wording, but appropriate for first-contact orientation.

Blockers/residual risks: no blockers.

Recommendation: `review_required`; parent should reconcile ticket/evidence/packet
status, then route to critique for high-risk protocol-authority change.

# Parent Merge Notes

Accepted child output as in scope. Parent reviewed the diff, recorded evidence
`evidence:bootstrap-invariant-validation`, moved `ticket:bootinv1` to
`review_required`, and routed next to mandatory critique.
