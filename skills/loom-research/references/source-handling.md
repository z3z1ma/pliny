# Source Handling

Research can draw from:

- repository records
- code
- tests
- logs
- operator notes
- web sources when current information matters

## Source posture

When source quality varies, say so.

When evidence is incomplete, say so.

When a recommendation depends on assumptions, state them.

## External and current source metadata

When research relies on external sources or current facts, include enough source
metadata for a future agent to understand the citation without rerunning the
whole investigation:

- source title or description
- provenance, such as publisher, author, repository, organization, quoted
  operator, or system that produced it
- URL or local path when available
- access date for time-sensitive or web sources
- short note on source quality when reliability, authority, or completeness
  materially affects the conclusion

State freshness limits when a conclusion may expire. Name the recheck or
invalidation trigger when it matters, such as a vendor release, policy change,
API deprecation, repository ref change, or new contradictory evidence.

Research should synthesize and cite sources; it does not need full raw source
dumps. Observed artifacts and command outputs belong in evidence when they need
to persist as observations. Accepted explanatory synthesis belongs in the wiki
after it is settled. Live execution state and ticket acceptance remain owned by
tickets.

## Promotion rule

If the research result becomes accepted understanding that future agents should read first, promote the synthesis into the wiki and link back to the research note.
