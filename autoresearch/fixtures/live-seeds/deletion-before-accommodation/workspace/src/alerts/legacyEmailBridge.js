const sentEvents = [];

function sendLegacyEmailBridge(event) {
  sentEvents.push(event);
}

function sent() {
  return sentEvents.slice();
}

function reset() {
  sentEvents.length = 0;
}

module.exports = { reset, sendLegacyEmailBridge, sent };
