---
id: evidence:route-status-vocabulary-validation
kind: evidence
status: recorded
created_at: 2026-05-03T04:57:59Z
updated_at: 2026-05-03T04:57:59Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  ticket:
    - ticket:vocabx08
  packet:
    - packet:ralph-ticket-vocabx08-20260503T045534Z
  initiative:
    - initiative:skills-corpus-context-integrity-hardening-pass
external_refs: {}
---

# Summary

Observed route/status/disposition vocabulary consolidation for `ticket:vocabx08`
and checked canonical cross-links, child-outcome boundaries, finding-state versus
ticket-disposition distinctions, and absence of runtime machinery requirements.

# Procedure

Observed at: 2026-05-03T04:57:59Z

Source state: working tree on `main` based on commit
`bd06422e297a3ff4dc9776ca37f36d12bbd77ddf`, after Ralph child output and before
mandatory critique.

Procedure:

- Ran targeted `rg` checks over route/status canonical sources and dependent
  vocabulary references.
- Added the new Ralph packet to the index with intent-to-add and ran
  `git diff --check` so the check covered new packet content and tracked edits.

Procedure verdict / exit code: pass; each targeted `rg` returned expected lines,
and `git diff --check` returned no output.

# Artifacts

## Canonical Source Cross-Links

Command:

```bash
rg -n 'canonical shared grammar|canonical shared source|Route tokens are owned by|state-machine\.md|status-lifecycle\.md|route-vocabulary\.md|packet-contract\.md' skills/loom-records/references/route-vocabulary.md skills/loom-records/references/status-lifecycle.md skills/loom-tickets/references/state-machine.md skills/loom-ralph/references/packet-contract.md skills/loom-critique/references/finding-format.md
```

Output:

```text
skills/loom-records/references/status-lifecycle.md:3:This reference is the canonical shared source for Loom lifecycle status and
skills/loom-records/references/status-lifecycle.md:8:`skills/loom-tickets/references/state-machine.md`. Route tokens live in
skills/loom-records/references/status-lifecycle.md:9:`skills/loom-records/references/route-vocabulary.md`. This reference covers the
skills/loom-records/references/route-vocabulary.md:3:This reference is the canonical shared grammar for Loom route tokens used in
skills/loom-records/references/route-vocabulary.md:11:`skills/loom-records/references/status-lifecycle.md`. Ticket execution states
skills/loom-records/references/route-vocabulary.md:12:are owned by `skills/loom-tickets/references/state-machine.md`, and Ralph child
skills/loom-records/references/route-vocabulary.md:13:outcomes are owned by `skills/loom-ralph/references/packet-contract.md`.
skills/loom-critique/references/finding-format.md:4:For route tokens, use `skills/loom-records/references/route-vocabulary.md`; for
skills/loom-critique/references/finding-format.md:6:`skills/loom-records/references/status-lifecycle.md`.
skills/loom-tickets/references/state-machine.md:5:statuses. Route tokens are owned by
skills/loom-tickets/references/state-machine.md:6:`skills/loom-records/references/route-vocabulary.md`; non-ticket record statuses,
skills/loom-tickets/references/state-machine.md:8:`skills/loom-records/references/status-lifecycle.md`.
skills/loom-ralph/references/packet-contract.md:10:Use `skills/loom-records/references/route-vocabulary.md` for route tokens and
skills/loom-ralph/references/packet-contract.md:11:`skills/loom-records/references/status-lifecycle.md` for packet lifecycle status
```

## Child Outcomes Versus Route Tokens

Command:

```bash
rg -n 'route-token use only|Ralph child outcome|Child Outcomes vs Routes|outcome: continue|next route: continue|outcome such as `continue`|child outcome' skills/loom-records/references/route-vocabulary.md skills/loom-records/references/status-lifecycle.md skills/loom-ralph/references/packet-contract.md
```

Output:

```text
skills/loom-ralph/references/packet-contract.md:12:boundaries. Ralph child outcomes are packet output vocabulary, not route tokens
skills/loom-ralph/references/packet-contract.md:228:## Child Outcomes vs Routes
skills/loom-ralph/references/packet-contract.md:230:A Ralph child should return one child outcome: `continue`, `stop`, `blocked`, or
skills/loom-ralph/references/packet-contract.md:234:The parent reconciles the child outcome into ticket truth and then chooses the
skills/loom-records/references/route-vocabulary.md:48:| `continue` | route-token use only: proceed to the next already-governed tranche or route named by owner records; do not use this row to interpret a Ralph child outcome named `continue` |
skills/loom-records/references/route-vocabulary.md:49:| `stop` | route-token use only: stop because the objective is satisfied, blocked, unsafe, out of scope, over budget, or awaiting external action; recorded stop routes must include a stop reason or condition; do not use this row to interpret a Ralph child outcome named `stop` |
skills/loom-records/references/route-vocabulary.md:69:| Ralph child outcomes | `continue`, `stop`, `blocked`, `escalate` | A child outcome is not a route token by itself. It becomes routing truth only after the parent reconciles the child output and translates it into the next owner-truth route, such as `ticket`, `research`, `critique`, `ask_user`, `continue`, or `stop`. |
skills/loom-records/references/route-vocabulary.md:77:Ralph packet `outcome: continue` is child output for parent reconciliation; a
skills/loom-records/references/route-vocabulary.md:78:recorded `next route: continue` is a parent-owned route decision.
skills/loom-records/references/route-vocabulary.md:118:next route: continue
skills/loom-records/references/route-vocabulary.md:119:continue reason: ticket:<token> already names the next governed tranche; this is not a Ralph child outcome.
skills/loom-records/references/status-lifecycle.md:31:  outcome such as `continue`, `stop`, `blocked`, or `escalate`, the parent must
```

## Status And Disposition Distinctions

Command:

```bash
rg -n 'Ticket lifecycle states|Record lifecycle statuses|packet: `compiled|Critique-owned finding state|Ticket-owned finding disposition|ticket lifecycle states|packet statuses|finding states|finding dispositions|critique finding states' skills/loom-records/references/route-vocabulary.md skills/loom-records/references/status-lifecycle.md skills/loom-tickets/references/state-machine.md skills/loom-critique/references/finding-format.md
```

Output:

```text
skills/loom-tickets/references/state-machine.md:3:This reference owns ticket lifecycle states: the live execution ledger values for
skills/loom-tickets/references/state-machine.md:7:packet statuses, and disposition vocabulary boundaries are summarized in
skills/loom-records/references/route-vocabulary.md:67:| Ticket lifecycle states | `proposed`, `ready`, `active`, `blocked`, `review_required`, `complete_pending_acceptance`, `closed`, `cancelled` | Describe live ticket execution state. They are not `next route:` values. |
skills/loom-records/references/route-vocabulary.md:68:| Record lifecycle statuses | `draft`, `active`, `accepted`, `recorded`, `superseded`, `abandoned` | Describe a record's lifecycle or support-surface state, not the next governed move. |
skills/loom-records/references/route-vocabulary.md:70:| Critique-owned finding states | `open`, `withdrawn` | Live inside critique records and describe whether the critique still stands behind a finding. They are not ticket states or route tokens. |
skills/loom-records/references/route-vocabulary.md:71:| Ticket-owned finding dispositions | `resolved`, `accepted_risk`, `superseded`, `converted_to_follow_up` | Live in the ticket's critique disposition section for qualified findings. They are not critique finding states and do not name the next route. |
skills/loom-records/references/status-lifecycle.md:10:normal non-ticket record statuses plus boundary guidance for packet statuses,
skills/loom-records/references/status-lifecycle.md:11:finding states, and ticket-owned dispositions.
skills/loom-records/references/status-lifecycle.md:34:- **Critique-owned finding state** lives inside critique records. Use `open` for a
skills/loom-records/references/status-lifecycle.md:38:  open medium/high findings require ticket-owned finding dispositions before
skills/loom-records/references/status-lifecycle.md:42:- **Ticket-owned finding disposition** lives in the ticket's
skills/loom-records/references/status-lifecycle.md:71:- packet: `compiled | consumed | superseded | abandoned`
skills/loom-records/references/status-lifecycle.md:168:Use packet statuses as operational state, not as archival decoration. This
skills/loom-critique/references/finding-format.md:45:the ticket's acceptance gate. They are not ticket lifecycle states, route tokens,
skills/loom-critique/references/finding-format.md:46:or ticket-owned finding dispositions. When critique needs to mention an existing
skills/loom-critique/references/finding-format.md:57:Only open medium/high findings require ticket-owned finding dispositions before
skills/loom-critique/references/finding-format.md:62:Use ticket-owned finding dispositions only in the ticket's
skills/loom-critique/references/finding-format.md:71:critique finding states, ticket lifecycle states, route tokens, runtime enums,
```

## Runtime Boundary

Command:

```bash
rg -n 'runtime enum|schema|validator|command router|new owner layer' skills/loom-records/references/route-vocabulary.md skills/loom-records/references/status-lifecycle.md skills/loom-tickets/references/state-machine.md skills/loom-ralph/references/packet-contract.md skills/loom-critique/references/finding-format.md
```

Output:

```text
skills/loom-records/references/route-vocabulary.md:6:Route tokens are not a runtime enum, command router, or new owner layer. They are
skills/loom-records/references/route-vocabulary.md:66:| Route tokens | `constitution`, `initiative`, `research`, `ralph`, `critique`, `continue`, `stop` | Use only when a route field asks for the next governed move. Tokens remain Markdown vocabulary, not a runtime enum, schema, validator, command router, skill inventory, or owner layer. |
skills/loom-records/references/status-lifecycle.md:5:legible without requiring a runtime enum, schema, validator, or command router.
skills/loom-records/references/status-lifecycle.md:53:required runtime enum, schema, validator, command router, or new owner layer.
skills/loom-critique/references/finding-format.md:71:critique finding states, ticket lifecycle states, route tokens, runtime enums,
skills/loom-critique/references/finding-format.md:72:schemas, validators, or command-router values.
```

## Full Diff Whitespace Check

Command:

```bash
git add -N ".loom/packets/ralph/20260503T045534Z-ticket-vocabx08-iter-01.md" && git diff --check
```

Output:

```text
```

Exit status: pass; no whitespace errors were reported.

# Supports Claims

- `initiative:skills-corpus-context-integrity-hardening-pass#OBJ-003`
- `ticket:vocabx08#ACC-001`
- `ticket:vocabx08#ACC-002`
- `ticket:vocabx08#ACC-003`
- `ticket:vocabx08#ACC-004`

# Challenges Claims

None - no challenged claims were observed.

# Environment

Commit: `bd06422e297a3ff4dc9776ca37f36d12bbd77ddf` plus uncommitted
ticket-scoped working-tree changes

Branch: `main`

Runtime: none; Markdown corpus only

OS: macOS / Darwin

Relevant config: no app runtime or automated test suite

# Validity

Valid for: the listed files observed at 2026-05-03T04:57:59Z.

Fresh enough for: mandatory critique and ticket acceptance review for
`ticket:vocabx08`.

Recheck when: route/status vocabulary wording, touched files, ticket criteria, or
critique findings change before closure.

Invalidated by: later edits that rename route tokens, blur ticket states with
route tokens, or introduce runtime enum/schema/validator/command-router
requirements.

Supersedes / superseded by: None.

# Limitations

This evidence does not prove the vocabulary model is sufficient; mandatory
critique and ticket-owned acceptance decide that.

# Result

The observed vocabulary consolidation is Markdown guidance only and stays within
the declared write scope.

# Interpretation

The observations support the ticket's structural claims, pending critique.

# Related Records

- `ticket:vocabx08`
- `packet:ralph-ticket-vocabx08-20260503T045534Z`
- `initiative:skills-corpus-context-integrity-hardening-pass`
