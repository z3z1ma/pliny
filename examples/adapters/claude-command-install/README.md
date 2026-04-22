# Claude Command Install

## Transport Surface

- rules, skills, and optional commands are copied into the Claude-readable
  surfaces
- command files remain invocation wrappers
- protocol skills remain the behavior source

## Expected Properties

- rules are visible before task execution
- full skill content is loaded only when relevant
- command wrappers do not add semantics absent from skills
- uninstall preserves project `.loom/` truth records

## Common Wrong Behavior

- copying optional utilities into the default protocol skill set
- making Claude command files the only place a workflow is described
- treating generated install state as a source-of-truth layer
