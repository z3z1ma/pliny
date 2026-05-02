# Claim Coverage

Claim coverage is Loom's lightweight trace from intended behavior to evidence and
review.

It is intentionally plain text. Stable IDs and ordinary search should answer
which records cover, support, or challenge a claim.

## ID Shapes

Use local IDs inside the record that owns the criterion or claim:

- `OBJ-001` for initiative objective criteria under Success Metrics
- `REQ-001` for requirements
- `ACC-001` for acceptance units in the spec or ticket that owns the acceptance
  contract
- `CLAIM-001` for non-spec claims that need traceability

Keep IDs stable after downstream records refer to them. If a claim is split,
mark the old ID as superseded in prose and introduce new IDs.

## Cross-Record References

Local IDs are not globally unique. When one record refers to a claim in another
record, qualify the ID with the owning record ID:

```text
initiative:<slug>#OBJ-001
spec:<slug>#ACC-001
ticket:<token>#ACC-001
research:<slug>#CLAIM-002
```

Use unqualified IDs only inside the owning record or in a tightly local section
where the owner is unmistakable.

## Initiative Shape

Initiatives own `OBJ-*` criteria under their Success Metrics. Use them for
strategic objective criteria that downstream plans, tickets, evidence, or
critique may need to cite:

```md
# Success Metrics

- OBJ-001: Operators can find the shared grammar surface for the record kinds in current supported use.
- OBJ-002: Downstream tickets can cite the initiative objective they advance.
```

Tickets may cover `initiative:<slug>#OBJ-001`, but the ticket owns only its
scoped coverage state, evidence disposition, critique disposition, and closure
decision. If the objective criterion itself changes, update the initiative.

## Spec Shape

Specs should give important requirements and acceptance units IDs:

```md
# Requirements

- REQ-001: The ticket acceptance gate refuses to close a ticket with unresolved high-severity critique.
- REQ-002: The ticket acceptance gate reports missing evidence before changing ticket status.

# Acceptance

- ACC-001: Given unresolved high-severity critique, the ticket acceptance gate leaves the ticket open.
- ACC-002: Given missing evidence, the ticket acceptance gate reports the gap and leaves a concrete next step.
```

## Ticket Shape

Tickets that advance an initiative objective or implement/verify a spec should
name covered objective and acceptance IDs:

First decide which acceptance owner applies. If a spec owns the reusable
acceptance contract, cite the spec-owned IDs under `# Coverage` and do not create
ticket-local `ACC-*` criteria for that contract:

```md
# Coverage

Covers:
- initiative:<slug>#OBJ-001
- spec:<slug>#ACC-001
- spec:<slug>#ACC-002
```

Replace placeholder refs with real claim IDs before saving a real ticket.

When no spec owns the acceptance contract, the ticket may own ticket-local
acceptance criteria. Write the local IDs in `# Acceptance Criteria` and cite them
from packets, evidence, and critique as `ticket:<token>#ACC-001`:

```md
# Acceptance Criteria

- ACC-001: The ticket readiness template is route-neutral.
- ACC-002: Evidence records the structural validation outputs.

# Coverage

Covers:
- initiative:<slug>#OBJ-001
- ticket:<token>#ACC-001
- ticket:<token>#ACC-002
```

Do not use ticket-local `ACC-*` IDs to replace a reusable spec-owned acceptance
contract. If the criterion should guide future tickets, promote or restate it in
a spec and cite `spec:<slug>#ACC-001` instead.

Tickets nearing acceptance may also carry a claim matrix. The matrix is a
ticket-owned view over links; it is not a new truth owner.

```md
# Claim Matrix

| Claim | Evidence | Critique | Status |
| --- | --- | --- | --- |
| initiative:<slug>#OBJ-001 | evidence:<slug> | critique:<slug>#FIND-002 resolved | supported_pending_review |
| spec:<slug>#ACC-001 | evidence:<slug> | critique:<slug>#FIND-001 resolved | supported |
| ticket:<token>#ACC-001 | evidence:<slug> | pending | supported_pending_review |
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

- initiative:<slug>#OBJ-001
- spec:<slug>#ACC-001
- ticket:<token>#ACC-001
```

## Evidence Shape

Evidence should name claims it supports:

```md
# Supports Claims

- initiative:<slug>#OBJ-001
- spec:<slug>#ACC-001
- spec:<slug>#ACC-002
- ticket:<token>#ACC-001
```

## Critique Shape

Critique findings should name claims they challenge when applicable:

```md
Challenges:
- initiative:<slug>#OBJ-001
- spec:<slug>#ACC-002
- ticket:<token>#ACC-001
```

## Useful Queries

```bash
rg -n 'initiative:<slug>#OBJ-001' .loom
rg -n '\bOBJ-[0-9]{3}\b' .loom/initiatives skills/loom-initiatives
rg -n 'spec:<slug>#ACC-002' .loom
rg -n 'ticket:<token>#ACC-001' .loom
rg -n '^# Supports Claims|^Supports:' .loom/evidence
rg -n '^Challenges:' .loom/critique
rg -n '^# Coverage|^Covers:' .loom/tickets
```

## Discipline

Do not invent IDs for every sentence. Use claim coverage for behavior,
acceptance, evidence, or critique relationships that future agents will need to
trace.
