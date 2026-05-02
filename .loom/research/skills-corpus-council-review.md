---
id: research:skills-corpus-council-review
kind: research
status: concluded
created_at: 2026-05-02T07:58:42Z
updated_at: 2026-05-02T07:58:42Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  roadmap:
    - roadmap:bootstrap-the-markdown-first-protocol-corpus
  initiative:
    - initiative:skills-corpus-protocol-sharpening
  evidence:
    - evidence:skills-corpus-council-review
  plan:
    - plan:skills-corpus-protocol-sharpening
  ticket:
    - ticket:3uv5l5fh
external_refs: {}
---

# Question

What should be improved in the shipped `skills/` corpus so Loom's operational
doctrine becomes more precise, internally consistent, recoverable by a fresh
agent, and resistant to shadow truth?

# Why This Matters

This repository's product surface is the skill corpus. If the skill corpus is
nearly correct but internally drifting, future agents may still complete tasks by
intuition, but Loom's central promise weakens: the repo should teach what matters
without transcript archaeology, hidden runtime assumptions, or one agent's private
memory.

The council review matters because it looked across the corpus as a protocol
surface rather than as isolated docs. The findings should therefore survive as
research, not merely as a chat summary or ticket checklist.

# Scope

This research covers council-observed improvement areas in:

- `README.md` and public framing that explains Loom's premise.
- `skills/loom-bootstrap/**` doctrine and routing.
- every `skills/loom-*/SKILL.md` surface.
- skill references and templates where record grammar, packet grammar, evidence,
  critique, wiki, memory, or routing behavior is taught.
- cross-surface consistency between public docs, skills, templates, and dogfooded
  Loom records.

This research does not decide the final wording of any protocol edit. It names
the observed gaps, the reasoning behind them, and the downstream route.

# Method

The user requested a council review of `skills/` with README context. A council
subagent was launched with instructions to read enough of the corpus to provide a
strategic, adversarial, actionable report covering bootstrap doctrine, every
skill, references/templates, cross-surface consistency, operator ergonomics,
failure modes, and writing quality.

The resulting council report was treated as an observed review artifact. This
research synthesizes its findings into stable claims, recommendations, rejected
approaches, and open questions for downstream plan and ticket work.

# Sources

- `README.md` read during the parent session for Loom premise and public framing.
- `AGENTS.md` repository guidance read from the active workspace context.
- `skills/` directory listing with 22 Loom skill directories.
- Council task result `ses_21866e25cffePOACghVwgMjBTa`, recorded in
  `evidence:skills-corpus-council-review`.
- Existing constitutional context: `constitution:main` and
  `roadmap:bootstrap-the-markdown-first-protocol-corpus`.

# Evidence

- CLAIM-001: The corpus is already conceptually strong and should be sharpened,
  not reinvented. The council explicitly warned against adding a runtime, daemon,
  database, CLI, or new ontology as core protocol.
- CLAIM-002: The most urgent cross-surface drift is `loom-drive` integration,
  especially its absence from README skill-map surfaces despite being an existing
  shipped skill.
- CLAIM-003: README's linear outer-loop diagram can mislead operators by making
  research, spec, plan, ticket, evidence, critique, wiki, and memory look like a
  single sequence rather than a backbone plus conditional routes.
- CLAIM-004: Cold-start and post-compaction resume deserve first-class workspace
  guidance because they are central to Loom's premise but currently appear mostly
  as an implication of other workflows.
- CLAIM-005: Shared grammar has outgrown the current record references in several
  places: `OBJ-*` objective coverage, valid `kind:` values, packet ID families,
  critique/wiki packet conventions, semantic link forms, and memory exceptions.
- CLAIM-006: Ticket and packet risk/change classification needs a clearer rule:
  tickets should carry explicit risk/change classification when it affects
  evidence or critique, while packets may narrow the ticket risk for one bounded
  iteration.
- CLAIM-007: Operator ergonomics can be improved by explicitly teaching scratchpad
  avoidance, pre-compaction checkpoints, external-reference lifecycle, concurrent
  edit safety, rejected Ralph iteration handling, memory pruning, and critique
  finding follow-up conversion.
- CLAIM-008: Some doctrine is duplicated across owner surfaces, especially atlas
  pages, retrospective mechanics, spike/sketch variants, and packetized non-Ralph
  work.
- CLAIM-009: The next work should be high-risk protocol-authority work with
  structural validation and mandatory critique before acceptance.

# Rejected Options

- Rejected option: introduce a required CLI, daemon, database, or hidden runtime to
  enforce consistency. Reason: this conflicts with `constitution:main`, the
  active roadmap, and the council consensus that Markdown skills are the product.
- Rejected option: treat the council output as enough and begin editing from chat.
  Reason: Loom's premise requires durable owner records before non-trivial
  protocol-authority work begins.
- Rejected option: make README the canonical authority and force skills to match
  it by recency. Reason: `skills/`, especially bootstrap doctrine, is the product
  surface and must stay aligned with README without losing owner-layer authority.
- Rejected option: solve all findings through one broad copyediting pass. Reason:
  several findings affect protocol behavior, record grammar, or acceptance gates
  and need evidence plus critique, not only prose polish.
- Rejected option: create a new canonical layer for resume, external references,
  drive handoffs, retrospective, or scratch notes. Reason: the council findings
  can be routed through existing owners.

# Null Results

No implementation experiments were run. This research records a review synthesis,
not a changed-source validation result.

# Conclusions

The council findings are coherent with the active roadmap: Loom is in a protocol
sharpening phase, not a platform-expansion phase.

The highest-value work is to make routing and grammar more explicit exactly where
the corpus already uses the concepts. The improvements should reduce the need for
agent inference without adding a second ontology or turning Loom into a command
system.

The findings are broad enough to justify an initiative and plan, but the first
execution pass can be owned by one high-risk ticket if it keeps a staged
implementation order and splits follow-up tickets when scope becomes too wide.

# Recommendations

- Create a strategic initiative for skills corpus protocol sharpening.
- Create a plan that sequences low-risk alignment, shared grammar hardening,
  operator ergonomics, duplicated-doctrine consolidation, and validation/critique.
- Create one detailed ready ticket for the first comprehensive pass, with
  mandatory critique and structural evidence gates.
- Treat `loom-drive` visibility and README diagram correction as low-risk early
  alignment work.
- Treat `OBJ-*` grammar, packet contract changes, ticket risk rules, cold-start
  doctrine, and bootstrap routing changes as high-risk or medium-risk protocol
  changes requiring critique before acceptance.
- Preserve any stable findings from critique as follow-up tickets or accepted
  risks instead of burying them in prose.

# Open Questions

- Should `OBJ-*` coverage use `initiative:skills-corpus-protocol-sharpening#OBJ-001`
  syntax, the existing prose style `initiative:skills-corpus-protocol-sharpening`
  `OBJ-001`, or both during a transition?
- Should `loom-drive/templates/outer-loop-handoff.md` become a frontmatter-bearing
  support artifact, a packet family, or remain a transient handoff template?
- Which `kind:` values should be treated as closed vocabulary versus examples of
  current corpus usage?
- Should ticket `change_class` and `risk_class` become mandatory for every new
  ticket, or only for tickets where evidence/critique posture depends on them?
- Should cold-start resume be taught only in `loom-workspace`, or also summarized
  in bootstrap doctrine and README?
- Which duplicated sections should be deleted versus replaced with short pointers
  to owner surfaces?

# Linked Work

- `initiative:skills-corpus-protocol-sharpening`
- `plan:skills-corpus-protocol-sharpening`
- `ticket:3uv5l5fh`
- `evidence:skills-corpus-council-review`
- `roadmap:bootstrap-the-markdown-first-protocol-corpus`
