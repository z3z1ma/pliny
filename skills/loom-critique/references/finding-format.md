# Finding Format

Each meaningful finding should normally include:

- a stable ID: `FIND-001`
- a short title
- severity: `low | medium | high`
- confidence: `low | medium | high`
- disposition: `open | resolved | accepted_risk | superseded`
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
critique:<slug>#FIND-001
```

Tickets should use those references when tracking critique disposition.

## Receiving Findings

Treat incoming review feedback as claims to verify, not commands to obey blindly.

For each finding:

1. read the finding completely
2. restate the technical requirement if it is unclear
3. inspect the relevant source, record, evidence, or diff
4. decide whether the finding is valid for this project and ticket scope
5. implement, clarify, accept risk, supersede with evidence, or create follow-up
6. update the ticket critique disposition

Do not partially implement a multi-item review when some items are unclear and
could affect the others. Clarify first or split the work into explicit follow-up
tickets.

If feedback is wrong, push back with evidence: cite code, tests, specs, tickets,
or project decisions. Avoid performative agreement; the useful durable artifact is
the technical disposition.
