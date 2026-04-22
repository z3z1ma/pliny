# Semantic Link Usage

Typed `links:` are navigation adjacency, not a dumping ground for every
semantic relationship.

Use the most specific section available before falling back to generic links.

## Where Relationships Belong

| Relationship | Use |
| --- | --- |
| hard execution prerequisite | `depends_on` |
| ticket implements or verifies spec acceptance | `# Coverage` |
| ticket acceptance view over claims | `# Claim Matrix` |
| packet iteration target claims | `# Verification Targets` |
| evidence supports a claim | `# Supports Claims` |
| evidence weakens or falsifies a claim | `# Challenges Claims` |
| critique challenges a claim | finding `Challenges:` |
| critique finding state on a ticket | `# Critique Disposition` |
| outside mirrors or requests | `external_refs` |
| source records for accepted explanation | wiki source sections and `links:` |
| ordinary navigation adjacency | `links:` |

## Generic Links

Use `links:` for durable adjacency a future agent should navigate:

```yaml
links:
  spec:
    - spec:shipping-workflow
  evidence:
    - evidence:shipping-workflow-smoke
```

Do not force relationship verbs into frontmatter unless the project has a
stable need. Plain typed adjacency plus specialized sections is enough for most
workspaces.

## Anti-Patterns

Do not:

- use `links:` instead of `depends_on` for hard execution prerequisites
- bury evidence support only in prose
- bury critique finding disposition only in prose
- copy outside issue tracker state into `links:`
- make `links:` a substitute for the acceptance dossier
