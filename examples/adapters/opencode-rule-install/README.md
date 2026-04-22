# OpenCode Rule Install

## Transport Surface

- rules are copied into a Loom-owned rule directory
- skills and commands are copied into the configured OpenCode surface
- OpenCode configuration references the Loom rule directory through its
  instruction loading mechanism

## Expected Properties

- symlinks are not required for a clean install
- rules remain Markdown instructions, not shell execution policy
- command wrappers are optional invocation adapters
- uninstall removes Loom-managed references without deleting project truth

## Common Wrong Behavior

- leaving stale symlinks to a development checkout
- treating OpenCode config as Loom ontology
- placing dogfood `.loom/` records into the adapter install surface
