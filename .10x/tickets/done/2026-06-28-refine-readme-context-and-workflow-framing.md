Status: done
Created: 2026-06-28
Updated: 2026-06-28
Depends-On: README.md, .10x/research/2026-06-28-10x-superpowers-comparison.md, .10x/tickets/done/2026-06-28-polish-readme-for-public-launch.md

# Refine README Context And Workflow Framing

## Scope

Apply focused README refinements from the user's post-polish review.

Included:

- Replace "project memory" framing with "project context" where appropriate.
- Rephrase the subagent workflow failure mode around opaque handoffs and missing
  intermediate reasoning/checkpoints/validation.
- Replace the thin decision-record example with a richer 10x-style record that
  demonstrates authority, provenance, limits, evidence, and follow-up ownership.
- Remove the RAG/vector/context-window section unless a more relevant framing is
  needed.
- Reframe the current-workflow section around augmenting existing AI coding
  workflows, including skill packs such as Superpowers, without making a direct
  comparison section.
- Lightly strengthen the autoresearch section as a novel evaluation/scientific
  environment without overclaiming.

Excluded:

- Changes to `SKILL.md`.
- Changes to autoresearch tooling.
- Direct competitive comparison section against Superpowers.

## Acceptance Criteria

- AC-001: README no longer uses "project memory" for the `.10x/` substrate.
- AC-002: The subagent row names black-box opacity more precisely.
- AC-003: The record example sells rich typed context rather than a thin ADR.
- AC-004: The RAG/vector section is removed.
- AC-005: The workflow section explains how 10x enhances existing tools.
- AC-006: The Superpowers comparison informs copy without becoming a direct
  comparison section.
- AC-007: README links and basic validation checks pass.

## Progress And Notes

- 2026-06-28: Opened from user review after the public-launch README polish
  commit.
- 2026-06-28: Updated `README.md` terminology, subagent row, rich record
  example, autoresearch paragraph, workflow augmentation table, Superpowers FAQ
  wording, and removed the RAG/vector section. Evidence:
  `.10x/evidence/2026-06-28-readme-context-workflow-refinement.md`. Review:
  `.10x/reviews/2026-06-28-readme-context-workflow-refinement.md`.

## Blockers

None.

## References

- `README.md`
- `.10x/research/2026-06-28-10x-superpowers-comparison.md`
- `.10x/tickets/done/2026-06-28-polish-readme-for-public-launch.md`
