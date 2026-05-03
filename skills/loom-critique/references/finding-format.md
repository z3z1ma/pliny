# Finding Format

This reference owns critique finding format and critique-owned finding state.
For route tokens, use `skills/loom-records/references/route-vocabulary.md`; for
shared lifecycle and disposition boundary guidance, use
`skills/loom-records/references/status-lifecycle.md`.

Each meaningful finding should normally include:

- a stable ID: `FIND-001`
- a short title
- severity: `low | medium | high`
- confidence: `low | medium | high`
- state: `open | withdrawn`
- what was observed
- why it matters
- what follow-up would reduce the risk

For code findings, include file and line references when practical.
For artifact findings, include record IDs or paths.

Keep findings concrete.
A critique record should help someone act, not merely worry.

## Finding References

When another record refers to a finding, qualify it:

```text
critique:example-review#FIND-001
```

Tickets should use those references when tracking critique disposition for open
medium/high findings. The ticket owns acceptance: it records whether each open
finding that affects closure has a ticket-owned disposition of `resolved`,
`accepted_risk`, `superseded`, or `converted_to_follow_up`.

## Finding State vs Ticket Disposition

Critique records produce findings, verdicts, residual risks, and follow-up
recommendations. They do not close ticket work and do not accept their own
findings on behalf of the ticket.

Acceptance recommendation labels in critique records are non-canonical advice for
the ticket's acceptance gate. They are not ticket lifecycle states, route tokens,
or ticket-owned finding dispositions. When critique needs to mention an existing
ticket state or route token, quote it as the ticket-owned next action and state
that critique does not apply it.

Use critique-owned finding state narrowly:

- `open` — the finding is part of the review output and the ticket must consume
  it.
- `withdrawn` — the critique retracts the finding with rationale; the ticket may
  cite that rationale when reconciling review history.

Only open medium/high findings require ticket-owned finding dispositions before
closure. Withdrawn findings require critique rationale, not ticket-owned finding
disposition; a ticket may cite them for audit history without treating them as
closure blockers.

Use ticket-owned finding dispositions only in the ticket's
`# Critique Disposition` section:

- `resolved`
- `accepted_risk`
- `superseded`
- `converted_to_follow_up`

These dispositions are ticket-owned closure-gate vocabulary. They are not
critique finding states, ticket lifecycle states, route tokens, runtime enums,
schemas, validators, or command-router values.

## Receiving Findings

Treat incoming review feedback as claims to verify, not commands to obey blindly.

For each finding:

1. read the finding completely
2. restate the technical requirement if it is unclear
3. inspect the relevant source, record, evidence, or diff
4. decide whether the finding is valid for this project and ticket scope
5. implement, clarify, accept risk with provenance, supersede with evidence, or
   create a linked follow-up ticket
6. update the ticket critique disposition for open findings, or cite withdrawn
   findings only as audit history when their critique rationale is sufficient

Do not partially implement a multi-item review when some items are unclear and
could affect the others. Clarify first or split the work into explicit follow-up
tickets.

If feedback is wrong, push back with evidence: cite code, tests, specs, tickets,
or project decisions. Avoid performative agreement; the useful durable artifact is
the technical disposition.
