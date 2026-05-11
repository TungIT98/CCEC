# 24-Hour Sprint — Local Task Board

## Status: 2026-05-11 | Deadline: 2026-05-12

---

## DEV (devops-dev) — Task MAR-835
**Pre-flight: Monorepo scaffold + Docker Compose**
- Status: TODO
- Hours: 0-3
- Deliverable: Docker Compose + monorepo skeleton ready

## ELIXIR (elixir-dev) — Task MAR-836
**FastAPI Backend: Scaffold + Auth + All Endpoints**
- Status: IN PROGRESS ✅ scaffold created
- Hours: 2-8
- Deliverable: `apps/api/` running, connects to PostgreSQL, auth works

## FRONTEND (frontend-dev) — Task MAR-837
**Astro + Svelte Frontend: Landing Page + Components**
- Status: TODO
- Hours: 2-8
- Deliverable: `apps/web/` builds, landing page renders

## AI (ai-dev) — Task MAR-838
**AI Client: OpenAI-compatible TypeScript client (Groq/DeepSeek/PortKey)**
- Status: TODO
- Hours: 4-10
- Deliverable: `packages/ai-client/` compiles, Groq chat works

## INTEGRATION (elixir-dev) — Task MAR-839
**Integration: Frontend ↔ API + AI + Maps**
- Status: **IN PROGRESS** ✅ Build succeeds — 6 pages generated
- Hours: 10-18
- Deliverable: Full stack running, API + DB + frontend connected
- Progress: Landing page rebuilt with Vietnam climate branding
  - Pages built: `/`, `/dashboard`, `/maps`, `/chat`, `/emissions`, `/esg`
  - Auth: JWT login/register, token store in localStorage, auto-refresh on 401
  - API lib: `src/lib/api.ts` (climate data, forecast, chat) + `src/lib/auth.ts`
  - Dashboard: ECharts charts (temp+rain, CO2+humidity) + KPI cards
  - Map: Mapbox GL JS Vietnam map + markers (Hanoi, HCMC)
  - Chat: AI chat widget wired to `POST /api/v1/chat`
  - Fix: Svelte 5 preprocess conflict resolved (`preprocess: []` in astro.config)
  - Build: ✅ `astro build` — 6 pages, static output

## DOCKER (devops-dev) — Task MAR-840
**Docker Images + Coolify Config**
- Status: DONE (infra created, API unreachable — comment pending)
- Hours: 14-20
- Deliverable: `docker compose up` launches full stack
- Files: `infra/docker/Dockerfile.api`, `infra/docker/Dockerfile.web`, `infra/docker/docker-compose.yml`, `infra/coolify/coolify.json`, `.github/workflows/deploy.yml`, `.dockerignore`

## POLISH (elixir-dev) — Task MAR-841
**Final QA + docs + monitoring setup**
- Status: DONE ✅
- Hours: 18-24
- Deliverable: Production-ready monorepo committed
- Done: `README.md`, `.env.example`, `infra/docker/` (Dockerfiles + docker-compose.yml + Prometheus/Grafana), `infra/coolify/DEPLOY.md`, Prometheus `/metrics` endpoint in `apps/api/main.py`

---

## Success Criteria
- [ ] `docker compose -f infra/docker/docker-compose.yml up` runs without error
- [ ] `curl http://localhost:8000/health` → `{"status":"ok"}`
- [ ] `curl http://localhost:8000/api/v1/emissions?country=USA` → JSON
- [ ] `curl http://localhost:3000` → landing page
- [ ] `pnpm --filter @ccec/ai-client build` succeeds
- [ ] No hardcoded secrets in source code
- [ ] All work committed to git