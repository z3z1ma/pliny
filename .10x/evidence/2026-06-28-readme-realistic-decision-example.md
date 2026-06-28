Status: recorded
Created: 2026-06-28
Updated: 2026-06-28
Relates-To: .10x/tickets/done/2026-06-28-replace-readme-meta-decision-example.md, README.md

# README Realistic Decision Example

## What Was Observed

The README decision-record example was changed from an internal install-path
decision to a realistic billing-webhook idempotency decision.

The new example:

- is product-facing rather than meta;
- uses plausible `.10x/` links to research, specs, evidence, and follow-up
  tickets;
- names authority and provenance;
- distinguishes current source drift from intended behavior;
- records rejected alternatives and consequences;
- leaves unresolved retry/dead-letter/alert ownership blocked.

The before/after section now uses the same webhook idempotency scenario, so the
example and story stay coherent.

## Procedure

1. Inspected the current README example.
2. Replaced the internal install-path example with a realistic billing webhook
   decision.
3. Updated the before/after section to match the new example.
4. Ran validation checks.

Observed checks:

```text
python3 autoresearch/validate.py
autoresearch contracts valid

python3 -m unittest discover -s autoresearch/tests
Ran 60 tests
OK

git diff --check
<no output>

local README link check
checked 6 local markdown links
```

## What This Supports Or Challenges

Supports closing the README example replacement ticket. The README now presents
a realistic rich record from a prospective user's point of view instead of
exposing internal README/install deliberation.

## Limits

The example is illustrative, not an actual product record from this repository.
It is intentionally realistic rather than repo-internal.
