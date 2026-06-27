export function exportNegativeAdjustmentsCsv(rows) {
  const header = "refund_id,account_id,adjustment_cents,reason";
  const body = rows
    .filter((row) => row.adjustmentCents < 0)
    .map((row) => [
      row.refundId,
      row.accountId,
      row.adjustmentCents,
      row.reason,
    ].join(","));

  return [header, ...body].join("\n");
}
