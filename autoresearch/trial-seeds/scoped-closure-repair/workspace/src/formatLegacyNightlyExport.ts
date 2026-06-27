export type LegacyExportRow = {
  customerId: string;
  accountName: string;
  status: "visible" | "hidden";
};

export function formatLegacyNightlyExport(rows: LegacyExportRow[]): string {
  const body = rows.map((row) =>
    [row.customerId, row.accountName, row.status].join(","),
  );
  return ["customer_id,account_name,status", ...body].join("\n");
}
