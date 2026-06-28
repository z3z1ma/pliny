# 10x Autoresearch Trial Report

Source: `.10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/v2-external-index`

## Summary

| Field | Value |
| --- | --- |
| experiment_id | EXP-20260628-s010-v2-external-index |
| mode | live |
| raw_artifacts | 4 |
| live_subject_calls | 4 |
| summary | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/v2-external-index/summary.json |
| plan | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/v2-external-index/plan.json |
| raw_output_dir | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/v2-external-index/raw |
| workspace_dir | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/v2-external-index/workspaces |
| prompt_dir | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/v2-external-index/prompts |
| harness_artifact_dir | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/v2-external-index/codex |

## Scientific Contract

| Field | Value |
| --- | --- |
| question | Does the compact cold-start record handoff candidate improve external canonical PRD indexing versus current 10x? |
| hypothesis | The compact candidate should preserve external PRD authority, behavior, limits, and next action with less record spread than first-batch broad candidates. |
| expected_behavior | Subject creates durable 10x records from the approved Nimbus Retention Controls Google Doc PRD without implementation edits. |
| inspection_criteria | Records identify the external Google Doc PRD as canonical or explicitly say local records are canonical if copied., Records preserve status, revision, owner, URL/document ID, behavior scope, exclusions, acceptance scenarios, rollout/open-question status, limits, and next action., Records avoid implementation edits, placeholder spread, missing source/provenance, and invented implementation names., Score S010 against cold-start completeness, provenance, edge cases, actionability, cross-record coherence, and economy. |
| quality_floor | Any wrong authority, implementation edit, missing PRD provenance, or future need to rediscover the PRD status and scope caps the candidate. |
| verdict_record_path | .10x/evidence/2026-06-28-record-richness-hypothesis-batch.md |

## Artifact Inspection Checklist

Presence only; the scientist still judges whether each artifact supports the claim.

| Artifact class | Status |
| --- | --- |
| summary.json | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/v2-external-index/summary.json |
| plan.json | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/v2-external-index/plan.json |
| canonical_guard.json | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/v2-external-index/canonical_guard.json |
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
| sha256-12a9c24b4924bba5ad115ec6f6f671acddd2e267e9e83b258e8c6ebb1ca00161.json | SCN-004 | current-10x | 1 | codex-developer-instructions | 0 | False | 1 | 84.59 | in=276182; out=3237 | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/v2-external-index/workspaces/sha256-12a9c24b4924bba5ad115ec6f6f671acddd2e267e9e83b258e8c6ebb1ca00161 | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/v2-external-index/workspaces/sha256-12a9c24b4924bba5ad115ec6f6f671acddd2e267e9e83b258e8c6ebb1ca00161/workspace-manifest.json |
| sha256-451b650ef886fa0da9850ac941200d9ff9194502d0ba369e845f943c1e72a5b5.json | SCN-004 | candidate-cold-start-record-handoff-check | 1 | codex-developer-instructions | 0 | False | 1 | 179.17 | in=273594; out=8178 | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/v2-external-index/workspaces/sha256-451b650ef886fa0da9850ac941200d9ff9194502d0ba369e845f943c1e72a5b5 | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/v2-external-index/workspaces/sha256-451b650ef886fa0da9850ac941200d9ff9194502d0ba369e845f943c1e72a5b5/workspace-manifest.json |
| sha256-48272e414ca556126cbf67584abf9b5c061388bc63f9a29d7858705ba3ba7865.json | SCN-004 | current-10x | 0 | codex-developer-instructions | 0 | False | 1 | 98.75 | in=173575; out=4411 | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/v2-external-index/workspaces/sha256-48272e414ca556126cbf67584abf9b5c061388bc63f9a29d7858705ba3ba7865 | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/v2-external-index/workspaces/sha256-48272e414ca556126cbf67584abf9b5c061388bc63f9a29d7858705ba3ba7865/workspace-manifest.json |
| sha256-c6500c686ea559f87d7b93fa73ad91c7e65eae621d936147fad5d31fc5ba13f0.json | SCN-004 | candidate-cold-start-record-handoff-check | 0 | codex-developer-instructions | 0 | False | 1 | 162.96 | in=253504; out=6940 | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/v2-external-index/workspaces/sha256-c6500c686ea559f87d7b93fa73ad91c7e65eae621d936147fad5d31fc5ba13f0 | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/v2-external-index/workspaces/sha256-c6500c686ea559f87d7b93fa73ad91c7e65eae621d936147fad5d31fc5ba13f0/workspace-manifest.json |

## Workspace And Tool Trace

| Artifact | Changed files | Suppressed changed files | Tool events | Raw references | Last assistant message |
| --- | --- | --- | --- | --- | --- |
| sha256-12a9c24b4924bba5ad115ec6f6f671acddd2e267e9e83b258e8c6ebb1ca00161.json | .10x/specs/nimbus-retention-controls-prd.md, .10x/tickets/2026-06-28-nimbus-retention-controls-planning.md | none | 8 | 9 | Created the durable 10x records:<br><br>- [nimbus-retention-controls-prd.md](/mnt/c/Users/butle/AppData/Local/Temp/10x-autoresearch-jetevw1v/workspace/.10x/specs/n... |
| sha256-451b650ef886fa0da9850ac941200d9ff9194502d0ba369e845f943c1e72a5b5.json | .10x/evidence/2026-06-28-nimbus-retention-prd-inspection.md, .10x/specs/nimbus-retention-audit-log.md, .10x/specs/nimbus-retention-controls-canonical-prd.md, .10x/specs/nimbus-retention-enforcement.md, .10x/specs/nimbus-retention-rollout.md, .10x/specs/nimbus-retention-settings-access.md, .10x/tickets/2026-06-28-implement-nimbus-retention-audit-log.md, .10x/tickets/2026-06-28-implement-nimbus-retention-enforcement.md, .10x/tickets/2026-06-28-implement-nimbus-retention-settings-access.md, .10x/tickets/2026-06-28-nimbus-retention-controls-implementation-plan.md, .10x/tickets/2026-06-28-prepare-nimbus-retention-rollout.md | none | 15 | 9 | Created the durable 10x planning graph from the approved Nimbus Retention Controls PRD. No code was implemented.<br><br>Added:<br><br>- `.10x/specs/nimbus-retention-cont... |
| sha256-48272e414ca556126cbf67584abf9b5c061388bc63f9a29d7858705ba3ba7865.json | .10x/evidence/2026-06-28-nimbus-retention-prd-export.md, .10x/specs/nimbus-retention-controls.md, .10x/tickets/2026-06-28-nimbus-retention-controls-planning.md | none | 11 | 9 | Created the durable 10x records from the approved PRD, with no code changes:<br><br>- [nimbus-retention-controls.md](/mnt/c/Users/butle/AppData/Local/Temp/10x-auto... |
| sha256-c6500c686ea559f87d7b93fa73ad91c7e65eae621d936147fad5d31fc5ba13f0.json | .10x/evidence/2026-06-28-nimbus-retention-prd-export.md, .10x/specs/nimbus-retention-controls.md, .10x/tickets/2026-06-28-nimbus-retention-audit-log.md, .10x/tickets/2026-06-28-nimbus-retention-controls-plan.md, .10x/tickets/2026-06-28-nimbus-retention-data-permissions.md, .10x/tickets/2026-06-28-nimbus-retention-nightly-enforcement.md, .10x/tickets/2026-06-28-nimbus-retention-rollout.md, .10x/tickets/2026-06-28-nimbus-retention-settings-surface.md | none | 12 | 9 | Created the durable 10x planning graph from the approved PRD. No product code was implemented.<br><br>Records added:<br><br>- [Nimbus Retention Controls spec index](/mnt... |

## Scientist Inspection

This report does not grade, aggregate, or promote a candidate.

Inspect the raw transcript, command artifacts, workspace manifest, changed files, and expected behavior for each scenario. Record rubric judgments, verdicts, limits, and any promotion or rejection rationale in durable `.10x/research/`, `.10x/evidence/`, or `.10x/reviews/` records.

## Report Limits

- This report is a secondary view over saved trial artifacts.
- Unknown means the field was absent, null, or not numeric in the loaded artifact.
- The runner does not replace the LLM researcher's rubric inspection.
