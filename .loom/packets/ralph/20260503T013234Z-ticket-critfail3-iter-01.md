---
id: packet:ralph-ticket-critfail3-20260503T013234Z
kind: packet
packet_kind: ralph
status: consumed
target: ticket:critfail3
mode: execution
change_class: protocol-authority
risk_class: medium
style: reference-first
verification_posture: observation-first
iteration: 1
created_at: 2026-05-03T01:32:34Z
updated_at: 2026-05-03T01:36:39Z
scope:
  kind: repository
  repositories:
    - repo:root
child_write_scope:
  records:
    - ticket:critfail3
    - evidence:mandatory-critique-template-validation
    - packet:ralph-ticket-critfail3-20260503T013234Z
  paths:
    - skills/loom-tickets/templates/ticket.md
    - skills/loom-tickets/references/acceptance-gate.md
    - .loom/tickets/20260503-critfail3-harden-mandatory-critique-template.md
    - .loom/evidence/20260503-mandatory-critique-template-validation.md
    - .loom/packets/ralph/20260503T013234Z-ticket-critfail3-iter-01.md
parent_merge_scope:
  records:
    - ticket:critfail3
    - evidence:mandatory-critique-template-validation
    - packet:ralph-ticket-critfail3-20260503T013234Z
  paths:
    - skills/loom-tickets/templates/ticket.md
    - skills/loom-tickets/references/acceptance-gate.md
    - .loom/tickets/20260503-critfail3-harden-mandatory-critique-template.md
    - .loom/evidence/20260503-mandatory-critique-template-validation.md
    - .loom/packets/ralph/20260503T013234Z-ticket-critfail3-iter-01.md
source_fingerprint:
  git_commit: f13ce09cdc7fb9128e318bd79e40fee1eb21c7a0
  integration_remote: origin
  integration_ref: origin/main
  integration_commit: f13ce09cdc7fb9128e318bd79e40fee1eb21c7a0
  git_status_summary: clean
  compiled_from:
    - initiative:skills-corpus-residual-protocol-sharpening-pass
    - plan:skills-corpus-residual-protocol-sharpening-pass
    - research:skills-corpus-residual-audit-synthesis
    - ticket:critfail3
execution_context:
  branch: main
  push_remote: origin
  worktree: /Users/alexanderbutler/code_projects/personal/agent-loom
  isolation: none
  git_shared_metadata_mutations: forbidden
  destructive_commands: forbidden
  network: forbidden
context_budget:
  posture: tight
  max_source_files: 6
  max_excerpt_lines_per_file: 140
  avoid_full_file_reads: false
sources:
  initiative:
    - initiative:skills-corpus-residual-protocol-sharpening-pass
  plan:
    - plan:skills-corpus-residual-protocol-sharpening-pass
  research:
    - research:skills-corpus-residual-audit-synthesis
  ticket:
    - ticket:critfail3
  records:
    - skills/loom-tickets/templates/ticket.md
    - skills/loom-tickets/references/acceptance-gate.md
    - skills/loom-bootstrap/references/07-validation-and-honesty.md
    - skills/loom-records/references/status-lifecycle.md
links:
  ticket:
    - ticket:critfail3
---

# Mission

Make the ticket template locally fail closed for mandatory critique disposition so
fresh agents cannot copy the template and treat mandatory critique as closeable by
deferral or `not_required`.

# Bound Context

This is the third ticket in
`plan:skills-corpus-residual-protocol-sharpening-pass` and covers
`initiative:skills-corpus-residual-protocol-sharpening-pass#OBJ-005`.

The ticket template is the primary target. `skills/loom-tickets/references/acceptance-gate.md`
may be edited only if the template needs a local pointer to the existing gate or
if a small consistency fix is required. Do not change the ticket state machine,
make recommended critique mandatory, or blur ticket-owned finding dispositions
with critique-owned finding states.

# Source Snapshot

Baseline commit: `f13ce09cdc7fb9128e318bd79e40fee1eb21c7a0`, matching
`origin/main` after `git fetch --prune origin`. Worktree was clean before packet
creation.

Current observations:

- `skills/loom-tickets/templates/ticket.md` lists `Disposition status: <TBD:
  choose pending, blocking, completed, deferred, or not_required>` and says to use
  `blocking` when unresolved required critique blocks acceptance.
- The template does not locally state that mandatory critique cannot be satisfied
  by `deferred`, `not_required`, or a draft/stub review.
- The template already states open medium/high findings need ticket-owned
  dispositions before closure.
- `skills/loom-bootstrap/references/07-validation-and-honesty.md` and the ticket
  acceptance gate already carry stronger mandatory critique closure rules; this
  ticket copies the closure-critical part into the template for safer local use.

# Change Class

Declared as `protocol-authority`; risk is medium because ticket templates shape
future acceptance gates and critique closure behavior.

# Verification Targets

- `initiative:skills-corpus-residual-protocol-sharpening-pass#OBJ-005`
- `ticket:critfail3#ACC-001`
- `ticket:critfail3#ACC-002`
- `ticket:critfail3#ACC-003`
- `ticket:critfail3#ACC-004`

# Task For This Iteration

1. Capture before-state searches for `Critique policy`, `mandatory`, `deferred`,
   `not_required`, `Disposition status`, `draft/stub`, open medium/high findings,
   and ticket-owned dispositions in the ticket template and acceptance-gate
   reference.
2. Add the smallest local fail-closed note to the ticket template critique
   disposition section:
   - mandatory critique remains `pending` or `blocking` until a final critique
     exists;
   - open medium/high mandatory critique findings need ticket-owned dispositions
     before closure;
   - `deferred` and `not_required` are closure-compatible only for recommended or
     optional critique with rationale, not for mandatory critique.
3. Preserve the existing distinction between mandatory, recommended, and optional
   critique.
4. Preserve ticket-owned finding dispositions as separate from critique-owned
   finding states and verdicts.
5. Record `evidence:mandatory-critique-template-validation` with before/after
   searches and `git diff --check`.
6. Update `ticket:critfail3` to `review_required`, link evidence and this packet,
   update claim matrix statuses, and set next route to `critique`.
7. Fill this packet's `# Child Output`. Parent will mark the packet consumed after
   reconciliation and run mandatory oracle critique.

# Verification Posture

`observation-first`.

The after-state must show the fail-closed mandatory critique rule in the ticket
template, preserved recommended/optional deferral semantics, preserved
ticket-owned finding disposition examples, and `git diff --check` passing.

# Stop Conditions

Stop and return `blocked` or `escalate` if:

- the fix requires changing the ticket state machine;
- the fix would make recommended critique a mandatory closure blocker by default;
- the fix would let critique records own ticket finding dispositions;
- the fix needs a broader policy change outside ticket template / acceptance gate;
- the source fingerprint is materially stale before launch.

# Output Contract

Return outcome, files changed, records changed, before/after observation
commands/results, `git diff --check` result, residual risks, self-review
concerns, and ticket recommendation. Include whether the ticket should proceed to
mandatory oracle critique with profiles `closure-honesty`, `template-safety`, and
`owner-boundary`.

# Working Notes

Parent compiled this packet after closing and pushing `ticket:promdisp2` at
`f13ce09`. Sequential execution remains required; do not start later tickets.

# Child Output

Outcome: `stop` — bounded implementation iteration completed; ticket should
proceed to mandatory oracle critique.

Files changed:

- `skills/loom-tickets/templates/ticket.md`
- `.loom/tickets/20260503-critfail3-harden-mandatory-critique-template.md`
- `.loom/evidence/20260503-mandatory-critique-template-validation.md`
- `.loom/packets/ralph/20260503T013234Z-ticket-critfail3-iter-01.md`

Records changed:

- `ticket:critfail3` — moved to `review_required`, linked
  `evidence:mandatory-critique-template-validation`, updated claim matrix statuses,
  and set next route to `critique`.
- `evidence:mandatory-critique-template-validation` — recorded before/after
  searches and `git diff --check` result.
- `packet:ralph-ticket-critfail3-20260503T013234Z` — filled child output.

Before observations:

- `Critique policy` existed only in the template status prompt.
- `mandatory` appeared in the template prompt and acceptance-gate reference, but
  not as a local template fail-closed rule for final critique existence.
- `deferred` / `not_required` appeared in disposition status prompts and
  retrospective/promotion wording; the template did not locally say those values
  are not closure-compatible for mandatory critique.
- `draft/stub` and exact `open medium/high findings` had no matches in the
  searched template/reference pair.
- `ticket-owned dispositions` and `ticket-owned finding dispositions` were
  already present as owner-boundary wording.

After observations:

- The template now says mandatory critique remains `pending` until final,
  non-draft/stub required critique exists.
- The template now says unresolved mandatory critique blockers use `blocking`.
- The template now says open medium/high findings missing ticket-owned
  dispositions use `blocking` until the ticket records `resolved`,
  `accepted_risk`, `superseded`, or `converted_to_follow_up` with required
  support.
- The template now says `deferred` and `not_required` are closure-compatible only
  for recommended or optional critique with rationale, not mandatory critique.
- Owner boundary is preserved: critique owns finding state and verdict; the
  ticket owns how findings affect closure.

Validation:

- `git diff --check` passed with no output after the template/ticket edit.
- Evidence details are recorded in
  `.loom/evidence/20260503-mandatory-critique-template-validation.md`.

Residual risks / self-review concerns:

- Mandatory oracle critique has not happened yet; `ticket:critfail3#ACC-005`
  remains open.
- This was structural Markdown validation only; there is no automated test suite
  for these protocol templates.

Ticket recommendation:

- Keep `ticket:critfail3` in `review_required` and run mandatory oracle critique
  with profiles `closure-honesty`, `template-safety`, and `owner-boundary`.

# Parent Merge Notes

2026-05-03T01:36:39Z: Parent accepted the bounded child output for mandatory
oracle critique. The implementation stayed inside write scope, updated
`evidence:mandatory-critique-template-validation`, and left `ticket:critfail3` in
`review_required` with next route `critique`. Parent normalized the ticket claim
matrix pending-review statuses to the canonical `supported_pending_review`
vocabulary from `skills/loom-records/references/claim-coverage.md`. `git diff
--check` passed after reconciliation.
