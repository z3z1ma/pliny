# Scope Registry

Repository and worktree aliases help agents write in the right place.

They do not own product behavior, strategy, or execution state.

## File

Use `.loom/workspace.md` when a workspace has more than one plausible repository,
service, worktree, or scope alias.

This is a support record for operational scope resolution. It is not a new
canonical truth layer.

## Alias Shape

```yaml
repo_aliases:
  repo:root: .
  repo:web: ./apps/web
  repo:api: ./services/api
  repo:infra: ./infra
```

Use aliases in record scope:

```yaml
scope:
  kind: repository
  repositories:
    - repo:web
```

## Rules

- aliases must resolve to paths inside the intended workspace unless explicitly
  documented otherwise
- aliases do not define behavior, policy, or ownership of execution state
- if an alias is ambiguous, stop and resolve scope before editing
- multi-repo tickets should name every affected alias in `scope.repositories`

## Useful Checks

```bash
git rev-parse --show-toplevel
git -C apps/web rev-parse --show-toplevel
rg -n 'repo:[a-z0-9-]+' .loom --glob '*.md'
```
