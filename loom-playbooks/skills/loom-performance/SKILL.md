---
name: loom-performance
description: "Measure, optimize, and guard performance. Use when load time, latency, throughput, memory, bundle size, Core Web Vitals, slow queries, regressions, budgets, or profiling evidence matter; measure before optimizing."
compatibility: Markdown-native, script-free Loom protocol.
metadata:
  skill_kind: workflow
---

# loom-performance

Performance work without measurement is guessing.

This playbook coordinates baseline measurement, bottleneck identification, focused
optimization, verification, guardrails, and evidence routing.

## Core Dependency

This playbook requires `loom-core`. If `using-loom` and the core owner-layer
skills are not installed or preloaded, stop and load/install `loom-core` instead
of treating this playbook as a substitute for Loom doctrine or record grammar.

## What This Workflow Coordinates

- performance baseline and budget definition
- frontend, backend, database, CI, and runtime bottleneck investigation
- before/after measurement evidence
- performance regression guards
- review of optimization complexity and tradeoffs

## What This Workflow Does Not Own

- performance requirements or budgets when reusable; use specs
- raw benchmark, trace, log, or dashboard output; use evidence
- live execution and accepted risk; use tickets
- launch/monitoring handoff; use `loom-ship`
- security or data-sensitive trace handling; use `loom-security` when applicable

## Use This Skill When

- a spec or user names performance requirements
- users, monitoring, CI, Lighthouse, browser traces, or logs report slowness
- a change may regress load time, latency, memory, bundle size, or throughput
- optimizing images, rendering, queries, caching, pagination, or heavy computation
- performance budgets or regression checks should be added to CI or evidence

## Do Not Use This Skill When

- no performance problem, requirement, or risk exists
- the proposed optimization is only aesthetic or speculative
- behavior is broken first; use debugging before optimizing
- measurement would expose sensitive data without a sanitization plan

## Default Procedure

1. Identify the user-visible or system-visible performance claim: what is slow, for
   whom, under what conditions, and what threshold matters.
2. Gather baseline evidence before changing code. Use synthetic and/or real-user
   data as appropriate.
3. Identify the actual bottleneck: network, server, database, rendering, bundle,
   main thread, memory, external service, CI runner, or algorithm.
4. Route reusable budgets or intended performance behavior to specs. Route
   investigation and tradeoffs to research when needed.
5. Fix the specific bottleneck with the smallest complexity increase.
6. Measure again under comparable conditions and preserve before/after evidence.
7. Add a guard when recurrence matters: test, benchmark, budget, monitoring, or CI gate.
8. Run critique when optimization changes architecture, caching correctness,
   data behavior, security posture, or user experience.

## Budget Examples

Use project-specific budgets when available. Generic starting points may include:

- LCP <= 2.5s, INP <= 200ms, CLS <= 0.1 for web UI
- API p95 latency under a specified threshold for critical endpoints
- initial JS/CSS/image sizes under project-defined limits
- no unbounded list endpoints or N+1 queries in critical paths
- CI pipeline target duration with measured bottleneck owners

Do not import generic budgets as product truth without spec or ticket acceptance.

## Common Rationalizations

- Rationalization: "This optimization is obvious."
  Reality: Without baseline data, you may optimize the wrong thing and add
  complexity.
- Rationalization: "It feels faster locally."
  Reality: Local subjective speed is not representative evidence.
- Rationalization: "The framework handles performance."
  Reality: Frameworks do not fix fetch-all endpoints, N+1 queries, huge images,
  or oversized bundles.
- Rationalization: "We can measure after."
  Reality: Measurement after cannot prove improvement without a baseline.

## Red Flags

- no before/after numbers
- optimizing code that is not on the hot path
- adding caching without invalidation or correctness review
- `useMemo`, memoization, indexes, or batching added everywhere without profiling
- no budget or monitoring for a recurring regression
- performance evidence gathered under incomparable conditions

## Verification

- [ ] Baseline and target are explicit.
- [ ] Bottleneck was identified from evidence, not assumption.
- [ ] Before/after measurements are comparable or limitations are stated.
- [ ] Optimization complexity and behavior/security risks were reviewed.
- [ ] Guardrail exists or absence is ticket-owned.

## Done Means

- the performance claim is evidence-backed
- budgets or expectations are owner-routed
- optimization addresses a measured bottleneck
- recurrence guard and residual risk are explicit

## Read In This Order

Read immediately for performance work:

1. `references/measure-optimize-guard.md` for baselines, bottlenecks, budgets,
   common frontend/backend fixes, and guardrails.
2. the core `loom-evidence` skill for traces, benchmark output, screenshots, and logs.
3. the core `loom-specs` skill when budgets or performance behavior need a reusable owner.

Then read conditionally:

4. `skills/loom-debugging/SKILL.md` when performance regression root cause is unknown.
5. `skills/loom-ui-browser/SKILL.md` for browser runtime and Core Web Vitals evidence.
6. `skills/loom-ci-cd/SKILL.md` when budgets should run in automation.
7. the core `loom-critique` skill for risky optimization review.
