# 10x Autoresearch Trial Report

Source: `.10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/v2-retrospective-learning`

## Summary

| Field | Value |
| --- | --- |
| experiment_id | EXP-20260628-s010-v2-retrospective-learning |
| mode | live |
| raw_artifacts | 4 |
| live_subject_calls | 4 |
| summary | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/v2-retrospective-learning/summary.json |
| plan | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/v2-retrospective-learning/plan.json |
| raw_output_dir | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/v2-retrospective-learning/raw |
| workspace_dir | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/v2-retrospective-learning/workspaces |
| prompt_dir | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/v2-retrospective-learning/prompts |
| harness_artifact_dir | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/v2-retrospective-learning/codex |

## Scientific Contract

| Field | Value |
| --- | --- |
| question | Does the compact cold-start record handoff candidate improve retrospective learning extraction versus current 10x? |
| hypothesis | The compact candidate should preserve procedure, vocabulary, follow-up risk, closure evidence, and noise filtering with fewer added characters than source-delta. |
| expected_behavior | Subject routes settlement reconciliation procedure learning, vocabulary, and FX follow-up risk into appropriate durable records; does not preserve local alias/laptop/log-style noise; does not change source. |
| inspection_criteria | Durable operational procedure becomes a skill or suitable procedural record with enough triggers, limits, and validation detail., Stable vocabulary becomes knowledge with examples/limits., Historical FX rounding gap gets a bounded follow-up owner with blockers if semantics are unratified., One-off local shell alias, laptop load, and personal log preference are not durable records., Child/parent closure status remains coherent with retrospective obligations. |
| quality_floor | Chat-only durable learning, untracked FX follow-up, noisy knowledge/skill records, source edits, or unsupported parent closure make the candidate non-promotable. |
| verdict_record_path | .10x/evidence/2026-06-28-record-richness-hypothesis-batch.md |

## Artifact Inspection Checklist

Presence only; the scientist still judges whether each artifact supports the claim.

| Artifact class | Status |
| --- | --- |
| summary.json | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/v2-retrospective-learning/summary.json |
| plan.json | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/v2-retrospective-learning/plan.json |
| canonical_guard.json | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/v2-retrospective-learning/canonical_guard.json |
| raw trial artifacts | 4 found |
| codex command metadata | 4 found |
| codex stdout JSONL | 4 found |
| codex stderr | 4 found |
| codex last assistant messages | 4 found |
| prompts | 4 found |
| instruction artifacts | 4 found |
| workspace manifests | 4 found |
| archived workspaces | 4 found |

## Trial Artifacts

| Artifact | Scenario | Arm | Rep | Instruction delivery | Command exits | Timed out | Turns | Wall seconds | Tokens | Archived workspace | Workspace manifest |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| sha256-219535f1006d58b744f5b3c47aa4f194eeea1ae10352517e5460bce7d3861909.json | SCN-012 | current-10x | 1 | codex-developer-instructions | 0 | False | 1 | 260.02 | in=576018; out=10656 | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/v2-retrospective-learning/workspaces/sha256-219535f1006d58b744f5b3c47aa4f194eeea1ae10352517e5460bce7d3861909 | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/v2-retrospective-learning/workspaces/sha256-219535f1006d58b744f5b3c47aa4f194eeea1ae10352517e5460bce7d3861909/workspace-manifest.json |
| sha256-2bc34249f7c9311ae1a6a5d98a72758bae041b8d550b7198fcddf8ffb8cf2b0f.json | SCN-012 | current-10x | 0 | codex-developer-instructions | 0 | False | 1 | 192.34 | in=462246; out=8513 | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/v2-retrospective-learning/workspaces/sha256-2bc34249f7c9311ae1a6a5d98a72758bae041b8d550b7198fcddf8ffb8cf2b0f | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/v2-retrospective-learning/workspaces/sha256-2bc34249f7c9311ae1a6a5d98a72758bae041b8d550b7198fcddf8ffb8cf2b0f/workspace-manifest.json |
| sha256-4f96036cf4487f2f66297700773823e21d8d749e63010720abcca7c631c922eb.json | SCN-012 | candidate-cold-start-record-handoff-check | 1 | codex-developer-instructions | 0 | False | 1 | 182.81 | in=632502; out=6918 | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/v2-retrospective-learning/workspaces/sha256-4f96036cf4487f2f66297700773823e21d8d749e63010720abcca7c631c922eb | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/v2-retrospective-learning/workspaces/sha256-4f96036cf4487f2f66297700773823e21d8d749e63010720abcca7c631c922eb/workspace-manifest.json |
| sha256-99aefcb32a3f79d2895a8ef1aa98abaeb106ae9f9707d3f1c227b32107067ce7.json | SCN-012 | candidate-cold-start-record-handoff-check | 0 | codex-developer-instructions | 0 | False | 1 | 185.37 | in=553415; out=7782 | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/v2-retrospective-learning/workspaces/sha256-99aefcb32a3f79d2895a8ef1aa98abaeb106ae9f9707d3f1c227b32107067ce7 | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/v2-retrospective-learning/workspaces/sha256-99aefcb32a3f79d2895a8ef1aa98abaeb106ae9f9707d3f1c227b32107067ce7/workspace-manifest.json |

## Workspace And Tool Trace

| Artifact | Changed files | Suppressed changed files | Tool events | Raw references | Last assistant message |
| --- | --- | --- | --- | --- | --- |
| sha256-219535f1006d58b744f5b3c47aa4f194eeea1ae10352517e5460bce7d3861909.json | .10x/evidence/2026-06-25-settlement-reconciliation-child-test-output.md, .10x/evidence/2026-06-28-settlement-reconciliation-parent-closure-check.md, .10x/knowledge/settlement-reconciliation-vocabulary.md, .10x/reviews/2026-06-25-settlement-reconciliation-child-review.md, .10x/skills/test-settlement-mismatches/SKILL.md, .10x/tickets/2026-06-28-cover-historical-fx-rounding-tolerance.md, .10x/tickets/done/2026-06-25-add-settlement-reconciliation-preview.md, .10x/tickets/done/2026-06-25-settlement-reconciliation-parent.md, .claude/skills/test-settlement-mismatches/SKILL.md | none | 37 | 9 | Performed the settlement reconciliation parent closure check and extracted the retrospective learning into durable records only.<br><br>Changed records:<br>- Added sk... |
| sha256-2bc34249f7c9311ae1a6a5d98a72758bae041b8d550b7198fcddf8ffb8cf2b0f.json | .10x/evidence/2026-06-25-settlement-reconciliation-child-test-output.md, .10x/knowledge/settlement-reconciliation-vocabulary.md, .10x/reviews/2026-06-25-settlement-reconciliation-child-review.md, .10x/skills/settlement-reconciliation-testing/SKILL.md, .10x/tickets/2026-06-28-add-historical-fx-rounding-tolerance-coverage.md, .10x/tickets/2026-06-28-mirror-settlement-reconciliation-skill.md, .10x/tickets/done/2026-06-25-add-settlement-reconciliation-preview.md, .10x/tickets/done/2026-06-25-settlement-reconciliation-parent.md | none | 31 | 9 | Completed the parent closure check and retrospective extraction. No source code was changed.<br><br>Closed:<br>- [parent ticket](/mnt/c/Users/butle/AppData/Local/Temp... |
| sha256-4f96036cf4487f2f66297700773823e21d8d749e63010720abcca7c631c922eb.json | .10x/evidence/2026-06-25-settlement-reconciliation-child-test-output.md, .10x/knowledge/settlement-reconciliation-vocabulary.md, .10x/reviews/2026-06-25-settlement-reconciliation-child-review.md, .10x/reviews/2026-06-28-settlement-reconciliation-parent-closure-check.md, .10x/skills/settlement-reconciliation-testing/SKILL.md, .10x/tickets/2026-06-28-define-historical-fx-rounding-tolerance-coverage.md, .10x/tickets/done/2026-06-25-add-settlement-reconciliation-preview.md, .10x/tickets/done/2026-06-25-settlement-reconciliation-parent.md, .claude/skills/settlement-reconciliation-testing/SKILL.md | none | 31 | 9 | Performed the parent closure check and extracted the retrospective learning without touching source code.<br><br>Closed records:<br>- [parent ticket](/mnt/c/Users/but... |
| sha256-99aefcb32a3f79d2895a8ef1aa98abaeb106ae9f9707d3f1c227b32107067ce7.json | .10x/evidence/2026-06-25-settlement-reconciliation-child-test-output.md, .10x/knowledge/settlement-reconciliation-vocabulary.md, .10x/reviews/2026-06-25-settlement-reconciliation-child-review.md, .10x/skills/settlement-mismatch-tests/SKILL.md, .10x/tickets/2026-06-28-historical-fx-rounding-tolerance-coverage.md, .10x/tickets/done/2026-06-25-add-settlement-reconciliation-preview.md, .10x/tickets/done/2026-06-25-settlement-reconciliation-parent.md, .claude/skills/settlement-mismatch-tests/SKILL.md | none | 35 | 9 | Parent closure check is complete. I closed both settlement reconciliation tickets by moving them to `.10x/tickets/done/` and updated evidence/review referenc... |

## Scientist Inspection

This report does not grade, aggregate, or promote a candidate.

Inspect the raw transcript, command artifacts, workspace manifest, changed files, and expected behavior for each scenario. Record rubric judgments, verdicts, limits, and any promotion or rejection rationale in durable `.10x/research/`, `.10x/evidence/`, or `.10x/reviews/` records.

## Report Limits

- This report is a secondary view over saved trial artifacts.
- Unknown means the field was absent, null, or not numeric in the loaded artifact.
- The runner does not replace the LLM researcher's rubric inspection.
