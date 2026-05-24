# HOTL Plugin Repository Scan

ID: research:20260516-hotl-plugin-scan
Type: Research
Status: completed
Created: 2026-05-16
Updated: 2026-05-16

## Summary

This scan reviewed `yimwoo/hotl-plugin` for transferable lessons for Agent Loom. HOTL's most useful lessons are operational: concise intent/verification/governance contracts, typed per-step verification, deterministic report/output contracts, explicit branch/worktree finish disposition, review-feedback handling as claims to verify, and smoke tests that check product-surface drift. Loom should not copy HOTL's `.hotl` runtime/state machine or `docs/designs` / `docs/plans` taxonomy because that would weaken Loom's Markdown surface-ownership model and current no-runtime boundary.

## Question

What, if anything, should Agent Loom learn from `https://github.com/yimwoo/hotl-plugin` without weakening Loom's Markdown control-plane boundary, surface ownership model, ticket-owned Ralph execution, evidence posture, audit discipline, or product-surface separation?

## Scope

Covered:

- Public `yimwoo/hotl-plugin` repository source as inspected on 2026-05-16.
- Repository product framing, prompt surfaces, plugin/bootstrap mechanics, docs, tests, and packaging details that reveal transferable patterns for Agent Loom.
- Comparison against current Agent Loom records and constraints around product-surface leakage, activation discipline, explicit Playbooks, ticket-owned worker handoffs, evidence, and audit.

Excluded:

- Executing untrusted external repository scripts.
- Treating HOTL Plugin source as authority for Agent Loom behavior.
- Creating implementation tickets before the operator selects a direction.
- Source changes outside `.loom/`.

## Method And Sources

- GitHub API metadata for `https://api.github.com/repos/yimwoo/hotl-plugin`, fetched 2026-05-16: public MIT repository, default branch `main`, pushed at `2026-05-10T20:47:12Z`, 22 stars, 3 forks, and repository description "HOTL plugin for Codex, Claude Code, and Cline. Human-on-the-Loop AI coding workflows with planning, review, and verification."
- Shallow clone of `https://github.com/yimwoo/hotl-plugin.git` into `/var/folders/1b/6mg4g2fs2zx99h46b9j5r7mh0000gp/T/opencode/hotl-plugin-scan-20260516`, observed at commit `b63ae89ed961a3a9f3fbbe65622126fc0e6512c6` with `VERSION` `2.17.0`.
- `README.md`, `docs/how-it-works.md`, and `docs/workflow-format.md` - product framing, workflow phases, artifact locations, typed verification, branch/worktree preflight, runtime sidecar, and finish lifecycle.
- `skills/using-hotl/SKILL.md`, `skills/brainstorming/SKILL.md`, `skills/writing-plans/SKILL.md`, `skills/loop-execution/SKILL.md`, `skills/executing-plans/SKILL.md`, `skills/subagent-execution/SKILL.md`, `skills/resuming/SKILL.md`, `skills/finishing-a-development-branch/SKILL.md`, `skills/requesting-code-review/SKILL.md`, `skills/receiving-code-review/SKILL.md`, `skills/code-review/SKILL.md`, `skills/document-review/SKILL.md`, and `skills/skill-authoring/SKILL.md` - model-visible workflow doctrine.
- `runtime/hotl-rt`, `scripts/document-lint.sh`, `scripts/hotl-prepare-execution-root.sh`, `scripts/hotl-locate-run.sh`, `scripts/render-execution-summary.sh`, and related script references - runtime/state/lint/report mechanics inspected as source only. No untrusted HOTL scripts were executed.
- `docs/contracts/execution-report-output.md`, `docs/contracts/code-review-output.md`, and representative checklists - output contract and review dimensions.
- `test/smoke.bats`, `test/runtime-integration.bats`, `test/execution-root.bats`, `test/fixtures/hotl-workflow-typed-verify-sample.md`, and representative scenario fixtures - validation shapes and product-surface drift checks.
- Local Agent Loom records: `research:20260516-product-surface-scan`, `research:20260516-aegis-method-pack-scan`, `research:20260513-superpowers-skill-activation`, `spec:playbook-explicit-macros`, `decision:0002`, and `spec:ticket-owned-worker-handoffs`.

Source quality note: this is source-backed external repository research, not live validation of HOTL behavior in Codex, Claude Code, Cline, Cursor, or OpenCode. Claims about runtime behavior are limited to what repository source and tests specify.

## Findings

- HOTL and Loom attack similar failure modes from different product shapes. HOTL frames itself as a Human-on-the-Loop workflow plugin that keeps coding grounded in a design, executable workflow, review checkpoints, and verification evidence. Loom frames the same class of work as a repo-local Markdown control plane with owned truth surfaces.

- HOTL's most compact shaping vocabulary is the three-contract model: intent contract, verification contract, and governance contract. In `brainstorming`, these capture goal/constraints/success/risk, proof steps, and approval/rollback/ownership. Loom already has richer surfaces for these truths, but the contract trio is a strong conversational compression for Weaver before routing to specs, tickets, evidence expectations, and audit posture.

- HOTL's executable workflow file is a concrete per-step contract: each step has `action`, `loop`, `max_iterations`, `verify`, and optional `gate`. This is more operationally constrained than many Loom tickets, but it is also narrower: it assumes a workflow execution engine rather than Loom's broader ticket-owned Ralph runs.

- The typed verification vocabulary is especially transferable. HOTL supports `shell`, `browser`, `human-review`, `artifact`, and multiple checks per step. The useful Loom lesson is not to add HOTL's runtime, but to give tickets/specs a clearer evidence-expectation vocabulary when acceptance depends on different proof modes.

- HOTL separates design shape from implementation detail with deterministic lint. `document-lint.sh` warns on implementation leakage in feature/phase design docs, including file:line references, long fenced code blocks, dense flag lines, and missing required sections. This overlaps strongly with Loom's product-surface leakage concern and shows a concrete static-check shape for keeping intended-behavior records from becoming brittle implementation scripts.

- HOTL makes execution provenance first-class. Workflow execution records `source_branch`, `source_head`, execution branch, execution root, worktree path, run id, report path, and executor mode. It distinguishes authoring checkout from execution checkout, rejects protected-branch host mode, avoids auto-stash, and forces a post-run finish decision: merge, publish/PR, keep, or discard.

- HOTL's `.hotl/state/<run-id>.json` sidecar and `.hotl/reports/<run-id>.md` are a real runtime state machine. The sidecar is authoritative, reports are durable human-readable mirrors, chat/progress UI is only presentation, and resume is verify-first. Loom should treat this as inspiration for stronger ticket/Ralph run provenance, not as a surface to copy.

- HOTL's review lifecycle has a strong safety invariant: review feedback is input to evaluate, not instructions to obey. `receiving-code-review` requires Verify → Evaluate → Respond → Implement, and technical claims from humans or external reviewers still need verification against current code. This maps cleanly to Loom's authority model and could sharpen audit/review follow-through guidance.

- HOTL uses output contracts to keep model results comparable across runs and platforms. `code-review-output.md` requires Scope, Reviewed Dimensions, Findings, What Was Not Covered, Residual Risks, and Verdict. `execution-report-output.md` defines durable report sections, status vocabulary, platform-specific summary rendering, and a deterministic renderer. Loom's audit/evidence/ticket records already have templates, but HOTL's contract tests are a useful reminder that output shape is product behavior.

- HOTL's tests cover product-surface drift in ways Loom can reuse: manifest version parity, command/skill name collision guard, command prompt delegation to canonical skills, docs prompt examples resolving to real installed skills, preflight section parity across execution skills, typed verification fixtures, design-lint warning fixtures, and update/install path behavior.

- HOTL's `skill-authoring` repeats lessons already present in Loom/Superpowers/Aegis research: skills are behavior-shaping code, frontmatter descriptions should be trigger-only, and behavior changes need pressure tests or smoke coverage. This reinforces Loom's current direction rather than introducing a new one.

- HOTL's `using-hotl` is deliberately lighter than Loom's `using-loom`: it says not every task needs a skill, directly answers questions and quick fixes, and routes debugging directly without brainstorm. This may improve adoption for HOTL's workflow-plugin shape, but it is not compatible with Loom's stronger first-action routing guarantee.

- HOTL has significant runtime/helper-script assumptions: Bash runtime, `jq`, updater scripts, install path resolution, `.hotl` state, `.hotl-worktrees`, and deterministic summary renderers. Directly importing that architecture would conflict with this repository's current product boundary unless Loom explicitly decides to become more than a Markdown skill/control-plane corpus.

## Tradeoffs

- Borrow HOTL contract vocabulary without adding runtime.
  - Strength: gives Weaver, specs, and tickets a compact way to name intent, proof, and governance without changing Loom surfaces.
  - Weakness: risks duplicating Loom's richer surface taxonomy if treated as a new record type.
  - Recommended as language, not structure.

- Add HOTL-style typed evidence expectations to Loom tickets/specs.
  - Strength: makes acceptance and evidence posture more concrete for future Ralph workers and audits.
  - Weakness: if over-formalized, it can turn tickets into brittle workflow scripts and undercut judgment.
  - Worth shaping as an optional vocabulary for acceptance/evidence, not a required runtime schema.

- Add HOTL-style deterministic lint/smoke checks.
  - Strength: catches drift between model-visible surfaces, docs, manifests, commands, prompts, and examples before users do.
  - Weakness: adds test maintenance in a repo that currently avoids a heavy test/tooling stack.
  - Recommended where checks are narrow and repository-owned, especially command/skill collision, example-resolution, manifest parity, and product-surface leakage.

- Copy HOTL's `.hotl` runtime/state machine.
  - Strength: would provide resumable execution and deterministic run summaries.
  - Weakness: violates Loom's current no-runtime/no-helper-script assumption, duplicates tickets/evidence/audit, and would change the product from Markdown control-plane to workflow engine.
  - Not recommended without a constitution-level architecture decision.

- Adopt HOTL's low-friction activation posture.
  - Strength: less ceremony for small tasks.
  - Weakness: reopens Loom's known failure modes: silent scope invention, retroactive tickets, unbounded worker prompts, and unsupported closure claims.
  - Not recommended for Core Loom.

## Rejected Paths And Null Results

- Do not copy `.hotl/state`, `.hotl/reports`, `.hotl-worktrees`, or `hotl-rt` as Loom product surfaces. Loom tickets, evidence, audit, and linked records already own durable execution truth.

- Do not replace `.loom/specs`, `.loom/plans`, `.loom/tickets`, `.loom/evidence`, and `.loom/audit` with `docs/designs`, `docs/plans`, and `.hotl` artifacts. HOTL's taxonomy is coherent for HOTL, but weaker than Loom's surface-ownership graph for this repo.

- Do not add a generic workflow executor, branch manager, updater, or deterministic renderer as a casual follow-up. That would be an architecture change, not a lesson learned.

- Do not treat HOTL's `auto_approve` / `risk_level` gate model as a substitute for Loom evidence and audit. Loom can use risk to shape audit posture, but a low-risk label should not itself grant proof or closure.

- Do not weaken `using-loom` to match `using-hotl`. HOTL's lighter router fits an optional workflow plugin; Loom's control-plane value depends on first-action surface routing.

## Conclusions

- HOTL is operationally more runtime-like than Loom and conceptually less precise about durable truth ownership. Its direct architecture should not be copied.

- The strongest transferable idea is HOTL's explicit proof/governance operationalization: every execution step has a verification type, retries have bounds, human review is a persisted gate, reviews have output contracts, and finish disposition is explicit.

- Loom's equivalent should live in existing surfaces: specs for intended behavior, tickets for executable scope and evidence expectations, evidence for observations, audit for adversarial review, and Driver/Ralph guidance for run provenance and closure.

- HOTL's tests are a concrete source of near-term validation ideas for Loom. They complement the Aegis/Superpowers lessons by focusing less on activation compliance and more on product-surface consistency, examples that resolve, command/skill collisions, version/manifest parity, output-contract conformance, and docs/runtime drift.

- If Loom wants resumable execution artifacts, the right first move is not implementation. It is a constitution/spec decision about whether Loom remains a Markdown control plane or adds runtime helpers. Current project guidance says no helper-script/product-runtime assumptions.

## Recommendations

1. Reuse HOTL's three-contract framing as a Weaver shorthand when shaping implementation work: intent, verification, governance. Route the durable pieces into existing Loom specs, tickets, evidence expectations, audit posture, and plans rather than creating a new contract record surface.

2. Shape a Loom-specific optional evidence-expectation vocabulary for tickets/specs, borrowing the useful HOTL categories: command/test, browser/manual UI, human review, artifact/file assertion, and combined checks. Keep it optional and claim-scoped.

3. Consider a bounded validation ticket for HOTL-style product-surface checks that fit Loom's current architecture: command/skill name collision guards, prompt/example references resolving to real skills or agents, version/manifest parity, and static scans for product-surface leakage. This overlaps with `research:20260516-aegis-method-pack-scan` recommendation 2.

4. Consider strengthening Loom Driver or ticket closure guidance with an explicit execution-disposition question when a worker run creates or uses a branch/worktree: merged, PR/published, kept for follow-up, discarded, or not applicable. This should be ticket-owned, not a runtime helper.

5. Consider promoting HOTL's review-response invariant into Loom audit/Driver wording: review findings and worker reports are claims to verify/evaluate/respond to, not instructions to obey. This aligns with `using-loom` authority rules and may prevent over-trusting reviewer output.

6. Do not create implementation tickets for a `.loom` runtime, `.hotl`-style state sidecar, updater, or branch manager unless the operator first accepts a durable architecture change in constitution/specs.

## Open Questions

- Should Loom tickets gain a small `Evidence Expectations` convention, or is the current acceptance/evidence prose enough?
- Should Loom's next validation work combine Aegis's activation/workflow-quality matrix with HOTL's product-surface consistency checks?
- Is branch/worktree finish disposition common enough in Loom/Ralph work to justify first-class ticket guidance?
- Should HOTL's implementation-leakage lint inspire checks over `.loom/specs` / `.loom/plans`, or should Loom restrict static leakage checks to shipped product surfaces first?

## Related Records

- `research:20260516-product-surface-scan` - current baseline of Agent Loom's product-surface strengths, drift, and accepted follow-up areas.
- `research:20260516-aegis-method-pack-scan` - prior external scan with validation, guardrail, context-budget, and install-doctor comparison points.
- `research:20260513-superpowers-skill-activation` - prior external scan on activation discipline and adapter bootstrap behavior.
