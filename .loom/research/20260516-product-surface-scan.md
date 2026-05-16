# Loom Product Surface Scan

ID: research:20260516-product-surface-scan
Type: Research
Status: completed
Created: 2026-05-16
Updated: 2026-05-16

## Summary

This scan reviewed Loom's model-visible product surfaces, human-facing protocol docs, adapter entrypoints, and validation scaffolding for improvement ideas. The core protocol is unusually coherent: surface ownership, shaping before execution, ticket-owned Ralph runs, evidence, audit, and knowledge all reinforce each other. The main improvements are not conceptual rewrites; they are friction and drift fixes around Playbook explicitness, activation validation, command metadata quality, and prompt duplication.

## Question

What should Loom change, remove, add, or refine across its product surface area, and what rating is justified for the current protocol and skill set?

## Scope

Covered:

- Core model-visible surfaces under `loom-core/skills/`.
- Named agent prompt surfaces under `loom-core/agents/` and `loom-core/codex/agents/`.
- Playbook source and generated command surfaces under `loom-playbooks/playbooks/` and `loom-playbooks/commands/`.
- Human-facing protocol and install docs: `README.md`, `PROTOCOL.md`, `ARCHITECTURE.md`, `INSTALL.md`, and package READMEs.
- Relevant dogfood records for packet retirement, Playbook explicit macro behavior, Loom Weaver, and Loom Driver.
- Activation/test fixtures where they revealed product-surface drift.

Excluded:

- Fresh live harness activation runs.
- Package smoke or pack checks beyond prior recorded evidence.
- Formal Ralph-backed audit. This is research synthesis, not an audit verdict.
- Source changes outside `.loom/`.

## Method And Sources

- Read `loom-core/skills/using-loom/SKILL.md` and its ordered references for current protocol doctrine.
- Read Core record skills including `loom-tickets`, `loom-plans`, `loom-specs`, `loom-research`, `loom-evidence`, `loom-audit`, `loom-ralph`, `loom-knowledge`, `loom-constitution`, and `loom-retrospective`.
- Read Loom Weaver and Loom Driver canonical and Codex agent prompts.
- Read representative Playbooks and generated command TOML, including idea refinement, incremental implementation, source-driven development, debugging, TDD, security, review, and parallel worker coordination.
- Read `PROTOCOL.md`, `ARCHITECTURE.md`, `INSTALL.md`, root and package READMEs, `CLAUDE.md`, activation scenarios, and activation test scripts.
- Read relevant records: `decision:0002`, `spec:ticket-owned-worker-handoffs`, `spec:playbook-explicit-macros`, `spec:loom-weaver-agent`, `spec:loom-driver-agent`, `research:20260515-playbooks-core-activation-pressure`, and related migration tickets/audits.
- Ran targeted repository searches for packet terms, Playbook explicitness language, contributor-leakage terms, and generated command description shapes; ran `git status --short` and observed a clean worktree.

Source quality note: project-owned source and accepted Loom records are strong for current product reality. This scan did not validate external harness behavior in live sessions.

## Findings

- Core's truth-surface model is the strongest part of the product. `using-loom` and the record skills consistently separate intended behavior, executable work, evidence, audit, research, knowledge, and durable judgment. The same distinction appears in `PROTOCOL.md` and `ARCHITECTURE.md`.

- The ticket-owned Ralph migration appears conceptually complete in active product surfaces. `decision:0002`, `spec:ticket-owned-worker-handoffs`, the closed migration plan/tickets, and the current Core/Playbook surfaces all point at tickets and linked records as durable worker context rather than packet records. Targeted searches found no packet terms in active Core skill or Playbook source surfaces.

- The Playbook explicit-macro direction is right and mostly implemented. All 25 Playbook source `SKILL.md` files carry `disable-model-invocation: true`, the OpenCode entrypoint registers Playbooks as commands instead of `config.skills.paths`, and generated command prompts include an explicit macro preamble.

- There is still validation/documentation drift around Playbook autoactivation. `evals/activation/loom-activation-scenarios.md` still says that with Playbooks installed `loom-idea-refine` and `loom-debugging-and-error-recovery` are expected natural-prompt routes. That conflicts with `spec:playbook-explicit-macros`, `CLAUDE.md`, current tests, and current docs, which say natural prompts must not auto-load Playbooks.

- Generated Playbook command descriptions are mechanically correct but product-polish poor. The generator strips `Use when` and prepends `Explicit optional workflow macro for`, producing descriptions such as `Explicit optional workflow macro for correctness depends...` and `...for implementation should be driven...`. This is visible in all 25 command TOML files and weakens the explicit command surface.

- The generic install story still has a sharp edge. `INSTALL.md` and package docs mention exposing `loom-playbooks/playbooks` directly. That is acceptable only when the harness respects explicit-only metadata or the user invokes Playbooks deliberately. In a generic skill-directory setup that ignores `disable-model-invocation`, this could recreate the autoactivation failure mode the explicit-macro spec was designed to remove.

- Explicit skill request tests are not as strict as the doctrine. `tests/explicit-skill-requests/run-test.sh` warns when non-skill tools run before the first skill invocation, but still passes if the requested skill eventually appears. That means the tests can tolerate exactly the first-action violation that `using-loom` says is material.

- Agent prompts are effective but duplicated. Canonical Markdown and Codex TOML prompts are intentionally exact-match checked, but the product still carries two large copies of Weaver and Driver prompt text. Exact-match smoke reduces drift after edits, but a generation path or single canonical source would reduce maintenance risk.

- The protocol has a high floor and a high ceiling, but it is intentionally heavy. The always-on activation threshold and full `using-loom` preload create reliable routing pressure, at the cost of token load and occasional over-activation anxiety. The product mitigates this with `Create records when they help`, but the tension remains a real adoption/design tradeoff.

## Tradeoffs

- Keep protocol force high.
  - Strength: fewer silent scope inventions, retroactive tickets, unsupported closures, and unbounded worker prompts.
  - Weakness: more ceremony pressure and context load for small work.
  - Best when Loom is used for serious, cross-session, reviewable engineering work.

- Loosen activation and record pressure.
  - Strength: lighter first-use experience and fewer skills loaded for borderline prompts.
  - Weakness: reintroduces the failure modes Loom exists to prevent.
  - Not recommended as a default direction.

- Keep Core strict but make Playbooks and agent personas explicit lenses.
  - Strength: preserves Core's reliability while reducing broad workflow pressure.
  - Weakness: requires continued adapter/docs/test discipline so Playbooks do not drift back into implicit skill activation.
  - Recommended; this is already the product direction.

## Rejected Paths And Null Results

- I would not remove Ralph. The current ticket-owned framing makes Ralph useful as bounded run discipline without making it another durable surface.

- I would not collapse evidence and audit. Their distinction is one of the protocol's strongest trust-preserving moves.

- I would not merge Weaver and Driver. Their separation maps cleanly to outer-loop shaping and inner-loop coordination, and their write boundaries differ materially.

- I would not add a daemon, database, dashboard, or product CLI based on this scan. The Markdown-native product boundary is coherent and is reinforced by project guidance.

## Conclusions

- The protocol and skill set are strong enough to treat as a serious product architecture, not just a prompt collection.

- I would not honestly rate the current state as a perfect `10/10` because the scan found concrete drift and polish issues. A defensible current score is about `8.5/10` for the full product surface, with the Core protocol closer to `9/10` and the Playbook/validation surfaces closer to `8/10`.

- The most valuable changes are small and high-leverage: fix stale activation scenarios, polish generated Playbook command descriptions, harden explicit-skill activation tests, and make generic Playbook exposure safer.

## Recommendations

1. Fix `evals/activation/loom-activation-scenarios.md` so natural prompts expect Core routing/shaping and explicitly do not expect Playbook autoactivation.

2. Improve `loom-playbooks/loom-playbooks.mjs` command description generation. Prefer a pattern like `Explicit optional workflow macro for cases where ...` or add hand-authored concise command summaries to each Playbook frontmatter.

3. Tighten generic install docs: only expose `loom-playbooks/playbooks` as raw skills when the harness respects explicit-only metadata, or document that generic Playbook use requires deliberate explicit invocation.

4. Change explicit-skill activation tests so premature non-skill tool invocation fails, not merely warns, when the test is claiming first-action skill discipline.

5. Consider a small generation or synchronization path for Codex agent TOML from canonical `loom-core/agents/*.md` prompts, or keep the exact-match smoke but document the edit workflow in contributor-facing docs/knowledge.

6. Add a lightweight spec or checklist for activation validation surfaces, not because the protocol lacks doctrine, but because tests/evals/docs have drifted around Playbook implicit versus explicit behavior more than once.

## Operator Disposition

- Recommendation 1 accepted straightforwardly. Routed to `ticket:20260516-activation-scenarios-core-first-playbooks`.
- Recommendation 2 accepted with a refined direction: generated Playbook command descriptions should use existing Playbook source descriptions and should not add the `Explicit optional workflow macro for` prefix. Routed through `spec:playbook-explicit-macros#REQ-013` and `ticket:20260516-playbook-command-descriptions-source`.
- Recommendation 3 accepted. Routed to `ticket:20260516-generic-playbook-install-safety`.
- Recommendation 4 accepted as an experiment. Routed to `ticket:20260516-explicit-skill-test-first-action-failures`.
- Recommendation 5 deferred by the operator; no ticket created.
- Recommendation 6 was not an actionable source-change recommendation as phrased; no ticket created from it.

## Open Questions

- Should Playbook command descriptions be fully generated from frontmatter, or should Playbook frontmatter gain a separate `command-description` field for human-quality explicit command menus?
- Should generic raw Playbook skill directory setup remain documented, or should docs route generic users to package/command surfaces only unless explicit-only support is known?
- Is the intended product rating supposed to score Core doctrine only, or the whole shipped product surface including Playbooks, generated commands, docs, and validation fixtures?

## Related Records

- `spec:playbook-explicit-macros` - owns the intended explicit Playbook invocation behavior.
- `research:20260515-playbooks-core-activation-pressure` - explains why implicit Playbook pressure was demoted.
- `decision:0002` and `spec:ticket-owned-worker-handoffs` - own the current ticket-owned Ralph model.
- `spec:loom-weaver-agent` and `spec:loom-driver-agent` - own named agent behavior contracts.
- `knowledge:playbook-activation-tests-procedure` - records the all-Playbook negative activation test procedure.
- `ticket:20260516-activation-scenarios-core-first-playbooks` - accepted follow-up for stale activation scenario expectations.
- `ticket:20260516-playbook-command-descriptions-source` - accepted follow-up for command description generation.
- `ticket:20260516-generic-playbook-install-safety` - accepted follow-up for generic Playbook install safety wording.
- `ticket:20260516-explicit-skill-test-first-action-failures` - accepted follow-up for stricter explicit-skill activation tests.
