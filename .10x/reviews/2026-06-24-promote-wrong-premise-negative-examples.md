Status: recorded
Created: 2026-06-24
Updated: 2026-06-24
Target: SKILL.md
Verdict: pass

# Promote Wrong Premise Negative Examples

## Target

Promotion of
`autoresearch/candidates/2026-06-24-wrong-premise-negative-examples.md` into
`SKILL.md` after
`EXP-20260624-873-wrong-premise-negative-examples-scn001-live-micro`.

## Findings

- **Pass:** The promoted text strengthens an existing invariant instead of
  adding a new process branch.
- **Pass:** The examples target the observed failure mode: familiar permission,
  lifecycle, notification, migration, source-field, and test patterns can make
  invented requirements look locally correct.
- **Pass:** The candidate outperformed current on manual inspection by refusing
  to rewrite active knowledge or create a partly ratified blocked ticket from a
  conflicting request.
- **Pass:** The language is concise enough to avoid example bloat.
- **Residual risk:** Examples can never be exhaustive. Future runs should watch
  for agents treating only the listed examples as wrong-premise risks.

## Verdict

Pass. Promote the concise negative examples into `SKILL.md`.

## Residual Risk

The next held-out check should test a different familiar pattern, such as
notifications or lifecycle migrations, to confirm the examples generalize beyond
role permissions.
