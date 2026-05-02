---
id: critique:command-route-wording-review
kind: critique
status: final
created_at: 2026-05-02T21:37:28Z
updated_at: 2026-05-02T21:37:28Z
scope:
  kind: repository
  repositories:
    - repo:root
review_target: "ticket:cmdroute diff 0458921..working-tree"
links:
  ticket:
    - ticket:cmdroute
  evidence:
    - evidence:command-route-wording-validation
  packet:
    - packet:ralph-ticket-cmdroute-20260502T213017Z
external_refs: {}
---

# Summary

Reviewed the command/adaptor route-wording hygiene for `ticket:cmdroute` after the
Ralph iteration removed optional-command route-peer phrasing from workspace and
wiki product guidance.

# Review Target

Current working-tree diff from baseline
`0458921db7377783651abd73a00159a6bbcf289d`, covering the ticket, evidence,
Ralph packet, and changed product guidance files.

Required critique profiles: `operator-clarity`, `routing-safety`, and
`records-grammar`.

# Verdict

`pass` - no findings.

# Findings

None - no findings.

# Evidence Reviewed

- `.loom/tickets/20260502-cmdroute-remove-command-route-ambiguity.md`
- `.loom/packets/ralph/20260502T213017Z-ticket-cmdroute-iter-01.md`
- `.loom/evidence/20260502-command-route-wording-validation.md`
- `skills/loom-records/references/route-vocabulary.md`
- `skills/loom-workspace/references/status-snapshot.md`
- `skills/loom-wiki/references/wiki-write.md`
- `skills/loom-wiki/references/wiki-audit.md`
- Current working-tree diff, including untracked packet and evidence records
- Exact route-peer wording search: no remaining product-surface matches in
  `skills/` or `README.md`
- Broad command/adaptor route wording search: remaining matches are transport,
  non-route doctrine, ordinary command examples, or non-runtime boundaries
- `git diff --check`: no output; parent follow-up with intent-to-add entries for
  new records also produced no output

# Acceptance Coverage

- `initiative:skills-corpus-council-precision-pass#OBJ-012`: covered; final
  wording no longer presents optional commands as route peers.
- `ticket:cmdroute#ACC-001`: covered; no remaining product guidance was found
  presenting optional commands as peers to owner layers or workflow routes.
- `ticket:cmdroute#ACC-002`: covered; remaining command/adaptor references are
  framed as invocation transport, non-route doctrine, ordinary command examples,
  or non-runtime boundaries.
- `ticket:cmdroute#ACC-003`: covered; changed wording aligns with
  `skills/loom-records/references/route-vocabulary.md` and introduces no new
  command/adaptor route token category.
- `ticket:cmdroute#ACC-004`: covered; evidence records before/after searches and
  `git diff --check`.
- `ticket:cmdroute#ACC-005`: covered by this critique result.

# Residual Risks

- Evidence is structural text-search evidence, not a proof against all future
  phrasing drift.
- The parent must include the new evidence and packet records in the ticket commit.

# Required Follow-up

None.

# Acceptance Recommendation

Close-ready after the ticket consumes this critique, records retrospective
disposition, and makes the acceptance decision.
