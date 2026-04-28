---
id: evidence:superpowers-workflow-adaptation-validation
kind: evidence
status: recorded
created_at: 2026-04-28T07:58:23Z
updated_at: 2026-04-28T08:05:59Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  tickets:
    - ticket:k7p4s2q9
  research:
    - research:superpowers-skill-workflow-adaptation
  critique:
    - critique:superpowers-workflow-adaptation-review
external_refs:
  github:
    - https://github.com/obra/superpowers/tree/main/skills
---

# Summary

Validation evidence for adapting Superpowers workflow disciplines into existing Loom skills without creating a parallel Superpowers namespace or new owner layers.

# Procedure

1. Cloned Superpowers into `/tmp/loom-superpowers.vDNOwa` with `git clone --depth 1 https://github.com/obra/superpowers.git`.
2. Read `README.md`, `.loom/constitution/constitution.md`, relevant constitutional decisions, and the current Loom skill corpus under `skills/`.
3. Read every meaningful Superpowers skill under `/tmp/loom-superpowers.vDNOwa/skills`, including adjacent prompts and references for planning, review, subagent execution, debugging, TDD, worktrees, verification, and skill authoring.
4. Recorded the adaptation matrix in `research:superpowers-skill-workflow-adaptation`.
5. Updated existing Loom skills and references to carry the adapted workflows through Loom layers.
6. Ran structural validation commands.

# Artifacts

- Superpowers clone path: `/tmp/loom-superpowers.vDNOwa`
- Superpowers commit inspected: `6efe32c9e2dd002d0c394e861e0529675d1ab32e`
- Superpowers top-level skills inspected:
  - `brainstorming`
  - `dispatching-parallel-agents`
  - `executing-plans`
  - `finishing-a-development-branch`
  - `receiving-code-review`
  - `requesting-code-review`
  - `subagent-driven-development`
  - `systematic-debugging`
  - `test-driven-development`
  - `using-git-worktrees`
  - `using-superpowers`
  - `verification-before-completion`
  - `writing-plans`
  - `writing-skills`
- Current commit before this work: `f7c941e2c14f26464497f5161e5da853befaedd4`
- Current branch: `main`
- `git diff --check`: no output, indicating no whitespace errors in tracked diff.
- `node "open-loom.mjs" --smoke` output:

```json
{
  "ok": true,
  "pluginId": "open-loom",
  "bootstrapReferenceCount": 7,
  "firstBootstrapReference": "skills/loom-bootstrap/references/01-core-identity.md",
  "lastBootstrapReference": "skills/loom-bootstrap/references/07-validation-and-honesty.md",
  "instructionCount": 7,
  "instructionsAreDeduped": true,
  "skillCount": 21,
  "skillPath": "/Users/alexanderbutler/code_projects/personal/agent-loom/skills",
  "bootstrapResult": "registered through config.instructions as ordered bootstrap references",
  "skillsResult": "registered through config.skills.paths"
}
```

- `grep` equivalent via tool search for `^name:|^description:` under `skills/*/SKILL.md`: 42 matches, two metadata lines for each of 21 skills.
- Tool search for new reference/read-order terms found the expected surfaces:
  - `skills/loom-debugging/SKILL.md` -> `references/systematic-debugging.md`
  - `skills/loom-ship/SKILL.md` -> `references/handoff-options.md`
  - `skills/loom-skill-authoring/SKILL.md` -> `references/skill-review.md`
  - `skills/loom-critique/references/critique-lens.md` -> `workflow-boundary` and `product-surface`
- Tool search for imported Superpowers product-surface strings under `skills/` found no files for `superpowers:`, `docs/superpowers`, `.superpowers`, `find-polluter`, `render-graphs`, or `start-server.sh`.
- Tool search for trailing whitespace in new reference directories and `.loom` records found no files.
- Tool search for `ticket:k7p4s2q9` and `research:superpowers-skill-workflow-adaptation` under `.loom` found bidirectional references between ticket and research.
- After critique fixes, `git diff --check` was rerun and remained clean.
- After critique fixes, `node "open-loom.mjs" --smoke` was rerun and still reported `ok: true`, seven bootstrap references, and 21 skills.

# Supports Claims

- ticket:k7p4s2q9/adapt-superpowers-skills
- ticket:k7p4s2q9/loom-layer-ownership-preserved
- ticket:k7p4s2q9/public-skill-surface-structurally-valid

# Challenges Claims

None.

# Environment

Commit: f7c941e2c14f26464497f5161e5da853befaedd4
Branch: main
Runtime: Node via `node open-loom.mjs --smoke`
OS: darwin
Relevant config: local repository checkout with uncommitted protocol edits

# Validity

Valid for: structural state of the working tree at 2026-04-28T08:05:59Z after the Superpowers adaptation edits and critique fixes, and for Superpowers commit `6efe32c9e2dd002d0c394e861e0529675d1ab32e`.
Recheck when: skill files, bootstrap references, OpenCode plugin registration, or public workflow maps change.

# Limitations

- This evidence does not prove every workflow instruction will produce ideal operator behavior in a live model session.
- This evidence does not include an external harness install test beyond the local OpenCode smoke check.
- This evidence does not prove future live-session behavior; it records observed structural validation and source inspection.

# Result

The structural checks passed. The OpenCode smoke check still reports seven bootstrap references and 21 canonical skills. No direct Superpowers namespace, helper runtime, or product-surface path was imported into `skills/`.

# Interpretation

The evidence supports the claim that the adaptation preserved Loom's skills-only surface and integrated the workflows into existing Loom skill owners structurally. Behavioral quality still requires critique and future real-work use.

# Related Records

- `ticket:k7p4s2q9`
- `research:superpowers-skill-workflow-adaptation`
- `critique:superpowers-workflow-adaptation-review`
