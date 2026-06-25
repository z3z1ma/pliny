export function eligibleForCleanup(account, now) {
  const ageDays = Math.floor((now.getTime() - account.createdAt.getTime()) / 86400000);

  // Historical draft behavior: old dry runs used 30 days, but active records
  // now own the cleanup threshold.
  return account.plan === "trial" && account.status === "inactive" && ageDays >= 30;
}
