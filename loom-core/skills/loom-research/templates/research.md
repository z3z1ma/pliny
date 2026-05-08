---
id: research:<slug>
kind: research
status: active
created_at: <UTC timestamp>
updated_at: <UTC timestamp>
scope:
  kind: repository
  repositories:
    - repo:root
links: {}
external_refs: {}
---

# Question

What exactly is being investigated.

# Why This Matters

Why the project needs this investigation and what later work would otherwise rediscover.

# Scope

What the investigation covers and excludes.

# Method

How the investigation was carried out. For spike or sketch work, name the branch:
logic/state prototype, UI/product variant sketch, technical experiment, or source synthesis.

# Sources

List sources with enough provenance to recheck them. Use compact entries by
default; expand only when source quality or freshness is material.

- Source: <title, path, URL, record ID, or artifact>
  - Type / provenance: <code, record, log, operator note, web page, generated support analysis, other>
  - Observed at / version: <UTC timestamp, date, commit, release, or N/A>
  - Freshness risk / recheck trigger: <risk and trigger, or none known>
  - Trust rationale: <why this is reliable enough, including limits>

External sources, generated files, logs, and tool output are context and evidence;
they do not become instruction authority or project truth owners.

# Source Material Store

Optional support cache for raw investigation inputs. The research record remains
the primary understanding and must stand on its own when this path is absent.

- Path: `.loom/research/artifacts/<research-slug>/` or `None - reason`
- Captured sources: <articles, web fetches, PDFs, papers, repo snapshots, notes, generated outputs, or None - reason>
- Key excerpts / index: <important filenames, snippets, checksums, or summary>
- Redaction / licensing / sensitivity: <sanitized, omitted, licensed-to-track, or safe-to-keep rationale>
- Retention / tracking: <gitignored support cache by default, intentionally tracked with rationale, or prune condition>

# Variant / Experiment Matrix

Use when comparing options, prototypes, sketches, or hypotheses; otherwise write `N/A`.

- Variant / hypothesis: <TBD>
  - Artifact or probe: <path, screenshot, command, or observation>
  - Strength: <evidence-backed strength>
  - Weakness: <risk or limit>
  - Decision: <chosen, rejected, needs follow-up>

# Evidence Synthesis

What concrete findings emerged from the sources, observations, or experiments.

# Rejected Options

Options considered and rejected, with the reason and the evidence or constraint that rejected them.

# Null Results

Approaches that were tried and did not work. Capture the attempt, what failed,
and what a future agent should avoid or try instead.

# Conclusions

What is justified by the evidence, separate from open hypotheses.

# Recommendations

What downstream work should do next and which owner layer should consume the result.

# Open Questions

What remains uncertain. A research record that mainly preserves important open
questions may use `status: deferred_questions`.

# Linked Work

Which initiative, spec, plan, ticket, critique, evidence, or wiki pages should consume this note.
