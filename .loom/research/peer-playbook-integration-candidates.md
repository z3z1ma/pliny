---
id: research:peer-playbook-integration-candidates
kind: research
status: concluded
created_at: 2026-05-08T01:03:41Z
updated_at: 2026-05-08T01:46:00Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  research:
    - research:peer-engineering-discipline-deep-dive
    - research:external-peer-skill-practices-synthesis
    - research:skill-template-benchmark-synthesis
    - research:superpowers-skill-workflow-adaptation
  decision:
    - decision:0008
  plan:
    - plan:split-core-and-playbooks-packages
external_refs:
  mattpocock_skills_github: https://github.com/mattpocock/skills
  mattpocock_skills_local_clone: file:///var/folders/1b/6mg4g2fs2zx99h46b9j5r7mh0000gp/T/opencode/loom-skill-benchmark-repos/mattpocock-skills
  addyosmani_agent_skills_github: https://github.com/addyosmani/agent-skills
  addyosmani_agent_skills_local_clone: file:///var/folders/1b/6mg4g2fs2zx99h46b9j5r7mh0000gp/T/opencode/loom-skill-benchmark-repos/addyosmani-agent-skills
  superpowers_github: https://github.com/obra/superpowers
  superpowers_local_clone: file:///var/folders/1b/6mg4g2fs2zx99h46b9j5r7mh0000gp/T/opencode/loom-skill-benchmark-repos/superpowers
---

# Question

Which stronger peer skill workflows should Loom bring in-house now that the product surface is split into `loom-core` and optional `loom-playbooks`, and which peer mechanics should instead be folded into existing playbooks or rejected as non-Loom runtime, tracker, or command behavior?

# Why This Matters

Earlier peer-skill passes correctly protected Loom's owner graph and rejected wholesale imports. The core/playbooks split changes the integration question: optional workflow skills no longer have to justify themselves as kernel behavior. A candidate can be good Loom product if it composes over `loom-core`, routes information through canonical records, and avoids creating a second ledger.

# Scope

This pass focuses on candidate `loom-playbooks` skills and playbook references inspired by:

- `mattpocock/skills`
- `addyosmani/agent-skills`
- `obra/superpowers`

It excludes adopting peer command wrappers, hooks, MCP requirements, issue tracker labels, `.superpowers` state directories, PR descriptions, generated plans, or peer docs paths as canonical Loom truth. It also excludes changing `loom-core` membership; `decision:0008` keeps owner layers, Ralph, retrospective, memory, and using-Loom doctrine in core.

# Method

- Re-read prior Loom research on peer skill assimilation and the core/playbooks split.
- Refreshed the existing benchmark clones to current `origin/main` where available.
- Directly sampled peer files that were less fully consumed by prior passes: product ideation, architecture deepening, code simplification, frontend/browser runtime evidence, security hardening, migration/deprecation, CI/CD, triage, visual brainstorming, and skill-testing pressure scenarios.
- Compared each candidate against the current `loom-playbooks/skills` package: `loom-drive`, `loom-git`, `loom-debugging`, `loom-spike`, `loom-codemap`, `loom-ship`, and `loom-skill-authoring`.
- Classified each opportunity as a new playbook candidate, an existing-playbook deepening, or a rejected non-Loom mechanic.

# Sources

- Source: `research:peer-engineering-discipline-deep-dive`
  - Type / provenance: repository research record
  - Observed at / version: current workspace read on 2026-05-08
  - Freshness risk / recheck trigger: stale if peer source mapping or playbook package membership changes materially
  - Trust rationale: accepted prior synthesis for engineering discipline; not a substitute for direct reads in this pass

- Source: `research:external-peer-skill-practices-synthesis`
  - Type / provenance: repository research record
  - Observed at / version: current workspace read on 2026-05-08
  - Freshness risk / recheck trigger: stale if peer-practice assimilation or playbook boundaries change materially
  - Trust rationale: prior direct-read synthesis; advisory to this investigation

- Source: `decision:0008` and `plan:split-core-and-playbooks-packages`
  - Type / provenance: repository constitution decision and active plan
  - Observed at / version: current workspace read on 2026-05-08
  - Freshness risk / recheck trigger: stale if the core/playbooks split is superseded
  - Trust rationale: owning project truth for package membership and playbook/core boundary

- Source: `loom-playbooks/skills/**`
  - Type / provenance: repository product source
  - Observed at / version: current workspace read on 2026-05-08
  - Freshness risk / recheck trigger: stale if playbook skills are added, removed, or substantially rewritten
  - Trust rationale: current implementation reality for available playbook routes

- Source: `mattpocock/skills` local clone
  - Type / provenance: external repository clone, direct file reads
  - Observed at / version: 2026-05-08T01:03:41Z, commit `733d312884b3878a9a9cff693c5886943753a741`
  - Freshness risk / recheck trigger: upstream can change; recheck before implementation tickets depend on exact wording
  - Trust rationale: primary peer source requested by the user; advisory evidence only
  - Key reads: `skills/engineering/improve-codebase-architecture/SKILL.md:8-71`, `DEEPENING.md:5-37`, `INTERFACE-DESIGN.md:9-44`, `LANGUAGE.md:3-53`, `to-prd/SKILL.md:6-76`, `to-issues/SKILL.md:8-83`, `triage/SKILL.md:8-103`, `prototype/SKILL.md:8-30`, `zoom-out/SKILL.md:1-7`, `misc/git-guardrails-claude-code/SKILL.md:6-95`

- Source: `addyosmani/agent-skills` local clone
  - Type / provenance: external repository clone, direct file reads
  - Observed at / version: 2026-05-08T01:03:41Z, commit `742dca58ae557bc67afec9ea8e6de59c085f0534`
  - Freshness risk / recheck trigger: upstream can change; recheck before implementation tickets depend on exact wording
  - Trust rationale: primary peer source requested by the user; advisory evidence only
  - Key reads: `skills/idea-refine/SKILL.md:8-178`, `spec-driven-development/SKILL.md:8-200`, `planning-and-task-breakdown/SKILL.md:8-223`, `incremental-implementation/SKILL.md:8-245`, `test-driven-development/SKILL.md:8-383`, `source-driven-development/SKILL.md:8-194`, `context-engineering/SKILL.md:8-289`, `code-review-and-quality/SKILL.md:8-347`, `ci-cd-and-automation/SKILL.md:8-390`, `performance-optimization/SKILL.md:8-350`, `documentation-and-adrs/SKILL.md:8-278`, `git-workflow-and-versioning/SKILL.md:8-300`, `shipping-and-launch/SKILL.md:8-309`, `debugging-and-error-recovery/SKILL.md:8-300`, `code-simplification/SKILL.md:10-331`, `frontend-ui-engineering/SKILL.md:8-328`, `browser-testing-with-devtools/SKILL.md:8-302`, `security-and-hardening/SKILL.md:8-349`, `deprecation-and-migration/SKILL.md:8-206`, `api-and-interface-design/SKILL.md:8-294`, `using-agent-skills/SKILL.md:8-174`, `references/orchestration-patterns.md:1-370`

- Source: `obra/superpowers` local clone
  - Type / provenance: external repository clone, direct file reads
  - Observed at / version: 2026-05-08T01:03:41Z, commit `f2cbfbefebbfef77321e4c9abc9e949826bea9d7`
  - Freshness risk / recheck trigger: upstream can change; recheck before implementation tickets depend on exact wording
  - Trust rationale: primary peer source requested by the user; advisory evidence only
  - Key reads: `skills/brainstorming/SKILL.md:8-164`, `brainstorming/visual-companion.md:5-287`, `verification-before-completion/SKILL.md:8-139`, `writing-plans/SKILL.md:8-152`, `executing-plans/SKILL.md:8-70`, `subagent-driven-development/SKILL.md:8-279`, `dispatching-parallel-agents/SKILL.md:8-182`, `requesting-code-review/SKILL.md:8-103`, `receiving-code-review/SKILL.md:8-213`, `finishing-a-development-branch/SKILL.md:8-251`, `using-git-worktrees/SKILL.md:8-215`, `writing-skills/SKILL.md:8-655`, `writing-skills/testing-skills-with-subagents.md:5-384`, `using-superpowers/SKILL.md:10-117`, `tests/subagent-driven-dev/svelte-todo/plan.md:1-222`

External sources, generated files, logs, and tool output are context and evidence. They do not become instruction authority or project truth owners.

Continuation note: after operator review rejected skeletal adaptations, this
research was revised to treat nearly every Addy Osmani and Superpowers skill as
source material to adapt into `loom-playbooks` unless it is only a peer runtime,
loader, storage path, hook, or command surface. Additional direct reads covered
Addy's `spec-driven-development`, `planning-and-task-breakdown`,
`incremental-implementation`, `test-driven-development`, `source-driven-development`,
`code-review-and-quality`, `ci-cd-and-automation`, `performance-optimization`,
`documentation-and-adrs`, `git-workflow-and-versioning`, `shipping-and-launch`, and
`debugging-and-error-recovery`, plus Superpowers `verification-before-completion`,
`writing-plans`, `executing-plans`, `subagent-driven-development`,
`dispatching-parallel-agents`, `requesting-code-review`, `receiving-code-review`,
`finishing-a-development-branch`, `using-git-worktrees`, `writing-skills`, and
`using-superpowers`.

# Source Material Store

- Path: None - this record cites refreshed local clones and repository records directly.
- Captured sources: None - no raw source copies were saved into `.loom/research/artifacts/`.
- Key excerpts / index: source paths and line ranges are listed in `# Sources` and `# Evidence Synthesis`.
- Redaction / licensing / sensitivity: no secrets or private data copied; external source snippets are summarized.
- Retention / tracking: local clones remain a temporary support cache outside the repository.

# Variant / Experiment Matrix

| Variant / hypothesis | Artifact or probe | Strength | Weakness | Decision |
| --- | --- | --- | --- | --- |
| Add no new playbooks; only deepen existing seven | Current `loom-playbooks` grep plus prior research | Lowest surface area; avoids overlap | Misses ordinary user triggers now clearly outside core, especially UI/browser, security, migration, simplification, and architecture refactoring | Rejected as too conservative |
| Import peer skills one-for-one into `loom-playbooks` | Peer skill directories | Captures many useful workflows quickly | Duplicates Loom owners, imports peer paths and command assumptions, and weakens graph routing | Rejected |
| Add a small set of optional Loom-native playbooks for recurring non-core workflows | Candidate matrix below | Makes optional workflow pack more useful while preserving `loom-core` boundaries | Requires careful boundaries so playbooks do not become new truth owners | Chosen |
| Put all candidates into one omnibus engineering playbook | Cross-cutting peer practices | Easy discovery in one file | Becomes a shadow operating manual and competes with drive/debugging/ship/codemap/skill-authoring | Rejected |

# Evidence Synthesis

## Current Loom Playbook Gap

The existing playbook package covers objective driving, Git isolation, reproduce-first debugging, bounded spikes/sketches, code maps, shipping packages, and skill authoring. Targeted searches show only partial coverage for security, migration, simplification, frontend/browser runtime evidence, and architecture refactoring:

- `loom-debugging` has a performance branch and root-cause seam language, but no full performance or security hardening workflow.
- `loom-spike` covers UI/product sketches and technical experiments, but not production UI engineering or browser-runtime verification as a standing route.
- `loom-codemap` can identify architectural friction and module boundaries, but it stops at mapping and accepted atlas work; it does not own an architecture-deepening or refactoring campaign.
- `loom-ship` covers feature flags, launch, rollback, and handoff summaries, but not the full replacement, migration, deprecation, usage-zero, and removal lifecycle.
- `loom-drive` can route broad objectives, but a broad route coordinator should not swallow every specialized workflow trigger.

That gap is exactly what `loom-playbooks` is now for: optional higher-level engineering workflows that compose over the core graph.

## Strong New Playbook Candidates

### 1. `loom-architecture`

Candidate strength: high.

Peer signal:

- Matt's architecture skill frames deepening as making modules more testable and AI-navigable, with shared vocabulary for module, interface, depth, seam, adapter, leverage, and locality (`improve-codebase-architecture/SKILL.md:8-29`, `LANGUAGE.md:3-53`).
- It gives concrete friction probes: bouncing across many modules for one concept, shallow interfaces, testability seams, and the deletion test (`improve-codebase-architecture/SKILL.md:33-60`).
- Its deepening reference classifies dependencies and seam strategies, then insists the interface is the test surface and old shallow-unit tests should be deleted after deeper interface tests exist (`DEEPENING.md:5-37`).
- Its interface-design reference uses multiple radically different designs before choosing one (`INTERFACE-DESIGN.md:9-44`).
- Addy's API/interface design adds Hyrum's Law, contract-first design, consistent errors, boundary validation, additive evolution, and interface verification (`api-and-interface-design/SKILL.md:20-145`, `:262-294`).

Loom-native shape:

- Use when the user asks to improve architecture, reduce coupling, design seams, make code more testable, consolidate shallow modules, or define API/module contracts.
- Route structure discovery to `loom-codemap`, tradeoffs and rejected designs to `loom-research`, intended interface behavior to core specs, decomposition to plans, execution to tickets/Ralph, before/after behavior to evidence, and seam/API risk to critique.
- Do not create an architecture ledger. The playbook coordinates: current structure in code/evidence/wiki, intended behavior in specs, strategy in plans, execution in tickets.

Why it should be new rather than folded into `loom-codemap`: codemap maps and explains structure; architecture improvement chooses a mutation path and needs interface/design alternatives, evidence, implementation slices, and critique.

### 2. `loom-product-discovery`

Candidate strength: high.

Peer signal:

- Addy's idea-refine skill has a crisp divergent/convergent loop: understand and expand, evaluate and converge, then produce a one-pager with problem, direction, assumptions, MVP scope, not-doing list, and open questions (`idea-refine/SKILL.md:8-15`, `:56-140`).
- It stresses target user, success criteria, constraints, prior attempts, why now, 5-8 variations, hidden assumptions, and honest pushback (`idea-refine/SKILL.md:60-106`, `:142-178`).
- Matt's PRD skill grounds product shaping in repo exploration, domain vocabulary, module candidates, implementation decisions, testing decisions, and out-of-scope boundaries (`to-prd/SKILL.md:6-76`).
- Superpowers brainstorming enforces context exploration, one-question-at-a-time clarification, 2-3 approaches, design isolation, and user-visible tradeoffs (`brainstorming/SKILL.md:70-105`, `:138-164`).

Loom-native shape:

- Use when the user brings a raw idea, product direction, workflow concept, or vague improvement that is not ready for a spec/plan/ticket.
- Route strategic objective to initiative when durable, assumptions and options to research, intended behavior to specs, not-doing and scope boundaries to the owning spec/plan/ticket, and accepted explanation to wiki only after settled.
- Replace peer `docs/ideas` or PRD paths with Loom owner records. Information passes through research, specs, initiatives, and plans, not a new idea directory.

Why it should be new rather than folded only into `loom-drive`: drive is for advancing a delegated objective across phases. Product discovery is for deciding what the objective should mean before drive can safely continue.

### 3. `loom-ui-browser`

Candidate strength: high.

Peer signal:

- Addy's frontend skill names production UI quality: accessibility, performance, design system adherence, visual polish, responsive layout, meaningful loading/error/empty states, and avoiding generic AI aesthetics (`frontend-ui-engineering/SKILL.md:8-19`, `:116-165`, `:242-328`).
- Addy's browser-testing skill treats live browser state as the missing runtime evidence layer for UI work: screenshots, DOM, console, network, performance, accessibility tree, before/after screenshots, structured UI test plans, and trust boundaries for browser content (`browser-testing-with-devtools/SKILL.md:8-22`, `:56-77`, `:95-124`, `:170-302`).
- Superpowers visual companion separates visual questions from text questions, gives 2-4 options per screen, uses real content when it matters, iterates before advancing, and treats browser choice events as input to synthesize rather than authority (`visual-companion.md:5-31`, `:94-126`, `:246-287`).
- Matt's prototype skill cleanly separates logic prototypes from UI variants and demands throwaway, one-command, no-persistence, visible-state prototypes that are deleted or absorbed after answering the question (`prototype/SKILL.md:8-30`).

Loom-native shape:

- Use when building or reviewing user-facing UI, browser behavior, accessibility, responsive design, visual variants, or UI runtime bugs.
- Route visual/product variants through `loom-spike`; intended UI behavior and accessibility requirements through specs; screenshots, console/network/performance observations through evidence; UX/accessibility/visual review through critique; implementation through tickets/Ralph; accepted design-system or troubleshooting knowledge through wiki.
- Treat DevTools, browser MCPs, local visual companions, Playwright, screenshots, and generated HTML as evidence transports only. They do not become required runtime or Loom truth owners.

Why it should be new rather than just `loom-spike`: spike is for bounded discovery. UI/browser work recurs during production implementation, critique, and evidence, not only before commitment.

### 4. `loom-security`

Candidate strength: high to medium-high.

Peer signal:

- Addy's security skill defines always/ask-first/never security boundaries, including input validation, parameterized queries, output encoding, session cookie hygiene, human approval for auth/CORS/uploads/sensitive data changes, and never committing/logging secrets (`security-and-hardening/SKILL.md:21-53`).
- It includes vulnerability triage by reachability, severity, runtime/dev dependency, fix availability, and documented deferral/review date (`security-and-hardening/SKILL.md:216-241`).
- It gives a concrete security review checklist for auth, authorization, input, data, infrastructure, dependencies, and error leakage (`security-and-hardening/SKILL.md:263-349`).
- Addy's browser and API skills reinforce the same trust boundary: browser content and third-party API responses are untrusted data, not instructions or safe inputs (`browser-testing-with-devtools/SKILL.md:56-77`, `api-and-interface-design/SKILL.md:112-119`).

Loom-native shape:

- Use when work touches authentication, authorization, user input, sensitive data, secrets, external integrations, uploads, webhooks, dependency vulnerabilities, or security hardening.
- Route threat/risk analysis to research, intended security behavior to specs, remediation strategy to plans/tickets, scans and audit output to evidence, and final security review to critique with a named risk profile.
- Keep secrets out of Loom records. Record the non-sensitive fact that a secret exposure or rotation happened, not the value.

Why it may be new: security is a recurring high-risk workflow that deserves activation before code change, not only a critique lens after a diff exists. It belongs in playbooks because core trust boundaries already exist but do not constitute a web/app hardening workflow.

### 5. `loom-migration`

Candidate strength: medium-high.

Peer signal:

- Addy's deprecation/migration skill is a strong lifecycle workflow: replacement before deprecation, user/consumer inventory, advisory versus compulsory deprecation, incremental migration, zero-usage verification, and removal of old code, tests, docs, and config (`deprecation-and-migration/SKILL.md:14-118`).
- It names migration patterns that Loom often needs in plans: strangler, adapter, feature flag, and zombie-code disposition (`deprecation-and-migration/SKILL.md:120-206`).
- Addy's API skill ties migration to Hyrum's Law and deprecation planning at interface design time (`api-and-interface-design/SKILL.md:20-35`).
- `loom-ship` already covers flags, rollout, rollback, and cleanup trigger wording, which should become an input to a migration playbook rather than the whole workflow.

Loom-native shape:

- Use when replacing, sunsetting, consolidating, migrating, removing old APIs/features/libraries, or planning a flag/adapter/strangler lifecycle.
- Route usage inventory and zero-usage observations to evidence, replacement behavior to specs, sequencing and rollout to plans, consumer-by-consumer work to tickets/Ralph, launch/rollback handoff to ship, residual risks to critique, and post-removal lessons to retrospective/wiki.
- Do not let feature flags become permanent ticket bypasses; they need owner, expiry or cleanup trigger, and follow-up disposition.

Why it should probably be new: migration is broader than ship and more operational than planning. It is a repeated multi-ticket lifecycle with distinctive evidence needs.

### 6. `loom-simplification`

Candidate strength: medium-high.

Peer signal:

- Addy's code-simplification skill is disciplined: preserve exact behavior, follow project conventions, prefer clarity over cleverness, avoid over-simplification, and scope to what changed (`code-simplification/SKILL.md:10-42`, `:44-104`).
- It uses Chesterton's Fence before deleting or changing code and requires understanding responsibilities, callers, edge cases, tests, and historical reasons before simplification (`code-simplification/SKILL.md:105-121`).
- It makes simplification incremental and reviewable, with one simplification at a time, tests after each, and separate refactor versus feature changes (`code-simplification/SKILL.md:157-171`).
- It captures common rationalizations and red flags that fit Loom's anti-rationalization style (`code-simplification/SKILL.md:297-331`).

Loom-native shape:

- Use when code works but is harder to read, maintain, review, or extend than it needs to be; when AI artifacts, speculative helpers, dead code, unclear names, or excessive abstraction accumulate; or when a review asks for behavior-preserving cleanup.
- Route behavior preservation to evidence/tests, scope to tickets, architectural simplification to `loom-architecture` or codemap/research, review sufficiency to critique, and durable simplification lessons to retrospective/wiki.
- Require evidence that behavior did not change; do not let simplification silently become feature work or architecture migration.

Why it may be new: the current playbooks mention cleanup, but no playbook owns a behavior-preserving simplification pass. It is narrower than architecture and should be independently activatable.

## Broader Adaptation And Overlap Handling

Operator review clarified that the first six new playbooks were too skeletal and
too conservative. The stronger product move is to adapt nearly every peer skill
into Loom-native playbooks or dense playbook references, while keeping core owner
layers authoritative.

New or broadened playbook targets after owner-boundary audit:

- `loom-incremental-implementation`: Addy's thin-slice execution, scope discipline, feature flags, safe defaults, and per-slice verification become a ticket/Ralph execution playbook.
- `loom-tdd`: Addy's and Superpowers' red/green/refactor, prove-it bug fixes, test pyramid, anti-patterns, and subagent test separation become Loom evidence-backed behavior proof.
- `loom-source-grounding`: Addy's version detection, official-doc source hierarchy, conflict surfacing, and citation discipline become a Loom source/documentation grounding workflow.
- `loom-context-engineering`: Addy's context hierarchy and context-pack practice become a Loom owner-record/source/test/error context assembly workflow.
- `loom-code-review`: Addy's five-axis review and Superpowers review request/reception become a Loom critique/ticket/evidence feedback workflow.
- `loom-ci-cd`: Addy's quality gates, automation feedback, preview deploy, staged rollout, rollback, secret separation, and pipeline optimization become a CI/CD evidence workflow without importing GitHub Actions as doctrine.
- `loom-performance`: Addy's measure -> identify -> fix -> verify -> guard loop and budgets become a performance evidence workflow.
- `loom-docs-sync`: Addy's docs discipline becomes README/API/changelog/comment synchronization that mirrors constitution decisions, wiki, specs, ticket/evidence truth, and ship output without owning ADRs or decisions.
- `loom-agent-orchestration`: Superpowers subagent-driven development, executing plans, and dispatching parallel agents become Loom-safe worker partitioning, Ralph/packet selection, review loops, and parent reconciliation.

Core-owner routes that should not become playbooks:

- Addy's spec-driven-development guidance routes to core `loom-specs`, using-Loom outer-loop doctrine, `loom-plans`, tickets, and evidence. A separate `loom-spec-driven` playbook would duplicate the spec owner and outer-loop gates.
- Addy's planning/task-breakdown and Superpowers writing/executing-plans guidance routes to core `loom-plans`, tickets, Ralph, and `loom-agent-orchestration` when worker partitioning is the actual extra workflow. A separate `loom-planning` playbook would duplicate `loom-plans`.
- Superpowers verification-before-completion guidance routes to using-Loom validation/honesty doctrine, core `loom-evidence`, core `loom-tickets`, and `loom-ship` packaging checks. A separate `loom-verification` playbook would duplicate mandatory evidence-before-claim behavior.
- Addy's ADR/decision guidance routes to core `loom-constitution` decision records; optional docs work is only documentation synchronization through `loom-docs-sync`.

Existing-playbook deepening remains appropriate where the peer skill is already
covered by a Loom playbook boundary:

- `loom-git`: Addy's git workflow/versioning and Superpowers worktree/branch finish mechanics deepen baseline, worktree, atomic-history, diff, PR, and cleanup guidance.
- `loom-debugging`: Addy's debugging/error recovery and Superpowers systematic debugging deepen reproduce/localize/reduce/root-cause/guard discipline.
- `loom-ship`: Addy's shipping/launch and Superpowers branch finishing deepen launch, rollback, handoff, and cleanup package guidance.
- `loom-skill-authoring`: Addy's using-agent-skills and Superpowers writing-skills become skill-routing, activation, pressure-scenario, and peer-runtime translation guidance.
- `loom-product-discovery`, `loom-ui-browser`, `loom-architecture`, `loom-security`, `loom-migration`, and `loom-simplification` continue to carry the first-pass peer candidates, now with dense references rather than shells.
- Triage remains deferred as a standalone Loom playbook until external issue intake becomes a repeated product surface; its useful pieces route into tickets, debugging, research, and external tracker adapters.

## Rejected Mechanics

- Peer docs or ideas directories as canonical truth: rejected. Loom records own product truth by layer.
- Issue tracker labels and comments as live state: rejected. External trackers may mirror or request work; tickets own live execution and acceptance.
- Mandatory hard user approval after every design/spec/plan phase: rejected as a default. Loom should ask when authority, risk, ambiguity, or user judgment requires it, and continue under recorded delegated authority when safe.
- DevTools MCP, visual companion servers, browser event files, hook scripts, GitHub Actions snippets, and worktree helper scripts as protocol requirements: rejected. They can be evidence or transport mechanisms when present.
- Hard-coded `.superpowers`, `docs/superpowers`, `docs/ideas`, or `.out-of-scope` storage: rejected. Translate the durable information into research, specs, plans, tickets, wiki, evidence, critique, or support artifacts.
- Router persona or deep orchestrator trees: rejected. Addy's orchestration reference shows these add paraphrasing cost and information loss (`references/orchestration-patterns.md:282-370`). Loom's equivalent is owner-layer routing plus Ralph/critique/wiki packets with parent reconciliation.
- Communication-mode skills such as caveman mode: rejected as product playbooks. They are user preference or memory-support concerns, not Loom workflow.

# Conclusions

The core/playbooks split makes a stronger integration path visible: bring in-house optional workflow playbooks when a recurring engineering discipline has its own activation triggers, evidence posture, and routing sequence, but still leaves durable truth in `loom-core` records.

The strongest new playbook candidates are now the owner-boundary-filtered
Addy/Superpowers adaptation set: `loom-architecture`,
`loom-product-discovery`, `loom-ui-browser`, `loom-security`, `loom-migration`,
`loom-simplification`, `loom-incremental-implementation`, `loom-tdd`,
`loom-source-grounding`, `loom-context-engineering`, `loom-code-review`,
`loom-ci-cd`, `loom-performance`, `loom-docs-sync`, and
`loom-agent-orchestration`.

The most important boundary is unchanged: these should be playbooks, not new owner
layers. Each should say this workflow coordinates and core records own truth. The
expected implementation pattern is a strong `SKILL.md` plus dense references where
needed, no templates unless the playbook creates a support artifact, no scripts, no
required MCPs, no copied peer storage paths, and no peer runtime state as Loom truth.

# Recommendations

Recommended implementation order:

1. Preserve the first six playbooks and keep their dense references.
2. Add the peer-skill equivalents listed above only when they are genuine
   workflow composition or specialist discipline. Route spec-first, planning,
   verification-before-completion, and ADR ownership into the core owner layers
   instead of creating duplicate playbooks.
3. Deepen existing playbooks with cross-links rather than forcing every discipline
   through `loom-drive`.
4. Validate membership and structure with package smoke checks, placeholder/path
   scans, evidence, and mandatory critique.

Before adding new playbooks, create tickets that constrain each one to:

- preserve `loom-core` dependency wording
- route durable facts into owner records
- avoid new canonical storage paths
- avoid required scripts/MCPs/harnesses
- include common rationalizations, red flags, and verification
- validate with structural scans and mandatory critique because playbook additions change operator behavior

# Open Questions

- Naming: `loom-ui-browser` may want a better name such as `loom-frontend`, `loom-ui`, or `loom-browser-evidence`. The boundary should include both UI quality and runtime browser evidence without requiring browser MCP.
- Split boundary: `loom-architecture` and `loom-simplification` overlap. If first implementation scope feels too wide, implement `loom-simplification` separately and keep `loom-architecture` focused on seams, interfaces, and architecture refactoring.
- Security depth: `loom-security` may need named critique profiles in core critique before it can be fully useful; otherwise it can start as a playbook that routes to existing high-risk critique policy.
- Product discovery overlap: `loom-product-discovery` must not become an alternative initiative/spec/plan ledger. Its durable output must be owner records, not a one-pager by default.

# Linked Work

- `research:peer-engineering-discipline-deep-dive`
- `research:external-peer-skill-practices-synthesis`
- `research:skill-template-benchmark-synthesis`
- `research:superpowers-skill-workflow-adaptation`
- `decision:0008`
- `plan:split-core-and-playbooks-packages`

# Completion Basis

Concluded initially at 2026-05-08T01:03:41Z after refreshing the three peer clones, direct-reading less-assimilated candidate areas, comparing them against current `loom-playbooks/skills`, and recording a ranked candidate matrix plus rejected mechanics.

Amended at 2026-05-08T01:46:00Z after operator review found the first implementation too skeletal. The amendment adds direct-read provenance for the broader Addy/Superpowers source set and revises the recommendation from six new playbooks to a near-complete peer-skill adaptation across new playbooks, existing-playbook deepenings, core owner routes, and rejected peer runtime surfaces.

Amended at 2026-05-08T02:21:22Z after owner-boundary audit found that some
near-complete peer-skill adaptations duplicated core owner layers. The amendment
removes `loom-spec-driven`, `loom-planning`, and `loom-verification` from the
recommended playbook set, routes their source material to core specs/plans /
validation/evidence/tickets, and narrows documentation work from `loom-docs-adrs`
to `loom-docs-sync` so decision authority stays with constitution records.

This research does not implement the playbooks; it constrains downstream implementation and critique.
