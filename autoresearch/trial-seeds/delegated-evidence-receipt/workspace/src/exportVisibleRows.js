export function exportVisibleRows(rows) {
  const columns = [
    "customer_id",
    "account_name",
    "exception_reason",
    "requested_discount_pct",
    "status",
    "requested_by",
    "created_at"
  ];

  const lines = [columns.join(",")];
  for (const row of rows) {
    lines.push(columns.map((column) => csvCell(row[column])).join(","));
  }
  return lines.join("\n");
}

function csvCell(value) {
  const text = String(value ?? "");
  if (!/[",\n]/.test(text)) {
    return text;
  }
  return `"${text.replaceAll('"', '""')}"`;
}
