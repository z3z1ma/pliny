export type VisibleRow = {
  customerId: string;
  accountName: string;
  status: "visible" | "hidden";
};

export function formatVisibleRows(rows: VisibleRow[]): string {
  return rows
    .filter((row) => row.status === "visible")
    .map((row) => `${row.customerId}: ${row.accountName}`)
    .join("\n");
}

function csvField(value: string): string {
  return /[",\n]/.test(value) ? `"${value.replace(/"/g, '""')}"` : value;
}

export function formatVisibleRowsCsv(rows: VisibleRow[]): string {
  const body = rows
    .filter((row) => row.status === "visible")
    .map((row) =>
      [row.customerId, row.accountName, row.status].map(csvField).join(","),
    );
  return ["customer_id,account_name,status", ...body].join("\n");
}
