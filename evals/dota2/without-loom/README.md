# Ancient Meta Atlas

A dependency-free Warcraft 3 inspired web experience for exploring the Dota 2 meta through the public [OpenDota API](https://docs.opendota.com/).

## Run

```bash
npm run dev
```

Then open `http://localhost:4173`.

## Data

- `https://api.opendota.com/api/heroStats` powers the hero meta, images, roles, pick rates, and win rates.
- `https://api.opendota.com/api/proMatches` powers the recent match ledger.
- If either endpoint is unavailable, the site falls back to a small cached sample so the interface remains explorable.
