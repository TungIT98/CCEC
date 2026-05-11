import { defineConfig } from 'astro/config';
import svelte from '@astrojs/svelte';

export default defineConfig({
  integrations: [
    svelte(),
  ],
  output: 'static',
  vite: {
    envPrefix: 'PUBLIC_',
    optimizeDeps: {
      exclude: ['leaflet'],
      include: ['leaflet'],
    },
  },
});