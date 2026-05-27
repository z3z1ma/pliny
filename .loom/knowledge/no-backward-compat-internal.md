# No Backward Compatibility for Internal Replacements

ID: knowledge:no-backward-compat-internal
Type: Knowledge Preference
Status: active
Created: 2026-05-26
Updated: 2026-05-26
Triggers: backward compatibility, backward compat, backwards compatible, legacy support, old format, deprecated, migration path, keep old code, maintain old
Applies To: loom-mill, internal APIs, parsers, data models, protocol changes

## Preference

When replacing an internal format, API, parser, protocol, or component that we
fully own (all producers and consumers in the same repo), do NOT maintain backward
compatibility. Rip out the old path completely. Replace clean.

Do not:
- Keep old parser functions "for backward compat"
- Add `if (oldFormat) { ... } else { ... }` branches
- Maintain deprecated fields in data models
- Write tests that verify the old format still parses
- Add migration layers for transient runtime state (`.mill/`)

Instead:
- Delete the old code
- Write the new code
- Update all consumers in the same commit or ticket
- If existing persisted data matters, make migration a bounded ticket (not permanent compat code)

## Use When

- Replacing a response protocol (e.g., ```action → XML nodes)
- Replacing a data model (e.g., blocks → graph nodes)
- Replacing a UI component (e.g., ShapingTimeline → ShapingCanvas)
- Changing API contracts between our own backend and frontend
- Changing WebSocket event formats
- Changing session persistence formats under `.mill/`

## Do Not Overapply

- Published npm packages with external consumers need semver and deprecation cycles
- If real data migration is needed (production databases, user files in `.loom/`),
  plan the migration as a ticket — but don't maintain permanent dual-path code

## Source Or Note

Operator directive 2026-05-26: "Backwards compatibility unequivocally equals tech
debt when we own the whole stack. DO NOT DO THIS."

## Related Records

- `principle:no-backward-compat-own-stack` — constitutional principle backing this
