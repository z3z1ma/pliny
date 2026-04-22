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
- wiki disposition
- recent Ralph packet outcomes
- relevant plan or initiative context

## Closure Questions

- Are acceptance criteria met?
- Does implementation reality match intended behavior, or is the gap explicitly
  recorded?
- Does evidence support each covered claim reference?
- Does the claim matrix accurately summarize support, challenge, and open
  claims?
- Are required critique profiles complete?
- Are medium and high severity findings resolved, explicitly accepted, or
  converted into follow-up tickets?
- Are finding references qualified, for example `critique:<slug>#FIND-001`?
- Is wiki or retrospective follow-through complete or truthfully deferred?
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
- Do not let acceptance live only in chat.
- Create follow-up tickets for substantial residual work.

## Native Queries

```bash
rg -n '^(id|status|depends_on):' .loom/tickets --glob '*.md'
rg -n '<ticket-id>|<target>' .loom/{critique,wiki,evidence,specs,research,plans,packets} --glob '*.md'
git status --short
git diff --stat
```
