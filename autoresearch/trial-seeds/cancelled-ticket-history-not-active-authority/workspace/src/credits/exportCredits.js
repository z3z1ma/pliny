export function exportCreditsCsv(rows) {
  const header = "customer_id,credit_cents,reason";
  const body = rows
    .filter((row) => row.status === "approved")
    .filter((row) => row.region === "us")
    .filter((row) => row.enterprise === true)
    .map((row) => [
      row.customerId,
      row.creditCents,
      row.reason,
    ].join(","));

  return [header, ...body].join("\n");
}
