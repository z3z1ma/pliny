---
id: plan:split-core-and-playbooks-packages
kind: plan
status: active
created_at: 2026-05-07T21:31:17Z
updated_at: 2026-05-08T01:46:00Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  initiative:
    - initiative:loom-install-experience
  spec:
    - spec:core-and-playbooks-package-contract
  ticket:
    - ticket:hi5e7nbr
    - ticket:u9vtemj3
    - ticket:7h8u6oxp
    - ticket:xtt24452
    - ticket:sbzmrvqv
    - ticket:mbkqbkgq
    - ticket:plybk508
  research:
    - research:core-workflow-plugin-split-feasibility
    - research:gemini-extension-subdirectory-feasibility
    - research:loom-install-distribution-methods
    - research:codex-plugin-distribution-surfaces
    - research:peer-playbook-integration-candidates
  decision:
    - decision:0004
    - decision:0005
    - decision:0006
    - decision:0008
    - decision:0009
  critique:
    - critique:core-playbooks-package-contract-review
    - critique:core-playbooks-constitutional-decision-review
---

# Purpose

Split Loom into two installable package roots while preserving Loom's core
discipline and making optional playbooks clearly compositional.

The target product shape is:

```text
loom-core/
  skills/
  .claude-plugin/ .codex-plugin/ .cursor-plugin/ gemini-extension.json package metadata

loom-playbooks/
  skills/
  .claude-plugin/ .codex-plugin/ .cursor-plugin/ gemini-extension.json package metadata
```

`loom-core` gives users the Loom kernel: canonical owner layers, shared record
grammar, workspace orientation, using-Loom doctrine, support memory, Ralph packet
execution, and retrospective closure/promotion discipline.

`loom-playbooks` gives users optional higher-level workflow playbooks that compose
on top of the core graph. Users can install core alone and bring their own
workflows, or install both packages for the full Loom experience.

This needs more than one ticket because it changes product authority, source
layout, documentation, harness manifests, package names, plugin validation, and
cross-skill routing prose.

# Context And Orientation

Current state:

- `skills/` is the current product surface.
- `.claude-plugin/plugin.json`, `.codex-plugin/plugin.json`,
  `.cursor-plugin/plugin.json`, `gemini-extension.json`, and `open-loom.mjs`
  all assume the repository root exposes one canonical `skills/` directory.
- `decision:0004` requires flat, self-contained skills and rejects hidden
  inheritance.
- `decision:0008` supersedes `decision:0006` as the active product-surface policy:
  the product surface is now `loom-core/` and `loom-playbooks/`, while fallback
  installers and command wrappers remain rejected.
- `research:core-workflow-plugin-split-feasibility` concludes that two package
  roots are feasible for the supported harnesses, but each root must be
  self-contained after install/cache and core-only installs require doctrine
  decoupling.

Agreed scoping decisions for this plan:

- Use top-level `loom-core/` and `loom-playbooks/` directories.
- Each package root contains its own `skills/` and native harness plugin/extension
  files.
- Retire the current top-level `skills/` directory instead of preserving a
  duplicate full bundle.
- Keep repo-level marketplace/catalog files as discovery surfaces that list both
  package roots.
- OpenCode splits into two packages only: `@z3z1ma/open-loom-core` and
  `@z3z1ma/open-loom-playbooks`; migration/deprecation of the current `open-loom` package
  is a follow-up concern, and `spec:opencode-plugin-install-contract` is
  historical/superseded for future split work.
- `loom-playbooks` requires `loom-core`; it must not duplicate core skills.

Core skill membership:

- `using-loom`
- `loom-workspace`
- `loom-records`
- `loom-memory`
- `loom-ralph`
- `loom-retrospective`
- `loom-constitution`
- `loom-initiatives`
- `loom-research`
- `loom-specs`
- `loom-plans`
- `loom-tickets`
- `loom-evidence`
- `loom-critique`
- `loom-wiki`

Playbook skill membership:

- `loom-drive`
- `loom-git`
- `loom-debugging`
- `loom-spike`
- `loom-codemap`
- `loom-ship`
- `loom-skill-authoring`
- `loom-architecture`
- `loom-product-discovery`
- `loom-ui-browser`
- `loom-security`
- `loom-migration`
- `loom-simplification`
- `loom-incremental-implementation`
- `loom-tdd`
- `loom-source-grounding`
- `loom-context-engineering`
- `loom-code-review`
- `loom-ci-cd`
- `loom-performance`
- `loom-docs-sync`
- `loom-agent-orchestration`

# Strategy

Do the split as a governed product-surface migration, not as a broad move-only
patch.

The order is:

1. Authorize the product-surface change in the constitutional layer.
2. Tighten the core/playbook behavior contract so core can stand alone.
3. Refactor doctrine and cross-skill references before moving files.
4. Move skills into the two package roots and preserve self-contained skill
   operation.
5. Move or recreate harness manifests, hooks, extension metadata, and OpenCode
   packages inside the package roots.
6. Keep root-level catalogs that list `./loom-core` and `./loom-playbooks`.
7. Update public docs and package framing.
8. Validate structure and harness surfaces with evidence, then critique before
   acceptance.

The main rejected route is keeping top-level `skills/` as a full compatibility
bundle. That creates a third product surface and makes drift likely.

# Planning Decisions

- Decision: Treat Ralph as core.
  - Rationale: Compiling Loom graph artifacts into bounded packets for
    fresh-context execution is part of Loom's transaction kernel, not an optional
    playbook.
  - Date / owner: 2026-05-07 operator-scoped planning decision.
  - Owner-layer route if this stops being plan truth: constitution decision or
    using-Loom doctrine.

- Decision: Treat retrospective as core.
  - Rationale: Promotion and closure discipline are part of Loom's compounding
    mechanism, even though retrospective is expressed as a workflow coordinator.
  - Date / owner: 2026-05-07 operator-scoped planning decision.
  - Owner-layer route if this stops being plan truth: constitution decision,
    ticket acceptance doctrine, or using-Loom doctrine.

- Decision: Treat memory as core.
  - Rationale: Support recall is part of the core operating surface even though it
    does not own canonical project truth.
  - Date / owner: 2026-05-07 operator-scoped planning decision.
  - Owner-layer route if this stops being plan truth: using-Loom truth-boundary
    doctrine or memory skill guidance.

- Decision: `loom-playbooks` depends on `loom-core` and does not duplicate core.
  - Rationale: Duplication would create a second copy of doctrine, templates, and
    record grammar. Playbooks should compose over core.
  - Date / owner: 2026-05-07 operator-scoped planning decision.
  - Owner-layer route if this stops being plan truth: package architecture
    decision and install documentation.

- Decision: Retire root `skills/`.
  - Rationale: Keeping root `skills/` as a full bundle would create a third
    product surface and make the core/playbooks split less truthful.
  - Date / owner: 2026-05-07 operator-scoped planning decision.
  - Owner-layer route if this stops being plan truth: constitution decision and
    package migration plan.

# Workstreams

- Product authority and contract: constitutional decision, behavior contract, and
  package-boundary wording.
- Core package: core skills, using-Loom doctrine, Ralph, retrospective, memory,
  and core harness metadata.
- Playbooks package: optional playbook skills and dependency notices on core.
- Harness catalogs and package metadata: repo-level catalogs plus per-package
  Claude, Codex, Cursor, Gemini, and OpenCode surfaces.
- Documentation and migration: README, INSTALL, ARCHITECTURE, PROTOCOL, AGENTS,
  package docs, and `open-loom` migration/deprecation notes.
- Validation and review: structural checks, harness smoke checks, evidence, and
  critique.

# Execution Units / Ticket Slices

## Unit: Authorize The Split

- Source claim / input: `decision:0006` says the product surface is `skills/`, and
  `research:core-workflow-plugin-split-feasibility` says the split reopens that
  truth.
- Observable outcome: `decision:0008` authorizes `loom-core/` and
  `loom-playbooks/` as the product package roots and states how they relate to
  the prior skills-only/product-surface doctrine.
- Likely ticket: satisfied directly by `decision:0008`; no separate ticket needed
  for the constitutional record creation.
- Likely write scope: `.loom/constitution/decisions/`,
  `.loom/constitution/constitution.md`, this plan, and linked research if needed.
- Dependencies / order reason: must precede package moves so implementation does
  not outrun product authority.
- Verification / evidence target: structural record checks, grep for product-surface
  wording conflicts in constitution/public docs, and diff review.
- Critique posture: mandatory because this changes product authority.
- Non-goals: moving source files or changing harness manifests in this unit.
- Stop or loopback condition: if the decision cannot reconcile with
  `decision:0004` or `decision:0006`, loop back into constitution before any file
  migration.

## Unit: Define Core And Playbook Contract

- Source claim / input: agreed membership and dependency decisions from this plan.
- Observable outcome: reusable behavior contract that explains core-only Loom,
  full Loom, and playbook dependency semantics without requiring transcript
  context.
- Likely ticket: satisfied directly by `spec:core-and-playbooks-package-contract`;
  implementation tickets should cite the spec's acceptance IDs.
- Likely write scope: a new or updated spec under `.loom/specs/`, this plan,
  and possibly `PROTOCOL.md` if the plan chooses to introduce public wording early.
- Dependencies / order reason: follows authorization and precedes doctrine edits.
- Verification / evidence target: membership table spot-check against actual skill
  directories; grep for unresolved `workflow` naming where `playbook` is intended.
- Critique posture: recommended because terminology drift here would affect every
  downstream package ticket.
- Non-goals: implementation of the directory move.
- Stop or loopback condition: if the contract reopens Ralph, retrospective, or
  memory membership, update the plan before creating migration tickets.

## Unit: Decouple Core Doctrine From Optional Playbooks

- Source claim / input: core-only install must work without `loom-playbooks`.
- Observable outcome: core skill prose routes optional playbook references as
  optional installed playbooks or user-provided equivalents, while retaining core
  Ralph, retrospective, memory, record, workspace, and canonical-layer behavior.
- Likely ticket: ticket:hi5e7nbr
- Likely write scope: core skill files currently under `skills/using-loom`,
  `skills/loom-workspace`, `skills/loom-records`, `skills/loom-plans`,
  `skills/loom-tickets`, and `skills/loom-research`; after migration, equivalent
  paths under `loom-core/skills`.
- Dependencies / order reason: should happen before or during the move so the
  moved core package is coherent when tested alone.
- Verification / evidence target: grep for direct optional playbook assumptions in
  core files; structural review that all core paths still point at installed skill
  paths rather than retired root `skills/` assumptions.
- Critique posture: mandatory because this changes operator routing and completion
  behavior.
- Non-goals: reducing Ralph, retrospective, critique, wiki, or memory from core.
- Stop or loopback condition: if a core skill cannot be made coherent without a
  playbook skill, revisit membership before moving package manifests.

## Unit: Move Core Package Root

- Source claim / input: authorized core package boundary and core skill membership.
- Observable outcome: `loom-core/skills/` contains the core skills and no root
  `skills/` dependency is needed for core operation.
- Likely ticket: ticket:u9vtemj3 covers this with the playbooks move as one
  source-layout migration slice.
- Likely write scope: move core skill directories into `loom-core/skills/`; update
  in-repo references that point to moved core paths; preserve history with normal
  Git moves where possible.
- Dependencies / order reason: follows doctrine decoupling enough that core can be
  validated alone.
- Verification / evidence target: skill frontmatter scan, directory membership
  check, stale path grep for core skill locations, and `git diff --check`.
- Critique posture: recommended because large path moves create reference drift.
- Non-goals: moving playbook skills or changing harness catalogs in the same
  ticket unless the ticket explicitly combines a narrow adapter smoke.
- Stop or loopback condition: if root `skills/` references are too entangled to
  update safely in one slice, split into smaller doctrine/reference tickets.

## Unit: Move Playbooks Package Root

- Source claim / input: playbook skill membership and dependency-on-core decision.
- Observable outcome: `loom-playbooks/skills/` contains playbook skills only, and
  playbook activation text clearly requires `loom-core`.
- Likely ticket: ticket:u9vtemj3 covers this with the core move as one
  source-layout migration slice.
- Likely write scope: move playbook skill directories into
  `loom-playbooks/skills/`; add dependency notices in playbook skill guidance;
  update references to core skills as installed-package dependencies rather than
  parent-directory assumptions.
- Dependencies / order reason: can proceed after core boundary is stable; should
  not duplicate core skills.
- Verification / evidence target: membership grep, no copied core skill dirs under
  `loom-playbooks/skills`, stale path checks, and `git diff --check`.
- Critique posture: recommended because dependency wording affects install safety.
- Non-goals: playbook behavior redesign beyond dependency and path alignment.
- Stop or loopback condition: if a playbook cannot operate without hidden core
  copies, revise its guidance or route back to the contract unit.

## Unit: Rebuild Harness Package Surfaces

- Source claim / input: each package root must be self-contained after install or
  cache, and repo-level catalogs list both roots.
- Observable outcome: per-package plugin/extension metadata exists inside
  `loom-core/` and `loom-playbooks/`, and root-level marketplace/catalog files
  point at both package roots.
- Likely ticket: ticket:7h8u6oxp for the non-OpenCode initial skeleton, with
  harness-specific follow-ups as needed.
- Likely write scope: `loom-core/.claude-plugin/`,
  `loom-playbooks/.claude-plugin/`, `loom-core/.codex-plugin/`,
  `loom-playbooks/.codex-plugin/`, `loom-core/.cursor-plugin/`,
  `loom-playbooks/.cursor-plugin/`, `loom-core/gemini-extension.json`,
  `loom-playbooks/gemini-extension.json`, root catalog files, and related hook or
  context files.
- Dependencies / order reason: follows package-root migration so manifests can
  point at real local paths.
- Verification / evidence target: JSON syntax checks, manifest path checks,
  marketplace source path checks, and harness-specific validation where available.
- Critique posture: mandatory for the first harness skeleton because package
  surfaces control install behavior.
- Non-goals: publishing marketplace packages.
- Stop or loopback condition: if any harness cannot consume the two-root layout,
  split that harness into a separate research or spike ticket before broad docs
  claim support.

## Unit: Split OpenCode Packages

- Source claim / input: OpenCode target is two packages only:
  `@z3z1ma/open-loom-core` and `@z3z1ma/open-loom-playbooks`.
- Observable outcome: each package root has its own OpenCode plugin module and
  package metadata; core registers using-Loom references and core skills, while
  playbooks registers playbook skills and does not preload core doctrine. The
  repository root package becomes private/non-published repo metadata, not a third
  publishable Loom package.
- Likely ticket: ticket:xtt24452.
- Likely write scope: `loom-core/package.json`, `loom-core/open-loom-core.mjs`,
  `loom-playbooks/package.json`, `loom-playbooks/open-loom-playbooks.mjs`, root
  `package.json`, root `open-loom.mjs`, and install docs.
- Dependencies / order reason: follows package-root migration and harness skeleton.
- Verification / evidence target: per-package smoke command, package dry-run for
  each package, local file/path OpenCode config check, and stale `open-loom`
  package claim check.
- Critique posture: mandatory because this affects existing published package
  expectations.
- Non-goals: publishing until package dry-runs and docs are accepted.
- Stop or loopback condition: if OpenCode cannot load two local packages cleanly,
  route to focused OpenCode research before publication work.

## Unit: Validate Codex Core Hooks

- Source claim / input: Codex hooks docs now describe `SessionStart` context and
  plugin-bundled lifecycle config, but runtime installed-plugin behavior needs
  validation.
- Observable outcome: a Codex validation record shows whether installed
  `loom-core` exposes `using-loom` and loads bundled hook/context preload from the
  plugin cache.
- Likely ticket: proposed, possibly paired with Codex package surface work.
- Likely write scope: Codex package fixtures under `loom-core/` and
  `loom-playbooks/`, Codex-specific evidence records, and docs only after proof.
- Dependencies / order reason: follows enough package skeleton to install or link.
- Verification / evidence target: Codex CLI/version note, marketplace/local install
  or link attempt, skill discovery observation, `SessionStart` context observation,
  and trust-boundary note.
- Critique posture: recommended before release claims.
- Non-goals: treating project-local `.codex/` hooks as equivalent to plugin-bundled
  hooks unless the evidence proves the installed plugin path.
- Stop or loopback condition: if plugin-bundled hooks do not load, keep Codex core
  skill packaging but document preload as unsupported or separate.

## Unit: Resolve Gemini Extension Distribution Route

- Source claim / input: `research:gemini-extension-subdirectory-feasibility`
  concludes the current docs and local CLI do not support seamless Git install of
  extension roots from repository subdirectories.
- Observable outcome: a Gemini validation/research record selects a truthful
  distribution route for `loom-core` and `loom-playbooks`: explicit local
  package-root linking for developers, repository-root core-only Gemini shim,
  separate release repositories, distribution branches, validated release archives,
  or deferred upstream subdirectory support.
- Likely ticket: `ticket:sbzmrvqv` for route disposition and `ticket:mbkqbkgq` for
  the accepted root core shim.
- Likely write scope: Gemini metadata under `loom-core/` and `loom-playbooks/`,
  root Gemini core-shim metadata, packaging/release metadata if a route is chosen,
  evidence records, and Gemini install docs only after proof.
- Dependencies / order reason: follows package skeleton.
- Verification / evidence target: real `gemini extensions install <source>` or
  `gemini extensions link <path>` output for the chosen route, `gemini extensions
  list` skill/context observation, and context preload observation for `loom-core`.
- Critique posture: recommended because Gemini is the weakest harness evidence.
- Non-goals: claiming Git one-repo subdirectory or two-extension support from this
  repository without upstream support or accepted release packaging; making root
  Gemini install include playbooks.
- Stop or loopback condition: if the root Gemini core shim cannot expose core
  without copied doctrine or confusing playbook claims, route back to
  product-surface planning before public docs claim support.

## Unit: Update Public Documentation And Examples

- Source claim / input: root `skills/` is retired and package roots are now the
  product surface.
- Observable outcome: README, INSTALL, ARCHITECTURE, PROTOCOL, AGENTS, and relevant
  examples describe core/playbooks accurately without claiming unvalidated harness
  behavior.
- Likely ticket: proposed.
- Likely write scope: public docs, AGENTS guidance, examples that name root
  `skills/`, and possibly existing `.loom` owner records when project truth needs
  reconciliation.
- Dependencies / order reason: follows the actual package shape or at least an
  accepted contract and skeleton.
- Verification / evidence target: stale path grep, docs link checks by search,
  structural diff review, and examples consistency spot-check.
- Critique posture: mandatory because documentation defines operator behavior.
- Non-goals: rewriting marketing copy beyond what the split requires.
- Stop or loopback condition: if docs need to describe an unproven harness path,
  leave that path as experimental or route back to harness validation.

## Unit: Final Structural Validation And Critique

- Source claim / input: split implementation tickets have landed.
- Observable outcome: evidence and critique records support that core-only install,
  full install, and playbook dependency behavior are accurately represented.
- Likely ticket: proposed acceptance/review ticket or closure tranche.
- Likely write scope: evidence records, critique records, ticket dispositions,
  and any final small fixes discovered by review.
- Dependencies / order reason: last tranche before acceptance.
- Verification / evidence target: package tree scan, skill membership scan, stale
  root `skills/` path scan, per-harness manifest validation where available,
  OpenCode smoke, Codex hook validation if available, Gemini validation if
  available, and docs consistency grep.
- Critique posture: mandatory.
- Non-goals: adding new playbook functionality.
- Stop or loopback condition: any unresolved high/medium critique finding loops
  back to the owning ticket before closure.

# Milestones

## Milestone: Authorized Split

Scope: product-surface authority and core/playbook contract.

Expected result: `decision:0008` authorizes the two package roots, and downstream
contract records define membership/dependencies.

Units / tickets: Authorize The Split satisfied by `decision:0008`; Define Core
And Playbook Contract remains proposed.

Validation and evidence: structural record checks, conflict grep, and mandatory
critique for product authority.

Acceptance checkpoint: no file migration starts until this milestone is accepted.

## Milestone: Coherent Package Roots

Scope: source layout and skill-level decoupling.

Expected result: `loom-core/skills` and `loom-playbooks/skills` exist with the
agreed membership and no root `skills/` product dependency.

Units / tickets: Decouple Core Doctrine From Optional Playbooks; Move Core
Package Root; Move Playbooks Package Root.

Validation and evidence: membership scans, stale path greps, frontmatter scans,
and critique of operator-routing changes.

Acceptance checkpoint: core-only skill package can be inspected without playbook
skills present.

## Milestone: Native Harness Split

Scope: package metadata, catalogs, hooks, and harness-specific validation.

Expected result: each supported harness has either a validated two-package path or
an explicit documented evidence gap.

Units / tickets: Rebuild Harness Package Surfaces; Split OpenCode Packages;
Validate Codex Core Hooks; Resolve Gemini Extension Distribution Route.

Validation and evidence: manifest checks, package smoke checks, runtime harness
checks where available, and evidence records for any unvalidated path.

Acceptance checkpoint: install docs only claim the behavior supported by evidence.

## Milestone: Publicly Coherent Release Candidate

Scope: public docs, examples, records reconciliation, final critique.

Expected result: repository presentation consistently describes Loom as core plus
playbooks, and validation/critique supports the release posture.

Units / tickets: Update Public Documentation And Examples; Final Structural
Validation And Critique.

Validation and evidence: stale reference checks, docs consistency checks, harness
validation evidence, and mandatory critique.

Acceptance checkpoint: plan can move toward completion when linked tickets own
acceptance decisions and residual risks.

# Sequencing

Authority comes first because implementation would otherwise contradict active
decisions. Contract and doctrine decoupling come before or alongside file moves so
`loom-core` is coherent as a standalone package. Harness metadata follows the
physical package roots so manifests can point at real files. Documentation waits
until package shape and validation posture are truthful enough to describe.

OpenCode, Codex, Gemini, Claude, and Cursor package work can split into separate
tickets after the common package skeleton exists. Codex and Gemini should remain
evidence-first because the current research names specific runtime gaps.

# Claim / Acceptance Coverage

| Source claim / acceptance ID | Downstream ticket | Coverage expectation | Evidence / critique expectation | Notes |
| --- | --- | --- | --- | --- |
| `initiative:loom-install-experience` success metric: native package installs expose Loom skills without hidden ontology | proposed split package tickets | Core and playbooks install through native harness package surfaces | Manifest checks, harness smoke checks, evidence records | Existing initiative remains the strategic frame |
| `decision:0008` and `decision:0009` product-surface doctrine | downstream package tickets | Implementation follows the authorized `loom-core` / `loom-playbooks` surface plus the Gemini-only root core shim exception | Constitutional critique and package evidence | `decision:0009` narrows `decision:0008` only for Gemini |
| `research:core-workflow-plugin-split-feasibility` conclusion: two roots feasible but harness-specific | proposed harness tickets | Each harness implements or explicitly defers its two-root path | Per-harness evidence and critique | Gemini and Codex require focused validation |
| Core-only install requirement | proposed doctrine/package tickets | Core package works without playbook skills installed | Core-only membership and stale optional route scans | Playbooks can be optional only if core is coherent |
| Playbooks require core | proposed playbook package ticket | Playbook package does not duplicate core and states dependency clearly | Duplicate-core scan and dependency wording review | Harness dependency enforcement may be documentation-only |

# Validation And Acceptance Strategy

Expected validation by tranche:

- record structure checks for constitutional decision, spec/contract, and plan
  updates
- `git diff --check` after each implementation tranche
- skill membership scan for `loom-core/skills` and `loom-playbooks/skills`
- skill frontmatter scan for all moved skills
- stale path searches for root `skills/`, old manifest paths, `open-loom`, and
  legacy workflow-package names, treating the Gemini root core shim as an explicit
  exception rather than current full-product truth
- JSON syntax checks for plugin and marketplace manifests
- OpenCode per-package smoke checks for `@z3z1ma/open-loom-core` and
  `@z3z1ma/open-loom-playbooks`
- Codex installed-plugin skill and hook validation before claiming core preload
- Gemini distribution-route validation before claiming remote extension install;
  current research rejects one-repo subdirectory install as unsupported, while
  `decision:0009` allows repository-root install as core-only
- mandatory critique for product authority, doctrine decoupling, harness package
  surfaces, and final release posture

Tickets own live evidence sufficiency and final acceptance. This plan names the
proof shape only.

# Interfaces And Dependencies

- Claude Code plugin roots and `.claude-plugin/marketplace.json` path rules.
- Codex plugin roots, `.agents/plugins/marketplace.json`, and hooks behavior from
  `https://developers.openai.com/codex/hooks`.
- OpenCode npm/file plugin loading and `config.instructions` /
  `config.skills.paths` mutation.
- Gemini CLI extension roots and `gemini-extension.json` context loading.
- Cursor plugin roots and marketplace metadata.
- Agent Skills directory requirements for `SKILL.md` frontmatter and supporting
  `references/` / `templates/` directories.
- Existing published `open-loom` package, which needs migration/deprecation
  handling outside the conceptual split.
- Git history preservation for skill directory moves.

# Idempotence And Recovery

Do not perform the whole migration in one ticket. Each tranche should leave the
graph and repository in a recoverable state:

- authorization has landed in `decision:0008` without file moves
- contract/doctrine edits can land before path moves
- core and playbook moves can be reviewed independently
- harness package skeleton can land before runtime validation for every harness
- unvalidated harness behavior must be recorded as a gap rather than smoothed over
  in docs

Live state belongs in downstream tickets. If a fresh agent resumes mid-plan, it
should inspect linked tickets first, then this plan, then the research note.

# Execution Waves

| Wave | Tickets | Independent because | Write-scope / shared-state check | Parent reconciliation |
| --- | --- | --- | --- | --- |
| Wave 1 | Authorization and core/playbook contract | Both are owner-record shaping, but authorization must be accepted before contract becomes final | Overlap on `.loom` records; run sequentially unless ticket scopes are separated carefully | Reconcile this plan and any new decision/spec links |
| Wave 2 | Doctrine decoupling, core move, playbook move | Can split after contract is stable, but references overlap heavily | Avoid parallel edits to `using-loom`, `loom-records`, routing docs, and moved path references | Parent runs stale path and membership scans after both moves |
| Wave 3 | Harness package surfaces by harness | Harness directories can be independent after package roots exist | Separate Claude/Codex/Cursor/OpenCode package files; Gemini requires a route decision before remote install claims; shared root catalogs require sequential reconciliation | Parent reconciles root catalogs and INSTALL docs |
| Wave 4 | Docs, final validation, critique | Final docs depend on validation evidence | Docs and final critique should run after package evidence | Parent updates tickets with evidence and finding dispositions |

# Risks And Loopbacks

- If constitutional decisions reject or constrain the split, loop back to
  constitution before implementation.
- If core-only doctrine still assumes playbook skills, loop back to the contract
  and doctrine unit before moving manifests.
- If a moved skill depends on relative `skills/...` paths that no longer exist,
  split the reference reconciliation into smaller tickets.
- If Codex installed-plugin hooks do not load as documented, keep skill packaging
  but remove or downgrade preload claims.
- If Gemini cannot install two extension roots from one repo, do not keep trying to
  validate the subdirectory path. Use `research:gemini-extension-subdirectory-feasibility`
  and choose a separate release/distribution route, local explicit link docs, or
  an explicit deferral.
- If OpenCode package split collides with the published `open-loom` name, route to
  migration/deprecation work rather than changing the split concept.
- If root `skills/` retirement breaks too much at once, stage the physical move and
  docs update, but do not preserve root `skills/` as a parallel product surface.

# Supporting Artifacts And Notes

- `research:core-workflow-plugin-split-feasibility` owns the current harness split
  feasibility synthesis.
- `research:loom-install-distribution-methods` owns the broader native package
  strategy.
- `research:codex-plugin-distribution-surfaces` owns the existing Codex plugin
  evidence and earlier gap analysis.
- `research:gemini-extension-subdirectory-feasibility` owns the current Gemini
  subdirectory-extension null result, local-link evidence, and hooks/preload
  assessment.
- `decision:0004`, `decision:0006`, and `decision:0008` constrain
  self-contained skills, rejected fallback installers, and current product surface
  truth.

# Plan Readiness Review

- Claim coverage: mapped to the install initiative, active decisions, and split
  research.
- Execution units / ticket-sized slices: defined as authority, contract, doctrine,
  core move, playbook move, harness surfaces, OpenCode packages, Codex validation,
  Gemini validation, docs, and final critique.
- Context and orientation: current root `skills/` assumptions and harness surfaces
  are named.
- Narrative milestones: four milestones cover authorization, package roots, native
  harness split, and release candidate coherence.
- Likely write scopes: named per unit.
- Validation and acceptance strategy: structural, path, manifest, package, harness,
  evidence, and critique checks are named.
- Interfaces and dependencies: supported harness surfaces and Agent Skills rules
  are named.
- Idempotence and recovery: sequential tranches preserve recovery and leave live
  truth to tickets.
- Parallel / wave independence: only harness-specific work appears parallelizable,
  and shared root catalogs require parent reconciliation.
- Stop / loopback conditions: constitutional, doctrine, harness, package, and docs
  loopbacks are named.

# Exit Criteria

This plan can complete when:

- the constitutional layer authorizes the core/playbooks product surface through
  `decision:0008`
- `loom-core/skills` and `loom-playbooks/skills` exist with agreed membership
- root `skills/` is retired as a product surface
- repo-level catalogs list both package roots where the harness supports catalogs
- OpenCode has two package surfaces or an explicit deferred migration record
- Codex hook preload claims are either evidenced or explicitly not claimed
- Gemini two-extension behavior is evidenced or explicitly scoped to a separate
  packaging route
- public docs and examples no longer describe top-level `skills/` as the product
  surface
- mandatory critique has reviewed product authority, routing doctrine, package
  surfaces, and final release posture
- downstream tickets own live acceptance and residual risks truthfully

# Completion Basis

When `status: completed`, record the linked implementation tickets, evidence,
critique verdicts, accepted residual risks, and any harness paths deliberately
deferred from the split release.
