export function exportVisibleRows(rows) {
  return rows
    .filter((row) => row.selected)
    .map((row) => [row.id, row.name, row.status].map(csvCell).join(","))
    .join("\n");
}

function csvCell(value) {
  const text = String(value ?? "");
  if (/[",\n]/.test(text)) {
    return `"${text.replaceAll('"', '""')}"`;
  }
  return text;
}
