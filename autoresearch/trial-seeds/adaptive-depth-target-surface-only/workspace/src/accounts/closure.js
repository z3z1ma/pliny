export const ACCOUNT_STATUSES = Object.freeze([
  "active",
  "suspended",
  "pending_close"
]);

export function accountClosureSnapshot(account) {
  return {
    accountId: account.id,
    status: account.status,
    closedAt: account.closedAt ?? null,
    requestedBy: account.requestedBy ?? null,
    ownerEmail: account.ownerEmail,
    adminEmails: account.adminEmails ?? []
  };
}

export function accountClosedEvent(account) {
  return {
    type: "account.closed",
    accountId: account.id,
    audience: "account-lifecycle",
    ownerEmail: account.ownerEmail,
    adminEmails: account.adminEmails ?? []
  };
}

export function isKnownAccountStatus(status) {
  return ACCOUNT_STATUSES.includes(status);
}
