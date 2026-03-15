import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

// Phase 1: Pure static output for Hostpoint shared hosting.
// Threshold runs client-side (localStorage). API endpoint disabled.
// Phase 2: Add server adapter when Python/Node backend is available.

export default defineConfig({
  site: 'https://kalam.ch',
  integrations: [sitemap()],
});
