# Doctor

Use these checks before trusting a Loom workspace deeply.

## Structural Checks

```bash
find .loom -maxdepth 2 -type d | sort
find .loom -type f -name '*.md' | sort | head -100
```

## Workspace Presence Checks

```bash
test -f .loom/constitution/constitution.md
test -d .loom/tickets
test -d .loom/packets/ralph
test -d .loom/wiki
```

These checks include canonical owner paths and support paths such as
`.loom/packets/ralph`; they are not a canonical-only path list.

If an empty canonical directory is absent in a Git checkout, treat that as a
bootstrap gap rather than automatic corruption. If records exist in a retired
or incorrect path, route to repair.

## Graph Discovery Checks

```bash
rg -n '^id:' .loom
rg -n '^status:' .loom/{initiatives,research,specs,plans,tickets,critique,wiki,evidence} 2>/dev/null
```

## Scope Checks

```bash
git rev-parse --show-toplevel
git -C path/to/target rev-parse --show-toplevel
```

## What "healthy enough" means

A workspace is healthy enough when:

- canonical owner paths exist where records exist, or bootstrap can create
  missing empty paths
- `constitution:main` exists or bootstrapping is clearly underway
- the owner chain for the current task is discoverable
- target repository ownership is explicit
- nothing important depends on hidden context
