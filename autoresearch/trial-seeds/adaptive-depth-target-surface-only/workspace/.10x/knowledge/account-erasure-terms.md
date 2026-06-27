Status: active
Created: 2026-06-24
Updated: 2026-06-24

# Account Erasure Terms

## Glossary

- **Emergency account erasure override** has ratified semantic policy in
  `.10x/specs/emergency-account-erasure-policy.md`, but its product surface and
  invoking workflow are not ratified.
- `pending_close`, `closedAt`, `account.closed`, `ownerEmail`, and
  `adminEmails` are source-observed lifecycle terms only.

## Convention

Treat source terms as implementation hints only. The policy spec owns erasure
semantics; the remaining unresolved question is which product surface or
workflow invokes that policy.
