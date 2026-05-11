# Ancient War Room

A Warcraft 3 inspired OpenDota Campaign Map. It uses a Vite/React frontend to turn live hero meta, match feeds, and on-demand deep analytics into navigable RTS-style territories.

## Run

Install dependencies first:

```bash
npm install
```

Start the development server:

```bash
npm start
```

Then open `http://127.0.0.1:4173`.

## Check

```bash
npm run check
```

## Data Sources

- `https://api.opendota.com/api/heroStats`
- `https://api.opendota.com/api/proMatches`
- `https://api.opendota.com/api/publicMatches`
- `https://api.opendota.com/api/heroes/{hero_id}/matchups`
- `https://api.opendota.com/api/heroes/{hero_id}/durations`
- `https://api.opendota.com/api/heroes/{hero_id}/players`
- `https://api.opendota.com/api/heroes/{hero_id}/itemPopularity`
- `https://api.opendota.com/api/heroes/{hero_id}/matches`
- `https://api.opendota.com/api/matches/{match_id}`
- `https://api.opendota.com/api/constants/items`

The visual style is original RTS-inspired treatment. It does not include Warcraft 3 assets.

Raw OpenDota account IDs from specialist aggregates are intentionally not displayed in the UI.
