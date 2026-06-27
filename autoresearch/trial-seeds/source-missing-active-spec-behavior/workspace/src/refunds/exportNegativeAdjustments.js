export function exportNegativeAdjustmentsCsv(rows) {
  const lines = ["refund_id,account_id,adjustment_cents,reason"];
  for (const row of rows) {
    if (row.adjustmentCents < 0) {
      lines.push(
        `${row.refundId},${row.accountId},${row.adjustmentCents},${row.reason}`,
      );
    }
  }
  return lines.join("\n");
}
