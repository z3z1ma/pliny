export function reportExportUrl(filters) {
  const params = new URLSearchParams(filters);
  return `/api/reports/export.csv?${params.toString()}`;
}

export function reportViewUrl(filters) {
  const params = new URLSearchParams(filters);
  return `/reports?${params.toString()}`;
}
