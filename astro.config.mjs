// @ts-check
import { defineConfig } from 'astro/config';

// https://astro.build/config
export default defineConfig({
  vite: {
    // <model-viewer> bundles three.js (~1 MB); it's only loaded on building pages.
    build: { chunkSizeWarningLimit: 1500 },
  },
});
