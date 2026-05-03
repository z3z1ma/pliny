---
id: packet:ralph-ticket-promdisp2-20260503T011837Z
kind: packet
packet_kind: ralph
status: consumed
target: ticket:promdisp2
mode: execution
change_class: protocol-authority
risk_class: medium
style: reference-first
verification_posture: observation-first
iteration: 1
created_at: 2026-05-03T01:18:38Z
updated_at: 2026-05-03T01:22:42Z
scope:
  kind: repository
  repositories:
    - repo:root
child_write_scope:
  records:
    - ticket:promdisp2
    - evidence:promotion-disposition-wording-validation
    - packet:ralph-ticket-promdisp2-20260503T011837Z
  paths:
    - PROTOCOL.md
    - README.md
    - skills/loom-bootstrap/references/05-critique-and-wiki.md
    - skills/loom-bootstrap/references/07-validation-and-honesty.md
    - skills/loom-critique/references/critique-lens.md
    - skills/loom-critique/references/review-pass-splitting.md
    - skills/loom-drive/references/tranche-decision-protocol.md
    - skills/loom-evidence/references/evidence-quality.md
    - skills/loom-git/SKILL.md
    - skills/loom-ralph/references/work-driver.md
    - skills/loom-ship/SKILL.md
    - skills/loom-ship/references/handoff-options.md
    - skills/loom-tickets/SKILL.md
    - skills/loom-tickets/references/acceptance-gate.md
    - skills/loom-tickets/templates/ticket.md
    - skills/loom-workspace/references/status-snapshot.md
    - .loom/tickets/20260503-promdisp2-align-promotion-disposition-wording.md
    - .loom/evidence/20260503-promotion-disposition-wording-validation.md
    - .loom/packets/ralph/20260503T011837Z-ticket-promdisp2-iter-01.md
parent_merge_scope:
  records:
    - ticket:promdisp2
    - evidence:promotion-disposition-wording-validation
    - packet:ralph-ticket-promdisp2-20260503T011837Z
  paths:
    - PROTOCOL.md
    - README.md
    - skills/loom-bootstrap/references/05-critique-and-wiki.md
    - skills/loom-bootstrap/references/07-validation-and-honesty.md
    - skills/loom-critique/references/critique-lens.md
    - skills/loom-critique/references/review-pass-splitting.md
    - skills/loom-drive/references/tranche-decision-protocol.md
    - skills/loom-evidence/references/evidence-quality.md
    - skills/loom-git/SKILL.md
    - skills/loom-ralph/references/work-driver.md
    - skills/loom-ship/SKILL.md
    - skills/loom-ship/references/handoff-options.md
    - skills/loom-tickets/SKILL.md
    - skills/loom-tickets/references/acceptance-gate.md
    - skills/loom-tickets/templates/ticket.md
    - skills/loom-workspace/references/status-snapshot.md
    - .loom/tickets/20260503-promdisp2-align-promotion-disposition-wording.md
    - .loom/evidence/20260503-promotion-disposition-wording-validation.md
    - .loom/packets/ralph/20260503T011837Z-ticket-promdisp2-iter-01.md
source_fingerprint:
  git_commit: ee938daf3e32e3a2d1d6806fc7c607828b2624cb
  integration_remote: origin
  integration_ref: origin/main
  integration_commit: ee938daf3e32e3a2d1d6806fc7c607828b2624cb
  git_status_summary: clean
  compiled_from:
    - initiative:skills-corpus-residual-protocol-sharpening-pass
    - plan:skills-corpus-residual-protocol-sharpening-pass
    - research:skills-corpus-residual-audit-synthesis
    - ticket:promdisp2
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
  max_source_files: 16
  max_excerpt_lines_per_file: 160
  avoid_full_file_reads: false
sources:
  initiative:
    - initiative:skills-corpus-residual-protocol-sharpening-pass
  plan:
    - plan:skills-corpus-residual-protocol-sharpening-pass
  research:
    - research:skills-corpus-residual-audit-synthesis
  ticket:
    - ticket:promdisp2
  records:
    - skills/loom-bootstrap/references/07-validation-and-honesty.md
    - skills/loom-tickets/references/acceptance-gate.md
    - skills/loom-tickets/templates/ticket.md
    - skills/loom-ralph/references/work-driver.md
    - skills/loom-ship/SKILL.md
    - README.md
links:
  ticket:
    - ticket:promdisp2
---

# Mission

Align closure and handoff wording so retrospective / promotion disposition is the
broader closure gate, while wiki disposition remains route-specific when wiki is
one selected promotion route.

# Bound Context

This is the second ticket in
`plan:skills-corpus-residual-protocol-sharpening-pass` and covers
`initiative:skills-corpus-residual-protocol-sharpening-pass#OBJ-004`.

The change is protocol-authority wording. Do not create a new retrospective
record kind, do not require wiki promotion for every ticket, and do not add a
runtime, validator, command router, or hidden helper.

# Source Snapshot

Baseline commit: `ee938daf3e32e3a2d1d6806fc7c607828b2624cb`, matching
`origin/main` after `git fetch --prune origin`. Worktree was clean before packet
creation.

Parent observations:

- `skills/loom-bootstrap/references/07-validation-and-honesty.md` still says
  "wiki follow-through has happened or is explicitly deferred" in the general
  done checklist.
- `PROTOCOL.md` still defines acceptance disposition using "wiki follow-through"
  rather than the broader retrospective / promotion gate.
- `skills/loom-ralph/references/work-driver.md`, `skills/loom-ship/SKILL.md`,
  `skills/loom-ship/references/handoff-options.md`, `skills/loom-git/SKILL.md`,
  `skills/loom-critique/references/critique-lens.md`,
  `skills/loom-critique/references/review-pass-splitting.md`,
  `skills/loom-workspace/references/status-snapshot.md`,
  `skills/loom-drive/references/tranche-decision-protocol.md`, and `README.md`
  have candidate "wiki disposition" shorthand that may need broader promotion
  wording.
- Some surfaces already correctly state that `# Wiki Disposition` is
  route-specific and should not replace `# Retrospective / Promotion
  Disposition`. Preserve that distinction.

# Change Class

Declared as `protocol-authority`; risk is medium because closure wording affects
whether agents record durable learning follow-through before accepting work.

# Verification Targets

- `initiative:skills-corpus-residual-protocol-sharpening-pass#OBJ-004`
- `ticket:promdisp2#ACC-001`
- `ticket:promdisp2#ACC-002`
- `ticket:promdisp2#ACC-003`
- `ticket:promdisp2#ACC-004`

# Task For This Iteration

1. Capture before-state searches for `wiki disposition`, `wiki follow-through`,
   `retrospective`, `promotion disposition`, `promotion route`, `not_required`,
   `deferred`, and closure/handoff wording across `skills/`, `README.md`, and
   `PROTOCOL.md`.
2. Replace stale wiki-only closure or handoff shorthand with retrospective /
   promotion disposition wording in affected product/public surfaces inside the
   declared write scope.
3. Keep wiki disposition route-specific: use it only when wiki is one selected
   promotion route, not as a replacement for the broader promotion decision.
4. Preserve honest closure outcomes: `completed`, `deferred`, `not_required`, and
   `blocking` where the acceptance gate or ticket template needs them.
5. Do not edit old closed tickets or prior evidence records merely because they
   contain historical `# Wiki Disposition` sections.
6. Record `evidence:promotion-disposition-wording-validation` with before/after
   searches and `git diff --check`.
7. Update `ticket:promdisp2` to `review_required`, link evidence and this packet,
   update claim matrix statuses, and set next route to `critique`.
8. Fill this packet's `# Child Output`. Parent will mark the packet consumed after
   reconciliation and run mandatory oracle critique.

# Verification Posture

`observation-first`.

The after-state must show broad closure/handoff wording for retrospective /
promotion disposition, route-specific wiki disposition preserved, honest
`completed` / `deferred` / `not_required` / `blocking` outcomes preserved, and
`git diff --check` passing.

# Stop Conditions

Stop and return `blocked` or `escalate` if:

- fixing the stale wording would require a new closure policy or new owner layer;
- the change would require wiki promotion for every ticket;
- the change would remove honest `deferred` or `not_required` closure outcomes;
- the stale wording lives outside the declared write scope and cannot be safely
  corrected without parent scope expansion;
- the source fingerprint is materially stale before launch.

# Output Contract

Return outcome, files changed, records changed, before/after observation
commands/results, `git diff --check` result, residual risks, self-review
concerns, and ticket recommendation. Include whether the ticket should proceed to
mandatory oracle critique with profiles `closure-honesty`, `workflow-boundary`,
and `operator-clarity`.

# Working Notes

Parent compiled this packet after closing and pushing `ticket:routebd1` at
`ee938da`. Sequential execution remains required; do not start later tickets.

# Child Output

Outcome: `blocked`.

Summary: I read the packet, verified `HEAD` was still
`ee938daf3e32e3a2d1d6806fc7c607828b2624cb`, and captured before-state searches
across `skills/`, `README.md`, and `PROTOCOL.md`. The search found expected
stale wiki-only closure and handoff wording inside the declared child write
scope, but also found stale `wiki follow-through` wording in
`skills/loom-records/references/implementation-reality.md`, which is outside the
packet child write scope. I stopped before product wording edits under the packet
stop condition for out-of-scope stale wording.

Files changed:

- `.loom/evidence/20260503-promotion-disposition-wording-validation.md`
- `.loom/tickets/20260503-promdisp2-align-promotion-disposition-wording.md`
- `.loom/packets/ralph/20260503T011837Z-ticket-promdisp2-iter-01.md`

Records changed:

- `evidence:promotion-disposition-wording-validation` created with before-state
  observations, the out-of-scope blocker, limitations, and `git diff --check`
  result.
- `ticket:promdisp2` moved from `active` to `blocked`, linked the evidence, and
  updated the claim matrix, blocker, next route, evidence, and journal sections.
- `packet:ralph-ticket-promdisp2-20260503T011837Z` child output filled.

Before observations:

- `README.md:415`, `PROTOCOL.md:48`,
  `skills/loom-bootstrap/references/07-validation-and-honesty.md:26`,
  `skills/loom-ship/SKILL.md`, `skills/loom-ralph/references/work-driver.md`,
  `skills/loom-git/SKILL.md`,
  `skills/loom-critique/references/critique-lens.md`,
  `skills/loom-critique/references/review-pass-splitting.md`, and
  `skills/loom-drive/references/tranche-decision-protocol.md` contain candidate
  stale wiki-only closure/handoff shorthand inside the declared write scope.
- `skills/loom-records/references/implementation-reality.md:26` also says
  `critique, evidence, or wiki follow-through remains open`, but that file is
  not in the declared child write scope.
- Existing ticket template and acceptance gate wording preserve `completed`,
  `deferred`, `not_required`, and `blocking` outcomes.

After observations:

- No product-surface after-state wording validation was completed because no
  product wording edits were made after the stop condition triggered.
- Record-only after-state: the ticket and evidence now truthfully record the
  blocker.

Validation:

- `git diff --check`: passed.

Residual risks / self-review concerns:

- The intended wording cleanup is not implemented.
- Parent must decide whether to expand scope to include
  `skills/loom-records/references/implementation-reality.md` or explicitly rule
  that occurrence not stale.
- This ticket should not proceed to mandatory oracle critique as a completed
  implementation yet; critique profiles `closure-honesty`, `workflow-boundary`,
  and `operator-clarity` remain appropriate after implementation completes.

Ticket recommendation: keep `ticket:promdisp2` blocked for parent scope
reconciliation, then compile a replacement Ralph packet or otherwise authorize
the missing product-surface edit before routing to critique.

# Parent Merge Notes

2026-05-03T01:22:42Z: Parent accepted the blocked child output as valid scope
discovery, not as completed implementation. The out-of-scope occurrence in
`skills/loom-records/references/implementation-reality.md` is part of the same
promotion-disposition closure wording issue, so parent is expanding the write
scope in replacement packet `packet:ralph-ticket-promdisp2-20260503T012242Z`.
This packet is consumed because child output was received and reconciled into
ticket/evidence truth; it did not satisfy implementation acceptance.
