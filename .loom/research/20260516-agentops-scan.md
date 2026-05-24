# AgentOps Repository Scan

ID: research:20260516-agentops-scan
Type: Research
Status: completed
Created: 2026-05-16
Updated: 2026-05-16

## Summary

This scan reviewed `boshu2/agentops` for transferable ideas for Agent Loom. The strongest lessons are AgentOps's context-density heuristic, public-claim evidence ledger, persona-constrained red-team probes, eval/canary schema discipline, and write-surface doctor pattern; the major non-lesson is that Loom should not copy AgentOps's CLI/daemon/software-factory product shape or broad `.agents/` artifact taxonomy.

## Question

What, if anything, should Agent Loom learn from `https://github.com/boshu2/agentops` without weakening Loom's Markdown control-plane boundary, surface ownership model, ticket-owned Ralph execution, evidence posture, or audit discipline?

## Scope

Covered:

- Public GitHub repository metadata for `boshu2/agentops`, fetched on 2026-05-16.
- Local clone of `boshu2/agentops` main branch at commit `d68db1893cd2485be94f0aaed3e1153f2fd04f2c` (`2026-05-15T20:25:27-04:00`, commit subject `fix(docs): convert cross-tree doc links to absolute URLs for mkdocs strict`).
- Repository product framing, model-visible skill surfaces, docs, schemas, eval/canary fixtures, hook/plugin surfaces, and representative CLI code that reveal transferable patterns for Agent Loom.
- Comparison against current Agent Loom constraints and recent records around product-surface leakage, activation validation, Playbook explicitness, ticket-owned worker handoffs, evidence, and audit.

Excluded:

- Executing untrusted external repository scripts.
- Treating AgentOps source as authority for Agent Loom behavior.
- Creating implementation tickets before the operator selects a direction.
- Source changes outside `.loom/`.
- Full line-by-line audit of AgentOps correctness, security, or runtime claims.

## Method And Sources

- `https://api.github.com/repos/boshu2/agentops` - public metadata observed `default_branch: main`, `pushed_at: 2026-05-16T00:30:29Z`, 350 stars, 34 forks, 9 open issues, primary language Go, and description "The operational layer for coding agents. Memory, validation, and feedback loops that compound between sessions." The GitHub API returned license `NOASSERTION`; the README text says Apache-2.0.
- Local clone at `/var/folders/1b/6mg4g2fs2zx99h46b9j5r7mh0000gp/T/opencode/agentops-scan-20260516-loom` - temporary source inspection only.
- `README.md` - product framing, install paths, CDLC narrow waist, four layers, RPI/council examples, CLI and daemon positioning.
- `PRODUCT.md`, `GOALS.md`, `PROGRAM.md`, `PRACTICE-REGISTRY.md`, `MEMORY.md` - product identity, desired-state gates, autonomous-slice contract, practice lineage, and project memory examples.
- `docs/context-lifecycle.md`, `docs/knowledge-flywheel.md`, `docs/trust-factory.md`, `docs/domain-practice-packets.md`, `docs/architecture/operating-loop.md`, `docs/templates/intent-issue.md`, and `docs/templates/slice-validation.md` - lifecycle and validation doctrine, context-density rule, trust primitive, BDD/slice/wave execution shape.
- `skills/using-agentops/SKILL.md`, `skills/rpi/SKILL.md`, `skills/council/SKILL.md`, `skills/pre-mortem/SKILL.md`, `skills/vibe/SKILL.md`, `skills/forge/SKILL.md`, and `skills/red-team/SKILL.md` plus selected references - representative model-visible operational doctrine.
- `docs/contracts/factory-claim-ledger.md`, `factory-claim-ledger.example.json`, and `factory-claim-ledger.schema.json` - public claim marker/evidence posture pattern.
- `docs/contracts/agents-write-surfaces.md`, `docs/agents-operator-guide.md`, and representative CLI files `cli/cmd/ao/agents*.go` - write-surface inventory, lint, and doctor pattern.
- `schemas/skill-frontmatter.v2.schema.json`, `registry.json`, `hooks/hooks.json`, `hooks/codex-hooks.json`, `.opencode/plugins/agentops.js`, `.codex/agentops-bootstrap.md`, and `.codex-plugin/plugin.json` - runtime/catalog/adapter metadata surfaces.
- `evals/agentops-core/*.json` representative fixtures including `core-surfaces`, `skill-change-scorecard`, `red-team-adversarial-validation`, `retrieval-contracts`, `workbench-behavioral-v1`, `model-upgrade-readiness`, and `lid-primitives-demo`; `evals/workbench/results/2026-05-06-yjzp9-counterstat.json` - offline canary and behavioral-eval patterns.
- `research:20260516-aegis-method-pack-scan` - prior external method-pack scan that sets a useful comparison pattern.
- `research:20260516-product-surface-scan` - current internal Agent Loom product-surface baseline and known improvement areas.

Source quality note: this is source-backed external repository research but not live validation of AgentOps behavior. The clone and public metadata are strong enough for product-shape and transferable-pattern analysis; AgentOps's own runtime, daemon, multi-agent, and evidence claims were not independently executed.

## Findings

### F1. AgentOps is much more of a runtime/control-plane product than Loom

AgentOps positions itself as an "engineering operating system for agent teams" with three surfaces: in-harness skills/hooks, the `ao` CLI, and a scheduling daemon. Its product story centers on `.agents/` as a repo-local wiki/ledger that records runs, findings, learnings, councils, evidence, and scheduling state, then compiles that corpus back into future sessions.

That is adjacent to Loom's recovery graph, but materially broader. AgentOps assumes many helper scripts, a Go CLI, hooks, a daemon, schedules, generated registry files, runtime state, and a large skill catalog. Agent Loom's repo guidance explicitly says this repo ships a Markdown skill corpus, not an app runtime. The transferable ideas must therefore be harvested as record/validation/product-discipline patterns, not as an argument to add AgentOps-like runtime machinery.

### F2. The Context Density Rule is highly transferable

AgentOps repeatedly uses a compact invariant: every high-value context token should carry one of six payloads: intent, boundary, evidence, decision, constraint, or next action. The dedicated domain reference calls this the "Context Density Rule" and applies it to prompts, packets, handoffs, plans, verdicts, and skills.

Loom already says record when it helps and avoid ceremony, but AgentOps's six-payload vocabulary is sharper and more operational. It maps cleanly onto Loom's surfaces:

- intent -> specs, tickets, plans
- boundary -> tickets, plans, specs, constitution
- evidence -> evidence records, ticket acceptance, audit inputs
- decision -> constitution, specs, research conclusions, ticket state
- constraint -> constitution, specs, ticket stop conditions
- next action -> tickets, plans, handoffs

This should not become a new durable surface. It is a compression heuristic that could strengthen Weaver's shaping responses, ticket acceptance language, Ralph launch context, and maybe a future static review checklist for model-visible doctrine.

### F3. The public claim ledger is the strongest governance pattern

AgentOps marks public claim-bearing prose with stable HTML comments such as `<!-- agentops:claim:AOP-CLAIM-README-FACTORY-CONTEXT -->`, then joins those markers to a machine-readable ledger row. Rows record current evidence, missing proof, owner issue, validation level `L0-L3`, closure gate, release posture, evidence status, authority state, promotion state, anti-overclaim wording, and evidence artifacts. The contract explicitly fails strict checks when high-claim language lacks a marker, markers are orphaned, enums drift, or L2/L3 claims lack evidence artifacts.

This pattern fits Loom better than most AgentOps runtime machinery because Loom already separates evidence, audit, and durable claims. Loom currently relies on doctrine and records to prevent unsupported closure/product claims; AgentOps shows a concrete way to make human-facing public claims mechanically visible and anti-overclaim wording explicit.

The direct transfer should be bounded: a Loom claim ledger would govern human-facing product/docs/release claims, not become a new proof authority for code correctness. Evidence and audit records would still own observations and review verdicts; the ledger would be a cross-reference and posture surface or test fixture.

### F4. Persona-constrained red-team probes are a useful audit lens

AgentOps's `/red-team` differs from council review: constrained personas attempt real tasks from limited context. Built-in examples include `panicked-sre`, `junior-engineer`, `first-time-consumer`, and `zero-context-agent`; the skill restricts allowed paths, excluded knowledge, and forbidden actions, then records PASS/FAIL/PARTIAL with navigation path, friction, evidence, severity, and recommendations.

For Loom, this is more useful than another generic review rubric. Current Loom audit can challenge claims, but a persona-constrained probe would test whether a future installed-model consumer can actually navigate a skill, Playbook, docs path, or ticket context without repository-maintainer knowledge. The strongest transfer is a red-team audit mode for:

- model-visible Core skills and Playbooks as `zero-context-agent`
- install/docs surfaces as `first-time-consumer`
- Ralph handoff tickets as `implementation-worker-with-only-ticket-context`
- closure/evidence claims as `skeptical-reviewer-with-only-record-graph`

This should route through `loom-audit` when a verdict is needed, not become a separate Loom surface.

### F5. Eval/canary schema discipline is stronger than Loom's current ad hoc validation surface

AgentOps carries many offline canary JSON suites with explicit fields for `visibility`, `tier`, `allowed_runtimes`, `offline_required`, `network`, scrubbed environment prefixes, timeouts, scoring dimensions, baseline policy, cases, objectives, expectations, and criticality. Representative suites cover skill-change scorecards, red-team contract parity, retrieval contracts, model-upgrade baseline regression, and workbench behavioral fixtures.

This reinforces the Aegis finding that Loom's next validation layer should not only be smoke commands. A Loom-specific validation matrix could name prompt/skill scenarios, expected route, forbidden route, record policy, evidence expectation, network posture, and whether the check is static, harness-live, or manual. The key lesson is not AgentOps's Go eval runner; it is the habit of making each validation case explicit about environment, dimensions, baseline posture, and proof limits.

### F6. Write-surface inventory and doctor pattern is useful, but only as static graph hygiene

AgentOps has a contract for `.agents/` write surfaces, a lint gate that scans production code for `.agents/<X>` literals, and `ao agents inspect|lint|doctor` commands that surface catalogued directories, skill-owned subdirs, orphans, and undocumented dirs.

Loom's `.loom/` graph is intentionally smaller and surface-owned, so it does not need AgentOps's broad directory taxonomy. But a static graph hygiene check could be valuable: verify records have IDs, types, statuses, dates, valid surface paths, expected filename/ID alignment, no raw artifacts without parent records, no evidence/audit overclaims, and no product-surface leakage into model-visible doctrine. This should be a repository validation/checklist or future ticket if selected, not a runtime CLI prerequisite.

### F7. BDD-shaped intent and vertical-slice/wave validation are partially transferable

AgentOps's operating loop requires BDD-shaped intent issues, vertical slices, a first failing test per slice, wave validity checks for parallel work, and roll-up acceptance mapping every Given/When/Then to proof. This is a coherent engineering loop for code execution.

Loom should not make BDD/TDD universal doctrine because Loom's Core is a control plane across many work types, not a code methodology package. However, the pieces are valuable when tickets route to implementation:

- acceptance examples can make specs/tickets less vague
- first-failing-test language can strengthen tickets for behavior-changing code when tests are appropriate
- wave validity maps directly to multi-Ralph or parallel worker planning: distinct write scopes, no shared migration/generated files, declared integration order, owner per slice, discard path per slice
- roll-up acceptance maps to Loom ticket closure: every acceptance criterion must have evidence, not activity logs

This is best as optional ticket/planning pressure, not Core doctrine.

### F8. Practice registry and skill metadata are informative but likely too heavy for Loom now

AgentOps annotates skills with practice slugs, `hexagonal_role`, `consumes`, `produces`, `context_rel`, tier metadata, context-window intent, and output contracts. It also generates a large `registry.json` cataloging skills, hooks, knowledge stores, job types, evals, commands, and recommended cadences.

This is impressive for a runtime product, but it is mostly not a Loom fit. Loom already has simpler surface ownership and skill descriptions. Adding broad metadata would increase product-surface weight and risk turning Loom into a catalog-management project. The narrow transfer is worth considering only where it solves known drift: e.g., `produces`/`consumes` or explicit output contracts for Playbook command generation and validation fixtures.

### F9. AgentOps exposes useful cautionary failure modes

AgentOps's ambition produces the very risks Loom is trying to avoid:

- many public claims require an explicit claim ledger because product copy easily outruns evidence
- a large catalog creates adapter parity, generated artifact, and command/skill drift pressure
- model-visible skills often mention hooks, CLI commands, runtime modes, daemon behavior, and repository-specific details
- install and runtime support require substantial tooling, docs, and smoke tests
- `.agents/` becomes a sprawling state taxonomy that needs its own hygiene tools

These are not flaws relative to AgentOps's chosen product; they are consequences of choosing a runtime/CLI/daemon product. For Loom, they are cautionary evidence supporting the existing boundary: keep product doctrine in model-visible skills/agents, contributor/runtime mechanics outside product doctrine, and durable truth in a small owned surface graph.

## Tradeoffs

- Adopt the Context Density Rule as a Loom wording/checklist heuristic.
  - Strength: improves all Loom handoffs and records without changing the surface graph.
  - Risk: if phrased as another mandatory doctrine block, it adds token load and ceremony.
  - Best route: weave into Weaver/ticket/Ralph context guidance when those surfaces are already being edited.

- Add a Loom claim-ledger/check for public docs/product claims.
  - Strength: directly supports Loom's evidence/audit honesty and product-surface anti-overclaim posture.
  - Risk: can become bookkeeping theater if every mild sentence needs a ledger row.
  - Best route: narrow to high-claim human-facing docs, launch/release claims, and claims using trigger words such as validated, audited, evidence-backed, review-complete, autonomous, or guaranteed.

- Add persona-constrained red-team audit probes.
  - Strength: tests whether records and product surfaces work for future agents with limited context, which normal expert review often misses.
  - Risk: can be expensive/noisy if used on every change.
  - Best route: use for model-visible surface changes, installation/onboarding docs, ticket/Ralph handoff templates, and closure/evidence claims.

- Copy AgentOps's CLI/daemon/flywheel automation.
  - Strength: would provide concrete retrieval, doctor, eval, and scheduling machinery.
  - Risk: directly conflicts with this repo's current architecture and would move Loom from Markdown skill corpus toward app/runtime product.
  - Not recommended without a separate constitution-level architecture decision.

## Rejected Paths And Null Results

- Do not copy AgentOps's `.agents/` taxonomy into `.loom/`. Loom's surface graph is cleaner and ownership-based; AgentOps's taxonomy exists to support a much broader runtime product.

- Do not add an `ao`-style CLI, scheduling daemon, or automatic flywheel as a casual follow-up. That would be an architectural product change, not a research lesson.

- Do not promote BDD/TDD/DDD/hexagonal practice as universal Loom Core doctrine. Those are useful execution lenses, but Loom must also shape research, specs, plans, evidence, audit, and project judgment outside code-delivery tasks.

- Do not add broad skill frontmatter metadata merely because AgentOps has it. Loom's activation discipline depends more on clear descriptions, owned surfaces, and explicit Playbook invocation than on a large generated registry.

- Do not treat AgentOps's dogfood corpus counts or runtime claims as evidence for Loom. They are AgentOps's claims and were not independently validated here.

## Conclusions

- AgentOps is most useful to Loom as a source of governance and validation patterns, not as a product-shape template.

- The highest-leverage lesson is the claim ledger: Loom could mechanically bind public product/release/doc claims to evidence/audit posture without weakening evidence and audit surface ownership.

- The second-highest lesson is persona-constrained red-team probing: Loom audits should sometimes ask whether a constrained future agent or first-time consumer can actually use a surface, not only whether an expert reviewer approves it.

- The third-highest lesson is context density: Loom already values concise durable truth, but AgentOps's six-payload vocabulary gives a reusable check for whether a record, ticket, or launch prompt is carrying useful context.

- AgentOps's BDD vertical-slice and wave-validity model is valuable for implementation tickets and parallel worker planning, but it should remain optional/task-shaped pressure rather than Core Loom identity.

- AgentOps's own sprawl is a warning: adding runtime, CLI, daemon, hook, and broad-catalog assumptions creates substantial validation and product-surface leakage work. Loom should preserve its Markdown-native boundary unless the operator explicitly changes the architecture.

## Recommendations

1. If the operator wants an execution follow-up, shape a small spec for a Loom public-claim posture check. Candidate scope: human-facing docs and release/launch claims only; output should map claim IDs to evidence/audit posture and anti-overclaim wording, while leaving evidence and audit records authoritative.

2. Shape a Loom audit playbook or spec addition for persona-constrained red-team review. Start with `zero-context-agent` over model-visible Core/Playbook surfaces and `worker-with-ticket-only-context` over Ralph handoff tickets.

3. Consider adding the six-payload Context Density Rule as a lightweight heuristic in the next planned edit to Weaver/ticket/Ralph guidance. Do not add it as a new surface or broad doctrine rewrite by itself.

4. Use AgentOps's eval/canary shape when designing Loom validation around activation, explicit Playbooks, product-surface leakage, and model-visible authority drift: each case should name environment, expected route, forbidden route, scoring/criticality, network posture, and proof limits.

5. Defer any `.loom` graph doctor until there is a concrete pain point or selected ticket. If pursued, keep it static and repo-local; do not introduce runtime daemon or CLI assumptions.

## Open Questions

- Should Loom's public-claim governance live as a dedicated research/spec-backed validation fixture, a docs checklist, or a small record under constitution/knowledge?
- Which Loom surfaces most need persona-constrained red-team review first: Core skills, Playbooks, named agents, install docs, or ticket/Ralph handoff records?
- Is the Context Density Rule already implicit enough in Loom doctrine, or would naming it improve future records without adding ceremony?

## Related Records

- `research:20260516-aegis-method-pack-scan` - recent external scan whose conclusions help distinguish transferable validation/guardrail ideas from incompatible surface-taxonomy changes.
- `research:20260516-product-surface-scan` - current baseline of Agent Loom's product-surface strengths and known drift/polish issues.
- `research:20260513-superpowers-skill-activation` - earlier source for activation discipline and skill-description trigger posture.
- `spec:playbook-explicit-macros` - current Loom answer to implicit Playbook activation pressure; relevant to eval/canary recommendations.
- `decision:0002` and `spec:ticket-owned-worker-handoffs` - current Loom worker-context model; relevant to rejecting AgentOps packet/runtime taxonomy and adopting only bounded wave/handoff checks.
