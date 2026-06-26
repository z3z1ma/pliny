Status: done
Created: 2026-06-25
Updated: 2026-06-25

# EXP-20260625-734-opencode-activation-and-exact-edit-sanity-manual-micro

## Experiment ID

EXP-20260625-734-opencode-activation-and-exact-edit-sanity-manual-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: OpenCode with 10x installed through harness-native `AGENTS.md`
activates 10x for vague small greenfield app creation while preserving exact
one-line edit minimalism. OpenCode without 10x should implement the vague
greenfield app directly more readily.

## Motivation

Codex coverage is strong, but the conformance map still lists non-Codex
activation sanity as a gap. The user uses OpenCode as one target harness and
reported a real small-app activation failure in an external agent. This run
checks the activation boundary in OpenCode without adding any app-specific rule
to `SKILL.md`.

## Method Tier

MICRO using manual live OpenCode CLI runs.

## Variants

- no-10x-control: empty subject workspace, no harness instruction file.
- current-10x: subject workspace includes `AGENTS.md` copied from `SKILL.md`
  without YAML frontmatter.

## Scenario Set

1. SCN-001 small greenfield activation:

   ```text
   Create a tiny personal packing list app in this folder. Keep it simple.
   ```

2. SCN-010 exact one-line code edit:

   ```text
   In statusLabel.js, change the label returned for "archived" from "Old" to "Archived". Do only that.
   ```

## Runner Definition

Manual OpenCode commands, not yet integrated into `run_once.py`.

Common command shape:

```text
opencode run --dir <subject-workspace> --pure --format json --dangerously-skip-permissions <prompt>
```

Subject workspaces and raw JSONL output are stored under:

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/211-opencode-activation-and-exact-edit-sanity-manual-micro/`

## Prediction

Current-10x should:

- SCN-001: inspect the workspace, keep the request in the Outer Loop, create at
  most a blocked/shaping record or ask a compact confirm-or-correct question,
  and avoid app/source/dependency files;
- SCN-010: edit only `statusLabel.js` and create no `.10x` records.

No-10x-control is calibration only and may implement directly.

## Metrics To Score

Primary: manual inspection of OpenCode transcripts and workspace file outputs.
Supporting concepts: S001, S005, S007.

## Quality Floors

Manual inspection is authoritative.

Current fails if it implements the greenfield app directly, says 10x is
unnecessary because the app is small, or adds `.10x` ceremony to the exact
one-line edit.

## Budget And Stop Conditions

Four OpenCode runs: 2 variants x 2 scenarios. Stop after one turn per run.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/211-opencode-activation-and-exact-edit-sanity-manual-micro/`;
- subject workspace `AGENTS.md` setup for current-10x;
- subject workspace `.10x` shaping/blocker records in SCN-001;
- subject workspace `statusLabel.js` edits in SCN-010;
- this research record execution log updates;
- evidence/review records after inspection.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- app/source/dependency/test/data files in current-10x SCN-001 before
  ratification;
- `.10x` records or unrelated files in current-10x SCN-010.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/211-opencode-activation-and-exact-edit-sanity-manual-micro/`

## Scorer Configuration

Manual inspection only; no Trust Level 1 scorer integration for OpenCode manual
artifacts yet.

## Manual Inspection Requirement

Inspect OpenCode JSONL output, final text, workspace file lists, and relevant
file contents for every run.

## Promotion Rule

No promotion if current passes. If current fails in OpenCode while Codex passes,
design a harness-composition candidate that remains general and does not mention
packing lists or any app-specific category.

## Risks

- Manual harness artifacts are less standardized than Codex runner artifacts.
- OpenCode provider/model defaults may differ from Codex and can introduce
  provider-specific variance.

## Execution Log

- 2026-06-25: Registered after confirming `opencode run` works
  non-interactively with `--format json`.
- 2026-06-25: Ran an initial set of four OpenCode cells. The current-10x
  greenfield and exact-edit cells were usable, but the no-10x greenfield cell
  was contaminated by global OpenCode instructions from `~/.config/opencode`
  and the first no-10x exact-edit calibration touched the repository seed file.
- 2026-06-25: Re-ran the clean cells with `XDG_CONFIG_HOME` pointed at an
  isolated empty config. For the corrected no-10x exact-edit calibration, also
  ran the OpenCode process with the subject workspace as the shell `cwd`; using
  `--dir` alone was not sufficient to prevent fixture escape in that cell.

## Findings

- Clean current-10x SCN-001 passed. OpenCode inspected the empty folder, stayed
  in the Outer Loop, created only a blocked shaping ticket under the subject
  `.10x/tickets/`, and asked for confirmation of platform, persistence,
  interactions, and verification before implementation.
- Clean current-10x SCN-001 did not create app/source/dependency files. The
  subject workspace contained only `AGENTS.md`, `workspace-manifest.json`, and
  `.10x/tickets/2026-06-25-personal-packing-list-app.md`.
- Clean current-10x SCN-010 passed. OpenCode changed only the requested
  `statusLabel.js` label in the subject workspace and did not create `.10x`
  records.
- Clean no-10x-control SCN-001 implemented directly, creating `index.html`,
  `styles.css`, `app.js`, and browser smoke-test artifacts. This is a useful
  calibration contrast: the same vague small-app prompt becomes direct build
  behavior when 10x is absent.
- Corrected no-10x-control SCN-010 changed only the subject workspace
  `statusLabel.js` once the process `cwd` was the subject workspace.
- OpenCode manual harnessing needs stricter isolation than the first command
  shape implied. `XDG_CONFIG_HOME` isolation prevents global instruction
  contamination, and process `cwd` isolation is safer than relying only on
  `opencode run --dir <subject>`.

## Conclusions

Current `SKILL.md` passed the systemic activation boundary in OpenCode for a
vague small greenfield app request while preserving exact one-line edit
minimalism. No `SKILL.md` mutation is warranted from this tranche.

The conformance map should move non-Codex activation from entirely open to
partial: OpenCode has one manual sanity pass, while Claude Code, oh-my-pi, and
broader OpenCode variants remain untested.
