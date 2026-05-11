# CCEC Climate Platform — 24-Hour Sprint Kickoff

## Sprint Metadata
- **Issue:** MAR-834
- **Start:** 2026-05-11
- **Deadline:** 2026-05-12 (24 hours)
- **Goal:** Phase 1 foundation + Phase 2 data infrastructure + Phase 3 AI client — operational
- **Board:** CCEC Climate Platform

---

## Sprint Strategy

### What's Achievable in 24h (with 4 agents working in parallel)

| Phase | Scope | Hours | Owner |
|-------|-------|-------|-------|
| 0 – Pre-flight | Repo structure, Docker Compose, secrets | 0–3h | devops-dev |
| 1A – Backend Scaffolding | FastAPI + SQLAlchemy + migrations + auth | 2–8h | elixir-dev |
| 1B – Frontend Scaffolding | Astro + Svelte + TailwindCSS 4 + landing | 2–8h | frontend-dev |
| 2A – Database Setup | PostgreSQL/PostGIS/TimescaleDB tables | 4–10h | devops-dev |
| 2B – AI Client | OpenAI-compatible TypeScript client | 4–10h | ai-dev |
| 3 – Integration Smoke Test | API + DB + frontend connecting | 10–18h | All |
| 4 – Docker Images | Dockerfile.api + Dockerfile.web | 14–20h | devops-dev |
| 5 – Documentation + Review | README, AGENTS.md update, final PR | 18–24h | All |

### Critical Path
```
devops-dev: Docker Compose → elixir-dev: FastAPI → frontend-dev: Connect
              ↓
          devops-dev: PostgreSQL/Redis → elixir-dev: DB models → ai-dev: AI client
```

---

## 24-Hour Timeline

### Hour 0–3: PRE-FLIGHT (devops-dev leads, all stand by)
- [ ] Create monorepo structure (`apps/`, `packages/`, `infra/`, `data/`, `logs/`, `temp/`)
- [ ] Create `pnpm-workspace.yaml` and root `package.json`
- [ ] Create `tsconfig.json`, `turbo.json`
- [ ] Create `.env.example` with all required env vars
- [ ] Create `infra/docker/docker-compose.yml` (PostgreSQL 16, Redis 7.2, TimescaleDB)
- [ ] Create `infra/docker/Dockerfile.api` (Python 3.12, FastAPI, uv)
- [ ] Create `infra/docker/Dockerfile.web` (Node 20, Astro)
- [ ] Initialize git repo, create `.gitignore`
- [ ] Create `infra/docker/README.md` with startup instructions
- **Deliverable:** Monorepo skeleton ready for `docker compose up`

### Hour 2–8: PHASE 1A — Backend (elixir-dev)
- [ ] Create `apps/api/` with FastAPI structure
- [ ] `main.py` — FastAPI app with CORS, health check
- [ ] `app/core/config.py` — settings from env
- [ ] `app/core/security.py` — JWT auth (HS256, 15min access + refresh)
- [ ] `app/db/base.py` — SQLAlchemy Base
- [ ] `app/db/session.py` — DB session factory
- [ ] Models: `countries`, `emissions`, `carbon_credits`, `esg_data`, `renewable_energy`, `policies`, `users`, `api_keys`
- [ ] `app/schemas/` — Pydantic schemas for all models
- [ ] `app/api/v1/router.py` + endpoints: `/auth/register`, `/auth/login`, `/auth/refresh`
- [ ] `app/api/v1/endpoints/emissions.py` — CRUD + filters
- [ ] `app/api/v1/endpoints/carbon_credits.py`
- [ ] `app/api/v1/endpoints/esg.py`
- [ ] `app/api/v1/endpoints/energy.py`
- [ ] `app/api/v1/endpoints/policies.py`
- [ ] `app/api/v1/endpoints/ai.py` — `/chat`, `/forecast`, `/analyze`
- [ ] `app/core/rate_limit.py` — Redis-backed rate limiter
- [ ] `requirements.txt` — all Python deps
- [ ] `alembic.ini` + migrations for all tables
- **Deliverable:** `apps/api/` runs with `uvicorn`, connects to PostgreSQL, auth works

### Hour 2–8: PHASE 1B — Frontend (frontend-dev)
- [ ] `apps/web/` — `npm create astro@latest` with Svelte integration
- [ ] `tailwind.config.mjs` — TailwindCSS 4.0 setup
- [ ] `astro.config.mjs` — Astro + Svelte + Mapbox + ECharts integrations
- [ ] `src/layouts/Layout.astro` — base layout with dark/light mode toggle
- [ ] `src/pages/index.astro` — landing page (hero, features, CTA)
- [ ] `src/pages/dashboard.astro` — placeholder dashboard
- [ ] `src/pages/emissions.astro` — placeholder emissions page
- [ ] `src/pages/esg.astro` — placeholder ESG page
- [ ] `src/pages/api-docs.astro` — Swagger UI link
- [ ] `src/components/ui/` — Button, Card, Badge components
- [ ] `src/components/chat/ChatWidget.svelte` — AI chat widget (UI only, wire later)
- [ ] `public/favicon.svg` — CCEC logo placeholder
- **Deliverable:** `apps/web/` builds with `astro build`, landing page renders

### Hour 4–10: PHASE 2A — Database (devops-dev + elixir-dev)
- [ ] Start TimescaleDB, create hypertable for `emissions` (partitioned by time)
- [ ] Create continuous aggregate views for monthly/yearly emissions rollups
- [ ] Create indexes on `country_code`, `sector`, `gas_type`, `year`
- [ ] Seed `countries` table with basic ISO country list (top 50 emitters)
- [ ] Seed sample `emissions` data (2015-2024, top 10 countries, 5 sectors)
- [ ] Verify queries: emissions by country, by sector, by gas, trend lines
- **Deliverable:** `SELECT * FROM emissions LIMIT 10` returns data

### Hour 4–10: PHASE 2B — AI Client (ai-dev)
- [ ] Create `packages/ai-client/package.json` (TypeScript, ESM)
- [ ] `src/index.ts` — main export
- [ ] `src/groq.ts` — Groq API client (mixtral-8x7b-32768, llama-3.3-70b-versatile)
- [ ] `src/deepseek.ts` — DeepSeek V3 fallback client
- [ ] `src/portkey.ts` — PortKey + Claude Opus 4.6 routing
- [ ] `src/types.ts` — shared request/response types
- [ ] `src/errors.ts` — custom error classes (RateLimitError, ModelError, etc.)
- [ ] `src/metrics.ts` — token usage tracking
- [ ] `packages/shared/package.json` — `src/types.ts` with shared types
- [ ] TypeScript config, build script
- **Deliverable:** `packages/ai-client/` compiles to JS, Groq chat works

### Hour 10–18: PHASE 3 — Integration (all agents)
- [ ] frontend-dev: Wire landing page → `/api/v1/emissions` for demo data
- [ ] frontend-dev: Wire `ChatWidget.svelte` → `POST /api/v1/ai/chat` (mock if AI not ready)
- [ ] elixir-dev: Add OpenAPI/Swagger docs to FastAPI
- [ ] elixir-dev: Add `/api/v1/emissions/trends` time-series endpoint
- [ ] devops-dev: Full `docker compose up` test — all services start
- [ ] devops-dev: Health check endpoint at `/health`
- [ ] ai-dev: Connect AI client to FastAPI `/ai/chat` endpoint
- [ ] All: Smoke test — API responds, DB connected, frontend loads
- **Deliverable:** End-to-end demo: landing page → API → DB → Chart

### Hour 14–20: PHASE 4 — Docker & Deploy (devops-dev)
- [ ] Multi-stage `Dockerfile.api` (builder + runtime)
- [ ] Multi-stage `Dockerfile.web` (builder + runtime)
- [ ] `infra/docker/docker-compose.yml` — all services with healthchecks
- [ ] `infra/coolify/docker-compose.yml` — Coolify-ready config
- [ ] `scripts/start-dev.sh` — `docker compose` shortcut
- [ ] `scripts/start-prod.sh` — production startup
- [ ] Test `docker build` for both images
- **Deliverable:** `docker compose up` launches full stack locally

### Hour 18–24: PHASE 5 — Polish & Handoff
- [ ] Update `README.md` with setup instructions, env vars, API docs link
- [ ] Update `AGENTS.md` with completed items checked off
- [ ] Add demo GIF/screenshot to README
- [ ] Final code review — no hardcoded secrets, no TODOs in prod code
- [ ] Git commit all work with descriptive messages
- [ ] Post sprint summary to board
- **Deliverable:** Production-ready monorepo committed to git

---

## Agent Assignments

| Agent | Primary | Secondary |
|-------|---------|-----------|
| **devops-dev** | Pre-flight (H0-3), Docker Compose (H4-14), DB setup (H4-10) | Coolify config |
| **elixir-dev** | FastAPI backend (H2-8), API endpoints (H10-18) | DB migrations |
| **frontend-dev** | Astro scaffold (H2-8), Landing page (H10-14) | Chat widget, charts |
| **ai-dev** | AI client (H4-10), AI endpoint wiring (H14-18) | Prophet scaffold |

---

## Success Criteria (24h)
- [ ] `docker compose -f infra/docker/docker-compose.yml up` runs without error
- [ ] `curl http://localhost:8000/health` returns `{"status":"ok"}`
- [ ] `curl http://localhost:8000/api/v1/emissions?country=USA` returns JSON
- [ ] `curl http://localhost:3000` serves the landing page
- [ ] `pnpm --filter @ccec/ai-client build` succeeds
- [ ] No hardcoded secrets in source code
- [ ] All work committed to git

---

## Dependency Graph
```
[PRE-FLIGHT] ──────────────────────────────────────────────► [DOCKER IMAGES]
     │                                                              │
     ├──► [FASTAPI BACKEND] ─────────────────────────────► [INTEGRATION]
     │           │                                              │
     ├──► [DB SETUP] ────────────────────────────────► [API ENDPOINTS]
     │                                                       │
[ASTRO FRONTEND] ────────────────────────────────────► [INTEGRATION]
                                                              │
[AI CLIENT] ──────────────────────────────────────────► [AI ENDPOINT]
                                                              │
                                              ┌───────────▼──────────┐
                                              │  SMOKE TEST + REVIEW  │
                                              └──────────────────────┘
```

---

*Version: 1.0 | Created: 2026-05-11*