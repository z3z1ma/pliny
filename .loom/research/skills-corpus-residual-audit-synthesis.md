---
id: research:skills-corpus-residual-audit-synthesis
kind: research
status: concluded
created_at: 2026-05-03T00:56:36Z
updated_at: 2026-05-03T01:57:25Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  initiative:
    - initiative:skills-corpus-residual-protocol-sharpening-pass
  plan:
    - plan:skills-corpus-residual-protocol-sharpening-pass
external_refs: {}
---

# Question

Which findings from the fresh council review and the older user-supplied corpus
audit remain relevant after `plan:skills-corpus-template-grammar-safety-pass`?

# Why This Matters

The next refinement pass should not repeat already-closed work, but it should
preserve useful audit findings that still improve fresh-agent safety, template
copyability, route clarity, or owner-boundary discipline.

# Scope

Covered:

- Fresh council findings `NC2-001` through `NC2-007` over current `skills/` and
  `README.md` after commit `3e7905a`.
- User-supplied older audit actions 1 through 10, except action 6, which the user
  explicitly asked to ignore for now.

Excluded:

- Any recommendation to shorten skill activation descriptions.
- Runtime validators, command wrappers, schema engines, daemons, databases, MCPs,
  hidden helpers, or new canonical owner layers.

# Method

Compared the fresh council report against targeted reads and searches in current
`skills/` and `README.md`, including workspace/support tree guidance, status
lifecycle, route vocabulary, ticket template, Ralph packet template, packet
frontmatter, evidence template, claim coverage, workspace template, drive skill,
memory entity template, and tracked files under `skills/loom-records/templates`.

# Sources

- Council review result from session `ses_214c624c3ffe758GQd25PGvi2S`.
- User-supplied older audit excerpt in the current operator request.
- Current repository state at pushed commit `3e7905a`.
- `skills/loom-workspace/references/workspace-tree.md`
- `skills/loom-records/references/status-lifecycle.md`
- `skills/loom-records/references/route-vocabulary.md`
- `skills/loom-records/references/query-and-linking.md`
- `skills/loom-tickets/templates/ticket.md`
- `skills/loom-workspace/templates/workspace.md`
- `skills/loom-ralph/templates/ralph-packet.md`
- `skills/loom-records/references/packet-frontmatter.md`
- `skills/loom-evidence/templates/evidence.md`
- `skills/loom-records/references/claim-coverage.md`
- `skills/loom-drive/SKILL.md`
- `skills/loom-memory/templates/entities.md`
- `README.md`

# Evidence

Relevant and folded into the next plan:

- `NC2-001`: residual shorthand still treats retrospective / promotion follow-up
  as mostly wiki disposition in some surfaces.
- `NC2-002`: ticket template critique disposition does not locally fail closed for
  mandatory critique.
- `NC2-003`: route vocabulary omits constitution/initiative route-token decision
  despite doctrine routes; older audit also asks for clearer vocabulary boundaries
  and uniform `ask_user` policy.
- `NC2-004`: workspace/support lifecycle and query grammar still need tightening;
  older audit action 5 overlaps with `kind: workspace` lifecycle.
- `NC2-005`: ticket claim matrix lacks a local pointer to canonical status values.
- `NC2-006`: workspace template duplicates `repo_aliases` in frontmatter and body.
- Older audit action 3: Ralph packet template lacks a parent launch checklist, and
  packet frontmatter can state `consumed` versus accepted more directly.
- Older audit action 7: evidence template has validity fields, but source-state,
  exit-code/verdict metadata and negative-evidence examples can be made more
  visible.
- Older audit action 9: the optional outer-loop subagent transport section in
  `loom-drive/SKILL.md` is valuable but large enough to justify moving to a
  reference under the corpus's progressive-disclosure posture.
- Older audit action 10: minor exact-polish remains for memory heading levels,
  skill-root-relative template-path wording, and the tracked wording around
  `loom-records` template ownership.

Resolved or not folded:

- Older audit action 1 is mostly already resolved: README and workspace tree now
  name `.loom/support/drive-handoffs/` as lazy-materialized noncanonical support.
  Residual query/lifecycle grammar is folded into `ticket:wssupp4`.
- Older audit action 4 is already substantially resolved: the bootstrap here-doc
  warns to replace placeholders and uses a fail-closed placeholder instead of a
  save-ready `TBD` line. Minor placeholder copyability remains in the polish
  ticket only if current scans show a real save-ready defect.
- Older audit action 6 is intentionally ignored per operator instruction.
- `NC2-007` is not directly actionable as a file deletion because
  `git ls-files skills/loom-records/templates` returns no tracked files. The
  useful part is folded into the minor polish ticket: clarify wording if it still
  implies `loom-records` owns templates.
- The older duplicate-numbering note for `loom-drive/SKILL.md` appears resolved in
  the current file.

## Follow-up Validation After `ticket:wssupp4`

Validated against current corpus state after pushed commit `dd6d01c`.

Still relevant and added to the plan:

- `skills/loom-drive/references/checkpoint-resume-protocol.md` still says
  mandatory critique may be `not required with rationale`; this should fail
  closed because mandatory critique cannot be satisfied by `not_required`. Added
  `ticket:drivegt11`.
- `README.md` uses `memory` in a route table while
  `skills/loom-records/references/route-vocabulary.md` does not include a memory
  route token, and `stop` route examples do not consistently require a stop
  reason or condition. Added `ticket:drivegt11`.
- Shared packet templates and packet-frontmatter guidance still use only coarse
  `source_fingerprint.git_status_summary`, default packet template `network:
  unknown`, and a Ralph `child_write_scope.records` placeholder that can invite
  overbroad canonical-record writes unless the parent narrows it. Added
  `ticket:pktmeta12`.
- `skills/loom-research/references/source-handling.md` is still too thin for
  external/current-source freshness, provenance, access date, source quality, and
  recheck triggers. Added `ticket:srcmeta13`.

Still relevant but covered by existing tickets:

- Ralph launch checklist and `consumed` versus accepted-work wording remain in
  `ticket:ralphchk7`.
- Evidence freshness and challenge examples remain in `ticket:evfresh8`.
- Memory entity heading levels remain in `ticket:minpol10`.
- The direct critique template's unquoted scalar `review_target` placeholder is a
  minor copyability hazard; folded into `ticket:minpol10` rather than creating a
  separate ticket.

Stale or already resolved:

- The missing `kind: workspace` lifecycle claim was resolved by `ticket:wssupp4`.
- The retrospective memory read-order claim is stale; current
  `skills/loom-retrospective/SKILL.md` includes memory in promotion routing,
  default procedure, done criteria, and conditional read order.

# Rejected Options

- Do not create a runtime/schema validation pass. The findings are Markdown
  protocol-sharpening issues, and the repository direction rejects hidden runtime
  enforcement as protocol truth.
- Do not shorten skill descriptions in this pass. The operator explicitly asked to
  leave activation descriptions as-is for now.
- Do not create a ticket solely to delete the empty `skills/loom-records/templates/`
  directory because it has no tracked files to mutate.

# Null Results

- `git ls-files "skills/loom-records/templates"` returned no tracked files, so
  removing that empty directory would not produce a committed product-surface
  change.

# Conclusions

The next pass should be a minor residual protocol-sharpening pass, not a platform
or runtime expansion. Relevant findings are bounded, mostly template/reference
edits that reinforce route vocabulary, closure gates, workspace/support grammar,
packet launch readiness, evidence freshness, and small copyability polish.

# Recommendations

Create `initiative:skills-corpus-residual-protocol-sharpening-pass` and
`plan:skills-corpus-residual-protocol-sharpening-pass` with thirteen sequential
tickets:

1. route vocabulary, vocabulary-boundary, and `ask_user` decision grammar;
2. retrospective / promotion disposition wording;
3. mandatory critique fail-closed template guidance;
4. workspace/support lifecycle and query grammar;
5. drive/README route and checkpoint gate grammar;
6. claim matrix status guidance;
7. workspace template alias dedupe;
8. packet metadata defaults and child write authority;
9. Ralph launch checklist and consumed-versus-accepted wording;
10. evidence freshness and negative-evidence examples;
11. research source provenance and freshness guidance;
12. drive outer-loop transport reference extraction;
13. minor template/path polish.

# Open Questions

None for planning. Each ticket should still fail closed if implementation finds a
broader product-direction decision.

# Linked Work

- `initiative:skills-corpus-residual-protocol-sharpening-pass`
- `plan:skills-corpus-residual-protocol-sharpening-pass`
