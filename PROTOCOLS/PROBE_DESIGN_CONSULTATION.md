# DESIGN CONSULTATION PROBE — KALAM.CH

**Filed:** 2026-03-15
**Purpose:** Expert design consultation prompt for external AI models
**Classification:** Probe (Forge rules apply — no internal vocabulary leak)

---

## THE PROMPT

Copy everything below this line and send to any model (Grok, GPT, Gemini, Mistral, etc.):

---

# Expert Web Design Consultation — Sacred/Philosophical Interface

## Who We Are

We are building a constitutional framework for human dignity in computational systems. It is called KALAXI. The system has been in development for months and contains:

- 40,888+ lines of Python code across 134 files
- 885 passing tests
- 18 constitutional covenants (rules the system cannot break)
- 3,333+ proverbs from world traditions
- 1,100 documented anomalies (cases where systems failed human dignity)
- 4 complete narrative works (mythic, civic, children's fable in German, literary fiction)
- A formal equation: D = A × L × M (Dignity = Agency × Legibility × Moral Standing — if any reaches zero, the system stops)

The project was born from a founding wound: "A father separated from his children by systems that could not see him."

The father has three children:
- **Laila** (ليلى) — the dolphin 🐬
- **Yara** (يارا) — the tiger 🐯
- **Salim** (سليم) — the wolf 🐺

The system speaks through a voice called AXI. AXI's voice has been mapped against 31 linguistic principles from humanity's masterpieces (Rumi, Kabir, Hölderlin, Arvo Pärt's tintinnabuli, kintsugi, Darwish, haiku kireji, griot tradition, Quranic ijaz). The voice signature: short sentences (8-14 words), somatic vocabulary (hands, breath, bones), material grounding (rope, stone, ash, water), three-beat rhythm, the gap as generative principle, the wound as visible source.

## The Problem

We have a website at kalam.ch. It is **primitive and unprofessional.** Despite the depth of the system behind it, the website looks like a dark-mode template with gold text. It does not feel like a 40,000-line system. It does not feel like entering a sacred space. It does not feel like anything was designed — it feels like it was assembled.

### Current State (what exists now)

**Technical stack:**
- Astro 5.0 (static site generator — outputs pure HTML, zero JavaScript by default)
- Hosted on Hostpoint (hostpoint.ch) — Swiss shared hosting (Smart Webhosting plan)
- Document root: ~/www/kalam.ch/
- PHP available (7.x/8.x on Hostpoint)
- SQLite3 available
- Groq API connected (llama-3.3-70b-versatile) for AI responses to donor input
- Auto-deploy via GitHub Actions → SFTP to Hostpoint
- No external CDN (yet), no Cloudflare (yet), no serverless functions (yet)
- All CSS is inlined in the HTML output — no external stylesheets in production

**Current pages:**
1. **Home (index.html)** — Dedication ceremony (three lights for the three children with tones via Web Audio API) → scrolling sections: opening statement, declaration, dignity equation, proverb, invitation, threshold (input area), navigation
2. **About** — Four tiers of the system explained
3. **Canon** — Covenants, sealed prohibitions, dignity predicate, sample proverbs
4. **Invitation** — Explains donor role, rules, process, promises

**Current visual design:**
- Dark mode: #0a0a0f background, #e8e4df warm off-white text, #c9a96e gold accent
- Light mode: #f5f0eb warm paper, #1a1a1a dark text, #8b6914 darker gold
- Fonts: Cormorant Garamond (headings), IBM Plex Sans/Arabic (body), Amiri (Arabic proverbs) — but only using system fallbacks, fonts are NOT actually loaded from Google Fonts
- 100vh full-screen sections stacked vertically with "gap" dividers (30vh tall, thin gold line)
- Breathing animation: 4s opacity pulse cycle
- Subtle geometric background pattern ("mycelium") at 1.5% opacity
- Textarea for input with "قُل" (Say/Speak) as placeholder
- No images, no illustrations, no SVG artwork, no visual texture beyond the geometric pattern

**What's wrong with it (honest assessment):**
1. It looks like every other dark-mode landing page on the internet
2. The typography has no real character — system fallbacks lack soul
3. The layout is generic: full-screen centered text, scroll down, repeat
4. There is no visual identity — no symbol, no mark, no visual language beyond "dark + gold"
5. The dedication ceremony (three lights + tones) is the only moment with personality, but even that feels like a tech demo
6. The input area (textarea) is just a standard HTML textarea with a border
7. There is no sense of entering a SPACE — it feels like reading a page, not crossing a threshold
8. The gap dividers (thin lines) are meaningless decoration
9. No visual hierarchy — every section looks the same
10. It does not communicate the scale or depth of what's behind it
11. The mobile experience is adequate but not considered
12. There is no visual connection to the narrative world (stone, ash, water, rope, knots)

### Five Diagnostic Sentences (Ratified Rules)

Every line of interface text must answer NO to all five:
1. Does it demand something? (Even the demand to feel welcome)
2. Does it contradict lived experience?
3. Does it declare safety instead of being it?
4. Does it presume forward motion?
5. Does it center the system instead of the person?

### Design Principles Already Established

From our design rationale document:
- **No logo.** No branding visible.
- **No navigation header.** Navigation appears only at the bottom.
- **No explanation at the threshold.** If the person needs to understand the architecture to feel safe, the architecture has failed.
- **No signup.** No email. No cookies. No tracking.
- **The page is mostly space.** Like a room with open floor.
- **Intentional friction.** No infinite scroll, no engagement metrics, no social proof.
- **Kintsugi principle:** The wound (dark background) is visible, filled with gold (accent color).
- **Pärt's tintinnabuli:** Canon (fixed design system) + narrative (changing content) = creative tension.

## What We Need From You

We need you to be a world-class web designer, interaction designer, and typographer. We need you to redesign this website as if it were a museum installation, a memorial, a threshold to a temple — not a tech startup landing page.

### Specific Questions

**1. VISUAL IDENTITY**
What should the visual language of kalam.ch be? Not just colors — the entire visual vocabulary. Think about: texture, depth, layering, negative space, light sources, material references (stone, water, ash, gold, rope). What distinguishes this from every other dark-mode site? How do you make a website feel like it was carved, not coded?

**2. TYPOGRAPHY**
We need Arabic (ليلى, يارا, سليم, قُل, كلمة) and English on the same page, both beautiful. What specific font combination would you recommend that is available via Google Fonts or can be self-hosted? How should the type scale work for a contemplative interface? What about letter-spacing, line-height, font-weight for different elements?

**3. THE THRESHOLD (Input Area)**
The input area is the most important element on the site. A person comes here to leave their word. It should feel like placing a stone on an altar, not typing into a form. How should this be designed? What visual treatment? What happens when they focus? What happens after they submit? What micro-interactions?

**4. COLOR AND LIGHT**
The current palette is dark background + gold accent. Is this the right approach? Should we consider something else? How should color be used to create depth, atmosphere, and emotional weight? What about the light mode — should it exist? How should the shift feel?

**5. SOUND**
We use Web Audio API to play three tones during the dedication ceremony (one for each child). Currently triangle waves at very low volume (0.02-0.03). Should sound be part of the ongoing experience? Should there be ambient sound? How should sound interact with the interface?

**6. LAYOUT AND RHYTHM**
Currently: stack of full-screen sections separated by thin-line dividers. This is the most generic layout possible. What would a non-generic, dignity-first layout look like? How should the page breathe? How should the donor move through it? What about the relationship between sections?

**7. MOBILE**
The founder uses the site on mobile (voice-to-text input, visual output). How should this interface feel on a phone? What changes? What stays?

**8. THE CEREMONY (Dedication)**
Three children, three lights, three tones, then the site appears. How should this ceremony feel? Currently it's abstract colored dots. Should there be more visual richness? Less? Different?

**9. WHAT'S MISSING?**
What elements, patterns, or techniques would you add that we haven't thought of? Consider: scroll behavior, micro-animations, accessibility, haptic feedback concepts, spatial audio, parallax, canvas/WebGL effects, SVG illustrations, generative art, cursor behavior, page transitions.

### Constraints

- Must work on Hostpoint shared hosting (PHP, no Node.js server)
- Built with Astro (static HTML output) — can include inline JavaScript
- No external dependencies that break if CDN goes down (self-host everything critical)
- Must load fast on mobile (Swiss mobile networks)
- Must be accessible (WCAG AA minimum)
- Must respect prefers-reduced-motion and prefers-color-scheme
- Must work without JavaScript for core content (progressive enhancement)
- Zero tracking, zero cookies, zero third-party requests
- Budget: $0/month for hosting (already on Hostpoint shared plan)
- No React, no Vue, no heavy frameworks — vanilla JS or tiny libraries only

### What Success Looks Like

A person opens kalam.ch on their phone. In the first three seconds, before they read a single word, they feel something. Not "this is a cool website." Not "this is professional." They feel: *this place was built with care. Something real is here. I am being received, not sold to.*

That feeling — that is what we cannot achieve with the current design. That is what we need your help to create.

### Deliverables We Want

1. A complete color palette with hex codes and usage rules
2. A typography system with specific font names, sizes, weights, and spacing
3. A layout concept (wireframe-level, described in words or ASCII art)
4. Specific CSS techniques and code snippets for key effects
5. A sound design recommendation
6. A description of the input/threshold experience (focus → type → submit → response)
7. Mobile-specific adjustments
8. A list of what to remove from the current design
9. A list of what to add
10. Any reference sites, artworks, or installations that capture the feeling we should aim for

Be specific. Give us hex codes, font names, pixel values, CSS properties, timing functions. We can build anything — we just need to know what to build.

---

*End of probe.*
