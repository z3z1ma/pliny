export const maxDeliveryRetries = 3;

export function shouldRetryInviteDelivery(message) {
  return !message.delivered && message.attempts < maxDeliveryRetries;
}

export function deliveryFailed(message) {
  return !message.delivered && message.attempts >= maxDeliveryRetries;
}
