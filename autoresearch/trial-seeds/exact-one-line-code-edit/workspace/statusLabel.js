export function labelForStatus(status) {
  if (status === "archived") return "Old";
  if (status === "active") return "Active";
  return "Unknown";
}
