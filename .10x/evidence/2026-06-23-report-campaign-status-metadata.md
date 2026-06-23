Status: recorded
Created: 2026-06-23
Updated: 2026-06-23
Relates-To: .10x/tickets/2026-06-23-propagate-campaign-statuses-to-reports.md

# Report Campaign Status Metadata

## What Was Observed

`autoresearch/report.py` now accepts optional campaign metadata through:

```text
python3 autoresearch/report.py --scores path/to/scores --campaign path/to/campaign.json --out path/to/report.md
```

The report renders a `## Campaign Verdict` section when metadata is supplied.
It includes campaign/candidate/baseline identifiers, verdict, result status,
promotion decision, statuses, manual inspection state, evidence references, and
limits when those fields are present.

The report explicitly states that campaign verdict metadata is
manual/contextual and does not modify score artifacts or upgrade scorer trust.

Unit tests passed:

```text
$ python3 -m unittest autoresearch.tests.test_report
Ran 5 tests in 0.025s
OK
```

The unit-test campaign metadata fixture includes:

```text
## Campaign Verdict
verdict = null
result_status = confounded
promotion_decision = not-performed
statuses = null; confounded
```

`autoresearch/tests/test_report.py` also covers the absence path: when no
campaign metadata is supplied, no campaign section is rendered.

## Procedure

1. Added optional campaign metadata loading to `autoresearch/report.py`.
2. Kept campaign metadata separate from `*.score.json` artifacts.
3. Added tests for a null/confounded campaign and for a report without campaign
   metadata.
4. Validated report rendering through unit tests.

## What This Supports Or Challenges

This supports:

- `.10x/tickets/2026-06-23-propagate-campaign-statuses-to-reports.md#AC-001`
- `.10x/tickets/2026-06-23-propagate-campaign-statuses-to-reports.md#AC-002`
- `.10x/tickets/2026-06-23-propagate-campaign-statuses-to-reports.md#AC-003`
- `.10x/tickets/2026-06-23-propagate-campaign-statuses-to-reports.md#AC-004`

This challenges the prior first calibration report behavior where campaign-level
null/confounded status was visible only in `.10x/` prose records.

## Limits

This evidence does not show that a campaign verdict is correct. It only shows
that, when supplied, campaign metadata is rendered without changing automated
score artifacts.
