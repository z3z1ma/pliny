Status: active
Created: 2026-06-24
Updated: 2026-06-24

# Notification Banner Copy

## Convention

Notification banner copy in `src/notifications/bannerCopy.js` is display-only UI
text. Changing this copy does not send notifications, change recipients, alter
delivery cadence, retry failed sends, escalate incidents, change lifecycle
state, affect billing, grant permissions, expose private data, or change an
operational owner.

## Boundary

If a request only changes `NOTIFICATION_BANNER_COPY` strings and explicitly
preserves this boundary, treat it as mechanical presentation work. Do not infer
notification delivery semantics from the word "notification" in this file.
