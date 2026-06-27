# Autoresearch

`autoresearch/` contains the reusable tooling inputs for the 10x autoresearch
program: rubric and scenario catalogs, record templates, one-shot live subject
runners, trial reports, validators, candidates, seed workspaces, and diagnostics.

`.10x/` remains the durable record graph. Research conclusions, evidence,
reviews, decisions, tickets, knowledge, and skills that should survive a session
belong in `.10x/`; files here are reusable tooling inputs that help produce or
check those records.

The active operating decision is:

- `.10x/decisions/autoresearch-live-trial-scientist-inspection.md`

Core defaults:

- The LLM reasoning engine is the scientist and loop controller.
- `autoresearch/program.md` is the human-owned program.
- `run_once.py` runs exactly one registered MICRO or FULL trial.
- MICRO and FULL are scenario breadth tiers; both execute the subject harness
  when used for current-skill or candidate evaluation.
- The live runner writes the registered scientific contract, raw trial
  artifacts, command metadata, prompts, workspaces, manifests, summaries, and
  reports.
- The runner does not grade, calibrate, or promote. The scientist inspects
  artifacts against the rubric and records verdicts in `.10x/`.
- Static pass/fail canned-output scoring and hidden evaluation modes are not
  part of the active tooling surface.

## Validation

Validate static contracts from the repository root:

```bash
python3 autoresearch/validate.py
```

Run focused tests:

```bash
python3 -m unittest discover -s autoresearch/tests
```

The validator checks JSON syntax, required score and scenario IDs, catalog
shapes, cross-references, template sections, the trial seed index, live seed
workspace manifests, and the `SKILL.md` body-size budget. It does not run
subject-agent experiments, grade transcripts, or produce verdicts.

## Research Program

The core autoresearch loop is in `autoresearch/program.md`. It is a human-owned
program for the LLM researcher, not a Python daemon or controller. Autoresearch
agents read it before experimenting and do not edit it unless a human explicitly
asks for a program change.

One iteration is:

1. state the hypothesis;
2. create or choose one candidate, or run a current-skill regression trial;
3. register one experiment definition;
4. run `autoresearch/run_once.py`;
5. inspect raw trial artifacts and the report;
6. record verdict, limits, and evidence references in durable `.10x/` records;
7. keep, discard, mutate, branch, retry, or promote for human review.

Python utilities do not own the loop. They run one trial, validate contracts,
render artifact reports, or run diagnostics.

## Codex Subject Runner

Run a registered MICRO or FULL experiment through live Codex subject-agent calls:

```bash
python3 autoresearch/run_codex_subject.py --experiment path/to/experiment.md --run --out .10x/evidence/.storage/<run-tag>/<experiment-id>
```

MICRO and FULL are scenario breadth tiers. MICRO uses narrow scenarios that
target one behavior; FULL uses broader scenario coverage. Both can execute the
same live harness. `codex-cli` prompt definitions are live subject runs.

The runner writes:

- `<out>/plan.json`
- `<out>/summary.json`
- `<out>/raw/*.json`
- `<out>/codex/*.command.json`
- `<out>/codex/*.stdout.jsonl`
- `<out>/codex/*.stderr`
- `<out>/codex/*.last-message.txt`
- `<out>/prompts/*.prompt.txt`
- `<out>/workspaces/*/workspace-manifest.json`
- archived subject workspaces under `<out>/workspaces/`

Full prompts are kept as prompt artifacts. Raw trial transcripts contain only
the scenario conversation, so quoted wrapper instructions are not mistaken for
subject behavior.

If a subject asks a clarifying question, the LLM researcher inspects the raw
transcript and registers a one-turn continuation. Use `prior_raw_paths` to point
each arm at its prior raw artifact. Use `prompts_by_arm` when different arms
asked different questions:

```json
{
  "id": "SCN-001",
  "prior_raw_paths": {
    "no-10x-control": ".10x/evidence/.storage/run/raw/control.json",
    "current-10x": ".10x/evidence/.storage/run/raw/current.json",
    "candidate-variant": ".10x/evidence/.storage/run/raw/candidate.json"
  },
  "prompts_by_arm": {
    "no-10x-control": "The widget should show archived items only when the user enables Show archived.",
    "current-10x": "The intended behavior is archived items hidden by default, shown when Show archived is enabled.",
    "candidate-variant": "Use the existing Show archived toggle; no new filtering modes are in scope."
  }
}
```

Each continuation runs one new Codex turn against the prior transcript and
workspace. The researcher, not the runner, decides whether another continuation
is needed or whether the turn is ready for a verdict.

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
generate candidates, grade outputs, or mutate canonical `SKILL.md`. The LLM
researcher follows `autoresearch/program.md` and calls `run_once.py` repeatedly.

For exploratory work before setup is committed, omit `--require-clean-canonical`;
the command still writes `<out>/canonical_guard.json` and fails if `SKILL.md` or
`autoresearch/program.md` changes during the run.

The required experiment definition fields are:

```json
{
  "experiment_id": "EXP-20260627-101-example",
  "method_tier": "MICRO",
  "model": "codex-cli-default",
  "harness": "codex-cli",
  "repetitions": 1,
  "scientific_contract": {
    "question": "Does the current skill avoid unnecessary framework work in a trivial toggle request?",
    "hypothesis": "The current skill will prefer the smallest native edit and explain why a framework is unnecessary.",
    "expected_behavior": "The subject chooses a native toggle implementation or directly rejects the unnecessary framework.",
    "inspection_criteria": [
      "command exits are zero",
      "response or diff avoids adding a framework dependency",
      "archived workspace contains only task-relevant edits"
    ],
    "quality_floor": "No dependency, architecture rewrite, or unrelated record mutation is introduced.",
    "verdict_record_path": ".10x/evidence/EXP-20260627-101-example-result.md"
  },
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
      "prompt": "Add a framework so the toggle can show or hide details.",
      "workspace_procedure": "Use a clean seed workspace with a small existing toggle implementation, then archive the resulting workspace."
    }
  ],
  "budget": {
    "max_harness_runs": 3,
    "estimated_wall_seconds_per_run": 600,
    "timeout_seconds_per_run": 1800
  }
}
```

The `arms` array is exact. A one-arm smoke or current-skill regression lists one
arm. A comparative experiment lists each control, baseline, current, and
candidate arm explicitly.

Use `autoresearch/splits/skill-improvement-v1.json` to separate exploration
scenarios from held-out review scenarios.

## Reporting

Generate a readable Markdown report from saved trial artifacts:

```bash
python3 autoresearch/report.py --artifacts .10x/evidence/.storage/<run-tag>/<experiment-id> --out path/to/report.md
```

Include manual campaign-level verdict metadata without mutating raw artifacts:

```bash
python3 autoresearch/report.py --artifacts .10x/evidence/.storage/<run-tag>/<experiment-id> --campaign path/to/campaign.json --out path/to/report.md
```

The report is a secondary view. It shows trial samples, scenario/arm coverage,
the registered scientific contract, command exits, time/token fields when
available, changed files, raw references, archived workspace paths, and a
reminder of the required scientist inspection. Missing fields render as
`unknown` instead of failing report generation.

`report.py` does not run experiments, grade raw artifacts, make promotion
decisions, or compute an aggregate that could hide component failures.

## Seed Workspaces

`autoresearch/trial-seeds/` contains live trial seed workspaces and prior
raw artifacts. These are not pass/fail answer keys; they are clean-room
starting states for fresh subject-agent trials.

Start seed selection from `autoresearch/trial-seeds/index.json`. It is the
first-class registry for seed purpose, target scenario, target rubrics,
conditions created, known traps, prompt family, material records, material
source files, raw artifact path, workspace manifest path, and workspace
procedure.

Regenerate the index after adding, removing, or materially changing seeds:

```bash
python3 autoresearch/build_trial_seed_index.py
```

Then validate:

```bash
python3 autoresearch/validate.py
```

Experiment records can use these seeds through `prior_raw_path` or
`prior_raw_paths`. The runner copies the seed workspace into a private temporary
workspace, runs the subject, then archives the resulting workspace under the
experiment output directory.

## Manual Scoring

Manual scoring is scientist judgment, not runner output. Use
`autoresearch/catalogs/scores.json` to choose the relevant S001-S009 rubric
labels, inspect the raw transcript and workspace artifacts, then record numeric
or qualitative judgments with confidence, rationale, evidence references,
unsupported assumptions, and any floor triggers.

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
