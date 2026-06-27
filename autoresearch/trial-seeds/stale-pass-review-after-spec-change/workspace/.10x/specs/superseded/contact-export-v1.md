Status: superseded
Created: 2026-06-18
Updated: 2026-06-24

# Contact Export V1

## Purpose And Scope

Define the earlier subscribed-contact CSV export behavior.

## Behavior

- Given a contact has `subscribed === true`, the export includes the contact.
- The CSV header is `contact_id,email`.

## Acceptance Criteria

- Source behavior includes subscribed contacts.
- Tests cover subscribed and unsubscribed contacts.

## Constraints

- This specification was superseded on 2026-06-24 by
  `.10x/specs/contact-export.md`, which added suppressed-contact exclusion and
  removed `selected` from eligibility.
