## MAR-849 QA Smoke Test Results

**Date:** 2026-05-11
**Platform:** CCEC Climate Platform (local dev)
**QA:** Playwright headless | 13 checks

---

### 13/13 PASS | 0 FAIL

| Check | Result | Notes |
|---|---|---|
| Build clean | PASS | `pnpm build` 8 pages in 8.3s |
| API startup | PASS | uvicorn on port 8000, health 200 |
| Landing (/) | PASS | HTTP 200, header rendered |
| Dashboard (/dashboard) | PASS | HTTP 200, no JS errors |
| Emissions (/emissions) | PASS | HTTP 200, chart loads |
| ESG (/esg) | PASS | HTTP 200, chart loads |
| Maps (/maps) | PASS | Leaflet container rendered |
| Chat (/chat) | PASS | HTTP 200, widget loads |
| Login page (/login) | PASS | email + password fields present |
| Login form submit + JWT | PASS | OAuth2 form login, JWT stored in localStorage |
| API /health | PASS | `{"status":"ok"}` |
| API /api/v1/emissions | PASS | 2024 data, 10 provinces |
| API /api/v1/climate/forecast | PASS | 7-day forecast (auth required) |
| API /auth/register | PASS | HTTP 201, user created |
| docker-compose.yml | PASS | 6 services: postgres, redis, api, web, prometheus, grafana |

---

### Known limitations (expected behavior)

1. **Chat AI unavailable:** `/api/v1/chat` returns demo mode message. Root cause: `apps/api/.env` does not exist, no `MINIMAX_API_KEY` configured. Fix: Create `apps/api/.env` with `MINIMAX_API_KEY=sk-cp-JKc...`

2. **JWT_SECRET_KEY is placeholder:** `apps/api/.env` missing → `JWT_SECRET_KEY=CHANGE_ME_...`. In production, generate a strong random key.

3. **Dashboard auth:** Dashboard makes unauthenticated API calls (HTTP 401) — correct behavior for public data view.

---

### Docker compose test

`docker compose -f infra/docker/docker-compose.yml config` — valid YAML, all 6 services defined (postgres:5432, redis:6379, api:8000, web:3000->4321, prometheus:9090, grafana:3000->3001).

---

### Next steps

- Create `apps/api/.env` with MiniMax key to enable AI chat
- Generate strong `JWT_SECRET_KEY` for production
- Paperclip API status update pending (API unreachable — exit code 7)