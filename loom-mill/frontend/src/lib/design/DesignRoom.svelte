<script lang="ts">
</script>

<div class="flex h-full w-full overflow-hidden">
  <!-- Left: Graph sidebar -->
  <div class="w-60 shrink-0 border-r border-border-default overflow-y-auto bg-bg-surface">
    <div class="p-4 text-[11px] text-text-tertiary">
      <p class="font-medium text-text-secondary mb-2">Records</p>
      <p>Graph sidebar will render here.</p>
    </div>
  </div>
  
  <!-- Center: Document editor -->
  <div class="flex-1 min-w-0 flex flex-col">
    <div class="flex items-center h-8 px-4 border-b border-border-default bg-bg-surface text-[11px] text-text-tertiary">
      No document open
    </div>
    <div class="flex-1 flex items-center justify-center text-[12px] text-text-tertiary">
      <p>Select a record from the graph to open it here.</p>
    </div>
  </div>
  
  <!-- Right: Chat panel -->
  <div class="w-[360px] shrink-0 border-l border-border-default flex flex-col bg-bg-surface">
    <div class="flex items-center h-8 px-4 border-b border-border-default text-[11px] font-medium text-text-secondary">
      Chat
    </div>
    <div class="flex-1 flex items-center justify-center text-[12px] text-text-tertiary p-4">
      <p>Chat panel will connect to your AI harness for shaping work.</p>
    </div>
  </div>
</div>
