const RETRY_HORIZON_HOURS = 72;

function eventKey(event) {
  return event.dedupeId;
}

function shouldRetry(statusCode) {
  return statusCode < 200 || statusCode >= 300;
}

function shouldDeadLetter(firstAttemptAt, now) {
  const ageMs = now.getTime() - firstAttemptAt.getTime();
  return ageMs >= RETRY_HORIZON_HOURS * 60 * 60 * 1000;
}

module.exports = {
  RETRY_HORIZON_HOURS,
  eventKey,
  shouldDeadLetter,
  shouldRetry,
};
