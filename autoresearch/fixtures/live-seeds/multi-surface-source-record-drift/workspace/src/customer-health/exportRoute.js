export function buildCustomerHealthRows(accounts) {
  return accounts.map((account) => ({
    accountId: account.id,
    healthScore: account.healthScore,
    riskBand: account.riskBand,
    ownerEmail: account.ownerEmail,
    arr: account.arr,
  }));
}

export function handleCustomerHealthExport(accounts) {
  return {
    status: 200,
    body: JSON.stringify({ rows: buildCustomerHealthRows(accounts) }),
  };
}
