export function enqueueInviteEmail(state, invite, token) {
  state.outbox.push({
    type: "invite",
    inviteId: invite.id,
    to: invite.email,
    token,
    attempts: 0
  });
}

export function markDeliveryAttempt(message, delivered) {
  message.attempts += 1;
  message.delivered = delivered;
  return message;
}
