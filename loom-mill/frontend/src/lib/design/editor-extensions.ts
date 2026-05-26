import { ViewPlugin, Decoration, DecorationSet, EditorView, WidgetType, hoverTooltip } from '@codemirror/view';
import { RangeSetBuilder } from '@codemirror/state';
import { autocompletion, CompletionContext } from '@codemirror/autocomplete';
import type { LoomRecord } from '../types';

// Regex to match record references
const RECORD_REF_RE = /\b(ticket|spec|plan|research|knowledge|evidence|audit|constitution):[a-zA-Z0-9_-]+\b/g;

// Create a ViewPlugin that decorates record references
export function recordLinks(onNavigate: (id: string) => void) {
  return ViewPlugin.fromClass(class {
    decorations: DecorationSet;
    
    constructor(view: EditorView) {
      this.decorations = this.buildDecorations(view);
    }
    
    update(update: any) {
      if (update.docChanged || update.viewportChanged) {
        this.decorations = this.buildDecorations(update.view);
      }
    }
    
    buildDecorations(view: EditorView) {
      const builder = new RangeSetBuilder<Decoration>();
      for (const { from, to } of view.visibleRanges) {
        const text = view.state.doc.sliceString(from, to);
        let match;
        RECORD_REF_RE.lastIndex = 0;
        while ((match = RECORD_REF_RE.exec(text)) !== null) {
          const start = from + match.index;
          const end = start + match[0].length;
          builder.add(start, end, Decoration.mark({
            class: 'cm-loom-ref',
            attributes: { 'data-ref': match[0] }
          }));
        }
      }
      return builder.finish();
    }
  }, { decorations: v => v.decorations });
}

export const recordLinksClick = (onNavigate: (id: string) => void) => {
  return EditorView.domEventHandlers({
    click(event, view) {
      if (event.metaKey || event.ctrlKey) {
        const pos = view.posAtCoords({ x: event.clientX, y: event.clientY });
        if (pos !== null) {
          const line = view.state.doc.lineAt(pos);
          const text = line.text;
          RECORD_REF_RE.lastIndex = 0;
          let match;
          while ((match = RECORD_REF_RE.exec(text)) !== null) {
            const start = line.from + match.index;
            const end = start + match[0].length;
            if (pos >= start && pos <= end) {
              onNavigate(match[0]);
              event.preventDefault();
              return true;
            }
          }
        }
      }
      return false;
    }
  });
};

export function recordHoverPreview(records: () => LoomRecord[]) {
  return hoverTooltip((view, pos, side) => {
    const { from, to, text } = view.state.doc.lineAt(pos);
    let start = pos, end = pos;
    while (start > from && /[a-zA-Z0-9_:-]/.test(text[start - from - 1])) start--;
    while (end < to && /[a-zA-Z0-9_:-]/.test(text[end - from])) end++;
    if (start == pos && side < 0 || start == end) return null;
    
    const word = text.slice(start - from, end - from);
    RECORD_REF_RE.lastIndex = 0;
    if (!RECORD_REF_RE.test(word)) return null;
    RECORD_REF_RE.lastIndex = 0;
    
    const record = records().find(r => r.metadata.id === word || r.path === word);
    if (!record) return null;
    
    return {
      pos: start,
      end,
      above: true,
      create(view) {
        const dom = document.createElement("div");
        dom.className = "p-2 bg-bg-surface border border-border-default rounded shadow-lg text-[11px] max-w-xs z-50";
        
        const header = document.createElement("div");
        header.className = "flex items-center gap-2 mb-1";
        
        const status = document.createElement("span");
        status.className = "w-2 h-2 rounded-full shrink-0 " + (record.metadata.status === 'open' ? 'bg-status-success-text' : 'bg-status-neutral-text');
        
        const title = document.createElement("span");
        title.className = "font-medium text-text-primary truncate";
        title.textContent = record.headings[0]?.[1] || record.metadata.id || record.path;
        
        header.appendChild(status);
        header.appendChild(title);
        dom.appendChild(header);
        
        const type = document.createElement("div");
        type.className = "text-text-tertiary";
        type.textContent = record.metadata.type || word.split(':')[0];
        dom.appendChild(type);
        
        return { dom };
      }
    };
  });
}

export function loomAutocompletion(records: () => LoomRecord[]) {
  return autocompletion({
    override: [
      (context: CompletionContext) => {
        const word = context.matchBefore(/\b(ticket|spec|plan|research|knowledge|evidence|audit|constitution):[a-zA-Z0-9_-]*/);
        if (!word) return null;
        
        const prefix = word.text;
        const [surface] = prefix.split(':');
        const afterColon = prefix.split(':')[1] || '';
        
        const options = records()
          .filter(r => r.metadata.id?.startsWith(prefix) || r.metadata.id?.includes(afterColon))
          .map(r => ({
            label: r.metadata.id || r.path,
            detail: r.headings[0]?.[1] || '',
            type: 'variable',
          }));
        
        return { 
          from: word.from, 
          options,
          validFor: /^(ticket|spec|plan|research|knowledge|evidence|audit|constitution):[a-zA-Z0-9_-]*$/
        };
      },
      (context: CompletionContext) => {
        const word = context.matchBefore(/(ACC-|REQ-)\d*/);
        if (!word) return null;
        
        // Only trigger if we're at the start of a line or after a space
        const textBefore = context.state.doc.sliceString(Math.max(0, word.from - 1), word.from);
        if (textBefore && !/\s/.test(textBefore)) return null;
        
        const prefix = word.text.substring(0, 4); // "ACC-" or "REQ-"
        
        // Find all existing numbers in the document
        const doc = context.state.doc.toString();
        const regex = new RegExp(`${prefix}(\\d+)`, 'g');
        let maxNum = 0;
        let match;
        while ((match = regex.exec(doc)) !== null) {
          const num = parseInt(match[1], 10);
          if (num > maxNum) maxNum = num;
        }
        
        const nextNum = String(maxNum + 1).padStart(3, '0');
        const nextId = `${prefix}${nextNum}`;
        
        return {
          from: word.from,
          options: [
            { label: nextId, type: 'text' }
          ],
          validFor: /^(ACC-|REQ-)\d*$/
        };
      }
    ]
  });
}
