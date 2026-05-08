# Interface And Seam Design

Use this reference when architecture work needs the concrete interface discipline
behind `loom-architecture`. Current structure still belongs to code and codemap;
intended behavior belongs to specs; execution belongs to plans, tickets, and
packets.

## Vocabulary

- Module: anything with an interface and an implementation: function, class,
  package, service slice, component, or workflow unit.
- Interface: everything a caller must know to use the module: types, invariants,
  errors, ordering, config, side effects, and compatibility promises. It is more
  than a type signature.
- Implementation: the code behind the interface.
- Depth: leverage at the interface. A deep module gives a lot of behavior through
  a small, clear interface. A shallow module exposes almost as much complexity as
  it hides.
- Seam: where behavior can be altered without editing all callers in place.
- Adapter: a concrete implementation satisfying an interface at a seam.
- Locality: change, bugs, and knowledge are concentrated near the concept.

## Architecture Friction Signals

Look for:

- understanding one concept requires bouncing through many small modules
- shallow modules whose interface is nearly as complex as their implementation
- pure functions extracted only for testability while real bugs hide in orchestration
- tightly coupled modules leaking implementation details across seams
- public or internal APIs returning inconsistent shapes
- tests that must change for internal refactors
- repeated packet/context discovery for the same module paths
- multiple consumers relying on undocumented behavior

Use the deletion test: if deleting a module makes complexity vanish, it was likely
a pass-through. If deleting it spreads complexity across many callers, it was
earning its keep.

## Dependency Categories

Classify dependencies before choosing a seam:

| Category | Description | Testing strategy |
| --- | --- | --- |
| In-process | Pure computation or in-memory state, no IO | Deepen directly and test through the new interface |
| Local-substitutable | Dependency has a local test stand-in, such as in-memory filesystem or local database | Test deep module with the stand-in; do not expose the seam unnecessarily |
| Remote but owned | Internal service across network boundary | Define a port at the seam; production adapter uses transport, tests use local adapter |
| True external | Third-party service you do not control | Inject a port; tests use mocks or contract fixtures |

Seam discipline:

- one adapter means a hypothetical seam
- two adapters usually means a real seam
- do not expose internal seams just because tests use them
- the interface is the test surface
- old shallow-module tests should be deleted when deeper interface tests cover the behavior

## Contract-First Interface Design

Define the interface before implementation when consumers or modules depend on it.
The spec owns the contract. A good contract states:

- inputs and outputs
- invariants
- error semantics
- idempotency and ordering
- side effects
- permission or trust-boundary requirements
- compatibility and deprecation rules
- observability that consumers may depend on

Do not rely on implementation prose to define the contract after the fact.

## Hyrum's Law Checks

With enough consumers, every observable behavior becomes depended on. Before
changing an interface, inspect:

- documented contract
- real call sites
- tests and fixtures
- logs/metrics or observed usage when available
- error text/status/shape
- ordering and pagination
- timing or retry behavior when visible
- undocumented fields or default values

Prefer additive evolution: add optional fields or new endpoints before changing or
removing existing behavior. Breaking changes require migration/deprecation routing.

## Error Semantics

Pick one strategy and use it consistently. For HTTP APIs, define status codes and
structured error bodies. For module APIs, define whether errors are thrown,
returned, nullable, or represented as result objects.

Common HTTP mapping:

- 400: malformed request
- 401: not authenticated
- 403: authenticated but not authorized
- 404: resource not found
- 409: conflict or version mismatch
- 422: semantically invalid input
- 500: server error with no internal details exposed

Mixed error strategies make interfaces hard to use and hard to test.

## Validation Boundary

Validate external input at boundaries:

- API route handlers
- form submissions
- webhook payloads
- third-party API responses
- environment/config loading
- file uploads

Do not scatter validation between internal functions that already share a trusted
contract. Boundary validation plus trusted internal types improves locality.

Third-party API responses are untrusted data. Validate their shape before using
them in logic, rendering, storage, or agent decisions.

## REST And Data Interface Patterns

Use consistent resource naming:

- nouns, not verbs: `/api/tasks`, not `/api/createTask`
- query params for filtering and sorting
- pagination for list endpoints before scale makes it painful
- PATCH for partial updates when clients do not send complete objects
- separate input shape from output shape when outputs include server-generated fields

Type/interface patterns:

- use discriminated unions for variants with different fields
- use branded or domain-specific ID types when accidental cross-use is likely
- keep boolean names predictable: `is`, `has`, `can`, `should`
- make default cases trivial for the common caller

## Designing Alternatives

When the best seam is not obvious, design it more than once. Produce three
radically different interfaces:

- minimal interface: one to three entry points, maximum leverage per entry point
- flexible interface: supports likely extension points explicitly
- common-case interface: optimizes the default caller path
- ports/adapters interface: when cross-process or external dependencies matter

For each option, record:

- interface sketch
- usage example
- hidden implementation behind the seam
- dependency/adapters strategy
- tradeoffs in depth, locality, compatibility, and testing

Route the comparison to research. Route the chosen behavior contract to spec.

## Review Questions

- Is the interface smaller and clearer than the implementation complexity it hides?
- Would tests through the interface survive internal refactors?
- Does the design concentrate change near the domain concept?
- Are dependency categories and adapters justified?
- Are error semantics and validation boundaries consistent?
- Are compatibility and migration concerns explicit?
- Is this a real seam or a single-adapter indirection layer?
