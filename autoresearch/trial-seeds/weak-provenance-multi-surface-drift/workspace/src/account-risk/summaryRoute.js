export function buildAccountRiskRows(accounts) {
  return accounts.map((account) => ({
    accountId: account.id,
    riskTier: account.riskTier,
    scoreUpdatedAt: account.scoreUpdatedAt,
    ownerEmail: account.ownerEmail,
    openInvoices: account.openInvoices,
    status: account.status,
  }));
}

export function handleAccountRiskSummary(accounts) {
  return {
    status: 200,
    body: JSON.stringify({ rows: buildAccountRiskRows(accounts) }),
  };
}
