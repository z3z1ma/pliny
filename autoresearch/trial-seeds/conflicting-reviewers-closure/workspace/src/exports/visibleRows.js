export function exportVisibleRows(rows) {
  const exported = rows
    .filter((row) => row.selected === true)
    .map((row) => `${row.id},${row.label}`);

  return ["row_id,label", ...exported].join("\n");
}
