---
id: evidence:workspace-support-grammar-validation
kind: evidence
status: recorded
created_at: 2026-05-03T01:42:43Z
updated_at: 2026-05-03T01:49:55Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  ticket:
    - ticket:wssupp4
  packet:
    - packet:ralph-ticket-wssupp4-20260503T014057Z
---

# Summary

Observation-first validation for `ticket:wssupp4`: workspace/support lifecycle
and query grammar now names `kind: workspace`, discovers `.loom/workspace.md`,
`.loom/harness.md`, and optional `.loom/support/` artifacts, and preserves the
support/canonical owner boundary.

# Supports Claims

- `initiative:skills-corpus-residual-protocol-sharpening-pass#OBJ-006`
- `ticket:wssupp4#ACC-001`
- `ticket:wssupp4#ACC-002`
- `ticket:wssupp4#ACC-003`
- `ticket:wssupp4#ACC-004`

# Procedure

Working tree source version at launch:

```text
$ git rev-parse HEAD
bce12c610dc46ec5a415c689f7d80520546a9a09

$ git status --short
 M .loom/tickets/20260503-wssupp4-complete-workspace-support-grammar.md
?? .loom/packets/ralph/20260503T014057Z-ticket-wssupp4-iter-01.md
```

The baseline commit matched the packet fingerprint. The modified ticket and
untracked packet were the active handoff surfaces supplied for this iteration.

Search scope:

```text
skills/loom-records/references/status-lifecycle.md
skills/loom-records/references/query-and-linking.md
skills/loom-records/references/naming-and-ids.md
skills/loom-records/references/frontmatter.md
skills/loom-workspace/references/workspace-tree.md
skills/loom-workspace/references/status-snapshot.md
.loom/tickets/20260503-wssupp4-complete-workspace-support-grammar.md
.loom/packets/ralph/20260503T014057Z-ticket-wssupp4-iter-01.md
```

# Before Observations

Command:

```bash
rg -n -- 'kind: workspace|\.loom/workspace\.md|\.loom/harness\.md|\.loom/support|drive-handoffs|workspace-support|support-artifact' \
  skills/loom-records/references/status-lifecycle.md \
  skills/loom-records/references/query-and-linking.md \
  skills/loom-records/references/naming-and-ids.md \
  skills/loom-records/references/frontmatter.md \
  skills/loom-workspace/references/workspace-tree.md \
  skills/loom-workspace/references/status-snapshot.md \
  .loom/tickets/20260503-wssupp4-complete-workspace-support-grammar.md \
  .loom/packets/ralph/20260503T014057Z-ticket-wssupp4-iter-01.md
```

Observed before-state highlights:

- `naming-and-ids.md` already listed `workspace`, `workspace-support`, and
  `support-artifact` rows, including `.loom/workspace.md`, `.loom/harness.md`,
  `.loom/support/<domain>/<slug>.md`, and
  `.loom/support/drive-handoffs/<UTC compact timestamp>-<slug>.md`.
- `status-lifecycle.md` listed `kind: workspace-support`, saved drive handoffs,
  memory, and support artifacts, but had no `kind: workspace` lifecycle row.
- `workspace-tree.md` showed optional `.loom/support/drive-handoffs/`, omitted
  `.loom/support/` from the bootstrap command, and listed `.loom/workspace.md`
  and `.loom/harness.md` as first files worth creating.
- `status-snapshot.md` mentioned optional `.loom/support/` artifacts and queried
  `.loom/support`, but did not query `.loom/workspace.md` or `.loom/harness.md`.
- `query-and-linking.md` broad discovery examples did not include
  `.loom/workspace.md`, `.loom/harness.md`, optional `.loom/support/` paths,
  `workspace-support`, or `support-artifact` support queries.

Boundary command:

```bash
rg -n -- 'canonical (owner|project truth|truth|owner layer)|noncanonical|support surfaces|support-local|own project truth|canonical owners' <same scope>
```

Observed before-state boundary highlights:

- `naming-and-ids.md`, `frontmatter.md`, `workspace-tree.md`, and
  `status-snapshot.md` already stated that packet, memory, workspace-support, and
  support-artifact surfaces are support-local or noncanonical.
- The scoped references did not yet pair `kind: workspace` lifecycle guidance
  with the same explicit noncanonical owner boundary.

# After Observations

Command:

```bash
rg -n -- 'kind: workspace|\.loom/workspace\.md|\.loom/harness\.md|\.loom/support|drive-handoffs|workspace-support|support-artifact' <same scope>
```

Observed after-state highlights:

- `status-lifecycle.md` now contains
  `workspace metadata records with kind: workspace: active | stale | superseded | retired`.
- `status-lifecycle.md` now states `.loom/workspace.md` may use `active`,
  `stale`, `superseded`, and `retired` for metadata currency only, and must not
  own project identity, objective state, live ticket state, acceptance, evidence
  sufficiency, critique verdicts, wiki truth, canonical truth, or packet
  lifecycle.
- `query-and-linking.md` now includes broad discovery for `workspace:harness`,
  `support:<domain>-<slug>`, `.loom/workspace.md`, `.loom/harness.md`, and
  `.loom/support/` while stating those support handles do not make the surfaces
  canonical project-truth owners.
- `query-and-linking.md` now includes optional support-surface queries for
  `.loom/workspace.md`, `.loom/harness.md`, `.loom/support`, and
  `.loom/support/drive-handoffs/`.
- `status-snapshot.md` now includes `.loom/workspace.md`, `.loom/harness.md`, and
  `.loom/support/` in optional support inputs and native queries.
- `workspace-tree.md` now explicitly labels `.loom/workspace.md` and
  `.loom/harness.md` as metadata/support files rather than canonical owners.

Post-critique repair at `2026-05-03T01:49:55Z` narrowed the optional support
metadata query in `query-and-linking.md`: `.loom/support` retains the `^status:`
search for saved support artifacts, while `skills/loom-*/templates` is searched
only for support-artifact template fields. This avoids unrelated template status
noise while keeping support template discovery.

Boundary command:

```bash
rg -n -- 'canonical (owner|project truth|truth|owner layer)|noncanonical|support surfaces|support-local|own project truth|canonical owners' <same scope>
```

Observed after-state boundary highlights:

- Boundary wording remains present for support-local IDs, support artifacts,
  memory, packets, and optional `.loom/support/` artifacts.
- New workspace lifecycle wording preserves the same boundary: `kind: workspace`
  status describes metadata currency only, not project truth or packet lifecycle.
- No guidance was added that requires `.loom/support/` at bootstrap or makes
  workspace, harness, memory, packets, or support artifacts canonical owner
  records.

# Validation

Command:

```bash
git diff --check
```

Initial result: passed with no output.

Post-critique repair result: passed with no output.

# Limitations

- This evidence records structural searches and diff validation only; mandatory
  oracle critique remains required before ticket acceptance.
