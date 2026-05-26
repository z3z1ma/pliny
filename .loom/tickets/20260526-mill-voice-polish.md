# Design Room: Voice Input + Final Polish

ID: ticket:20260526-mill-voice-polish
Type: Ticket
Status: closed
Created: 2026-05-26
Updated: 2026-05-26
Risk: low - Web Speech API is browser-native; polish is incremental

Priority: medium - final layer after all panels work
Depends On: ticket:20260526-mill-editor-chat-link

## Summary

Add voice input via Web Speech API and apply final polish to the Design Room:
smooth panel transitions, responsive behavior, and refined animations. Voice lets
the operator think aloud - stream of consciousness that becomes structured through
the AI. Polish makes the Design Room feel native and responsive.

Single closure claim: Voice input works via browser speech recognition. All Design
Room panels have smooth transitions. The layout is responsive from 768px-2560px.

## Related Records

- `spec:mill-design-room` - REQ-014
- `plan:20260526-mill-design-room` - parent plan
- `ticket:20260526-mill-chat-panel` - chat panel where voice input lands

## Scope

### Must Create/Change

- `loom-mill/frontend/src/lib/design/ChatInput.svelte` - Add voice button behavior:
  - Microphone button (already in UI from Unit 5, needs behavior wired)
  - On click: start `SpeechRecognition` (or `webkitSpeechRecognition`)
  - While recording: mic icon pulses red, transcription appears in input textarea live
  - On stop (click again, or silence detected): finalize transcription in input
  - Text remains in input for editing before sending (not auto-sent)
  - Handle browser permission prompt gracefully
  - Show "Voice not supported" in browsers without SpeechRecognition API

- `loom-mill/frontend/src/lib/design/VoiceIndicator.svelte` - Visual feedback:
  - Pulsing ring around mic button while recording
  - Small waveform animation (CSS-only, no canvas needed)
  - "Listening..." text below input while active

- `loom-mill/frontend/src/lib/design/DesignRoom.svelte` - Panel transitions:
  - Panel collapse/expand: slide animation (200ms ease-out)
  - Panel resize: smooth CSS transition
  - Mode switch: crossfade between Design Room and Factory Floor (150ms)

- `loom-mill/frontend/src/lib/design/GraphSidebar.svelte` - Transitions:
  - Record list items: fade-in on mount
  - Status dot color changes: transition color (200ms)
  - Section collapse: height animation

- `loom-mill/frontend/src/lib/design/DocumentEditor.svelte` - Transitions:
  - Document switch: brief fade (100ms) between documents
  - Save indicator: brief flash of success color

- `loom-mill/frontend/src/lib/design/ChatPanel.svelte` - Transitions:
  - New messages: slide in from bottom (150ms)
  - Streaming text: smooth appearance (no jumps)

- Responsive behavior for Design Room:
  - `≥1280px`: three panels visible (240 + flex + 360)
  - `1024-1279px`: graph collapsed by default, editor + chat visible
  - `768-1023px`: single panel visible with panel switcher tabs
  - `<768px`: not supported for Design Room (show "Desktop recommended" message)

### Web Speech API Integration

```typescript
let recognition: SpeechRecognition | null = null;
let isRecording = $state(false);

function startVoice() {
  if (!('SpeechRecognition' in window || 'webkitSpeechRecognition' in window)) {
    // Show "not supported" message
    return;
  }
  const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
  recognition = new SR();
  recognition.continuous = true;
  recognition.interimResults = true;
  recognition.lang = 'en-US';
  
  recognition.onresult = (event) => {
    let transcript = '';
    for (let i = event.resultIndex; i < event.results.length; i++) {
      transcript += event.results[i][0].transcript;
    }
    // Update input textarea with transcript
    inputText = existingText + transcript;
  };
  
  recognition.onend = () => { isRecording = false; };
  recognition.start();
  isRecording = true;
}

function stopVoice() {
  recognition?.stop();
  isRecording = false;
}
```

### Must Not Change

- Backend
- Factory Floor
- Core panel functionality (only add transitions and voice)

### Non-Goals

- Custom wake word
- Continuous hands-free mode
- Voice commands (only transcription into chat input)
- External speech-to-text services (Whisper, etc.)
- Mobile layout for Design Room

## Acceptance

- ACC-001: Clicking microphone button activates speech recognition; transcription appears in input
  - Evidence: Manual test with microphone: speak → text appears in input field
  - Audit: Verify text is editable before sending

- ACC-002: Clicking microphone again (or silence) stops recording; text remains in input
  - Evidence: Manual test: record → stop → text stays, can edit, can send
  - Audit: Verify no auto-send behavior

- ACC-003: Visual feedback during recording (pulsing indicator)
  - Evidence: Playwright screenshot showing active recording state
  - Audit: Verify animation runs smoothly

- ACC-004: Panel collapse/expand animations are smooth (200ms, no jumps)
  - Evidence: Playwright visual inspection of panel transitions
  - Audit: Verify CSS transition properties

- ACC-005: Mode switch (Design Room ↔ Factory Floor) has crossfade transition
  - Evidence: Visual inspection of switch animation
  - Audit: Verify no content flash

- ACC-006: Design Room is usable at 1024px (editor + chat, graph collapsed)
  - Evidence: Playwright screenshot at 1024px
  - Audit: Verify all interactions work at this width

- ACC-007: Browser without SpeechRecognition shows "not supported" gracefully
  - Evidence: Test in a context where API is unavailable
  - Audit: Verify no crash, just informative message

## Current State

Ready to start after editor-chat link (Unit 6) lands. This is the final polish
layer.

## Journal

- 2026-05-26: Created ticket with Status `open`. Voice + polish is the final
  layer that makes the Design Room feel native. Web Speech API is free and
  immediate - no external dependencies.
