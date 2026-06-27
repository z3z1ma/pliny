export const roles = ["admin", "member", "viewer"];

export function canManageInvites(user) {
  return user?.role === "admin";
}

export function requireInviteAdmin(user) {
  if (!canManageInvites(user)) {
    const error = new Error("invite management requires admin role");
    error.statusCode = 403;
    throw error;
  }
}
