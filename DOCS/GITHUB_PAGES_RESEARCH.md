# GitHub Pages Research: Gen Z Attractive Site for Research Toolkit
## Research Date: 2026-03-14

---

## 1. FRAMEWORK RECOMMENDATION

### Winner: Astro
- **Ships zero JavaScript by default** — pure static HTML output, perfect match for GitHub Pages
- 2-3x faster than Next.js for content sites, 50-80% cheaper to build
- Mix React/Svelte/Vue components inside Astro pages (Islands Architecture)
- Official GitHub Action (`withastro/action`) for near-zero-config deploy
- Official starter template: github.com/withastro/github-pages
- ~200K weekly npm downloads, 48K+ GitHub stars
- Write pages in Markdown/MDX natively
- SEO works out of the box with clean static HTML

### Deploy Setup (3 files total):
1. `astro.config.mjs` — set `site` and `base` for GitHub Pages
2. `.github/workflows/deploy.yml` — uses `withastro/action`
3. Pages content in `src/pages/`

### Runner-Up: Plain HTML + Tailwind CSS
- Zero build step possible (CDN Tailwind)
- Maximum simplicity, zero framework lock-in
- Good if we want absolute minimal tooling

### Avoid for GitHub Pages:
- Next.js (needs `next export`, loses SSR/ISR, overkill for static)
- SvelteKit (possible but less GitHub Pages ecosystem)
- Jekyll (dated, Ruby dependency, slow)

---

## 2. GEN Z DESIGN TRENDS (2025-2026)

### Visual Style
- **Controlled Maximalism**: Bold but intentional, not chaotic
- **Dark Glassmorphism**: Frosted glass panels over deep gradients — THE defining aesthetic
- **Kinetic Typography**: Text that moves, stretches, reacts to scroll/cursor
- **Exaggerated Hierarchy**: Oversized headlines + tiny supporting text
- **Retro-Futurism**: 80s/90s nostalgia remixed with holographic/metallic gradients
- **Collage/Scrapbook**: Sticker graphics, torn textures, hand-drawn elements
- **Anti-AI Aesthetic**: Imperfection, texture, glitch — rebellion against sterile automation

### What Gen Z Rejects
- Corporate minimalism
- Sterile white backgrounds
- Cookie-cutter templates
- Over-polished perfection
- "Helpful" blandness

### Key Principles
- Emotion over order
- Self-made over systematized
- Real over perfect
- Dopamine design (bright, saturated, joyful)

---

## 3. COLOR PALETTES (Specific Hex Codes)

### PALETTE A: "Dark Glassmorphism Research" (RECOMMENDED)
Best for a dignity/AI research toolkit — feels techy, warm, sophisticated.

| Role | Color Name | Hex | Notes |
|------|-----------|-----|-------|
| Background | Deep Space | `#0a0a0f` | Near-black with slight blue |
| Background Alt | Midnight Navy | `#1a1a2e` | Layered sections |
| Glass Panel | Frost | `rgba(255,255,255,0.05-0.15)` | With backdrop-filter blur(12px) |
| Glass Border | Ice Edge | `rgba(255,255,255,0.1-0.2)` | Subtle 1px borders |
| Primary Accent | Electric Violet | `#7b2ff7` | CTAs, highlights |
| Secondary Accent | Cyan Glow | `#00d4ff` | Links, secondary actions |
| Warm Accent | Hot Pink | `#ff0080` | Sparingly, for energy |
| Text Primary | Snow | `#f3f4f6` | Body text on dark |
| Text Secondary | Cool Gray | `#9ca3af` | Muted labels |
| Success/Positive | Mint | `#34d399` | Status indicators |

### PALETTE B: "Warm Tech" (Alternative — Light Mode)
| Role | Color Name | Hex |
|------|-----------|-----|
| Background | Warm Off-White | `#F4F2EE` |
| Background Alt | Soft Beige | `#DCC2B6` |
| Primary Accent | Bold Orange | `#F48C06` |
| Secondary | Deep Teal | `#2A9D8F` |
| Text | Charcoal | `#262626` |
| Highlight | Warm Yellow | `#E9C46A` |

### PALETTE C: "Monochrome Bold" (Striking Single-Hue)
Pick ONE dominant color and push it to extremes:
- Electric Blue: `#2563eb` across backgrounds, type, visuals
- Crimson: `#dc2626`
- Lime: `#84cc16`
- Muted Purple: `#7c3aed`

### Gradient Combos (for backgrounds/hero sections):
- Violet to Cyan: `#7b2ff7` → `#00d4ff`
- Deep Purple to Hot Pink: `#4c1d95` → `#ff0080`
- Midnight to Teal: `#1a1a2e` → `#2A9D8F`
- Black to Deep Purple: `#0a0a0f` → `#4c1d95`

---

## 4. GLASSMORPHISM CSS (Ready to Use)

```css
/* Dark glassmorphism card */
.glass-card {
  background: rgba(255, 255, 255, 0.08);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 16px;
  padding: 2rem;
}

/* Fallback for unsupported browsers */
@supports not (backdrop-filter: blur(12px)) {
  .glass-card {
    background: rgba(26, 26, 46, 0.95);
  }
}

/* Gradient background behind glass */
.gradient-bg {
  background: linear-gradient(135deg, #0a0a0f 0%, #1a1a2e 50%, #4c1d95 100%);
}

/* Glow accent */
.glow {
  box-shadow: 0 0 30px rgba(123, 47, 247, 0.3);
}
```

---

## 5. TYPOGRAPHY (Google Fonts)

### RECOMMENDED STACK:

#### Headlines: Space Grotesk
- Futuristic feel, distinctive character shapes
- Weights: 300-700 (5 weights, no italics)
- Perfect for: tech-focused, cutting-edge research vibe
- `font-family: 'Space Grotesk', sans-serif;`

#### Body Text: DM Sans
- Rounded corners, open apertures, generous spacing
- Optical sizing auto-adjusts for size
- Super readable at small sizes (mobile-perfect)
- `font-family: 'DM Sans', sans-serif;`

#### Code/Technical: JetBrains Mono
- Made for developers, maximized lowercase height
- Ligatures for code readability
- Dot-zero to distinguish from O
- 8 weights + italics
- `font-family: 'JetBrains Mono', monospace;`

### Alternative Stacks:

**Stack B (Warmer):**
- Headlines: Plus Jakarta Sans (geometric, friendly, modern)
- Body: Inter (workhorse, tall x-height, screen-optimized)
- Code: JetBrains Mono

**Stack C (Editorial):**
- Headlines: Instrument Serif (expressive, distinctive)
- Body: Instrument Sans (clean companion)
- Code: Space Mono

**Stack D (Vercel-inspired):**
- Headlines + Body: Geist (polished Inter variant by Vercel)
- Code: Geist Mono

### Google Fonts Import:
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=DM+Sans:opsz,wght@9..40,400;9..40,500;9..40,700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
```

---

## 6. LANDING PAGE STRUCTURE (Optimal Order)

For a research toolkit measuring dignity in human-AI interaction:

### Section 1: HERO (Above the Fold)
- Bold headline: What the tool does in one line
- Subheadline: Why it matters (2 sentences max)
- One strong visual (animated diagram, glassmorphic card with live metric)
- Primary CTA: "Try the Framework" or "Read the Paper"
- Micro social proof: "Used by X researchers" or star count badge

### Section 2: THE PROBLEM
- 2-3 sentences on why dignity measurement in AI matters
- Visual: before/after or gap diagram
- Emotional hook — this is where Gen Z connects

### Section 3: HOW IT WORKS
- 3-4 feature cards (glassmorphic)
- Icon + short title + one-line description each
- Possible features: Measurement, Framework, Scoring, Reports

### Section 4: LIVE DEMO / INTERACTIVE
- Embedded interactive element or animated visualization
- Show the tool in action — even a static screenshot beats nothing
- Code snippet showing API usage (in JetBrains Mono)

### Section 5: KEY METRICS / STATS
- Big numbers in oversized type (Space Grotesk 4-6rem)
- e.g., "6 Dimensions Measured" / "0.648 Baseline Reading" / "Open Source"
- Counter animation on scroll

### Section 6: METHODOLOGY (For Researchers)
- Collapsible/expandable section
- Links to papers, equations, formal definitions
- Keep it dense but scannable

### Section 7: GET STARTED / CTA
- Installation command in a code block
- "pip install kalam-framework" style
- GitHub link, documentation link
- Final CTA button

### Section 8: FOOTER
- MIT License badge, GitHub link, citation format
- Minimal — no bloat

### Dev Tool Landing Page Rules (from study of 100+ devtool pages):
- No salesy language
- Clever and simple wins
- Clean design + solid typography + breathing room
- Curated testimonials (not auto-pulled)

---

## 7. SINGLE-PAGE vs MULTI-PAGE

### RECOMMENDATION: Single-Page with Anchor Sections

**Why single-page:**
- Gen Z scrolls, doesn't click nav
- Smooth scroll between sections feels modern
- Simpler to build and maintain
- Better storytelling flow (problem → solution → proof → action)
- Works perfectly with GitHub Pages (no SPA routing hacks needed)
- Mobile-native feel (scroll > navigate)

**When to add sub-pages:**
- Documentation (link out to docs site or /docs)
- Blog/changelog (separate pages via Astro's Markdown routing)
- Detailed methodology paper

**Implementation:**
- Single `index.html` with anchor links (#hero, #features, #demo, etc.)
- Sticky/fixed nav with smooth scroll
- Optional: separate /docs route for deep content

---

## 8. MOBILE-FIRST DESIGN

### Critical Stats:
- 60%+ of web traffic is mobile
- 75%+ expected in 2025
- Gen Z: phone is primary (often only) screen
- 1-second delay = 7% conversion drop

### Must-Do:
1. **Touch targets**: Minimum 48x48px tap areas
2. **Thumb zone**: Primary CTAs in bottom half of screen
3. **Font size**: 16px minimum body text (no zoom needed)
4. **Spacing**: Generous padding between tappable elements (66% of mobile sites fail this)
5. **Dark mode support**: Auto-detect via `prefers-color-scheme` media query
6. **No horizontal scroll**: Ever
7. **Hamburger menu**: Collapsible nav on mobile
8. **Sticky header**: Thin, stays visible on scroll
9. **Bottom nav**: Consider for multi-section single-page

### CSS Media Query Strategy:
```css
/* Mobile first — base styles ARE mobile */
.container { padding: 1rem; }
.hero-title { font-size: 2rem; }

/* Tablet */
@media (min-width: 768px) {
  .container { padding: 2rem; }
  .hero-title { font-size: 3.5rem; }
}

/* Desktop */
@media (min-width: 1024px) {
  .container { padding: 4rem; max-width: 1200px; margin: 0 auto; }
  .hero-title { font-size: 5rem; }
}
```

### Performance:
- Lazy-load images below fold
- Use WebP/AVIF image formats
- Minimize JS (Astro ships zero by default)
- Target < 3 second full load
- Consider PWA for app-like experience

---

## 9. BEAUTIFUL GITHUB PAGES EXAMPLES TO STUDY

### Repos with Stunning Pages:
- `nordicgiant2/awesome-landing-page` — curated landing page templates
- `PaulleDemon/awesome-landing-pages` — free templates, browsable at awesome-landingpages.vercel.app
- `withastro/github-pages` — Astro's official GitHub Pages starter
- GitHub Topics: `landing-page-template` — many Astro + Tailwind starters

### Common Tech Stack of Beautiful Pages:
1. Astro + Tailwind CSS (rising fast)
2. Next.js + Tailwind + TypeScript (most popular overall)
3. Plain HTML/CSS/JS (for simplicity)

### What Makes Them Stand Out:
- Dark backgrounds with vibrant accent gradients
- Glassmorphic cards for feature sections
- Oversized typography in hero
- Smooth scroll animations
- Code snippets styled with syntax highlighting
- Minimal, focused navigation
- Strong visual hierarchy
- Interactive demos or live previews

---

## 10. IMPLEMENTATION RECOMMENDATION

### Stack:
- **Framework**: Astro (static output, GitHub Pages native)
- **Styling**: Tailwind CSS (utility-first, responsive, dark mode built-in)
- **Fonts**: Space Grotesk + DM Sans + JetBrains Mono
- **Palette**: Dark Glassmorphism (Palette A above)
- **Structure**: Single-page with anchor sections
- **Animations**: CSS-only (scroll-driven animations via `animation-timeline: scroll()`)
- **Deploy**: GitHub Actions via `withastro/action`

### File Structure:
```
public-site/
  src/
    pages/
      index.astro          # Single page with all sections
    components/
      Hero.astro
      Problem.astro
      Features.astro
      Demo.astro
      Stats.astro
      Methodology.astro
      GetStarted.astro
      Footer.astro
    layouts/
      Base.astro            # HTML head, fonts, meta
    styles/
      global.css            # Tailwind + glassmorphism utilities
  public/
    favicon.svg
    og-image.png
  astro.config.mjs
  tailwind.config.mjs
  .github/
    workflows/
      deploy.yml
```

---

## Sources

### Frameworks
- https://cloudcannon.com/blog/the-top-five-static-site-generators-for-2025-and-when-to-use-them/
- https://pagepro.co/blog/astro-nextjs/
- https://docs.astro.build/en/guides/deploy/github/
- https://github.com/withastro/github-pages

### Gen Z Design
- https://www.figma.com/resource-library/web-design-trends/
- https://graphicdesignjunction.com/2025/12/web-design-trends-of-2026/
- https://www.supercharged.studio/blog/gen-z-design-trends
- https://reallygooddesigns.com/graphic-design-trends-2026/

### Color
- https://hookagency.com/blog/website-color-schemes-2020/
- https://www.elegantthemes.com/blog/design/color-palettes-for-balanced-web-design
- https://macaronsandmimosas.com/web-design-colors-for-2025-warm-natural-vibes-cheerful-pops-of-joy/

### Glassmorphism
- https://medium.com/@developer_89726/dark-glassmorphism-the-aesthetic-that-will-define-ui-in-2026-93aa4153088f
- https://playground.halfaccessible.com/blog/glassmorphism-design-trend-implementation-guide
- https://natebal.com/glassmorphism-web-design/

### Landing Pages
- https://evilmartians.com/chronicles/we-studied-100-devtool-landing-pages-here-is-what-actually-works-in-2025
- https://www.flow.ninja/blog/landing-page-checklist
- https://landingi.com/landing-page/41-best-practices/

### Typography
- https://medium.com/design-bootcamp/best-google-font-pairings-for-ui-design-in-2025-ba8d006aa03d
- https://www.typewolf.com/google-fonts
- https://shakuro.com/blog/best-fonts-for-web-design
- https://maxibestof.one/typefaces/jetbrains-mono

### Mobile
- https://www.brandvm.com/post/mobile-first-design-principles-2025
- https://mobisoftinfotech.com/resources/blog/ui-ux-design/gen-z-ux-design-guide
- https://www.convergine.com/blog/what-is-mobile-first-design-complete-guide-2025/
