# 10x Autoresearch Trial Report

Source: `.10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/ticket-handoff`

## Summary

| Field | Value |
| --- | --- |
| experiment_id | EXP-20260628-s010-ticket-handoff |
| mode | live |
| raw_artifacts | 6 |
| live_subject_calls | 6 |
| summary | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/ticket-handoff/summary.json |
| plan | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/ticket-handoff/plan.json |
| raw_output_dir | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/ticket-handoff/raw |
| workspace_dir | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/ticket-handoff/workspaces |
| prompt_dir | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/ticket-handoff/prompts |
| harness_artifact_dir | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/ticket-handoff/codex |

## Scientific Contract

| Field | Value |
| --- | --- |
| question | Which S010 candidate best creates a cold-start executable ticket from mixed active and terminal record authority? |
| hypothesis | Executor-handoff should improve ticket actionability and evidence expectations; source-material-delta should better preserve authority boundaries. |
| expected_behavior | Subject creates a bounded executable ticket for bringing invoice retry export source/tests into alignment with active policy/spec while treating superseded, done, and cancelled records as history. |
| inspection_criteria | Ticket references active decision and spec, not superseded or terminal records as authority., Ticket states source drift: current code uses delinquent and enterprise filtering while active spec requires overdue, production, retryEligible, non-cancelled, no enterprise filter., Ticket includes explicit exclusions, first source/tests to inspect, edge cases, evidence expectations, and blockers if required data is missing., No implementation edits occur. |
| quality_floor | Any implementation edit, terminal-record authority mistake, missing acceptance criteria, or ticket that omits the known source drift caps the candidate. |
| verdict_record_path | .10x/evidence/2026-06-28-record-richness-hypothesis-batch.md |

## Artifact Inspection Checklist

Presence only; the scientist still judges whether each artifact supports the claim.

| Artifact class | Status |
| --- | --- |
| summary.json | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/ticket-handoff/summary.json |
| plan.json | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/ticket-handoff/plan.json |
| canonical_guard.json | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/ticket-handoff/canonical_guard.json |
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
| sha256-2b15bb60fab38b02ea3d9475c5b9916d4971ad277ecc63d7421ace2f1f76b696.json | SCN-006 | candidate-record-regeneration-check | 0 | codex-developer-instructions | 0 | False | 1 | 60.72 | in=207484; out=2512 | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/ticket-handoff/workspaces/sha256-2b15bb60fab38b02ea3d9475c5b9916d4971ad277ecc63d7421ace2f1f76b696 | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/ticket-handoff/workspaces/sha256-2b15bb60fab38b02ea3d9475c5b9916d4971ad277ecc63d7421ace2f1f76b696/workspace-manifest.json |
| sha256-395012c15b343e10fa0c78f0d8cbefae9b38fb133de736edc90e537cf19f4617.json | SCN-006 | candidate-record-economy-density | 0 | codex-developer-instructions | 0 | False | 1 | 63.25 | in=213046; out=2622 | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/ticket-handoff/workspaces/sha256-395012c15b343e10fa0c78f0d8cbefae9b38fb133de736edc90e537cf19f4617 | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/ticket-handoff/workspaces/sha256-395012c15b343e10fa0c78f0d8cbefae9b38fb133de736edc90e537cf19f4617/workspace-manifest.json |
| sha256-79c1bd8bf275f8d6c36d8775016ffe20e5f18d1588347ebe87a102551856f4ed.json | SCN-006 | current-10x | 0 | codex-developer-instructions | 0 | False | 1 | 64.72 | in=203027; out=2581 | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/ticket-handoff/workspaces/sha256-79c1bd8bf275f8d6c36d8775016ffe20e5f18d1588347ebe87a102551856f4ed | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/ticket-handoff/workspaces/sha256-79c1bd8bf275f8d6c36d8775016ffe20e5f18d1588347ebe87a102551856f4ed/workspace-manifest.json |
| sha256-8f127a4f6bca7346aa99ba51916cfd6671273b5cc63275ada22165270d468970.json | SCN-006 | candidate-audit-limits-redaction | 0 | codex-developer-instructions | 0 | False | 1 | 64.90 | in=181526; out=2109 | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/ticket-handoff/workspaces/sha256-8f127a4f6bca7346aa99ba51916cfd6671273b5cc63275ada22165270d468970 | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/ticket-handoff/workspaces/sha256-8f127a4f6bca7346aa99ba51916cfd6671273b5cc63275ada22165270d468970/workspace-manifest.json |
| sha256-9aebf46a2d21fc66d68c9d585a3b7099f59e580861b652f688d4ab961a6060b8.json | SCN-006 | candidate-source-material-delta-audit | 0 | codex-developer-instructions | 0 | False | 1 | 63.65 | in=184610; out=2674 | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/ticket-handoff/workspaces/sha256-9aebf46a2d21fc66d68c9d585a3b7099f59e580861b652f688d4ab961a6060b8 | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/ticket-handoff/workspaces/sha256-9aebf46a2d21fc66d68c9d585a3b7099f59e580861b652f688d4ab961a6060b8/workspace-manifest.json |
| sha256-aa7aa3e67af911bf53701e5f54145596ee78440550163d3edb3298e040fb6f1c.json | SCN-006 | candidate-executor-handoff-contract | 0 | codex-developer-instructions | 0 | False | 1 | 76.43 | in=207520; out=3118 | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/ticket-handoff/workspaces/sha256-aa7aa3e67af911bf53701e5f54145596ee78440550163d3edb3298e040fb6f1c | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/ticket-handoff/workspaces/sha256-aa7aa3e67af911bf53701e5f54145596ee78440550163d3edb3298e040fb6f1c/workspace-manifest.json |

## Workspace And Tool Trace

| Artifact | Changed files | Suppressed changed files | Tool events | Raw references | Last assistant message |
| --- | --- | --- | --- | --- | --- |
| sha256-2b15bb60fab38b02ea3d9475c5b9916d4971ad277ecc63d7421ace2f1f76b696.json | .10x/tickets/2026-06-28-align-invoice-retry-export-active-policy.md | none | 14 | 9 | Created the executable ticket: [.10x/tickets/2026-06-28-align-invoice-retry-export-active-policy.md](/mnt/c/Users/butle/AppData/Local/Temp/10x-autoresearch-p... |
| sha256-395012c15b343e10fa0c78f0d8cbefae9b38fb133de736edc90e537cf19f4617.json | .10x/tickets/2026-06-28-align-invoice-retry-export.md | none | 15 | 9 | Created the executable ticket: [.10x/tickets/2026-06-28-align-invoice-retry-export.md](/mnt/c/Users/butle/AppData/Local/Temp/10x-autoresearch-fn3j78_f/worksp... |
| sha256-79c1bd8bf275f8d6c36d8775016ffe20e5f18d1588347ebe87a102551856f4ed.json | .10x/tickets/2026-06-28-align-invoice-retry-export-active-policy.md | none | 15 | 9 | Created the executable implementation ticket:<br><br>[.10x/tickets/2026-06-28-align-invoice-retry-export-active-policy.md](/mnt/c/Users/butle/AppData/Local/Temp/10... |
| sha256-8f127a4f6bca7346aa99ba51916cfd6671273b5cc63275ada22165270d468970.json | .10x/tickets/2026-06-28-align-invoice-retry-export-active-policy.md | none | 12 | 9 | Created the executable implementation ticket:<br><br>[2026-06-28-align-invoice-retry-export-active-policy.md](/mnt/c/Users/butle/AppData/Local/Temp/10x-autoresearc... |
| sha256-9aebf46a2d21fc66d68c9d585a3b7099f59e580861b652f688d4ab961a6060b8.json | .10x/tickets/2026-06-28-align-invoice-retry-export-active-policy.md | none | 15 | 9 | Created the executable implementation ticket:<br><br>[2026-06-28-align-invoice-retry-export-active-policy.md](/mnt/c/Users/butle/AppData/Local/Temp/10x-autoresearc... |
| sha256-aa7aa3e67af911bf53701e5f54145596ee78440550163d3edb3298e040fb6f1c.json | .10x/tickets/2026-06-28-align-invoice-retry-export-current-policy.md | none | 17 | 9 | Created the executable implementation ticket:<br><br>[.10x/tickets/2026-06-28-align-invoice-retry-export-current-policy.md](/mnt/c/Users/butle/AppData/Local/Temp/1... |

## Scientist Inspection

This report does not grade, aggregate, or promote a candidate.

Inspect the raw transcript, command artifacts, workspace manifest, changed files, and expected behavior for each scenario. Record rubric judgments, verdicts, limits, and any promotion or rejection rationale in durable `.10x/research/`, `.10x/evidence/`, or `.10x/reviews/` records.

## Report Limits

- This report is a secondary view over saved trial artifacts.
- Unknown means the field was absent, null, or not numeric in the loaded artifact.
- The runner does not replace the LLM researcher's rubric inspection.
