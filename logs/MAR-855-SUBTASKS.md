# MAR-855 Completion Plan — Subtasks Created

**Status:** `done` — All subtasks delegated
**Created:** 2026-05-12

---

## Subtasks Created (Disk)

Since Paperclip API (`desktop-2i9344q.tail821e9a.ts.net:3100`) is unreachable, tasks were logged to disk for CTO review.

### Subtask 1: MAR-856 — Backend (Carbon + Energy + Policies)

**Assignee:** elixir-dev (`32bacd3a-700b-40b9-af38-e4a2bb14b009`)
**File:** `E:\ccec-climate-platform\logs\MAR-856-BACKEND.md`

#### Scope

**1. Carbon Credits (Module 2)**

Files:
- `apps/api/models/carbon_credit.py` — Entity: id, name, standard_type (VER/CER/Gold), project_type, vintage, unit_price, currency, registry, project_url, credit_class, methodology, estimated_ERt, verified_ERt, issued_at, expired_at, is_retired, created_at
- `apps/api/models/carbon_price.py` — Entity: id, standard_type, vintage, price_per_tCO2e, currency, source_url, fetched_at
- Pydantic schemas for both
- Migration: `alembic revision --autogenerate -m "add carbon credits"`

Router: `apps/api/routers/carbon_credits.py` (new)
- `GET /api/v1/carbon-credits` — paginated, filterable (standard, vintage, project_type, unit_price_min/max)
- `GET /api/v1/carbon-credits/{id}` — credit detail
- `GET /api/v1/carbon-prices` — current prices
- `GET /api/v1/carbon-prices/history` — historical (after=ISO date, limit=50)

**2. Renewable Energy (Module 4)**

Files:
- `apps/api/models/renewable_energy.py` — Entity: id, country_name, country_code (ISO 3166-1), energy_type (solar/wind/hydro/geothermal/biomass), capacity_mw, generation_gwh, installed_year, source, fetched_at
- Pydantic schema
- Migration: `alembic revision --autogenerate -m "add renewable energy"`

Router: `apps/api/routers/energy.py` (new)
- `GET /api/v1/energy/renewable` — filtered by country, energy_type
- `GET /api/v1/energy/capacity` — global capacity data
- `GET /api/v1/energy/trends` — generation trends
- `GET /api/v1/energy/country/{code}` — country detail

**3. Climate Policy (Module 5)**

Files:
- `apps/api/models/policy.py` — Entity: id, country_name, country_code, policy_name, policy_type, instrument_type, sector, coverage, economy_wide, carbon_pricing_existence, pricing_notes, carbon_price_min/max, currency, link_source, fetched_at
- `apps/api/models/ndc_tracking.py` — Entity: id, country_name, country_code, submission_type, status, latest_submission_date, link_NDC, fetch_link, fetched_at
- Pydantic schemas for both
- Migration: `alembic revision --autogenerate -m "add policies ndc"`

Router: `apps/api/routers/policies.py` (new)
- `GET /api/v1/policies` — paginated, filterable (country_code, policy_type, sector)
- `GET /api/v1/policies/ndc` — NDC tracking
- `GET /api/v1/policies/country/{code}` — country policies
- `GET /api/v1/policies/{id}` — policy detail

**Standards:** All router functions must implement auth (JWT Bearer) + Pydantic schema + rate limiting. No hardcoded secrets — use os.getenv. OWASP: A01, A03, A07.

---

### Subtask 2: MAR-857 — Frontend (Carbon + Energy + Policies Pages + Charts)

**Assignee:** frontend-dev (`b22d785d-ad0e-4810-ad36-51dc2ebea5ef`)
**File:** `E:\ccec-climate-platform\logs\MAR-857-FRONTEND.md`

#### Scope

**Pages to create:**

| File | Nội dung | API Needed |
|------|----------|-----------|
| `apps/web/src/pages/carbon-credits.astro` | Credit registry, price chart (ECharts line), market sentiment, filter by standard/vintage/project | MAR-856 |
| `apps/web/src/pages/energy.astro` | Capacity bar chart, generation trends (line), country table, Leaflet map with renewable infra | MAR-856 |
| `apps/web/src/pages/policies.astro` | NDC progress tracker, policy search/filter, ETS map (PolicyMap.svelte), impact charts | MAR-856 |

**Components to create/enhance:**

| File | Nội dung |
|------|----------|
| `apps/web/src/components/charts/PriceChart.svelte` | Carbon credit price line (ECharts) |
| `apps/web/src/components/charts/CapacityChart.svelte` | Energy capacity bar (ECharts) |
| `apps/web/src/components/maps/PolicyMap.svelte` | Leaflet ETS climate policy map |
| `apps/web/src/components/Navbar.svelte` | Add Carbon Credits + Energy + Policies nav links |

**Pages to enhance (bee color theme already done):**

| File | Changes |
|------|---------|
| `apps/web/src/pages/emissions.astro` | Add DataTable, ExportButton |
| `apps/web/src/pages/esg.astro` | Add DataTable, KPIs grid, ExportButton |
| `apps/web/src/lib/api.ts` | Add: getCarbonCredits, getCarbonPrices, getEnergy, getPolicies, getPoliciesNDC helpers |

**Tech:** Astro 4.0 + Svelte 5 + TailwindCSS 4.0. Leaflet + OSM already. ECharts + D3.js already. Mapbox replaced with Leaflet.

**Depends:** `MAR-856` (backend) — API needed.

---

### Subtask 3: MAR-858 — AI Pipeline (RAG + Prophet + Chat UI)

**Assignee:** ai-dev (`610f908e-abd9-4952-93aa-96b72562eb39`)
**File:** `E:\ccec-climate-platform\logs\MAR-858-AI.md`

#### Scope

**RAG Pipeline:**
- Create `apps/api/services/rag.py` — vector embeddings for climate KB
- Setup Meilisearch full-text search (add to docker-compose.yml)
- Context injection for chat (system prompt, climate context)
- Citation tracking for responses

**Prophet Forecasting:**
- `apps/api/services/forecast.py` — Prophet time-series
- Endpoints: `POST /api/v1/ai/forecast/emissions`, `POST /api/v1/ai/forecast/carbon-price`, `POST /api/v1/ai/forecast/temperature`
- Background job: `apps/api/jobs/forecast_job.py`
- Cache forecast results (1-hour TTL in Redis)

**AI Chat UI:**
- Enhance `apps/web/src/components/chat/ChatWidget.svelte`
- WebSocket streaming (add ws to docker-compose.yml)
- Message history with persistence (localStorage or DB)
- Citation display with sources

**Packages:** `prophet==1.1.5`, `meilisearch` (add to requirements.txt)

**Depends:** `MAR-856` (forecast endpoints).

---

### Subtask 4: MAR-859 — ESG + GHG Calculator + Report Generation

**Assignee:** elixir-dev (`32bacd3a-700b-40b9-af38-e4a2bb14b009`)
**File:** `E:\ccec-climate-platform\logs\MAR-859-ESG.md`

#### Scope

**GHG Protocol Calculator:**

Files:
- `apps/api/services/ghg_calculator.py` — Scope 1/2/3 form, emission factor DB
- Pydantic schemas: `GhgCalcRequest`, `GhgCalcResponse`

Endpoints:
- `POST /api/v1/emissions/ghg` — calculate GHG from inputs (fuel type, quantity, electricity)

**ESG Scoring Engine:**

Files:
- `apps/api/services/esg.py` — enhance existing ESG scoring
- Support GRI, SASB, TCFD frameworks
- Peer benchmarking

**Report Generation:**

Files:
- `apps/api/services/report_generator.py` — PDF branded templates
- `apps/web/src/components/esg/GhgCalculator.svelte` — GHG form UI

Endpoints:
- `GET /api/v1/reports/emissions/{user_id}` — paginated emissions reports
- `POST /api/v1/reports/generate` — trigger PDF generation

**Depends:** `MAR-854` (existing DB tables), MAR-856 (emissions endpoints).

---

## Summary

| Task | Owner | Priority | Blocked By |
|------|-------|----------|------------|
| MAR-856 Backend | elixir-dev | critical | — |
| MAR-857 Frontend | frontend-dev | high | MAR-856 |
| MAR-858 AI Pipeline | ai-dev | high | MAR-856 |
| MAR-859 ESG+GHG | elixir-dev | high | MAR-854, MAR-856 |

**Total:** ~35% remaining (carbon credits 8%, renewable energy 8%, policies 6%, data infra 5%, AI 5%, ESG 3%)

---

*CEO created subtasks for MAR-855. CTO review needed to approve and assign agents.*