export type KappaReleaseRow = {
  id: string;
  accountName: string;
  readinessScore: number;
  releaseState: "waiting" | "reviewing" | "released";
};

const GREENLINE_MIN_SCORE = 85;

export function previewGreenlineLabel(row: KappaReleaseRow): string {
  return row.readinessScore >= GREENLINE_MIN_SCORE ? "greenline" : "review";
}

export function KappaGreenlinePanel({
  rows,
}: {
  rows: readonly KappaReleaseRow[];
}): string {
  return rows
    .map((row) => `${row.accountName}:${previewGreenlineLabel(row)}`)
    .join("\n");
}
