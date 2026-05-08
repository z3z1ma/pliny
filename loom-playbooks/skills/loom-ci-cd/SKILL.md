---
name: loom-ci-cd
description: "Design, repair, or interpret automated quality and deployment gates. Use when CI/CD, test pipelines, lint/type/build checks, preview deploys, branch protection, generated artifacts, secrets in automation, rollout, rollback, or pipeline failures affect Loom work."
compatibility: Markdown-native, script-free Loom protocol.
metadata:
  skill_kind: workflow
---

# loom-ci-cd

CI/CD is automated evidence and deployment control, not acceptance by itself.

This playbook coordinates quality gates, automation feedback, deployment strategy,
rollback posture, and pipeline evidence while routing truth through Loom owner records.

## Core Dependency

This playbook requires `loom-core`. If `using-loom` and the core owner-layer
skills are not installed or preloaded, stop and load/install `loom-core` instead
of treating this playbook as a substitute for Loom doctrine or record grammar.

## What This Workflow Coordinates

- lint, format, type, test, build, integration, E2E, security, and bundle gates
- CI failure triage and feedback into debugging or tickets
- preview deployment, staged rollout, rollback, and monitoring posture
- automation secret/environment separation
- pipeline performance and generated-artifact discipline

## What This Workflow Does Not Own

- evidence records; use core evidence
- ticket acceptance, closure, accepted risk, or blockers; use tickets
- release packaging; use `loom-ship`
- security review; use `loom-security` and critique
- Git branch or PR state; use `loom-git`

## Use This Skill When

- setting up or modifying CI, checks, deployment pipelines, or automation
- a ticket depends on automated quality gates
- CI fails and the failure must be classified before source changes
- preview, staging, rollout, rollback, or monitoring facts affect handoff
- secrets, environment variables, generated files, or automation permissions are in scope

## Do Not Use This Skill When

- the user only needs a local verification command; use core evidence and ticket
  validation guidance
- the failure root cause is unknown and needs reproduce-first debugging
- a green pipeline is being used to bypass ticket evidence or critique
- the work would require importing one vendor's YAML as Loom doctrine

## Default Procedure

1. Identify current automation surfaces: local commands, CI workflows, required
   checks, deployment targets, secrets, generated artifacts, and branch protections.
2. Map gates to claims: what lint, typecheck, tests, build, integration, E2E,
   security, bundle, or deployment checks actually prove.
3. Preserve CI output as evidence when ticket acceptance, debugging, critique, or
   shipping depends on it.
4. When CI fails, classify source bug, test flake, dependency/cache issue,
   environment drift, config error, resource limit, or external service problem.
5. Route unknown failures to `loom-debugging` instead of changing source by guess.
6. For deployment automation, require rollback path, environment separation,
   monitoring signal, and post-deploy verification before launch claims.
7. For secrets, ensure automation uses secret managers and does not place values in
   Loom records, logs, or committed config.
8. Optimize slow CI only after measuring bottlenecks; do not skip gates as an
   optimization.
9. Package already-truthful CI/release state through `loom-ship`; tickets still own acceptance.

## Gate Model

Default gates for code projects, adapted to project stack:

- format/lint for style and simple static issues
- typecheck or compile for static integration
- unit tests for local behavior
- integration tests for boundaries
- build/package for deployable artifact
- E2E/browser checks for critical user flows
- security/dependency audit for vulnerability signals
- bundle/performance budget for user-facing regressions
- preview/staging smoke for release confidence

Not every project has every gate. Missing gates are explicit evidence limits, not
assumed success.

## Common Rationalizations

- **Rationalization:** "CI is green, so this is accepted."
  **Reality:** CI is evidence. Ticket acceptance and critique disposition still decide closure.
- **Rationalization:** "CI is slow, so skip it."
  **Reality:** Measure and optimize the pipeline; skipping gates hides risk.
- **Rationalization:** "The flake passed on rerun."
  **Reality:** Flakiness is a signal to classify and fix or record, not proof the issue vanished.
- **Rationalization:** "Test secrets are harmless in YAML."
  **Reality:** Secrets belong in secret stores, not code or Loom evidence.

## Red Flags

- failing checks ignored, silenced, or marked optional without ticket rationale
- CI output copied into Loom with secrets or sensitive data
- production deploy has no rollback or monitoring check
- branch protection or required checks do not match the claimed quality gate
- generated artifacts change without review
- pipeline time is optimized by dropping meaningful checks

## Verification

- [ ] Gate list and what each gate proves are explicit.
- [ ] CI/deployment outputs that support claims are preserved or linked as evidence.
- [ ] Failures are classified before fixes or deferrals.
- [ ] Secrets and environment boundaries are safe and sanitized.
- [ ] Rollout, rollback, monitoring, and post-deploy checks are routed to ship/tickets.

## Done Means

- automated gates are mapped to Loom claims without overclaiming
- pipeline output is evidence, not acceptance authority
- failures have owner-routed disposition
- deployment automation has rollback and observation posture proportional to risk

## Read In This Order

Read immediately for CI/CD work:

1. `references/automation-gates-and-rollouts.md` for quality gates, CI failure
   classification, environment/secrets, rollout, rollback, and optimization.
2. the core `loom-evidence` skill when preserving CI, build, audit, or deploy output.
3. `skills/loom-debugging/SKILL.md` when a failing gate needs root-cause work.

Then read conditionally:

4. `skills/loom-security/SKILL.md` when automation touches secrets, permissions, or vulnerabilities.
5. `skills/loom-performance/SKILL.md` when budgets, bundle size, or pipeline speed are in scope.
6. `skills/loom-ship/SKILL.md` when packaging release or handoff notes.
