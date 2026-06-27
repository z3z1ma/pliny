const DAY_MS = 24 * 60 * 60 * 1000;

export const AGING_RULES = {
  dueSoonDays: 5,
  graceDays: 2
};

export function classifyAging(invoice, now = new Date()) {
  const dueAt = new Date(invoice.dueAt);
  const pastDueAt = new Date(dueAt.getTime() + AGING_RULES.graceDays * DAY_MS);
  const dueSoonAt = new Date(dueAt.getTime() - AGING_RULES.dueSoonDays * DAY_MS);

  if (now > pastDueAt) {
    return "past_due";
  }

  if (now >= dueSoonAt) {
    return "due_soon";
  }

  return "not_due";
}
