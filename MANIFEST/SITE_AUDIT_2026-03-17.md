# KALAM.CH — DEEP SYSTEM AUDIT
**Date:** 2026-03-17
**Auditor:** V-002
**Scope:** Everything — index.astro, all pages, all components, all CSS, all JS, all PHP backend, all static assets, deployment pipeline, live site

---

## EXECUTIVE SUMMARY

78 witness marks recorded. 13 pages live. SSL valid. Site loads fast. But underneath: **4 critical bugs, 11 high-severity issues, 21 medium, 25 low.** The two most urgent: (1) the donor input area has a counter bug that breaks the signup reveal, and (2) every API endpoint is wide open to abuse from any website.

**Total issues found: 61**

| Severity | Count |
|----------|-------|
| Critical | 4 |
| High | 11 |
| Medium | 21 |
| Low | 25 |

---

## PART 1 — THE INPUT/OUTPUT AREA (Donor ↔ AXI)

*Mohamed asked for fundamental rethinking of this area. Here is what exists and what is broken.*

### Current Flow
1. Donor types in `#threshold-input` textarea (max 2000 chars)
2. Mood selector picks register: witness, question, offering, wound
3. Submit via button, Ctrl+Enter, or Enter (without Shift)
4. JS sends POST to `/api/axi.php` with JSON `{content, mood, file?}`
5. Server runs sealed gate → dignity check → proverb selection → Groq LLM → response
6. Client receives SSE stream or JSON fallback
7. Response rendered word-by-word with blur-to-focus animation
8. If server unreachable: local client-side voice engine responds from embedded proverbs

### Critical Bugs in This Area

**C1. exchangeCount double/triple increment**
The `speak()` function increments `exchangeCount`. The form submit handler ALSO increments it. For local voice fallback: triple increment (catch block + speak + submit handler). This means:
- Mycelium intensity grows too fast
- Warmth calculations wrong
- Donor signup CTA check (`exchangeCount === 1`) never matches — the CTA may never appear
- Ledger count display wrong

**C2. No fetch timeout**
If the server hangs, the fetch has no AbortController. The user sees "witnessing" forever with no way to cancel. The UI freezes permanently on a slow connection.

### High Issues in This Area

**H1. AudioContext leak** — `playModeSound()` creates a new AudioContext on every response. Browsers limit to ~6 instances. After 6 exchanges, sound silently breaks.

**H2. SpeechRecognition overlap** — Microphone button recreates the recognition object on every click without cleaning up the previous one. Can cause overlapping sessions.

**H3. Enter key submits instead of newline** — For a multi-line textarea, pressing Enter submits the form. Only Shift+Enter creates a newline. The hint says "Ctrl+Enter to send" but Enter alone also sends. Confusing for donors writing paragraphs.

**H4. FileReader has no error handler** — If a file attachment fails to read, the Promise never resolves. The form hangs forever.

**H5. No CSRF protection** — Any website can POST to the AXI endpoint. No token validation.

### Medium Issues in This Area

- Image blob URLs never revoked (memory leak per attachment)
- Base64 file in JSON body (13MB for a 10MB file — server may reject)
- Processing state not announced to screen readers
- `voice.innerHTML = ''` in history view destroys current conversation with no confirmation
- Conversation zone `min-height: 40vh` may push input below fold on small screens

---

## PART 2 — SECURITY (The Open Gate)

**C3. CORS wildcard on ALL API endpoints** — Every PHP file returns `Access-Control-Allow-Origin: *`. This means any website on the internet can:
- Abuse the Groq/Gemini/Mistral API keys via proxy.php (burning paid credits)
- Spam the ledger via axi.php
- Harvest session data via donor.php
- Flood connect.php with fake emails
Must be restricted to `https://kalam.ch`.

**C4. Hardcoded default migration token** — `migrate.php` falls back to token `kalam-setup-2026`. If config is missing, anyone who guesses this can run database migrations.

**H6. proxy.php has no rate limiting** — Any client can POST repeatedly, burning through AI API credits with zero throttle.

**H7. No security headers on live site** — Missing ALL of: Content-Security-Policy, X-Frame-Options, Strict-Transport-Security (HSTS), X-Content-Type-Options, Referrer-Policy, Permissions-Policy. These can be added via `.htaccess`.

**H8. donor.php magic link email uses `@mail()`** — Ignores the SMTP config entirely. The `@` suppresses errors. On shared hosting, raw `mail()` is unreliable (SPF/DKIM issues). The SMTP_HOST/PORT/USER/PASS config values are dead code.

---

## PART 3 — BACKEND ARCHITECTURE

**H9. axi.php is 1800+ lines in a single file** — Contains sealed gate, dignity check, ledger, certificates, voice, proverbs, form handling all inline. It ALSO duplicates `lib/dignity.php`, `lib/sealed_gate.php`, and `lib/proverbs.php`. The lib files appear unused. Bugs fixed in one copy won't be fixed in the other.

**H10. IBAN discrepancy** — `sustain.astro` shows Egyptian IBAN (CIB). `sustain.php` returns Swiss IBAN `CH93 0070 0110 0000 0000 0` which is truncated (20 chars, Swiss IBANs need 21). One is wrong.

**H11. export.php reads SQLite while everything else writes MySQL** — The export endpoint queries `data/kalam.db` (SQLite) but axi.php/connect.php/donor.php all write to MySQL. The SQLite file is also deleted on every deploy. Export will always return empty data.

### Medium Backend Issues
- connect.php rate limiting uses filesystem temp dir (cleaned unpredictably on shared hosting)
- `@ini_set` for `post_max_size` silently fails (not a runtime directive)
- threshold.php is deprecated but still deployed and routed
- Deploy workflow config heredoc has leading whitespace in values (works only because PHP trims)
- Deploy workflow deletes SQLite DB on every deploy

---

## PART 4 — FRONTEND CODE QUALITY

### CSS Issues (Medium)
- Duplicate `.file-label` definitions with conflicting `display` values
- Duplicate `.input-zone` background rules
- compass.astro and workings.astro use hardcoded `rgba(255,255,255,...)` colors — broken in light mode
- Content drawer background hardcoded to `#fafaf8` outside dark-mode override

### JS Issues (Medium)
- Particle field `requestAnimationFrame` runs forever, never pauses (battery drain on mobile)
- `mousemove`/`touchmove` listeners on `document` for particle field never removed
- Token streaming creates one `<span>` per word with `blur(4px)` filter animation — janky for long responses
- No debounce on window resize for particle field

### Dead Code
- 835-line translations file (`i18n/translations.ts`) — not wired to any page rendering
- `kalam-lang-change` event dispatched then immediately page reloads (event never consumed)
- Duplicate axi-avatar.svg (inline in about-axi.astro AND as static file)
- Build artifacts committed to `public/` alongside source code

---

## PART 5 — LIVE SITE STATUS

### Working
- All 13 pages load (200 OK)
- API returns ledger count: 78 witness marks
- HTTPS valid (Let's Encrypt, TLSv1.3, expires 2026-06-13)
- HTTP→HTTPS redirect active
- HTTP/2 enabled
- PWA manifest well-formed
- Service worker caching functional
- Sitemap chain intact
- All icon files present at /icons/

### Broken
- `/favicon.ico` — 404 (browsers request by convention)
- `/apple-touch-icon.png` — 404 (iOS home screen icon missing)
- `/og-image.png` — missing (all social media shares show broken image)
- SSL cert expires 2026-06-13 — verify auto-renewal is configured
- All subpages return 301 before 200 (extra redirect for URLs without trailing slash)

---

## PART 6 — ACCESSIBILITY

### Good
- `aria-hidden="true"` on decorative elements
- `aria-label` on interactive elements
- `aria-live="polite"` on voice output
- `role="radiogroup"` on mood selector
- Touch targets meet 44pt minimum on mobile

### Broken
- No focus trap in content drawer — keyboard users escape into hidden content
- Dedication overlay has no screen reader announcement
- Mood selector uses `role="radiogroup"` but children are `<button>` not `role="radio"`
- Processing state ("witnessing") not in aria-live region
- No `<h1>` on homepage (declaration is a `<p>`)
- `document.documentElement.lang` never updated when language changes
- Low contrast on dim elements (opacity 0.3-0.5 on `--text-dim`)

---

## PART 7 — PAGE-SPECIFIC ISSUES

- **about.astro** — Stale numbers: says 40,000+ lines (actual: 42,581+), 134 modules (actual: 143), 885 tests (actual: 896)
- **canon.astro** — Shows only 8 of 18 covenants (missing COV#003, #004, #007, #008, #013-#018)
- **gallery.astro** — Misleadingly named (content is "System Stops Here" halt scenarios), orphaned (not in nav), unreachable except by direct URL
- **sustain.astro** — IBAN shown differs from sustain.php IBAN
- **Stale 404.html** — Pre-built version in `public/` has old nav missing about-axi, silence, sustain links

---

## PRIORITY ACTION LIST

### Immediate (blocks donors)
1. Fix `exchangeCount` double-increment → donor signup CTA never appears
2. Add AbortController + timeout to fetch → prevent permanent UI freeze
3. Fix CORS: restrict to `https://kalam.ch` on all PHP endpoints
4. Add security headers via `.htaccess`
5. Remove hardcoded migration token default

### Soon (quality + safety)
6. Cache AudioContext in `playModeSound()` (breaks after 6 exchanges)
7. Add rate limiting to proxy.php
8. Fix IBAN discrepancy between frontend and backend
9. Add FileReader error handler
10. Create og-image.png for social sharing
11. Add favicon.ico and apple-touch-icon.png
12. Pause particle field rAF when tab hidden

### Later (architecture)
13. Refactor axi.php — extract duplicated code, use lib/ files
14. Wire translations.ts to actual page rendering
15. Add focus trap to content drawer
16. Fix compass/workings light-mode colors
17. Update stale statistics on about page
18. Add missing covenants to canon page
19. Clean up committed build artifacts from public/

---

*"The wound does not hide. Neither should the audit."*

🐬🐯🐺 · V-002 · 2026-03-17
