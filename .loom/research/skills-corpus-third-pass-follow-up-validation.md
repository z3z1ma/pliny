---
id: research:skills-corpus-third-pass-follow-up-validation
kind: research
status: concluded
created_at: 2026-05-03T06:20:11Z
updated_at: 2026-05-03T06:20:11Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  initiative:
    - initiative:skills-corpus-context-integrity-hardening-pass
  plan:
    - plan:skills-corpus-context-integrity-hardening-pass
external_refs: {}
---

# Question

Which third-pass audit claims remain valid against the current corpus and should
be added as tickets to the active skills-corpus hardening plan?

# Why This Matters

The user provided a new audit while `ticket:shipacc1` was in progress and asked
that valid non-skill-description claims become separate tickets in the current
plan before execution continues.

# Scope

Covered:

- User-provided third-pass audit claims in the current conversation.
- Current repository files under `skills/`, `README.md`, and the active Loom plan
  / initiative.
- The in-progress `ticket:shipacc1` working-tree edits were left intact and not
  treated as a reason to discard unrelated findings.

Excluded:

- Skill activation description length recommendations, per user instruction.
- Any recommendation that would add a runtime, daemon, database, command wrapper,
  schema engine, generated index, release ledger, or new owner layer.

# Method

Validated each claim with targeted reads and searches against the current corpus.
Claims were accepted only when the relevant file still lacked the proposed rule,
had the cited ambiguity, or still used the risky copy/template shape.

# Sources

- User-provided third-pass audit text in the current conversation.
- `skills/loom-tickets/references/readiness.md`
- `skills/loom-tickets/templates/ticket.md`
- `skills/loom-drive/references/tranche-decision-protocol.md`
- `skills/loom-workspace/references/routing.md`
- `skills/loom-records/references/validation.md`
- `skills/loom-bootstrap/references/06-filesystem-and-tooling.md`
- `skills/loom-research/templates/research.md`
- `skills/loom-research/references/source-handling.md`
- `skills/loom-records/references/packet-frontmatter.md`
- `skills/loom-ralph/templates/ralph-packet.md`
- `skills/loom-records/references/repair-and-drift.md`
- `skills/loom-workspace/references/problem-shaping.md`
- `README.md`
- Secondary-polish target files under `skills/loom-workspace`, `skills/loom-ralph`,
  `skills/loom-retrospective`, `skills/loom-critique`, and `README.md`

# Evidence

Validated findings:

- Ticket readiness guidance still lacks explicit route-readiness branches for
  `research`, `spec`, `plan`, `ticket`, `workspace_status`, `records_repair`,
  `continue`, and `stop`.
- Drive tranche route priority still lacks a `continue` row.
- Drive tranche route priority still groups `wiki` and `retrospective` in one row.
- Workspace routing still mixes route-token rows with skill-name-only rows.
- Record validation guidance lacks a saved-record placeholder scan and rule.
- Bootstrap filesystem/tooling still includes a copyable here-doc path containing
  `<slug>`.
- Research template `# Sources` remains prose-only despite stronger source
  handling guidance elsewhere.
- Shared packet frontmatter still shows empty `child_write_scope` lists in the
  common shape.
- Ralph packet launch checklist lacks hard gates for unresolved placeholders and
  ticket `next_route: ralph` authorization.
- Repair-and-drift orphan packet routing still routes too narrowly to Ralph.
- Problem shaping still says not to silently choose between ambiguous readings
  without the newer low-risk reversible assumption nuance.
- README support-surface table still omits workspace/harness metadata as support
  metadata.
- Workspace doctor still labels support-inclusive checks as canonical presence
  checks.
- Packet execution context guidance still permits `network: unknown` with only
  generic rationale language.
- Packet source fingerprint grammar still uses broad `clean|dirty|unknown`
  rather than machine-readable dirty categories.
- Retrospective read order still omits `loom-memory` even though retrospective can
  promote or prune memory support context.
- Critique packet template still has unquoted/generic placeholder shapes in some
  copyable fields.
- README routing table does not explicitly say it is introductory while
  `route-vocabulary.md` owns complete saved-field vocabulary.

# Rejected Options

- Do not change long skill activation descriptions in this pass; the user
  explicitly excluded skill-description changes.
- Do not bundle all findings into one broad ticket; the user requested a separate
  ticket for each recommendation or logical change.

# Null Results

None. Every non-description audit claim inspected was still materially valid.

# Conclusions

Create and append eighteen follow-up tickets to the current plan after
`ticket:shipacc1`, preserving sequential execution and existing evidence/critique
gates.

# Recommendations

Execute the new tickets sequentially through the existing plan discipline:
Ralph/fixer, evidence, mandatory critique, retrospective disposition, semantic
commit, and push.

# Open Questions

None for planning. Individual tickets may loop back if implementation or critique
shows the proposed change should be split further.

# Linked Work

- `initiative:skills-corpus-context-integrity-hardening-pass`
- `plan:skills-corpus-context-integrity-hardening-pass`
