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
