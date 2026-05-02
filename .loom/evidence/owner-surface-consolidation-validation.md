---
id: evidence:owner-surface-consolidation-validation
kind: evidence
status: recorded
created_at: 2026-05-02T10:58:42Z
updated_at: 2026-05-02T11:05:58Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  tickets:
    - ticket:53cf2989
  packets:
    - packet:ralph-ticket-53cf2989-20260502T105317Z
  critique:
    - critique:owner-surface-consolidation-review
  plan:
    - plan:skills-corpus-protocol-sharpening
external_refs: {}
---

# Summary

Structural validation for owner-surface consolidation of atlas, retrospective,
spike/sketch, and skill metadata doctrine under `ticket:53cf2989`.

# Procedure

The parent reviewed the Ralph child output, manually inspected the product diff,
reconciled packet and ticket state to review, fixed oracle findings about
retrospective procedure relocation and support-layer metadata convention,
recorded final critique, closed the ticket, and ran targeted structural checks on
the resulting diff.

Commands and searches performed:

```text
git diff --check
git diff --stat
git diff --stat -- "skills/loom-wiki" "skills/loom-codemap" "skills/loom-retrospective" "skills/loom-records" "skills/loom-research" "skills/loom-spike" "skills/loom-skill-authoring"
rg -n "Atlas page shape is owned by|page-types\.md|atlas-page\.md|Codebase atlas page|Recommended sections" "skills/loom-wiki" "skills/loom-codemap"
rg -n "workflow mechanics|shared grammar|observe/distill/promote/prevent|not a new record kind|retrospective-only ledger|Routing Pointers" "skills/loom-retrospective" "skills/loom-records/references/retrospective.md"
rg -n "spike and sketch conclusions|spike or sketch produced|Spike And Sketch Variants|loom-spike|procedural spike|workflow detail|research owns conclusions" "skills/loom-research" "skills/loom-spike"
rg -n "skill_kind|compatibility|metadata\.owns_layer|owns_layer|frontmatter|activation description|workflow-coordinator|Markdown-native" "skills/loom-skill-authoring"
rg -n "observe -> distill -> promote -> prevent|behavior ambiguity|bad architectural choice|recurring operator confusion|support-only reminder|nothing durable to promote" "skills/loom-retrospective/SKILL.md" "skills/loom-records/references/retrospective.md"
rg -n "support-layer skills may also name|named non-canonical support layer|does not make the support layer canonical truth|metadata\.owns_layer|skill_kind: support-layer" "skills/loom-skill-authoring/references/structure.md" "skills/loom-memory/SKILL.md"
```

# Artifacts

Observed product files changed:

- `skills/loom-wiki/SKILL.md`
- `skills/loom-codemap/SKILL.md`
- `skills/loom-retrospective/SKILL.md`
- `skills/loom-records/references/retrospective.md`
- `skills/loom-research/SKILL.md`
- `skills/loom-research/references/research-shape.md`
- `skills/loom-research/templates/research.md`
- `skills/loom-skill-authoring/SKILL.md`
- `skills/loom-skill-authoring/references/structure.md`
- `skills/loom-skill-authoring/templates/simple-skill.md`
- `skills/loom-skill-authoring/templates/router-skill.md`

Observed outputs:

```text
git diff --check
-> no output

git diff --stat
-> 12 files changed, 154 insertions(+), 95 deletions(-)

git diff --stat -- <changed product surfaces>
-> 11 files changed, 113 insertions(+), 73 deletions(-)

rg atlas ownership terms
-> found codemap pointer to wiki page types/template and wiki-owned atlas shape

rg retrospective ownership terms
-> found retrospective workflow mechanics owned by loom-retrospective, records
   retrospective as shared grammar/routing pointers, and no retrospective-only ledger

rg spike/sketch split terms
-> found research-owned spike/sketch conclusions and null results with procedural
   detail delegated to loom-spike

rg skill metadata terms
-> found skill_kind, compatibility, metadata.owns_layer, frontmatter,
   activation-description, workflow-coordinator, and Markdown-native guidance in
   skill-authoring surfaces

rg retrospective procedure repair terms
-> found the observe/distill/promote/prevent loop and detailed prevention mapping
   in loom-retrospective, with records retaining shared grammar pointers

rg support-layer metadata convention terms
-> found structure guidance allowing support-layer skills to name a non-canonical
   support layer with metadata.owns_layer, and found loom-memory as the existing
   support-layer example
```

# Supports Claims

- `ticket:53cf2989` ACC-001
- `ticket:53cf2989` ACC-002
- `ticket:53cf2989` ACC-003
- `ticket:53cf2989` ACC-004
- `ticket:53cf2989` ACC-005
- `initiative:skills-corpus-protocol-sharpening#OBJ-004`
- `research:skills-corpus-council-review#CLAIM-008`

# Challenges Claims

None observed.

# Environment

Commit: `9b35c1fcd2e444a65dcf7732052d560d1ad6fb49` plus the current working-tree
diff for `ticket:53cf2989` before commit.

Branch: `main`

Runtime: OpenCode parent session with Ralph fixer subagent and oracle critique
subagent.

OS: darwin

Relevant config: repository has no automated test suite; validation is structural
and manual per `AGENTS.md`.

# Validity

Valid for: the working tree after `packet:ralph-ticket-53cf2989-20260502T105317Z`,
parent reconciliation to review, oracle FIND-001/FIND-002 repairs, final critique,
and ticket closure.

Recheck when: atlas page shape, codemap routing, retrospective mechanics,
research/spike/sketch split, or skill metadata conventions change.

# Limitations

This evidence validates structural presence and obvious duplicate removal in the
touched surfaces. It does not audit every example fixture or prove there are no
remaining duplicate concepts outside the ticket write boundary.

# Result

Atlas page shape is now wiki-owned with codemap pointing to it, retrospective
mechanics are owned by `loom-retrospective` with records retaining shared grammar,
spike/sketch truth is research-owned with procedure owned by `loom-spike`, and
skill metadata conventions are owned by `loom-skill-authoring`.

# Interpretation

The observations support acceptance of `ticket:53cf2989` only when combined with
critique and ticket-owned acceptance. Evidence does not itself close the ticket.

# Related Records

- `ticket:53cf2989`
- `packet:ralph-ticket-53cf2989-20260502T105317Z`
- `critique:owner-surface-consolidation-review`
- `plan:skills-corpus-protocol-sharpening`
