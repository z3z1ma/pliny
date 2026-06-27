export function statusLabel(status) {
  if (status === "active") return "Active";
  if (status === "archived") return "Archived";
  return "Unknown";
}
