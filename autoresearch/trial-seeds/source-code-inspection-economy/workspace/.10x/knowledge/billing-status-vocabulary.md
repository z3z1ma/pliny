Status: active
Created: 2026-06-25
Updated: 2026-06-25

# Billing Status Vocabulary

## Glossary

- `blocked`: invoice requires human action before collection, currently caused
  by manual hold or dispute flags.
- `overdue`: invoice is open and past the grace-adjusted due date.
- `due_soon`: invoice is open and due within the configured due-soon window.
- `open`: invoice is not paid, blocked, overdue, or due soon.

## Convention

Use source identifiers when describing behavior. UI labels and fixture names are
descriptive hints, not behavior authority.
