# Migration Lifecycle

Use this reference when replacing, deprecating, or removing a system, API, feature,
library, flag, or storage path. Migration truth routes through specs, plans,
tickets, evidence, critique, ship, and retrospective.

## Core Ideas

### Code Is A Liability

Code has ongoing cost: tests, docs, dependencies, security patches, onboarding,
and future comprehension. Code is valuable because of the behavior it provides,
not because it exists. When the same behavior can be delivered with less risk or
less complexity, the old path should eventually go.

### Hyrum's Law Makes Removal Hard

Observable behavior becomes a contract once consumers depend on it. That includes
bugs, ordering, timing, response shape, error text, and side effects. Migration
must inventory real consumers and observable behavior before removal.

### Deprecation Planning Starts At Design Time

When adding a new system, ask how it could be removed later. Clean interfaces,
small public surfaces, flags with owners, and explicit compatibility promises make
future migration possible.

## Deprecation Decision Questions

Before deprecating, answer in research, spec, plan, or ticket as appropriate:

1. Does the old path still provide unique value?
2. Who or what consumes it today?
3. Does a replacement exist, and is it production-proven enough?
4. Which old observable behaviors must the replacement preserve?
5. What is migration cost per consumer?
6. What is the maintenance cost of not deprecating: security, dependency, support,
   mental overhead, opportunity cost?
7. Is deprecation advisory or compulsory?
8. What evidence will prove migration is complete?

If no replacement exists, build or specify the replacement first unless the
accepted decision is deliberate removal without replacement.

## Advisory vs Compulsory

Advisory deprecation:

- migration is optional for now
- old path is stable enough to maintain temporarily
- use warnings, docs, and incentives
- track review date and cleanup trigger

Compulsory deprecation:

- old path has security, correctness, cost, or blocking risk that justifies forcing movement
- needs deadline, owner, migration guide, tooling or support, and acceptance criteria
- needs stronger evidence and critique before enforcement

Default to advisory unless risk or maintenance cost justifies compulsory movement.

## Lifecycle

### 1. Build Or Specify The Replacement

The replacement must cover critical use cases, have intended behavior in specs,
and have enough evidence to be trusted for migration. If not production-proven,
state the remaining proof needed.

### 2. Inventory Consumers

Inventory should include:

- code references
- runtime metrics and logs
- API consumers
- docs and examples
- tests and fixtures
- config and deployment references
- external users or integrations when known

Preserve usage inventory or scan output in evidence when it supports removal or
hold decisions.

### 3. Announce And Document

For durable deprecation truth, route:

- replacement behavior to spec
- migration sequence to plan
- live consumer work to tickets
- external release or PR wording to ship
- accepted explanation to wiki when future agents need it

A deprecation notice should include status, replacement, reason, removal date or
review date, migration steps, verification method, and owner.

### 4. Migrate Incrementally

For each consumer:

1. Identify all touchpoints.
2. Move to the replacement.
3. Verify behavior matches.
4. Remove old references.
5. Record evidence and ticket status.

If the team owns the infrastructure being deprecated, it also owns either the
migration or backward-compatible path. Do not leave consumers to guess.

### 5. Prove Zero Usage Or Safe Removal

Before removal, gather evidence such as:

- reference scans
- runtime metrics or logs
- dependency graph output
- build/test output
- deprecation warning counters
- external consumer confirmation where needed

If zero usage cannot be proven, state the evidence limit and accepted risk in the
ticket. Do not silently round uncertainty up to safe removal.

### 6. Remove And Reconcile

Remove old code plus associated tests, docs, config, examples, flags, adapters,
deprecation notices, and wiki references. Search by canonical ID, path, symbol,
package name, endpoint, and old terminology.

### 7. Retrospective

Promote reusable lessons: better design-time deprecation hooks, test gaps, wiki
troubleshooting, research null results, or constitution decisions when policy changed.

## Migration Patterns

### Strangler

Run old and new paths in parallel. Shift traffic or consumers gradually:

1. new path handles 0 percent
2. small canary
3. partial rollout
4. new path handles all traffic
5. old path idle with monitoring
6. old path removed

Needs rollout thresholds, rollback conditions, and evidence at each stage.

### Adapter

Expose the old interface while delegating to the new implementation. Use when
consumer migration is expensive or staged. Adapters need owners and deletion
triggers; otherwise they become permanent complexity.

### Feature Flag

Switch consumers or cohorts between old and new paths. Flags need owner, expiry or
cleanup trigger, enabled/disabled evidence, and ship handoff notes.

### Bulk Cutover

Move all consumers at once. Use only when blast radius is small, rollback is clear,
and evidence supports the risk.

### Zombie-Code Disposition

Zombie code has active consumers but no owner, stale tests, old dependencies, or
broken docs. It cannot stay in limbo. Assign an owner and maintain it, or create a
migration/deprecation plan.

## Red Flags

- deprecated path has no replacement or explicit no-replacement decision
- new features are still added to a deprecated path
- advisory deprecation stays open indefinitely without review date
- adapter or flag has no deletion trigger
- consumer inventory is based on memory only
- removal happens without zero-usage evidence or accepted risk
- docs/tests/config still mention the old path after removal
- two systems doing the same job are maintained with no plan to converge

## Verification Checklist

- replacement behavior is spec-owned and critical use cases are covered
- consumer inventory exists and is fresh enough for the removal claim
- migration guide or owner-record equivalent names concrete steps
- consumers have moved or have ticket-owned accepted risk
- old code, tests, docs, config, flags, and notices are removed or dispositioned
- reference scans find no active current-truth references to the removed path
- rollout, rollback, and monitoring claims are backed by evidence
