Status: active
Created: 2026-06-24
Updated: 2026-06-24

# Icon Action Button Accessibility

## Purpose And Scope

Define the baseline accessibility contract for reusable icon-only action
buttons.

In scope:

- `src/components/IconActionButton.tsx`
- Native button semantics or an explicitly equivalent accessible replacement.
- Accessible name for icon-only controls.
- Keyboard activation and focus behavior.

Out of scope:

- Visual redesign.
- Tooltip implementation.
- Icon library changes.
- Analytics events.

## Behavior

Given an icon-only action, when it renders, then assistive technology can
identify the control by its accessible label.

Given keyboard users focus the action, when they press Enter or Space, then the
action activates.

## Acceptance Criteria

- The component exposes an accessible name from its `label` prop.
- The component remains a native `<button>` or provides an explicitly equivalent
  role, tab stop, keyboard activation, and disabled-state behavior.
- Simplification must not remove accessible name, focusability, or keyboard
  activation.

## Constraints

- Do not replace a native button with a non-semantic clickable element unless
  equivalent accessibility behavior is implemented and verified.
- Do not rely on visual icon shape or tooltip text as the only accessible name.
