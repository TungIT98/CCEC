# MAR-854: Missing DB tables + AI client not climate-domain aligned — DONE

**Date:** 2026-05-11
**Status:** DONE (Paperclip API unreachable — on disk only)
**CTO Review:** ✅ APPROVED 2026-05-12 (CTO agent 44928386-bda4-4322-a168-472dc9902b1e)
**API Status Update:** Failed — connection refused `desktop-2i9344q.tail821e9a.ts.net:3100` (2026-05-12)

## Deliverables

### 1. DB Tables (apps/api/models/entities.py + schemas.py)

| Table | Purpose | Key Columns |
|---|---|---|
| `emissions_records` | GHG emissions tracking | scope (1/2/3), gas_type, co2e_tonnage, sector, reporting_year |
| `esg_metrics` | ESG scores + KPIs | category (E/S/G), metric_name, value, score (0–100), reporting_period |
| `alerts` | Threshold-based climate alerts | metric, operator, threshold_value, actual_value, is_resolved |
| `audit_logs` | Immutable compliance log | action, entity_type, entity_id, changes (JSON), ip_address |

- SQLAlchemy entities use existing `Base` from `database.py`
- Pydantic schemas: `from_attributes=True`, `Optional` fields, numeric constraints
- Matches existing column patterns (id, timestamps, indexes)

### 2. AI Client Climate-Domain (packages/ai-client/src/)

**models.ts additions:**
- `VIETNAM_CLIMATE_CONTEXT` — system prompt with NDC targets, typhoon risks, monsoon patterns, net-zero 2050, data sources, unit conventions, Vietnamese-language preference
- `CLIMATE_TOOLS` — 4 tool definitions: `get_emissions`, `get_esg_score`, `get_forecast`, `get_climate_alerts`

**index.ts additions:**
- `createClimateAI(options)` — factory with MiniMax primary (1M context) + Groq fast fallback
- Auto-injects `VIETNAM_CLIMATE_CONTEXT` as system message in every chat session
- Exports `CLIMATE_TOOLS`, `VIETNAM_CLIMATE_CONTEXT`, `createClimateAI`

**Verification:**
- TypeScript: `tsc --noEmit` clean (0 errors)
- Tests: 15/15 vitest passing

## Non-blocking Notes
- `ESGMertic` typo fixed → `ESGMetric` in both entities.py and schemas.py (entity class, Base, Create, Response schemas)
- Paperclip API unreachable (exit 7) — status update pending on API recovery
- Children tasks (sub-issues) could not be created via API — on disk only

## Files Changed
- `apps/api/models/entities.py` — 4 new SQLAlchemy entity classes
- `apps/api/models/schemas.py` — Pydantic schemas for all 4 tables
- `packages/ai-client/src/models.ts` — climate tools + Vietnam context
- `packages/ai-client/src/index.ts` — createClimateAI factory