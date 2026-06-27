export type LedgerImportRow = {
  sourceRef: string;
  amountCents: number;
  postedAt: string;
};

export function previewLedgerImport(rows: LedgerImportRow[]): string[] {
  return rows.map((row) => `${row.sourceRef}:${row.amountCents}:${row.postedAt}`);
}
