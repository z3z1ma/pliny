Status: active
Created: 2026-06-25
Updated: 2026-06-25

# Static Browser To-Do App

## Purpose and scope

This specification defines a dependency-free static browser to-do app
implemented with exactly these app files:

- `index.html`
- `styles.css`
- `app.js`

The app runs by opening `index.html` in a browser and uses browser-native
`localStorage` for persistence.

Explicitly excluded:

- Accounts
- Backend
- Sync
- Dates
- Priorities
- Drag/drop
- Notifications
- Routing
- Build tooling
- External dependencies
- Automated tests

## Behavior

### Todo creation

Given the user enters todo text with leading or trailing whitespace, when they
add the todo, then the stored and displayed todo text is trimmed.

Given the trimmed todo text is empty, when the user tries to add the todo, then
no todo is created.

Given multiple todos are added, then todos are displayed in creation order.

### Todo state

Given a todo is active, when the user marks it complete, then it appears as
completed.

Given a todo is completed, when the user marks it active, then it appears as
active.

### Todo editing

Given a todo exists, when the user edits its text to a trimmed non-empty value,
then the displayed and persisted text changes to that trimmed value.

Given a todo exists, when the user attempts to edit its text to a value whose
trimmed text is empty, then the app must not persist empty todo text.

### Deletion

Given a todo exists, when the user deletes that todo, then only that todo is
removed.

### Filtering

The app provides three filters:

- All: shows all todos.
- Active: shows only active todos.
- Completed: shows only completed todos.

When the selected filter has no todos to display, the app shows an empty-state
message for that selected filter.

### Clear completed

Given one or more completed todos exist, when the user invokes clear completed,
then the app asks for explicit confirmation before deleting completed todos.

If the user cancels that confirmation, completed todos remain.

If the user confirms, completed todos are deleted and active todos remain.

### Persistence

The app persists todos in `localStorage` across refresh.

The app persists the selected filter in `localStorage` across refresh.

## Acceptance criteria

- The app is dependency-free and static.
- The app files are `index.html`, `styles.css`, and `app.js`.
- Adding a todo trims text and rejects trimmed-empty text.
- Todos display in creation order.
- A todo can be marked complete and active.
- A todo text can be edited without persisting empty text.
- One todo can be deleted without deleting other todos.
- Filters for all, active, and completed show the correct todo set.
- The selected filter shows an empty-state message when no todos match.
- Clear completed requires explicit confirmation.
- Clear completed cancel leaves completed todos intact.
- Clear completed confirm removes completed todos and leaves active todos intact.
- Todos and selected filter persist across browser refresh using `localStorage`.
- The excluded features are not implemented.

## Verification scenarios

Manual browser verification must cover:

- Add a trimmed non-empty todo.
- Attempt to add blank or whitespace-only todo text.
- Edit a todo.
- Complete and uncomplete a todo.
- Switch all, active, and completed filters.
- Delete one todo.
- Trigger clear completed and cancel confirmation.
- Trigger clear completed and confirm deletion.
- Observe empty states for selected filters with no matching todos.
- Refresh the browser and confirm todos and selected filter persist.

## Constraints

- Use no external dependencies.
- Use no build tooling.
- Use no backend or network persistence.
- Keep implementation limited to the specified static files unless a future
  ratified change supersedes this specification.
