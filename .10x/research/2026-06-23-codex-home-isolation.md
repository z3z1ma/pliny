Status: done
Created: 2026-06-23
Updated: 2026-06-23

# Codex CODEX_HOME Isolation

## Question

What is the minimum supported Codex CLI mechanism for no-10x control runs to
avoid CODEX_HOME plugin, skill, and user configuration contamination without
copying secrets into benchmark artifacts?

## Sources And Methods

- Read `.10x/tickets/done/2026-06-23-codex-home-isolation.md`.
- Read `.10x/evidence/2026-06-23-codex-live-isolation-smoke.md`.
- Read `.10x/evidence/2026-06-23-autoresearch-codex-full-harness.md`.
- Inspected `autoresearch/run_full_codex.py` and
  `autoresearch/tests/test_run_full_codex.py`.
- Ran `codex --version`: observed `codex-cli 0.132.0`.
- Ran `codex --help` and `codex exec --help`.
- Ran `codex features list`.
- Ran one live smoke with an empty `CODEX_HOME` under
  `.10x/evidence/.storage/2026-06-23-codex-home-isolation/codex-home/`.
- Ran one live smoke with the authenticated default `CODEX_HOME`,
  `--disable plugins`, and `--ignore-user-config`.

## Findings

`codex exec --help` documents `--ignore-user-config` narrowly: it does not load
`$CODEX_HOME/config.toml`, while auth still uses `CODEX_HOME`. This means
replacing `CODEX_HOME` with a fresh temporary directory is also an auth change,
not only an isolation change.

`codex features list` showed `plugins` as a stable enabled feature in the
observed environment. It also showed related plugin feature flags, including
`plugin_hooks` and `plugin_sharing`.

The empty-CODEX_HOME smoke used:

```text
env CODEX_HOME=.10x/evidence/.storage/2026-06-23-codex-home-isolation/codex-home codex --ask-for-approval never exec --cd .10x/evidence/.storage/2026-06-23-codex-home-isolation/workspace --skip-git-repo-check --ephemeral --json --output-last-message .10x/evidence/.storage/2026-06-23-codex-home-isolation/last-message.txt --ignore-user-config --sandbox read-only <prompt>
```

It exited 1. `codex.stdout.jsonl` ended with `turn.failed` after repeated
401 Unauthorized errors. `codex.stderr` showed missing authentication and also
showed plugin activity from the temporary home, including remote plugin sync and
a plugin manifest warning under the temporary `codex-home/.tmp/plugins/`
directory. Empty `CODEX_HOME` therefore failed both goals: it did not preserve
auth and did not by itself eliminate plugin loader activity.

The authenticated-CODEX_HOME smoke used:

```text
codex --ask-for-approval never --disable plugins exec --cd .10x/evidence/.storage/2026-06-23-codex-home-isolation/workspace --skip-git-repo-check --ephemeral --json --output-last-message .10x/evidence/.storage/2026-06-23-codex-home-isolation/disable-plugins-last-message.txt --ignore-user-config --sandbox read-only <prompt>
```

It exited 0. `disable-plugins-last-message.txt` contained exactly
`DISABLE_PLUGINS_SMOKE_OK`. `disable-plugins.stdout.jsonl` contained
`thread.started`, `turn.started`, `item.completed`, and `turn.completed`; usage
reported 19,306 input tokens. `disable-plugins.stderr` contained rollout state
warnings, but no observed `codex_core_plugins`, skill loader, plugin manifest,
or CODEX_HOME plugin/skill loader warnings.

## Conclusions

The recommended no-10x Codex control mechanism is:

- Run from a generated workspace that omits project instruction files and skill
  directories.
- Invoke Codex with `--disable plugins` and `--ignore-user-config`.
- Do not override `CODEX_HOME` by default; inherit the operator's authenticated
  Codex home so auth remains supported without copying `auth.json` or tokens.
- Record only env policy metadata, never secret values.

Tradeoffs:

- This is not a sterile CODEX_HOME. It intentionally preserves auth state from
  the operator-provisioned home.
- It addresses the observed CODEX_HOME plugin and skill loader warning class,
  but it does not prove every hidden token or base instruction source is absent.
- If an operator requires a temporary CODEX_HOME, auth must be provisioned in
  that home by a supported Codex login or environment-auth setup before the run.
  The runner must not copy secrets into that home or record them in artifacts.

The runner should therefore record planned argv/env policy metadata only. Live
Codex execution remains outside `autoresearch/run_full_codex.py` for this slice.
