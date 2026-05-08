---
id: critique:peer-playbook-integration-review
kind: critique
status: final
created_at: 2026-05-08T01:26:58Z
updated_at: 2026-05-08T01:56:40Z
scope:
  kind: repository
  repositories:
    - repo:root
review_target: "ticket:plybk508 broadened Addy/Superpowers playbook integration diff"
links:
  ticket:
    - ticket:plybk508
  evidence:
    - evidence:peer-playbook-integration-check
  research:
    - research:peer-playbook-integration-candidates
  spec:
    - spec:core-and-playbooks-package-contract
external_refs: {}
---

# Summary

Reviewed the broadened Addy/Superpowers `loom-playbooks` expansion for
protocol-change and operator-clarity risk: package-contract amendment, 25-skill
package membership, eighteen added playbook directories, existing-playbook
deepenings, ticket scope, research provenance, structural evidence, and required
runtime / shadow-ledger boundaries.

# Review Target

Target: `ticket:plybk508` current uncommitted diff, including:

- `.loom/specs/core-and-playbooks-package-contract.md`
- `.loom/plans/20260507-split-core-and-playbooks-packages.md`
- `.loom/tickets/20260508-plybk508-add-peer-playbook-integrations.md`
- `.loom/evidence/20260508-peer-playbook-integration-check.md`
- `.loom/research/peer-playbook-integration-candidates.md`
- eighteen added playbook directories under `loom-playbooks/skills/`
- modified existing playbooks under `loom-playbooks/skills/`
- `loom-skill-authoring/references/skill-routing-and-pressure-testing.md`

Profiles: `protocol-change`, `operator-clarity`.

# Verdict

`pass_with_findings`

No blocking findings on playbook substance, owner-layer boundaries, package
membership, or required peer-runtime leakage. The broadened playbooks are
materially adapted, not skeletal. Ticket closure should wait until the evidence,
critique, and provenance findings below are consumed by the ticket ledger.

# Findings

## FIND-001: Evidence scan does not cover all changed playbook surfaces

Severity: medium
Confidence: high
State: resolved by `evidence:peer-playbook-integration-check` supplement

Observation:

The evidence initially validated placeholder / rejected-surface scans only over
the eighteen added playbook directories. Ticket scope also includes deepened
existing playbooks and the new `loom-skill-authoring` reference, so
`ticket:plybk508#ACC-002` and `ticket:plybk508#ACC-004` were not fully evidenced
for all changed `loom-playbooks/skills/**` surfaces.

Why it matters:

Rejected peer runtime surfaces and copied placeholder residue can enter through
modified existing playbooks or dense references, not only through newly added
playbook directories. Acceptance evidence needs to match the full write scope.

Follow-up:

Add a changed-file or diff-scoped scan / review covering modified existing
playbooks plus the new `loom-skill-authoring` reference. Classify expected
anti-pattern/template hits as non-requirements.

Resolution:

`evidence:peer-playbook-integration-check` now records changed-surface scans over
44 changed `loom-playbooks/skills` files, strict required-runtime scans, tracked
playbook diff-added-line scans, and classifications for intentional
`loom-skill-authoring` rejection/routing references.

Challenges:

- `ticket:plybk508#ACC-002`
- `ticket:plybk508#ACC-004`

## FIND-002: Ticket ledger still marks current evidence/critique state stale

Severity: medium
Confidence: high
State: open pending ticket-owned disposition

Observation:

`ticket:plybk508` still says validation and critique remain pending/stale even
though refreshed structural evidence exists and this broader critique has a final
verdict.

Why it matters:

Tickets are the live execution ledger. If the ticket evidence and critique
sections remain stale, a future agent could miss the validation and review state
or incorrectly continue already-completed reconciliation work.

Follow-up:

Reconcile ticket evidence disposition after `FIND-001`, record this critique
disposition, and update acceptance basis / residual risks before closure.

Challenges:

- `ticket:plybk508#ACC-004`
- `ticket:plybk508#ACC-005`

## FIND-003: Broadened source-read provenance is weaker than the adaptation claim

Severity: low
Confidence: high
State: resolved by `research:peer-playbook-integration-candidates` amendment

Observation:

The added Addy/Superpowers coverage was mapped substantively in prose, but some
broadened Addy and Superpowers reads were only named in a continuation note
without the same path/line-range provenance as the earlier source list.
Completion basis also still referenced the original research pass.

Why it matters:

This ticket claims practical peer workflow knowledge was preserved rather than
thinly summarized. The research record should make the broader source material
auditable without transcript context.

Follow-up:

Promote the added source reads into the Sources / Evidence Synthesis section
with concrete path and line ranges, and update the completion basis for the
broadened amendment.

Resolution:

`research:peer-playbook-integration-candidates` now includes concrete key-read
path and line-range provenance for the broader Addy and Superpowers source set
and an amended completion basis for the post-review broadened adaptation.

# Evidence Reviewed

- Git status and scoped diff for the current uncommitted Loom records and
  `loom-playbooks/skills/**` changes.
- `research:peer-playbook-integration-candidates`
- `spec:core-and-playbooks-package-contract` amended `REQ-004`
- `plan:split-core-and-playbooks-packages` playbook membership list
- `ticket:plybk508`
- `evidence:peer-playbook-integration-check`
- New and deepened playbooks under `loom-playbooks/skills/**`, including the
  eighteen added playbook directories and modified existing playbook entries.
- Package membership comparison, OpenCode playbooks smoke output, npm dry-run
  package check, diff whitespace check, required-runtime scans, placeholder /
  rejected-surface scans, and non-ASCII scans.

# Residual Risks

- Long-term operator clarity is still empirical; first real use may expose overlap
  between drive, spec, planning, verification, and specialist playbooks.
- Harness runtime behavior beyond local OpenCode smoke remains outside this
  evidence, correctly so.
- Peer-source adaptation is substantively improved, but future upstream changes
  can stale the research provenance.

# Required Follow-up

- Record ticket-owned dispositions for `FIND-001`, `FIND-002`, and `FIND-003`
  before closure.

# Acceptance Recommendation

`follow-up-needed-before-acceptance`

Do not close `ticket:plybk508` until `FIND-001` and `FIND-002` are resolved or
dispositioned. `FIND-003` may be fixed before closure or accepted as low-risk
provenance debt with ticket-owned rationale. After the recorded evidence,
research, and ticket reconciliation dispositions are complete, no critique
blocker remains from this review.
