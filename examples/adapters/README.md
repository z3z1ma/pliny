# Adapter Fixtures

These fixtures describe expected adapter surfaces for common harnesses.

They are not runtime tests and not protocol truth. They exist to make installer
and adapter drift easier to review.

Adapter fixtures should check:

- rules are visible where the harness reads always-on instructions
- skills are discoverable without making every skill always-on
- command wrappers remain explicit invocation surfaces
- generated files are marked as Loom-managed when appropriate
- uninstall can remove generated surfaces without touching project `.loom/`
  records

Protocol semantics still live in `rules/`, `skills/`, templates, and owner
records.
