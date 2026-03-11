# KALAM.CH — Technical Stack Decision

Date: 2026-03-11
Decided by: V-002 (research) + V-001 (authority)

## The Stack

**Astro 5 + Cloudflare Pages + Claude Haiku 4.5 (Phase 2)**

## Why This Stack

### Framework: Astro 5
- Starts as pure static HTML — zero JavaScript shipped by default
- Islands architecture: add interactive components (input field) without rebuilding
- Growth path: static → hybrid → full SSR by changing one config line
- Content-first philosophy matches a dignity-first, canon-driven project
- Framework-agnostic islands (Preact, Svelte, or vanilla JS)
- Official Cloudflare adapter (`@astrojs/cloudflare`)

### Hosting: Cloudflare Pages + Workers
- **Swiss data center (Zurich)** — serve Swiss users from Swiss soil
- Free tier: unlimited bandwidth, 500 builds/month, 100K Worker requests/day
- Workers AI: run open-source models on-edge without third-party API calls
- D1 (SQLite at edge): lightweight pattern storage for Phase 2
- R2: append-only log storage with zero egress fees
- All-in-one: CDN + DNS + DDoS + serverless + storage + AI inference
- EU Data Localization Suite available for strict compliance

### AI: Claude Haiku 4.5 (Phase 2)
- ~$3/month at 100 interactions/day
- Streaming via SSE through Cloudflare Worker
- Anthropic API does not train on API inputs by default
- Escalate to Sonnet for complex interactions

### Rejected Alternatives
- **Next.js 15**: Over-engineered. React Server Components add complexity this project doesn't need. Vercel-optimized. Wrong energy for a philosophical foundation.
- **Plain HTML + htmx**: Beautiful simplicity but no growth path. When AI integration arrives, requires bolting on a separate backend.
- **SvelteKit**: Viable but Astro's content-first approach and framework-agnostic islands are a better fit.
- **Vercel**: $20/month Pro tier, no Swiss data center, Astro is second-class citizen.
- **Netlify**: US-centric data processing, weaker streaming support.

## Phase Plan

### Phase 1 (Current): Static Site
- Astro static output
- Deploy to Cloudflare Pages via git integration
- Four pages: Home, About, Canon, Invitation
- Zero JavaScript, zero tracking, zero cookies
- Cost: $0/month

### Phase 2: AI Integration
- Switch to hybrid output with Cloudflare adapter
- Add Preact/Svelte island for the input field (Threshold)
- Cloudflare Worker as AI API proxy with SSE streaming
- Pattern extraction → D1 storage (no raw input stored)
- Consent flow before every interaction
- Cost: $5/month

### Phase 3: Full Donor Platform
- D1 for pattern index, R2 for append-only logs
- Workers AI for on-edge inference (privacy maximum)
- Receipt system with thermal delay tracking
- Merkle roots published to git for audit trail
- Cost: $5-15/month

### Phase 4: Sovereignty
- Swiss-hosted Ollama backend (Infomaniak/Hetzner) for complete data sovereignty
- Distributed stewardship infrastructure
- Cost: $20-50/month
