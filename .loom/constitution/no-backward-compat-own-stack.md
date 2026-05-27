# No Backward Compatibility When We Own The Stack

ID: principle:no-backward-compat-own-stack
Type: Constitution Principle Fragment
Status: active
Created: 2026-05-26
Updated: 2026-05-26

## Principle

When we own the entire stack — backend, frontend, parser, engine, protocol,
persistence — backward compatibility with replaced formats, APIs, or data models
is tech debt, not a feature. Replace cleanly. Do not maintain dead code paths,
deprecated parsers, or compatibility shims for formats we are actively replacing.

## Why It Matters

Backward compatibility exists to protect consumers you do not control. When the
producer and all consumers are in the same repo under the same authority, there are
no external consumers to protect. Maintaining the old path alongside the new:

- doubles the test surface
- creates two code paths that can silently diverge
- makes future agents maintain code that will never run in production
- signals uncertainty about whether the replacement is actually complete
- creates a temptation to "fall back" instead of fixing the new path

## Where It Applies

- Loom Mill (we own backend + frontend + harness + persistence)
- Internal data formats (session JSON, WebSocket event shapes, API contracts)
- Parser formats (response protocols between engine and model)
- Component replacements (ShapingTimeline → ShapingCanvas)
- Database/persistence schema migrations within `.mill/` runtime state

## Where It Does Not Apply

- Published packages consumed by external users (Agent Loom core/playbooks)
- APIs exposed to third-party integrations we don't control
- File formats shared with external tools
- Situations where data migration is genuinely expensive and incremental rollout
  is the safer path (but then make the migration a ticket, not permanent compat)

## Promotion Or Retirement

Promote to a decision record if the team grows and backward compatibility becomes
a real engineering concern (multiple consumers, versioned APIs, breaking change
costs). Retire if external consumers appear that we must protect.
