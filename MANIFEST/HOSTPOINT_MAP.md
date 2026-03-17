# HOSTPOINT CAPABILITY MAP

> What we have. What we can do. What we'll need to upgrade.

## Current Plan: Smart Webhosting

**Provider:** Hostpoint (hostpoint.ch)
**Account:** faragmoh
**Domain:** kalam.ch
**Cost:** ~CHF 7.90/month

### What's Included

| Capability | Status | Used By |
|------------|--------|---------|
| PHP 8.x | Available | axi.php, donor.php, proxy.php, migrate.php |
| MySQL/MariaDB | Available | Ledger, donors, interactions, exp001_runs |
| 250GB Storage | Available | Site files, database |
| SFTP/FTP | Available | GitHub Actions deployment |
| SSL/TLS | Available | HTTPS on kalam.ch |
| Email (SMTP) | Available | Magic link auth (MOVE-003) |
| Cron Jobs | Available | Scheduled tasks |
| .htaccess | Available | URL rewriting, security headers |
| PHP mail() | Available | Transactional email |
| File Manager | Available | Explorer at admin.hostpoint.ch |

### What's NOT Available (Smart Webhosting)

| Capability | Why Needed | When |
|------------|-----------|------|
| WebSocket | Real-time AXI responses | After 100 donors |
| Python runtime | Server-side organism | After 100 donors |
| Node.js runtime | SSR if needed | Not planned |
| Redis/Memcached | Caching, sessions | After 500 donors |
| Docker/containers | Isolation | After 1000 donors |
| Custom ports | Additional services | After 1000 donors |

### Upgrade Path

1. **Current (CHF 7.90/mo):** Smart Webhosting — covers MOVE-002 through MOVE-006
2. **Next (CHF 9.90/mo):** Cloud Server Basic — adds Python, WebSocket, full control
3. **Later (CHF 19.90/mo):** Cloud Server Standard — more CPU/RAM for training inference

### What We Can Do NOW Without Upgrading

- [x] Static site (Astro → HTML)
- [x] PHP backend (axi.php — full organism)
- [x] MySQL database (ledger, donors, interactions, experiments)
- [x] Magic link auth (PHP mail)
- [x] Multi-AI proxy (PHP cURL → external APIs)
- [x] GitHub Actions auto-deploy (SFTP)
- [x] Health checks (PHP endpoint)
- [x] Data export (PHP JSON generation)
- [ ] Cron jobs for scheduled analysis
- [ ] .htaccess security hardening

### What We CANNOT Do Without Upgrading

- [ ] Run Python organism server-side
- [ ] WebSocket for real-time streaming
- [ ] Host the trained LLM (too small anyway — use external inference)
- [ ] Background training jobs
- [ ] Server-sent events (SSE)

### Security Considerations

- `.config` file must be outside web root or protected by .htaccess
- Database credentials in GitHub Secrets, not in repo
- Magic link tokens expire in 15 minutes
- No raw PII in logs
- HTTPS enforced via .htaccess redirect

### Recommended .htaccess

```apache
# Force HTTPS
RewriteEngine On
RewriteCond %{HTTPS} off
RewriteRule ^(.*)$ https://%{HTTP_HOST}/$1 [R=301,L]

# Protect config files
<Files ".config">
    Require all denied
</Files>

# Security headers
Header always set X-Content-Type-Options "nosniff"
Header always set X-Frame-Options "DENY"
Header always set Referrer-Policy "strict-origin-when-cross-origin"
Header always set Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline' fonts.googleapis.com; font-src fonts.gstatic.com; connect-src 'self' api.groq.com"
```

---

**Assessment:** We do NOT need to upgrade yet. PHP + MySQL covers everything through 100 donors. Upgrade to Cloud Server when we need real-time responses or server-side Python.

[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
