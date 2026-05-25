<script lang="ts">
  let activeLane = $state("Scaffold");
  let status = $derived(`${activeLane} ready`);

  $effect(() => {
    document.title = `Loom Mill - ${status}`;
  });
</script>

<main class="min-h-screen bg-slate-950 text-slate-100">
  <section class="mx-auto flex min-h-screen max-w-5xl flex-col justify-center px-6 py-16">
    <p class="mb-3 text-sm font-medium uppercase tracking-[0.4em] text-cyan-300">Factory Floor</p>
    <h1 class="text-5xl font-semibold tracking-tight sm:text-7xl">Loom Mill</h1>
    <p class="mt-6 max-w-2xl text-lg leading-8 text-slate-300">
      Local control-room shell for Loom execution. The scaffold is intentionally empty of business logic.
    </p>
    <div class="mt-10 rounded-2xl border border-slate-800 bg-slate-900/70 p-5 shadow-2xl shadow-cyan-950/30">
      <p class="text-sm text-slate-400">Current lane</p>
      <p class="mt-2 text-2xl font-medium text-cyan-100">{status}</p>
    </div>
  </section>
</main>
