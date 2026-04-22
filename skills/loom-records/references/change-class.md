# Change Class

`risk_class` says how dangerous a change is.
`change_class` says what kind of mutation it is.

Use change class to choose evidence, critique, and verification posture without
guessing from vibes.

## Values

- `record-hygiene` — links, statuses, filenames, frontmatter, or narrow record cleanup
- `documentation-explanation` — explanatory prose or wiki pages without behavior change
- `behavior-contract` — specs, acceptance criteria, or user-visible intended behavior
- `code-behavior` — source changes that affect runtime behavior
- `protocol-authority` — rules, ownership, acceptance, critique, packet, or truth-boundary changes
- `data-migration` — schema, storage, migration, or persistence changes
- `security-sensitive` — auth, secrets, permissions, injection, or trust-boundary changes
- `release-packaging` — PR, release, handoff, changelog, or external package work

## Default Routing

| Change class | Default evidence | Default critique |
| --- | --- | --- |
| `record-hygiene` | structural check | optional |
| `documentation-explanation` | source comparison | `operator-clarity` when meaningful |
| `behavior-contract` | spec diff and acceptance review | `operator-clarity` |
| `code-behavior` | test-first or observation-first proof | `code-change`, `test-coverage` |
| `protocol-authority` | structural checks and examples | `protocol-change`, `operator-clarity` |
| `data-migration` | before/after and rollback or idempotency proof | `data-migration` |
| `security-sensitive` | threat-focused evidence | `security` |
| `release-packaging` | package output compared to owner records | `operator-clarity` |

## Template Use

Tickets and packets may declare change class:

```yaml
change_class: code-behavior
```

When a ticket has several classes, name the primary class in frontmatter and
list secondary classes in the body.

## Discipline

Do not use change class as a substitute for risk judgment.

A `record-hygiene` change can still be high risk if it changes a protocol
owner boundary. A `code-behavior` change can be low risk if it is small,
well-tested, and isolated.
