# 10x Autoresearch Trial Report

Source: `.10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/v2-ticket-handoff`

## Summary

| Field | Value |
| --- | --- |
| experiment_id | EXP-20260628-s010-v2-ticket-handoff |
| mode | live |
| raw_artifacts | 4 |
| live_subject_calls | 4 |
| summary | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/v2-ticket-handoff/summary.json |
| plan | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/v2-ticket-handoff/plan.json |
| raw_output_dir | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/v2-ticket-handoff/raw |
| workspace_dir | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/v2-ticket-handoff/workspaces |
| prompt_dir | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/v2-ticket-handoff/prompts |
| harness_artifact_dir | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/v2-ticket-handoff/codex |

## Scientific Contract

| Field | Value |
| --- | --- |
| question | Does the compact cold-start record handoff candidate improve executable ticket handoff versus current 10x? |
| hypothesis | The compact candidate should preserve active authority, source drift, exclusions, evidence expectations, and first inspection targets without bloating the ticket. |
| expected_behavior | Subject creates a bounded executable ticket for bringing invoice retry export source/tests into alignment with active policy/spec while treating superseded, done, and cancelled records as history. |
| inspection_criteria | Ticket references active decision and spec, not superseded or terminal records as authority., Ticket states source drift: current code uses delinquent and enterprise filtering while active spec requires overdue, production, retryEligible, non-cancelled, no enterprise filter., Ticket includes explicit exclusions, first source/tests to inspect, edge cases, evidence expectations, blockers/provenance, and next action., No implementation edits occur. |
| quality_floor | Any implementation edit, terminal-record authority mistake, missing acceptance criteria, or ticket that omits the known source drift caps the candidate. |
| verdict_record_path | .10x/evidence/2026-06-28-record-richness-hypothesis-batch.md |

## Artifact Inspection Checklist

Presence only; the scientist still judges whether each artifact supports the claim.

| Artifact class | Status |
| --- | --- |
| summary.json | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/v2-ticket-handoff/summary.json |
| plan.json | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/v2-ticket-handoff/plan.json |
| canonical_guard.json | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/v2-ticket-handoff/canonical_guard.json |
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
| sha256-0684884837e43e49b83dd2065b11cf08af5bc91d545e0fea6e300c553eaeff26.json | SCN-006 | candidate-cold-start-record-handoff-check | 0 | codex-developer-instructions | 0 | False | 1 | 78.85 | in=238890; out=3099 | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/v2-ticket-handoff/workspaces/sha256-0684884837e43e49b83dd2065b11cf08af5bc91d545e0fea6e300c553eaeff26 | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/v2-ticket-handoff/workspaces/sha256-0684884837e43e49b83dd2065b11cf08af5bc91d545e0fea6e300c553eaeff26/workspace-manifest.json |
| sha256-219908b7b860deb17da2ab2ae123a3e12a41267747533fd2bdab691ab757ed03.json | SCN-006 | current-10x | 1 | codex-developer-instructions | 0 | False | 1 | 69.61 | in=205028; out=3040 | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/v2-ticket-handoff/workspaces/sha256-219908b7b860deb17da2ab2ae123a3e12a41267747533fd2bdab691ab757ed03 | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/v2-ticket-handoff/workspaces/sha256-219908b7b860deb17da2ab2ae123a3e12a41267747533fd2bdab691ab757ed03/workspace-manifest.json |
| sha256-32b57c7f3df7ef5c75ec2016fe2257b716e07be0298ccd1d4950f7e2d34f0c27.json | SCN-006 | current-10x | 0 | codex-developer-instructions | 0 | False | 1 | 71.47 | in=234580; out=2930 | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/v2-ticket-handoff/workspaces/sha256-32b57c7f3df7ef5c75ec2016fe2257b716e07be0298ccd1d4950f7e2d34f0c27 | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/v2-ticket-handoff/workspaces/sha256-32b57c7f3df7ef5c75ec2016fe2257b716e07be0298ccd1d4950f7e2d34f0c27/workspace-manifest.json |
| sha256-f5c4ae3edb15c4e034dd87b9e5ce259c0fcf0e7f02b44fcb66ccc7b187c1e9b3.json | SCN-006 | candidate-cold-start-record-handoff-check | 1 | codex-developer-instructions | 0 | False | 1 | 73.60 | in=216899; out=2810 | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/v2-ticket-handoff/workspaces/sha256-f5c4ae3edb15c4e034dd87b9e5ce259c0fcf0e7f02b44fcb66ccc7b187c1e9b3 | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/v2-ticket-handoff/workspaces/sha256-f5c4ae3edb15c4e034dd87b9e5ce259c0fcf0e7f02b44fcb66ccc7b187c1e9b3/workspace-manifest.json |

## Workspace And Tool Trace

| Artifact | Changed files | Suppressed changed files | Tool events | Raw references | Last assistant message |
| --- | --- | --- | --- | --- | --- |
| sha256-0684884837e43e49b83dd2065b11cf08af5bc91d545e0fea6e300c553eaeff26.json | .10x/tickets/2026-06-28-align-invoice-retry-export-active-policy.md | none | 20 | 9 | Created the executable ticket:<br><br>[.10x/tickets/2026-06-28-align-invoice-retry-export-active-policy.md](/mnt/c/Users/butle/AppData/Local/Temp/10x-autoresearch-... |
| sha256-219908b7b860deb17da2ab2ae123a3e12a41267747533fd2bdab691ab757ed03.json | .10x/tickets/2026-06-28-align-invoice-retry-export.md | none | 15 | 9 | Created the executable implementation ticket:<br><br>[.10x/tickets/2026-06-28-align-invoice-retry-export.md](/mnt/c/Users/butle/AppData/Local/Temp/10x-autoresearch... |
| sha256-32b57c7f3df7ef5c75ec2016fe2257b716e07be0298ccd1d4950f7e2d34f0c27.json | .10x/tickets/2026-06-28-align-invoice-retry-export-with-active-policy.md | none | 19 | 9 | Created the executable implementation ticket:<br><br>[.10x/tickets/2026-06-28-align-invoice-retry-export-with-active-policy.md](/mnt/c/Users/butle/AppData/Local/Te... |
| sha256-f5c4ae3edb15c4e034dd87b9e5ce259c0fcf0e7f02b44fcb66ccc7b187c1e9b3.json | .10x/tickets/2026-06-28-align-invoice-retry-export-with-active-policy.md | none | 16 | 9 | Created the executable implementation ticket:<br><br>[.10x/tickets/2026-06-28-align-invoice-retry-export-with-active-policy.md](/mnt/c/Users/butle/AppData/Local/Te... |

## Scientist Inspection

This report does not grade, aggregate, or promote a candidate.

Inspect the raw transcript, command artifacts, workspace manifest, changed files, and expected behavior for each scenario. Record rubric judgments, verdicts, limits, and any promotion or rejection rationale in durable `.10x/research/`, `.10x/evidence/`, or `.10x/reviews/` records.

## Report Limits

- This report is a secondary view over saved trial artifacts.
- Unknown means the field was absent, null, or not numeric in the loaded artifact.
- The runner does not replace the LLM researcher's rubric inspection.
