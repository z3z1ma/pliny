import tailwindcss from "@tailwindcss/vite";
import { svelte } from "@sveltejs/vite-plugin-svelte";
import { defineConfig } from "vite";

export default defineConfig({
  plugins: [svelte(), tailwindcss()],
  build: {
    assetsDir: "assets",
    emptyOutDir: true,
  },
  server: {
    port: 5173,
  },
});
