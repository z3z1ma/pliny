# Acceptance Gate

Acceptance is the fail-closed decision for ticket closure.

`closed` means the durable story is coherent. It is not a synonym for finished
implementation.

## Inputs

- ticket
- change class and risk class
- linked spec and coverage IDs
- ticket claim matrix when present
- evidence
- critique records and finding dispositions
- critique policy: `optional`, `recommended`, or `mandatory`, plus rationale and
  disposition status `pending`, `completed`, `deferred`, or `not_required`
- wiki disposition
- recent Ralph packet outcomes
- relevant plan or initiative context

## Acceptance Dossier

The acceptance dossier is the composed ticket-owned view used for closure.
It is not a new record kind.

```text
Acceptance Dossier =
  Acceptance Criteria
  + Coverage
  + Claim Matrix
  + Evidence
  + Critique Policy
  + Critique Disposition
  + Wiki Disposition
  + Journal
  + Acceptance Decision when required
```

## Closure Questions

- Are acceptance criteria met?
- Does implementation reality match intended behavior, or is the gap explicitly
  recorded?
- Does evidence support each covered claim reference?
- Is the evidence fresh enough for the current source, record, dependency, and
  environment state, or are its limits explicit?
- Does the claim matrix accurately summarize support, challenge, and open
  claims?
- Is critique policy explicit enough for this change class and risk class?
- When critique policy requires profiles, are those profiles complete?
- If critique is mandatory, does required critique exist and are medium/high
  findings resolved, explicitly accepted as risk, or converted into linked
  follow-up tickets?
- If critique is recommended but not performed, does the ticket record why it
  was deferred or intentionally not needed before closure?
- For any existing critique, are medium and high severity findings resolved,
  explicitly accepted, or converted into follow-up tickets?
- Are finding references qualified, for example `critique:<slug>#FIND-001`?
- Is wiki or retrospective follow-through complete or truthfully deferred?
- If human signoff or accepted-risk provenance is required, does
  `# Acceptance Decision` name who accepted, when, on what basis, and with what
  residual risks?
- Are links and status fields coherent?

## Outcomes

- `closed`: durable story is complete and coherent
- `complete_pending_acceptance`: work is substantially done but an acceptance
  step remains
- `review_required`: critique is still the next governed move
- `active`: implementation is still underway
- `blocked`: a named blocker prevents progress

## Guardrails

- Fail closed.
- Do not close because the code feels done.
- Do not close over unresolved required critique.
- Do not close over missing mandatory critique.
- Do not close over recommended critique without a ticket-owned disposition.
- Do not let acceptance live only in chat.
- Create follow-up tickets for substantial residual work.

## Acceptance Provenance

For regulated work, accepted risk, or explicit human gates, record:

```md
# Acceptance Decision

Accepted by:
Accepted at:
Basis:
Residual risks:
```

Leave fields blank only while the ticket is not yet accepted.

## Native Queries

```bash
rg -n '^(id|status|depends_on):' .loom/tickets --glob '*.md'
rg -n '<ticket-id>|<target>' .loom/{critique,wiki,evidence,specs,research,plans,packets} --glob '*.md'
git status --short
git diff --stat
```
