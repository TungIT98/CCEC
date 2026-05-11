# MAR-858 — AI Pipeline (RAG + Prophet + Chat UI)

**Owner:** ai-dev (`610f908e-abd9-4952-93aa-96b72562eb39`)
**Parent:** MAR-855
**File:** `E:\ccec-climate-platform\logs\MAR-858-AI.md`

## Status

`todo` — Waiting on MAR-856 (backend API for forecast endpoints).

## Scope

### 1. RAG Pipeline

**Files to create:**

| File | Description |
|---|---|
| `apps/api/services/rag.py` | Vector embeddings (OpenAI-compatible embeddings or MiniMax) for climate KB documents |
| `apps/api/services/search_service.py` | Meilisearch full-text search integration |

**Requirements (add to `apps/api/requirements.txt`):**
```
meilisearch>=0.28.0
sentence-transformers>=2.0.0
```
(Note: Meilisearch added to `docker-compose.yml` by devops-dev)

**Endpoints:**
- `GET /api/v1/ai/search?q=query` — semantic climate search (Meilisearch)
- Context injection in `/api/v1/chat` — inject retrieved KB chunks

**Steps:**
1. Index climate KB documents (from `knowledge/climate/`) with embeddings
2. Setup Meilisearch index: `climate_kb`
3. Implement `/api/v1/ai/search` — retrieve top-k chunks + inject as context
4. Citation tracking — mark which KB chunk sourced which chat response

---

### 2. Prophet Forecasting

**File to create:** `apps/api/services/forecast.py`

```python
# prophet==1.1.5 required
from prophet import Prophet
import pandas as pd

def forecast_emissions(country_code, horizon_days=365):
    """Time-series forecast for emissions."""

def forecast_carbon_price(standard_type, vintage, horizon_days=90):
    """Carbon credit price forecast."""

def forecast_temperature(station_id, horizon_days=365):
    """Temperature forecast for climate zone."""
```

**Requirements (add to `apps/api/requirements.txt`):**
```
prophet==1.1.5
holidays>=0.25
```

**Endpoints:**
| Method | Path | Description |
|---|---|---|
| POST | `/api/v1/ai/forecast/emissions` | Body: `{country_code, horizon_days}` → forecast JSON |
| POST | `/api/v1/ai/forecast/carbon-price` | Body: `{standard_type, vintage, horizon_days}` → forecast JSON |
| POST | `/api/v1/ai/forecast/temperature` | Body: `{station_id, horizon_days}` → forecast JSON |

**Background Job:** `apps/api/jobs/forecast_job.py` — run daily forecasts, cache in Redis (1-hour TTL).

---

### 3. AI Chat UI Enhancement

**File to enhance:** `apps/web/src/components/chat/ChatWidget.svelte`

**Changes:**

| Change | Description |
|---|---|
| WebSocket | Add ws:// to docker-compose.yml; stream AI responses character-by-character |
| Message history | Persist to `localStorage` key `ccec_chat_history`; load on mount |
| Citations | Display inline `[source]` with tooltip showing KB chunk |
| Typing indicator | Show "..." while AI is generating response |

**API helper (add to `packages/ai-client/src/`):**

```typescript
// Streaming via fetch
export const streamChat = (messages, onChunk) => api.postStream('/v1/chat/stream', {messages}, onChunk)
```

---

## Context

- MiniMax API (primary): `sk-cp-JKcLn8JXdkygpTgwCS72isp9Zz7AswQeFdh5uKnvk0vngQHaLa6NVBOwSZ8v6xZybbPM3ck-L1UmOYff7EsliddMUK4Hk-za3N0-wUWse_Nsj--6J_n9XPw`
- AI Client: `packages/ai-client/src/` — Groq/DeepSeek/Claude
- Tech: FastAPI Python 3.12, PostgreSQL 16 + PostGIS + TimescaleDB, Redis 7.2
- Prophet: `prophet==1.1.5`

---

## Depends

`MAR-856` (backend) — Endpoints `/api/v1/ai/forecast/*` required.

Also:
- `MAR-854` — DB tables (emissions_records, esg_metrics) for Prophet training data
- devops-dev: Meilisearch added to docker-compose.yml

---

## Output Checklist

- [ ] `apps/api/services/rag.py` — RAG pipeline
- [ ] `apps/api/services/forecast.py` — Prophet forecasting
- [ ] `apps/api/routers/forecast.py` — 3 forecast endpoints (auth + Pydantic + rate limit)
- [ ] `apps/api/jobs/forecast_job.py` — background daily job
- [ ] `apps/web/src/components/chat/ChatWidget.svelte` — enhanced with streaming/history/citations
- [ ] `requirements.txt` — updated with `prophet`, `meilisearch`, `sentence-transformers`
- [ ] TypeScript tests: vitest passing for new AI helpers