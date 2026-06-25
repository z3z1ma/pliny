Status: done
Created: 2026-06-23
Updated: 2026-06-23
Parent: .10x/tickets/done/2026-06-23-implement-autoresearch-loop.md
Depends-On: .10x/tickets/done/2026-06-23-codex-live-isolation-smoke.md

# Isolate Codex Home Context For No-10x Controls

## Scope

Determine and implement the minimum safe mechanism for preventing CODEX_HOME
plugins, skills, and user configuration from contaminating no-10x control runs.

Included:

- Investigate Codex CLI behavior for `--ignore-user-config`, `CODEX_HOME`, and
  plugin/skill loading.
- Decide whether no-10x controls should run with a temporary CODEX_HOME, a
  profile override, explicit plugin/skill disable flags, or another supported
  mechanism.
- Preserve authentication requirements without copying secrets into durable
  artifacts.
- Add or update runner support only if the mechanism is clear and testable.
- Capture evidence showing whether plugin/skill loader warnings disappear.

Excluded:

- Canonical 10x instruction changes.
- Claude/OpenCode/oh-my-pi isolation design.
- Campaign-scale benchmark runs.

## Acceptance Criteria

- AC-001: Research or evidence records the observed Codex CLI behavior around
  `--ignore-user-config`, CODEX_HOME, plugins, and skills.
- AC-002: A no-10x Codex control isolation mechanism is recommended with explicit
  tradeoffs and secret-handling limits.
- AC-003: If implemented, the runner records the mechanism in planned argv/env
  metadata and tests cover it.
- AC-004: A smoke run or dry-run evidence shows whether CODEX_HOME plugin/skill
  loader warnings are absent under the recommended mechanism.
- AC-005: If the mechanism requires user/operator setup, that setup is documented
  as a blocker or prerequisite rather than silently assumed.

## Progress And Notes

- 2026-06-23: Ticket opened after
  `.10x/evidence/2026-06-23-codex-live-isolation-smoke.md` showed that
  `codex exec --ignore-user-config` still emitted CODEX_HOME plugin and skill
  loader warnings, and a tiny smoke prompt still reported 20,328 input tokens.
- 2026-06-23: Investigated Codex CLI 0.132.0. `codex exec --help` says
  `--ignore-user-config` skips `$CODEX_HOME/config.toml` while auth still uses
  `CODEX_HOME`. An empty temporary `CODEX_HOME` smoke failed auth and still
  produced plugin activity under the temporary home. A smoke using the
  authenticated home with `--disable plugins` plus `--ignore-user-config`
  exited 0 and did not emit observed plugin or skill loader warnings. Research
  captured in `.10x/research/2026-06-23-codex-home-isolation.md`; smoke
  artifacts are under
  `.10x/evidence/.storage/2026-06-23-codex-home-isolation/`. Implemented
  runner metadata for planned no-10x argv/env policy only; the runner still
  does not execute live Codex.
- 2026-06-23: Parent verification completed. Evidence recorded at
  `.10x/evidence/2026-06-23-codex-home-isolation.md`; AC-001 through AC-005 are
  satisfied. Calibration can proceed with the remaining limitation that this is
  not proof of all hidden context absence.

## Blockers

None.
