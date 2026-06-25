Status: recorded
Created: 2026-06-23
Updated: 2026-06-23
Relates-To: .10x/tickets/done/2026-06-23-autoresearch-static-contracts.md, .10x/specs/10x-autoresearch-loop.md

# Autoresearch Static Contracts Validation

## What Was Observed

The static-contract implementation produced these files:

- `autoresearch/README.md`
- `autoresearch/catalogs/scores.json`
- `autoresearch/catalogs/scenarios.json`
- `autoresearch/templates/experiment.md`
- `autoresearch/templates/manual-inspection.md`
- `autoresearch/schemas/score-artifact.schema.json`

JSON syntax checks completed successfully for:

```text
python3 -m json.tool autoresearch/catalogs/scores.json >/tmp/scores.pretty.json
python3 -m json.tool autoresearch/catalogs/scenarios.json >/tmp/scenarios.pretty.json
python3 -m json.tool autoresearch/schemas/score-artifact.schema.json >/tmp/schema.pretty.json
```

Static ID and field check output:

```text
scores 9 ['S001', 'S002', 'S003', 'S004', 'S005', 'S006', 'S007', 'S008', 'S009']
scenarios 15 SCN-001 SCN-015
scores has schema_version True
scores has source_spec True
scores has scores True
scenarios has schema_version True
scenarios has source_spec True
scenarios has scenarios True
schema has $schema True
schema has type True
schema has required True
schema has properties True
schema required ['experiment_id', 'scenario_id', 'variant_id', 'rep', 'model', 'harness', 'instruction_digest', 'fixture_digest', 'scores', 'cost', 'limits', 'scorer']
```

Acceptance-field check output for the scenario catalog:

```text
scenario_count 15
missing_acceptance_fields none
```

ASCII scan command produced no output:

```text
LC_ALL=C grep -R -n '[^ -~]' autoresearch .10x/tickets/done/2026-06-23-autoresearch-static-contracts.md || true
```

Manual inspection found:

- `autoresearch/README.md` states that `.10x/` remains the durable record graph
  and `autoresearch/` is tooling/static contracts.
- `autoresearch/templates/experiment.md` includes the required registered
  experiment fields from the active spec.
- `autoresearch/templates/manual-inspection.md` includes the required inspection
  checks and recording triggers.
- `autoresearch/catalogs/scenarios.json` uses `fixture_paths` and `fixture_reset`
  as the fixture/reset placeholders for every scenario.

## Procedure

1. Read the active ticket, active spec, decision record, and worker output.
2. Inspected the new static files directly.
3. Parsed all JSON artifacts with `python3 -m json.tool`.
4. Ran a read-only Python check to count scores, count scenarios, and confirm
   required top-level schema fields.
5. Ran a read-only Python check to confirm every scenario has the fields required
   by the ticket acceptance criteria.
6. Ran an ASCII scan over the static contract files and active ticket.

## What This Supports Or Challenges

This supports:

- `.10x/tickets/done/2026-06-23-autoresearch-static-contracts.md#AC-001`
- `.10x/tickets/done/2026-06-23-autoresearch-static-contracts.md#AC-002`
- `.10x/tickets/done/2026-06-23-autoresearch-static-contracts.md#AC-003`
- `.10x/tickets/done/2026-06-23-autoresearch-static-contracts.md#AC-004`
- `.10x/tickets/done/2026-06-23-autoresearch-static-contracts.md#AC-005`
- `.10x/tickets/done/2026-06-23-autoresearch-static-contracts.md#AC-006`

The observation supports static contract shape and coverage. It does not itself
accept the ticket; ticket closure remains a separate judgment.

## Limits

This evidence does not show that:

- The JSON Schema validates a real score artifact.
- A semantic validator exists.
- Scorers, runners, reports, or harness integrations exist.
- Scenario fixtures are concrete enough to run.
- The catalogs are complete enough for every future scoring nuance.

Those checks belong to later tickets in the implementation graph.

