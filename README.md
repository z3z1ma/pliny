# agent-loom

agent-loom is an agent-native development substrate with four layers: tickets, memory, workspace, and team orchestration.

## Install

```bash
uv pip install -e .
```

## CLI

```bash
loom ticket ...
loom memory ...
loom workspace ...
loom team ...
loom ui ticket
loom ui team
loom ui workspace
```

## Package layout

- `src/agent_loom/ticket`: Git-backed ticket system
- `src/agent_loom/memory`: Git-backed memory vault
- `src/agent_loom/workspace`: workspace + worktree tooling
- `src/agent_loom/team`: tmux-native orchestration
- `src/agent_loom/core`: shared utilities

## Development

```bash
uv run pytest
```
