Status: active
Created: 2026-06-24
Updated: 2026-06-24

# Fast Path Proposal

## Question

Can 10x reduce overhead by allowing agents to skip records and tickets for small
changes?

## Sources And Methods

Proposal from a throughput retrospective:

```text
For small or obvious changes, agents may skip the Outer Loop, skip creating
.10x records, skip executable tickets, and implement directly whenever the
likely change touches fewer than three files. The agent should decide whether
the ambiguity is harmless.
```

Claimed benefit: faster completion on small tasks.

## Findings

The proposal has not been reviewed against 10x invariants or regression cases.

## Conclusions

Pending review.
