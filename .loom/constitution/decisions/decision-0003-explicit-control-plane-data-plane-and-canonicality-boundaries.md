---
id: decision:0003
kind: decision
status: active
created_at: 2026-04-01T18:06:00Z
updated_at: 2026-04-17T23:48:34Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  roadmap:
    - roadmap:bootstrap-the-markdown-first-protocol-corpus
---

# Decision

Loom in this repository keeps an explicit boundary between the control plane
and the data plane, and it keeps an explicit distinction between canonical and
merely durable artifacts.

Rules, skill activation guidance, templates, query recipes, scope and packet
doctrine, and parent workflow judgment form the visible control plane.
Canonical records and evidence live in the data plane alongside packets and
derived reports, but not all data-plane artifacts are canonical truth.

# Why This Decision Exists

The rewrite removes helper scripts precisely so workflow judgment stays visible
in Markdown and ordinary file operations rather than disappearing into a second
implementation layer.

That architectural separation is necessary to prevent authority inversion,
hidden behavior, and shadow ledgers.

# Alternatives Considered

- letting packets or other support artifacts silently outrank canonical records
  because they are newer or more detailed
- treating everything under `.loom/` as equally canonical
- hiding workflow judgment inside helper scripts or runtime behavior instead of
  preserving it in the visible control surfaces

# Consequences

- canonical records remain the top project-truth layer beneath the active rules
  and operator constraints
- `.loom/evidence/` stores proof artifacts without taking over policy, plan, or
  ticket truth
- `.loom/packets/` and other support artifacts may persist for replayability,
  but they do not silently mutate canonical truth
- recipes and optional automation may mechanize published doctrine, but they
  must not become a shadow control plane
- future wiki pages, specs, plans, and tickets should explain which artifact
  owns the next durable truth change instead of blending layers together

# Supersession

This supersedes any assumption that durable artifact persistence alone makes an
artifact canonical, or that helper behavior may quietly redefine authority
boundaries.
