# ============================================================
# Coolify Deployment Guide — CCEC Climate Platform
# ============================================================

## Overview

This platform deploys to a single Coolify server as a monorepo with 4 services:
- **API**: FastAPI backend (port 8000)
- **Web**: Astro frontend (port 4321)
- **Database**: PostgreSQL 16 + PostGIS (port 5432)
- **Cache**: Redis 7.2 (port 6379)

---

## Option A: Docker Compose (Recommended for single-server)

### Step 1 — Create Coolify Application

1. In Coolify dashboard → **New Application**
2. Name: `ccec-climate-platform`
3. Git repo: `<your-git-repo-url>`
4. Build pack: **Dockerfile**

### Step 2 — Add Services

Add these as **Persistent Services** (runs independently, not rebuilt):

#### PostgreSQL
```
Image: postgis/postgis:16-3.4
Ports: 5432
Environment:
  POSTGRES_PASSWORD: <strong-password>
  POSTGRES_DB: ccec
Volumes:
  - ccec_pgdata:/var/lib/postgresql/data
```

#### Redis
```
Image: redis:7.2-alpine
Ports: 6379
Volumes:
  - ccec_redisdata:/data
Command: redis-server --appendonly yes
```

### Step 3 — Deploy API

1. Add a **New Service** linked to the repo
2. Name: `ccec-api`
3. Port: `8000`
4. Dockerfile: `infra/docker/Dockerfile.api`
5. Pre-deploy: `cd apps/api && pip install -r requirements.txt`
6. Environment variables (from `.env.example`):
   - `DATABASE_URL`: `postgresql+asyncpg://postgres:<pwd>@ccec-postgres:5432/ccec`
   - `DATABASE_URL_SYNC`: `postgresql+psycopg2://postgres:<pwd>@ccec-postgres:5432/ccec`
   - `REDIS_URL`: `redis://ccec-redis:6379/0`
   - `JWT_SECRET_KEY`: `<32+-char-random-key>`
   - `OPENAI_API_KEY`: `<groq-key>`
   - `DEBUG`: `false`

### Step 4 — Deploy Web

1. Add a **New Service**
2. Name: `ccec-web`
3. Port: `4321`
4. Build command: `pnpm install --frozen-lockfile && pnpm build:web`
5. Dockerfile: `infra/docker/Dockerfile.web`
6. Environment:
   - `PUBLIC_API_URL`: `https://api.ccec.example.com` (your domain)
   - `HOST`: `0.0.0.0`
   - `PORT`: `4321`

### Step 5 — Domain Configuration

In Coolify → Service → **Domains**:

| Service | Domain | Type |
|---------|--------|------|
| `ccec-web` | `ccec.example.com` | Production |
| `ccec-api` | `api.ccec.example.com` | Production |

Enable **SSL** (Let's Encrypt) for both domains.

---

## Option B: Docker Compose via Coolify (Docker Compose v2)

If Coolify supports docker-compose, deploy with:

```yaml
# infra/docker/docker-compose.yml
version: "3.9"
services:
  postgres:
    image: postgis/postgis:16-3.4
    ...
  redis:
    image: redis:7.2-alpine
    ...
  api:
    build: ../../  # repo root
    dockerfile: infra/docker/Dockerfile.api
    ...
```

Point Coolify to `infra/docker/docker-compose.yml` as the compose file path.

---

## Environment Variables Reference

Copy from `.env.example` — at minimum:

```bash
# Required
DATABASE_URL=postgresql+asyncpg://postgres:<pwd>@<host>:5432/ccec
JWT_SECRET_KEY=<32+ random chars>
OPENAI_API_KEY=<groq-key>

# Optional (set in production)
MAPBOX_ACCESS_TOKEN=<mapbox-token>
DEEPSEEK_API_KEY=<deepseek-key>
PORTKEY_API_KEY=<portkey-key>

# Monitoring (Prometheus/Grafana auto-configured via docker-compose)
# See infra/docker/docker-compose.yml for full stack
```

---

## Health Checks

| Endpoint | Expected Response | Use |
|----------|------------------|-----|
| `GET /health` | `{"status":"ok"}` | Load balancer health check |
| `GET /metrics` | Prometheus metrics | Prometheus scrape target |
| `GET /docs` | Swagger UI | API documentation |

## Post-Deploy Verification

```bash
# Check API health
curl https://api.ccec.example.com/health

# Check Prometheus metrics
curl https://api.ccec.example.com/metrics

# Check frontend
curl https://ccec.example.com
```

## Performance Baselines (record after deploy)

| Metric | Target |
|--------|--------|
| API p95 latency | < 200ms |
| Time to First Byte (frontend) | < 1.5s |
| Uptime | > 99.5% |
| Error rate (5xx) | < 0.5% |