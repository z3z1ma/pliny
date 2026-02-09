---
name: pack-change-workflow
description: Procedure for changing Loom packs while keeping sample content and invariant tests aligned.
license: MIT
compatibility: opencode,claude
metadata:
  created_at: "2026-02-09T17:11:23.591265Z"
  source_episode_ids: "5dfc6781237a6acefa31edefa0ee4f60e94438077468b740966caa758a3c31bf"
  source_instinct_ids: "agile-pack-invariants-first,pack-change-sync-sample-and-tests,python-change-run-gates-even-for-doc-heavy-prs"
  tags: "contract,packs,testing,workflow"
  updated_at: "2026-02-09T17:11:23.591265Z"
  version: "1"
---
<!-- BEGIN:compound:skill-managed -->
# Pack Change Workflow

When you touch pack behavior, keep the repo's three references in lockstep: implementation, sample pack content, and tests.

## Use When
- You change anything under `src/agent_loom/pack/`.
- You change pack validation rules, lock behavior, or pack CLI UX.
- You update the loom-agile pack content under `src/agent_loom/pack/packs/`.

## Procedure
1. Identify the contract surface you changed.
   - Implementation: `src/agent_loom/pack/core.py`, `src/agent_loom/pack/lock.py`, `src/agent_loom/pack/packs.py`, `src/agent_loom/pack/cli.py`.
   - Public entrypoint (if relevant): `src/agent_loom/cli.py`.
2. Update the reference sample pack.
   - Keep `src/agent_loom/pack/packs/sample/pack.yaml` valid and representative of the current rules.
   - If the pack relies on files shipped with it, update `src/agent_loom/pack/packs/sample/files/` accordingly.
3. Re-align the tests to the intended contract.
   - Lifecycle/behavior: `tests/test_pack_lifecycle.py`.
   - Core invariants (especially loom-agile): `tests/test_pack_loom_agile_core_invariants.py`.
   - Prefer tightening tests to express the contract clearly; only relax if you intentionally broaden behavior.
4. Sweep docs that anchor user expectations.
   - If the pack UX changed, update `src/agent_loom/pack/README.md`.
5. Verify in this order.
   - `uv run ruff check .`
   - `uv run basedpyright`
   - `uv run pytest tests/test_pack_lifecycle.py tests/test_pack_loom_agile_core_invariants.py`

## Pitfalls
- Updating pack code without updating `src/agent_loom/pack/packs/sample/pack.yaml` creates silent drift: tests may pass while the sample misleads users.
- Weakening invariants tests to "unblock" a change usually hides a real contract decision; make the contract explicit instead.
<!-- END:compound:skill-managed -->

## Manual notes

_This section is preserved when the skill is updated. Put human notes, caveats, and exceptions here._
