const ACCOUNT_EXPORT_COLUMNS = ["accountId", "status", "balanceCents"];

function buildAccountExportRows(accounts) {
  return accounts
    .filter((account) => account.isVisible && !account.isTest)
    .map((account) => ({
      accountId: account.accountId,
      status: account.status,
      balanceCents: account.balanceCents,
    }));
}

module.exports = {
  ACCOUNT_EXPORT_COLUMNS,
  buildAccountExportRows,
};
