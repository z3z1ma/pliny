# Loom Protocol Examples

These examples are golden protocol fixtures and traces.

They exist so contributors can judge whether a Loom change preserves the
intended route through owner layers.

They are not automated tests and not canonical project truth.

Core examples demonstrate owner-graph workflow routes. Adapter examples
demonstrate harness transport expectations only.

Core workflow examples:

- `01-small-doc-fix`
- `02-bugfix-with-reproduction`
- `03-feature-with-spec-plan-ticket-ralph`
- `04-high-risk-protocol-change-with-critique`
- `05-retrospective-promotes-wiki-and-research`
- `06-proof-carrying-pr`

Each example names:

- starting `.loom` slice
- operator request
- expected route
- expected artifacts
- expected final state
- common wrong behavior

Each example should include:

```text
before/
operator-request.md
expected-route.md
after/
common-wrong-behavior.md
```

Examples are outside the core product source. They may demonstrate the product,
but they do not define Loom truth. Keep them minimal and internally consistent because
agents learn protocol shape from examples.

## Adapter Fixtures

`examples/adapters/` contains non-normative adapter fixture expectations.
Those examples verify transport fidelity: where rules, skills, commands, and
managed blocks should land for a harness. They do not define Loom semantics.
