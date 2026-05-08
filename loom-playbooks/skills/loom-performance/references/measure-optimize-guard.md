# Measure Optimize Guard

Use this reference when performance claims require proof.

## Workflow

```text
MEASURE -> IDENTIFY -> FIX -> VERIFY -> GUARD
```

Do not skip MEASURE. Do not fix every possible issue. Optimize the bottleneck that
evidence shows matters.

## Baseline Types

- synthetic: Lighthouse, browser traces, benchmark harnesses, controlled load tests
- real-user monitoring: production metrics, Core Web Vitals, APM, logs
- local profiling: CPU, heap, database query logs, network waterfall
- CI measurement: bundle size, test duration, build duration

Synthetic data is reproducible. Real-user data validates actual impact. Use both
when stakes justify it.

## Symptom To Measurement

- Symptom: slow first load
  First measurements: LCP, TTFB, network waterfall, bundle size, image/font size.
- Symptom: input lag
  First measurements: INP, long tasks, render profiling, event handlers.
- Symptom: layout jump
  First measurements: CLS, layout shift attribution, image/font dimensions.
- Symptom: slow endpoint
  First measurements: p95 latency, query log, trace spans, external call timing.
- Symptom: memory growth
  First measurements: heap snapshots, object retention, cache growth.
- Symptom: CI slow
  First measurements: job duration, dependency install, test shard timing,
  cache hits.

## Common Bottlenecks

### Frontend

- oversized initial bundle
- render-blocking CSS or JS
- unoptimized images or fonts
- missing dimensions causing layout shift
- excessive main-thread work
- unnecessary rerenders in hot interactions
- data waterfalls across routes or components

### Backend

- N+1 queries
- missing indexes
- fetch-all endpoints without pagination
- synchronous heavy computation in request path
- unbounded caches or memory leaks
- repeated external calls without timeout or caching strategy

### Automation

- repeated installs without cache
- serial jobs that can run independently
- unsharded slow suites
- E2E overuse in critical path
- generated artifact churn

## Budget Ownership

Budgets become project truth only when a spec, plan, ticket, or constitution layer
owns them. Generic defaults are starting points, not acceptance.

Possible budgets:

- Core Web Vitals thresholds
- API p95/p99 latency
- bundle and asset sizes
- memory ceiling
- query count or database response target
- CI duration target

## Fix Patterns

Use only when evidence points there:

- add pagination or limits for unbounded data
- batch or join queries to remove N+1 patterns
- add indexes after checking query shape and write cost
- split code by route or lazy path
- optimize images with dimensions, responsive sources, and lazy loading for below-fold assets
- cache stable expensive results with invalidation strategy
- defer non-critical work off the critical path
- reduce rerenders only after profiling identifies them

## Guardrails

Recurring performance requirements need guards:

- CI bundle-size check
- Lighthouse CI or browser performance smoke
- benchmark test with stable thresholds
- API latency monitor or alert
- regression test for query count
- dashboard plus ticket-owned monitoring expectations after launch

Guardrails should fail usefully. A flaky or noisy performance gate needs tuning,
not blind enforcement.

## Evidence Comparability

Before/after measurements should match:

- source version boundary
- environment and hardware class
- dataset size
- cache state
- network condition
- browser/runtime version
- command flags

When they cannot match, state the limitation and avoid overclaiming improvement.

## Complexity Review

Every optimization adds maintenance risk. Ask:

- did the fix address the measured bottleneck?
- did it change behavior, freshness, ordering, or consistency?
- does caching have invalidation and security boundaries?
- does memoization obscure logic or create stale data?
- did indexes or batching change write cost or transaction behavior?
- can future agents understand why this exists?

Route risky changes to critique and wiki/research if the lesson should persist.
