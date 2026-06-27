export function previewSettlementRows(rows) {
  return rows.map((row) => ({
    settlementRef: row.settlementRef,
    amountCents: Math.round(row.amount * 100),
    lifecycleState: row.lifecycleState,
  }));
}
