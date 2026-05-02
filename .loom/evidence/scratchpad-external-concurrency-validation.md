---
id: evidence:scratchpad-external-concurrency-validation
kind: evidence
status: recorded
created_at: 2026-05-02T10:34:20Z
updated_at: 2026-05-02T10:41:26Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  tickets:
    - ticket:233cfdeb
  packets:
    - packet:ralph-ticket-233cfdeb-20260502T102943Z
  critique:
    - critique:scratchpad-external-concurrency-review
  plan:
    - plan:skills-corpus-protocol-sharpening
external_refs: {}
---

# Summary

Structural validation for scratchpad avoidance, external-reference lifecycle, and
file-first concurrency guidance added under `ticket:233cfdeb`.

# Procedure

The parent reviewed the Ralph child output, manually inspected the product diff,
reconciled packet and ticket state to review, fixed oracle FIND-001 by routing
critique-like scratchpad material to critique, recorded final critique, closed
the ticket, and ran targeted structural checks on the resulting diff.

Commands and searches performed:

```text
git diff --check
git diff --stat
git diff --stat -- "skills/loom-workspace/references/status-snapshot.md" "skills/loom-records/references/frontmatter.md" "skills/loom-records/references/semantic-link-usage.md" "skills/loom-records/references/repair-and-drift.md" "skills/loom-git/references/worktree-discipline.md"
git diff --name-status -- "skills"
rg -n "scratchpad|scratch\.md|notes\.md|junk-drawer|owner layer|support-only recall|adversarial findings|residual risks" "skills/loom-workspace/references/status-snapshot.md"
rg -n "external_refs|external reference|request|mirror|package|navigate|issue tracker|pull request|dashboard|generated context|harness artifact|release" "skills/loom-records/references/frontmatter.md" "skills/loom-records/references/semantic-link-usage.md"
rg -ni "re-read|preserve unrelated|fail closed|overlap|stale source|ambiguous dirty|concurrent|concurrency" "skills/loom-git/references/worktree-discipline.md"
rg -ni "latest-file-wins|latest file wins|newest timestamp|most recent file|owner layer|stale or contradictory" "skills/loom-records/references/repair-and-drift.md"
rg -ni "lockfile|daemon|helper script|generated index|scratchpad record kind|coordination service" "skills/loom-records" "skills/loom-workspace" "skills/loom-git" "skills/loom-evidence" "skills/loom-research" "skills/loom-tickets" "skills/loom-memory"
```

# Artifacts

Observed product files changed:

- `skills/loom-workspace/references/status-snapshot.md`
- `skills/loom-records/references/frontmatter.md`
- `skills/loom-records/references/semantic-link-usage.md`
- `skills/loom-records/references/repair-and-drift.md`
- `skills/loom-git/references/worktree-discipline.md`

Observed outputs:

```text
git diff --check
-> no output

git diff --stat
-> 6 files changed, 111 insertions(+), 30 deletions(-)

git diff --stat -- "skills/loom-workspace/references/status-snapshot.md" "skills/loom-records/references/frontmatter.md" "skills/loom-records/references/semantic-link-usage.md" "skills/loom-records/references/repair-and-drift.md" "skills/loom-git/references/worktree-discipline.md"
-> 5 files changed, 71 insertions(+), 8 deletions(-)

git diff --name-status -- "skills"
-> modified only allowed skill files under loom-workspace, loom-records, and loom-git

rg -n "scratchpad|scratch\.md|notes\.md|junk-drawer|owner layer|support-only recall|adversarial findings|residual risks" "skills/loom-workspace/references/status-snapshot.md"
-> found generic scratchpad/junk-drawer warning, owner-layer alternatives, and critique routing for adversarial findings/residual risks

rg -n "external_refs|external reference|request|mirror|package|navigate|issue tracker|pull request|dashboard|generated context|harness artifact|release" "skills/loom-records/references/frontmatter.md" "skills/loom-records/references/semantic-link-usage.md"
-> found request, mirror, package, navigate, issue tracker, PR, URL, dashboard,
   generated context, harness artifact, package, and release surface guidance

rg -ni "re-read|preserve unrelated|fail closed|overlap|stale source|ambiguous dirty|concurrent|concurrency" "skills/loom-git/references/worktree-discipline.md"
-> found re-read, preserve unrelated edits, fail closed, overlap, stale source,
   and ambiguous dirty-state guidance

rg -ni "latest-file-wins|latest file wins|newest timestamp|most recent file|owner layer|stale or contradictory" "skills/loom-records/references/repair-and-drift.md"
-> found stale/contradictory record routing and rejection of latest-file-wins semantics

rg -ni "lockfile|daemon|helper script|generated index|scratchpad record kind|coordination service" "skills/loom-records" "skills/loom-workspace" "skills/loom-git" "skills/loom-evidence" "skills/loom-research" "skills/loom-tickets" "skills/loom-memory"
-> found only existing lockfile/helper-script discussion in Git/validation references;
   no new required lock, daemon, helper, generated index, or scratchpad record kind
   was introduced
```

# Supports Claims

- `ticket:233cfdeb` ACC-001
- `ticket:233cfdeb` ACC-002
- `ticket:233cfdeb` ACC-003
- `ticket:233cfdeb` ACC-004
- `ticket:233cfdeb` ACC-005
- `initiative:skills-corpus-protocol-sharpening#OBJ-003`
- `research:skills-corpus-council-review#CLAIM-007`

# Challenges Claims

None observed.

# Environment

Commit: `ed612a2df0b51b329ced496031422b86d9030bf1` plus the current working-tree
diff for `ticket:233cfdeb` before commit.

Branch: `main`

Runtime: OpenCode parent session with Ralph fixer subagent and oracle critique
subagent.

OS: darwin

Relevant config: repository has no automated test suite; validation is structural
and manual per `AGENTS.md`.

# Validity

Valid for: the working tree after `packet:ralph-ticket-233cfdeb-20260502T102943Z`,
parent reconciliation to review, oracle FIND-001/FIND-002 repairs, final critique,
and ticket closure.

Recheck when: scratchpad routing, external-reference ownership, file-first
concurrency, or stale-record repair guidance changes.

# Limitations

This evidence validates structural presence and consistency of the guardrail
guidance. It does not prove operator behavior in a real concurrent editing
incident, and it does not replace oracle critique.

# Result

The corpus now warns against generic scratchpads, routes scratchpad-like material
to existing owner layers, frames external references as support surfaces, teaches
file-first re-read and fail-closed concurrency behavior, and rejects latest-file
wins as a record reconciliation model.

# Interpretation

The observations support acceptance of `ticket:233cfdeb` only when combined with
critique and ticket-owned acceptance. Evidence does not itself close the ticket.

# Related Records

- `ticket:233cfdeb`
- `packet:ralph-ticket-233cfdeb-20260502T102943Z`
- `critique:scratchpad-external-concurrency-review`
- `plan:skills-corpus-protocol-sharpening`
