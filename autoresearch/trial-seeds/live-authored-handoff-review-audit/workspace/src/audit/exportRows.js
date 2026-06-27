export function auditExportContext(account) {
  return {
    accountId: account.accountId,
    createdAt: account.createdAt,
    status: account.status,
    balanceCents: account.balanceCents,
    email: account.email,
    closedAt: account.closedAt
  };
}

export function classifyAuditExportReadiness() {
  return { status: "policy_required", reason: "audit_export_policy_unratified" };
}
