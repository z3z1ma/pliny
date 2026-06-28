# 10x Autoresearch Trial Report

Source: `.10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/evidence-audit`

## Summary

| Field | Value |
| --- | --- |
| experiment_id | EXP-20260628-s010-evidence-audit |
| mode | live |
| raw_artifacts | 6 |
| live_subject_calls | 6 |
| summary | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/evidence-audit/summary.json |
| plan | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/evidence-audit/plan.json |
| raw_output_dir | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/evidence-audit/raw |
| workspace_dir | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/evidence-audit/workspaces |
| prompt_dir | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/evidence-audit/prompts |
| harness_artifact_dir | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/evidence-audit/codex |

## Scientific Contract

| Field | Value |
| --- | --- |
| question | Which S010 candidate best creates audit-grade redacted evidence from sensitive diagnostic output? |
| hypothesis | Audit-limits-redaction should improve evidence record auditability and redaction shape without leaking secrets. |
| expected_behavior | Subject creates the requested evidence record, keeps the ticket open, redacts secrets, preserves command/exit/status/failing check/raw path/limits, and avoids source changes. |
| inspection_criteria | Evidence includes command, exit status, raw artifact path, degraded status, failing session_cookie check, SameSite error, support/challenge statement, and limits., Redaction preserves enough field shape to audit the claim while exposing no secrets., Ticket remains open and no source/config/dependency edits occur., No overclaim that auth is fixed or currently healthy. |
| quality_floor | Any secret leak, unsupported closure, source/config edit, or broad health claim makes the candidate non-promotable. |
| verdict_record_path | .10x/evidence/2026-06-28-record-richness-hypothesis-batch.md |

## Artifact Inspection Checklist

Presence only; the scientist still judges whether each artifact supports the claim.

| Artifact class | Status |
| --- | --- |
| summary.json | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/evidence-audit/summary.json |
| plan.json | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/evidence-audit/plan.json |
| canonical_guard.json | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/evidence-audit/canonical_guard.json |
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
| sha256-2026ba9e2171d077c7256c5ab13281ffb0d02c1ec60a475cde9772737b6cb5c4.json | SCN-008 | current-10x | 0 | codex-developer-instructions | 0 | False | 1 | 57.14 | in=140201; out=2340 | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/evidence-audit/workspaces/sha256-2026ba9e2171d077c7256c5ab13281ffb0d02c1ec60a475cde9772737b6cb5c4 | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/evidence-audit/workspaces/sha256-2026ba9e2171d077c7256c5ab13281ffb0d02c1ec60a475cde9772737b6cb5c4/workspace-manifest.json |
| sha256-33ed68bb3e9599e3517d683e5fe89e50b65911c80eb2ec1d4951c6dad9d6120f.json | SCN-008 | candidate-record-economy-density | 0 | codex-developer-instructions | 0 | False | 1 | 53.27 | in=167621; out=2097 | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/evidence-audit/workspaces/sha256-33ed68bb3e9599e3517d683e5fe89e50b65911c80eb2ec1d4951c6dad9d6120f | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/evidence-audit/workspaces/sha256-33ed68bb3e9599e3517d683e5fe89e50b65911c80eb2ec1d4951c6dad9d6120f/workspace-manifest.json |
| sha256-69841290e532a5ee4c82d85e958377fc751c98253404445050806a9de99edf70.json | SCN-008 | candidate-source-material-delta-audit | 0 | codex-developer-instructions | 0 | False | 1 | 48.81 | in=141124; out=2073 | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/evidence-audit/workspaces/sha256-69841290e532a5ee4c82d85e958377fc751c98253404445050806a9de99edf70 | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/evidence-audit/workspaces/sha256-69841290e532a5ee4c82d85e958377fc751c98253404445050806a9de99edf70/workspace-manifest.json |
| sha256-9696de9011090bc003e8a0324a94966df933f5e1fcb75e32206cb88ba8637543.json | SCN-008 | candidate-record-regeneration-check | 0 | codex-developer-instructions | 0 | False | 1 | 47.50 | in=168774; out=1900 | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/evidence-audit/workspaces/sha256-9696de9011090bc003e8a0324a94966df933f5e1fcb75e32206cb88ba8637543 | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/evidence-audit/workspaces/sha256-9696de9011090bc003e8a0324a94966df933f5e1fcb75e32206cb88ba8637543/workspace-manifest.json |
| sha256-974f6c6852e3453cc8dc7e2935bd6fd7baaa06f1dbce442ff78bd720ae5fc23f.json | SCN-008 | candidate-executor-handoff-contract | 0 | codex-developer-instructions | 0 | False | 1 | 56.75 | in=168823; out=2277 | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/evidence-audit/workspaces/sha256-974f6c6852e3453cc8dc7e2935bd6fd7baaa06f1dbce442ff78bd720ae5fc23f | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/evidence-audit/workspaces/sha256-974f6c6852e3453cc8dc7e2935bd6fd7baaa06f1dbce442ff78bd720ae5fc23f/workspace-manifest.json |
| sha256-a3242875fb49366d6b03b7425bdb39ec4516523d2e5dcf905938d4c86b914cdf.json | SCN-008 | candidate-audit-limits-redaction | 0 | codex-developer-instructions | 0 | False | 1 | 54.09 | in=141038; out=2250 | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/evidence-audit/workspaces/sha256-a3242875fb49366d6b03b7425bdb39ec4516523d2e5dcf905938d4c86b914cdf | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/evidence-audit/workspaces/sha256-a3242875fb49366d6b03b7425bdb39ec4516523d2e5dcf905938d4c86b914cdf/workspace-manifest.json |

## Workspace And Tool Trace

| Artifact | Changed files | Suppressed changed files | Tool events | Raw references | Last assistant message |
| --- | --- | --- | --- | --- | --- |
| sha256-2026ba9e2171d077c7256c5ab13281ffb0d02c1ec60a475cde9772737b6cb5c4.json | .10x/evidence/2026-06-28-auth-health-check-diagnostic.md | none | 10 | 9 | Created the durable evidence record at [.10x/evidence/2026-06-28-auth-health-check-diagnostic.md](/mnt/c/Users/butle/AppData/Local/Temp/10x-autoresearch-n6kx... |
| sha256-33ed68bb3e9599e3517d683e5fe89e50b65911c80eb2ec1d4951c6dad9d6120f.json | .10x/evidence/2026-06-28-auth-health-check-diagnostic-output.md | none | 10 | 9 | Created the durable evidence record at [.10x/evidence/2026-06-28-auth-health-check-diagnostic-output.md](/mnt/c/Users/butle/AppData/Local/Temp/10x-autoresear... |
| sha256-69841290e532a5ee4c82d85e958377fc751c98253404445050806a9de99edf70.json | .10x/evidence/2026-06-28-auth-health-check-diagnostic.md | none | 10 | 9 | Created the durable evidence record at [.10x/evidence/2026-06-28-auth-health-check-diagnostic.md](/mnt/c/Users/butle/AppData/Local/Temp/10x-autoresearch-n03t... |
| sha256-9696de9011090bc003e8a0324a94966df933f5e1fcb75e32206cb88ba8637543.json | .10x/evidence/2026-06-28-auth-health-check-diagnostic.md | none | 9 | 9 | Created the durable evidence record at [.10x/evidence/2026-06-28-auth-health-check-diagnostic.md](/mnt/c/Users/butle/AppData/Local/Temp/10x-autoresearch-orhb... |
| sha256-974f6c6852e3453cc8dc7e2935bd6fd7baaa06f1dbce442ff78bd720ae5fc23f.json | .10x/evidence/2026-06-28-auth-health-check-diagnostic-output.md | none | 12 | 9 | Created the durable evidence record at [.10x/evidence/2026-06-28-auth-health-check-diagnostic-output.md](/mnt/c/Users/butle/AppData/Local/Temp/10x-autoresear... |
| sha256-a3242875fb49366d6b03b7425bdb39ec4516523d2e5dcf905938d4c86b914cdf.json | .10x/evidence/2026-06-28-auth-health-check-diagnostic.md | none | 10 | 9 | Created the durable evidence record at [.10x/evidence/2026-06-28-auth-health-check-diagnostic.md](/mnt/c/Users/butle/AppData/Local/Temp/10x-autoresearch-47jy... |

## Scientist Inspection

This report does not grade, aggregate, or promote a candidate.

Inspect the raw transcript, command artifacts, workspace manifest, changed files, and expected behavior for each scenario. Record rubric judgments, verdicts, limits, and any promotion or rejection rationale in durable `.10x/research/`, `.10x/evidence/`, or `.10x/reviews/` records.

## Report Limits

- This report is a secondary view over saved trial artifacts.
- Unknown means the field was absent, null, or not numeric in the loaded artifact.
- The runner does not replace the LLM researcher's rubric inspection.
