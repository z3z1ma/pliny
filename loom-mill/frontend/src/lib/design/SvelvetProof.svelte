<script lang="ts">
  import { Svelvet, Node, Controls, Minimap, Anchor } from 'svelvet';

  // Custom node content using Svelte 5 runes
  let counter = $state(0);
  let nodeLabel = $state('Custom Svelte 5 Node');

  function increment() {
    counter++;
  }
</script>

<div class="w-full h-full bg-bg-primary relative">
  <div class="absolute top-4 left-4 z-10 bg-bg-surface border border-border-default rounded px-3 py-2 text-[12px] text-text-primary">
    <strong>Svelvet + Svelte 5 Proof</strong>
    <p class="text-text-tertiary mt-1">If you see nodes with edges below, it works.</p>
  </div>

  <Svelvet width={800} height={600} minimap controls theme="dark">
    <!-- Node 1: Custom Svelte 5 content with runes -->
    <Node id="node-1" position={{ x: 100, y: 100 }} let:selected>
      <div class="bg-[#1a1a2e] border rounded-lg p-4 min-w-[200px] text-white {selected ? 'border-blue-400 ring-2 ring-blue-400/30' : 'border-blue-500/50'}">
        <div class="text-[13px] font-semibold mb-2">{nodeLabel}</div>
        <div class="text-[12px] text-gray-400 mb-2">Counter: {counter}</div>
        <button
          onclick={increment}
          class="px-3 py-1 text-[11px] bg-blue-500/20 border border-blue-500/40 rounded hover:bg-blue-500/30 text-blue-300"
        >
          Click me (+1)
        </button>
      </div>
      <div class="anchor output" slot="anchorSouth">
        <Anchor output connections={[["node-2", "input-1"]]} />
      </div>
    </Node>

    <!-- Node 2: Observation-style node -->
    <Node id="node-2" position={{ x: 400, y: 100 }}>
      <div class="bg-[#1a1a2e] border border-green-500/50 rounded-lg p-4 min-w-[180px] text-white">
        <div class="text-[13px] font-semibold text-green-400">Observation Node</div>
        <div class="text-[12px] text-gray-300 mt-1">Found existing graph implementation using d3-force.</div>
      </div>
      <div class="anchor input" slot="anchorNorth">
        <Anchor id="input-1" input />
      </div>
      <div class="anchor output" slot="anchorSouth">
        <Anchor output connections={[["node-3", "input-2"]]} />
      </div>
    </Node>

    <!-- Node 3: Question-style node with interactive buttons -->
    <Node id="node-3" position={{ x: 250, y: 320 }}>
      <div class="bg-[#1a1a2e] border border-purple-500/50 rounded-lg p-4 min-w-[220px] text-white">
        <div class="text-[13px] font-semibold text-purple-400 mb-2">Question</div>
        <div class="text-[12px] text-gray-300 mb-3">Which layout algorithm?</div>
        <div class="flex gap-2">
          <button class="px-2 py-1 text-[10px] border border-gray-600 rounded hover:border-purple-400 text-gray-300 hover:text-purple-300">
            Force-directed
          </button>
          <button class="px-2 py-1 text-[10px] border border-gray-600 rounded hover:border-purple-400 text-gray-300 hover:text-purple-300">
            DAG
          </button>
        </div>
      </div>
      <div class="anchor input" slot="anchorNorth">
        <Anchor id="input-2" input />
      </div>
    </Node>
  </Svelvet>
</div>
