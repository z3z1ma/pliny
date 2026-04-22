# Claim Coverage

Claim coverage is Loom's lightweight trace from intended behavior to proof and
review.

It is intentionally plain text. Stable IDs and ordinary search should answer
which records cover, support, or challenge a claim.

## ID Shapes

Use local IDs inside a spec or closely related record:

- `REQ-001` for requirements
- `ACC-001` for acceptance units
- `CLAIM-001` for non-spec claims that need traceability

Keep IDs stable after downstream records refer to them. If a claim is split,
mark the old ID as superseded in prose and introduce new IDs.

## Cross-Record References

Local IDs are not globally unique. When one record refers to a claim in another
record, qualify the ID with the owning record ID:

```text
spec:acceptance-hardening#ACC-001
research:packet-safety#CLAIM-002
```

Use unqualified IDs only inside the owning record or in a tightly local section
where the owner is unmistakable.

## Spec Shape

Specs should give important requirements and acceptance units IDs:

```md
# Requirements

- REQ-001: The command refuses to close a ticket with unresolved high-severity critique.
- REQ-002: The command reports missing evidence before changing ticket status.

# Acceptance

- ACC-001: Given unresolved high-severity critique, `/loom-accept` leaves the ticket open.
- ACC-002: Given missing evidence, `/loom-accept` reports the gap and leaves a concrete next step.
```

## Ticket Shape

Tickets that implement or verify a spec should name covered acceptance IDs:

```md
# Coverage

Covers:
- spec:acceptance-hardening#ACC-001
- spec:acceptance-hardening#ACC-002
```

Tickets nearing acceptance may also carry a claim matrix. The matrix is a
ticket-owned view over links; it is not a new truth owner.

```md
# Claim Matrix

| Claim | Evidence | Critique | Status |
| --- | --- | --- | --- |
| spec:acceptance-hardening#ACC-001 | evidence:acceptance-red-green | critique:acceptance-review#FIND-001 resolved | supported |
```

Use this status vocabulary:

- `open` — no sufficient support or challenge has been reconciled yet
- `supported` — evidence supports the claim and required review is complete or not required
- `supported_pending_review` — evidence supports the claim but required critique or acceptance review remains
- `challenged` — evidence or critique currently challenges the claim
- `accepted_risk` — the claim has a known challenge or limitation accepted by the ticket owner
- `superseded` — the claim reference has been replaced by a successor

## Packet Shape

Packets should declare the verification targets for the bounded iteration:

```md
# Verification Targets

- spec:acceptance-hardening#ACC-001
```

## Evidence Shape

Evidence should name claims it supports:

```md
# Supports Claims

- spec:acceptance-hardening#ACC-001
- spec:acceptance-hardening#ACC-002
```

## Critique Shape

Critique findings should name claims they challenge when applicable:

```md
Challenges:
- spec:acceptance-hardening#ACC-002
```

## Useful Queries

```bash
rg -n 'spec:acceptance-hardening#ACC-002' .loom
rg -n '^# Supports Claims|^Supports:' .loom/evidence
rg -n '^Challenges:' .loom/critique
rg -n '^# Coverage|^Covers:' .loom/tickets
```

## Discipline

Do not invent IDs for every sentence. Use claim coverage for behavior,
acceptance, proof, or critique relationships that future agents will need to
trace.
