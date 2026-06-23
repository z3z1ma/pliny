Status: recorded
Created: 2026-06-23
Updated: 2026-06-23
Target: autoresearch/run_codex_subject.py, autoresearch/tests/test_run_codex_subject.py, .10x/tickets/done/2026-06-23-isolate-live-subject-workspaces.md
Verdict: pass

# Live Subject Workspace Isolation Review

## Target

The change to `autoresearch/run_codex_subject.py` that executes each live Codex
subject sample in a private temporary workspace and archives the finished
workspace back to the planned artifact path.

## Findings

No blocking findings.

The new regression test models the observed failure mode directly: each arm
writes `arm-marker.txt`, then later arms search their Codex working directory's
parent for prior markers. Under the old layout, the second and third arms would
see markers in sibling artifact workspaces. With the fix, the actual working
directory parent is a private temporary directory and the archived artifact
workspaces remain inspectable only after each run completes.

The runner still reports archived workspace paths in manifests and raw artifact
references, preserving report compatibility.

## Verdict

Pass. The fix addresses the candidate-contamination path observed in
`EXP-20260623-820-ticket-readiness-gate-scn006-handoff-live-micro` without
changing score definitions or candidate instructions.

## Residual Risk

This review covers sibling generated-workspace isolation only. The runner still
cannot isolate Codex system context, authenticated home state, or external
services, which remains an explicit harness limitation.
