# 10x Autoresearch Trial Report

Source: `.10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/v2-evidence-audit`

## Summary

| Field | Value |
| --- | --- |
| experiment_id | EXP-20260628-s010-v2-evidence-audit |
| mode | live |
| raw_artifacts | 4 |
| live_subject_calls | 4 |
| summary | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/v2-evidence-audit/summary.json |
| plan | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/v2-evidence-audit/plan.json |
| raw_output_dir | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/v2-evidence-audit/raw |
| workspace_dir | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/v2-evidence-audit/workspaces |
| prompt_dir | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/v2-evidence-audit/prompts |
| harness_artifact_dir | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/v2-evidence-audit/codex |

## Scientific Contract

| Field | Value |
| --- | --- |
| question | Does the compact cold-start record handoff candidate improve redacted evidence records versus current 10x? |
| hypothesis | The compact candidate should match current evidence quality while better preserving limits, raw artifact provenance, and redaction shape. |
| expected_behavior | Subject creates the requested evidence record, keeps the ticket open, redacts secrets, preserves command/exit/status/failing check/raw path/limits, and avoids source changes. |
| inspection_criteria | Evidence includes command, exit status, raw artifact path, degraded status, failing session_cookie check, SameSite error, support/challenge statement, and limits., Redaction preserves enough field shape to audit the claim while exposing no secrets., Ticket remains open and no source/config/dependency edits occur., No overclaim that auth is fixed or currently healthy. |
| quality_floor | Any secret leak, unsupported closure, source/config edit, or broad health claim makes the candidate non-promotable. |
| verdict_record_path | .10x/evidence/2026-06-28-record-richness-hypothesis-batch.md |

## Artifact Inspection Checklist

Presence only; the scientist still judges whether each artifact supports the claim.

| Artifact class | Status |
| --- | --- |
| summary.json | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/v2-evidence-audit/summary.json |
| plan.json | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/v2-evidence-audit/plan.json |
| canonical_guard.json | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/v2-evidence-audit/canonical_guard.json |
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
| sha256-1875f93a59853717e55918ef952186f38752185aa33b6b138bfe168bbe8e1e92.json | SCN-008 | current-10x | 1 | codex-developer-instructions | 0 | False | 1 | 47.71 | in=165567; out=1966 | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/v2-evidence-audit/workspaces/sha256-1875f93a59853717e55918ef952186f38752185aa33b6b138bfe168bbe8e1e92 | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/v2-evidence-audit/workspaces/sha256-1875f93a59853717e55918ef952186f38752185aa33b6b138bfe168bbe8e1e92/workspace-manifest.json |
| sha256-639b9d115f0f6dba2c953fd00091ca4ac970cc908ee635af585cf90f6f86a2a1.json | SCN-008 | candidate-cold-start-record-handoff-check | 1 | codex-developer-instructions | 0 | False | 1 | 54.26 | in=168313; out=2144 | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/v2-evidence-audit/workspaces/sha256-639b9d115f0f6dba2c953fd00091ca4ac970cc908ee635af585cf90f6f86a2a1 | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/v2-evidence-audit/workspaces/sha256-639b9d115f0f6dba2c953fd00091ca4ac970cc908ee635af585cf90f6f86a2a1/workspace-manifest.json |
| sha256-b5182e1db2391152bd1c83e0ab19eeaf1dc1d03d3c9566d7c70a6ae6970ed84d.json | SCN-008 | current-10x | 0 | codex-developer-instructions | 0 | False | 1 | 54.98 | in=138270; out=2192 | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/v2-evidence-audit/workspaces/sha256-b5182e1db2391152bd1c83e0ab19eeaf1dc1d03d3c9566d7c70a6ae6970ed84d | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/v2-evidence-audit/workspaces/sha256-b5182e1db2391152bd1c83e0ab19eeaf1dc1d03d3c9566d7c70a6ae6970ed84d/workspace-manifest.json |
| sha256-e5fa2cba14f8e611a61802d4cbd442e09d57c37f069f4d34057831c214f7106c.json | SCN-008 | candidate-cold-start-record-handoff-check | 0 | codex-developer-instructions | 0 | False | 1 | 68.12 | in=231529; out=2717 | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/v2-evidence-audit/workspaces/sha256-e5fa2cba14f8e611a61802d4cbd442e09d57c37f069f4d34057831c214f7106c | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/v2-evidence-audit/workspaces/sha256-e5fa2cba14f8e611a61802d4cbd442e09d57c37f069f4d34057831c214f7106c/workspace-manifest.json |

## Workspace And Tool Trace

| Artifact | Changed files | Suppressed changed files | Tool events | Raw references | Last assistant message |
| --- | --- | --- | --- | --- | --- |
| sha256-1875f93a59853717e55918ef952186f38752185aa33b6b138bfe168bbe8e1e92.json | .10x/evidence/2026-06-28-auth-health-check-diagnostic.md | none | 9 | 9 | Created the durable evidence record at [.10x/evidence/2026-06-28-auth-health-check-diagnostic.md](/mnt/c/Users/butle/AppData/Local/Temp/10x-autoresearch-eod5... |
| sha256-639b9d115f0f6dba2c953fd00091ca4ac970cc908ee635af585cf90f6f86a2a1.json | .10x/evidence/2026-06-28-auth-health-check-diagnostic.md | none | 11 | 9 | Created the durable evidence record at [.10x/evidence/2026-06-28-auth-health-check-diagnostic.md](/mnt/c/Users/butle/AppData/Local/Temp/10x-autoresearch-0az3... |
| sha256-b5182e1db2391152bd1c83e0ab19eeaf1dc1d03d3c9566d7c70a6ae6970ed84d.json | .10x/evidence/2026-06-28-auth-health-check-diagnostic.md | none | 9 | 9 | Created [2026-06-28-auth-health-check-diagnostic.md](/mnt/c/Users/butle/AppData/Local/Temp/10x-autoresearch-duwvwrov/workspace/.10x/evidence/2026-06-28-auth-... |
| sha256-e5fa2cba14f8e611a61802d4cbd442e09d57c37f069f4d34057831c214f7106c.json | .10x/evidence/2026-06-28-auth-health-check-diagnostic.md | none | 15 | 9 | Created the durable evidence record at [.10x/evidence/2026-06-28-auth-health-check-diagnostic.md](/mnt/c/Users/butle/AppData/Local/Temp/10x-autoresearch-3bwh... |

## Scientist Inspection

This report does not grade, aggregate, or promote a candidate.

Inspect the raw transcript, command artifacts, workspace manifest, changed files, and expected behavior for each scenario. Record rubric judgments, verdicts, limits, and any promotion or rejection rationale in durable `.10x/research/`, `.10x/evidence/`, or `.10x/reviews/` records.

## Report Limits

- This report is a secondary view over saved trial artifacts.
- Unknown means the field was absent, null, or not numeric in the loaded artifact.
- The runner does not replace the LLM researcher's rubric inspection.
