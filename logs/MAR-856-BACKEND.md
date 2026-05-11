# MAR-856 — Backend (Carbon + Energy + Policies)

**Owner:** elixir-dev (`32bacd3a-700b-40b9-af38-e4a2bb14b009`)
**Parent:** MAR-855
**File:** `E:\ccec-climate-platform\logs\MAR-856-BACKEND.md`

## Status

`todo` — Ready to assign.

## Scope

### 1. Carbon Credits (Module 2 — ~8%)

**Files to create:**

| File | Entity/Schema |
|---|---|
| `apps/api/models/carbon_credit.py` | CarbonCredit: id, name, standard_type (VER/CER/Gold), project_type, vintage, unit_price, currency, registry, project_url, credit_class, methodology, estimated_ERt, verified_ERt, issued_at, expired_at, is_retired, created_at |
| `apps/api/models/carbon_price.py` | CarbonPrice: id, standard_type, vintage, price_per_tCO2e, currency, source_url, fetched_at |
| `apps/api/schemas/carbon_credit.py` | Pydantic: CarbonCreditResponse, CarbonPriceHistoryResponse |
| `apps/api/schemas/carbon_price.py` | Pydantic: CarbonPriceResponse |

**Router (new):** `apps/api/routers/carbon_credits.py`

| Method | Path | Description |
|---|---|---|
| GET | `/api/v1/carbon-credits` | Paginated, filterable (standard, vintage, project_type, unit_price_min/max, country_code, vintage_min/max) |
| GET | `/api/v1/carbon-credits/{id}` | Credit detail |
| GET | `/api/v1/carbon-prices` | Current prices (standard, vintage) |
| GET | `/api/v1/carbon-prices/history` | Historical (after=ISO date, limit=50) |

**Migrations:**
```bash
alembic revision --autogenerate -m "add carbon credits"
```

---

### 2. Renewable Energy Tracking (Module 4 — ~8%)

**Files to create:**

| File | Entity/Schema |
|---|---|
| `apps/api/models/renewable_energy.py` | RenewableEnergy: id, country_name, country_code (ISO 3166-1), energy_type (solar/wind/hydro/geothermal/biomass), capacity_mw, generation_gwh, installed_year, source, fetched_at |
| `apps/api/schemas/renewable_energy.py` | Pydantic: RenewableEnergyResponse, CapacityResponse, TrendsResponse |

**Router (new):** `apps/api/routers/energy.py`

| Method | Path | Description |
|---|---|---|
| GET | `/api/v1/energy/renewable` | Filtered by country_code, energy_type (query params) |
| GET | `/api/v1/energy/capacity` | Global capacity data |
| GET | `/api/v1/energy/trends` | Generation trends |
| GET | `/api/v1/energy/country/{code}` | Country detail |

**Migrations:**
```bash
alembic revision --autogenerate -m "add renewable energy"
```

---

### 3. Climate Policy Analysis (Module 5 — ~6%)

**Files to create:**

| File | Entity/Schema |
|---|---|
| `apps/api/models/policy.py` | Policy: id, country_name, country_code, policy_name, policy_type, instrument_type, sector, coverage, economy_wide, carbon_pricing_existence, pricing_notes, carbon_price_min_tCO2e, carbon_price_max_tCO2e, currency, link_source, fetched_at |
| `apps/api/models/ndc_tracking.py` | NdcTracking: id, country_name, country_code, submission_type, status, latest_submission_date, link_NDC, fetch_link, fetched_at |
| `apps/api/schemas/policy.py` | Pydantic: PolicyResponse, NdcTrackingResponse |
| `apps/api/schemas/ndc_tracking.py` | Pydantic: NdcResponse |

**Router (new):** `apps/api/routers/policies.py`

| Method | Path | Description |
|---|---|---|
| GET | `/api/v1/policies` | Paginated, filterable (country_code, policy_type, sector) |
| GET | `/api/v1/policies/ndc` | NDC tracking |
| GET | `/api/v1/policies/country/{code}` | Country policies |
| GET | `/api/v1/policies/{id}` | Policy detail |

**Migrations:**
```bash
alembic revision --autogenerate -m "add policies ndc"
```

---

## Standards

- All router functions: auth (JWT Bearer) + Pydantic input validation + rate limiting per-route
- No hardcoded secrets — use `os.getenv`
- OWASP: A01 Broken Access Control, A03 Injection, A07 Auth Session Failures
- Register new routers in `apps/api/main.py`

## Dependencies

`MAR-857` (frontend): blocked until MAR-856 API ready.

---

## Output Checklist

- [ ] `apps/api/models/carbon_credit.py` + `carbon_price.py` + schemas
- [ ] `apps/api/models/renewable_energy.py` + schema
- [ ] `apps/api/models/policy.py` + `ndc_tracking.py` + schemas
- [ ] `apps/api/routers/carbon_credits.py` — 4 endpoints (auth + Pydantic + rate limit)
- [ ] `apps/api/routers/energy.py` — 4 endpoints
- [ ] `apps/api/routers/policies.py` — 4 endpoints
- [ ] Alembic migrations x3
- [ ] `apps/api/main.py` — register 3 routers
- [ ] Vitest: TypeScript tests passing for new AI client helpers (MAR-858 blocks)