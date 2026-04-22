---
id: spec:proof-carrying-pr
kind: spec
status: accepted
created_at: 2026-04-22T00:00:00Z
updated_at: 2026-04-22T00:00:00Z
scope:
  kind: repository
  repositories:
    - repo:root
links: {}
external_refs: {}
---

# Summary

Define the package shape for proof-carrying PR summaries.

# Requirements

- REQ-001: A PR package cites the owning ticket and covered acceptance IDs.
- REQ-002: A PR package summarizes evidence, critique findings, residual
  risks, and follow-ups.
- REQ-003: A PR package does not close tickets.

# Acceptance

- ACC-001: Given a ticket with evidence and critique, the PR body names the
  ticket, covered claims, proof, findings, and residual risk.
- ACC-002: Given a ticket not yet accepted, the PR body leaves closure to
  acceptance.
