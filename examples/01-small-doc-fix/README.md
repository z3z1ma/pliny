# 01 - Small Doc Fix

## Starting `.loom` Slice

- `constitution:main`
- one active wiki page with a broken link
- no open ticket for the typo or link

## Operator Request

"Fix the broken link in the wiki page."

## Expected Route

Local edit is acceptable when the change is tiny, low risk, and does not widen
scope.

Route:

1. orient enough to confirm Loom is present
2. read `constitution:main`
3. inspect the target wiki page
4. fix the link
5. run a targeted reference check

## Expected Artifacts

- updated wiki page
- no new initiative, plan, ticket, packet, or critique unless the link exposes
  broader graph drift

## Expected Final State

- link resolves or is explicitly marked stale
- `git diff` is small and limited to the target page

## Common Wrong Behavior

- creating a ticket for a trivial local fix
- treating the wiki page as a behavior spec
- claiming all docs were validated after checking only one link
