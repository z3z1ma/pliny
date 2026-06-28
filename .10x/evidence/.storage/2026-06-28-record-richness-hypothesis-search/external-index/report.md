# 10x Autoresearch Trial Report

Source: `.10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/external-index`

## Summary

| Field | Value |
| --- | --- |
| experiment_id | EXP-20260628-s010-external-index |
| mode | live |
| raw_artifacts | 6 |
| live_subject_calls | 6 |
| summary | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/external-index/summary.json |
| plan | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/external-index/plan.json |
| raw_output_dir | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/external-index/raw |
| workspace_dir | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/external-index/workspaces |
| prompt_dir | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/external-index/prompts |
| harness_artifact_dir | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/external-index/codex |

## Scientific Contract

| Field | Value |
| --- | --- |
| question | Which S010 candidate best preserves rich cold-start context when indexing an approved external canonical PRD? |
| hypothesis | Source-material-delta and record-regeneration candidates should create the richest external-canonical index without copying the full PRD, while economy-density should avoid unnecessary record spread. |
| expected_behavior | Subject creates the minimum appropriate .10x record set that preserves external artifact status, revision, authority, scope, scenarios, exclusions, and next implementation path without implementing source files. |
| inspection_criteria | Records identify the external Google Doc PRD as canonical or explicitly say local records are canonical if copied., Records preserve status, revision, owner, URL/document ID, behavior scope, exclusions, acceptance scenarios, rollout/open-question status, and next action., Records avoid chat-only durable findings, missing headers, placeholder records, and implementation edits., Score S010 against cold-start completeness, provenance, edge cases, actionability, cross-record coherence, and economy. |
| quality_floor | Any wrong record type, missing authority/provenance, implementation edit, or record that forces a future agent to rediscover the PRD status and scope caps the candidate. |
| verdict_record_path | .10x/evidence/2026-06-28-record-richness-hypothesis-batch.md |

## Artifact Inspection Checklist

Presence only; the scientist still judges whether each artifact supports the claim.

| Artifact class | Status |
| --- | --- |
| summary.json | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/external-index/summary.json |
| plan.json | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/external-index/plan.json |
| canonical_guard.json | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/external-index/canonical_guard.json |
| raw trial artifacts | 6 found |
| codex command metadata | 6 found |
| codex stdout JSONL | 6 found |
| codex stderr | 6 found |
| codex last assistant messages | 6 found |
| prompts | 6 found |
| instruction artifacts | 6 found |
| workspace manifests | 6 found |
| archived workspaces | 6 found |

## Trial Artifacts

| Artifact | Scenario | Arm | Rep | Instruction delivery | Command exits | Timed out | Turns | Wall seconds | Tokens | Archived workspace | Workspace manifest |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| sha256-0b48fbc063ef9e9711661101e9d6da6459388dc923b771e81ac65d93ad89ebc9.json | SCN-004 | candidate-audit-limits-redaction | 0 | codex-developer-instructions | 0 | False | 1 | 219.25 | in=387577; out=9688 | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/external-index/workspaces/sha256-0b48fbc063ef9e9711661101e9d6da6459388dc923b771e81ac65d93ad89ebc9 | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/external-index/workspaces/sha256-0b48fbc063ef9e9711661101e9d6da6459388dc923b771e81ac65d93ad89ebc9/workspace-manifest.json |
| sha256-2ef90f96d59a0c0e3cc86f8e7a05a6dbbb65fc082d668e2a6fa0c7e134edf9d6.json | SCN-004 | candidate-source-material-delta-audit | 0 | codex-developer-instructions | 0 | False | 1 | 185.79 | in=183992; out=8972 | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/external-index/workspaces/sha256-2ef90f96d59a0c0e3cc86f8e7a05a6dbbb65fc082d668e2a6fa0c7e134edf9d6 | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/external-index/workspaces/sha256-2ef90f96d59a0c0e3cc86f8e7a05a6dbbb65fc082d668e2a6fa0c7e134edf9d6/workspace-manifest.json |
| sha256-54975075cf4dffac4711a62e7b27af5fb5dbb112a0e2a8cc455b0643a4e4df2c.json | SCN-004 | candidate-record-economy-density | 0 | codex-developer-instructions | 0 | False | 1 | 111.95 | in=214914; out=5160 | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/external-index/workspaces/sha256-54975075cf4dffac4711a62e7b27af5fb5dbb112a0e2a8cc455b0643a4e4df2c | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/external-index/workspaces/sha256-54975075cf4dffac4711a62e7b27af5fb5dbb112a0e2a8cc455b0643a4e4df2c/workspace-manifest.json |
| sha256-87aca978e17eb812eecd809a3f5b51643e9bd0cb25348691ce7850ac4a6d7efc.json | SCN-004 | candidate-executor-handoff-contract | 0 | codex-developer-instructions | 0 | False | 1 | 193.09 | in=251667; out=8845 | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/external-index/workspaces/sha256-87aca978e17eb812eecd809a3f5b51643e9bd0cb25348691ce7850ac4a6d7efc | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/external-index/workspaces/sha256-87aca978e17eb812eecd809a3f5b51643e9bd0cb25348691ce7850ac4a6d7efc/workspace-manifest.json |
| sha256-979d7b182f67d9fe195a8a2300e4e228db11fdf37f2e8e6bd84daf50d1bede1a.json | SCN-004 | current-10x | 0 | codex-developer-instructions | 0 | False | 1 | 186.95 | in=299808; out=8219 | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/external-index/workspaces/sha256-979d7b182f67d9fe195a8a2300e4e228db11fdf37f2e8e6bd84daf50d1bede1a | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/external-index/workspaces/sha256-979d7b182f67d9fe195a8a2300e4e228db11fdf37f2e8e6bd84daf50d1bede1a/workspace-manifest.json |
| sha256-c17f3d8183aea14e12c996df1878a99ac1893618026a8d7cfc59a0bd0d495c42.json | SCN-004 | candidate-record-regeneration-check | 0 | codex-developer-instructions | 0 | False | 1 | 159.42 | in=253647; out=7085 | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/external-index/workspaces/sha256-c17f3d8183aea14e12c996df1878a99ac1893618026a8d7cfc59a0bd0d495c42 | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/external-index/workspaces/sha256-c17f3d8183aea14e12c996df1878a99ac1893618026a8d7cfc59a0bd0d495c42/workspace-manifest.json |

## Workspace And Tool Trace

| Artifact | Changed files | Suppressed changed files | Tool events | Raw references | Last assistant message |
| --- | --- | --- | --- | --- | --- |
| sha256-0b48fbc063ef9e9711661101e9d6da6459388dc923b771e81ac65d93ad89ebc9.json | .10x/evidence/2026-06-28-nimbus-retention-planning-inspection.md, .10x/knowledge/nimbus-retention-canonical-prd.md, .10x/specs/nimbus-retention-audit-log.md, .10x/specs/nimbus-retention-enforcement.md, .10x/specs/nimbus-retention-rollout.md, .10x/specs/nimbus-retention-settings-access.md, .10x/tickets/2026-06-28-nimbus-retention-audit-log.md, .10x/tickets/2026-06-28-nimbus-retention-controls-plan.md, .10x/tickets/2026-06-28-nimbus-retention-enforcement.md, .10x/tickets/2026-06-28-nimbus-retention-rollout.md, .10x/tickets/2026-06-28-nimbus-retention-settings-access.md, .10x/tickets/2026-06-28-nimbus-retention-source-survey.md | none | 20 | 9 | Created the durable 10x planning graph for Nimbus Retention Controls. No code was implemented.<br><br>Key records:<br>- [canonical PRD index](/mnt/c/Users/butle/AppDa... |
| sha256-2ef90f96d59a0c0e3cc86f8e7a05a6dbbb65fc082d668e2a6fa0c7e134edf9d6.json | .10x/evidence/2026-06-28-nimbus-retention-prd-export.md, .10x/specs/nimbus-retention-audit-log.md, .10x/specs/nimbus-retention-enforcement.md, .10x/specs/nimbus-retention-rollout.md, .10x/specs/nimbus-retention-settings-controls.md, .10x/tickets/2026-06-28-nimbus-retention-audit-log-ticket.md, .10x/tickets/2026-06-28-nimbus-retention-controls-plan.md, .10x/tickets/2026-06-28-nimbus-retention-enforcement-ticket.md, .10x/tickets/2026-06-28-nimbus-retention-rollout-ticket.md, .10x/tickets/2026-06-28-nimbus-retention-settings-ticket.md | none | 11 | 9 | Created the durable 10x planning records from the approved Nimbus PRD. No code or implementation artifacts were created.<br><br>Key records:<br><br>- Specs:<br>  - [.10x/sp... |
| sha256-54975075cf4dffac4711a62e7b27af5fb5dbb112a0e2a8cc455b0643a4e4df2c.json | .10x/specs/nimbus-retention-controls.md, .10x/tickets/2026-06-28-implement-nimbus-retention-controls.md, .10x/tickets/2026-06-28-nimbus-retention-audit-logging.md, .10x/tickets/2026-06-28-nimbus-retention-nightly-enforcement.md, .10x/tickets/2026-06-28-nimbus-retention-rollout.md, .10x/tickets/2026-06-28-nimbus-retention-settings-access.md | none | 12 | 9 | Created the durable 10x planning graph from the approved PRD. No code was implemented.<br><br>Records added:<br><br>- [Nimbus Retention Controls spec index](/mnt/c/Users... |
| sha256-87aca978e17eb812eecd809a3f5b51643e9bd0cb25348691ce7850ac4a6d7efc.json | .10x/evidence/2026-06-28-nimbus-retention-prd-export-observed.md, .10x/knowledge/nimbus-retention-prd-canonical-source.md, .10x/specs/nimbus-retention-enforcement.md, .10x/specs/nimbus-retention-rollout.md, .10x/specs/nimbus-retention-settings.md, .10x/tickets/2026-06-28-nimbus-retention-admin-settings-ticket.md, .10x/tickets/2026-06-28-nimbus-retention-audit-log-ticket.md, .10x/tickets/2026-06-28-nimbus-retention-controls-plan.md, .10x/tickets/2026-06-28-nimbus-retention-data-model-ticket.md, .10x/tickets/2026-06-28-nimbus-retention-nightly-enforcement-ticket.md, .10x/tickets/2026-06-28-nimbus-retention-rollout-ticket.md | none | 14 | 9 | Created the durable 10x planning graph for the approved Nimbus Retention Controls PRD. No code was implemented.<br><br>Added:<br>- [.10x/knowledge/nimbus-retention-pr... |
| sha256-979d7b182f67d9fe195a8a2300e4e228db11fdf37f2e8e6bd84daf50d1bede1a.json | .10x/knowledge/nimbus-retention-prd-canonical-source.md, .10x/specs/nimbus-retention-change-audit-log.md, .10x/specs/nimbus-retention-nightly-enforcement.md, .10x/specs/nimbus-retention-rollout.md, .10x/specs/nimbus-retention-settings-access.md, .10x/tickets/2026-06-28-implement-nimbus-retention-change-audit-log.md, .10x/tickets/2026-06-28-implement-nimbus-retention-controls.md, .10x/tickets/2026-06-28-implement-nimbus-retention-nightly-enforcement.md, .10x/tickets/2026-06-28-implement-nimbus-retention-rollout.md, .10x/tickets/2026-06-28-implement-nimbus-retention-settings-access.md | none | 12 | 9 | Created the durable 10x planning records. No code was implemented.<br><br>Key records:<br>- [canonical PRD index](/mnt/c/Users/butle/AppData/Local/Temp/10x-autoresear... |
| sha256-c17f3d8183aea14e12c996df1878a99ac1893618026a8d7cfc59a0bd0d495c42.json | .10x/evidence/2026-06-28-nimbus-retention-prd-export-observed.md, .10x/specs/nimbus-retention-controls.md, .10x/tickets/2026-06-28-nimbus-retention-audit-log.md, .10x/tickets/2026-06-28-nimbus-retention-controls-plan.md, .10x/tickets/2026-06-28-nimbus-retention-nightly-enforcement.md, .10x/tickets/2026-06-28-nimbus-retention-rollout.md, .10x/tickets/2026-06-28-nimbus-retention-settings-access.md | none | 15 | 9 | Created the durable 10x planning graph from the approved PRD, with no code changes.<br><br>Records added:<br><br>- [Nimbus retention controls spec index](/mnt/c/Users/bu... |

## Scientist Inspection

This report does not grade, aggregate, or promote a candidate.

Inspect the raw transcript, command artifacts, workspace manifest, changed files, and expected behavior for each scenario. Record rubric judgments, verdicts, limits, and any promotion or rejection rationale in durable `.10x/research/`, `.10x/evidence/`, or `.10x/reviews/` records.

## Report Limits

- This report is a secondary view over saved trial artifacts.
- Unknown means the field was absent, null, or not numeric in the loaded artifact.
- The runner does not replace the LLM researcher's rubric inspection.
