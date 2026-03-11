import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

// Phase 1: Static output. When ready for AI integration,
// switch to hybrid + cloudflare adapter:
// import cloudflare from '@astrojs/cloudflare';
// output: 'hybrid', adapter: cloudflare()

export default defineConfig({
  output: 'static',
  site: 'https://kalam.ch',
  integrations: [sitemap()],
});
