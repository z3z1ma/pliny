<script lang="ts">
  import { Node, Anchor } from 'svelvet';

  let { node, position, connections = [] } = $props();
</script>

<Node id={node.id} {position} let:selected>
  <div class="bg-bg-surface border border-accent-primary/50 rounded-lg p-2 min-w-[150px] shadow-sm animate-pulse flex items-center gap-2
    {selected ? 'ring-2 ring-accent-primary/50' : ''}
  ">
    <div class="w-2 h-2 rounded-full bg-accent-primary animate-ping"></div>
    <div class="text-[12px] text-text-secondary italic">
      {node.content.message || 'Processing...'}
    </div>
  </div>

  <div slot="anchorNorth">
    <Anchor id="{node.id}-in" input />
  </div>

  <div slot="anchorSouth">
    <Anchor id="{node.id}-out" output {connections} />
  </div>
</Node>
