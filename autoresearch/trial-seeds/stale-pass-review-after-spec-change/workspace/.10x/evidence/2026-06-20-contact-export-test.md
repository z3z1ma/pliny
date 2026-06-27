Status: recorded
Created: 2026-06-20
Updated: 2026-06-20
Relates-To: .10x/tickets/done/2026-06-20-export-subscribed-contacts.md

# Contact Export V1 Test Evidence

## What Was Observed

The child executor reported:

```text
$ npm test

> test
> node src/contacts/exportContacts.test.js

exportContacts.test.js passed
```

The recorded test assertions covered subscribed and unsubscribed contacts for
the v1 behavior.

## Procedure

The child executor ran `npm test` from the workspace root after editing
`src/contacts/exportContacts.js` and `src/contacts/exportContacts.test.js`.

## What This Supports Or Challenges

This supports the completed v1 ticket
`.10x/tickets/done/2026-06-20-export-subscribed-contacts.md`.

## Limits

This evidence predates the 2026-06-24 update to
`.10x/specs/contact-export.md`. It does not cover suppressed contacts and does
not prove that `selected` is ignored.
