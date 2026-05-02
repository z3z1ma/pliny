---
id: critique:scratchpad-external-concurrency-review
kind: critique
status: final
created_at: 2026-05-02T10:40:45Z
updated_at: 2026-05-02T10:40:45Z
scope:
  kind: repository
  repositories:
    - repo:root
review_target: ticket:233cfdeb
links:
  tickets:
    - ticket:233cfdeb
  packets:
    - packet:ralph-ticket-233cfdeb-20260502T102943Z
  evidence:
    - evidence:scratchpad-external-concurrency-validation
  plan:
    - plan:skills-corpus-protocol-sharpening
external_refs: {}
---

# Summary

Oracle critique of scratchpad avoidance, external-reference lifecycle,
file-first concurrency, and stale-record repair guidance implemented under
`ticket:233cfdeb`.

# Review Target

Reviewed the current working-tree diff for:

- `skills/loom-workspace/references/status-snapshot.md`
- `skills/loom-records/references/frontmatter.md`
- `skills/loom-records/references/semantic-link-usage.md`
- `skills/loom-records/references/repair-and-drift.md`
- `skills/loom-git/references/worktree-discipline.md`
- `ticket:233cfdeb`
- `packet:ralph-ticket-233cfdeb-20260502T102943Z`
- `evidence:scratchpad-external-concurrency-validation`

Required critique profiles:

- operator-clarity
- routing-safety

# Verdict

`pass`.

Initial oracle critique returned `pass_with_findings` with two low findings.
Parent resolved both, and final oracle re-check returned `pass` with no new
findings.

# Findings

## FIND-001: Scratchpad routing omitted critique

Severity: low
Confidence: medium
Disposition: resolved

Observation:

Initial scratchpad routing listed ticket, evidence, research, wiki, memory, spec,
plan, and constitution, but omitted critique. Adjacent pre-compaction guidance did
include critique, so this was not a hard contradiction.

Why it matters:

A future operator could have parked adversarial review notes or residual risks in
a scratchpad instead of a critique record.

Follow-up:

Resolved by adding `adversarial findings, verdicts, residual risks, or required
follow-up -> critique` to `skills/loom-workspace/references/status-snapshot.md`.

Challenges:

- `ticket:233cfdeb` ACC-001 before repair.

## FIND-002: Evidence searches were not replayable enough

Severity: low
Confidence: high
Disposition: resolved

Observation:

Initial evidence summarized targeted searches as labels such as `rg scratchpad
routing terms` instead of recording exact command patterns and scopes.

Why it matters:

The evidence was directionally useful but less replayable than a future reviewer
should expect for protocol-authority work.

Follow-up:

Resolved by replacing summarized search labels with exact `rg` command patterns,
file scopes, and refreshed diff stats in
`evidence:scratchpad-external-concurrency-validation`.

Challenges:

- Evidence replayability for `ticket:233cfdeb` ACC-001 through ACC-005 before
  repair.

# Evidence Reviewed

- Current working-tree status and diff.
- `git diff --check`, with no whitespace output.
- `ticket:233cfdeb` acceptance, evidence, and critique posture.
- `packet:ralph-ticket-233cfdeb-20260502T102943Z` contract and child output.
- `evidence:scratchpad-external-concurrency-validation`.
- Scratchpad routing in `skills/loom-workspace/references/status-snapshot.md`.
- External refs guidance in `skills/loom-records/references/frontmatter.md` and
  `skills/loom-records/references/semantic-link-usage.md`.
- Stale/latest-file repair guidance in
  `skills/loom-records/references/repair-and-drift.md`.
- Concurrency safety in `skills/loom-git/references/worktree-discipline.md`.

# Residual Risks

Validation remains structural and does not prove behavior in a real concurrent
editing incident.

# Required Follow-up

None for this ticket. The final corpus validation ticket remains responsible for
broader cross-surface review.

# Acceptance Recommendation

Close-ready. ACC-001 through ACC-005 are satisfied without introducing a
scratchpad record kind, new ledger, locks, daemons, helper-script requirement,
generated index, external tracker truth model, or latest-file-wins behavior.
