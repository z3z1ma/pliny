---
id: ticket:plybk508
kind: ticket
status: closed
change_class: protocol-authority
risk_class: medium
created_at: 2026-05-08T01:16:04Z
updated_at: 2026-05-08T02:25:02Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  research:
    - research:peer-playbook-integration-candidates
  decision:
    - decision:0008
  plan:
    - plan:split-core-and-playbooks-packages
  spec:
    - spec:core-and-playbooks-package-contract
  evidence:
    - evidence:peer-playbook-integration-check
  critique:
    - critique:peer-playbook-integration-review
    - critique:playbook-owner-boundary-audit
external_refs: {}
depends_on: []
---

# Summary

Comprehensively adapt Addy Osmani `agent-skills` and Obra `superpowers` engineering workflows into `loom-playbooks`, accounting for overlap while preserving `loom-core` ownership boundaries.

# Context

`research:peer-playbook-integration-candidates` concluded that the core/playbooks split enables optional Loom-native workflow playbooks for recurring engineering disciplines that should not live in `loom-core`. Operator review rejected the first six-playbook pass as too skeletal relative to the upstream source material, so this ticket now covers a broader adaptation: nearly every Addy and Superpowers skill should become either a substantial Loom playbook, a dense reference inside an overlapping playbook, a core owner-layer route, or an explicit rejected runtime/surface.

# Scope

In:

- Amend `spec:core-and-playbooks-package-contract` so `loom-playbooks/skills` may contain the broader optional playbook set needed for the Addy/Superpowers adaptation.
- Preserve and deepen the first-pass playbooks: `loom-architecture`, `loom-product-discovery`, `loom-ui-browser`, `loom-security`, `loom-migration`, and `loom-simplification`.
- Add substantial Loom-native playbooks for peer disciplines that deserve their own activation triggers: `loom-incremental-implementation`, `loom-tdd`, `loom-source-grounding`, `loom-context-engineering`, `loom-code-review`, `loom-ci-cd`, `loom-performance`, `loom-docs-sync`, and `loom-agent-orchestration`.
- Deepen existing playbooks where peer discipline overlaps current routes: `loom-debugging`, `loom-spike`, `loom-codemap`, `loom-ship`, `loom-git`, `loom-drive`, and `loom-skill-authoring`.
- Update `research:peer-playbook-integration-candidates` and `plan:split-core-and-playbooks-packages` so the broader source-material adaptation is recoverable from records, not only from chat.
- Preserve `loom-core` dependency wording and route durable facts through core owner layers instead of creating new truth owners.
- Validate package structure with smoke / pack checks, targeted placeholder and stale-path scans, an evidence record, and mandatory critique.

Out:

- Moving any new workflow into `loom-core`.
- Importing peer command wrappers, hooks, MCP requirements, issue tracker labels, `.superpowers`, `docs/ideas`, generated plans, or peer runtime state as Loom truth.
- Adding templates, scripts, hidden runtime dependencies, required browser/devtools tooling, required subagent transport, or required CI vendor configuration for the new playbooks.
- Claiming harness runtime behavior beyond structural/package checks.
- Closing or modifying unrelated untracked example-app artifacts already present in the worktree.

Assumptions / decision triggers:

| Assumption or question | Reversible? | Blocks execution? | Disposition |
| --- | --- | --- | --- |
| One implementation ticket can cover the spec amendment, playbook files, structural evidence, and critique because all changes share one package-membership contract. | yes | no | accepted for this bounded expansion; split follow-up tickets only if validation or critique finds scope too broad |
| The broader candidate set remains workflow skills rather than owner layers. | yes, but costly after release | yes | accepted by revised `research:peer-playbook-integration-candidates` and constrained by `decision:0008` |
| `loom-ui-browser` is the name for the frontend/browser route. | yes | no | accepted for this ticket; critique may recommend rename before closure |

# Acceptance

Owner: spec-owned plus ticket-local skill-quality criteria.

Criteria / covered IDs:

- `spec:core-and-playbooks-package-contract#REQ-004`
- `spec:core-and-playbooks-package-contract#REQ-005`
- `spec:core-and-playbooks-package-contract#REQ-008`
- `spec:core-and-playbooks-package-contract#ACC-001`
- `spec:core-and-playbooks-package-contract#ACC-003`
- `ticket:plybk508#ACC-001`
- `ticket:plybk508#ACC-002`
- `ticket:plybk508#ACC-003`
- `ticket:plybk508#ACC-004`
- `ticket:plybk508#ACC-005`
- `ticket:plybk508#ACC-006`

Ticket-local criteria, only when no spec owns the reusable contract:

- ACC-001: Each new playbook has `name`, `description`, `compatibility`, `metadata.skill_kind`, core dependency wording, ownership / non-ownership boundaries, use and exclusion triggers, actionable procedure, common rationalizations, red flags, verification, done means, and read-order guidance.
- ACC-002: Each new playbook routes durable truth to existing Loom owner layers and does not introduce new canonical storage paths, templates, scripts, MCPs, command wrappers, or external-tool requirements.
- ACC-003: Addy and Superpowers source skills are accounted for as new playbooks, existing-playbook deepenings, core owner routes, or rejected peer runtime/surface mechanics, with practical procedures preserved in Loom-native form rather than only summarized.
- ACC-004: Structural checks show package smoke / pack validation still passes, new skills are discovered, no copied template placeholders remain, and no rejected peer storage paths or required runtime surfaces were introduced.
- ACC-005: Mandatory critique reviews the behavior-changing playbook expansion, and any open medium/high findings receive ticket-owned disposition before closure.
- ACC-006: Optional playbooks have distinct workflow-composition or specialist-discipline boundaries; peer skills that merely duplicate core owner layers or mandatory using-Loom doctrine are routed into the core layer instead of shipped as playbooks.

# Current State

Status rationale: closed after owner-boundary audit pruned the previous
25-playbook set to 22 optional playbooks. `loom-planning`, `loom-spec-driven`,
and `loom-verification` were removed because they duplicated core plans, specs,
and validation/evidence doctrine. `loom-docs-adrs` was renamed and tightened to
`loom-docs-sync` so ADR/decision authority remains with core constitution.
Refreshed evidence and critique are sufficient for the scoped acceptance claims.

Blockers: None.

Execution notes:

- Local execution was used because the write boundary was known, validation could be performed in the current context, and no fresh child contract was needed.
- The write boundary was `.loom/specs/core-and-playbooks-package-contract.md`, `.loom/plans/20260507-split-core-and-playbooks-packages.md`, this ticket, evidence and critique records for this ticket, and `loom-playbooks/skills/**` playbook skill files.
- The six first-pass playbooks were added under `loom-playbooks/skills/`, and existing playbooks were deepened where `research:peer-playbook-integration-candidates` recommended folding peer practice into current routes.
- Operator feedback expanded scope from six candidate playbooks to a near-complete Addy/Superpowers source-material adaptation.
- Added twelve more optional playbooks with dense references in the broadened pass; operator boundary audit later identified `loom-spec-driven`, `loom-planning`, and `loom-verification` as duplicates of core owner-layer / validation doctrine and `loom-docs-adrs` as needing a docs-sync boundary.
- Refreshed `evidence:peer-playbook-integration-check` with package smoke / pack checks, owner-boundary-pruned scans across 38 changed `loom-playbooks/skills` files, removed-playbook active-reference scans, and classifications for intentional anti-pattern/template hits.
- Updated `critique:peer-playbook-integration-review` with the broader final review and added `critique:playbook-owner-boundary-audit` for the strict core-owner duplication audit.

# Evidence

Disposition: sufficient

Records:

- `evidence:peer-playbook-integration-check`

Gaps / limits:

- Evidence is structural and package-inspection based; it does not prove harness runtime install behavior beyond the local OpenCode smoke path.
- Evidence does not prove long-term operator clarity in real use; first practical use may expose playbook overlap that needs later tightening.
- Existing intentional template placeholders and pre-existing non-ASCII in old playbook files were classified rather than cleaned because they were outside this ticket's product-surface mutation.

# Review And Follow-Through

Critique policy: mandatory
Critique rationale: The change adds and modifies optional skills that affect future operator routing, verification, and risk decisions across Loom workflows.
Critique disposition: completed

Required critique profiles:

- protocol-change
- operator-clarity

Findings:

- `critique:peer-playbook-integration-review#FIND-001` (medium): resolved by supplementing `evidence:peer-playbook-integration-check` with changed-surface scans across 44 changed `loom-playbooks/skills` files, strict required-runtime scans, tracked diff-added-line scans, and explicit classification of intentional `loom-skill-authoring` rejection/routing references.
- `critique:peer-playbook-integration-review#FIND-002` (medium): resolved by this ticket update; evidence disposition is sufficient, critique disposition is completed, acceptance basis is current, and residual risks are explicit.
- `critique:peer-playbook-integration-review#FIND-003` (low): resolved by promoting broader Addy/Superpowers source reads into `research:peer-playbook-integration-candidates` key-read provenance and amending the completion basis for the broadened pass.
- `critique:playbook-owner-boundary-audit#FIND-001` (medium): resolved by refreshing `evidence:peer-playbook-integration-check` for the 22-skill pruned package state and recording ticket-owned acceptance against the current package membership.

Promotion disposition: not_required
Promotion / deferral rationale: Durable learning from this ticket was already promoted into the product skill corpus, the package contract, and the concluded research. No separate wiki or additional owner-layer promotion is needed for closure.

Promoted / deferred:

- None - no separate promotion artifact was needed beyond the edited product skill
  corpus, package contract, and concluded research.

Wiki disposition: not_required - accepted explanation is embodied in the new and updated playbook skills plus `research:peer-playbook-integration-candidates`; no standalone wiki page is needed.

# Acceptance Decision

Required before closure when acceptance, accepted risk, or operator provenance needs to be explicit.

Accepted by:
OpenCode

Accepted at:
2026-05-08T02:25:02Z

Basis: Accepted because `spec:core-and-playbooks-package-contract#REQ-004` now permits the owner-boundary-pruned 22 optional playbooks, `REQ-005` / `REQ-008` remain satisfied by package smoke inspection, `loom-planning`, `loom-spec-driven`, and `loom-verification` were removed as core-layer duplicates, `loom-docs-adrs` was replaced by `loom-docs-sync`, the playbook package smoke and dry-run package checks pass, changed playbook surfaces were scanned for removed-playbook active references / placeholder residue / rejected peer runtime surfaces / required runtime wording, `research:peer-playbook-integration-candidates` records the core-owner routes for pruned peer skills, and mandatory critique has no remaining blocker after ticket-owned finding dispositions.

Residual risks:

- Harness runtime behavior beyond local OpenCode smoke was not proven and is outside this ticket's claim.
- Long-term operator clarity is empirical; later use may reveal overlap among the remaining specialist playbooks that should be tightened in follow-up work.
- Upstream Addy/Superpowers repositories may change after the observed commits; recheck research provenance before future tickets depend on exact upstream wording.

# Dependencies

No hard upstream ticket prerequisites. This work depends on `research:peer-playbook-integration-candidates`, `decision:0008`, and the amended package contract for scope.

# Journal

- 2026-05-08T01:16:04Z: Created active ticket for the peer playbook integration implementation, including the required package-contract amendment, product-surface edits, evidence, and critique gates.
- 2026-05-08T01:26:58Z: Added six optional playbooks, deepened seven existing playbooks, amended the package contract and plan membership, recorded structural evidence, completed mandatory critique, resolved the critique finding by reconciling ticket evidence, and closed the ticket.
- 2026-05-08T01:28:42Z: Reopened after operator feedback that the first implementation preserved Loom boundaries but dropped too much practical knowledge from the peer source skills; evidence and critique are stale until a deeper pass lands.
- 2026-05-08T01:46:00Z: Expanded scope to comprehensive Addy/Superpowers adaptation, revised research/spec/plan membership, added twelve optional playbooks with dense references, and cross-linked existing playbooks; evidence and critique remain pending refresh.
- 2026-05-08T01:56:40Z: Supplemented evidence with changed-surface scans over 44 changed `loom-playbooks/skills` files and updated research provenance / completion basis for the broadened Addy/Superpowers source set.
- 2026-05-08T01:59:21Z: Reconciled the broader mandatory critique, recorded ticket-owned dispositions for all findings, reran final smoke / pack / scoped diff checks, accepted the scoped structural / operator-boundary claims, and closed the ticket.
- 2026-05-08T02:14:36Z: Reopened after operator review found that some supplementary playbooks duplicate core owner-layer responsibilities instead of adding genuine workflow composition. Audit target: remove or merge those skills and update package membership, references, evidence, and critique.
- 2026-05-08T02:25:02Z: Removed `loom-planning`, `loom-spec-driven`, and `loom-verification`; replaced `loom-docs-adrs` with `loom-docs-sync`; reconciled spec, plan, research, evidence, and critique to the 22-playbook package state; recorded ticket-owned finding dispositions; reran final smoke / pack / scoped diff checks; and closed the ticket.
