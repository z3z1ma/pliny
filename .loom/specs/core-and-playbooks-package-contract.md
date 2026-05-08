---
id: spec:core-and-playbooks-package-contract
kind: spec
status: active
created_at: 2026-05-07T21:41:42Z
updated_at: 2026-05-08T01:46:00Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  initiative:
    - initiative:loom-install-experience
  plan:
    - plan:split-core-and-playbooks-packages
  research:
    - research:core-workflow-plugin-split-feasibility
    - research:gemini-extension-subdirectory-feasibility
    - research:loom-install-distribution-methods
    - research:peer-playbook-integration-candidates
  decision:
    - decision:0008
    - decision:0006
    - decision:0009
  spec:
    - spec:opencode-plugin-install-contract
  ticket:
    - ticket:hi5e7nbr
    - ticket:u9vtemj3
    - ticket:7h8u6oxp
    - ticket:xtt24452
    - ticket:sbzmrvqv
    - ticket:mbkqbkgq
    - ticket:plybk508
  critique:
    - critique:core-playbooks-package-contract-review
external_refs:
  codex_hooks:
    - https://developers.openai.com/codex/hooks
---

# Summary

This spec defines the intended behavior for splitting Loom's distributable package
surface into `loom-core/` and `loom-playbooks/`.

Downstream tickets should use this contract when moving skill directories,
rewriting references, updating harness manifests, publishing OpenCode packages,
validating Codex/Gemini behavior, or updating public documentation.

# Rigor Level

Full.

Rationale: this contract affects public package layout, native harness install
behavior, deprecation of the existing root `skills/` product surface, and several
downstream implementation tickets. Ambiguity here would create broken installs or
duplicate semantic owners.

# Problem

The current single root `skills/` tree makes Loom installable but conflates two
different products:

- Loom's core kernel: canonical layers, record grammar, using-Loom doctrine,
  Ralph packet execution, retrospective closure, workspace orientation, and
  support memory
- optional Loom playbooks: higher-level workflows that compose over core Loom

Users need a core-only install that can work with external workflows or local team
skills. Maintainers need a package boundary that makes core policy changes harder
to confuse with optional playbook additions.

# Problem Pressure Check

| Lens | Current answer | Disposition |
| --- | --- | --- |
| Evidence / baseline | `decision:0008` authorizes the split, and `research:core-workflow-plugin-split-feasibility` shows supported harnesses can plausibly expose two package roots. | accepted |
| Specific beneficiary or surface | Loom users who want only canonical layer discipline; maintainers deciding whether a skill is kernel or playbook; harness install docs and plugin manifests. | accepted |
| Current workaround / counterfactual | Keep one root `skills/` tree and ask users to ignore optional workflows. This makes core-only adoption unclear and keeps playbooks visually indistinguishable from canon. | rejected by `decision:0008` |
| Smallest valuable shape / solution attachment | Two top-level package roots, each with a `skills/` directory and native package metadata. Root catalogs may list both. | accepted |
| Durability risk | Harness plugin systems may change; Codex installed-plugin hooks and Gemini two-extension behavior still need runtime validation before release claims. | accepted with evidence gates |

# Desired Behavior

The repository should expose Loom as two package roots:

- `loom-core/` installs the Loom kernel and is sufficient for core Loom operation.
- `loom-playbooks/` installs optional playbooks and requires `loom-core`.

The split should be visible in source layout, skill membership, harness metadata,
package names, docs, and validation evidence. No generated adapter, root catalog,
legacy package, or retained compatibility directory should become a semantic owner
of Loom behavior.

# Quality Bar

A future user or agent should be able to answer these questions without transcript
context:

- which package do I install for core Loom only
- which package do I install for Loom's optional playbooks
- which skills are kernel and which are playbooks
- what happens if playbooks are installed without core
- which harness claims are validated versus still experimental
- where using-Loom references live after the split

The result is not acceptable if it only moves files while leaving docs, manifests,
or skill prose implying that top-level `skills/` remains the product surface.

# Options Considered

- Two top-level package roots: chosen because it matches `decision:0008`, makes the
  product boundary visible, and lets native harness package files live next to the
  relevant `skills/` root.
- Bare `skills-core/` and `skills-workflows/`: rejected because supported harnesses
  need package roots with metadata, not only skill directories.
- Retain root `skills/` as a full compatibility bundle: rejected because it creates
  a third product surface and drift risk.
- Add a Gemini-only root core shim: accepted by `decision:0009` because Gemini
  root manifest indexing is useful and can be scoped to core-only behavior.
- Duplicate core inside playbooks: rejected because it creates competing copies of
  the kernel.

# Not Doing

- Do not add a monolithic `loom` CLI, daemon, MCP, dashboard, hidden router, or
  required installer runtime.
- Do not preserve root `skills/` as a full compatibility product surface; a
  Gemini-only core shim may expose core skills from `loom-core` when documented as
  core-only transport.
- Do not make `loom-playbooks` standalone by copying core skills.
- Do not claim Gemini or Codex preload behavior without runtime evidence.
- Do not redefine canonical layers, ticket ledger authority, packet semantics, or
  critique/evidence ownership in package metadata.
- Do not treat root marketplace/catalog files as semantic owners.

# Boundary Tiers

- Always: preserve `loom-core` as the owner of using-Loom doctrine, canonical
  layer skills, record/workspace operation, memory support, Ralph, and
  retrospective.
- Always: make `loom-playbooks` depend on `loom-core` without duplicating core
  skills or doctrine.
- Always: validate harness-specific claims before public docs present them as
  supported behavior.
- Accepted exception: `decision:0009` allows a Gemini-specific repository-root
  core shim for `gemini-extension.json` indexing and core-only install.
- Ask first: adding any other third package, changing core/playbook membership,
  retaining a root full bundle, or repurposing `open-loom` as a compatibility
  meta-package.
- Never: let generated adapter files, marketplace catalogs, package metadata,
  examples, or external systems become Loom's ontology or ticket ledger.

# Interface / API Contract

- Inputs: a repository checkout or release package containing `loom-core/` and
  optionally `loom-playbooks/`; harness configuration that can install or point at
  one or both package roots.
- Outputs: harness-discoverable skills and optional preload/context behavior that
  point to the package-root source files.
- Error semantics: if `loom-playbooks` is installed or invoked without `loom-core`,
  playbook guidance must fail closed by naming the core dependency instead of
  pretending the playbook package can define Loom truth by itself.
- Validation boundary: package metadata can expose or point at skills and preload
  references; it cannot redefine Loom semantics.
- Compatibility / deprecation: root `skills/` is retired as product surface except
  for the Gemini-only core shim authorized by `decision:0009`;
  existing `open-loom` behavior is historical single-package behavior under
  superseded `spec:opencode-plugin-install-contract`; migration, deprecation, or
  replacement handling belongs in downstream OpenCode work before release claims
  change.

# Examples / Non-Examples

Positive examples:

- A core-only user installs `loom-core` and sees `using-loom`, canonical owner-layer
  skills, `loom-records`, `loom-workspace`, `loom-memory`, `loom-ralph`, and
  `loom-retrospective`, with no `loom-debugging` or `loom-drive` skills present.
- A Gemini user installs the repository root and gets core only, with docs clearly
  pointing full users to clone and link both package roots.
- A full user installs both packages. Playbook skills route durable truth back into
  core owner layers and cite core as a prerequisite.
- A Claude/Codex/Cursor repo-level marketplace lists both package roots but does
  not own semantic behavior itself.
- OpenCode install docs name `@z3z1ma/open-loom-core` and
  `@z3z1ma/open-loom-playbooks`, not a single full `open-loom` package, after the
  split is implemented.

Non-examples:

- `loom-playbooks/skills/using-loom/` as a copied core skill.
- Root `skills/` retained as the recommended full install.
- Root Gemini install described as including playbooks.
- A generated `AGENTS.md`, plugin hook, or marketplace description that becomes
  the only place a core requirement exists.
- Docs that say Codex or Gemini preload works before runtime evidence exists.

# Constraints

- `decision:0008` owns the package-root policy.
- `decision:0009` owns the Gemini-specific root core shim exception.
- `decision:0006` remains relevant only for the preserved rejection of fallback
  Makefile, shell installer, and top-level command-wrapper product surfaces.
- Skills must remain self-contained inside their package root and use skill-local
  references/templates rather than hidden parent inheritance.
- Native harness adapters and plugin metadata are derivative transport surfaces.
- `loom-playbooks` must not redefine canonical layers, acceptance, evidence,
  critique, ticket state, or packet lifecycle.
- Package-root implementation must avoid paths that break after harnesses copy or
  cache plugin roots.

# Requirements

- REQ-001: The repository MUST expose `loom-core/` and `loom-playbooks/` as the
  two intended top-level package roots.
- REQ-002: Each package root MUST contain its own `skills/` directory and any
  native plugin, extension, hook, package, or metadata files needed to expose that
  package.
- REQ-003: `loom-core/skills` MUST contain `using-loom`, `loom-workspace`,
  `loom-records`, `loom-memory`, `loom-ralph`, `loom-retrospective`, and the
  canonical owner-layer skills for constitution, initiatives, research, specs,
  plans, tickets, evidence, critique, and wiki.
- REQ-004: `loom-playbooks/skills` MUST contain only optional playbook skills:
  `loom-drive`, `loom-git`, `loom-debugging`, `loom-spike`, `loom-codemap`,
  `loom-ship`, `loom-skill-authoring`, `loom-architecture`,
  `loom-product-discovery`, `loom-ui-browser`, `loom-security`,
  `loom-migration`, `loom-simplification`, `loom-incremental-implementation`,
  `loom-tdd`, `loom-source-grounding`, `loom-context-engineering`,
  `loom-code-review`, `loom-ci-cd`, `loom-performance`, `loom-docs-sync`, and
  `loom-agent-orchestration`, unless a later constitutional or spec amendment
  changes membership. Optional playbooks MUST provide genuine workflow
  composition or specialist discipline on top of core owner layers; playbooks
  that merely duplicate core owner-layer skills or mandatory using-Loom doctrine
  are not allowed.
- REQ-005: `loom-playbooks` MUST require `loom-core` and MUST NOT duplicate core
  doctrine, canonical owner-layer skills, record grammar, `using-loom`, Ralph, or
  retrospective.
- REQ-006: Root `skills/` MUST be retired as a product surface and MUST NOT be kept
  as a recommended full compatibility bundle. A Gemini-only root core shim MAY
  expose `loom-core/skills` for Gemini discovery when it is documented as core-only
  transport.
- REQ-007: Core package prose MUST remain coherent when playbooks are absent; any
  optional playbook route named by core must be framed as optional or replaceable
  by a user-provided workflow.
- REQ-008: Playbook skill prose MUST fail closed when core is absent by naming the
  `loom-core` dependency and routing durable truth back to core owner layers.
- REQ-009: Repo-level marketplace or catalog files MAY list both package roots when
  the harness supports catalogs, but they MUST remain discovery/transport surfaces
  rather than semantic owners.
- REQ-010: OpenCode split work MUST target `@z3z1ma/open-loom-core` and
  `@z3z1ma/open-loom-playbooks`; it MUST NOT present the existing `open-loom`
  package as the new full-package answer without an explicit follow-up decision.
- REQ-011: Codex package docs MUST NOT claim installed-plugin hook preload until a
  current runtime validation proves bundled core hooks load as expected.
- REQ-012: Gemini package docs MUST NOT claim a one-repository subdirectory or
  two-extension install path from this repository. Gemini docs may claim only
  behavior backed by current evidence: explicit local package-root link/install,
  repository-root core-only install through the Gemini shim, an accepted separate
  release/distribution route, or an explicitly deferred upstream-support gap.
- REQ-013: Public docs, AGENTS guidance, architecture notes, examples, and harness
  manifests MUST reference package-root paths after migration and MUST NOT treat
  retired root `skills/` as current product truth.
- REQ-014: Implementation tickets MUST preserve or reconcile references when moving
  paths so future agents can search IDs and package paths without stale ambiguity.
- REQ-015: After OpenCode split work, the repository root package MUST be
  non-published workspace/repo metadata, while publishable OpenCode package
  surfaces live only under `loom-core` and `loom-playbooks`.
- REQ-016: The repository-root Gemini extension, if present, MUST install core only,
  MUST preload using-Loom context from `loom-core`, MUST expose no playbook skills,
  and MUST be documented as a Gemini-specific shim rather than the preferred full
  install path.

# Scenarios

## SCN-001: Core-only install

Exercises: REQ-001, REQ-002, REQ-003, REQ-006, REQ-007, ACC-001, ACC-002

GIVEN a harness or repository is configured with only `loom-core`
WHEN skill discovery runs or an agent inspects the package
THEN `using-loom` and all core skills are available from `loom-core/skills`
AND optional playbook skills are absent
AND core guidance does not require playbook installation to operate Loom.

## SCN-002: Full install through both packages

Exercises: REQ-001, REQ-002, REQ-003, REQ-004, REQ-005, ACC-001, ACC-003

GIVEN a user installs both `loom-core` and `loom-playbooks`
WHEN the harness discovers skills
THEN both package skill sets are available
AND playbooks route durable truth to core owner layers instead of redefining Loom
truth.

## SCN-003: Playbooks without core

Exercises: REQ-005, REQ-008, ACC-003

GIVEN `loom-playbooks` is present without `loom-core`
WHEN a playbook skill is invoked or inspected
THEN the skill guidance names the missing core dependency
AND it does not provide copied using-Loom doctrine or canonical owner-layer skill
content as a substitute.

## SCN-004: Catalog-backed harness install

Exercises: REQ-002, REQ-009, REQ-013, ACC-004

GIVEN a harness supports a marketplace or catalog that can list multiple plugin
roots
WHEN the repository catalog is inspected
THEN it lists `loom-core` and `loom-playbooks` as separate package roots
AND the catalog does not contain the only copy of any Loom semantic requirement.

## SCN-005: OpenCode split packages

Exercises: REQ-010, REQ-015, ACC-004, ACC-005

GIVEN OpenCode package work has been implemented
WHEN a user configures OpenCode with the split packages
THEN `@z3z1ma/open-loom-core` exposes core using-Loom references and core skills
AND `@z3z1ma/open-loom-playbooks` exposes playbook skills only
AND the repository root package is private/non-published repo metadata rather than
a third publishable `open-loom` package or compatibility meta-package.

## SCN-006: Evidence-gated Codex preload

Exercises: REQ-011, ACC-006

GIVEN Codex package work wants to claim installed-plugin `SessionStart` preload
WHEN docs or acceptance claim that preload works
THEN current runtime evidence exists showing installed `loom-core` bundled hooks
load from the plugin path and add using-Loom context as expected.

## SCN-007: Evidence-gated Gemini extension packaging

Exercises: REQ-012, REQ-016, ACC-006, ACC-009

GIVEN Gemini package work wants to claim install support
WHEN docs or acceptance describe how Gemini users install Loom
THEN the described route is one of: explicit local package-root link/install,
repository-root core-only install through the Gemini shim, accepted separate
release/distribution packaging, or explicitly deferred upstream support
AND docs do not present this repository's subdirectories as a seamless remote
extension install path
AND docs do not imply repository-root Gemini install includes playbooks.

## SCN-009: Gemini root core shim

Exercises: REQ-006, REQ-012, REQ-016, ACC-006, ACC-009

GIVEN a user installs the repository root as a Gemini extension
WHEN Gemini extension discovery runs
THEN `loom-core` using-Loom context and core skills are visible
AND playbook skills are absent
AND install docs prefer clone-and-link for full core plus playbooks installs.

## SCN-008: Stale root path rejection

Exercises: REQ-006, REQ-013, REQ-014, ACC-007

GIVEN package-root migration is complete
WHEN a future agent searches public docs, active owner records, and harness
manifests
THEN no active current-truth surface points to root `skills/` as the product
surface, except the Gemini-only core shim authorized by `decision:0009`
AND historical references are marked superseded, historical, or scoped to prior
evidence.

# Acceptance

- ACC-001: The repository contains `loom-core/skills` and `loom-playbooks/skills`
  with the membership defined by REQ-003 and REQ-004.
- ACC-002: A core-only package-root inspection shows core skills and using-Loom
  references are available without playbook skills and without a root `skills/`
  dependency.
- ACC-003: A playbook package inspection shows no duplicated core skill directories
  and clear dependency wording on `loom-core`.
- ACC-004: Harness package metadata and root catalogs, where present, expose the
  two package roots as separate installable units.
- ACC-005: OpenCode package checks demonstrate `@z3z1ma/open-loom-core` and
  `@z3z1ma/open-loom-playbooks` register the correct package-root skill paths and
  any core preload paths, while the repository root package is private/non-published
  and does not present a third publishable Loom package.
- ACC-006: Codex and Gemini docs only claim behavior that has current runtime
  evidence or explicitly mark the behavior as unvalidated/deferred.
- ACC-007: Public docs, active owner records, examples intended as current review
  fixtures, and harness manifests no longer present root `skills/` as current
  product truth except for the Gemini-only core shim authorized by `decision:0009`.
- ACC-008: Final split critique records no open medium/high findings without
  ticket-owned disposition before release acceptance.
- ACC-009: Gemini root install evidence shows the repository-root extension exposes
  core context/skills only, and install docs state root install is core-only while
  full Gemini installs should use explicit package-root links.

Coverage:

| Acceptance ID | Requirements | Scenarios | Evidence target |
| --- | --- | --- | --- |
| ACC-001 | REQ-001, REQ-002, REQ-003, REQ-004 | SCN-001, SCN-002 | membership scan and skill frontmatter scan |
| ACC-002 | REQ-003, REQ-006, REQ-007 | SCN-001 | core-only package inspection and stale root path scan |
| ACC-003 | REQ-005, REQ-008 | SCN-002, SCN-003 | duplicate-core scan and playbook dependency wording review |
| ACC-004 | REQ-002, REQ-009, REQ-013 | SCN-004 | manifest/catalog syntax and path checks |
| ACC-005 | REQ-010, REQ-015 | SCN-005 | OpenCode smoke checks, package dry-runs, and root private package inspection |
| ACC-006 | REQ-011, REQ-012, REQ-016 | SCN-006, SCN-007, SCN-009 | Codex/Gemini runtime evidence or explicit deferral notes |
| ACC-007 | REQ-006, REQ-013, REQ-014 | SCN-008 | grep for stale current-truth root `skills/` claims with Gemini shim exception |
| ACC-008 | REQ-014 | SCN-008 | final critique and ticket-owned finding dispositions |
| ACC-009 | REQ-006, REQ-012, REQ-016 | SCN-007, SCN-009 | Gemini root install/list evidence and install-doc review |

# Evidence Plan

| Claim / acceptance ID | Evidence type | Expected artifact | Limits / notes |
| --- | --- | --- | --- |
| ACC-001 | structural scan | Evidence record with package tree and skill membership output | Does not prove harness runtime behavior |
| ACC-002 | package inspection | Evidence record showing core-only skill discovery or equivalent structural proof | Harness-specific discovery should be captured separately |
| ACC-003 | targeted grep/review | Evidence record showing no duplicated core directories under playbooks and dependency wording present | Review should include playbook `SKILL.md` files |
| ACC-004 | manifest/catalog validation | Evidence record with JSON checks and path checks | Runtime install may need harness-specific evidence |
| ACC-005 | OpenCode smoke | Evidence record for `@z3z1ma/open-loom-core`, `@z3z1ma/open-loom-playbooks`, and root private package checks | Root package should remain repo metadata, not a third published package |
| ACC-006 | runtime harness validation or deferral | Codex/Gemini evidence records or explicit ticket deferral | Do not infer from docs alone |
| ACC-007 | stale reference scan | Evidence record with grep queries and review notes | Historical/superseded records may still mention root `skills/` |
| ACC-008 | critique | Final critique record and ticket dispositions | Critique does not close tickets itself |
| ACC-009 | Gemini runtime and docs review | Evidence record for root install/list behavior plus install-doc diff review | Does not validate remote playbook install |

# Amendment Notes

- 2026-05-07T23:20:14Z: Added `decision:0009` Gemini-only root core shim
  exception, `REQ-016`, `SCN-009`, and `ACC-009`.
- 2026-05-08T01:16:04Z: Amended `REQ-004` to add the optional peer-inspired
  playbooks accepted by `research:peer-playbook-integration-candidates` under
  `ticket:plybk508`.

# Contract Review

- Completeness: covers package roots, membership, dependency, root `skills/`
  retirement with the Gemini shim exception, harness catalog boundaries, OpenCode
  naming, Codex/Gemini evidence gates, docs, and reference reconciliation.
- Correctness: reflects `decision:0008`, `decision:0009`, the split feasibility
  research, `research:peer-playbook-integration-candidates`, and the active split
  plan rather than the current unsplit source tree.
- Coherence: uses `core`, `playbooks`, `package roots`, and `product surface` as
  stable terms; distinguishes package metadata from semantic ownership.

# Assumptions / Decision Points

| Assumption or question | Reversible? | Blocks downstream work? | Disposition |
| --- | --- | --- | --- |
| `loom-core` and `loom-playbooks` are the package-root names | yes | no | accepted by `decision:0008` |
| `loom-playbooks` requires core instead of duplicating it | yes, but costly | yes for playbook packaging | accepted by `decision:0008` |
| OpenCode uses two scoped packages only | yes | yes for OpenCode package work | accepted for this contract; legacy `open-loom` migration remains follow-up |
| Existing root `open-loom` package handling after split | yes | yes for OpenCode package work | root package becomes private/non-published repo metadata; no compatibility meta-package |
| Codex installed-plugin hooks work for core preload | yes | no for package layout; yes for preload claims | requires runtime evidence |
| Gemini can support two package roots cleanly | yes | no for package layout; yes for Gemini install claims | root install is accepted as core-only by `decision:0009`; playbooks still require local-link docs, accepted release/distribution route, or upstream support |

# Open Questions

- Should future releases add a convenience meta-package after core/playbooks are
  stable, or would that recreate the confusion this split is meant to remove?
- What versioning scheme should tie `@z3z1ma/open-loom-core` and
  `@z3z1ma/open-loom-playbooks` together when playbooks depend on core behavior?
- Which harnesses can enforce package dependencies mechanically, and which must rely
  on docs and skill prose?
