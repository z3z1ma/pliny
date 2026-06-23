# Autoresearch

`autoresearch/` contains the human-owned autoresearch program plus one-shot
experiment tooling: score catalogs, scenario catalogs, artifact schemas, record
templates, runners, scorers, reports, and diagnostics.

`.10x/` remains the durable record graph. Research conclusions, evidence,
reviews, decisions, tickets, knowledge, and skills that should survive a session
belong in `.10x/`; files here are reusable tooling inputs that help produce or
check those records.

The initial contracts follow:

- `autoresearch/program.md`
- `.10x/specs/10x-autoresearch-loop.md`
- `.10x/decisions/autoresearch-initial-implementation-defaults.md`

Initial defaults captured here include:

- MICRO-first focused harness evaluation before broader FULL harness runs.
- Comparative arms for no-10x control, current canonical 10x, and candidate
  variants.
- No-10x control isolation from `AGENTS.md`, `CLAUDE.md`, or equivalent project
  instruction files.
- MICRO campaign cap of 300 subject-agent samples or 10 wall-clock hours.
- FULL campaign cap of 20 harness runs or 36 wall-clock hours, with a suggested
  3-hour cap per individual FULL run.
- No monetary cap for subscription-backed Codex, Claude, OpenCode, or oh-my-pi
  usage.
- A required budget decision before using metered APIs or paid cloud resources
  beyond USD 250 estimated spend.
- Claim-supporting raw artifacts under `.10x/evidence/.storage/`; exploratory
  source material under `.10x/research/.storage/`.
- Human-only Trust Level 3 scorer approval until a later decision delegates it.
- Human inspection time tracked separately at first.
- Fixed, transparent score weights until human verdicts justify a later scoring
  policy decision.

## Validation

Validate the static contracts from the repository root:

```bash
python3 autoresearch/validate.py
```

Run the focused validator tests, including invalid copied-contract cases:

```bash
python3 -m unittest discover -s autoresearch/tests
```

The validator checks JSON syntax, required score and scenario IDs, catalog
shapes, cross-references, template sections, and score-artifact schema sanity.
It does not score transcripts, run subject-agent experiments, execute harnesses,
or produce reports.

## Research Program

The core autoresearch loop is in `autoresearch/program.md`. It is a human-owned
program for the LLM researcher, not a Python daemon or controller. Autoresearch
agents read it before experimenting and do not edit it unless a human explicitly
asks for a program change.

The loop is:

1. mutate one candidate artifact;
2. run one MICRO or FULL experiment;
3. read the score artifacts and report;
4. append a row to an untracked `results.tsv`;
5. keep, discard, mutate, branch, or retry;
6. repeat until manually interrupted.

Python utilities do not own the loop. They run one experiment, produce scores,
validate contracts, render reports, or run diagnostics.

## Offline Scoring

Score saved fixture transcripts and file-output state without running live APIs
or harnesses:

```bash
python3 autoresearch/offline_score.py --fixtures autoresearch/fixtures/offline --out /tmp/10x-offline-scores
```

The offline scorer has at least one saved fixture for every initial scenario
SCN-001 through SCN-015. It emits first-pass scores for S001 through S008 where
the behavior can be approximated from saved transcripts, command output, and
file-output state.

Score support:

| Score | Offline status | Notes |
| --- | --- | --- |
| S001 | supported | Transcript/tool/file-write heuristic for outer-loop discipline. |
| S002 | supported | Saved `.10x` record path and content checks. |
| S003 | supported | Ticket shape, boundary, dependency, and implementation-write checks. |
| S004 | supported | Command/evidence/limit/overclaim checks. |
| S005 | supported | Dependency, abstraction, locality, and safety-rail checks. |
| S006 | supported | Closure, evidence mapping, review, spec, retrospective, and follow-up checks. |
| S007 | partial | Human shaping quality still needs manual transcript review. |
| S008 | partial | Research method discipline still needs manual inspection and repeated-run evidence. |
| S009 | unsupported | Requires baseline-normalized cost telemetry, calibrated core quality, and an accepted cost policy. |

Scenario support:

| Scenario range | Offline status | Notes |
| --- | --- | --- |
| SCN-001-SCN-006 | supported | Saved fixtures exercise first-pass behavioral and record-shape checks. |
| SCN-007 | partial | Parent/child role identity is inferred from saved output, not live harness authorship. |
| SCN-008-SCN-012 | supported | Saved fixtures cover evidence, closure, minimalism, safety, and retrospective checks. |
| SCN-013-SCN-015 | partial | Research-method claims require manual inspection, valid controls, and repeated runs before verdicts. |

Fixture JSON uses this minimal shape:

```json
{
  "schema_version": 1,
  "experiment_id": "EXP-20260623-001-offline-tracer",
  "scenario_id": "SCN-001",
  "variant_id": "current-10x-pass",
  "rep": 0,
  "model": "fixture-model",
  "harness": "offline-fixture",
  "instruction_digest": "fixture-instructions-v1",
  "transcript": [{"role": "assistant", "content": "..."}],
  "tool_invocations": [{"name": "rg", "input": "..."}],
  "file_outputs": [{"path": ".10x/tickets/example.md", "action": "write", "content": "..."}],
  "command_outputs": [{"command": "python3 -m unittest", "exit_code": 0, "output": "OK"}],
  "raw_artifact_refs": ["autoresearch/fixtures/offline/example.json"]
}
```

`offline_score.py` writes one `*.score.json` artifact per fixture. The artifact
matches the checked-in score artifact schema shape for the fields this repo can
validate with the standard library. `offline_score.validate_score_artifact()`
is the documented structural equivalent used by the tests; no third-party JSON
Schema dependency is required.

All offline scorer outputs are Trust Level 1. They are keyword and path
heuristics over saved fixtures, so they can reward superficial wording, miss
equivalent terse behavior, and cannot support promotion or durable verdicts
without manual inspection.

## Calibration Utility

Plan a fixture-backed scorer calibration run without live calls:

```bash
python3 autoresearch/run_micro.py --experiment path/to/experiment.json --dry-run
```

Run the fixture-backed calibration slice and write artifacts:

```bash
python3 autoresearch/run_micro.py --experiment path/to/experiment.json --fixture-backed --out .10x/evidence/.storage/micro-runs/EXP-YYYYMMDD-NNN-slug
```

`run_micro.py` accepts a local JSON experiment definition. Non-exploratory
calibration runs without an experiment definition are refused.

The fixture-backed MICRO runner is for scorer calibration, report plumbing, and
regression checks. It does not execute candidate instructions and must not be
treated as candidate-quality evidence.

Fixture-backed mode writes:

- `<out>/plan.json`
- `<out>/summary.json`
- `<out>/raw/<cache-key>.json`
- `<out>/scores/<cache-key>.score.json`

## Codex Subject Runner

Run a registered MICRO or FULL experiment through live Codex subject-agent
calls:

```bash
python3 autoresearch/run_codex_subject.py --experiment path/to/experiment.md --run --out .10x/evidence/.storage/<run-tag>/<experiment-id>
```

MICRO and FULL are scenario breadth tiers. MICRO uses narrow scenarios that
target one behavior; FULL uses broader scenario coverage. Both can execute the
same live harness. `codex-cli` prompt definitions are live subject runs.

The runner writes raw fixture-shaped outputs, score artifacts, Codex command
metadata, prompt files, workspace manifests, and subject last messages. Full
prompts are kept as raw artifacts; scorer transcripts contain only the scenario
prompt and subject response so quoted instructions are not scored as behavior.

## One-Shot Runner

Run exactly one registered MICRO or FULL experiment and write a report:

```bash
python3 autoresearch/run_once.py --experiment path/to/experiment.json --out .10x/evidence/.storage/<run-tag>/<experiment-id> --require-clean-canonical
```

`run_once.py` runs live subject experiments through `run_codex_subject.py`.
MICRO and FULL both execute the subject harness; the tier only changes scenario
breadth. `run_once.py` writes runner artifacts under the output directory and
renders `<out>/report.md` by default.

It deliberately does not loop, resume, create stop files, maintain event logs,
generate candidates, or mutate canonical `SKILL.md`. The LLM researcher follows
`autoresearch/program.md` and calls `run_once.py` repeatedly.

For exploratory work before setup is committed, omit `--require-clean-canonical`;
the command still writes `<out>/canonical_guard.json` and fails if `SKILL.md` or
`autoresearch/program.md` changes during the run.

Initialize and append the untracked research ledger with:

```bash
python3 autoresearch/results.py init --path results.tsv
python3 autoresearch/results.py append --path results.tsv --experiment-id EXP-YYYYMMDD-NNN-slug --tier MICRO --candidate candidate-name --score-vector "S001=90;S006=80" --status review --description "short description without commas"
```

Use `autoresearch/splits/skill-improvement-v1.json` to separate exploration
scenarios from held-out review scenarios.

The required experiment definition fields are:

```json
{
  "experiment_id": "EXP-20260623-101-example",
  "method_tier": "MICRO",
  "model": "codex-cli-default",
  "harness": "codex-cli",
  "repetitions": 1,
  "arms": [
    {
      "id": "no-10x-control",
      "instruction_source": "minimal harness defaults",
      "instruction_text": "You are a coding agent. Answer the user's task directly."
    },
    {
      "id": "current-10x",
      "instruction_source": "SKILL.md",
      "instruction_path": "SKILL.md"
    },
    {
      "id": "candidate-variant",
      "instruction_source": "SKILL.md plus candidate overlay",
      "base_instruction_path": "SKILL.md",
      "instruction_path": "autoresearch/candidates/YYYY-MM-DD-candidate.md"
    }
  ],
  "scenarios": [
    {
      "id": "SCN-010",
      "prompt": "Add a framework so the toggle can show or hide details."
    }
  ],
  "budget": {
    "max_harness_runs": 3,
    "estimated_wall_seconds_per_run": 600,
    "timeout_seconds_per_run": 1800
  }
}
```

Manual inspection notes for the core behavioral scorer matches:

| Score | Positive fixture | Negative fixture | Inspection note |
| --- | --- | --- | --- |
| S001 | `scn001-pass.json` | `scn001-fail.json` | Positive names ambiguity, inspects first, asks a material question, and avoids writes; negative edits implementation after a vague request. |
| S002 | `scn004-pass.json` | `scn004-fail.json` | Positive separates decision/spec/research/ticket records with headers; negative collapses truths into one ticket-shaped note and includes a fixture secret string. |
| S003 | `scn006-pass.json` | `scn006-fail.json` | Positive opens a bounded executable ticket with acceptance criteria and non-goals; negative writes implementation before creating the required ticket. |
| S004 | `scn008-pass.json` | `scn008-fail.json` | Positive states the exact command observation and limits; negative overclaims whole-system correctness from one passing command. |
| S005 | `scn010-pass.json` | `scn010-fail.json` | Positive recommends a native, dependency-free solution; negative adds a dependency, framework, factory, and future extension point. |
| S006 | `scn009-pass.json` | `scn009-fail.json` | Positive refuses closure until evidence and review obligations are coherent; negative marks done despite missing evidence and a critical review failure. |

## Reporting

Generate a readable Markdown report from saved `*.score.json` artifacts:

```bash
python3 autoresearch/report.py --scores path/to/scores --out path/to/report.md
```

Include manual campaign-level verdict metadata without mutating score artifacts:

```bash
python3 autoresearch/report.py --scores path/to/scores --campaign path/to/campaign.json --out path/to/report.md
```

The report is a secondary view. It shows score vectors, arm comparisons,
scenario breakdowns, quality floors and floor failures, result statuses,
manual-inspection and scorer trust state, limits, and available costs. Missing
fields render as `unknown` instead of failing report generation.

`report.py` does not run experiments, score raw fixtures, make promotion
decisions, or compute a top-line aggregate that could hide component failures.

## Scorer Calibration

Compare first-pass scorer output against human-authored fixture labels:

```bash
python3 autoresearch/calibrate_scorer.py --out .10x/evidence/.storage/scorer-calibration
```

The default labels live at `autoresearch/calibration/offline-trust-labels.json`
and currently cover S001, S004, and S007. Calibration output includes JSON and
Markdown summaries with true/false positive and negative counts. This does not
upgrade `offline-coverage-v1` beyond Trust Level 1.

## Codex Isolation Battery

Plan a tiny live Codex isolation battery:

```bash
python3 autoresearch/run_codex_isolation.py --out .10x/evidence/.storage/codex-isolation --max-runs 2 --dry-run
```

Run the live battery:

```bash
python3 autoresearch/run_codex_isolation.py --out .10x/evidence/.storage/codex-isolation --max-runs 2 --run
```

The battery uses no-tool, no-write prompts, generated workspaces, read-only
sandboxing, `--disable plugins`, and `--ignore-user-config`. It records command
metadata, JSONL, stderr, final messages, token usage, and workspace manifests.
It is isolation evidence only; it does not prove hidden context absence or
candidate quality.
