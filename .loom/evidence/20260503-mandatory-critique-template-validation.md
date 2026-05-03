---
id: evidence:mandatory-critique-template-validation
kind: evidence
status: recorded
created_at: 2026-05-03T01:34:06Z
updated_at: 2026-05-03T01:34:06Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  ticket:
    - ticket:critfail3
  packet:
    - packet:ralph-ticket-critfail3-20260503T013234Z
external_refs: {}
---

# Summary

Observed the ticket template and acceptance gate before and after adding local
fail-closed mandatory critique wording to `skills/loom-tickets/templates/ticket.md`.

# Procedure

At commit `f13ce09cdc7fb9128e318bd79e40fee1eb21c7a0` on branch `main`, ran
before/after `rg` searches over:

- `skills/loom-tickets/templates/ticket.md`
- `skills/loom-tickets/references/acceptance-gate.md`

Patterns searched:

- `Critique policy`
- `mandatory`
- `deferred`
- `not_required`
- `Disposition status`
- `draft/stub`
- `open medium/high findings`
- `open medium/high`
- `ticket-owned dispositions`
- `ticket-owned finding dispositions`

After the edit, ran `git diff --check`.

# Artifacts

## Before searches

Command shape:

```bash
for pattern in 'Critique policy' 'mandatory' 'deferred' 'not_required' 'Disposition status' 'draft/stub' 'open medium/high findings' 'open medium/high' 'ticket-owned dispositions' 'ticket-owned finding dispositions'; do
  rg -n "$pattern" skills/loom-tickets/templates/ticket.md skills/loom-tickets/references/acceptance-gate.md || true
done
```

Observed output:

```text
### Critique policy
skills/loom-tickets/templates/ticket.md:185:Critique policy: <TBD: choose optional, recommended, or mandatory>

### mandatory
skills/loom-tickets/templates/ticket.md:185:Critique policy: <TBD: choose optional, recommended, or mandatory>
skills/loom-tickets/references/acceptance-gate.md:16:- critique policy: `optional`, `recommended`, or `mandatory`, plus rationale and
skills/loom-tickets/references/acceptance-gate.md:69:- If critique is mandatory, does required critique exist and do all open
skills/loom-tickets/references/acceptance-gate.md:157:- Do not close over missing mandatory critique.

### deferred
skills/loom-tickets/templates/ticket.md:213:Disposition status: <TBD: choose pending, blocking, completed, deferred, or not_required>
skills/loom-tickets/templates/ticket.md:228:Disposition status: <TBD: choose pending, blocking, completed, deferred, or not_required>
skills/loom-tickets/templates/ticket.md:236:- Use `deferred` when promotion or prevention is intentionally moved to linked
skills/loom-tickets/references/acceptance-gate.md:17:  ticket-owned disposition status `pending`, `blocking`, `completed`, `deferred`,
skills/loom-tickets/references/acceptance-gate.md:20:  `blocking`, `completed`, `deferred`, or `not_required`, plus promoted owner
skills/loom-tickets/references/acceptance-gate.md:73:  was deferred or intentionally not needed before closure?
skills/loom-tickets/references/acceptance-gate.md:81:  `deferred`, or `not_required`, or does it remain `blocking` because required

### not_required
skills/loom-tickets/templates/ticket.md:213:Disposition status: <TBD: choose pending, blocking, completed, deferred, or not_required>
skills/loom-tickets/templates/ticket.md:228:Disposition status: <TBD: choose pending, blocking, completed, deferred, or not_required>
skills/loom-tickets/templates/ticket.md:238:- Use `not_required` when the ticket has no durable lesson to promote.
skills/loom-tickets/references/acceptance-gate.md:18:  or `not_required`
skills/loom-tickets/references/acceptance-gate.md:20:  `blocking`, `completed`, `deferred`, or `not_required`, plus promoted owner
skills/loom-tickets/references/acceptance-gate.md:81:  `deferred`, or `not_required`, or does it remain `blocking` because required

### Disposition status
skills/loom-tickets/templates/ticket.md:213:Disposition status: <TBD: choose pending, blocking, completed, deferred, or not_required>
skills/loom-tickets/templates/ticket.md:228:Disposition status: <TBD: choose pending, blocking, completed, deferred, or not_required>

### draft/stub
No matches.

### open medium/high findings
No matches.

### open medium/high
skills/loom-tickets/references/acceptance-gate.md:161:- Do not close over open medium/high critique findings unless the ticket records

### ticket-owned dispositions
skills/loom-tickets/references/acceptance-gate.md:70:  medium/high findings have ticket-owned dispositions of `resolved`,
skills/loom-tickets/references/acceptance-gate.md:75:  ticket-owned dispositions of `resolved`, `accepted_risk`, `superseded`, or
skills/loom-tickets/templates/ticket.md:207:Open medium/high findings must have ticket-owned dispositions of `resolved`,

### ticket-owned finding dispositions
skills/loom-tickets/references/acceptance-gate.md:15:- critique records and ticket-owned finding dispositions
skills/loom-tickets/templates/ticket.md:195:List real finding references and ticket-owned finding dispositions, or write
```

## After searches

Command shape was the same as the before searches.

Observed output:

```text
### Critique policy
skills/loom-tickets/templates/ticket.md:185:Critique policy: <TBD: choose optional, recommended, or mandatory>

### mandatory
skills/loom-tickets/templates/ticket.md:185:Critique policy: <TBD: choose optional, recommended, or mandatory>
skills/loom-tickets/templates/ticket.md:221:- If critique policy is `mandatory`, keep this disposition `pending` until a
skills/loom-tickets/templates/ticket.md:223:- If mandatory critique exists but has unresolved blocking issues, use
skills/loom-tickets/templates/ticket.md:230:  optional critique with rationale; do not use them to satisfy mandatory
skills/loom-tickets/references/acceptance-gate.md:16:- critique policy: `optional`, `recommended`, or `mandatory`, plus rationale and
skills/loom-tickets/references/acceptance-gate.md:69:- If critique is mandatory, does required critique exist and do all open
skills/loom-tickets/references/acceptance-gate.md:157:- Do not close over missing mandatory critique.

### deferred
skills/loom-tickets/templates/ticket.md:213:Disposition status: <TBD: choose pending, blocking, completed, deferred, or not_required>
skills/loom-tickets/templates/ticket.md:229:- `deferred` and `not_required` are closure-compatible only for recommended or
skills/loom-tickets/templates/ticket.md:244:Disposition status: <TBD: choose pending, blocking, completed, deferred, or not_required>
skills/loom-tickets/templates/ticket.md:252:- Use `deferred` when promotion or prevention is intentionally moved to linked
skills/loom-tickets/references/acceptance-gate.md:17:  ticket-owned disposition status `pending`, `blocking`, `completed`, `deferred`,
skills/loom-tickets/references/acceptance-gate.md:20:  `blocking`, `completed`, `deferred`, or `not_required`, plus promoted owner
skills/loom-tickets/references/acceptance-gate.md:73:  was deferred or intentionally not needed before closure?
skills/loom-tickets/references/acceptance-gate.md:81:  `deferred`, or `not_required`, or does it remain `blocking` because required

### not_required
skills/loom-tickets/templates/ticket.md:213:Disposition status: <TBD: choose pending, blocking, completed, deferred, or not_required>
skills/loom-tickets/templates/ticket.md:229:- `deferred` and `not_required` are closure-compatible only for recommended or
skills/loom-tickets/templates/ticket.md:244:Disposition status: <TBD: choose pending, blocking, completed, deferred, or not_required>
skills/loom-tickets/templates/ticket.md:254:- Use `not_required` when the ticket has no durable lesson to promote.
skills/loom-tickets/references/acceptance-gate.md:18:  or `not_required`
skills/loom-tickets/references/acceptance-gate.md:20:  `blocking`, `completed`, `deferred`, or `not_required`, plus promoted owner
skills/loom-tickets/references/acceptance-gate.md:81:  `deferred`, or `not_required`, or does it remain `blocking` because required

### Disposition status
skills/loom-tickets/templates/ticket.md:213:Disposition status: <TBD: choose pending, blocking, completed, deferred, or not_required>
skills/loom-tickets/templates/ticket.md:244:Disposition status: <TBD: choose pending, blocking, completed, deferred, or not_required>

### draft/stub
skills/loom-tickets/templates/ticket.md:222:  final, non-draft/stub required critique exists.

### open medium/high findings
skills/loom-tickets/templates/ticket.md:225:- If open medium/high findings are missing ticket-owned dispositions, use

### open medium/high
skills/loom-tickets/templates/ticket.md:225:- If open medium/high findings are missing ticket-owned dispositions, use
skills/loom-tickets/references/acceptance-gate.md:161:- Do not close over open medium/high critique findings unless the ticket records

### ticket-owned dispositions
skills/loom-tickets/references/acceptance-gate.md:70:  medium/high findings have ticket-owned dispositions of `resolved`,
skills/loom-tickets/references/acceptance-gate.md:75:  ticket-owned dispositions of `resolved`, `accepted_risk`, `superseded`, or
skills/loom-tickets/templates/ticket.md:207:Open medium/high findings must have ticket-owned dispositions of `resolved`,
skills/loom-tickets/templates/ticket.md:225:- If open medium/high findings are missing ticket-owned dispositions, use

### ticket-owned finding dispositions
skills/loom-tickets/templates/ticket.md:195:List real finding references and ticket-owned finding dispositions, or write
skills/loom-tickets/references/acceptance-gate.md:15:- critique records and ticket-owned finding dispositions
```

## Diff check

Command:

```bash
git diff --check
```

Observed output: no output; exit status 0.

# Supports Claims

- `ticket:critfail3#ACC-001`
- `ticket:critfail3#ACC-002`
- `ticket:critfail3#ACC-003`
- `ticket:critfail3#ACC-004`
- `initiative:skills-corpus-residual-protocol-sharpening-pass#OBJ-005`

# Challenges Claims

None.

# Environment

Commit: `f13ce09cdc7fb9128e318bd79e40fee1eb21c7a0`
Branch: `main`
Runtime: Markdown/file tool structural validation
OS: Darwin
Relevant config: no automated test suite; validation is structural and manual.

# Validity

Valid for: current uncommitted diff for `ticket:critfail3`.
Fresh enough for: the edited ticket template, ticket record, packet, and this evidence record at `2026-05-03T01:34:06Z`.
Recheck when: ticket template, acceptance gate, ticket, evidence, or packet changes before critique/acceptance.
Invalidated by: edits that change critique disposition wording, owner boundaries, or claim/evidence links.
Supersedes / superseded by: None.

# Limitations

This evidence does not provide the mandatory oracle critique required by
`ticket:critfail3#ACC-005`, and it does not close the ticket.

# Result

The after-state shows local template wording that mandatory critique remains
`pending` until final non-draft/stub required critique exists, uses `blocking`
for unresolved mandatory critique blockers or open medium/high findings lacking
ticket-owned dispositions, and keeps `deferred` / `not_required` limited to
recommended or optional critique with rationale. `git diff --check` passed.

# Interpretation

The structural observations support the template-update claims for `ACC-001`
through `ACC-004`. They do not establish acceptance or critique sufficiency; the
ticket should proceed to mandatory critique.

# Related Records

- `ticket:critfail3`
- `packet:ralph-ticket-critfail3-20260503T013234Z`
