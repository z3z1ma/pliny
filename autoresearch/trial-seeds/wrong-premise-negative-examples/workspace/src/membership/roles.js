export const WORKSPACE_ROLES = Object.freeze([
  "owner",
  "admin",
  "member",
  "viewer"
]);

export function membershipSummary(membership) {
  return {
    workspaceId: membership.workspaceId,
    userId: membership.userId,
    role: membership.role,
    invitedBy: membership.invitedBy,
    joinedAt: membership.joinedAt,
    disabledAt: membership.disabledAt ?? null
  };
}

export function isKnownWorkspaceRole(role) {
  return WORKSPACE_ROLES.includes(role);
}
