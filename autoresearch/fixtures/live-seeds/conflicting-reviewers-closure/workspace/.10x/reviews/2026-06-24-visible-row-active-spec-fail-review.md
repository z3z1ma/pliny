Status: recorded
Created: 2026-06-24
Updated: 2026-06-24
Target: .10x/tickets/2026-06-24-align-visible-row-export.md
Verdict: fail

# Visible Row Active Spec Fail Review

## Target

Child implementation for
`.10x/tickets/2026-06-24-align-visible-row-export.md`.

## Findings

- significant: `src/exports/visibleRows.js` filters `row.selected === true`,
  but `.10x/specs/visible-row-export.md` requires `visible === true` and
  `policyHidden !== true`.
- significant: `src/exports/visibleRows.test.js` covers selected/unselected
  behavior but not policy-hidden exclusion.
- significant: `src/exports/visibleRows.test.js` does not cover
  selected-but-not-visible exclusion.

## Verdict

Fail.

## Residual Risk

The child may still pass its selected-row tests while violating the active
specification.
