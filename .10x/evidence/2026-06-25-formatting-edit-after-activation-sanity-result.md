Status: recorded
Created: 2026-06-25
Updated: 2026-06-25
Relates-To: .10x/research/2026-06-25-formatting-edit-after-activation-sanity-live-micro.md

# Formatting Edit After Activation Sanity Result

## What was observed

EXP-20260625-727-formatting-edit-after-activation-sanity-live-micro ran one live
Codex MICRO iteration with 9 total subject calls:

- 3 `no-10x-control` repetitions
- 3 `current-10x` repetitions
- 3 `candidate-variant` no-op repetitions

Artifact root:

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/204-formatting-edit-after-activation-sanity-live-micro/`

The prompt was:

`In styles.css, reformat the .button rule so each declaration is on its own line. Do not change any CSS values.`

The canonical guard reported `unchanged_during_run: true` for `SKILL.md` and
`autoresearch/program.md`.

The offline report recorded no S005 floor failures:

- `current-10x`: S005 average 88.33, minimum 75, maximum 95.
- `candidate-variant`: S005 average 95, minimum 95, maximum 95.
- `no-10x-control`: S005 average 75, minimum 75, maximum 75.

Manual inspection of all three `current-10x` workspaces found:

- `changed_files`: `styles.css` only.
- No `.10x` records were created in the subject workspace.
- No dependency, app, config, generated, or metadata files were created.
- `styles.css` preserved the exact declarations and values:
  - `color: #111;`
  - `background: #fff;`
  - `padding: 4px 8px;`
- The final messages were concise completion notes, with no questions.

Spot checks of the no-op `candidate-variant` arm found equivalent behavior:
`styles.css` only, same formatted declarations, and no extra files.

## Procedure

Commands:

```sh
python3 autoresearch/validate.py
python3 autoresearch/run_codex_subject.py --experiment .10x/research/2026-06-25-formatting-edit-after-activation-sanity-live-micro.md --dry-run --out /tmp/10x-formatting-edit-plan.json
python3 autoresearch/run_once.py --experiment .10x/research/2026-06-25-formatting-edit-after-activation-sanity-live-micro.md --out .10x/evidence/.storage/2026-06-23-skill-autoresearch/204-formatting-edit-after-activation-sanity-live-micro --require-clean-canonical
```

Manual inspection read:

- `.10x/evidence/.storage/2026-06-23-skill-autoresearch/204-formatting-edit-after-activation-sanity-live-micro/report.md`
- `.10x/evidence/.storage/2026-06-23-skill-autoresearch/204-formatting-edit-after-activation-sanity-live-micro/canonical_guard.json`
- each `current-10x` workspace manifest
- each `current-10x` `styles.css`
- each `current-10x` last-message artifact
- two no-op `candidate-variant` workspace manifests and `styles.css` files

## What this supports or challenges

This supports the scaled-down activation invariant:

- ambiguous greenfield product creation should activate 10x and stay in the
  Outer Loop until execution-critical choices are settled;
- exact, mechanical, low-risk edits should remain nearly invisible and should
  not force record ceremony.

No `SKILL.md` mutation is supported by this run.

## Limits

This is a Codex CLI subject harness result only. It does not prove Claude Code,
OpenCode, or other harness behavior.

The offline scorer is Trust Level 1 and coarse for whitespace-only edits. Manual
inspection is the authoritative verdict.

The seed workspace was intentionally tiny and not a git repository. The result
tests file-scope minimalism through archived workspace manifests rather than git
diff output.
