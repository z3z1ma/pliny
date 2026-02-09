## Pack

Pack is Loom's pack system.

It installs prebuilt, OpenCode-first artifacts into a target repo in a way that is:

- deterministic (pack files are stored in Loom)
- safe (tracks drift via checksums and won't overwrite edits unless forced)
- language/toolchain agnostic (packs can be used in any repo)

### Concepts

- Pack: a versioned bundle of files that install into a repo (commonly `.opencode/agents` and `.opencode/commands`).
- Lock file: `.loom/pack/lock.json` records installed packs and per-file sha256.

### Commands

List packs:

```bash
loom pack list
```

Install a pack into the current repo:

```bash
loom pack install <pack-id>
```

Update an installed pack:

```bash
loom pack update <pack-id>
```

If files drifted, update with overwrite:

```bash
loom pack update <pack-id> --force
```

Check status / drift:

```bash
loom pack status
loom pack doctor
```

Uninstall:

```bash
loom pack uninstall <pack-id>
loom pack uninstall <pack-id> --force
```

### Included packs

- `loom-agile-core`: role agents + workflow skills (OpenCode-first, language-agnostic)
