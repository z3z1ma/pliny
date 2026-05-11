const API_BASE = "https://api.opendota.com/api";
const STEAM_CDN = "https://cdn.cloudflare.steamstatic.com";

const FALLBACK_HEROES = [
  heroFixture(2, "Axe", "str", "Melee", ["Initiator", "Durable", "Disabler", "Carry"], 183, 96, 712000, 369000, "axe"),
  heroFixture(5, "Crystal Maiden", "int", "Ranged", ["Support", "Disabler", "Nuker"], 164, 84, 690000, 352000, "crystal_maiden"),
  heroFixture(8, "Juggernaut", "agi", "Melee", ["Carry", "Pusher", "Escape"], 142, 75, 782000, 401000, "juggernaut"),
  heroFixture(14, "Pudge", "str", "Melee", ["Disabler", "Initiator", "Durable", "Nuker"], 105, 51, 1120000, 563000, "pudge"),
  heroFixture(21, "Windranger", "all", "Ranged", ["Carry", "Support", "Disabler", "Escape", "Nuker"], 132, 72, 520000, 277000, "windrunner"),
  heroFixture(22, "Zeus", "int", "Ranged", ["Nuker", "Carry"], 121, 66, 640000, 336000, "zuus"),
  heroFixture(35, "Sniper", "agi", "Ranged", ["Carry", "Nuker"], 117, 61, 760000, 379000, "sniper"),
  heroFixture(74, "Invoker", "int", "Ranged", ["Carry", "Nuker", "Disabler", "Escape", "Pusher"], 155, 81, 618000, 304000, "invoker"),
  heroFixture(86, "Rubick", "int", "Ranged", ["Support", "Disabler", "Nuker"], 188, 91, 428000, 210000, "rubick"),
  heroFixture(97, "Magnus", "all", "Melee", ["Initiator", "Disabler", "Nuker", "Escape"], 151, 80, 360000, 190000, "magnataur"),
  heroFixture(106, "Ember Spirit", "agi", "Melee", ["Carry", "Escape", "Nuker", "Disabler", "Initiator"], 170, 86, 408000, 206000, "ember_spirit"),
  heroFixture(120, "Pangolier", "all", "Melee", ["Carry", "Nuker", "Disabler", "Durable", "Escape", "Initiator"], 176, 92, 390000, 205000, "pangolier")
];

const FALLBACK_MATCHES = [
  matchFixture(8806354486, "Vitality Warriors", "CrimsonSky", 23, 29, false, "Dota 2 Space League", 1585),
  matchFixture(8806335556, "CrimsonSky", "Vitality Warriors", 28, 20, true, "Dota 2 Space League", 1534),
  matchFixture(8806065028, "Nigma Galaxy", "PlayTime", 21, 29, false, "1win Essence I", 3164),
  matchFixture(8805862156, "PARIVISION", "1w Team", 41, 18, true, "1win Essence I", 2373),
  matchFixture(8805527012, "Two Move", "Rune Eaters", 45, 18, true, "European Pro League", 2440),
  matchFixture(8803798979, "Tundra Esports", "Yellow Submarine", 14, 30, false, "1win Essence I", 1948)
];

const ROLES = ["All", "Carry", "Support", "Nuker", "Disabler", "Initiator", "Durable", "Escape", "Pusher"];
const ATTRIBUTES = ["All", "str", "agi", "int", "all"];
const LENSES = {
  Tempo: {
    title: "Hit before the enemy techs up.",
    copy: "Fast cores and mobile nukers with enough presence to force early objectives.",
    roles: ["Carry", "Escape", "Nuker"],
    attack: null
  },
  Siege: {
    title: "Turn one won fight into a fallen lane.",
    copy: "Pushers and durable frontliners that convert map control into building damage.",
    roles: ["Pusher", "Durable", "Carry"],
    attack: null
  },
  Brawl: {
    title: "Drag the fight into the river and never leave.",
    copy: "Initiators and disablers that reward constant skirmishing around runes and towers.",
    roles: ["Initiator", "Disabler", "Durable"],
    attack: "Melee"
  },
  Control: {
    title: "Win the screen before the fight begins.",
    copy: "Supports, nukers, and layered disables that make enemy movement feel expensive.",
    roles: ["Support", "Disabler", "Nuker"],
    attack: "Ranged"
  }
};

const state = {
  heroes: [],
  matches: [],
  role: "All",
  attr: "All",
  lens: "Tempo",
  search: "",
  selectedMatchId: null
};

const els = {};

document.addEventListener("DOMContentLoaded", init);

function init() {
  cacheElements();
  bindControls();
  renderLoadingState();
  loadOpenDotaData();
}

function cacheElements() {
  [
    "data-status",
    "pulse-hero",
    "pulse-copy",
    "stat-heroes",
    "stat-matches",
    "stat-radiant",
    "stat-duration",
    "briefing-title",
    "briefing-copy",
    "signal-list",
    "role-filters",
    "attr-filters",
    "hero-search",
    "contested-list",
    "winrate-list",
    "hero-grid",
    "lens-tabs",
    "lens-kicker",
    "lens-title",
    "lens-copy",
    "lens-picks",
    "match-list",
    "match-detail"
  ].forEach((id) => {
    els[toCamel(id)] = document.getElementById(id);
  });
}

function bindControls() {
  els.heroSearch.addEventListener("input", (event) => {
    state.search = event.target.value.trim().toLowerCase();
    renderHeroes();
  });

  document.querySelectorAll("[data-scroll-target]").forEach((node) => {
    node.addEventListener("click", () => {
      document.querySelectorAll("[data-scroll-target]").forEach((item) => item.classList.remove("active"));
      node.classList.add("active");
      document.getElementById(node.dataset.scrollTarget).scrollIntoView({ behavior: "smooth", block: "start" });
    });
  });
}

async function loadOpenDotaData() {
  const [heroesResult, matchesResult] = await Promise.allSettled([
    fetchJson(`${API_BASE}/heroStats`),
    fetchJson(`${API_BASE}/proMatches`)
  ]);

  const liveSources = [];
  const fallbackSources = [];

  if (heroesResult.status === "fulfilled" && Array.isArray(heroesResult.value)) {
    state.heroes = heroesResult.value.map(normalizeHero).filter(Boolean);
    liveSources.push("hero meta");
  } else {
    state.heroes = FALLBACK_HEROES.map(normalizeHero);
    fallbackSources.push("hero meta");
  }

  if (matchesResult.status === "fulfilled" && Array.isArray(matchesResult.value)) {
    state.matches = matchesResult.value.map(normalizeMatch).filter(Boolean).slice(0, 40);
    liveSources.push("pro matches");
  } else {
    state.matches = FALLBACK_MATCHES.map(normalizeMatch);
    fallbackSources.push("pro matches");
  }

  state.selectedMatchId = state.matches[0]?.match_id ?? null;
  setDataStatus(liveSources, fallbackSources);
  renderAll();
}

async function fetchJson(url) {
  const response = await fetch(url, { headers: { Accept: "application/json" } });
  if (!response.ok) {
    throw new Error(`OpenDota request failed: ${response.status}`);
  }
  return response.json();
}

function renderLoadingState() {
  renderFilters();
  renderLensTabs();
  els.heroGrid.innerHTML = Array.from({ length: 8 }, () => '<div class="loading-card"></div>').join("");
  els.matchList.innerHTML = Array.from({ length: 6 }, () => '<div class="loading-card"></div>').join("");
  els.matchDetail.innerHTML = '<div class="empty-state">Scouts are crossing the river with fresh match parchments.</div>';
}

function renderAll() {
  renderHeroSummary();
  renderBriefing();
  renderFilters();
  renderRankLists();
  renderHeroes();
  renderLensTabs();
  renderLensPicks();
  renderMatches();
}

function renderHeroSummary() {
  const heroes = sortedHeroes();
  const topHero = heroes[0];
  const radiantWins = state.matches.filter((match) => match.radiant_win).length;
  const avgDuration = average(state.matches.map((match) => match.duration));
  const radiantRate = state.matches.length ? radiantWins / state.matches.length : 0;

  els.statHeroes.textContent = formatNumber(state.heroes.length);
  els.statMatches.textContent = formatNumber(state.matches.length);
  els.statRadiant.textContent = percent(radiantRate);
  els.statDuration.textContent = formatDuration(avgDuration);

  if (topHero) {
    els.pulseHero.textContent = topHero.localized_name;
    els.pulseCopy.textContent = `${percent(topHero.winRate)} win pressure across ${formatNumber(topHero.presence)} tracked picks.`;
  }
}

function renderBriefing() {
  const heroes = sortedHeroes();
  const contested = sortBy(state.heroes, (hero) => hero.proPick).slice(0, 3);
  const fastest = state.matches.length ? sortBy(state.matches, (match) => -match.duration)[0] : null;
  const longest = state.matches.length ? sortBy(state.matches, (match) => match.duration)[0] : null;

  els.briefingTitle.textContent = heroes[0] ? `${heroes[0].localized_name} is glowing on the altar` : "Awaiting scouts";
  els.briefingCopy.textContent = heroes[0]
    ? "The highest meta signal combines win pressure, professional presence, and public-volume gravity."
    : "The courier is collecting hero stats and match records.";

  const signals = [
    ["Top omen", heroes[0]?.localized_name ?? "Unknown"],
    ["Most contested", contested.map((hero) => hero.localized_name).join(", ") || "Unknown"],
    ["Fastest battle", fastest ? `${formatDuration(fastest.duration)} in ${safeText(fastest.league_name)}` : "Unknown"],
    ["Longest siege", longest ? `${formatDuration(longest.duration)} in ${safeText(longest.league_name)}` : "Unknown"]
  ];

  els.signalList.innerHTML = signals
    .map(
      ([label, value]) => `
        <div class="signal">
          <span>${escapeHtml(label)}</span>
          <strong>${escapeHtml(value)}</strong>
        </div>
      `
    )
    .join("");
}

function renderFilters() {
  els.roleFilters.innerHTML = ROLES.map((role) => filterButton(role, state.role, "role")).join("");
  els.attrFilters.innerHTML = ATTRIBUTES.map((attr) => filterButton(attrLabel(attr), state.attr, "attr", attr)).join("");

  els.roleFilters.querySelectorAll("button").forEach((button) => {
    button.addEventListener("click", () => {
      state.role = button.dataset.value;
      renderFilters();
      renderHeroes();
    });
  });

  els.attrFilters.querySelectorAll("button").forEach((button) => {
    button.addEventListener("click", () => {
      state.attr = button.dataset.value;
      renderFilters();
      renderHeroes();
    });
  });
}

function filterButton(label, activeValue, type, value = label) {
  const active = value === activeValue ? " active" : "";
  return `<button class="pill${active}" type="button" data-filter="${type}" data-value="${escapeHtml(value)}">${escapeHtml(label)}</button>`;
}

function renderRankLists() {
  const contested = sortBy(state.heroes, (hero) => hero.proPick || hero.presence).slice(0, 5);
  const winrates = sortedHeroes().filter((hero) => hero.presence >= 25).slice(0, 5);

  els.contestedList.innerHTML = contested.map((hero, index) => rankItem(hero, index, formatNumber(hero.proPick || hero.presence))).join("");
  els.winrateList.innerHTML = winrates.map((hero, index) => rankItem(hero, index, percent(hero.winRate))).join("");
}

function rankItem(hero, index, score) {
  return `
    <div class="rank-item">
      <span class="rank-score">${index + 1}</span>
      <div>
        <strong>${escapeHtml(hero.localized_name)}</strong>
        <small>${escapeHtml(hero.roles.slice(0, 3).join(" / "))}</small>
      </div>
      <div>
        <img src="${heroImage(hero)}" alt="" loading="lazy" />
        <span class="rank-score">${escapeHtml(score)}</span>
      </div>
    </div>
  `;
}

function renderHeroes() {
  const heroes = filteredHeroes().slice(0, 24);

  if (!heroes.length) {
    els.heroGrid.innerHTML = '<div class="empty-state">No heroes match this tavern order. Try clearing a filter.</div>';
    return;
  }

  els.heroGrid.innerHTML = heroes.map(heroCard).join("");
}

function heroCard(hero) {
  const roles = hero.roles.slice(0, 4).map((role) => `<span>${escapeHtml(role)}</span>`).join("");
  return `
    <article class="hero-card">
      <img src="${heroImage(hero)}" alt="${escapeHtml(hero.localized_name)} portrait" loading="lazy" />
      <div class="hero-body">
        <div class="hero-title">
          <h3>${escapeHtml(hero.localized_name)}</h3>
          <span class="attr-badge attr-${escapeHtml(hero.primary_attr)}">${escapeHtml(attrLabel(hero.primary_attr))}</span>
        </div>
        <small>${escapeHtml(hero.attack_type)} ${hero.attack_type === "Melee" ? "frontliner" : "spell range"}</small>
        <div class="role-tags">${roles}</div>
        <div class="hero-metrics" aria-label="Hero metrics">
          <div class="metric">
            <span class="metric-value">${percent(hero.winRate)}</span>
            <span class="mini-label">win rate</span>
          </div>
          <div class="metric">
            <span class="metric-value">${formatNumber(hero.proPick)}</span>
            <span class="mini-label">pro picks</span>
          </div>
          <div class="metric">
            <span class="metric-value">${Math.round(hero.metaScore)}</span>
            <span class="mini-label">omen</span>
          </div>
        </div>
      </div>
    </article>
  `;
}

function renderLensTabs() {
  els.lensTabs.innerHTML = Object.keys(LENSES)
    .map((lens) => `<button class="lens-tab${lens === state.lens ? " active" : ""}" type="button" data-lens="${lens}">${lens}</button>`)
    .join("");

  els.lensTabs.querySelectorAll("button").forEach((button) => {
    button.addEventListener("click", () => {
      state.lens = button.dataset.lens;
      renderLensTabs();
      renderLensPicks();
    });
  });
}

function renderLensPicks() {
  const lens = LENSES[state.lens];
  const picks = sortedHeroes()
    .filter((hero) => lens.roles.some((role) => hero.roles.includes(role)))
    .filter((hero) => !lens.attack || hero.attack_type === lens.attack)
    .slice(0, 4);

  els.lensKicker.textContent = `${state.lens} lens`;
  els.lensTitle.textContent = lens.title;
  els.lensCopy.textContent = lens.copy;
  els.lensPicks.innerHTML = picks.map(pickToken).join("") || '<div class="empty-state">No picks found for this lens yet.</div>';
}

function pickToken(hero) {
  return `
    <article class="pick-token">
      <img src="${heroImage(hero)}" alt="" loading="lazy" />
      <div>
        <strong>${escapeHtml(hero.localized_name)}</strong>
        <small>${percent(hero.winRate)} WR, ${formatNumber(hero.proPick)} pro picks</small>
      </div>
    </article>
  `;
}

function renderMatches() {
  els.matchList.innerHTML = state.matches.map(matchRow).join("") || '<div class="empty-state">No recent matches found.</div>';

  els.matchList.querySelectorAll("button").forEach((button) => {
    button.addEventListener("click", () => {
      state.selectedMatchId = Number(button.dataset.matchId);
      renderMatches();
    });
  });

  renderMatchDetail();
}

function matchRow(match) {
  const radiantWinner = match.radiant_win;
  const active = match.match_id === state.selectedMatchId ? " active" : "";
  return `
    <button class="match-row${active}" type="button" data-match-id="${match.match_id}">
      <div class="teams">
        <div class="team-line${radiantWinner ? " winner" : ""}">
          <span class="team-name">${escapeHtml(teamName(match.radiant_name, "Radiant"))}</span>
          <span class="score">${formatNumber(match.radiant_score)}</span>
        </div>
        <div class="team-line${!radiantWinner ? " winner" : ""}">
          <span class="team-name">${escapeHtml(teamName(match.dire_name, "Dire"))}</span>
          <span class="score">${formatNumber(match.dire_score)}</span>
        </div>
      </div>
      <div class="match-meta">
        <span>${formatDuration(match.duration)}</span>
        <span>${escapeHtml(matchTempo(match.duration, match.radiant_score + match.dire_score))}</span>
        <span>${escapeHtml(relativeTime(match.start_time))}</span>
      </div>
    </button>
  `;
}

function renderMatchDetail() {
  const match = state.matches.find((item) => item.match_id === state.selectedMatchId) ?? state.matches[0];
  if (!match) {
    els.matchDetail.innerHTML = '<div class="empty-state">Select a battle to reveal the parchment.</div>';
    return;
  }

  const winner = match.radiant_win ? teamName(match.radiant_name, "Radiant") : teamName(match.dire_name, "Dire");
  const killTotal = match.radiant_score + match.dire_score;
  const tempo = matchTempo(match.duration, killTotal);
  const stomp = Math.abs(match.radiant_score - match.dire_score) >= 18 ? "Decisive" : "Contested";

  els.matchDetail.innerHTML = `
    <p class="eyebrow">Selected Battle</p>
    <h3>${escapeHtml(winner)} claimed the throne</h3>
    <p>${escapeHtml(match.league_name || "Unknown league")} ended as a ${escapeHtml(tempo.toLowerCase())} with ${formatNumber(killTotal)} total kills.</p>
    <div class="detail-score">
      <div class="detail-team">
        <span>Radiant</span>
        <strong>${escapeHtml(teamName(match.radiant_name, "Radiant"))}</strong>
      </div>
      <div class="versus">${formatNumber(match.radiant_score)} - ${formatNumber(match.dire_score)}</div>
      <div class="detail-team">
        <span>Dire</span>
        <strong>${escapeHtml(teamName(match.dire_name, "Dire"))}</strong>
      </div>
    </div>
    <div class="detail-grid">
      <div class="detail-tile"><span>Duration</span><strong>${formatDuration(match.duration)}</strong></div>
      <div class="detail-tile"><span>Battle type</span><strong>${escapeHtml(tempo)}</strong></div>
      <div class="detail-tile"><span>Readout</span><strong>${escapeHtml(stomp)}</strong></div>
      <div class="detail-tile"><span>Started</span><strong>${escapeHtml(relativeTime(match.start_time))}</strong></div>
    </div>
    <a class="button ghost small" href="https://www.opendota.com/matches/${match.match_id}" target="_blank" rel="noreferrer">Open match scroll</a>
  `;
}

function filteredHeroes() {
  return sortedHeroes().filter((hero) => {
    const matchesRole = state.role === "All" || hero.roles.includes(state.role);
    const matchesAttr = state.attr === "All" || hero.primary_attr === state.attr;
    const haystack = `${hero.localized_name} ${hero.attack_type} ${hero.roles.join(" ")}`.toLowerCase();
    const matchesSearch = !state.search || haystack.includes(state.search);
    return matchesRole && matchesAttr && matchesSearch;
  });
}

function sortedHeroes() {
  return [...state.heroes].sort((a, b) => b.metaScore - a.metaScore);
}

function normalizeHero(hero) {
  if (!hero || !hero.localized_name) return null;
  const proPick = Number(hero.pro_pick || hero.proPick || 0);
  const proWin = Number(hero.pro_win || hero.proWin || 0);
  const pubPick = Number(hero.pub_pick || hero.pubPick || 0);
  const pubWin = Number(hero.pub_win || hero.pubWin || 0);
  const presence = proPick > 0 ? proPick : pubPick;
  const winRate = proPick >= 10 ? safeRate(proWin, proPick) : safeRate(pubWin, pubPick);
  const metaScore = winRate * 100 + Math.log10(presence + 1) * 9 + Math.min(proPick, 260) / 12;

  return {
    ...hero,
    primary_attr: hero.primary_attr || "all",
    attack_type: hero.attack_type || "Unknown",
    roles: Array.isArray(hero.roles) ? hero.roles : [],
    proPick,
    proWin,
    pubPick,
    pubWin,
    presence,
    winRate,
    metaScore
  };
}

function normalizeMatch(match) {
  if (!match || !match.match_id) return null;
  return {
    match_id: Number(match.match_id),
    duration: Number(match.duration || 0),
    start_time: Number(match.start_time || Date.now() / 1000),
    radiant_name: match.radiant_name || match.radiant_team_name || match.radiantName,
    dire_name: match.dire_name || match.dire_team_name || match.direName,
    radiant_score: Number(match.radiant_score || 0),
    dire_score: Number(match.dire_score || 0),
    radiant_win: Boolean(match.radiant_win),
    league_name: match.league_name || "Unknown league"
  };
}

function heroFixture(id, name, attr, attackType, roles, proPick, proWin, pubPick, pubWin, slug) {
  return {
    id,
    localized_name: name,
    primary_attr: attr,
    attack_type: attackType,
    roles,
    pro_pick: proPick,
    pro_win: proWin,
    pub_pick: pubPick,
    pub_win: pubWin,
    img: `/apps/dota2/images/dota_react/heroes/${slug}.png`
  };
}

function matchFixture(matchId, radiantName, direName, radiantScore, direScore, radiantWin, leagueName, duration) {
  return {
    match_id: matchId,
    radiant_name: radiantName,
    dire_name: direName,
    radiant_score: radiantScore,
    dire_score: direScore,
    radiant_win: radiantWin,
    league_name: leagueName,
    duration,
    start_time: Math.floor(Date.now() / 1000) - Math.floor(Math.random() * 86400)
  };
}

function setDataStatus(liveSources, fallbackSources) {
  const liveText = liveSources.length ? `Live ${liveSources.join(" + ")}` : "";
  const fallbackText = fallbackSources.length ? `cached ${fallbackSources.join(" + ")}` : "";
  const text = [liveText, fallbackText].filter(Boolean).join("; ") || "Demo data loaded";
  els.dataStatus.textContent = text;
  els.dataStatus.classList.toggle("is-warn", fallbackSources.length > 0);
}

function heroImage(hero) {
  if (hero.img?.startsWith("http")) return hero.img;
  if (hero.img) return `${STEAM_CDN}${hero.img}`;
  if (hero.icon) return `${STEAM_CDN}${hero.icon}`;
  return "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 320 180'%3E%3Crect width='320' height='180' fill='%23160f0a'/%3E%3Cpath d='M30 140 160 28l130 112' fill='none' stroke='%23f0c15a' stroke-width='10'/%3E%3Ccircle cx='160' cy='88' r='34' fill='%237fd057' opacity='.7'/%3E%3C/svg%3E";
}

function matchTempo(duration, kills) {
  const killsPerMinute = duration ? kills / (duration / 60) : 0;
  if (duration < 1500 && killsPerMinute > 1.6) return "Blood Rush";
  if (duration < 1800) return "Fast Push";
  if (duration > 3000) return "Elder Siege";
  if (killsPerMinute > 1.45) return "Constant Brawl";
  return "Measured War";
}

function relativeTime(timestamp) {
  const seconds = Math.max(0, Math.floor(Date.now() / 1000 - timestamp));
  const days = Math.floor(seconds / 86400);
  const hours = Math.floor(seconds / 3600);
  const minutes = Math.floor(seconds / 60);
  if (days > 0) return `${days}d ago`;
  if (hours > 0) return `${hours}h ago`;
  if (minutes > 0) return `${minutes}m ago`;
  return "just now";
}

function attrLabel(attr) {
  return {
    All: "All",
    str: "Strength",
    agi: "Agility",
    int: "Intelligence",
    all: "Universal"
  }[attr] || attr;
}

function teamName(name, fallback) {
  return name?.trim() || `${fallback} Ancients`;
}

function safeRate(wins, picks) {
  return picks > 0 ? wins / picks : 0;
}

function average(values) {
  const usable = values.filter((value) => Number.isFinite(value) && value > 0);
  return usable.length ? usable.reduce((sum, value) => sum + value, 0) / usable.length : 0;
}

function sortBy(items, selector) {
  return [...items].sort((a, b) => selector(b) - selector(a));
}

function formatDuration(seconds) {
  if (!seconds) return "--";
  const minutes = Math.floor(seconds / 60);
  const remainder = Math.round(seconds % 60).toString().padStart(2, "0");
  return `${minutes}:${remainder}`;
}

function percent(value) {
  if (!Number.isFinite(value)) return "--";
  return `${Math.round(value * 100)}%`;
}

function formatNumber(value) {
  return new Intl.NumberFormat("en", { notation: Number(value) >= 10000 ? "compact" : "standard" }).format(Number(value) || 0);
}

function safeText(value) {
  return value || "Unknown league";
}

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function toCamel(id) {
  return id.replace(/-([a-z])/g, (_, letter) => letter.toUpperCase());
}
