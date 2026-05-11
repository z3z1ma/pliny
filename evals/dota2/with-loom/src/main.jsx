import React, { useEffect, useState } from "react";
import { createRoot } from "react-dom/client";
import { fetchArray, fetchObject, OPEN_DOTA_MATCH } from "./api";
import {
  BRACKETS,
  ROLE_ORDER,
  attrLabel,
  buildHeroMap,
  buildItemMap,
  filterHeroes,
  formatCompact,
  formatDate,
  formatDuration,
  formatNumber,
  formatPercent,
  getBattleReport,
  getDurationCurve,
  getItemPhases,
  getMatchupLanes,
  getSpecialists,
  heroImage,
  normalizeHero,
  rankHeroes,
  rankLabel,
  safeNumber,
} from "./analytics";
import "./styles.css";

const TERRITORIES = [
  { id: "war-table", label: "War Table", subtitle: "Meta campaign", x: 46, y: 48 },
  { id: "counterlands", label: "Counterlands", subtitle: "Matchups", x: 22, y: 34 },
  { id: "time-rift", label: "Time Rift", subtitle: "Duration curve", x: 68, y: 29 },
  { id: "item-forge", label: "Item Forge", subtitle: "Build paths", x: 73, y: 67 },
  { id: "adept-tower", label: "Adept Tower", subtitle: "Specialists", x: 30, y: 72 },
  { id: "chronicle", label: "Chronicle", subtitle: "Recent battles", x: 50, y: 82 },
  { id: "battle-report", label: "Battle Report", subtitle: "Selected match", x: 50, y: 18 },
];

const initialFilters = { query: "", role: "All", bracket: "pub", sort: "meta" };
const emptyHeroIntel = { heroId: null, loading: false, errors: [], matchups: [], durations: [], players: [], itemPopularity: null, matches: [] };
const emptyMatchIntel = { matchId: null, loading: false, error: "", report: null };

function App() {
  const [summary, setSummary] = useState({ loading: true, errors: [], heroes: [], proMatches: [], publicMatches: [], lastUpdated: "" });
  const [filters, setFilters] = useState(initialFilters);
  const [selectedHeroId, setSelectedHeroId] = useState(null);
  const [selectedMatchId, setSelectedMatchId] = useState(null);
  const [activeTerritory, setActiveTerritory] = useState("war-table");
  const [heroIntel, setHeroIntel] = useState(emptyHeroIntel);
  const [matchIntel, setMatchIntel] = useState(emptyMatchIntel);
  const [itemMap, setItemMap] = useState(new Map());
  const [itemError, setItemError] = useState("");

  const heroMap = buildHeroMap(summary.heroes);
  const rankedHeroes = rankHeroes(summary.heroes, filters.bracket, filters.sort);
  const visibleHeroes = filterHeroes(rankedHeroes, filters);
  const selectedHero = rankedHeroes.find((hero) => hero.id === selectedHeroId) || rankedHeroes[0] || null;
  const topHero = rankedHeroes[0] || null;
  const matchupLanes = getMatchupLanes(heroIntel.matchups, heroMap);
  const durationCurve = getDurationCurve(heroIntel.durations);
  const itemPhases = getItemPhases(heroIntel.itemPopularity, itemMap);
  const specialists = getSpecialists(heroIntel.players);
  const battleReport = matchIntel.report;

  useEffect(() => {
    const controller = new AbortController();
    loadSummary(controller.signal);
    return () => controller.abort();
  }, []);

  useEffect(() => {
    if (!summary.heroes.length || selectedHeroId) return;
    setSelectedHeroId(summary.heroes[0].id);
  }, [summary.heroes, selectedHeroId]);

  useEffect(() => {
    if (!visibleHeroes.length) return;
    if (!visibleHeroes.some((hero) => hero.id === selectedHeroId)) {
      setSelectedHeroId(visibleHeroes[0].id);
    }
  }, [visibleHeroes, selectedHeroId]);

  useEffect(() => {
    if (!selectedHero?.id) return;
    const controller = new AbortController();
    loadHeroIntel(selectedHero.id, controller.signal);
    return () => controller.abort();
  }, [selectedHero?.id]);

  useEffect(() => {
    if (activeTerritory !== "item-forge" || itemMap.size || itemError) return;
    const controller = new AbortController();
    fetchObject("/constants/items", { signal: controller.signal })
      .then((items) => setItemMap(buildItemMap(items)))
      .catch((error) => {
        if (error.name !== "AbortError") setItemError(error.message || "Item constants failed");
      });
    return () => controller.abort();
  }, [activeTerritory, itemMap.size, itemError]);

  useEffect(() => {
    if (!selectedMatchId) return;
    const controller = new AbortController();
    const currentHeroMap = buildHeroMap(summary.heroes);
    setMatchIntel({ matchId: selectedMatchId, loading: true, error: "", report: null });
    fetchObject(`/matches/${selectedMatchId}`, { signal: controller.signal })
      .then((detail) => setMatchIntel({ matchId: selectedMatchId, loading: false, error: "", report: getBattleReport(detail, currentHeroMap) }))
      .catch((error) => {
        if (error.name !== "AbortError") {
          setMatchIntel({ matchId: selectedMatchId, loading: false, error: error.message || "Match detail failed", report: null });
        }
      });
    return () => controller.abort();
  }, [selectedMatchId, summary.heroes]);

  async function loadSummary(signal) {
    setSummary((current) => ({ ...current, loading: true, errors: [] }));
    const [heroesResult, proResult, publicResult] = await Promise.allSettled([
      fetchArray("/heroStats", { signal }),
      fetchArray("/proMatches", { signal }),
      fetchArray("/publicMatches", { signal }),
    ]);
    if (signal.aborted) return;

    const heroes = settledData(heroesResult, "Hero stats").map(normalizeHero).filter(Boolean);
    const proMatches = settledData(proResult, "Pro matches").slice(0, 18);
    const publicMatches = settledData(publicResult, "Public matches").slice(0, 18);
    const errors = [settledError(heroesResult, "Hero stats"), settledError(proResult, "Pro matches"), settledError(publicResult, "Public matches")].filter(Boolean);
    setSummary({ loading: false, errors, heroes, proMatches, publicMatches, lastUpdated: new Date().toLocaleTimeString() });
  }

  async function loadHeroIntel(heroId, signal) {
    setHeroIntel({ ...emptyHeroIntel, heroId, loading: true });
    const [matchups, durations, players, itemPopularity, matches] = await Promise.allSettled([
      fetchArray(`/heroes/${heroId}/matchups`, { signal }),
      fetchArray(`/heroes/${heroId}/durations`, { signal }),
      fetchArray(`/heroes/${heroId}/players`, { signal }),
      fetchObject(`/heroes/${heroId}/itemPopularity`, { signal }),
      fetchArray(`/heroes/${heroId}/matches`, { signal }),
    ]);
    if (signal.aborted) return;

    setHeroIntel({
      heroId,
      loading: false,
      errors: [
        settledError(matchups, "Matchups"),
        settledError(durations, "Duration curve"),
        settledError(players, "Specialists"),
        settledError(itemPopularity, "Item paths"),
        settledError(matches, "Hero matches"),
      ].filter(Boolean),
      matchups: settledData(matchups, "Matchups"),
      durations: settledData(durations, "Duration curve"),
      players: settledData(players, "Specialists"),
      itemPopularity: itemPopularity.status === "fulfilled" ? itemPopularity.value : null,
      matches: settledData(matches, "Hero matches").slice(0, 12),
    });
  }

  function selectMatch(matchId) {
    if (!matchId) return;
    setSelectedMatchId(Number(matchId));
    setActiveTerritory("battle-report");
  }

  return (
    <div className="campaign-shell">
      <div className="ambient ambient-one" aria-hidden="true" />
      <div className="ambient ambient-two" aria-hidden="true" />
      <Header summary={summary} onRefresh={() => loadSummary(new AbortController().signal)} />

      <main className="campaign-main">
        <section className="map-stage" aria-labelledby="map-title">
          <div className="map-heading">
            <p className="eyebrow">Campaign Map</p>
            <h1 id="map-title">Chart the current war for the Ancients.</h1>
            <p>
              Scout the meta as territories: counterlands, timing rifts, item forges, specialist towers, and live battle reports from OpenDota.
            </p>
          </div>

          <CampaignMap activeTerritory={activeTerritory} setActiveTerritory={setActiveTerritory} selectedHero={selectedHero} />
          <StatusRibbon summary={summary} topHero={topHero} heroIntel={heroIntel} selectedHero={selectedHero} />
        </section>

        <aside className="side-command" aria-label="Campaign controls">
          <HeroPanel hero={selectedHero} filters={filters} setFilters={setFilters} visibleCount={visibleHeroes.length} totalCount={summary.heroes.length} />
          <HeroRoster heroes={visibleHeroes.slice(0, 24)} selectedHeroId={selectedHeroId} setSelectedHeroId={setSelectedHeroId} />
        </aside>

        <section className="territory-panel" aria-live="polite">
          <TerritoryContent
            activeTerritory={activeTerritory}
            selectedHero={selectedHero}
            rankedHeroes={rankedHeroes}
            summary={summary}
            heroIntel={heroIntel}
            matchupLanes={matchupLanes}
            durationCurve={durationCurve}
            itemPhases={itemPhases}
            itemMap={itemMap}
            itemError={itemError}
            specialists={specialists}
            battleReport={battleReport}
            matchIntel={matchIntel}
            selectMatch={selectMatch}
          />
        </section>
      </main>

      <footer className="site-footer">
        Public OpenDota data, transformed into an original RTS-inspired campaign interface. No Warcraft 3 assets are used.
      </footer>
    </div>
  );
}

function Header({ summary, onRefresh }) {
  return (
    <header className="top-bar">
      <a className="brand" href="#map-title" aria-label="Ancient War Room home">
        <span className="brand-sigil">AW</span>
        <span>
          <strong>Ancient War Room</strong>
          <small>OpenDota campaign intelligence</small>
        </span>
      </a>
      <div className="top-meta" aria-live="polite">
        <span>{summary.loading ? "Opening scrying portals" : `${summary.heroes.length} heroes scouted`}</span>
        <span>{summary.lastUpdated ? `Last ritual ${summary.lastUpdated}` : "Awaiting first reading"}</span>
      </div>
      <button className="gold-button" type="button" onClick={onRefresh} disabled={summary.loading}>
        {summary.loading ? "Scrying..." : "Refresh Map"}
      </button>
    </header>
  );
}

function CampaignMap({ activeTerritory, setActiveTerritory, selectedHero }) {
  return (
    <div className="campaign-map" aria-label="OpenDota campaign territories">
      <div className="map-rings" aria-hidden="true" />
      <div className="map-route route-a" aria-hidden="true" />
      <div className="map-route route-b" aria-hidden="true" />
      {TERRITORIES.map((territory) => (
        <button
          key={territory.id}
          className="territory-node"
          type="button"
          style={{ "--x": `${territory.x}%`, "--y": `${territory.y}%` }}
          aria-pressed={activeTerritory === territory.id}
          onClick={() => setActiveTerritory(territory.id)}
        >
          <span className="node-flare" aria-hidden="true" />
          <strong>{territory.label}</strong>
          <small>{territory.subtitle}</small>
        </button>
      ))}
      <div className="map-hero-card">
        <span className="eyebrow">Chosen champion</span>
        <strong>{selectedHero?.localized_name || "No hero selected"}</strong>
        <small>{selectedHero ? `${attrLabel(selectedHero.primary_attr)} · ${selectedHero.roles.slice(0, 2).join(" / ")}` : "Load heroStats to scout"}</small>
      </div>
    </div>
  );
}

function StatusRibbon({ summary, topHero, heroIntel, selectedHero }) {
  return (
    <div className="status-ribbon">
      <StatTile label="Top omen" value={topHero?.localized_name || "Unknown"} detail={topHero ? `${formatPercent(topHero.meta.winRate)} · ${formatCompact(topHero.meta.picks)} picks` : "No heroStats"} />
      <StatTile label="Portals" value={`${[summary.heroes.length, summary.proMatches.length, summary.publicMatches.length].filter(Boolean).length}/3`} detail={summary.errors.length ? `${summary.errors.length} warnings` : "summary endpoints"} />
      <StatTile label="Deep scout" value={heroIntel.loading ? "moving" : selectedHero?.localized_name || "idle"} detail={heroIntel.errors.length ? `${heroIntel.errors.length} territory warnings` : "lazy hero analytics"} />
      <StatTile label="Recent battles" value={formatNumber(summary.proMatches.length + summary.publicMatches.length)} detail="pro and public feeds" />
    </div>
  );
}

function StatTile({ label, value, detail }) {
  return (
    <div className="stat-tile">
      <span>{label}</span>
      <strong>{value}</strong>
      <small>{detail}</small>
    </div>
  );
}

function HeroPanel({ hero, filters, setFilters, visibleCount, totalCount }) {
  return (
    <section className="panel hero-panel">
      <div className="portrait-frame">
        {hero && heroImage(hero) ? <img src={heroImage(hero)} alt="" /> : null}
        <div>
          <p className="eyebrow">Hero scout</p>
          <h2>{hero?.localized_name || "Awaiting roster"}</h2>
          <p>{hero ? `${attrLabel(hero.primary_attr)} · ${hero.attack_type} · ${hero.roles.join(" / ")}` : "OpenDota heroStats is required."}</p>
        </div>
      </div>

      <div className="control-grid">
        <label>
          <span>Search tavern</span>
          <input value={filters.query} onChange={(event) => setFilters({ ...filters, query: event.target.value })} placeholder="Invoker, Axe, Crystal..." />
        </label>
        <label>
          <span>Bracket lens</span>
          <select value={filters.bracket} onChange={(event) => setFilters({ ...filters, bracket: event.target.value })}>
            {Object.entries(BRACKETS).map(([value, label]) => <option key={value} value={value}>{label}</option>)}
          </select>
        </label>
        <label>
          <span>Sort ritual</span>
          <select value={filters.sort} onChange={(event) => setFilters({ ...filters, sort: event.target.value })}>
            <option value="meta">Meta score</option>
            <option value="winRate">Win rate</option>
            <option value="picks">Pick volume</option>
            <option value="proHeat">Pro heat</option>
          </select>
        </label>
      </div>

      <div className="role-chips" aria-label="Role filters">
        {ROLE_ORDER.map((role) => (
          <button key={role} type="button" aria-pressed={filters.role === role} onClick={() => setFilters({ ...filters, role })}>{role}</button>
        ))}
      </div>

      <p className="panel-note">Showing {visibleCount} of {totalCount} heroes. Deep scouting follows the selected hero.</p>
    </section>
  );
}

function HeroRoster({ heroes, selectedHeroId, setSelectedHeroId }) {
  if (!heroes.length) return <section className="panel empty-card">No heroes match the current scouting order.</section>;
  return (
    <section className="panel roster-panel" aria-label="Hero roster">
      {heroes.map((hero) => (
        <button key={hero.id} type="button" className="roster-card" aria-pressed={selectedHeroId === hero.id} onClick={() => setSelectedHeroId(hero.id)}>
          {heroImage(hero, "icon") ? <img src={heroImage(hero, "icon")} alt="" /> : <span className="icon-fallback" />}
          <span>
            <strong>{hero.localized_name}</strong>
            <small>{formatPercent(hero.meta.winRate)} · {formatCompact(hero.meta.picks)} picks</small>
          </span>
        </button>
      ))}
    </section>
  );
}

function TerritoryContent(props) {
  const territory = TERRITORIES.find((item) => item.id === props.activeTerritory);
  return (
    <article className="panel territory-content">
      <div className="territory-heading">
        <div>
          <p className="eyebrow">{territory?.subtitle || "Territory"}</p>
          <h2>{territory?.label || "War Table"}</h2>
        </div>
        <span className="territory-badge">OpenDota live</span>
      </div>
      {props.summary.errors.length ? <WarningList warnings={props.summary.errors} /> : null}
      {props.heroIntel.errors.length ? <WarningList warnings={props.heroIntel.errors} label="Deep scout warnings" /> : null}
      {renderTerritory(props)}
    </article>
  );
}

function renderTerritory(props) {
  switch (props.activeTerritory) {
    case "counterlands":
      return <Counterlands selectedHero={props.selectedHero} heroIntel={props.heroIntel} matchupLanes={props.matchupLanes} />;
    case "time-rift":
      return <TimeRift selectedHero={props.selectedHero} heroIntel={props.heroIntel} durationCurve={props.durationCurve} />;
    case "item-forge":
      return <ItemForge selectedHero={props.selectedHero} heroIntel={props.heroIntel} itemPhases={props.itemPhases} itemMap={props.itemMap} itemError={props.itemError} />;
    case "adept-tower":
      return <AdeptTower specialists={props.specialists} heroIntel={props.heroIntel} selectedHero={props.selectedHero} />;
    case "chronicle":
      return <Chronicle summary={props.summary} heroIntel={props.heroIntel} heroMap={buildHeroMap(props.summary.heroes)} selectMatch={props.selectMatch} />;
    case "battle-report":
      return <BattleReport matchIntel={props.matchIntel} battleReport={props.battleReport} />;
    default:
      return <WarTable rankedHeroes={props.rankedHeroes} selectedHero={props.selectedHero} summary={props.summary} selectMatch={props.selectMatch} />;
  }
}

function WarTable({ rankedHeroes, selectedHero, summary, selectMatch }) {
  const banLord = [...rankedHeroes].sort((a, b) => safeNumber(b.pro_ban) - safeNumber(a.pro_ban))[0];
  const sleeper = [...rankedHeroes].filter((hero) => hero.meta.picks > 100 && hero.meta.winRate > 0.52).sort((a, b) => a.meta.picks - b.meta.picks)[0];
  return (
    <div className="territory-stack">
      <div className="edict-grid">
        <Edict title="Campaign banner" hero={rankedHeroes[0]} note="Highest blended meta score in the chosen lens." />
        <Edict title="Ban sigil" hero={banLord} note="Loudest professional draft pressure." />
        <Edict title="Sleeper rune" hero={sleeper || selectedHero} note="Positive win signal before the tavern fully catches on." />
      </div>
      <div className="two-column">
        <HeroLeaderboard heroes={rankedHeroes.slice(0, 8)} />
        <RecentMiniFeed matches={summary.proMatches.slice(0, 5)} selectMatch={selectMatch} title="Tournament smoke" />
      </div>
    </div>
  );
}

function Edict({ title, hero, note }) {
  return (
    <div className="edict-card">
      <span>{title}</span>
      <strong>{hero?.localized_name || "Unknown"}</strong>
      <p>{note}</p>
      {hero ? <small>{formatPercent(hero.meta.winRate)} · {formatCompact(hero.meta.picks)} picks · {formatNumber(hero.meta.proHeat)} pro heat</small> : null}
    </div>
  );
}

function HeroLeaderboard({ heroes }) {
  return (
    <div className="sub-panel">
      <h3>Top campaign forces</h3>
      <div className="leaderboard">
        {heroes.map((hero, index) => (
          <div className="leader-row" key={hero.id}>
            <span>{String(index + 1).padStart(2, "0")}</span>
            <strong>{hero.localized_name}</strong>
            <small>{formatPercent(hero.meta.winRate)}</small>
            <small>{formatCompact(hero.meta.picks)} picks</small>
          </div>
        ))}
      </div>
    </div>
  );
}

function Counterlands({ selectedHero, heroIntel, matchupLanes }) {
  if (heroIntel.loading) return <LoadingRunes label="Scouting enemy borders" />;
  return (
    <div className="two-column">
      <MatchupList title={`Favorable routes for ${selectedHero?.localized_name || "hero"}`} rows={matchupLanes.favorable} tone="good" />
      <MatchupList title="Dangerous passes" rows={matchupLanes.dangerous} tone="danger" />
    </div>
  );
}

function MatchupList({ title, rows, tone }) {
  if (!rows.length) return <div className="sub-panel empty-card">No matchup rows returned for this territory.</div>;
  return (
    <div className="sub-panel">
      <h3>{title}</h3>
      <div className="matchup-list">
        {rows.map((row) => (
          <div className={`matchup-row ${tone}`} key={row.hero_id}>
            {heroImage(row.hero, "icon") ? <img src={heroImage(row.hero, "icon")} alt="" /> : null}
            <strong>{row.hero.localized_name}</strong>
            <span>{formatPercent(row.winRate)}</span>
            <small>{formatNumber(row.games)} games</small>
          </div>
        ))}
      </div>
    </div>
  );
}

function TimeRift({ selectedHero, heroIntel, durationCurve }) {
  if (heroIntel.loading) return <LoadingRunes label="Measuring time rifts" />;
  if (!durationCurve.length) return <div className="empty-card">No duration curve returned for {selectedHero?.localized_name || "this hero"}.</div>;
  return (
    <div className="sub-panel full-width">
      <h3>{selectedHero?.localized_name} across match duration</h3>
      <div className="duration-chart">
        {durationCurve.map((row) => (
          <div className="duration-bar" key={row.bin}>
            <div style={{ height: `${row.height}%` }} title={`${formatDuration(row.bin)} · ${formatNumber(row.games)} games`} />
            <strong>{formatPercent(row.winRate)}</strong>
            <span>{Math.round(row.bin / 60)}m</span>
          </div>
        ))}
      </div>
      <p className="panel-note">Bars show game volume by duration bin; labels show win rate in that time band.</p>
    </div>
  );
}

function ItemForge({ selectedHero, heroIntel, itemPhases, itemMap, itemError }) {
  if (heroIntel.loading) return <LoadingRunes label="Heating the item forge" />;
  return (
    <div className="territory-stack">
      {itemError ? <WarningList warnings={[`Item constants failed: ${itemError}`]} /> : null}
      {!itemMap.size ? <p className="panel-note">Item names are being loaded from OpenDota constants. Fallback relic IDs are shown until then.</p> : null}
      <div className="phase-grid">
        {itemPhases.map((phase) => (
          <div className="sub-panel" key={phase.key}>
            <h3>{phase.label}</h3>
            {phase.entries.length ? phase.entries.map((item) => <ItemRow key={item.id} item={item} />) : <p className="panel-note">No items returned for {selectedHero?.localized_name || "this hero"}.</p>}
          </div>
        ))}
      </div>
    </div>
  );
}

function ItemRow({ item }) {
  return (
    <div className="item-row">
      {item.img ? <img src={item.img} alt="" /> : <span className="icon-fallback" />}
      <strong>{item.name}</strong>
      <small>{formatNumber(item.count)} sightings</small>
      <small>{item.cost ? `${formatNumber(item.cost)}g` : "cost unknown"}</small>
    </div>
  );
}

function AdeptTower({ specialists, heroIntel, selectedHero }) {
  if (heroIntel.loading) return <LoadingRunes label="Finding hero specialists" />;
  if (!specialists.length) return <div className="empty-card">No specialist aggregates returned.</div>;
  return (
    <div className="sub-panel full-width">
      <h3>{selectedHero?.localized_name} specialist tower</h3>
      <p className="panel-note">Raw account IDs are intentionally hidden; these are anonymized aggregate ranks from public OpenDota data.</p>
      <div className="specialist-grid">
        {specialists.map((player) => (
          <div className="specialist-card" key={player.label}>
            <span>{player.label}</span>
            <strong>{formatNumber(player.games)} games</strong>
            <small>{formatPercent(player.winRate)} win rate · {formatNumber(player.wins)} wins</small>
          </div>
        ))}
      </div>
    </div>
  );
}

function Chronicle({ summary, heroIntel, heroMap, selectMatch }) {
  return (
    <div className="territory-stack">
      <div className="two-column">
        <RecentMiniFeed matches={summary.proMatches.slice(0, 8)} selectMatch={selectMatch} title="Pro battle banners" />
        <PublicDraftFeed matches={summary.publicMatches.slice(0, 8)} heroMap={heroMap} selectMatch={selectMatch} />
      </div>
      <RecentHeroMatches matches={heroIntel.matches} loading={heroIntel.loading} selectMatch={selectMatch} />
    </div>
  );
}

function RecentMiniFeed({ matches, selectMatch, title }) {
  return (
    <div className="sub-panel">
      <h3>{title}</h3>
      {matches.length ? matches.map((match) => (
        <button className="battle-card" type="button" key={match.match_id} onClick={() => selectMatch(match.match_id)}>
          <strong>{match.league_name || "Unknown league"}</strong>
          <span>{match.radiant_name || "Radiant"} vs {match.dire_name || "Dire"}</span>
          <small>{formatDate(match.start_time)} · {formatDuration(match.duration)} · {safeNumber(match.radiant_score)}-{safeNumber(match.dire_score)}</small>
        </button>
      )) : <p className="panel-note">No pro match summaries returned.</p>}
    </div>
  );
}

function PublicDraftFeed({ matches, heroMap, selectMatch }) {
  return (
    <div className="sub-panel">
      <h3>Public draft pulses</h3>
      {matches.length ? matches.map((match) => (
        <button className="battle-card" type="button" key={match.match_id} onClick={() => selectMatch(match.match_id)}>
          <strong>{match.radiant_win ? "Radiant" : "Dire"} victory in {rankLabel(match.avg_rank_tier)}</strong>
          <DraftIcons ids={[...(match.radiant_team || []), ...(match.dire_team || [])].slice(0, 10)} heroMap={heroMap} />
          <small>{formatDate(match.start_time)} · {formatDuration(match.duration)} · Match #{match.match_id}</small>
        </button>
      )) : <p className="panel-note">No public match summaries returned.</p>}
    </div>
  );
}

function RecentHeroMatches({ matches, loading, selectMatch }) {
  return (
    <div className="sub-panel full-width">
      <h3>Selected hero recent raids</h3>
      {loading ? <LoadingRunes label="Gathering selected hero raids" /> : null}
      <div className="hero-match-grid">
        {!loading && matches.length ? matches.slice(0, 8).map((match) => (
          <button className="hero-match-card" key={match.match_id} type="button" onClick={() => selectMatch(match.match_id)}>
            <strong>{match.league_name || "Public battlefield"}</strong>
            <span>{safeNumber(match.kills)}/{safeNumber(match.deaths)}/{safeNumber(match.assists)}</span>
            <small>{formatDate(match.start_time)} · {formatDuration(match.duration)}</small>
          </button>
        )) : null}
        {!loading && !matches.length ? <p className="panel-note">No recent hero matches returned.</p> : null}
      </div>
    </div>
  );
}

function BattleReport({ matchIntel, battleReport }) {
  if (!matchIntel.matchId) return <div className="empty-card">Select a battle from the Chronicle to open a focused match report.</div>;
  if (matchIntel.loading) return <LoadingRunes label={`Opening match ${matchIntel.matchId}`} />;
  if (matchIntel.error) return <div className="empty-card">Battle report failed: {matchIntel.error}</div>;
  if (!battleReport) return <div className="empty-card">No usable battle report returned.</div>;

  return (
    <div className="territory-stack">
      <div className="battle-report-hero">
        <div>
          <p className="eyebrow">Match #{battleReport.matchId}</p>
          <h3>{battleReport.radiantName} vs {battleReport.direName}</h3>
          <p>{battleReport.league} · {formatDuration(battleReport.duration)} · Patch {battleReport.patch || "unknown"}</p>
        </div>
        <a className="gold-link" href={`${OPEN_DOTA_MATCH}${battleReport.matchId}`} target="_blank" rel="noreferrer">Open in OpenDota</a>
      </div>
      <div className="edict-grid">
        <StatTile label="Victor" value={battleReport.radiantWin ? battleReport.radiantName : battleReport.direName} detail={`${battleReport.radiantScore}-${battleReport.direScore}`} />
        <StatTile label="Teamfights" value={formatNumber(battleReport.teamfights)} detail="parsed from match detail" />
        <StatTile label="Objectives" value={formatNumber(battleReport.objectiveCount)} detail="first objectives summarized" />
      </div>
      <div className="two-column">
        <Scoreboard players={battleReport.players.filter((player) => player.isRadiant)} title="Radiant warband" />
        <Scoreboard players={battleReport.players.filter((player) => !player.isRadiant)} title="Dire warband" />
      </div>
      <div className="edict-grid">
        <LeaderCard title="Damage commander" player={battleReport.leaders.damage} metric={formatCompact(battleReport.leaders.damage?.damage)} />
        <LeaderCard title="Gold commander" player={battleReport.leaders.netWorth} metric={formatCompact(battleReport.leaders.netWorth?.netWorth)} />
        <LeaderCard title="KDA commander" player={battleReport.leaders.kda} metric={battleReport.leaders.kda?.kda.toFixed(1)} />
      </div>
    </div>
  );
}

function Scoreboard({ players, title }) {
  return (
    <div className="sub-panel">
      <h3>{title}</h3>
      <div className="scoreboard">
        {players.map((player) => (
          <div className="score-row" key={`${player.slot}-${player.hero?.id || player.name}`}>
            {heroImage(player.hero, "icon") ? <img src={heroImage(player.hero, "icon")} alt="" /> : <span className="icon-fallback" />}
            <strong>{player.hero?.localized_name || player.name}</strong>
            <span>{player.kills}/{player.deaths}/{player.assists}</span>
            <small>{formatCompact(player.netWorth)} NW</small>
          </div>
        ))}
      </div>
    </div>
  );
}

function LeaderCard({ title, player, metric }) {
  return (
    <div className="edict-card">
      <span>{title}</span>
      <strong>{player?.hero?.localized_name || player?.name || "Unknown"}</strong>
      <p>{metric || "0"}</p>
      <small>{player ? `${player.kills}/${player.deaths}/${player.assists}` : "No player row"}</small>
    </div>
  );
}

function DraftIcons({ ids, heroMap }) {
  return (
    <div className="draft-icons">
      {ids.map((id, index) => {
        const hero = heroMap.get(Number(id));
        return hero && heroImage(hero, "icon") ? <img key={`${id}-${index}`} src={heroImage(hero, "icon")} alt={hero.localized_name} title={hero.localized_name} /> : <span key={`${id}-${index}`}>?</span>;
      })}
    </div>
  );
}

function WarningList({ warnings, label = "Scrying warnings" }) {
  return (
    <div className="warning-list" role="status">
      <strong>{label}</strong>
      {warnings.map((warning) => <span key={warning}>{warning}</span>)}
    </div>
  );
}

function LoadingRunes({ label }) {
  return (
    <div className="loading-runes">
      <span aria-hidden="true" />
      <strong>{label}...</strong>
    </div>
  );
}

function settledData(result) {
  return result.status === "fulfilled" ? result.value : [];
}

function settledError(result, label) {
  return result.status === "rejected" ? `${label}: ${result.reason?.message || "request failed"}` : "";
}

createRoot(document.getElementById("root")).render(<App />);
