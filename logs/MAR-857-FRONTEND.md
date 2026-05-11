# MAR-857 — Frontend Pages + Charts

**Owner:** frontend-dev (`b22d785d-ad0e-4810-ad36-51dc2ebea5ef`)
**Parent:** MAR-855
**File:** `E:\ccec-climate-platform\logs\MAR-857-FRONTEND.md`

## Status

`todo` — Waiting on MAR-856 (backend API).

## Scope

### Pages to Create

| File | Nội dung | API Endpoint |
|---|---|---|
| `apps/web/src/pages/carbon-credits.astro` | Credit registry table, ECharts price line (market sentiment), filter by standard/vintage/project_type | GET /api/v1/carbon-credits + /carbon-prices |
| `apps/web/src/pages/energy.astro` | Bar chart capacity by energy type, line trends generation, country table, Leaflet map renewable | GET /api/v1/energy/* |
| `apps/web/src/pages/policies.astro` | NDC progress tracker, policy search/filter, ETS policy map, impact charts | GET /api/v1/policies/* + /policies/ndc |

### Components to Create

| File | Description | Tech |
|---|---|---|
| `apps/web/src/components/charts/PriceChart.svelte` | ECharts line — carbon credit price history | Svelte 5 + ECharts |
| `apps/web/src/components/charts/CapacityChart.svelte` | ECharts bar — energy capacity by type | Svelte 5 + ECharts |
| `apps/web/src/components/maps/PolicyMap.svelte` | Leaflet OSM — ETS climate policy locations | Leaflet + OSM |

### Navbar Updates

In `apps/web/src/components/Navbar.svelte`, add links:
- `/carbon-credits` — Carbon Credits
- `/energy` — Energy
- `/policies` — Policies

Remove Mapbox references (already replaced with Leaflet per spec).

### lib/api.ts Updates

Add to `apps/web/src/lib/api.ts`:

```typescript
export const getCarbonCredits = (params) => api.get('/v1/carbon-credits', {params})
export const getCarbonPrices = (params) => api.get('/v1/carbon-prices', {params})
export const getCarbonPricesHistory = (params) => api.get('/v1/carbon-prices/history', {params})
export const getEnergyRenewable = (params) => api.get('/v1/energy/renewable', {params})
export const getEnergyCapacity = (params) => api.get('/v1/energy/capacity', {params})
export const getEnergyCountry = (code) => api.get(`/v1/energy/country/${code}`)
export const getPolicies = (params) => api.get('/v1/policies', {params})
export const getPoliciesNDC = () => api.get('/v1/policies/ndc')
export const getPolicy = (id) => api.get(`/v1/policies/${id}`)
export const getEnergyTrends = () => api.get('/v1/energy/trends')
```

### Enhancements to Existing Pages

| File | Changes |
|---|---|
| `apps/web/src/pages/emissions.astro` | Add DataTable (sort/filter), ExportButton CSV |
| `apps/web/src/pages/esg.astro` | Add DataTable, KPIs grid, ExportButton |
| `apps/web/src/lib/auth.ts` | Add: `logout()`, `getUser()` |

**Bee color theme already applied** (MAR-853 done). No color changes needed.

---

## Context

- AGENTS.md: `E:/ccec-climate-platform/AGENTS.md`
- Tech: Astro 4.0 + Svelte 5 + TailwindCSS 4.0
- Leaflet + OSM (Mapbox already replaced)
- ECharts + D3.js already integrated
- MiniMax API: `sk-cp-JKcLn8JXdkygpTgwCS72isp9Zz7AswQeFdh5uKnvk0vngQHaLa6NVBOwSZ8v6xZybbPM3ck-L1UmOYff7EsliddMUK4Hk-za3N0-wUWse_Nsj--6J_n9XPw`

---

## Depends

`MAR-856` (backend) — API endpoints required.