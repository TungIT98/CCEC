# MAR-859 — ESG + GHG Calculator + Report Generation

**Owner:** elixir-dev (`32bacd3a-700b-40b9-af38-e4a2bb14b009`)
**Parent:** MAR-855
**File:** `E:\ccec-climate-platform\logs\MAR-859-ESG.md`

## Status

`todo` — Waiting on MAR-856 (backend API for data infra).

## Scope

### 1. GHG Protocol Calculator

**File to create:** `apps/api/services/ghg_calculator.py`

**Schema (Pydantic):**

```python
class GhgCalcScope1Input(BaseModel):
    """Direct emissions — Scope 1."""
    fuel_type: Literal["natural_gas", "diesel", "gasoline", "lpg", "coal", "biomass"]
    quantity_tCO2e: float  # Tonnes CO2e directly emitted
    source_type: Literal["stationary_combustion", "mobile_comustion", "fugitive", "process"]


class GhgCalcScope2Input(BaseModel):
    """Indirect emissions from purchased electricity — Scope 2."""
    electricity_kwh: float
    market_type: Literal["location_based", "market_based"]  # grid factor vs REC


class GhgCalcScope3Input(BaseModel):
    """Value chain — Scope 3."""
    category: Literal["purchased_goods", "capital_goods", "fuel_and_energy", "upstream_transportation", "waste_disposed"]
    quantity_tCO2e: float
    source: Literal["category1_purchased_goods", "category2_capital_goods", "category3_fuel_energy", "category4_upstream", "category9_waste"]


class GhgCalcRequest(BaseModel):
    user_id: int
    scope1: list[GhgCalcScope1Input] | None
    scope2: list[GhgCalcScope2Input] | None
    scope3: list[GhgCalcScope3Input] | None


class GhgCalcResponse(BaseModel):
    user_id: int
    scope1_total_tCO2e: float
    scope2_total_tCO2e: float
    scope3_total_tCO2e: float
    grand_total_tCO2e: float
    method: Literal["GHG Protocol", "ISO14064"]
    calculated_at: datetime
```

**Endpoint:**
| Method | Path | Description |
|---|---|---|
| POST | `/api/v1/emissions/ghg` | Body: GhgCalcRequest → GhgCalcResponse |

**GHG Factor DB (add to `knowledge/climate/ghg_factors.json`):**
```json
{
  "stationary_combustion": {
    "natural_gas": 2.0,  # tCO2e per MMBtu
    "diesel": 10.2,
    "gasoline": 8.9,
    "lpg": 6.1,
    "coal": 9.7
  }
}
```
(Note: factor DB loaded into memory on startup, no DB required)

---

### 2. ESG Scoring Engine Enhancement

**File to enhance:** `apps/api/services/esg.py` (already exists per MAR-854)

**Changes:**

| Enhancement | Description |
|---|---|
| GRI framework | GRI-405 Diversity, GRI-302 Energy, GRI-305 Emissions |
| SASB framework | EU-En1200 Energy Management, HY-HY100 Greenhouse Gas Emissions |
| TCFD framework | Climate risk scenario analysis (2°C pathway) |
| Peer benchmarking | Compare ES score against Vietnam peers (FMCG, steel, cement) |
| Data normalization | Min-max normalization across ESG metrics |

**Note:** MAR-854 DB tables (`esg_metrics`) already exist. Add scoring algo on top.

---

### 3. Report Generation

**File to create:** `apps/api/services/report_generator.py`

**Schemas:**

```python
class ReportRequest(BaseModel):
    user_id: int
    report_type: Literal["GHG Protocol", "GRI", "TCFD", "NDC_Summary"]
    scope: list[Literal["scope1", "scope2", "scope3"]]
    period_start: date
    period_end: date


class ReportResponse(BaseModel):
    report_id: int
    user_id: int
    report_type: Literal["GHG Protocol", "GRI", "TCFD", "NDC_Summary"]
    file_url: str  # Pre-signed S3 or internal path
    generated_at: datetime
```

**Endpoints:**

| Method | Path | Description |
|---|---|---|
| GET | `/api/v1/reports/emissions/{user_id}` | Paginated list of generated reports |
| POST | `/api/v1/reports/generate` | Body: ReportRequest → async PDF generation |
| GET | `/api/v1/reports/{report_id}/download` | Pre-signed URL or file stream |

**Backend (FastAPI):** Background task using `BackgroundTasks`:
1. Accept POST `/api/v1/reports/generate`
2. Return `report_id` immediately
3. Trigger `generate_pdf_task(report_id)` in background
4. Store file to `data/reports/{report_id}.pdf`

**Frontend (`apps/web/src/pages/esg.astro` already exists — enhance):**

| Component | Description |
|---|---|
| `apps/web/src/components/esg/GhgCalculator.svelte` | GHG form UI — Scope 1/2/3 tabs |
| `apps/web/src/components/esg/GhgCalculator.svelte` | GHG form fields: fuel type, quantity, method |

**api.ts helper:**

```typescript
export const calculateGHG = (body) => api.post('/v1/emissions/ghg', body)
export const getReports = (userId) => api.get(`/v1/reports/emissions/${userId}`)
export const generateReport = (body) => api.post('/v1/reports/generate', body)
export const downloadReport = (reportId) => api.get(`/v1/reports/${reportId}/download`)
```

---

## Depends

`MAR-854` — Existing DB tables (`emissions_records`, `esg_metrics`) for MAR-859.

`MAR-856` — Backend data infra (data ingestion for GHG factors).

`frontend-dev MAR-857` — `GhgCalculator.svelte` frontend component (depends on backend).

---

## Output Checklist

- [ ] `apps/api/services/ghg_calculator.py` — Scope 1/2/3 calculator
- [ ] `apps/api/routers/emissions.py` — GHGP endpoint (already exists per spec, enhance)
- [ ] `apps/api/services/esg.py` — enhanced scoring GRI/SASB/TCFD
- [ ] `apps/api/services/report_generator.py` — PDF branded GRI/TCFD/GHG
- [ ] `apps/api/routers/reports.py` — 3 report endpoints (auth + Pydantic + rate limit)
- [ ] `knowledge/climate/ghg_factors.json` — emission factor DB
- [ ] `apps/web/src/components/esg/GhgCalculator.svelte` — GHG form UI
- [ ] `apps/web/src/lib/api.ts` — add GHG + report helpers