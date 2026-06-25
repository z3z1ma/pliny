Status: done
Created: 2026-06-25
Updated: 2026-06-25

# Payout Export Maintenance History

## Question

Why did older records mention
`.10x/tickets/2026-06-25-align-payout-export-csv.md` at a top-level path?

## Sources And Methods

Reviewed the historical workstream before ticket closure.

## Findings

Before terminal movement, the child ticket correctly lived at
`.10x/tickets/2026-06-25-align-payout-export-csv.md`. That historical sentence
must remain accurate as history after the ticket moves.

Captured command output from before closure:

```text
$ rg 'align-payout-export-csv' .10x
.10x/tickets/2026-06-25-align-payout-export-csv.md:Status: done
.10x/reviews/2026-06-25-payout-export-csv-review.md:Target: .10x/tickets/2026-06-25-align-payout-export-csv.md
```

## Conclusions

Live references should follow the terminal move. Historical prose and captured
command output should preserve the old top-level path.
