Status: recorded
Created: 2026-06-28
Updated: 2026-06-28
Relates-To: .10x/research/2026-06-28-record-richness-hypothesis-search.md, .10x/tickets/done/2026-06-28-broaden-record-richness-experiments.md, SKILL.md

# Record Richness Hypothesis Batch

## What Was Observed

Two live autoresearch batches tested `S010` record richness hypotheses against
the canonical `SKILL.md`.

- First batch: five scenarios x six arms = 30 live Codex samples.
- Second-stage confirmation: five scenarios x two arms x two repetitions = 20
  live Codex samples.
- Total: 50 live samples.
- Scenarios: external canonical PRD indexing, account-export record economy,
  invoice retry ticket handoff, redacted evidence capture, and noisy
  retrospective learning.
- All canonical guards reported unchanged `SKILL.md` and
  `autoresearch/program.md` during each run.
- Runner promotion was `not-performed` for every experiment.

Persisted artifact roots:

- `.10x/evidence/.storage/2026-06-28-record-richness-hypothesis-search/`
- First-batch experiment definitions under
  `.10x/research/.storage/2026-06-28-record-richness-hypothesis-search/`
- Second-stage experiment definitions under the same research storage path.

## Procedure

The canonical skill was first rolled back to the pre-promotion wording. Five
parallel first-batch experiments compared current 10x against five candidate
overlays:

- `record-regeneration-check`, 796 overlay chars.
- `source-material-delta-audit`, 697 overlay chars.
- `executor-handoff-contract`, 566 overlay chars.
- `record-economy-density`, 520 overlay chars.
- `audit-limits-redaction`, 444 overlay chars.

After inspecting the first-batch artifacts, a synthesized 457-character
`cold-start-record-handoff-check` candidate was created and tested against
current 10x with two repetitions on the same five scenarios. The canonical
promotion uses a 297-character compression of the same behavior to satisfy the
`SKILL.md` 40k body budget.

Manual scoring used `S010` judgment: cold-start completeness, provenance,
edge cases, actionability, evidence/limits, cross-record coherence, and economy.
Scores are subjective 0-10 researcher judgments from the raw artifacts, not an
automated metric.

## Score Summary

| Candidate | Chars | Mean S010 | Uplift vs current | Finding |
| --- | ---: | ---: | ---: | --- |
| current controls | 0 | 8.7 | baseline | Strong already; high variance on external indexing. |
| record-regeneration-check | 796 | 8.7 | 0.0 | Not enough uplift for the size; original promotion was not justified. |
| source-material-delta-audit | 697 | 9.2 | +0.5 | Highest raw richness on retrospective/source-loss tasks, but verbose and slower. |
| executor-handoff-contract | 566 | 9.2 | +0.5 | Best first-batch ticket handoff and record-economy ergonomics. |
| record-economy-density | 520 | 9.1 | +0.4 | Useful economy guard, but sometimes compressed independent spec surfaces. |
| audit-limits-redaction | 444 | 9.1 | +0.4 | Best evidence/redaction and conservative external blocking, weaker retrospective closure. |
| cold-start-record-handoff-check | 457 tested / 297 canonical | 9.2 | +0.5 | Best uplift-per-character; near source/executor quality with lower instruction cost. |

Second-stage current-vs-v2 scenario scores:

| Scenario | Current | V2 | Result |
| --- | ---: | ---: | --- |
| `SCN-004` external PRD index | 7.8 | 9.2 | V2 recovered PRD provenance and source blockers more consistently. |
| `SCN-005` record economy | 8.7 | 9.1 | V2 preserved distinct docs-gap ownership and references better. |
| `SCN-006` ticket handoff | 9.2 | 9.2 | Tie; current best replicate was already excellent. |
| `SCN-008` evidence audit | 9.3 | 9.1 | Slight current edge; v2 remained acceptable. |
| `SCN-012` retrospective learning | 9.1 | 9.3 | V2 improved blocked follow-up and noise filtering consistency. |

## What This Supports Or Challenges

Supports promoting the compact `cold-start-record-handoff-check` behavior into
canonical `SKILL.md` using the compressed budget-fitting wording. The candidate
improved or tied current behavior in four of five second-stage scenarios and
had only a small, non-floor evidence-capture regression.

Challenges promoting the original `record-regeneration-check`; it did not
outperform current strongly enough to justify 796 added characters.

Challenges promoting the larger source-delta or executor-handoff overlays as-is:
they produced strong artifacts, but their benefits were mostly captured by the
shorter synthesized candidate.

## Limits

- All live samples used the Codex CLI harness and the available authenticated
  model/provider state.
- Manual scoring remains judgment-based.
- The second-stage v2 evidence includes only two repetitions per scenario.
- The raw archived workspaces and Codex stdout files were retained locally under
  ignored storage during the run; the durable baseline commit preserves summary,
  plan, report, canonical guard, and raw JSON artifacts.
