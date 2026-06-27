export function isExportEnabled(rows) {
  return rows.some((row) => row.selected);
}
