# Change Class

`change_class` says what kind of mutation it is.
`risk_class` says how dangerous the scoped ticket or packet is.

Use change class to choose evidence, critique, and verification posture without
guessing from vibes.

## Values

- `record-hygiene` — links, statuses, filenames, frontmatter, or narrow record cleanup
- `documentation-explanation` — explanatory prose or wiki pages without behavior,
  routing, acceptance, or protocol-authority change
- `behavior-contract` — specs, acceptance criteria, or user-visible intended behavior
- `code-behavior` — source changes that affect runtime behavior
- `code-structure` — behavior-preserving refactor, simplification,
  architecture cleanup, module boundary improvement, or maintainability work
- `validation-instrumentation` — tests, fixtures, smoke checks, CI checks,
  browser checks, harnesses, or other validation surfaces
- `dependency-tooling` — package, runtime, build, lint, typecheck, formatter,
  toolchain, or local automation configuration changes
- `performance-sensitive` — performance, scalability, bundle size, latency,
  memory, hot path, or large-data work where measurement matters
- `ui-product` — user-facing interface, product flow, accessibility, visual
  design, interaction, content, or information-architecture changes
- `protocol-authority` — rules, ownership, acceptance, critique, packet, or truth-boundary changes
- `data-migration` — schema, storage, migration, or persistence changes
- `security-sensitive` — auth, secrets, permissions, injection, or trust-boundary changes
- `release-packaging` — PR, release, handoff, changelog, or external package work

## Default Routing

- `record-hygiene`
  - Default evidence: structural check
  - Default critique: optional
- `documentation-explanation`
  - Default evidence: source comparison
  - Default critique: `operator-clarity` when meaningful
- `behavior-contract`
  - Default evidence: spec diff and acceptance review
  - Default critique: `operator-clarity`
- `code-behavior`
  - Default evidence: test-first or observation-first evidence
  - Default critique: `code-change`, `test-coverage`
- `code-structure`
  - Default evidence: behavior-preservation checks and diff review
  - Default critique: `code-structure`, plus `code-change` when behavior risk is
    plausible
- `validation-instrumentation`
  - Default evidence: red/green check or before/after proof that validation
    catches the intended signal
  - Default critique: `test-coverage`
- `dependency-tooling`
  - Default evidence: install/build/lint/typecheck/test/tool output and
    compatibility notes
  - Default critique: `dependency-tooling`, plus `security` when dependency risk
    matters
- `performance-sensitive`
  - Default evidence: baseline and after measurements or explicit measurement
    limits
  - Default critique: `performance`
- `ui-product`
  - Default evidence: before/after visual, interaction, accessibility, or
    product-task evidence
  - Default critique: `product-ux`, `visual-design`, `accessibility` as
    applicable
- `protocol-authority`
  - Default evidence: structural checks, examples, and reference reconciliation
  - Default critique: `protocol-change`, `operator-clarity`
- `data-migration`
  - Default evidence: before/after and rollback or idempotency evidence
  - Default critique: `data-migration`
- `security-sensitive`
  - Default evidence: threat-focused evidence
  - Default critique: `security`
- `release-packaging`
  - Default evidence: package output compared to owner records
  - Default critique: `operator-clarity`

## Template Use

New tickets must declare both fields in frontmatter:

```yaml
change_class: code-behavior
risk_class: medium
```

When a ticket has several classes, name the primary class in frontmatter and
list secondary classes in the body.

This strictness is intentional: even low-risk governed work needs an explicit
risk and change judgment so evidence, critique, packet posture, and acceptance
can fail closed instead of being inferred from vibes.

Apply this requirement to new tickets and to tickets being materially updated for
readiness, Ralph, critique, acceptance, reopening, or closure. Legacy tickets
without these fields should be normalized when touched or before governed
execution or acceptance; their prior absence does not make them broken merely by
existing.

Packets may repeat or narrow the ticket risk for one iteration, but the ticket
owns the final risk and critique disposition. If a ticket's
`# Review And Follow-Through` restates `risk_class`, that value must match
frontmatter `risk_class`; if it does not, reconcile the ticket before routing
review or closure.

## Discipline

Do not use change class as a substitute for risk judgment.

A `record-hygiene` change can still be high risk if it changes a protocol
owner boundary. A `code-behavior`, `code-structure`, or `ui-product` change can
be low risk if it is small, well-tested, and isolated.

Do not classify a Markdown edit as `documentation-explanation` merely because it
is prose. Rules, skills, templates, acceptance gates, routing guidance, and
operator instructions can be `protocol-authority` or `behavior-contract` changes.
