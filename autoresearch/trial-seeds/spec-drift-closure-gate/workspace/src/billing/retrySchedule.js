export const RETRY_OFFSETS_DAYS = [1, 3, 7];

export function shouldScheduleRetry(invoice) {
  return invoice.status === "failed";
}
