# Aegis Method Pack Scan

ID: research:20260516-aegis-method-pack-scan
Type: Research
Status: completed
Created: 2026-05-16
Updated: 2026-05-16

## Summary

This scan reviewed and then locally cloned `GanyuanRan/Aegis` for transferable ideas for Agent Loom. The strongest lessons are not Aegis's runtime-ready artifact taxonomy itself; Loom already has a cleaner durable surface graph and stricter Core activation. The useful lessons are Aegis's trigger-health diagnostic layers, sample-driven workflow-quality matrix, context-budget checks, authority-boundary tests, prompt-hygiene evidence indexing, and install/discovery doctor posture.

## Question

What, if anything, should Agent Loom learn from `https://github.com/GanyuanRan/Aegis` without weakening Loom's existing surface-ownership, ticket-owned Ralph, evidence, and audit model?

## Scope

Covered:

- Public GitHub repository metadata and `main` branch ref for `GanyuanRan/Aegis` as fetched on 2026-05-16.
- Local shallow clone of Aegis `main` at commit `c7537ec42e35367cb73356a74c0cecf3fe39b8eb`, under `/var/folders/1b/6mg4g2fs2zx99h46b9j5r7mh0000gp/T/opencode/aegis-analysis-20260516.vVEvr5/Aegis`.
- Aegis README and current docs around workflow quality, trigger health, activation mode, runtime-ready boundary, and artifact schemas.
- Representative Aegis skills: `using-aegis`, `using-aegis/references/skill-discipline.md`, `brainstorming`, `systematic-debugging`, `goal-framing`, `long-task-continuation`, `writing-plans`, `executing-plans`, `test-driven-development`, `subagent-driven-development`, `requesting-code-review`, `first-principles-review`, `writing-skills`, and `verification-before-completion`.
- Aegis OpenCode plugin bootstrap, Claude/Cursor hook bootstrap, package manifests, commands, agents, workspace helper scripts, doctor script, and representative E2E/static checks.
- Comparison against current Agent Loom doctrine, existing product-surface scan, Playbook explicit macro spec, and ticket-owned worker handoff decision/spec.

Excluded:

- Live host tests against Aegis.
- Running Aegis tests locally; the deep pass inspected source instead of executing scripts that may write temporary or repository-local test outputs.
- Treating Aegis docs as authority for Agent Loom behavior.
- Creating implementation tickets before operator selection.

## Method And Sources

- `https://api.github.com/repos/GanyuanRan/Aegis` - repository metadata; public MIT repo described as making agents architecture-aware, baseline-first, evidence-verified, drift-checked, and safe across long tasks. Observed `default_branch: main`, `pushed_at: 2026-05-15T05:31:23Z`, and 231 stars at fetch time.
- `https://api.github.com/repos/GanyuanRan/Aegis/git/refs/heads/main` - main ref observed at commit `c7537ec42e35367cb73356a74c0cecf3fe39b8eb`.
- Local clone created with `git clone --depth 1 https://github.com/GanyuanRan/Aegis.git` and `git rev-parse HEAD`, confirming commit `c7537ec42e35367cb73356a74c0cecf3fe39b8eb`.
- `README.md` from Aegis `main` - product framing, install flows, activation mode, host compatibility, workspace behavior, core workflow, relationship to Superpowers, and runtime-ready artifact list.
- `skills/using-aegis/SKILL.md` and `skills/using-aegis/references/skill-discipline.md` - compact hot path router, lazy workspace policy, bounded historical context guardrails, on-demand detail reference, trigger priority, project baseline bootstrap, and workspace rules.
- Representative Aegis workflow skills inspected from the clone: `brainstorming`, `systematic-debugging`, `goal-framing`, `long-task-continuation`, `writing-plans`, `executing-plans`, `test-driven-development`, `subagent-driven-development`, `requesting-code-review`, and `first-principles-review`.
- `skills/writing-skills/SKILL.md` - process-documentation-as-TDD discipline and trigger-only skill description guidance.
- `skills/verification-before-completion/SKILL.md` - evidence card, confidence grading, goal closure, ADR backfill, and prompt hygiene closure structure.
- `docs/current/AEGIS_PROCESS_BASELINE.md` and `docs/current/AEGIS_PROMPT_HYGIENE_AND_INJECTION_BOUNDARY.md` - TLREF/DIVE process baseline, ripple signal triage, prompt hygiene, bounded evidence intake, and index-window-excerpt handling.
- `docs/current/AEGIS_WORKFLOW_QUALITY_BASELINE.md` - representative workflow-quality dimensions and compact output contracts.
- `docs/current/AEGIS_TRIGGER_HEALTH_BASELINE.md` - layered trigger diagnosis from install/version through false-positive control.
- `docs/current/AEGIS_ARTIFACT_SCHEMA_BASELINE.md` and `docs/current/AEGIS_RUNTIME_READY_BOUNDARY.md` - draft/hint/projection artifact posture and explicit non-authority boundary.
- `docs/current/AEGIS_ACTIVATION_MODE.md` and `.opencode/plugins/aegis.js` - automatic versus explicit activation mode and OpenCode bootstrap implementation.
- `scripts/aegis-doctor.py`, `scripts/aegis-workspace.py`, and `scripts/log-window.sh` - install/discovery/config/workspace helper verification, target-project workspace lifecycle support, structural proof bundle assembly, and bounded log-window readback.
- `tests/e2e/fixtures/workflow-quality-matrix.json`, `tests/e2e/fixtures/trigger-health-matrix.json`, `tests/e2e/workflow-quality-check.sh`, `tests/e2e/trigger-health-check.sh`, `tests/e2e/context-budget-check.sh`, `tests/e2e/boundary-compliance-check.sh`, `tests/skill-triggering/run-test.sh`, and `tests/explicit-skill-requests/run-test.sh` - representative matrices, static guardrail checks, and live-harness activation test shapes.
- Aegis `AGENTS.md`, `CLAUDE.md`, `.codex-plugin/plugin.json`, `.claude-plugin/plugin.json`, `.cursor-plugin/plugin.json`, `gemini-extension.json`, `.opencode/plugins/aegis.js`, `hooks/session-start`, `commands/brainstorm.md`, and `agents/code-reviewer.md` - repo/contributor authority, adapter packaging, bootstrap injection, deprecated command posture, and named review-agent projection.
- Local Agent Loom records: `research:20260516-product-surface-scan`, `research:20260513-superpowers-skill-activation`, `spec:playbook-explicit-macros`, `decision:0002`, and `spec:ticket-owned-worker-handoffs`.

Source quality note: this is source-backed external repository research with a local clone, but not a live validation of Aegis behavior. Claims about runtime behavior remain limited to what the repository source and tests intend, not what a host actually did during this session.

## Findings

- Aegis positions itself as a runtime-ready method pack, not a runtime core. Its README and runtime-boundary docs repeatedly say Aegis can produce drafts, hints, projections, evidence bundles, and gate input packs, but must not produce authoritative `GateDecision`, final evidence sufficiency, or completion authority.

- Aegis's current `using-aegis` hot path is dramatically smaller and weaker than Loom's preloaded `using-loom` doctrine. It says to load a skill when explicitly requested or clearly relevant, and keeps the red flags, priority, baseline bootstrap, and workspace rules in `references/skill-discipline.md`. This reduces token load but is not equivalent to Loom's 1% activation threshold and required first-action skill invocation.

- Aegis inherited Superpowers activation ideas, but the current Aegis posture has been deliberately softened. `using-aegis` says simple/local/low-risk tasks can stay fast path; the full reference says uncertain relevance should be classified through the compact hot path rather than loading a full skill. Loom should not interpret Aegis as evidence that stricter Core routing is unnecessary.

- Aegis has a stronger explicit trigger-health diagnostic model than Loom currently records as a single product concept. It separates failures into install/version, host discovery, activation/bootstrap, router entry, task-to-skill routing, skill execution depth, context pressure/re-entry, and false-positive over-triggering. This is more actionable than treating all missed activation as prompt wording failure.

- Aegis's workflow-quality matrix is a strong transferable testing shape. Each representative sample names expected primary skill, allowed secondary skills, forbidden behavior, expected output shape, workspace policy, expected artifacts, and verification signal. Loom has activation tests and Playbook explicit macro checks, but the Aegis matrix combines false-negative, false-positive, output-depth, evidence, and workspace-policy expectations in one reviewable fixture.

- Aegis has two distinct fixture levels. `trigger-health-matrix.json` is compact and diagnoses routing failures by layer. `workflow-quality-matrix.json` is richer and checks output shape, workspace policy, artifacts, and verification signals. Loom's current activation tests are closer to Aegis's trigger-health level; Loom lacks the richer workflow-quality fixture concept.

- Aegis tests skill-description discipline statically: active skill descriptions must start with `Use when` and avoid workflow summaries. Loom already moved in this direction after `research:20260513-superpowers-skill-activation`, but Aegis shows a broader product-quality check around description shape and trigger health.

- Aegis's context-budget check is worth studying. It limits `using-aegis` hot-path size, keeps red flags and priority detail in a reference, requires bounded history/log searches, checks prompt-hygiene documentation, and verifies bootstrap surfaces do not claim full skill injection. Loom has safety doctrine, but not an equivalent automated context-budget/product-surface guardrail.

- Aegis's prompt-hygiene doctrine is more operational than Loom's current safety references. It names an `Evidence Index Before Evidence Payload` shape, a host-context intake order of `index -> window -> excerpt -> expand`, and a bounded `scripts/log-window.sh` helper that refuses directory input and line windows above 200. Loom's `using-loom` safety doctrine already treats logs/tool output as data, but Aegis provides a sharper reusable procedure for large logs, transcripts, retrieval output, and repeated policy-warning text.

- Aegis's boundary-compliance check automates a concern that Agent Loom currently carries mostly in `AGENTS.md`: product-surface leakage and authority drift. Aegis scans agent-facing prompt assets for phrases that would overclaim completion authority or final gate decisions. Loom's analogous high-value static check would scan model-visible surfaces for contributor-facing leakage and inappropriate authority claims.

- Aegis's install/discovery doctor is user-support useful. It verifies key skills, workspace helper support, config status, hot-path freshness, stale pattern absence, optional discovery-root freshness, and no live workspace shipped inside the method-pack repo. Loom currently has package smoke and pack checks, but not a user-facing install doctor. This could reduce adapter-support ambiguity, though adding helper-script assumptions would be a real architecture choice for Loom.

- Aegis's `activation_mode = auto | explicit` is a useful user-control pattern. For Loom, the direct transfer is limited: Playbooks already moved toward explicit macros, while Core Loom's value depends on always-on routing. A Core-wide explicit mode could undercut Loom's control-plane promise unless treated as an advanced opt-out, not the normal path.

- Aegis's runtime-ready artifact taxonomy overlaps with things Loom deliberately keeps in separate surfaces. `TaskIntentDraft`, `BaselineReadSetHint`, `ImpactStatementDraft`, `EvidenceBundleDraft`, `TodoCheckpointDraft`, `ResumeStateHint`, `DriftCheckDraft`, and `SubagentContextPacket` are useful names, but copying them as new Loom artifacts would risk duplicating specs, tickets, evidence, plans, knowledge, and the recently retired packet pattern.

- The deep clone confirmed that Aegis's runtime-ready artifact taxonomy is not just docs prose. `scripts/aegis-workspace.py` can create `docs/aegis/`, JSON sidecars, lifecycle work files, drift checks, evidence bundle drafts, resume hints, and proof bundles. This is deliberately bounded as method-pack structure, but it is still a helper-script-supported project workspace. Loom's current repo guidance explicitly says not to add daemon, database, dashboard, CLI, or helper-script assumptions unless changing architecture; copying this part would be a product-architecture change, not a simple doctrine edit.

- Aegis's `SubagentContextPacket` is only a compact delegation packet and repeatedly says it is not proof. Even so, copying the name would conflict with Loom's recent packet retirement. Loom already has a better place for durable worker context: tickets and linked records. The transferable idea is not the artifact; it is the warning to pass must-read excerpts and unsafe assumptions rather than full chat history.

- Aegis's `goal-framing` idea is a compact user-facing entry point: goal, success evidence, stop condition, non-goals, route, next. Loom Weaver already does this conversationally and can preserve it into specs/tickets/plans. A direct command could be convenient, but it is a workflow affordance, not a new durable surface.

- Aegis's current command story is not a model for Loom Playbooks. The inspected `commands/brainstorm.md` is deprecated and tells users to use the `aegis:brainstorming` skill instead. Loom's Playbook direction is the opposite: explicit command macros exist to keep optional workflow lenses out of natural model activation.

- Aegis uses `docs/current/` as a high-authority repository baseline and current-doc corpus for contributors. That works for Aegis, but it is not a transferable model-visible pattern for Loom. Loom's existing constraint remains important: consuming agents do not reliably see README/protocol docs unless the harness injects them, so runtime doctrine must live in shipped skills, Playbooks, or intentional agent prompts.

- Aegis's explicit skill request test currently warns, rather than fails, when commands/tools run before the requested skill is loaded. Loom's local `tests/explicit-skill-requests/run-test.sh` has already hardened this into a failure after the product-surface scan follow-up. This is a case where Loom is now stricter than Aegis.

## Precise Similarity And Difference Map

### Same Shape

Both Agent Loom and Aegis are Markdown-first method packs for AI coding agents, not conventional application runtimes. Both ship behavior through skills, prompts, manifests, hooks, and adapter packaging rather than through a daemon or central service.

Both inherit from or respond to the Superpowers lineage: skill discovery, forceful skill activation, multi-host support, TDD/debugging/review workflows, and tests that inspect whether agents actually load skills.

Both use adapter bootstrap to make the method visible early. Aegis injects a compact `using-aegis` hot path in OpenCode and hooks. Loom injects stripped `using-loom` doctrine plus ordered references into the first user message and registers Core skills.

Both reject unsupported completion claims. Aegis says evidence before claims and uses Evidence Cards. Loom routes observations into evidence records, treats worker reports as claims, and uses audit when closure needs adversarial review.

Both distinguish method guidance from final authority. Aegis repeatedly says method-pack outputs are drafts, hints, projections, not authoritative `GateDecision` or completion authority. Loom distinguishes records, evidence, audit, and operator authority, and does not let evidence or audit decide intent.

Both have a long-task/handoff concern. Aegis uses checkpoints, resume hints, drift checks, and subagent context packets. Loom uses ticket-owned Ralph runs, ticket state, evidence, audit, and record reconciliation.

Both care about prompt hygiene. Aegis has a dedicated prompt-hygiene current doc and bounded evidence intake procedure. Loom's `using-loom` safety reference treats logs, records, generated files, worker reports, and external material as data unless higher authority makes them actionable.

Both are trying to prevent the same broad agent failure modes: premature implementation, weak scope, unsupported done claims, stale context after compaction, subagent drift, local symptom patches, and user-visible process theater.

### Different Center Of Gravity

| Axis | Agent Loom | Aegis |
| --- | --- | --- |
| Primary identity | Human-agent control plane / recovery graph | Architecture-driven method pack |
| Durable workspace | `.loom/` surfaces | Optional `docs/aegis/` workspace |
| Truth model | Surface ownership: constitution, specs, plans, tickets, evidence, audit, research, knowledge | Draft/hint/projection artifacts plus baseline/ADR/process docs |
| Default activation | Strict always-on Core routing; 1% skill threshold | Automatic by default, but current hot path loads skills only when explicitly requested or clearly relevant |
| Optional workflows | Playbooks are explicit macros/lenses | Workflows are skills; current legacy commands are deprecated toward skills |
| Execution unit | Ticket is the fundamental executable work unit | Plan/task/work-record flow; no single ticket surface equivalent |
| Worker discipline | Ralph bounded worker/review runs from tickets or owning records | Subagent-driven development with `SubagentContextPacket`, checkpoints, and review stages |
| Review trust | Audit is a separate Loom surface for adversarial review findings | Code review and verification are advisory; no separate audit record surface |
| Evidence owner | `.loom/evidence/` owns observed facts | `EvidenceBundleDraft`, evidence card, and work-record evidence notes |
| Long-task state | Ticket journals/state plus linked records/evidence/audit | `TodoCheckpointDraft`, `ResumeStateHint`, `DriftCheckDraft`, proof bundle |
| Architecture memory | Constitution decisions/specs/plans/knowledge by truth type | ADRs, baseline snapshots, baseline governance, ADR auto-backfill |
| Context strategy | Preloads full Core doctrine/references for strong routing | Compact hot path; detailed discipline in references; explicit context-budget tests |
| Helper tooling | Current repo guidance avoids helper-script assumptions unless architecture changes | Ships `aegis-doctor.py`, `aegis-workspace.py`, `log-window.sh` |
| Product docs role | Human-facing docs restate model; runtime doctrine must be in skills/playbooks/agents | `docs/current/` is high-authority repo baseline for contributors and projected into skills |
| Safety failure emphasis | Truth-surface confusion, retroactive tickets, unbounded Ralph, unsupported closure | Architecture drift, baseline defects, fallback growth, prompt-context bloat, completion authority drift |

### Activation Differences

Loom's Core is stricter. `using-loom` requires relevant skill invocation before responding, clarifying, exploring, quick checks, editing, ticket creation, Ralph launches, evidence claims, audit claims, or closure. The threshold is explicitly `1% chance a skill might apply`.

Aegis's current `using-aegis` is a compact router. It says to check whether an Aegis skill is explicitly requested or clearly relevant, load only that skill, otherwise proceed normally. Its full discipline reference still contains anti-rationalization language, but it also preserves fast-path cheapness and warns not to broaden every trigger.

Implication for Loom: Aegis is not evidence that Loom should relax activation. It is evidence that Loom should measure false positives, context cost, and trigger-health layers more explicitly.

### Record And Artifact Differences

Loom records are authoritative by truth type. A ticket does not own intended behavior; a spec does. Evidence does not decide intent; it records observations. Audit does not implement; it records adversarial review verdicts. This is the core Loom distinction.

Aegis artifacts are mostly process projections. `TaskIntentDraft`, `BaselineReadSetHint`, `ImpactStatementDraft`, `EvidenceBundleDraft`, `GateInputPack`, `TodoCheckpointDraft`, `ResumeStateHint`, `DriftCheckDraft`, and `SubagentContextPacket` are useful runtime-ready shapes, but they are explicitly drafts, hints, or future-runtime inputs.

Implication for Loom: Aegis artifact names may inspire compact output contracts, but adopting them as records would blur Loom's ownership model.

### Worker And Review Differences

Loom retired packet records and made tickets own durable worker context. Ralph remains the bounded worker/review discipline. Worker launch prompts are transient; returned worker output must be reconciled into tickets, evidence, audit, or another owning surface.

Aegis still uses a compact packet concept for delegation, but calls it non-authoritative and says subagents should verify raw excerpts. It has staged review in `subagent-driven-development` and a `code-reviewer` projection, but not a separate audit surface.

Implication for Loom: the transferable idea is bounded must-read excerpts and unsafe assumptions, not a `SubagentContextPacket` record.

### Validation Differences

Aegis has broader static validation around workflow quality, context budget, trigger health, and authority drift. Its matrices include positive and negative cases, expected output shape, workspace policy, expected artifacts, and verification signals.

Loom currently has package smoke/pack checks, activation tests, explicit skill request tests, Playbook no-autoactivation checks, and Markdown diff checks. Loom's explicit-skill test is stricter than Aegis's current explicit request test because Loom fails premature non-skill tool use instead of warning.

Implication for Loom: the most direct adoption path is validation shape, not workflow doctrine.

### Packaging And Adapter Differences

Both support multiple hosts and use similar surfaces: Claude/Cursor plugin manifests, Codex plugin manifests, OpenCode plugin entrypoints, hooks, Gemini context, skills, commands, and agents.

Loom is split into Core and Playbooks packages. Core is always-on doctrine and record skills; Playbooks are optional explicit macro lenses. Aegis is one method pack with all workflow skills in one corpus.

Loom's Playbooks now intentionally move away from implicit skill discovery. Aegis's inspected command file for `brainstorm` is deprecated and points users back to skills.

Implication for Loom: Aegis packaging is useful for host-compatibility comparison, but not for Playbook invocation semantics.

## Tradeoffs

- Keep Loom's full `using-loom` preload.
  - Strength: maximizes first-action surface routing and reduces silent scope invention.
  - Weakness: context-heavy and may create over-activation anxiety.
  - Best when Loom prioritizes reliability over first-token cheapness.

- Move toward an Aegis-style compact hot path plus references.
  - Strength: lower context load, clearer fast path, easier context-budget testing.
  - Weakness: may weaken the always-on surface distinctions unless activation tests prove agents still route correctly.
  - Should be treated as a research spike, not a casual refactor.

- Add Aegis-style quality fixtures without changing doctrine weight.
  - Strength: captures the highest-value lesson while preserving Loom's current product model.
  - Weakness: adds test/fixture maintenance.
  - Recommended first.

- Add a Loom install/discovery doctor.
  - Strength: better user support across adapters and clearer failure diagnosis.
  - Weakness: risks moving Loom toward helper-script/product-runtime assumptions if not bounded as package inspection only.
  - Worth shaping only if adapter support friction is recurring.

## Rejected Paths And Null Results

- Do not copy Aegis's `docs/aegis/` workspace model into Loom. Loom already has `.loom/` as a durable recovery graph with owned surfaces.

- Do not recreate `SubagentContextPacket` as a Loom durable artifact. `decision:0002` and `spec:ticket-owned-worker-handoffs` deliberately moved worker context into tickets and linked records.

- Do not recreate `docs/aegis/work/` as a second Loom task-process tree. Loom tickets, evidence, audit, specs, plans, research, and knowledge already own those truths.

- Do not adopt Aegis's future runtime-core vocabulary as Loom product language. Loom is a Markdown control plane, not a promised authoritative runtime core.

- Do not make Core Loom explicit-only by default. That would conflict with Loom's always-on routing purpose. Playbooks are the appropriate explicit-macro layer.

- Do not treat Aegis's heavier docs/current corpus as a model-visible product-surface pattern. Agent Loom's existing rule remains right: model-visible doctrine belongs in shipped skills, playbooks, and intentional agent prompts, not scattered docs.

- Do not adopt Aegis's deprecated command posture for Loom Playbooks. Loom explicitly needs Playbook command/macros as an activation-pressure solution.

## Conclusions

- Aegis is closest to Loom in problem space, but its best transferable ideas are around validation, support diagnostics, prompt-hygiene procedure, and operational guardrails, not the core conceptual model.

- Loom's surface graph is stronger than Aegis's draft/hint/projection artifact vocabulary for durable work ownership. The Aegis artifact names are useful inspiration for output contracts, but they should not become new Loom surfaces.

- Loom's activation discipline is currently stronger than Aegis's. Aegis is useful as a pressure test for context budget and false-positive control, not as a reason to relax Loom's first-action skill rule.

- The highest-leverage next move is a Loom activation/workflow quality matrix that combines expected Core route, forbidden Playbook autoactivation, false-positive cases, output shape, record policy, evidence expectation, and stop condition.

- The second highest-leverage next move is a static product-surface guardrail that automates known Loom risks: contributor-facing leakage in model-visible surfaces, stale adapter/test-harness details in product doctrine, and overclaiming authority/completion/evidence/audit.

- A compact `using-loom` hot path may be worth investigating, but only behind evidence that routing compliance stays high. It should not be assumed superior just because it is cheaper.

## Recommendations

1. Shape a Loom-specific activation quality baseline before changing source. It should be owned by a spec or research-backed ticket and include representative prompts for Core skill routing, explicit Playbook invocation, natural-prompt no-Playbook cases, evidence/audit claims, worker requests, tiny fast-path tasks, and context-pressure continuation.

2. Create a bounded ticket, if the operator wants execution, for a static product-surface leakage and authority-drift check over `loom-core/skills/`, `loom-playbooks/playbooks/`, `loom-core/agents/`, and `loom-core/codex/agents/`.

3. Consider a Loom prompt-hygiene procedure or test inspired by Aegis's `index -> window -> excerpt -> expand` discipline, especially for logs, transcripts, long command output, retrieval results, and repeated host policy warnings. The likely consuming surface is `using-loom` safety references, `loom-evidence`, or `loom-knowledge`, not a new durable record type.

4. Defer any `using-loom` compact-hot-path redesign until there is a research spike with activation tests comparing current full preload against a compact-router-plus-references variant. The hypothesis should be that context load falls without reducing Core routing compliance; do not assume this from Aegis.

5. Treat an install/discovery doctor as a separate product decision. If pursued, frame it as package inspection and adapter-support diagnostics, not as a Loom runtime, daemon, or new execution authority.

6. Reuse Aegis's goal-frame output shape conversationally in Weaver when helpful, but route durable results into existing Loom specs, tickets, plans, or research rather than creating a new goal artifact surface.

## Open Questions

- Should Loom's next validation artifact be a single JSON matrix like Aegis, or Markdown scenarios plus shell tests consistent with the current repository style?
- Should product-surface leakage checks live as package smoke, a separate test script, or a documented grep checklist?
- Is context load currently a real operator pain for Loom Core, or merely a theoretical cost?
- Would users benefit from a Core explicit opt-out, or would that mainly disable the behavior Loom exists to provide?
- Should Loom add a prompt-hygiene / bounded evidence intake procedure as knowledge first, or directly into `using-loom` safety references and evidence skill guidance?
- Should Loom's static guardrails scan only shipped model-visible product surfaces, or also human-facing docs that restate model behavior?

## Related Records

- `research:20260516-product-surface-scan` - prior internal scan that already identified activation validation, command metadata, generic install safety, and prompt duplication improvements.
- `research:20260513-superpowers-skill-activation` - predecessor research on Superpowers activation discipline, which Aegis inherits and extends.
- `spec:playbook-explicit-macros` - current Loom answer to explicit workflow lenses and Playbook autoactivation pressure.
- `decision:0002` and `spec:ticket-owned-worker-handoffs` - reason not to copy Aegis's subagent packet artifact as a durable Loom surface.
- `loom-core/skills/using-loom/SKILL.md` and ordered references - current Core preload and routing doctrine.
