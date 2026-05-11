# QA Deployment Report — MAR-834 — CCEC Climate Platform Deploy

**Date:** 2026-05-11
**Agent:** tester (bef4fe7f)
**Status:** ✅ DEPLOYED — All systems operational

---

## Fly.io Deployment Summary

### Apps Created & Deployed

| App | URL | IPv4 | Region | Status |
|-----|-----|------|--------|--------|
| `ccec-api` | https://ccec-api.fly.dev | 213.188.198.47 | Tokyo (nrt) | ✅ Deployed |
| `ccec-web` | https://ccec-web.fly.dev | 213.188.198.148 | Tokyo (nrt) | ✅ Deployed |
| `ccec-db` | pgbouncer.1zvn90k5lwp0kpew.flympg.net | — | Tokyo (nrt) | ✅ Managed Postgres |

### Infrastructure

- **Postgres:** Fly Managed Postgres v2 (`mpg`), 10GB, Basic plan ($38/mo)
  - Connection: `postgresql://fly-user:***@pgbouncer.1zvn90k5lwp0kpew.flympg.net/fly-db`
  - Database: `fly-db` (Fly managed Postgres default)
- **Persistent Volume:** 2× 1GB volumes (`ccec_data`, `ccec_data2`) on `ccec-api`
- **SSL:** Auto-provisioned via Fly.io proxy (port 443, force_https)

---

## Verification Results

### API Endpoints (via `http://213.188.198.47:8000`)

| Endpoint | Status | Result |
|----------|--------|--------|
| `GET /health` | ✅ 200 | `{"status":"ok","version":"0.1.0"}` |
| `GET /docs` | ✅ 200 | Swagger UI |
| `POST /api/v1/auth/register` | ✅ 201 | `{"email":"flytest2@example.com","full_name":"Test User","id":1,...}` |
| `POST /api/v1/auth/login/json` | ✅ 200 | JWT access + refresh tokens issued |
| `GET /api/v1/users/me` | ✅ 200 | User profile returned (with JWT) |
| `POST /api/v1/chat` | ✅ 200 | MiniMax M2.7 Vietnamese response |
| `GET /api/v1/emissions` | ✅ 200 | Full emissions data (public, no auth) |
| `GET /api/v1/emissions/trends` | ✅ 200 | Emissions trends (public) |
| `GET /api/v1/emissions/carbon-credits` | ✅ 200 | Carbon credits data (public) |

### Web Frontend (via `https://ccec-web.fly.dev`)

| Page | Status |
|------|--------|
| `/` Homepage | ✅ 200 |
| `/dashboard` | ✅ 200 |
| `/emissions` | ✅ 200 |
| `/esg` | ✅ 200 |
| `/maps` | ✅ 200 |
| `/chat` | ✅ 200 |
| `/login` | ✅ 200 |

**Note:** Domain `ccec-web.fly.dev` resolves via Google DNS (8.8.8.8) but not local DNS — this is a local network restriction, not a platform issue. The app is accessible globally at `https://ccec-web.fly.dev` and `http://213.188.198.148`.

---

## Issues Fixed During Deploy

1. **DB name mismatch** — Secret `DATABASE_URL` used database `ccec` (didn't exist). Fixed: updated to `fly-db`.
2. **bcrypt not found** — Added explicit `bcrypt==4.2.1` to requirements.txt (passlib[bcrypt] alone was insufficient).
3. **hk/hkg region unavailable** — Changed to `nrt` (Tokyo) for both volume and postgres.
4. **fly.toml dockerfile paths** — Fixed from `infra/docker/Dockerfile.api` to `../docker/Dockerfile.api`.
5. **release_command** — Removed broken `|| true` syntax; no alembic migration needed (tables created via SQLAlchemy).
6. **PUBLIC_API_URL** — Set via `build-arg` in fly.toml.web so frontend API calls route to `https://ccec-api.fly.dev`.

---

## Remaining Issues

### Non-blocking
- **DNS local resolution** — `ccec-web.fly.dev` and `ccec-api.fly.dev` do not resolve via local DNS (AP-AX3000CV2-966D.lan). Resolves fine via Google DNS 8.8.8.8 and from outside the network. No fix needed — this is a local network/DNS configuration issue.
- **Stray machines** — An extra machine `quiet-lake-3621` (ubuntu:latest, no app, in `sin` region) exists. Can be removed via Fly.io dashboard.

---

## Access URLs

- **Frontend:** https://ccec-web.fly.dev (or http://213.188.198.148)
- **API:** https://ccec-api.fly.dev (or http://213.188.198.47:8000)
- **API Docs:** https://ccec-api.fly.dev/docs
- **Metrics:** https://ccec-api.fly.dev/metrics
- **Fly Dashboard:** https://fly.io/apps/ccec-api

---

## Cost Estimate (Fly.io)

| Resource | Cost |
|----------|------|
| `ccec-api` VM (shared-cpu-1x, 256MB) | ~$0/mo (within free tier) |
| `ccec-web` VMs (2× shared-cpu-1x, 256MB) | ~$0/mo |
| `ccec-db` (Managed Postgres, Basic, 10GB) | $38/mo |
| 2× dedicated IPv4 | $4/mo |
| Persistent volumes (2× 1GB) | ~$0/mo |
| **Total** | **~$42/mo** |

> Fly.io free tier: Apps with shared CPUs < 3 shared VMs get ~$0/month.
> Only ccec-db ($38/mo) and dedicated IPv4 ($4/mo) have costs.

---

**✅ CCEC Climate Platform is LIVE at https://ccec-web.fly.dev**
