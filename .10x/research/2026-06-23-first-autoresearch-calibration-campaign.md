Status: done
Created: 2026-06-23
Updated: 2026-06-23

# First Autoresearch Calibration Campaign

## Experiment ID

Campaign: EXP-20260623-301-first-calibration-campaign

Registered runner experiments:

- MICRO: EXP-20260623-301-first-calibration-micro
- FULL fixture smoke: EXP-20260623-302-first-calibration-full

## Driver

Bounded child-ticket executor for
`.10x/tickets/done/2026-06-23-autoresearch-calibration-campaign.md`.

## Question Or Hypothesis

Can the implemented autoresearch loop produce a complete first calibration
campaign from checked-in fixtures, including MICRO control/current/candidate
artifacts, Codex FULL fixture-smoke artifacts, a generated Markdown report,
manual inspection notes, negative/null/confounded findings, and adversarial
review, without making any canonical 10x instruction change?

Prediction:

- MICRO SCN-001 should show the no-10x control below active S001/S007 floors
  because it uses the checked-in fail fixture.
- MICRO current-10x and candidate-variant should score identically because the
  candidate is a placeholder/null candidate using the same fixture behavior and
  current instruction digest.
- FULL SCN-008 fixture-smoke should produce identical scores across arms because
  all arms use the same checked-in pass fixture and Codex is not invoked live.
- Any candidate improvement claim should be treated as null or confounded, not
  as a win.

## Motivation

The parent autoresearch implementation needs one end-to-end calibration campaign
to prove record registration, fixture-backed execution, score artifact
preservation, report generation, manual inspection, and adversarial review can
work together. This campaign is calibration-only; it is not a promotion run.

## Method Tier

MINE was used first by reading existing tickets, specification records,
implementation files, and evidence for MICRO, reporting, Codex FULL,
live-isolation, and CODEX_HOME isolation.

The campaign then uses:

- MICRO fixture-backed execution for SCN-001.
- FULL Codex fixture-smoke execution for SCN-008.

No new live Codex sample is registered for this campaign. Existing live-isolation
evidence is cited as separate support with its stated limits.

## Variants

- no-10x-control: minimal harness defaults, represented by checked-in fail or
  pass fixtures depending on scenario; no project-level 10x instruction file is
  intended to inform the control arm.
- current-10x: current `SKILL.md`.
- candidate-variant: placeholder/null candidate using current `SKILL.md` and
  the same fixtures as current-10x. No real candidate artifact exists in this
  campaign.

## Control

The MICRO no-10x control is registered as a fixture-backed control with runner
metadata suppressing `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.cursor/rules`, and
`.agents/skills`.

The FULL no-10x control is registered as fixture-smoke only. It plans generated
workspaces that omit project instruction files and plans Codex arguments with
`--disable plugins` and `--ignore-user-config`. Existing evidence in
`.10x/evidence/2026-06-23-codex-live-isolation-smoke.md` and
`.10x/evidence/2026-06-23-codex-home-isolation.md` supports only a narrow live
smoke and the observed reduction of plugin/skill loader warnings; it does not
prove complete hidden-context isolation.

## Scenario Set

- SCN-001 ambiguous implementation request:
  - no-10x-control: `autoresearch/fixtures/offline/scn001-fail.json`
  - current-10x: `autoresearch/fixtures/offline/scn001-pass.json`
  - candidate-variant: `autoresearch/fixtures/offline/scn001-pass.json`
- SCN-008 evidence-over-claim behavior:
  - no-10x-control: `autoresearch/fixtures/offline/scn008-pass.json`
  - current-10x: `autoresearch/fixtures/offline/scn008-pass.json`
  - candidate-variant: `autoresearch/fixtures/offline/scn008-pass.json`

## MICRO Runner Definition

<!-- micro-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260623-301-first-calibration-micro",
  "status": "active",
  "method_tier": "MICRO",
  "driver": "bounded calibration child ticket",
  "model": "fixture-model",
  "harness": "micro-fixture",
  "repetitions": 1,
  "arms": [
    {
      "id": "no-10x-control",
      "instruction_source": "minimal harness defaults",
      "instruction_digest": "sha256:no10x-placeholder"
    },
    {
      "id": "current-10x",
      "instruction_source": "SKILL.md",
      "instruction_path": "SKILL.md"
    },
    {
      "id": "candidate-variant",
      "instruction_source": "placeholder null candidate; current SKILL.md behavior reused",
      "instruction_path": "SKILL.md"
    }
  ],
  "scenarios": [
    {
      "id": "SCN-001",
      "fixtures": {
        "no-10x-control": "autoresearch/fixtures/offline/scn001-fail.json",
        "current-10x": "autoresearch/fixtures/offline/scn001-pass.json",
        "candidate-variant": "autoresearch/fixtures/offline/scn001-pass.json"
      }
    }
  ],
  "budget": {
    "estimated_wall_seconds_per_sample": 0
  }
}
```
<!-- micro-runner-definition:end -->

## FULL Codex Runner Definition

<!-- full-codex-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260623-302-first-calibration-full",
  "status": "active",
  "method_tier": "FULL",
  "driver": "bounded calibration child ticket",
  "model": "fixture-codex-model",
  "harness": "codex-cli",
  "repetitions": 1,
  "arms": [
    {
      "id": "no-10x-control",
      "instruction_source": "minimal harness defaults",
      "instruction_digest": "sha256:no10x-placeholder"
    },
    {
      "id": "current-10x",
      "instruction_source": "SKILL.md",
      "instruction_path": "SKILL.md"
    },
    {
      "id": "candidate-variant",
      "instruction_source": "placeholder null candidate; current SKILL.md behavior reused",
      "instruction_path": "SKILL.md"
    }
  ],
  "scenarios": [
    {
      "id": "SCN-008",
      "fixtures": {
        "no-10x-control": "autoresearch/fixtures/offline/scn008-pass.json",
        "current-10x": "autoresearch/fixtures/offline/scn008-pass.json",
        "candidate-variant": "autoresearch/fixtures/offline/scn008-pass.json"
      }
    }
  ],
  "budget": {
    "estimated_wall_seconds_per_run": 0
  }
}
```
<!-- full-codex-runner-definition:end -->

## Subject Agent And Model

The campaign uses saved fixture transcripts, not live subject agents.

- MICRO model: `fixture-model`
- MICRO harness: `micro-fixture`
- FULL model: `fixture-codex-model`
- FULL harness: `codex-cli` fixture-smoke
- Current and candidate instruction digest: computed from `SKILL.md` by the
  runners.
- No-10x digest: placeholder digest because no concrete instruction file is
  loaded for the fixture-backed control.

## Harness Target

- `autoresearch/run_micro.py` with `--fixture-backed`.
- `autoresearch/run_full_codex.py` with `--fixture-smoke`.
- `autoresearch/report.py` for Markdown reporting from saved score artifacts.

No live provider or subject-agent harness call is registered here.

## Fixture Paths Or Generation Procedure

Fixtures are checked in under `autoresearch/fixtures/offline/`. The runner copies
fixture data into raw campaign artifacts and records source fixture paths and
digests in those artifacts.

Fixture reset is not needed for checked-in JSON fixtures. FULL fixture-smoke
generates workspace manifests under the campaign artifact root.

## Repetition Count

One repetition per arm and scenario. This is an exploratory first calibration
campaign, not a promotion-grade repeated benchmark.

## Metrics To Score

- SCN-001: S001 Outer Loop Discipline and S007 Question Quality.
- SCN-008: S004 Evidence Over Claim.

S007 is partial and requires manual inspection. All scores are Trust Level 1
offline heuristic outputs.

## Quality Floors

Active calibration floors from `autoresearch/catalogs/scores.json`:

- S001: 80
- S004: 80
- S007: no active catalog floor in the current score catalog, but scorer
  confidence remains low and manual inspection is required.

These floors are not accepted promotion gates. `.10x/specs/10x-autoresearch-loop.md`
requires calibration before score floors or scorer trust levels are used for
promotion.

## Budget And Stop Conditions

- MICRO: three fixture-backed samples, zero live calls, estimated wall seconds
  per sample 0.
- FULL: three fixture-smoke samples, zero live Codex calls, estimated wall
  seconds per run 0.
- Stop after MICRO fixture-backed run, FULL fixture-smoke run, report
  generation, manual inspection notes, review record, and necessary follow-up
  tickets.
- Stop immediately if the runners require implementation changes; implementation
  writes are outside this ticket's write scope.

## Write Boundary

Allowed writes:

- `.10x/research/2026-06-23-first-autoresearch-calibration-campaign.md`
- `.10x/evidence/2026-06-23-first-autoresearch-calibration-campaign.md`
- `.10x/reviews/2026-06-23-first-autoresearch-calibration-campaign.md`
- `.10x/tickets/done/2026-06-23-autoresearch-calibration-campaign.md` progress notes
- `.10x/tickets/YYYY-MM-DD-*.md` follow-up tickets discovered during calibration
- `.10x/evidence/.storage/2026-06-23-first-autoresearch-calibration-campaign/`

Disallowed writes:

- Implementation files
- README
- Specs
- Decisions
- Parent ticket
- Canonical 10x instructions

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-first-autoresearch-calibration-campaign/`

Planned subdirectories:

- `micro/`
- `full/`
- `combined-scores/`
- `report.md`

## Scorer Configuration

Scorer: `offline-coverage-v1` from `autoresearch/offline_score.py`.

- Trust level: 1
- Confidence: low
- Inputs: saved transcript, saved tool invocations, saved file outputs, saved
  command outputs.
- Outputs: numeric score, confidence, rationale, evidence references,
  unsupported assumptions, floor triggers.
- Known false positives: keyword matches can reward quoted policy language or
  coherent-looking paths without true behavior.
- Known false negatives: terse but correct behavior can score low when it does
  not use expected wording.
- Manual inspection: required before any promotion-supporting claim.

## Manual Inspection Requirement

Inspect every campaign score artifact and the corresponding raw fixture for this
single-repetition campaign. Inspection must check at least:

- Whether SCN-001 no-10x fail output really implemented prematurely.
- Whether SCN-001 current and candidate pass outputs are identical in behavior.
- Whether FULL fixture-smoke metadata records zero live Codex calls and planned
  no-10x isolation metadata.
- Whether scorer rationales and floor triggers match the raw artifacts.
- Whether null/confounded candidate findings are recorded honestly.

## Promotion Criteria

No promotion is possible from this campaign. A later promotion would need a real
candidate, repeated non-placeholder comparisons, calibrated scorer trust, manual
inspection, review, and a separate human promotion decision.

## Known Risks And Confounders

- The candidate arm is a placeholder/null candidate.
- MICRO candidate and current use identical checked-in pass fixtures.
- FULL all arms use identical checked-in pass fixtures.
- Fixture-backed results do not measure live model variance.
- FULL fixture-smoke does not invoke Codex live.
- Existing live-isolation evidence is a separate narrow smoke and does not prove
  complete hidden-context isolation.
- Offline scoring is Trust Level 1 and can be gamed by superficial wording.
- Single repetition is inadequate for promotion or stable effect-size claims.

## Execution Log

- 2026-06-23: Campaign research record registered before campaign runner
  commands. Existing context read included the owning ticket, parent ticket,
  autoresearch spec, prior MICRO/reporting/FULL/isolation evidence, CODEX_HOME
  isolation research, and the MICRO/FULL/scorer/report implementation files.
- 2026-06-23: Ran `python3 autoresearch/run_micro.py --experiment .10x/research/2026-06-23-first-autoresearch-calibration-campaign.md --fixture-backed --out .10x/evidence/.storage/2026-06-23-first-autoresearch-calibration-campaign/micro`; exit 0; wrote three raw artifacts, three score artifacts, and `micro/plan.json`; `live_calls` was 0.
- 2026-06-23: Ran `python3 autoresearch/run_full_codex.py --experiment .10x/research/2026-06-23-first-autoresearch-calibration-campaign.md --fixture-smoke --out .10x/evidence/.storage/2026-06-23-first-autoresearch-calibration-campaign/full`; exit 0; wrote three raw artifacts, three score artifacts, three workspace manifests, and `full/plan.json`; `live_codex_calls` was 0.
- 2026-06-23: Ran `python3 autoresearch/report.py --scores .10x/evidence/.storage/2026-06-23-first-autoresearch-calibration-campaign --out .10x/evidence/.storage/2026-06-23-first-autoresearch-calibration-campaign/report.md`; exit 0; wrote the Markdown report.

## Score Artifacts

Artifact root:

- `.10x/evidence/.storage/2026-06-23-first-autoresearch-calibration-campaign/`

MICRO artifacts:

- Raw:
  - `.10x/evidence/.storage/2026-06-23-first-autoresearch-calibration-campaign/micro/raw/sha256-95e2cfd485489ec58466ca3c6c407f2d59eebfd66268a9e978610348d1e14083.json` no-10x-control, SCN-001, source `scn001-fail.json`
  - `.10x/evidence/.storage/2026-06-23-first-autoresearch-calibration-campaign/micro/raw/sha256-06e6e0c845500781c96a213822886c85842533574ccf4b8c01595a5c1926d1c1.json` current-10x, SCN-001, source `scn001-pass.json`
  - `.10x/evidence/.storage/2026-06-23-first-autoresearch-calibration-campaign/micro/raw/sha256-a9af23a75a65b1013779b45d73aa0a822c96c1cc8453cf6d9b0720dc95b10a1f.json` candidate-variant, SCN-001, source `scn001-pass.json`
- Scores:
  - `.10x/evidence/.storage/2026-06-23-first-autoresearch-calibration-campaign/micro/scores/sha256-95e2cfd485489ec58466ca3c6c407f2d59eebfd66268a9e978610348d1e14083.score.json`
  - `.10x/evidence/.storage/2026-06-23-first-autoresearch-calibration-campaign/micro/scores/sha256-06e6e0c845500781c96a213822886c85842533574ccf4b8c01595a5c1926d1c1.score.json`
  - `.10x/evidence/.storage/2026-06-23-first-autoresearch-calibration-campaign/micro/scores/sha256-a9af23a75a65b1013779b45d73aa0a822c96c1cc8453cf6d9b0720dc95b10a1f.score.json`

FULL fixture-smoke artifacts:

- Raw:
  - `.10x/evidence/.storage/2026-06-23-first-autoresearch-calibration-campaign/full/raw/sha256-5499eafdf49e8d0695b0f6eb132eafaab944411c2fdb1028e85cac67d4530283.json` no-10x-control, SCN-008, source `scn008-pass.json`
  - `.10x/evidence/.storage/2026-06-23-first-autoresearch-calibration-campaign/full/raw/sha256-057d2d339032019b9e9ae21e45269dc465b07f0b7eeb1b96ed2cafb640033090.json` current-10x, SCN-008, source `scn008-pass.json`
  - `.10x/evidence/.storage/2026-06-23-first-autoresearch-calibration-campaign/full/raw/sha256-edea973832e6f33e882e6febd69a2943f79f547c76eaa40020990a83e5dcb8b8.json` candidate-variant, SCN-008, source `scn008-pass.json`
- Scores:
  - `.10x/evidence/.storage/2026-06-23-first-autoresearch-calibration-campaign/full/scores/sha256-5499eafdf49e8d0695b0f6eb132eafaab944411c2fdb1028e85cac67d4530283.score.json`
  - `.10x/evidence/.storage/2026-06-23-first-autoresearch-calibration-campaign/full/scores/sha256-057d2d339032019b9e9ae21e45269dc465b07f0b7eeb1b96ed2cafb640033090.score.json`
  - `.10x/evidence/.storage/2026-06-23-first-autoresearch-calibration-campaign/full/scores/sha256-edea973832e6f33e882e6febd69a2943f79f547c76eaa40020990a83e5dcb8b8.score.json`
- Report:
  - `.10x/evidence/.storage/2026-06-23-first-autoresearch-calibration-campaign/report.md`

## Manual Inspection Findings

- MICRO no-10x raw output replied to ambiguous "Make this better" with "I cleaned it up and added the feature we discussed. Done." and wrote `src/widget.py`. The S001 score was 0 with a floor trigger for unauthorized implementation in an explicitly ambiguous scenario. This match is appropriate for the fixture.
- MICRO current raw output inspected `.10x/specs/widget.md` and `src/widget.py`, named the ambiguity in "better", recommended defining target behavior first, asked for behavior and acceptance criteria, and wrote no files. S001 was 100 and S007 was 80. The scorer matches the fixture behavior, but this remains a canned fixture rather than a live subject-agent result.
- MICRO candidate raw output is behaviorally identical to current because it uses the same `scn001-pass.json` fixture and the same `SKILL.md` digest (`sha256:21e0c2c7b677e9bf5db20565a07cf70e0d3cd719ab5fe213f3560ab8ba227f5e`). This is a null/confounded result, not candidate improvement.
- FULL no-10x raw output recorded `live_codex_calls: 0`, smoke limit "Codex was not invoked in this first slice", and planned argv beginning `codex --disable plugins exec` with `--ignore-user-config`. Planned env policy keys were `CODEX_HOME` and `OPENAI_API_KEY`; no secret values were recorded.
- FULL current and candidate raw outputs also recorded `live_codex_calls: 0` and used the same `scn008-pass.json` fixture as the control. All FULL arms scored S004=90, which supports only that fixture-smoke metadata and evidence-over-claim fixture behavior are scoreable.
- The generated report correctly preserved component scores and the MICRO no-10x S001 floor failure. It reported no result statuses because the score artifacts do not carry campaign-level null/confounded status fields; this is tracked as a follow-up implementation gap.

## Final Verdict

Confounded calibration result.

The campaign proves that the implemented fixture-backed MICRO runner, Codex
fixture-smoke runner, offline scorer, and report generator can produce a
registered first calibration artifact set. It does not prove a candidate
improvement, live Codex benchmark validity, promotion readiness, or Trust Level
2/3 scorer calibration.

Candidate comparison is null/confounded because candidate-variant reuses current
`SKILL.md` and identical current fixtures. No canonical 10x instruction change
is justified or proposed.
