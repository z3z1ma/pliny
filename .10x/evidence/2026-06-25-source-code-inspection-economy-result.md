Status: recorded
Created: 2026-06-25
Updated: 2026-06-25
Relates-To: .10x/research/2026-06-25-source-code-inspection-economy-live-micro.md

# Source-Code Inspection Economy Result

## What Was Observed

EXP-20260625-710 ran 6 live Codex subject calls:

- 1 scenario: SCN-003 source-code inspection economy;
- 3 arms: no-10x-control, current-10x, and candidate-variant with a no-op
  overlay;
- 2 repetitions per arm.

Raw artifacts are stored under:

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/187-source-code-inspection-economy-live-micro/`

Current-10x produced correct answers in both repetitions:

- identified `src/billing/statusSummary.js` as the summary surface;
- identified `src/billing/invoiceStatus.js` as the status pipeline authority;
- listed statuses `paid`, `blocked`, `overdue`, `due_soon`, and `open`;
- cited `src/billing/rules/holdRules.js` for blocked semantics;
- cited `src/billing/rules/agingRules.js` for aging semantics;
- treated `src/ui/invoiceLabels.js`, fixtures, and tests as non-authoritative
  behavior sources.

Current-10x used shell-native discovery and targeted command reads in both
repetitions. Representative command shapes:

```text
rg --files .10x
rg -n "invoice|status summary|blocked|aging|age" .10x
rg --files
sed -n '1,220p' .10x/specs/invoice-status-summary.md
sed -n '1,220p' src/billing/invoiceStatus.js
sed -n '1,220p' src/billing/rules/holdRules.js
sed -n '1,220p' src/billing/rules/agingRules.js
```

The current-10x repetitions produced no `file_outputs`. Their workspace
manifests recorded `changed_files: []`, `workspace_contamination_present:
false`, and `timed_out: false`. A manual diff against the seed workspace found
only runner-owned `workspace-manifest.json` metadata differences.

All arms used `rg`/`sed` rather than assistant-side file browsing. This means
the experiment supports current 10x conformance, but does not show a sharp
current-vs-control contrast for this seed.

Residual efficiency issue: one current-10x repetition read more files than
strictly necessary, including fixtures/tests and a second line-numbered pass
with `nl`. That is acceptable for this MICRO because it still used bounded
repo-native commands, stayed non-mutating, and answered correctly. It remains a
candidate area for a narrower future optimization around source-inspection
target precision.

Trust Level 1 automated scores under-scored all arms for S001 and some S002
cases. Manual inspection is authoritative because this experiment's primary
metric is command-shape workflow quality, which the offline scorer does not yet
measure.

## Procedure

Command run:

```text
python3 autoresearch/run_once.py --experiment .10x/research/2026-06-25-source-code-inspection-economy-live-micro.md --out .10x/evidence/.storage/2026-06-23-skill-autoresearch/187-source-code-inspection-economy-live-micro --require-clean-canonical
```

Manual inspection used:

- `report.md`
- `plan.json`
- `summary.json`
- per-sample raw JSON artifacts
- per-sample `stdout.jsonl` command events
- per-sample last messages
- current-10x workspace manifests
- manual `diff -rq` and manifest diff against the seed workspace

## What This Supports Or Challenges

This supports the claim that canonical current `SKILL.md` induces a simple
mechanical source-inspection workflow in this seed without scenario-level
prompting to use bash, `rg`, one-liners, or shell-native tools.

It also supports that the prior mechanical-tool-economy promotions did not
cause unsafe writes in a read-only source-answering scenario.

## Limits

This is one Codex CLI MICRO batch with two current repetitions. It does not
prove behavior in large repositories, non-Codex harnesses, or implementation
tasks that require deeper source tracing.

Because no-10x control also used `rg`/`sed`, this result is a conformance pass
for current 10x rather than strong evidence of unique 10x lift.
