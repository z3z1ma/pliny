# Candidate: Audit Limits Redaction

Candidate ID: `candidate-audit-limits-redaction-v1`
Created: 2026-06-28
Canonical target: `SKILL.md`
Status: draft
Promotion: manual-only

## Target Behavior

Improve `S010` for evidence and research records by making auditability and
redaction shape explicit.

## Proposed Instruction Overlay

Add near Evidence and Research:

```text
Evidence and research records are audit notes, not summaries. Preserve the
procedure, exact observation, raw artifact path, what the observation supports
or challenges, and limits or null results. When redacting, keep enough field
shape, prefixes/classes, counts, and surrounding nonsecret output to audit the
claim without exposing secrets. Never let a passing command, child report, or
sanitized excerpt imply broader behavior than it proves.
```

## Expected Score Movement

- Strongest on evidence-overclaim, redaction, and research-capture seeds.
- Should preserve evidence integrity while improving cold-start auditability.

## Expected Failure Modes

- Subject quotes too much raw output or leaks sensitive values.
- Subject creates evidence records for claims that do not need durability.
