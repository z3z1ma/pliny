# Cursor Install

## Transport Surface

- protocol skills are distributed through Cursor's native plugin or skill package
  surface
- `.cursor-plugin/plugin.json` exposes canonical `skills/` using Cursor's native
  plugin manifest shape and overrides root hook discovery with an empty Cursor
  hook config so Claude-specific `hooks/hooks.json` is not loaded by Cursor
- `loom-bootstrap` is the required first skill; adapters may preload its
  references only through a Cursor-native rule surface when that remains a native
  package feature

## Expected Properties

- Cursor project rules are not treated as the product surface
- Loom bootstrap references remain part of the `loom-bootstrap` skill, even when
  a native adapter preloads them
- protocol skills remain the subsystem behavior source
- disable/uninstall follows Cursor's native plugin or skill package UX
- source installs use Cursor's native local plugin directory:
  `~/.cursor/plugins/local/agent-loom`

## Common Wrong Behavior

- assuming project `.cursor/rules/` is a global install surface
- placing optional utilities into the default protocol skill set
- making generated files more canonical than source skills
