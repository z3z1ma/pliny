---
id: consult-ticket-cli-help-before-subcommand-use
title: Consult ticket CLI help before subcommand use
trigger: When operating ticket commands with uncertain flags, aliases, or argument forms
confidence: 0.7600
status: active
domain: workflow
source: local
created_at: 2026-02-15T23:40:44.698691Z
updated_at: 2026-02-16T06:22:48.260602Z
tags: workflow, ticket, cli, discovery, safety
notes: This sequence is tightly clustered and immediately followed by ticket transitions, which supports it as a reliable preflight habit for CLI correctness.
---

## Action
Before mutating ticket state with unfamiliar ticket subcommands, query `loom ticket --help` and relevant subcommand help (`-h`/`--help`) to verify exact syntax and flags, then execute.

## Evidence
- ts=2026-02-15T23:37:14.536528Z source_id=obs-help-233714-root source_hash=loom-ticket-help
- ts=2026-02-15T23:37:16.999914Z source_id=obs-help-233716-add-note source_hash=loom-ticket-add-note-help
- ts=2026-02-15T23:37:17.678647Z source_id=obs-help-233717-update source_hash=loom-ticket-update-help
- ts=2026-02-15T23:37:19.719600Z source_id=obs-help-233719-status source_hash=loom-ticket-status-help
- ts=2026-02-15T23:55:37.540635Z source_id=obs-help-235537-update source_hash=loom-ticket-update-help-then-update
- ts=2026-02-16T05:31:12.699298Z source_id=obs-help-053112-update source_hash=loom-ticket-update-help
- ts=2026-02-16T05:31:14.957797Z source_id=obs-help-053114-create source_hash=loom-ticket-create-help

## Notes
This sequence is tightly clustered and immediately followed by ticket transitions, which supports it as a reliable preflight habit for CLI correctness.
