---
id: evidence:playbook-core-alignment-check
kind: evidence
status: recorded
created_at: 2026-05-08T05:13:28Z
updated_at: 2026-05-08T05:21:35Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  ticket:
    - ticket:pbalign8
  spec:
    - spec:core-and-playbooks-package-contract
external_refs: {}
---

# Summary

Observed structural and text-scan validation after aligning `loom-playbooks/skills`
with core Loom vocabulary and owner boundaries for `ticket:pbalign8`.

Evidence records observations only. Ticket acceptance owns whether these checks are
sufficient for closure.

# Procedure

Observed at: 2026-05-08T05:21:35Z

Source state: branch `main`, HEAD `035fecd81e6b09249b61bf71ef6cff2426e41ef2`, with
working-tree edits for `ticket:pbalign8` not yet committed.

Procedure:

- Ran `npm run pack:check` in `loom-playbooks/`.
- Ran `npm run smoke` in `loom-core/`.
- Ran `git diff --check -- loom-playbooks/skills .loom/tickets/20260508-pbalign8-align-playbooks-with-core.md`.
- Listed `loom-playbooks/skills/*/SKILL.md` with the workspace glob tool.
- Ran targeted playbook greps for noncanonical severity/disposition/status,
  workflow-as-owner, support-checkpoint, and removed-playbook vocabulary. Exact
  patterns and result counts are listed under `# Artifacts`.
- Ran three read-only subagent audits against `loom-playbooks/skills` and
  `loom-core/skills`; the last content audit found no remaining high-confidence
  content faults after patching, and a final structural audit found an empty
  orphan `loom-verification/` directory that was removed.

Expected result when applicable: package checks pass; playbooks report 22 skill
directories; no whitespace errors; targeted scan has no active noncanonical
guidance. Deliberate warning text may still mention peer or transport labels only
to say they are not core vocabulary.

Actual observed result: checks matched the expected result.

Procedure verdict / exit code: pass for package commands and diff check; targeted
scan results were reviewed semantically and found only intentional warning
examples, not active noncanonical definitions.

# Artifacts

- Final `npm run pack:check` in `loom-playbooks/` passed. The embedded smoke output
  reported `ok: true`, `doesNotPreloadCoreDoctrine: true`, `skillCount: 22`, and
  package dry-run `total files: 58`.
- `npm run smoke` in `loom-core/` passed. Output reported `ok: true`,
  `usingLoomReferenceCount: 8`, `instructionCount: 8`, and `skillCount: 15`.
- `git diff --check -- loom-playbooks/skills .loom/tickets/20260508-pbalign8-align-playbooks-with-core.md`
  produced no output, indicating no diff whitespace errors for the scoped files.
- The `loom-playbooks/skills/*/SKILL.md` glob returned 22 skill files and no
  `loom-verification` skill file.
- Targeted grep pattern 1:
  `support checkpoint facts|ship-owned|drive-owned|skills own the work|critique disposition that accepted|codemap/wiki|wiki/codemap|owner output.*spike|Route durable output.*spike|spike: experiment|open, accepted, or resolved|accepted/deferred|resolved, accepted`.
  Result: no files found under `loom-playbooks/skills`.
- Targeted grep pattern 2:
  `Critical|Important|Suggestion|Nit|FYI|done_with_concerns|needs_context`.
  Result: four matches under `loom-playbooks/skills`: two `loom-code-review/SKILL.md`
  lines explicitly saying peer labels are not core severity, and two
  `loom-agent-orchestration/references/worker-partition-and-review.md` lines
  explicitly saying `done_with_concerns` and `needs_context` are non-Ralph
  transport summaries that must be mapped back to owner truth.
- Earlier targeted grep pattern before the support-checkpoint fix:
  `Critical|Important|Suggestion|Nit|FYI|Severity: Important|accepted/deferred|resolved, accepted|open, accepted, or resolved|remain open, accepted|linked follow-up work|accepted as risk|accepted-risk note|bug report, or current implementation contract|ship-owned|drive-owned|skills own the work|codemap/wiki|wiki/codemap|codemap artifact|codemap explanation|owner output.*spike|Route durable output.*spike|spike: experiment`.
  Result after the second patch pass: only deliberate peer-label warning lines and
  stale `ship-owned` / `drive-owned` hits in `loom-ship/references/handoff-options.md`;
  those stale hits were subsequently patched and pattern 1 above returned no files.

# Raw Artifact Store

- Path: None - command outputs and scan summaries are small enough to summarize in
  this record.
- Captured artifacts: None.
- Key excerpts / index: exact targeted scan patterns and result counts are listed
  in `# Artifacts`.
- Redaction / sensitivity: no secrets or sensitive data observed in these outputs.
- Retention / tracking: this evidence record is the retained artifact.

# Visual / Product Evidence

N/A.

- Baseline artifact: N/A
- After artifact: N/A
- Viewport / environment: N/A
- Primary user task checked: N/A
- What improved: N/A
- What still looks weak: N/A
- What this evidence does not prove: does not prove long-term operator clarity in
  real projects.

# Supports Claims

- Supports `ticket:pbalign8#ACC-001` by showing the known noncanonical critique
  labels and finding disposition vocabulary were replaced or explicitly framed as
  noncanonical warning examples; pattern 2 preserves the exact remaining peer-label
  mentions.
- Supports `ticket:pbalign8#ACC-002` by showing remaining `done_with_concerns` /
  `needs_context` mentions are explicit non-Ralph transport-label warnings, not
  active child status definitions.
- Supports `ticket:pbalign8#ACC-003` by showing pattern 1 found no active guidance
  treating `spike`, `codemap`, `ship`, `drive`, support checkpoint facts, bug
  reports, current implementation, or generic gate words as core owners or
  interchangeable statuses after the final fixes.
- Supports `spec:core-and-playbooks-package-contract#REQ-004`, `REQ-005`, and
  `REQ-008` for the edited playbook surface by preserving 22 optional playbooks,
  no core doctrine preload in playbooks, and playbook routing back to core owners.

# Challenges Claims

None observed.

# Environment

Commit: `035fecd81e6b09249b61bf71ef6cff2426e41ef2`

Branch: `main`

Runtime: Node/npm via package scripts.

OS: macOS / Darwin.

Relevant config: `loom-core/package.json`, `loom-playbooks/package.json`, and the
current `loom-core/skills` / `loom-playbooks/skills` source trees.

External service / harness / data source when applicable: none.

# Validity

Valid for: the current working-tree source state of the edited playbook corpus and
the package smoke/dry-run checks listed above.

Fresh enough for: `ticket:pbalign8` review and acceptance, subject to ticket-owned
judgment.

Recheck when: `loom-playbooks/skills`, package manifests, core vocabulary, or the
ticket scope changes materially.

Invalidated by: new playbook edits that reintroduce noncanonical severity,
disposition, outcome, owner-layer, or gate vocabulary; package membership changes;
or package script changes.

Supersedes / superseded by: None.

# Limitations

- Smoke and dry-run package checks validate package shape, not semantic quality by
  themselves.
- Targeted grep can miss semantically wrong wording that uses different terms.
- Subagent audits are review evidence, not a replacement for ticket-owned
  acceptance.
- Real operator clarity remains empirical and may need future tightening.

# Result

The edited playbook corpus passed package shape checks, retained 22 playbook skill
entries, removed the empty orphan `loom-verification` directory, and no remaining
high-confidence core-alignment faults were observed by the final audit pass.

# Interpretation

The evidence supports that this alignment pass removed the known hard conflicts
between `loom-playbooks` guidance and core Loom grammar. It does not prove that no
future reader will find softer overlap, ambiguity, or wording that could be
tightened later.

# Related Records

- ticket:pbalign8
- spec:core-and-playbooks-package-contract
- research:peer-playbook-integration-candidates
