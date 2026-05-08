---
id: evidence:peer-playbook-integration-check
kind: evidence
status: recorded
created_at: 2026-05-08T01:16:04Z
updated_at: 2026-05-08T02:25:02Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  ticket:
    - ticket:plybk508
  spec:
    - spec:core-and-playbooks-package-contract
  research:
    - research:peer-playbook-integration-candidates
external_refs: {}
---

# Summary

Observed structural validation for the owner-boundary-pruned peer playbook
integration work. The checks support that `loom-playbooks` now discovers 22
skills, still avoids core doctrine preload, passes the OpenCode package smoke
check, passes the npm dry-run package check, and the changed playbook surfaces
contain no unresolved targeted placeholder residue, removed-playbook active
references, rejected peer storage paths, or required runtime surfaces.
Supplemental scans cover the 38 changed `loom-playbooks/skills` files and the
tracked playbook diff.

Evidence records observations. The ticket owns acceptance and critique consumes
this evidence when reviewing the behavior-changing skill expansion.

# Procedure

Observed at: 2026-05-08T01:48:34Z for the first broadened package checks;
supplemental owner-boundary-pruned smoke / pack / scan / diff-check rerun
observed at 2026-05-08T02:17:20Z, with final record update at
2026-05-08T02:25:02Z after ticket and critique reconciliation.

Source state: branch `main`, HEAD `d725051d572b049330fe2fb9f77487648d3368c1`, with uncommitted changes for `ticket:plybk508` and the prior untracked `research:peer-playbook-integration-candidates` record.

Procedure:

- `npm --prefix "loom-playbooks" run smoke`
- `npm --prefix "loom-playbooks" run pack:check`
- `rg -n 'required MCP|MCP requirement|must use .*MCP|requires? .*MCP|required browser|required subagent|required CI vendor|must use GitHub Actions|must use \.superpowers|must write to docs/ideas|must use command wrapper|must install hook' "loom-playbooks/skills"`
- `rg -n '\.superpowers|docs/ideas|docs/superpowers|~/.config/superpowers|command wrapper|hook script' "loom-playbooks/skills"`
- `rg -n 'TBD|my-skill|my-router|<specific|<owner|<reference>' "loom-playbooks/skills"`
- `git ls-files --modified --others --exclude-standard -- "loom-playbooks/skills"`
- `git ls-files -z --modified --others --exclude-standard -- "loom-playbooks/skills" | xargs -0 rg -n 'TBD|my-skill|my-router|<specific|<owner|<reference>|\.superpowers|docs/ideas|docs/superpowers|required MCP|MCP requirement|hook script|command wrapper|~/.config/superpowers' || true`
- `git ls-files -z --modified --others --exclude-standard -- "loom-playbooks/skills" | xargs -0 rg -n '[^[:ascii:]]' || true`
- `git ls-files -z --modified --others --exclude-standard -- "loom-playbooks/skills" | xargs -0 rg -n 'required MCP|MCP requirement|must use .*MCP|requires? .*MCP|required browser|required subagent|required CI vendor|must use GitHub Actions|must use \.superpowers|must write to docs/ideas|must use command wrapper|must install hook' || true`
- `git diff -- "loom-playbooks/skills" | rg -n '^\+.*(TBD|my-skill|my-router|<specific|<owner|<reference>|\.superpowers|docs/ideas|docs/superpowers|required MCP|MCP requirement|hook script|command wrapper|~/.config/superpowers)' || true`
- `git diff -- "loom-playbooks/skills" | rg -n '^\+.*[^[:ascii:]]' || true`
- `git diff -- "loom-playbooks/skills" | rg -n '^\+.*(required MCP|MCP requirement|must use .*MCP|requires? .*MCP|required browser|required subagent|required CI vendor|must use GitHub Actions|must use \.superpowers|must write to docs/ideas|must use command wrapper|must install hook)' || true`
- `git diff --check -- "loom-playbooks" ".loom/specs/core-and-playbooks-package-contract.md" ".loom/plans/20260507-split-core-and-playbooks-packages.md" ".loom/tickets/20260508-plybk508-add-peer-playbook-integrations.md" ".loom/research/peer-playbook-integration-candidates.md"`
- Final rerun after record reconciliation: `npm --prefix "loom-playbooks" run smoke`, `npm --prefix "loom-playbooks" run pack:check`, and scoped `git diff --check` over `loom-playbooks` plus the linked Loom records.
- Owner-boundary-pruned rerun: `git ls-files --modified --others --deleted --exclude-standard -- "loom-playbooks/skills"`, changed-playbook `rg` scan for removed skill references / placeholders / required runtimes, tracked-diff added-line scan for the same terms, `npm --prefix "loom-playbooks" run smoke`, `npm --prefix "loom-playbooks" run pack:check`, and scoped `git diff --check`.
- Final reconciliation rerun: `npm --prefix "loom-playbooks" run smoke`, `npm --prefix "loom-playbooks" run pack:check`, and scoped `git diff --check` after ticket, evidence, and critique record edits.

Expected result when applicable: package smoke and dry-run checks pass; package
inspection reports 22 playbook skills; changed-surface scans produce no active
references to removed playbooks, placeholder residue, rejected-surface terms, or
required-runtime terms; tracked playbook diff-added-line scans produce no active
removed-playbook, rejected-surface, or required-runtime hits; changed-file
whitespace check reports no issues.

Actual observed result: expected result observed.

Procedure verdict / exit code: pass; package commands returned exit code 0,
package inspection reported 22 skills, strict changed-surface and tracked-diff
scans produced no output for active removed-playbook references / placeholders /
required runtimes, and scoped `git diff --check` produced no output.

# Artifacts

Package smoke output excerpt:

```json
{
  "ok": true,
  "pluginId": "open-loom-playbooks",
  "usingLoomReferenceCount": 0,
  "instructionCount": 0,
  "doesNotPreloadCoreDoctrine": true,
  "skillCount": 22,
  "skillPath": "/Users/alexanderbutler/code_projects/personal/agent-loom/loom-playbooks/skills",
  "skillPathsAreDeduped": true,
  "usingLoomResult": "not registered by this playbook package",
  "skillsResult": "registered through config.skills.paths"
}
```

Package dry-run output summary:

- `npm --prefix "loom-playbooks" run pack:check` completed successfully.
- Dry-run tarball contents included 22 `skills/*/SKILL.md` files and the new dense references.
- Dry-run tarball summary: 58 total files, package size 114.7 kB, unpacked size 350.4 kB.

Changed-file whitespace check: no output.

Changed playbook surface list: 38 changed `loom-playbooks/skills` files,
including the fifteen retained added playbook directories, seven modified
existing playbook `SKILL.md` files, and
`loom-skill-authoring/references/skill-routing-and-pressure-testing.md`.

Removed playbook active-reference scan: no output for `skills/loom-planning`,
`skills/loom-spec-driven`, `skills/loom-verification`, `skills/loom-docs-adrs`,
or `loom-docs-adrs` in changed playbook files or tracked diff-added lines.

Changed playbook placeholder / required-runtime / rejected-surface scan: no
output for the strict owner-boundary-pruned scan terms.

Tracked playbook diff-added-line scans for removed-playbook active references,
placeholder / rejected-surface terms, and required-runtime terms: no output.

Whole `loom-playbooks/skills` broad placeholder scan previously observed
intentional template/reference/example hits in pre-existing templates and
anti-pattern prose; the current strict changed-surface scan had no hits.

Strict required-runtime scan across `loom-playbooks/skills`: no output. This
specifically checked for required MCP/browser/subagent/CI-vendor/command-wrapper
phrasing.

Broad peer-surface scan across `loom-playbooks/skills` found only rejection or
anti-pattern context:

- `loom-skill-authoring/references/skill-routing-and-pressure-testing.md` mentions
  command wrappers, `.superpowers`, and `docs/ideas` only as peer runtime or
  storage surfaces to translate/reject.
- `loom-drive/references/outer-loop-subagent-transport.md` and
  `loom-skill-authoring/references/skill-review.md` mention command wrappers only
  as non-owner or hidden-runtime risks.

Broad placeholder scan across `loom-playbooks/skills` found only intentional
template placeholders in `loom-drive/templates/outer-loop-handoff.md`,
`loom-skill-authoring/templates/simple-skill.md`, and
`loom-skill-authoring/templates/router-skill.md`, plus one pre-existing example
placeholder in `loom-drive/references/continuity-contract.md`. These are template
or example surfaces, not copied placeholder residue in the added playbooks.

Whole `loom-playbooks/skills` non-ASCII scan still observes existing non-ASCII in
pre-existing files, including em dashes in `loom-drive/SKILL.md` and tree glyphs in
`loom-skill-authoring/references/structure.md`; the current tracked-diff
added-line scan did not add non-ASCII.

# Raw Artifact Store

- Path: None - command outputs were small enough to summarize in this record.
- Captured artifacts: None - no bulky logs, screenshots, or traces were preserved.
- Key excerpts / index: package smoke JSON excerpt and dry-run tarball summary above.
- Redaction / sensitivity: safe to keep; no secrets or sensitive data observed.
- Retention / tracking: evidence record is sufficient.

# Visual / Product Evidence

N/A - this was structural package and skill-corpus validation, not a visual/UI claim.

# Supports Claims

- `spec:core-and-playbooks-package-contract#REQ-004`: supports package membership
  inspection for 22 optional playbook skills after the owner-boundary-pruned
  `REQ-004` amendment.
- `spec:core-and-playbooks-package-contract#REQ-005`: supports that playbooks still
  do not preload core doctrine.
- `spec:core-and-playbooks-package-contract#REQ-008`: supports continued core
  dependency posture in the playbook package surface.
- `ticket:plybk508#ACC-001`: supports new playbook structure through package
  discovery, targeted scans, and changed-surface scans; prose quality still needs
  critique.
- `ticket:plybk508#ACC-002`: supports absence of rejected peer paths, required MCP
  wording, command wrapper requirements, peer runtime storage, and unresolved
  placeholder residue in the changed playbook surfaces.
- `ticket:plybk508#ACC-003`: supports source-material adaptation structurally by
  showing all new playbooks and cross-links are discoverable; critique must still
  judge sufficiency and overlap.
- `ticket:plybk508#ACC-004`: supports smoke, pack, targeted placeholder,
  non-ASCII, rejected-surface, changed-surface, and whitespace checks.
- `ticket:plybk508#ACC-006`: supports that duplicate peer playbook shapes were
  removed or renamed: `loom-planning`, `loom-spec-driven`, and
  `loom-verification` were removed; `loom-docs-adrs` became `loom-docs-sync`
  with decision authority routed to core constitution.

# Challenges Claims

None - no observed check challenged the scoped structural claims.

# Environment

Commit: `d725051d572b049330fe2fb9f77487648d3368c1` plus uncommitted scoped changes.
Branch: `main`
Runtime: Node `v22.22.1`, npm `10.9.4`
OS: darwin
Relevant config: `loom-playbooks/package.json` scripts `smoke` and `pack:check`
External service / harness / data source when applicable: None

# Validity

Valid for: structural package discovery, npm dry-run packaging,
owner-boundary-pruned changed-surface scans for the 38 changed
`loom-playbooks/skills` files, tracked-diff added-line scans, removed-playbook
active-reference checks, and changed-file whitespace check in the observed source
state.

Fresh enough for: `ticket:plybk508` structural acceptance and critique review of
the current diff.

Recheck when: any `loom-playbooks` skill file, package script, package manifest,
or linked package-contract record changes after this evidence.

Invalidated by: new skill additions/removals, new runtime requirements, new
template additions, failed package smoke/dry-run on a later source state, or a
critique finding that shows the scans missed a relevant rejected surface.

Supersedes / superseded by: supersedes the stale first-pass structural observation
inside this same evidence record.

# Limitations

This evidence does not prove harness runtime install behavior beyond local
OpenCode package inspection. It does not prove the new playbook prose is clear,
non-overlapping, or sufficient; mandatory critique must review that. It does not
validate every existing template placeholder in `loom-playbooks`; broad hits in
pre-existing templates and anti-pattern prose were classified rather than removed
because they are not copied placeholder residue or imported peer runtime
requirements.

# Result

The package and structural checks passed for the owner-boundary-pruned peer
playbook integration source state. `open-loom-playbooks` discovered 22 playbook
skills and still did not preload core doctrine.

# Interpretation

The observations support structural readiness for critique and ticket acceptance
review. They do not by themselves close `ticket:plybk508` or satisfy the mandatory
critique gate.

# Related Records

- `ticket:plybk508`
- `spec:core-and-playbooks-package-contract`
- `research:peer-playbook-integration-candidates`
- `plan:split-core-and-playbooks-packages`
