import { EditorView } from '@codemirror/view';
import { HighlightStyle, syntaxHighlighting } from '@codemirror/language';
import { tags } from '@lezer/highlight';

export const millTheme = EditorView.theme({
  '&': {
    backgroundColor: 'var(--color-bg-primary)',
    color: 'var(--color-text-primary)',
    fontSize: '13px',
    fontFamily: 'var(--font-mono, ui-monospace, monospace)',
  },
  '.cm-content': { padding: '16px 0' },
  '.cm-gutters': {
    backgroundColor: 'var(--color-bg-surface)',
    color: 'var(--color-text-tertiary)',
    border: 'none',
    borderRight: '1px solid var(--color-border-default)',
  },
  '.cm-activeLine': { backgroundColor: 'var(--color-bg-surface-active)' },
  '.cm-selectionBackground': { 
    backgroundColor: 'rgba(99, 102, 241, 0.25) !important'
  },
  '&.cm-focused .cm-selectionBackground': {
    backgroundColor: 'rgba(99, 102, 241, 0.35) !important'
  },
  '&.cm-focused .cm-cursor': { borderLeftColor: 'var(--color-accent-primary)' },
  '.cm-line': { padding: '0 16px' },
  '.cm-loom-ref': {
    color: 'var(--color-accent-primary)',
    textDecoration: 'underline',
    textDecorationStyle: 'dotted',
    cursor: 'pointer',
    borderRadius: '2px',
    padding: '0 1px',
  },
  '.cm-loom-ref:hover': {
    backgroundColor: 'rgba(99, 102, 241, 0.1)',
    textDecorationStyle: 'solid',
  },
});

export const millHighlighting = syntaxHighlighting(HighlightStyle.define([
  { tag: tags.heading1, fontWeight: '700', fontSize: '1.4em', color: 'var(--color-text-primary)' },
  { tag: tags.heading2, fontWeight: '600', fontSize: '1.2em', color: 'var(--color-text-primary)' },
  { tag: tags.heading3, fontWeight: '600', fontSize: '1.1em', color: 'var(--color-text-primary)' },
  { tag: tags.emphasis, fontStyle: 'italic' },
  { tag: tags.strong, fontWeight: '700' },
  { tag: tags.monospace, fontFamily: 'var(--font-mono)', backgroundColor: 'var(--color-bg-surface-active)', padding: '1px 4px', borderRadius: '3px' },
  { tag: tags.link, color: 'var(--color-accent-primary)', textDecoration: 'underline' },
  { tag: tags.url, color: 'var(--color-text-tertiary)' },
  { tag: tags.quote, color: 'var(--color-text-secondary)', fontStyle: 'italic' },
  { tag: tags.list, color: 'var(--color-text-secondary)' },
]));
