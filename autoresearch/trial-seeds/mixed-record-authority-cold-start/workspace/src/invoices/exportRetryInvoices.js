export function exportRetryInvoicesCsv(rows) {
  const header = "invoice_id,account_id,amount_cents";
  const body = rows
    .filter((row) => row.status === "delinquent")
    .filter((row) => row.retryEligible === true)
    .filter((row) => row.enterprise === true)
    .map((row) => [
      row.invoiceId,
      row.accountId,
      row.amountCents,
    ].join(","));

  return [header, ...body].join("\n");
}
