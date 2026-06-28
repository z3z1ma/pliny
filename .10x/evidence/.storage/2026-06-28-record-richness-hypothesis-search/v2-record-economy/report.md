# 10x Autoresearch Trial Report

Source: `.10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/v2-record-economy`

## Summary

| Field | Value |
| --- | --- |
| experiment_id | EXP-20260628-s010-v2-record-economy |
| mode | live |
| raw_artifacts | 4 |
| live_subject_calls | 4 |
| summary | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/v2-record-economy/summary.json |
| plan | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/v2-record-economy/plan.json |
| raw_output_dir | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/v2-record-economy/raw |
| workspace_dir | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/v2-record-economy/workspaces |
| prompt_dir | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/v2-record-economy/prompts |
| harness_artifact_dir | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/v2-record-economy/codex |

## Scientific Contract

| Field | Value |
| --- | --- |
| question | Does the compact cold-start record handoff candidate improve record economy versus current 10x? |
| hypothesis | The compact candidate should create a distinct docs-gap owner only when needed while preserving source/spec/test provenance. |
| expected_behavior | Subject inspects account export records/source/tests/docs, avoids duplicate or placeholder records, and creates or updates only the durable owner needed for the operator documentation email-column gap. |
| inspection_criteria | Subject does not reopen cancelled or done history as active authority., Subject does not create a spread of placeholder records., Any new or updated record names the docs gap, active governing spec, existing test ticket, explicit exclusions, source/docs/test provenance, and next action., No source implementation or docs edits occur. |
| quality_floor | Duplicate tickets, placeholder records, implementation/docs edits, or a terse record that omits why the docs gap is distinct from the email-redaction test make the candidate non-promotable. |
| verdict_record_path | .10x/evidence/2026-06-28-record-richness-hypothesis-batch.md |

## Artifact Inspection Checklist

Presence only; the scientist still judges whether each artifact supports the claim.

| Artifact class | Status |
| --- | --- |
| summary.json | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/v2-record-economy/summary.json |
| plan.json | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/v2-record-economy/plan.json |
| canonical_guard.json | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/v2-record-economy/canonical_guard.json |
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
| sha256-0413f58d7d2040df5a04aa4b3e1784f851617f6bb0c0c0f1415bdecb103ced3e.json | SCN-005 | candidate-cold-start-record-handoff-check | 1 | codex-developer-instructions | 0 | False | 1 | 85.99 | in=216460; out=3076 | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/v2-record-economy/workspaces/sha256-0413f58d7d2040df5a04aa4b3e1784f851617f6bb0c0c0f1415bdecb103ced3e | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/v2-record-economy/workspaces/sha256-0413f58d7d2040df5a04aa4b3e1784f851617f6bb0c0c0f1415bdecb103ced3e/workspace-manifest.json |
| sha256-1fc1e0ee85ac4e38186bfdef16c19f19bb06b707dfd576a1d9bb5fd76a05b40b.json | SCN-005 | current-10x | 0 | codex-developer-instructions | 0 | False | 1 | 65.03 | in=178127; out=2602 | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/v2-record-economy/workspaces/sha256-1fc1e0ee85ac4e38186bfdef16c19f19bb06b707dfd576a1d9bb5fd76a05b40b | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/v2-record-economy/workspaces/sha256-1fc1e0ee85ac4e38186bfdef16c19f19bb06b707dfd576a1d9bb5fd76a05b40b/workspace-manifest.json |
| sha256-33d9c40517323e4e547cf18e949da93286aeb9f56966ecb70422ef1d6fa07fe6.json | SCN-005 | candidate-cold-start-record-handoff-check | 0 | codex-developer-instructions | 0 | False | 1 | 78.14 | in=209580; out=3281 | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/v2-record-economy/workspaces/sha256-33d9c40517323e4e547cf18e949da93286aeb9f56966ecb70422ef1d6fa07fe6 | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/v2-record-economy/workspaces/sha256-33d9c40517323e4e547cf18e949da93286aeb9f56966ecb70422ef1d6fa07fe6/workspace-manifest.json |
| sha256-de6b00378e14acb53ed5abcca72b88777dda64ac49bdfc2372a064330a47f7ee.json | SCN-005 | current-10x | 1 | codex-developer-instructions | 0 | False | 1 | 62.14 | in=147203; out=2516 | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/v2-record-economy/workspaces/sha256-de6b00378e14acb53ed5abcca72b88777dda64ac49bdfc2372a064330a47f7ee | .10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/v2-record-economy/workspaces/sha256-de6b00378e14acb53ed5abcca72b88777dda64ac49bdfc2372a064330a47f7ee/workspace-manifest.json |

## Workspace And Tool Trace

| Artifact | Changed files | Suppressed changed files | Tool events | Raw references | Last assistant message |
| --- | --- | --- | --- | --- | --- |
| sha256-0413f58d7d2040df5a04aa4b3e1784f851617f6bb0c0c0f1415bdecb103ced3e.json | .10x/tickets/2026-06-25-account-export-hardening-parent.md, .10x/tickets/2026-06-28-remove-account-export-email-from-operator-docs.md | none | 18 | 9 | Created the distinct docs owner: [.10x/tickets/2026-06-28-remove-account-export-email-from-operator-docs.md](/mnt/c/Users/butle/AppData/Local/Temp/10x-autore... |
| sha256-1fc1e0ee85ac4e38186bfdef16c19f19bb06b707dfd576a1d9bb5fd76a05b40b.json | .10x/tickets/2026-06-25-account-export-hardening-parent.md, .10x/tickets/2026-06-28-remove-email-from-account-export-operator-docs.md | none | 15 | 9 | Distinct owner needed. The existing email-redaction ticket explicitly excludes operator docs, while `docs/account-export.md` still lists `email` against the ... |
| sha256-33d9c40517323e4e547cf18e949da93286aeb9f56966ecb70422ef1d6fa07fe6.json | .10x/tickets/2026-06-25-account-export-hardening-parent.md, .10x/tickets/2026-06-28-align-account-export-operator-docs.md | none | 19 | 9 | Yes, the stale operator docs need a durable owner distinct from the existing email-redaction test ticket.<br><br>I created [2026-06-28-align-account-export-operato... |
| sha256-de6b00378e14acb53ed5abcca72b88777dda64ac49bdfc2372a064330a47f7ee.json | .10x/tickets/2026-06-25-account-export-hardening-parent.md, .10x/tickets/2026-06-28-remove-account-export-email-from-operator-docs.md | none | 13 | 9 | Inspected the account export spec, parent/test tickets, source, tests, and operator docs.<br><br>Decision: the stale operator docs need a distinct durable owner. T... |

## Scientist Inspection

This report does not grade, aggregate, or promote a candidate.

Inspect the raw transcript, command artifacts, workspace manifest, changed files, and expected behavior for each scenario. Record rubric judgments, verdicts, limits, and any promotion or rejection rationale in durable `.10x/research/`, `.10x/evidence/`, or `.10x/reviews/` records.

## Report Limits

- This report is a secondary view over saved trial artifacts.
- Unknown means the field was absent, null, or not numeric in the loaded artifact.
- The runner does not replace the LLM researcher's rubric inspection.
