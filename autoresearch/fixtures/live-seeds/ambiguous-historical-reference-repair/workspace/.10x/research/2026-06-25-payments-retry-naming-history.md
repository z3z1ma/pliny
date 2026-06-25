Status: done
Created: 2026-06-25
Updated: 2026-06-25

# Payments Retry Naming History

## Question

Why did the payments retry spec originally use "retry window"?

## Sources And Methods

Reviewed early notes and record search output.

## Findings

The first version of the record focused on duration and lived at
`.10x/specs/payments-retry-window.md`. Later review expanded the durable term to
"payments webhook retry policy".

Historical `rg` output from before the rename:

```text
.10x/specs/payments-retry-window.md:5:# Payments Retry Window
.10x/specs/superseded/payments-local-retry-notes.md:25:Superseded by .10x/specs/payments-retry-window.md
```

## Conclusions

The active record should move to the durable term. Historical notes should keep
the old path where they describe past state.
