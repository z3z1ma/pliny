// When served from same origin (production), use relative URLs.
// When VITE_API_URL is set (dev with separate ports), use that.
export const API_BASE = import.meta.env.VITE_API_URL || '';

export function apiUrl(path: string): string {
  // Ensure path starts with /
  const normalizedPath = path.startsWith('/') ? path : `/${path}`;
  return `${API_BASE}${normalizedPath}`;
}

export function wsUrl(path: string): string {
  const base = import.meta.env.VITE_WS_URL || '';
  const normalizedPath = path.startsWith('/') ? path : `/${path}`;
  if (base) return `${base}${normalizedPath}`;
  const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
  return `${protocol}//${window.location.host}${normalizedPath}`;
}
