---
id: evidence:acceptance-red-green
kind: evidence
status: recorded
created_at: 2026-04-22T00:00:00Z
updated_at: 2026-04-22T00:05:00Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  ticket:
    - ticket:bug00001
external_refs: {}
---

# Summary

Red/green proof for high-severity critique blocking acceptance.

# Procedure

1. Capture before behavior from `before/src/acceptance_gate.txt`.
2. Apply the acceptance gate change in `after/src/acceptance_gate.txt`.
3. Compare after behavior to `spec:acceptance-hardening#ACC-001`.

# Artifacts

- `before/src/acceptance_gate.txt`
- `after/src/acceptance_gate.txt`

# Supports Claims

- spec:acceptance-hardening#ACC-001

# Challenges Claims

None.

# Environment

Commit: abcdef0
Branch: bugfix/acceptance-gate
Runtime: fixture
OS: unknown
Relevant config: none

# Validity

Valid for: fixture demonstration of red/green evidence routing.
Recheck when: the acceptance gate workflow or evidence template changes.

# Limitations

Fixture evidence illustrates the route, not a real executable test harness.

# Result

Before: ticket closed despite unresolved high-severity critique.
After: ticket remained open and reported the blocking finding.

# Interpretation

This supports the claim that the acceptance gate now fails closed for the
demonstrated case. It does not prove every acceptance path.

# Related Records

- ticket:bug00001
- spec:acceptance-hardening
