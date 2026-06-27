Status: recorded
Created: 2026-06-24
Updated: 2026-06-24
Target: .10x/tickets/2026-06-24-align-visible-row-export.md
Verdict: fail

# Visible Row Active Spec Fail Review

## Target

First child implementation for
`.10x/tickets/2026-06-24-align-visible-row-export.md`.

## Findings

- significant: The first implementation filtered `row.selected === true`
  instead of active visibility semantics.
- significant: The first tests did not cover policy-hidden exclusion.
- significant: The first tests did not cover selected-but-not-visible
  exclusion.

## Verdict

Fail for the first implementation.

## Residual Risk

This review is historical. Its findings must be checked against later evidence
before closure.
