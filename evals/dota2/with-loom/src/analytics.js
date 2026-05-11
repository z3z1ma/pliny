import { dotaAsset } from "./api";

export const BRACKETS = {
  pub: "All public",
  pro: "Professional",
  1: "Herald / Guardian",
  2: "Crusader",
  3: "Archon",
  4: "Legend",
  5: "Ancient",
  6: "Divine",
  7: "Immortal",
  8: "Immortal elite",
};

export const ROLE_ORDER = ["All", "Carry", "Support", "Nuker", "Disabler", "Durable", "Escape", "Initiator", "Pusher", "Jungler"];

export function normalizeHero(hero) {
  if (!hero || !hero.id) return null;
  return {
    ...hero,
    id: Number(hero.id),
    localized_name: hero.localized_name || hero.name || "Unknown hero",
    roles: Array.isArray(hero.roles) ? hero.roles : [],
    primary_attr: hero.primary_attr || "all",
    attack_type: hero.attack_type || "Unknown",
  };
}

export function buildHeroMap(heroes) {
  return new Map(heroes.map((hero) => [hero.id, hero]));
}

export function buildItemMap(items) {
  const map = new Map();
  Object.values(items || {}).forEach((item) => {
    if (!item || !item.id) return;
    map.set(Number(item.id), {
      id: Number(item.id),
      name: item.dname || item.name || `Relic ${item.id}`,
      cost: safeNumber(item.cost),
      img: dotaAsset(item.img, ["/apps/dota2/images/dota_react/items/"]),
    });
  });
  return map;
}

export function rankHeroes(heroes, bracket, sortMode) {
  const base = heroes.map((hero) => ({ ...hero, meta: getHeroMeta(hero, bracket) }));
  const maxPicks = Math.max(1, ...base.map((hero) => hero.meta.picks));
  return base
    .map((hero) => {
      const proHeat = safeNumber(hero.pro_pick) + safeNumber(hero.pro_ban);
      const pickPressure = Math.sqrt(hero.meta.picks / maxPicks);
      const metaScore = hero.meta.picks
        ? hero.meta.winRate * 68 + pickPressure * 22 + Math.min(proHeat / 80, 1) * 10
        : 0;
      return { ...hero, meta: { ...hero.meta, proHeat, metaScore } };
    })
    .sort((a, b) => sortHeroes(a, b, sortMode));
}

export function filterHeroes(heroes, { query, role }) {
  const search = query.trim().toLowerCase();
  return heroes.filter((hero) => {
    const matchesSearch = !search || hero.localized_name.toLowerCase().includes(search);
    const matchesRole = role === "All" || hero.roles.includes(role);
    return matchesSearch && matchesRole;
  });
}

export function getHeroMeta(hero, bracket) {
  if (bracket === "pro") {
    const picks = safeNumber(hero.pro_pick);
    const wins = safeNumber(hero.pro_win);
    return { picks, wins, bans: safeNumber(hero.pro_ban), winRate: picks ? wins / picks : 0, label: BRACKETS.pro };
  }
  if (bracket === "pub") {
    const picks = safeNumber(hero.pub_pick);
    const wins = safeNumber(hero.pub_win);
    return { picks, wins, bans: safeNumber(hero.pro_ban), winRate: picks ? wins / picks : 0, label: BRACKETS.pub };
  }
  const picks = safeNumber(hero[`${bracket}_pick`]);
  const wins = safeNumber(hero[`${bracket}_win`]);
  return { picks, wins, bans: safeNumber(hero.pro_ban), winRate: picks ? wins / picks : 0, label: BRACKETS[bracket] || "Selected bracket" };
}

export function getMatchupLanes(matchups, heroMap) {
  const normalized = (matchups || [])
    .map((matchup) => {
      const games = safeNumber(matchup.games_played);
      const wins = safeNumber(matchup.wins);
      return {
        ...matchup,
        hero: heroMap.get(Number(matchup.hero_id)),
        games,
        wins,
        winRate: games ? wins / games : 0,
      };
    })
    .filter((matchup) => matchup.hero && matchup.games >= 10);

  return {
    favorable: [...normalized].sort((a, b) => b.winRate - a.winRate || b.games - a.games).slice(0, 8),
    dangerous: [...normalized].sort((a, b) => a.winRate - b.winRate || b.games - a.games).slice(0, 8),
  };
}

export function getDurationCurve(durations) {
  const rows = [...(durations || [])]
    .map((row) => ({
      bin: safeNumber(row.duration_bin),
      games: safeNumber(row.games_played),
      wins: safeNumber(row.wins),
      winRate: safeNumber(row.games_played) ? safeNumber(row.wins) / safeNumber(row.games_played) : 0,
    }))
    .filter((row) => row.games > 0)
    .sort((a, b) => a.bin - b.bin);
  const maxGames = Math.max(1, ...rows.map((row) => row.games));
  return rows.map((row) => ({ ...row, height: Math.max(8, (row.games / maxGames) * 100) }));
}

export function getItemPhases(itemPopularity, itemMap) {
  const phases = [
    ["start_game_items", "Opening satchel"],
    ["early_game_items", "Lane relics"],
    ["mid_game_items", "Warpath arsenal"],
    ["late_game_items", "Ancient armory"],
  ];

  return phases.map(([key, label]) => {
    const entries = Object.entries(itemPopularity?.[key] || {})
      .map(([itemId, count]) => {
        const item = itemMap.get(Number(itemId));
        return {
          id: Number(itemId),
          count: safeNumber(count),
          name: item?.name || `Relic #${itemId}`,
          img: item?.img || "",
          cost: item?.cost || 0,
        };
      })
      .sort((a, b) => b.count - a.count)
      .slice(0, 6);
    return { key, label, entries };
  });
}

export function getSpecialists(players) {
  return [...(players || [])]
    .map((player, index) => {
      const games = safeNumber(player.games_played);
      const wins = safeNumber(player.wins);
      return { label: `Adept ${String(index + 1).padStart(2, "0")}`, games, wins, winRate: games ? wins / games : 0 };
    })
    .filter((player) => player.games > 0)
    .sort((a, b) => b.games - a.games)
    .slice(0, 10);
}

export function getBattleReport(match, heroMap) {
  if (!match || !Array.isArray(match.players)) return null;
  const players = match.players.map((player) => {
    const hero = heroMap.get(Number(player.hero_id));
    return {
      slot: safeNumber(player.player_slot),
      isRadiant: Boolean(player.isRadiant),
      name: player.personaname || player.name || hero?.localized_name || "Unknown combatant",
      hero,
      kills: safeNumber(player.kills),
      deaths: safeNumber(player.deaths),
      assists: safeNumber(player.assists),
      netWorth: safeNumber(player.net_worth),
      damage: safeNumber(player.hero_damage),
      gpm: safeNumber(player.gold_per_min),
      xpm: safeNumber(player.xp_per_min),
      kda: (safeNumber(player.kills) + safeNumber(player.assists)) / Math.max(1, safeNumber(player.deaths)),
    };
  });

  const leaders = {
    damage: [...players].sort((a, b) => b.damage - a.damage)[0],
    netWorth: [...players].sort((a, b) => b.netWorth - a.netWorth)[0],
    kda: [...players].sort((a, b) => b.kda - a.kda)[0],
  };

  return {
    matchId: match.match_id,
    radiantName: match.radiant_name || "Radiant",
    direName: match.dire_name || "Dire",
    radiantWin: Boolean(match.radiant_win),
    radiantScore: safeNumber(match.radiant_score),
    direScore: safeNumber(match.dire_score),
    duration: safeNumber(match.duration),
    league: match.league?.name || match.league_name || "Unknown league",
    patch: match.patch,
    teamfights: Array.isArray(match.teamfights) ? match.teamfights.length : 0,
    objectiveCount: Array.isArray(match.objectives) ? match.objectives.length : 0,
    objectives: Array.isArray(match.objectives) ? match.objectives.slice(0, 8) : [],
    picksBans: Array.isArray(match.picks_bans) ? match.picks_bans : [],
    players,
    leaders,
  };
}

export function heroImage(hero, variant = "img") {
  const path = variant === "icon" ? hero?.icon : hero?.img;
  const prefix = variant === "icon"
    ? "/apps/dota2/images/dota_react/heroes/icons/"
    : "/apps/dota2/images/dota_react/heroes/";
  if (variant !== "icon" && typeof path === "string" && path.startsWith("/apps/dota2/images/dota_react/heroes/icons/")) {
    return "";
  }
  return dotaAsset(path, [prefix]);
}

export function formatNumber(value) {
  return new Intl.NumberFormat(undefined, { maximumFractionDigits: 0 }).format(safeNumber(value));
}

export function formatCompact(value) {
  return new Intl.NumberFormat(undefined, { notation: "compact", maximumFractionDigits: 1 }).format(safeNumber(value));
}

export function formatPercent(value) {
  return new Intl.NumberFormat(undefined, { style: "percent", maximumFractionDigits: 1 }).format(safeNumber(value));
}

export function formatDuration(seconds) {
  const safe = safeNumber(seconds);
  if (!safe) return "unknown";
  const minutes = Math.floor(safe / 60);
  const remaining = String(safe % 60).padStart(2, "0");
  return `${minutes}:${remaining}`;
}

export function formatDate(timestamp) {
  const safe = safeNumber(timestamp);
  if (!safe) return "Unknown time";
  return new Intl.DateTimeFormat(undefined, { month: "short", day: "numeric", hour: "numeric", minute: "2-digit" }).format(new Date(safe * 1000));
}

export function rankLabel(rankTier) {
  const tier = safeNumber(rankTier);
  if (!tier) return "unranked fog";
  const medal = Math.floor(tier / 10);
  const star = tier % 10;
  const medals = { 1: "Herald", 2: "Guardian", 3: "Crusader", 4: "Archon", 5: "Legend", 6: "Ancient", 7: "Divine", 8: "Immortal" };
  return `${medals[medal] || "Unknown"} ${star || ""}`.trim();
}

export function attrLabel(attr) {
  return { agi: "Agility", int: "Intelligence", str: "Strength", all: "Universal" }[attr] || attr || "Unknown";
}

export function safeNumber(value) {
  const number = Number(value);
  return Number.isFinite(number) ? number : 0;
}

function sortHeroes(a, b, sortMode) {
  const sorters = {
    meta: () => b.meta.metaScore - a.meta.metaScore,
    winRate: () => b.meta.winRate - a.meta.winRate || b.meta.picks - a.meta.picks,
    picks: () => b.meta.picks - a.meta.picks,
    proHeat: () => b.meta.proHeat - a.meta.proHeat,
  };
  return (sorters[sortMode] || sorters.meta)();
}
