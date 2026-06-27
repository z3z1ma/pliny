Status: recorded
Created: 2026-06-27
Updated: 2026-06-27
Target: .10x/evidence/2026-06-27-autoresearch-ergonomics-result.md
Verdict: pass
Relates-To: .10x/tickets/done/2026-06-27-tighten-autoresearch-happy-path-ergonomics.md, .10x/specs/10x-autoresearch-loop.md

# Review: Autoresearch Ergonomics Tightening

## Verdict

Pass.

The active setup now presents one clear happy path: register a scientific
contract, list the exact arms to run, define the scenario and seed provenance,
run one trial, inspect artifacts, and record the verdict.

## Findings

No blocking findings.

Resolved: one-arm current-skill smoke runs are first-class. The same `arms`
array now supports one-arm regression checks and multi-arm comparisons.

Resolved: experiment definitions are scientifically richer. The required
`scientific_contract` captures the hypothesis, expected behavior, inspection
criteria, quality floor, and verdict destination before execution.

Resolved: reports point to durable workspace artifacts. Trial rows now include
the archived workspace path, and the report surfaces the scientific contract
before artifact details.

Resolved: the active spec and templates no longer steer readers toward removed
static evaluation concepts. The active spec is smaller, live-trial-oriented, and
keeps the existing requirement IDs for catalog continuity.

## Residual Risk

Historical evidence and research records still describe earlier runs using older
tooling language. That is acceptable as record history. The active docs,
templates, spec, runner, report, and validation path now agree.
