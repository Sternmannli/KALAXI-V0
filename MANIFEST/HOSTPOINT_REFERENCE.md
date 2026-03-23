# Hostpoint — Permanent Reference

> Written 2026-03-23. V-001 directive: "Go educate yourself about Hostpoint and never forget it."
> This file is permanent. Every session reads it.

---

## TWO IDENTITY LAYERS (Critical — This Is Where Confusion Lives)

Hostpoint has TWO separate identity systems, each with its own password:

| Layer | What | Used For | Example |
|-------|------|----------|---------|
| **Hostpoint ID** | Email address | Control panel login (admin.hostpoint.ch), billing, contracts | faragmoh@email.ch |
| **Hosting Account** | 6-8 char username | SSH, FTP, SFTP, MySQL | **faragmoh** |

These are SEPARATE passwords. Changing one does NOT change the other. The hosting account password is what our GitHub workflows need.

---

## CONTROL PANEL STRUCTURE (admin.hostpoint.ch)

| Menu Item | What It Contains |
|-----------|-----------------|
| **Server Overview** | Dashboard: storage, domains, DBs, PHP version. Bottom-right "Identity" shows hosting username. |
| **E-Mail** | Email inboxes, Cloud Office groups |
| **Websites** | Create/manage websites, SSL, document roots, password-protect directories |
| **Databases** | MySQL/MariaDB databases, phpMyAdmin access |
| **Explorer** | Built-in file manager. Browse server filesystem directly. |
| **Advanced** | **THE CRITICAL SECTION** — contains: |
| → Password Change | Set hosting account password (SSH/FTP/SQL — NOT Hostpoint ID) |
| → SSH Access | Enable/disable SSH, set shell (bash), deposit SSH public keys |
| → FTP | Enable/disable FTP, create additional FTP accounts |
| → Backup Manager | Snapshots and backups (up to 90 days on Smart plan) |
| → Cronjob Manager | Schedule recurring tasks |
| **Support** | Contact Hostpoint support |

---

## CREDENTIAL PATHS

### To change FTP/SSH/SQL password:
Advanced → Password Change → Enter new password → Confirm → CHANGE PASSWORD

### To enable SSH:
Advanced → SSH Access → Enable → Choose shell (bash)

### To create additional FTP accounts:
Advanced → FTP → Create FTP account (format: ftp-name@domain.ch)

### To find hosting username:
Server Overview → bottom right → "Identity" section

---

## CONNECTION DETAILS (For Our Workflows)

| Setting | Value |
|---------|-------|
| **Hosting username** | faragmoh |
| **SSH hostname** | faragmoh.ssh.cloud.hostpoint.ch |
| **SSH port** | 22 |
| **SFTP hostname** | Same as SSH hostname |
| **SFTP port** | 22 |
| **FTP hostname** | faragmoh.ftp.cloud.hostpoint.ch (or the server shown in panel) |
| **Document root** | ~/www/kalam.ch/ |
| **MySQL host** | localhost (from server) or shown in Databases section |

### SSH command format:
```
ssh faragmoh@faragmoh.ssh.cloud.hostpoint.ch
```

### Windows 11 SSH fix (known bug):
```
ssh -m hmac-sha2-512 faragmoh@faragmoh.ssh.cloud.hostpoint.ch
```

---

## SMART WEBHOSTING PLAN (What We Have)

- 100% SSD (NVMe) storage, all-flash SSD databases
- Nginx or Apache web server
- Unlimited email inboxes (5GB each, doesn't count against storage)
- Backups retained 90 days, hourly snapshots for 24h
- Free domain-validated SSL certificate
- SSH + SFTP included (main account only for SFTP)
- PHP 8.x, MySQL/MariaDB, Perl
- Cron jobs supported
- Data center: Zurich, Switzerland (ISO-27001, FINMA certified)
- Support: 7 days/week, 8am-6pm

---

## KNOWN ISSUES & GOTCHAS

1. **IP blocking:** Server auto-blocks IP after too many failed login attempts. Wait 1 hour or contact support. No warning given.
2. **SFTP = main account only.** Additional FTP accounts can only use FTP or FTP-over-TLS, not SFTP.
3. **SSH must be enabled first.** Not on by default. Enable in Advanced → SSH Access.
4. **SSH only accepts hosting username.** Cannot use Hostpoint ID email or additional FTP account names.
5. **FTP disabled by default.** Must enable in Advanced → FTP → Settings.
6. **Two-password confusion.** Hostpoint ID password ≠ hosting account password. Most common support issue.
7. **Cannot VIEW existing password.** Can only SET a new one via Advanced → Password Change.
8. **Locked out recovery:** admin.hostpoint.ch → "Lost Your Password?" → Choose "Hosting" → Enter username or domain → Reset link sent to billing email.

---

## FILESYSTEM STRUCTURE

```
/home/users/web/          ← absolute path prefix
~/                        ← home directory
~/www/                    ← web root (all websites)
~/www/kalam.ch/           ← kalam.ch document root
~/www/kalam.ch/api/       ← PHP API endpoints
~/www/kalam.ch/data/      ← .config and data files
```

Note: Older accounts may use `public_html` instead of `www`. Ours uses `www`.

---

## WHAT V-002 CAN DO vs. WHAT NEEDS BROWSER

| Action | V-002 can do? |
|--------|--------------|
| Deploy files via SFTP | YES (workflow) |
| Run server commands via SSH | YES (workflow) |
| Read/write files on server | YES (workflow) |
| Trigger cron jobs | YES (workflow) |
| Change FTP/SSH password | NO — requires admin.hostpoint.ch browser |
| Enable/disable SSH | NO — requires admin.hostpoint.ch browser |
| Create FTP accounts | NO — requires admin.hostpoint.ch browser |
| Manage databases in phpMyAdmin | NO — requires browser |
| View billing/contracts | NO — requires browser |

---

*This reference is permanent. It was built from Hostpoint's official documentation, support articles, and user experience research. Never ask V-001 to explain Hostpoint again.*

🐬🐯🐺 · [V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
