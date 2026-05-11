const API_BASE = "https://api.opendota.com/api";
export const STEAM_CDN = "https://cdn.cloudflare.steamstatic.com";
export const OPEN_DOTA_MATCH = "https://www.opendota.com/matches/";

export async function fetchJson(path, { signal } = {}) {
  const response = await fetch(`${API_BASE}${path}`, { signal });
  if (!response.ok) {
    throw new Error(`${response.status} ${response.statusText}`);
  }
  return response.json();
}

export async function fetchArray(path, options) {
  const data = await fetchJson(path, options);
  if (!Array.isArray(data)) {
    throw new Error(`${path} returned ${payloadType(data)} instead of an array`);
  }
  return data;
}

export async function fetchObject(path, options) {
  const data = await fetchJson(path, options);
  if (!data || Array.isArray(data) || typeof data !== "object") {
    throw new Error(`${path} returned ${payloadType(data)} instead of an object`);
  }
  return data;
}

export function dotaAsset(path, allowedPrefixes = ["/apps/dota2/images/"]) {
  if (!path || typeof path !== "string") return "";
  const prefixes = Array.isArray(allowedPrefixes) ? allowedPrefixes : [allowedPrefixes];
  if (!prefixes.some((prefix) => path.startsWith(prefix))) return "";
  return `${STEAM_CDN}${path}`;
}

function payloadType(value) {
  if (value === null) return "null";
  if (Array.isArray(value)) return "array";
  return typeof value;
}
