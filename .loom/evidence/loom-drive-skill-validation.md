---
id: evidence:loom-drive-skill-validation
kind: evidence
status: recorded
created_at: 2026-04-28T20:33:07Z
updated_at: 2026-04-28T21:55:53Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  tickets:
    - ticket:odpl001
  specs:
    - spec:objective-driven-parent-loop
  packets:
    - packet:ralph-ticket-odpl001-20260428T202948Z
external_refs: {}
---

# Summary

Structural validation for the first `loom-drive` skill implementation. The
observations support that the skill surface exists, exposes read-order guidance,
is discoverable from workspace routing, and states no-script/no-daemon/no-new-layer
constraints as prohibitions rather than requirements.

# Procedure

The parent inspected the Ralph child output, read the changed files, and ran
targeted structural checks after the child returned.

Commands and searches performed:

```text
Glob skills/loom-drive/**
Grep "^name: loom-drive|^description:" skills/loom-drive/SKILL.md
Grep "references/drive-loop\.md|templates/outer-loop-handoff\.md" skills/loom-drive/SKILL.md
Grep "loom-drive" skills/loom-workspace/references/routing.md
Grep "required script|required.*daemon|required.*product CLI|required.*dashboard|required.*hidden database|required.*poller|new canonical layer|new truth layer" skills/loom-drive/*.md
Grep "tickets are the only live execution ledger|parent reconciles|transport only|canonical records retain truth ownership|parent review and reconciliation|Workflow coordination is not truth ownership" skills/loom-drive/*.md
git diff --check
```

# Artifacts

Observed changed product files:

- `skills/loom-drive/SKILL.md`
- `skills/loom-drive/references/drive-loop.md`
- `skills/loom-drive/references/continuity-contract.md`
- `skills/loom-drive/references/tranche-decision-protocol.md`
- `skills/loom-drive/references/checkpoint-resume-protocol.md`
- `skills/loom-drive/templates/outer-loop-handoff.md`
- `skills/loom-workspace/references/routing.md`

Observed structural outputs:

```text
Glob skills/loom-drive/**
-> skills/loom-drive/templates/outer-loop-handoff.md
-> skills/loom-drive/references/drive-loop.md
-> skills/loom-drive/SKILL.md

Grep "^name: loom-drive|^description:" skills/loom-drive/SKILL.md
-> line 2: name: loom-drive
-> line 3: description: "Drive a high-level chat objective through Loom's existing owner records, bounded tickets, Ralph/local execution, evidence, critique, wiki, and continuation decisions. Use when the user wants an outcome advanced across multiple steps without manually prompting every downstream ticket, while preserving tickets as the live execution ledger and avoiding scripts, daemons, or new truth layers."

Grep "references/drive-loop\.md|templates/outer-loop-handoff\.md" skills/loom-drive/SKILL.md
-> lines 117, 133, 163, and 180 reference the drive-loop reference and handoff template.

Grep "loom-drive" skills/loom-workspace/references/routing.md
-> line 22: `loom-drive`

Grep forbidden implication pattern under skills/loom-drive/*.md
-> 6 matches, all prohibition/constraint wording rather than requirements.

Grep owner/transport/parent authority pattern under skills/loom-drive/*.md
-> 5 matches confirming parent reconciliation, transport-only subagents, and owner-truth boundaries.

git diff --check
-> no output

Product-facing wording audit after activation-description feedback:

```text
Grep "daemon|poller|hidden database|new canonical layer|new truth layer|external runtime|script, daemon|without a daemon|transcript memory|chat memory|compaction|helper-script" skills/loom-drive/*.md
-> no matches

Grep "^description:.*(new truth layer|new canonical layer|daemon|poller|hidden database|runtime|helper-script|truth ledger|execution ledger|new ledger)" skills/*.md
-> no matches

Grep "new truth layer|new canonical layer|hidden database|background poller|external poller|without creating a new ledger|truth ledger|execution ledger|helper-script|transcript memory|chat memory|compaction|daemon|poller" skills/*.md
-> remaining matches are limited to ordered bootstrap doctrine references, where
   they define Loom's core truth-boundary vocabulary.
```

Final post-iteration checks:

```text
Glob skills/loom-drive/**
-> SKILL.md, references/drive-loop.md, references/continuity-contract.md,
   references/tranche-decision-protocol.md,
   references/checkpoint-resume-protocol.md, templates/outer-loop-handoff.md

Grep "checkpoint-resume-protocol|tranche-decision-protocol|continuity-contract|drive-loop|outer-loop-handoff" skills/loom-drive/SKILL.md
-> found all read-order references and the handoff template.

Grep "repair route|required checkpoint|checkpoint fields are current|failed gates do not block their own repair routes|Route federation" skills/loom-drive/*.md
-> found repair-route, checkpoint-freshness, and route-federation guidance.

Grep forbidden implication pattern under skills/loom-drive/*.md
-> matches are prohibition/constraint wording, not requirements.

git diff --check
-> no output
```
```

# Supports Claims

- `spec:objective-driven-parent-loop` ACC-001
- `spec:objective-driven-parent-loop` ACC-002
- `spec:objective-driven-parent-loop` ACC-003
- `spec:objective-driven-parent-loop` ACC-004
- `spec:objective-driven-parent-loop` ACC-005
- `spec:objective-driven-parent-loop` ACC-006
- `spec:objective-driven-parent-loop` ACC-007
- `ticket:odpl001` ACC-001
- `ticket:odpl001` ACC-002
- `ticket:odpl001` ACC-003
- `ticket:odpl001` ACC-004
- `ticket:odpl001` ACC-005
- `ticket:odpl001` ACC-006
- `ticket:odpl001` ACC-007

# Challenges Claims

None observed.

# Environment

Commit: `9540b551bc8e78c94c02440bfed27b57a0f5a8e1`

Branch: `main`

Runtime: OpenCode parent session with Ralph fixer subagent

OS: darwin

Relevant config: repository has no automated test suite; validation is structural
and manual per `AGENTS.md`.

# Validity

Valid for: current working tree after `packet:ralph-ticket-odpl001-20260428T202948Z` returned.

Recheck when: `skills/loom-drive/**`, `skills/loom-workspace/references/routing.md`, or the governing spec/ticket changes.

# Limitations

This evidence does not provide critique. It does not prove the workflow wording is
optimal, safe enough for acceptance, or free of subtle protocol-boundary drift.
Mandatory critique is recorded separately in `critique:loom-drive-skill-review`.

# Result

The `loom-drive` skill surface exists, its supporting references and template are
named from `SKILL.md`, the workspace routing reference points to `loom-drive`, and
structural checks found no whitespace errors. Forbidden runtime/daemon/poller/new
layer terms appear only in constraint/prohibition contexts. Later iterations added
continuity, tranche decision, checkpoint/resume, hard gate, and route federation
guidance that was structurally visible in the final checks.

After wording cleanup, `loom-drive` product-facing files no longer use the
internal design-debate terms searched above, and skill frontmatter descriptions no
longer use ledger/new-layer/helper-script phrasing as activation criteria. A
broader skills scan leaves the remaining terminology only in bootstrap doctrine
references where it is part of Loom's core operating vocabulary.

# Interpretation

The implementation satisfies the structural validation needed for the
`loom-drive` skill surface. This evidence supports completion pending acceptance
when combined with `critique:loom-drive-skill-review`; it does not by itself own
the ticket acceptance decision.

# Related Records

- `ticket:odpl001`
- `spec:objective-driven-parent-loop`
- `plan:objective-driven-parent-loop-skill`
- `packet:ralph-ticket-odpl001-20260428T202948Z`
