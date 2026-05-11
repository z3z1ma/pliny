# OpenDota API Shape For Meta Explorer

ID: research:20260510-opendota-api-shape
Type: Research
Status: completed
Created: 2026-05-10
Updated: 2026-05-10

## Summary

The MVP can be built as a static browser app against OpenDota public endpoints. `heroStats` supplies hero identity, roles, image paths, public bracket pick/win fields, pro picks/wins/bans, and trend arrays. `proMatches` and `publicMatches` supply recent match summary data that can power a readable battle chronicle without full match-detail calls.

## Question

Which OpenDota endpoints and data fields are strong enough to support a static, immersive meta explorer for heroes and recent games without adding a backend or API key?

## Scope

Covered:

- Official OpenDota docs entry point at `https://docs.opendota.com/`.
- Live public endpoint checks for `https://api.opendota.com/api/heroStats`.
- Live public endpoint checks for `https://api.opendota.com/api/proMatches`.
- Live public endpoint checks for `https://api.opendota.com/api/publicMatches`.
- Field-level inspection of the first `heroStats` object from the fetched response.

Excluded:

- Full match detail endpoint payloads.
- Authenticated OpenDota usage or API-key behavior.
- Long-term availability, rate limits, or API SLA guarantees.
- Dota patch-note or hero-lore source synthesis.

## Method And Sources

- Fetched `https://docs.opendota.com/` on 2026-05-10. The fetch returned only a minimal page title in this environment, so live endpoint responses carried the useful shape verification.
- Fetched `https://api.opendota.com/api/heroStats`; response was large and stored by the tool at `/Users/alexanderbutler/.local/share/opencode/tool-output/tool_e15375370001em2gKUsYbTqN2u`.
- Fetched `https://api.opendota.com/api/proMatches`; response showed recent pro match summary fields such as `match_id`, `duration`, `start_time`, team IDs/names, league information, scores, and `radiant_win`.
- Fetched `https://api.opendota.com/api/publicMatches`; response showed recent public match summary fields such as `match_id`, `radiant_win`, `start_time`, `duration`, `avg_rank_tier`, `game_mode`, and `radiant_team`/`dire_team` hero ID arrays.
- Used a fresh explore worker to inspect the saved `heroStats` response and summarize the first object.

## Findings

- `heroStats` objects include hero identity fields such as `id`, `name`, and `localized_name`.
- `heroStats` objects include hero classification fields such as `primary_attr`, `attack_type`, and `roles`.
- `heroStats` objects include relative image paths such as `img` and `icon`; these need a CDN base before use in the browser.
- `heroStats` objects include pro fields such as `pro_pick`, `pro_win`, and `pro_ban`.
- `heroStats` objects include public bracket fields using numeric prefixes, such as `1_pick`/`1_win` through `8_pick`/`8_win`.
- `heroStats` objects include aggregate and trend fields such as `pub_pick`, `pub_win`, `pub_pick_trend`, and `pub_win_trend`.
- `proMatches` can support recent professional match cards, but it does not include draft lineups in the summary payload observed here.
- `publicMatches` can support recent public match cards with hero lineups because it includes hero ID arrays for both teams.

## Tradeoffs

- Static direct API client:
  - Strength: fastest path, no backend, no secrets, simple deployment, matches the greenfield workspace.
  - Risk: depends on browser network access to OpenDota and exposes users to upstream rate limits or outage behavior.

- Backend/API proxy:
  - Strength: could cache data, normalize fields, and protect the browser from partial API quirks.
  - Risk: adds architecture and operational scope not requested for this workspace.

- Summary endpoints only:
  - Strength: enough for a novel meta and recent-games experience without high request volume.
  - Risk: cannot show full drafts, item builds, player performance, or timeline details.

## Rejected Paths And Null Results

- Rejected adding a backend cache for the MVP because the workspace is empty and the requested experience can be delivered with direct public endpoints.
- Rejected relying on the docs page content as the only source because the fetched docs output was too minimal in this environment.
- Rejected using Warcraft 3 assets because the spec requires inspired original styling, not copied copyrighted material.

## Conclusions

- A static browser MVP is justified for the first complete build.
- `/heroStats`, `/proMatches`, and `/publicMatches` are sufficient for the requested meta exploration and recent-games chronicle.
- The implementation should clearly communicate that computed meta scores are heuristics from public API fields, not official ratings or predictions.
- The implementation should handle partial endpoint failure because the product has no backend cache in this slice.

## Recommendations

- Use `spec:opendota-rts-meta-explorer` as the behavior contract for the MVP.
- Use a plan to track the broader build route because the product includes source research, behavior contract, implementation, verification, and audit.
- Use a bounded implementation ticket for the static MVP after the contract and research are in place.
- Consider a future research record if the product expands into full match details, player lookup, caching, or prediction models.

## Open Questions

- OpenDota rate-limit behavior was not characterized.
- Browser visual evidence was not captured at this research stage.

## Related Records

- `spec:opendota-rts-meta-explorer` - consumes the endpoint findings as the product behavior contract.
