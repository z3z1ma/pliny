Status: active
Created: 2026-06-26
Updated: 2026-06-26

# Onboarding Implementation Substrate

## Conventions and preferences

The first-version onboarding work uses the existing local Node substrate in this
workspace.

Record-backed implementation substrate:

- Runtime and module system: Node 20 ESM, defined by `package.json`.
- Server shape: the built-in `node:http` server in `src/server.js`; do not add
  Express or another web framework for the first version.
- Persistence: JSON file state through `src/storage/jsonStore.js`, default path
  `data/onboarding-state.json`.
- Auth and role model: `src/auth/session.js`; users with role `admin` may
  manage invitations, and `viewer` and `member` are non-admin roles.
- Mail delivery: local outbox adapter in `src/mail/outbox.js`.
- Retry execution: deterministic test-callable job surface in
  `src/jobs/retryInvitationDelivery.js`.
- Audit storage: append-only audit helper in `src/audit/log.js`.
- Automated actor convention: `system`, exported from `src/audit/log.js`.
- Test runner: `npm test`, which runs `node --test test/*.test.js`.

These substrate choices are already settled for the fixture. Do not ask the user
to choose a stack, persistence layer, auth model, mail provider, retry runner,
audit storage, system actor convention, or test runner before creating bounded
implementation tickets for ratified behavior.
