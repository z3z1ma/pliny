Status: active
Created: 2026-06-20
Updated: 2026-06-24

# Contact Export

## Purpose And Scope

Define the CSV export behavior for the customer contact list. This
specification covers row eligibility and the exported columns. It does not
cover delivery transport, scheduling, or notification copy.

## Behavior

- Given a contact has `subscribed === true` and `suppressed !== true`, the
  export MUST include that contact.
- Given a contact has `suppressed === true`, the export MUST exclude that
  contact even when `subscribed === true`.
- Given a contact has `selected === false`, the export decision MUST ignore
  `selected`; operator selection is no longer part of this export surface.
- The CSV header MUST be exactly `contact_id,email`.

## Acceptance Criteria

- Source behavior excludes suppressed contacts.
- Tests or equivalent evidence cover the suppressed-contact exclusion.
- Tests or equivalent evidence cover that `selected` does not affect export
  eligibility.
- Closure evidence maps the implementation, tests, evidence, and review back
  to this active specification.

## Constraints

- Do not change contact delivery, subscription storage, or notification copy.
- A review or test pass created before this active specification update does
  not establish conformance to the current behavior.
