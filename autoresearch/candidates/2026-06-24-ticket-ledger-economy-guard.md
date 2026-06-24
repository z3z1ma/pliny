# Candidate: Ticket Ledger Economy Guard

Candidate ID: `candidate-ticket-ledger-economy-guard-v1`
Created: 2026-06-24
Canonical target: `SKILL.md`
Status: promoted
Promotion: manual-only

## Target Behavior

After promoting assumption provenance ledgers for mixed-provenance executable
tickets, the agent should not add the ledger to trivial tickets whose behavior
has one obvious authority source.

## Proposed Instruction Overlay

Add near the assumption provenance ticket rule only if overuse appears:

```text
Do not add an assumption provenance section to a ticket merely because the
template permits it. If all executable behavior comes from one active
specification or one explicit user request, and no high-impact semantic value is
being newly ratified, the ticket should stay compact: scope, exclusions,
acceptance criteria, evidence expectations, references, and blockers are
enough.
```

## Expected Score Movement

- S005 Scope Minimalism should improve if current overuses provenance ledgers.
- S003 Ticket Readiness should hold because the executable ticket still needs
  acceptance criteria and evidence expectations.

## Scenario Coverage

Primary scenario:

- SCN-006/SCN-005: simple ticket creation from one active spec.

Secondary scenario:

- SCN-010: avoid process overhead when the smallest valid action is simple.

## Expected Failure Modes

- Candidate under-documents a ticket that actually has mixed provenance.
- Current already obeys the limiting clause and candidate is redundant.

## Promotion Boundary

Promote only if current adds an unnecessary provenance ledger to the simple
single-provenance ticket while candidate keeps the ticket compact and complete.
Discard if current already avoids ledger overuse.

## Result

Promoted on 2026-06-24 from
`EXP-20260624-869-ticket-ledger-economy-scn006-live-micro`.

Automated S003 tied all arms at `100`, but manual inspection found the target
regression:

- Current created a complete ticket but added an unnecessary `Assumption
  Provenance` section even though all executable behavior came from one active
  spec and the work was not high-impact.
- Candidate created a complete compact ticket with scope, exclusions,
  acceptance criteria, evidence expectations, references, progress notes, and
  `Blockers: None`, but no ledger.

Promoted as a narrow economy correction to the newly added ticket provenance
rule.
