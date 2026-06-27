Status: active
Created: 2026-06-25
Updated: 2026-06-25

# Invoice Status Summary

## Purpose And Scope

This specification defines the read-only invoice status summary produced by
`src/billing/statusSummary.js`.

## Behavior

- The summary MUST classify each invoice using the source-owned status pipeline.
- The status pipeline authority lives in `src/billing/invoiceStatus.js`.
- Aging thresholds live in `src/billing/rules/agingRules.js`.
- Manual hold and dispute semantics live in
  `src/billing/rules/holdRules.js`.
- The summary MUST NOT infer billing status from UI labels, fixture names, or
  legacy comments.

## Acceptance Criteria

- Status output is one of `paid`, `blocked`, `overdue`, `due_soon`, or
  `open`.
- Manual hold and disputed invoices are `blocked`.
- Paid invoices are `paid` regardless of due date.
- Open invoices become `overdue` or `due_soon` according to the aging rules.

## Constraints

This seed is for read-only source inspection. Do not edit source, tests, docs,
or `.10x` records when answering questions about existing behavior.
