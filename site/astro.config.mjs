import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import cloudflare from '@astrojs/cloudflare';

// Phase 2: Static pages + server API routes via Cloudflare adapter.
// Astro 5 uses output: 'static' by default. Server routes (like /api/threshold)
// opt out of prerendering with export const prerender = false in the file.

export default defineConfig({
  adapter: cloudflare({
    platformProxy: { enabled: true },
  }),
  site: 'https://kalam.ch',
  integrations: [sitemap()],
});
