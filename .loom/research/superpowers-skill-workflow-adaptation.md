---
id: research:superpowers-skill-workflow-adaptation
kind: research
status: completed
created_at: 2026-04-28T07:47:02Z
updated_at: 2026-04-28T08:05:59Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  tickets:
    - ticket:k7p4s2q9
  evidence:
    - evidence:superpowers-workflow-adaptation-validation
  critique:
    - critique:superpowers-workflow-adaptation-review
external_refs:
  github:
    - https://github.com/obra/superpowers/tree/main/skills
---

# Question

Which Superpowers skills represent capabilities Loom does not already express as first-class workflows, and how should each be adapted into Loom's layer-owned protocol without creating a parallel methodology?

# Why This Matters

Superpowers is a named Loom influence and provides a mature skills-based development methodology. Adapting its useful workflows can sharpen Loom's operator guidance, but only if the adaptation preserves Loom's composition model: canonical layers own truth, workflow skills coordinate routes, and packets/tickets/evidence/critique keep execution honest.

# Scope

This investigation covers `obra/superpowers/skills` as cloned on 2026-04-28 and the current Loom `skills/` package. It excludes Superpowers installation packaging except where a skill depends on a harness behavior that must be translated into Loom's harness-neutral workflow vocabulary.

# Method

Read Loom's README, constitution, current skill corpus, and every meaningful Superpowers skill file. Map each Superpowers capability to one of:

- existing Loom skill already owns it, no product change needed
- existing Loom skill owns it but needs stronger workflow guidance
- missing first-class Loom workflow skill should be added
- not appropriate for Loom core because it would create a second ontology or harness-specific behavior

# Sources

- `README.md`
- `skills/**`
- `.loom/constitution/constitution.md`
- `.loom/constitution/decisions/decision-0001-markdown-first-protocol-over-product-runtime.md`
- `.loom/constitution/decisions/decision-0002-packetized-fresh-context-execution-with-ticket-ledger-truth.md`
- `.loom/constitution/decisions/decision-0004-flat-sibling-skills-with-self-contained-distribution.md`
- `https://github.com/obra/superpowers/tree/main/skills`, cloned to `/tmp/loom-superpowers.vDNOwa` at commit `6efe32c9e2dd002d0c394e861e0529675d1ab32e`
- `evidence:superpowers-workflow-adaptation-validation`
- `critique:superpowers-workflow-adaptation-review`

# Evidence

## Superpowers Skill Inventory

| Superpowers skill | Core workflow discipline | Loom owner / route | Adaptation decision |
| --- | --- | --- | --- |
| `using-superpowers` | Mandatory skill activation and platform tool mapping. | `loom-bootstrap`, `loom-workspace`, harness adapters. | Already owned. Preserve Loom's bootstrap-first doctrine and route-by-truth-owner model; do not import the 1% trigger rule because it would create ceremony and weak skill activation. |
| `brainstorming` | Context exploration, one-question-at-a-time clarification, 2-3 approaches, design approval, spec review before planning. | `loom-workspace` problem shaping, `loom-research`, `loom-specs`, `loom-plans`, `loom-spike` for visual/sketch variants. | Strengthen problem shaping and spike/sketch guidance so brainstorming becomes a route into research/spec/plan/evidence, not a `docs/superpowers` design-doc ledger. |
| `writing-plans` | Concrete implementation plans, no placeholders, exact paths, TDD steps, self-review, execution handoff. | `loom-plans`, `loom-tickets`, `loom-ralph`. | Strengthen plan readiness, slicing, execution-wave, and template guidance while preserving the boundary that plans sequence tickets and do not track live progress. |
| `executing-plans` | Critical plan review, execute one bounded task at a time, stop on blockers, finish branch when done. | `loom-plans`, `loom-tickets`, `loom-ralph`, `loom-ship`. | Express execution as tickets and packets beneath a plan, not direct plan checkbox execution. Add explicit stop/loopback guidance. |
| `subagent-driven-development` | Fresh subagent per task, strict context handoff, implementer status vocabulary, spec-compliance review before code-quality review. | `loom-ralph`, `loom-critique`, `loom-tickets`. | Already structurally owned by Ralph. Strengthen packet output contract and critique pass splitting with child concerns, independent verification, and spec/acceptance compliance before quality review. |
| `dispatching-parallel-agents` | One agent per independent problem domain, no shared state, review/integrate after return. | `loom-plans` execution waves, `loom-ralph`, `loom-git`. | Already owned. Strengthen wave planning and parallel Git guidance with independent-domain grouping and full-suite/integration validation after child returns. |
| `test-driven-development` | Red-green-refactor, watched failing test before production change, real-behavior tests over mock-behavior tests. | `loom-ralph` verification posture, `loom-evidence`, `loom-records` implementation reality. | Strengthen `test-first` posture and packet template. Do not add a separate `loom-tdd` skill because TDD is a verification posture and evidence discipline for packets. |
| `systematic-debugging` | No fixes before root-cause investigation; reproduce, pattern analysis, hypothesis testing, root-cause fix, regression evidence, defense in depth. | `loom-debugging`, `loom-research`, `loom-evidence`, `loom-ralph`, `loom-retrospective`. | Add a dedicated systematic debugging reference and make it the first debugging read. Preserve helper techniques as prose patterns, not shipped scripts. |
| `verification-before-completion` | Fresh verification evidence before completion claims. | `loom-bootstrap` validation doctrine, `loom-records`, `loom-evidence`, `loom-tickets`. | Strengthen fresh-evidence guidance. Preserve Loom's distinction between current observation and durable evidence instead of requiring every claim to be verified only inside the current chat message. |
| `using-git-worktrees` | Isolated worktree, safe location, baseline setup/test, cleanup discipline. | `loom-git`, `loom-ralph`, `loom-ship`. | Already owned. Add baseline validation after worktree creation and keep non-destructive cleanup rules. Do not auto-edit `.gitignore` or auto-install dependencies as core protocol. |
| `requesting-code-review` | Review early/often with context, git range, severity, readiness verdict. | `loom-critique`, critique packets, ticket critique disposition. | Already owned. Strengthen critique packet required questions and review pass order; keep reviewer actors transport-neutral. |
| `receiving-code-review` | Verify feedback before acting, clarify unclear feedback, push back with evidence, implement one item at a time. | `loom-critique`, `loom-tickets`, `loom-evidence`. | Add finding disposition guidance that treats review feedback as claims to verify, not orders to blindly apply. |
| `finishing-a-development-branch` | Verify tests, present merge/PR/keep/discard options, cleanup safely. | `loom-ship`, `loom-git`, `loom-tickets`. | Add handoff-options reference. Preserve ticket acceptance boundary and forbid destructive discard without explicit confirmation. |
| `writing-skills` | Skill authoring as TDD for process documentation; trigger-focused descriptions; pressure testing; anti-rationalization guidance. | `loom-skill-authoring`, `loom-critique`, `loom-evidence`. | Strengthen skill authoring principles, anti-patterns, templates, and add skill-review guidance. Do not make failing subagent tests mandatory for every Markdown edit; use structural evidence and critique proportional to risk. |

## Existing Loom Skill Readiness

Current Loom already has first-class workflow owners for the Superpowers workflow families:

- `loom-workspace` owns entry, problem shaping, and routing.
- `loom-plans` owns sequencing, slicing, and execution waves.
- `loom-tickets` owns live execution and acceptance disposition.
- `loom-ralph` owns fresh bounded implementation handoff.
- `loom-critique` owns review, findings, and review pass splitting.
- `loom-evidence` owns observed verification artifacts.
- `loom-git` owns branch and worktree isolation support.
- `loom-debugging` owns reproduce-first debug routing.
- `loom-ship` owns PR/release/handoff packaging without closure.
- `loom-skill-authoring` owns skill boundary and structure quality.

The main missing product value is not new layers. It is sharper references inside those existing skills so operators can run Superpowers-grade workflows through Loom's owner graph.

# Rejected Options

- Importing Superpowers skills one-for-one under `skills/` was rejected because it would duplicate existing Loom owners, introduce a parallel vocabulary, and make workflow activation transport-shaped instead of layer-shaped.
- Adding new canonical owner layers for design docs, plan checkboxes, subagent tasks, code-review requests, worktree state, or branch-finish state was rejected because Loom already has specs, plans, tickets, packets, critique, evidence, wiki, and Git support boundaries for those truths.
- Shipping Superpowers helper scripts, browser companion runtime, or named reviewer agents as Loom core was rejected because this repository's constitution forbids hidden runtimes and keeps harness transports derivative.
- Making strict TDD a separate top-level Loom skill was rejected because Loom already models this as `verification_posture: test-first` plus evidence and critique disposition.

# Null Results

- No Superpowers skill required a new Loom owner layer.
- No Superpowers skill required a new top-level Loom workflow skill after mapping capabilities against the current corpus; the better adaptation path is strengthening existing workflow skills.
- Superpowers' harness tool maps are useful as adapter examples, but they do not change Loom's core protocol because Loom already separates owner, route, and transport.

# Conclusions

Superpowers and Loom share the same useful instincts: design before building, test-first behavior changes, reproduce-first debugging, fresh-context subagents, scoped parallelism, review gates, branch finish discipline, and evidence before completion claims.

The systems diverge at the ownership boundary. Superpowers packages workflows as mandatory skills with harness-specific prompts and some helper runtimes. Loom should adapt the discipline into owner-preserving routes: fuzzy idea -> workspace problem shaping -> research/spec/plan; implementation task -> ticket/Ralph/evidence; review -> critique/ticket disposition; branch finish -> ship/git/ticket acceptance; durable lesson -> retrospective/wiki/research/spec.

The correct implementation is therefore a deepening of existing Loom skills, not a Superpowers clone.

# Recommendations

Update the existing Loom corpus as follows:

1. Add systematic debugging detail to `loom-debugging` and make it the first debugging reference.
2. Strengthen `loom-ralph` test-first verification posture and packet output contract with explicit red/green commands, expected failure reasons, real-behavior testing, and child self-review concerns.
3. Strengthen `loom-records` and bootstrap validation guidance so completion claims cite fresh enough procedure, output, context, and limitations.
4. Strengthen `loom-workspace`, `loom-plans`, and `loom-spike` so brainstorming, design gating, sketches, plan review, no-placeholder checks, and execution-wave readiness are first-class Loom routes.
5. Strengthen `loom-critique` with spec/acceptance compliance before code-quality review, feedback disposition rules, and critique-packet required questions.
6. Strengthen `loom-git` and `loom-ship` with worktree baseline validation and handoff options for merge, PR, keep, or abandon without ticket closure drift.
7. Strengthen `loom-skill-authoring` with trigger-focused descriptions, pressure-scenario review, and anti-patterns without making a hidden test runtime mandatory.

# Open Questions

- Whether future examples should include a golden end-to-end trace that demonstrates the full brainstorming -> plan -> Ralph -> critique -> ship -> retrospective route.
- Whether future critique profile work should split `acceptance/spec compliance` and
  `implementation quality` into named profiles, or keep them as review-pass
  defaults under the broader `workflow-boundary`, `code-change`, and
  `test-coverage` profiles.

# Linked Work

- `ticket:k7p4s2q9`
