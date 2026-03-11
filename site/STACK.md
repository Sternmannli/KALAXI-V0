# KALAM.CH — Technical Stack Decision

Date: 2026-03-11
Decided by: V-002 (research) + V-001 (authority)

## The Stack

**Astro 6 + Cloudflare Pages + Claude Haiku 4.5 (Phase 2)**

Note: Cloudflare acquired the Astro Technology Company in January 2026.
The framework remains MIT-licensed. This is now the native pairing.

## Why This Stack

### Framework: Astro 6
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
- $0.25/$1.25 per million tokens (input/output) — under $1 per 10,000 interactions
- Streaming via SSE through Cloudflare Worker (~600ms time-to-first-token)
- Anthropic API does not train on API inputs by default
- Escalate to Sonnet for complex interactions
- For maximum sovereignty: route through AWS Bedrock Zurich cross-region inference

### Interactive Islands: Svelte
- Write interactive components (input field, Threshold) in Svelte from day one
- If KALAXI outgrows islands, Svelte components transfer directly to SvelteKit with zero rewrite
- Svelte 5 runes system is mature; smallest bundle size of any reactive framework

### Rejected Alternatives
- **Next.js 16**: Over-engineered. CVSS 10.0 RCE in Jan 2026. 17% negative developer sentiment. Wrong energy for a philosophical foundation.
- **Plain HTML + htmx**: Beautiful simplicity but requires backend from day one. No static-first path.
- **SvelteKit alone**: Viable but ships JS runtime even in static mode. Astro's zero-JS default is more aligned with dignity-first minimalism.
- **Vercel**: $20/month Pro tier (Hobby restricted to non-commercial). No Swiss data center. Astro is second-class citizen.
- **Netlify**: US-centric data processing, weaker streaming support.

### Sovereignty Note (CLOUD Act)
All US-headquartered providers (Cloudflare, Vercel, Netlify) are subject to the US CLOUD Act.
For Phase 1 (static site, no user data), this is not a concern — no data to compel.
For Phase 2 (AI input processing donor text), options:
- **Pragmatic**: Cloudflare Workers as AI proxy. Accept exposure, document in privacy policy.
- **Sovereign**: Swiss-hosted backend on Infomaniak (Geneva, 100% Swiss-owned, zero CLOUD Act) + AWS Bedrock Zurich for AI inference.
- **Hybrid**: Static site on Cloudflare, AI proxy on Swiss infrastructure.
Decision deferred to Phase 2. Documented here so it is conscious, not accidental.

## Phase Plan

### Phase 1 (Current): Static Site
- Astro static output
- Deploy to Cloudflare Pages via git integration
- Four pages: Home, About, Canon, Invitation
- Zero JavaScript, zero tracking, zero cookies
- Cost: $0/month

### Phase 2: AI Integration
- Switch to hybrid output with Cloudflare adapter
- Add Svelte island for the input field (Threshold)
- Cloudflare Worker as AI API proxy with SSE streaming
- Pattern extraction → NDJSON append-only log in R2 (no raw input stored)
- Consent flow before every interaction: "Your words will be processed. The pattern will be kept. Your identity will not."
- SHA-256 hash receipts for contribution verification
- Umami (self-hosted) for privacy-preserving analytics — no cookies, <2KB
- Typography: 29LT Azahar variable superfamily (Arabic-Latin unified)
- Cost: $5/month

### Phase 3: Full Donor Platform
- Turso/libSQL for pattern index (5GB free, edge SQLite)
- R2 for append-only pattern logs with Merkle roots published to git
- Workers AI for on-edge inference (privacy maximum)
- Receipt system with thermal delay tracking
- Blind signatures for verifiable anonymous receipts
- DuckDB for periodic analytical passes over pattern archive
- Cost: $5-15/month

### Phase 4: Sovereignty
- Swiss-hosted backend on Infomaniak (Geneva/Zurich, zero CLOUD Act)
- Ollama for local AI inference
- AWS Bedrock Zurich for Claude inference within Swiss jurisdiction
- Distributed stewardship infrastructure
- Cost: CHF 20-50/month

## Design Principles
- Deep Night palette: #0a0a0f background, #e8e4df text, #c9a96e gold accent
- Light mode fallback via prefers-color-scheme
- Typography: Cormorant Garamond + IBM Plex Sans/Arabic (Phase 1), 29LT Azahar (Phase 2)
- 100vh sections, 65ch max-width, 8px spacing grid
- Breathing animation (4s cycle) for loading states — matches calm human breath
- Islamic-inspired geometric background at <2% opacity — felt, not seen
- Input field as threshold, not form. Placeholder: "قُل" (Speak). Submit: "→"
- Intentional friction: no infinite scroll, no engagement metrics, no social proof
- Respects prefers-reduced-motion and prefers-color-scheme

## Privacy Architecture
- No login, no cookies, no tracking, no fingerprinting
- Each interaction is complete in itself — no session concept
- Raw input processed by AI → pattern extracted → raw input discarded
- Only the pattern is stored (category, tags, linked covenants, day-precision timestamp)
- Compensating events for corrections (never modify, append only)
- Differential privacy noise on aggregate statistics
- Contribution bounding per session to limit sensitivity
