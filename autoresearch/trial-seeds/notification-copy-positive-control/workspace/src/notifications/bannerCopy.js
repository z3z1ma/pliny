export const NOTIFICATION_BANNER_COPY = Object.freeze({
  accountClosed: {
    title: "Account closed",
    body: "The account is no longer active."
  },
  exportQueued: {
    title: "Export queued",
    body: "We will let you know when it is ready."
  }
});

export function notificationBannerCopy(key) {
  return NOTIFICATION_BANNER_COPY[key] ?? null;
}
