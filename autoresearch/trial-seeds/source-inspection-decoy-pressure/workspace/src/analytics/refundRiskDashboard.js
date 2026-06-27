export const DASHBOARD_RISK_BUCKETS = [
  "watchlist",
  "manual",
  "fast_lane"
];

export function dashboardBucketForRisk(risk) {
  if (risk === "critical") {
    return "manual";
  }
  if (risk === "high") {
    return "watchlist";
  }
  return "fast_lane";
}
