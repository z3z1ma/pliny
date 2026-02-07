# Loom Compound Evidence

This folder contains **committed evidence capsules** (Episodes) used by Loom Compound.

Why this exists:
- Raw observations are runtime-only and typically gitignored.
- Episodes are the smallest durable unit that preserves *what happened* (bounded) and lets Loom compile durable memory deterministically.

Layout:
- `.loom/compound/episodes/YYYY/MM/<episode_id>.json`

Notes:
- Episodes are intended to be small. Large diffs may be stored as references (base/head sha + diffstat) instead of full patches.
- Do not edit Episodes casually; use `loom compound triage` for status/tagging.
