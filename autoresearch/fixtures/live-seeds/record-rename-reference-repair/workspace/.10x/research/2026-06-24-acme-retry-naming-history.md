Status: done
Created: 2026-06-24
Updated: 2026-06-24

# ACME Retry Naming History

## Question

Why did the ACME webhook retry behavior start under the path
`.10x/specs/acme-retry-window.md`?

## Sources And Methods

- Inspected the active specification at `.10x/specs/acme-retry-window.md`.
- Inspected the implementation ticket that depends on the specification.
- Recorded the reference search below before the rename was authorized.

```text
$ rg ".10x/specs/acme-retry-window.md" .10x
.10x/tickets/2026-06-24-implement-acme-webhook-retry.md:Depends-On: .10x/specs/acme-retry-window.md
.10x/evidence/2026-06-24-acme-retry-source-inspection.md:Relates-To: .10x/specs/acme-retry-window.md, .10x/tickets/2026-06-24-implement-acme-webhook-retry.md
.10x/reviews/2026-06-24-acme-retry-spec-review.md:Target: .10x/specs/acme-retry-window.md
```

## Findings

The old path `.10x/specs/acme-retry-window.md` reflects an early shorthand.
Product and Engineering later ratified "ACME webhook retry policy" as the
durable term for the same behavior.

## Conclusions

The record path should be renamed. Historical notes and captured command output
should continue to show the old path as history.
