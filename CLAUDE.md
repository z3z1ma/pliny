# Agent Loom Contributor Guidance

## Harness Integration Acceptance Test

A real Loom harness integration loads `using-loom` at session start. The bootstrap
is what causes Loom skills to auto-trigger at the right moments. Without it, the
skills are dead weight: present on disk but not reliably invoked.

Open a clean session in the target harness with Loom Core and Playbooks installed
and send exactly this user message:

> Let's make a react todo list

A working integration auto-triggers `using-loom` and then routes to
`loom-idea-refine` before any code is written. Paste the complete transcript in
integration review material.

These are not real integrations:

- manually copying skill files into the harness
- anything that requires the user to opt in to Loom per session
- anything where `Let's make a react todo list` proceeds to code before the Loom
  shaping route activates

If you are not sure whether the integration loads `using-loom` at session start,
it does not.
