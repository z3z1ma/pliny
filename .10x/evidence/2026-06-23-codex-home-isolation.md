Status: recorded
Created: 2026-06-23
Updated: 2026-06-23
Relates-To: .10x/tickets/done/2026-06-23-codex-home-isolation.md, .10x/evidence/2026-06-23-codex-live-isolation-smoke.md

# Codex Home Isolation Validation

## What Was Observed

Codex CLI 0.132.0 was investigated for no-10x control isolation.

Research record:

- `.10x/research/2026-06-23-codex-home-isolation.md`

Storage artifacts:

- `.10x/evidence/.storage/2026-06-23-codex-home-isolation/codex.stderr`
- `.10x/evidence/.storage/2026-06-23-codex-home-isolation/codex.stdout.jsonl`
- `.10x/evidence/.storage/2026-06-23-codex-home-isolation/disable-plugins.stderr`
- `.10x/evidence/.storage/2026-06-23-codex-home-isolation/disable-plugins.stdout.jsonl`
- `.10x/evidence/.storage/2026-06-23-codex-home-isolation/disable-plugins-last-message.txt`

Worker observations:

```text
codex --version -> codex-cli 0.132.0
codex --help -> exit 0
codex exec --help -> exit 0
codex plugin --help -> exit 0
codex features -> exit 2
codex features list -> exit 0
codex features list --all -> exit 2
codex doctor -> exit 1, auth configured but mixed auth signals noted
empty CODEX_HOME smoke -> exit 1
authenticated CODEX_HOME + --disable plugins smoke -> exit 0
```

The empty `CODEX_HOME` smoke failed authentication and still showed plugin
activity:

```text
codex.stderr plugin_loader_warnings True
codex.stderr unauthorized True
codex.stdout.jsonl ended with turn.failed after 401 Unauthorized errors
```

The authenticated home smoke used `--disable plugins` with
`--ignore-user-config` and succeeded:

```text
disable-plugins-last-message.txt DISABLE_PLUGINS_SMOKE_OK
disable-plugins.stderr plugin_loader_warnings False
disable-plugins.stderr unauthorized False
disable-plugins.stdout.jsonl events: thread.started, turn.started, item.completed, turn.completed
```

Runner metadata was updated for no-10x Codex plans:

```text
planned argv prefix: codex --disable plugins exec
planned argv includes: --ignore-user-config
planned env policy keys: CODEX_HOME, OPENAI_API_KEY
```

Parent verification output:

```text
$ python3 -m unittest autoresearch.tests.test_run_full_codex
....
----------------------------------------------------------------------
Ran 4 tests in 0.094s

OK

$ python3 -m py_compile autoresearch/run_full_codex.py autoresearch/tests/test_run_full_codex.py
no output

$ python3 autoresearch/validate.py
autoresearch contracts valid

$ python3 -m unittest discover -s autoresearch/tests
.....................
----------------------------------------------------------------------
Ran 21 tests in 0.256s

OK
```

Parent post-patch dry-run and fixture-smoke inspection:

```text
dry_no10x_argv_prefix ['codex', '--disable', 'plugins', 'exec']
dry_no10x_ignore_user_config True
dry_no10x_env_keys ['CODEX_HOME', 'OPENAI_API_KEY']
summary_samples_written 3
manifest_no10x_argv_prefix ['codex', '--disable', 'plugins', 'exec']
manifest_env_keys ['CODEX_HOME', 'OPENAI_API_KEY']
manifest_present_suppressed []
```

A source-only ASCII scan over `autoresearch/run_full_codex.py`,
`autoresearch/tests/test_run_full_codex.py`,
`.10x/tickets/done/2026-06-23-codex-home-isolation.md`, and
`.10x/research/2026-06-23-codex-home-isolation.md` produced no output.

## Procedure

1. Read the Codex home isolation ticket, live isolation evidence, FULL harness
   evidence, runner source, and runner tests.
2. Investigated Codex CLI behavior with help, feature, doctor, empty
   `CODEX_HOME`, and authenticated home smoke commands.
3. Recorded research findings in
   `.10x/research/2026-06-23-codex-home-isolation.md`.
4. Updated Codex FULL runner planning metadata so no-10x control plans include
   `--disable plugins`, `--ignore-user-config`, and non-secret env policy notes.
5. Ran focused Codex FULL tests.
6. Ran Python compilation, contract validation, and the full autoresearch test
   suite.
7. Ran a post-patch Codex FULL dry-run and fixture-smoke inspection to confirm
   planned argv/env metadata reaches plan and workspace manifest artifacts.
8. Checked source text for non-ASCII characters.

## What This Supports Or Challenges

This supports:

- `.10x/tickets/done/2026-06-23-codex-home-isolation.md#AC-001`
- `.10x/tickets/done/2026-06-23-codex-home-isolation.md#AC-002`
- `.10x/tickets/done/2026-06-23-codex-home-isolation.md#AC-003`
- `.10x/tickets/done/2026-06-23-codex-home-isolation.md#AC-004`
- `.10x/tickets/done/2026-06-23-codex-home-isolation.md#AC-005`

The observations support recommending authenticated operator `CODEX_HOME` plus
`--disable plugins` and `--ignore-user-config` for no-10x Codex control plans.
They also support avoiding a fresh temporary `CODEX_HOME` unless the operator
has provisioned authentication there through a supported Codex setup path.

## Limits

This evidence does not show that:

- `--disable plugins` removes every possible hidden Codex context source.
- A campaign-scale Codex benchmark is free of all contamination.
- A temporary `CODEX_HOME` can be safely authenticated without operator setup.
- Plugin cache files created during failed empty-home experimentation are useful
  source artifacts; they are raw storage artifacts under an ignored evidence
  storage directory.
- The no-10x control is promotion-grade without campaign review.

The recommended runner behavior records env policy descriptions only. It does
not record secret values and does not copy authentication files.
