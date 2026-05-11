# Fly.io Deployment Guide — CCEC Climate Platform

## Overview

CCEC Climate Platform deploys to Fly.io with two apps:
- **`ccec-api`** — FastAPI backend (port 8000)
- **`ccec-web`** — Astro static frontend (port 4321, served via `npx serve`)

Both apps run in Hong Kong (`hkg`) region for low latency across Asia.

## Prerequisites

1. **Fly.io account** at [fly.io](https://fly.io)
2. **`flyctl` CLI** installed:
   ```bash
   # Windows (PowerShell)
   iwr https://fly.io/install.ps1 -UseBasicParsing | iex

   # macOS/Linux
   curl -L https://fly.io/install.sh | sh
   ```
3. **`fly.toml` files** present in `infra/fly/` (already configured)

## One-Time Setup

### 1. Login to Fly.io

```bash
flyctl auth login
```

### 2. Create the apps (first time only)

```bash
# Create API app
flyctl apps create ccec-api --org personal

# Create Web app
flyctl apps create ccec-web --org personal
```

### 3. Allocate a persistent volume for API data

```bash
flyctl volumes create ccec_data --region hkg --size 1
```

### 4. Add secrets for API

```bash
# Required secrets — set these before first deploy
flyctl secrets set DATABASE_URL="postgresql://postgres:YOUR_PASSWORD@YOUR_FLY_HOST.internal:5432/ccec" --app ccec-api
flyctl secrets set JWT_SECRET="your-super-secret-jwt-key-min-32-chars" --app ccec-api
flyctl secrets set GROQ_API_KEY="gsk_YOUR_KEY" --app ccec-api
flyctl secrets set DEEPSEEK_API_KEY="sk-YOUR_KEY" --app ccec-api
flyctl secrets set PORTKEY_API_KEY="YOUR_KEY" --app ccec-api

# Optional
flyctl secrets set REDIS_URL="redis://YOUR_REDIS_INTERNAL:6379" --app ccec-api
```

### 5. Provision Fly Postgres (for production DB)

```bash
# Launch a dedicated Postgres app
flyctl postgres create ccec-db --region hkg

# Attach it to the API app
flyctl postgres attach ccec-db --app ccec-api
```

### 6. Set fly.toml app names

In `infra/fly/fly.toml.api` and `infra/fly/fly.toml.web`, confirm the `app` field matches the created apps:
```toml
app = "ccec-api"   # infra/fly/fly.toml.api
app = "ccec-web"   # infra/fly/fly.toml.web
```

## Manual Deploy

### Deploy API
```bash
flyctl deploy --config infra/fly/fly.toml.api --image ghcr.io/YOUR_ORG/ccec-climate-platform/api:HASH
```

### Deploy Web
```bash
flyctl deploy --config infra/fly/fly.toml.web --image ghcr.io/YOUR_ORG/ccec-climate-platform/web:HASH
```

### Check status
```bash
flyctl status --app ccec-api
flyctl status --app ccec-web

# View logs
flyctl logs --app ccec-api
flyctl logs --app ccec-web
```

### Open browser
```bash
flyctl open --app ccec-web
```

## CI/CD (GitHub Actions)

Set these **GitHub Secrets** in your repo (`Settings → Secrets and variables → Actions`):

| Secret | Value |
|--------|-------|
| `FLY_API_TOKEN` | Fly.io API token from `flyctl auth token` |
| `GROQ_API_KEY` | Groq API key |
| `DEEPSEEK_API_KEY` | DeepSeek API key |
| `PORTKEY_API_KEY` | PortKey API key |
| `JWT_SECRET` | JWT signing secret (min 32 chars) |
| `DATABASE_URL` | PostgreSQL connection string |

The workflow (`.github/workflows/deploy.yml`) handles deploys automatically on push to `main`:
1. Lint & build
2. Push Docker images to GHCR
3. Deploy to Fly.io via `flyctl deploy`

## Architecture Notes

- **Web** is served as static files via `npx serve dist -l 4321`
- **API** connects to Fly Postgres via internal DNS (`ccec-db.internal`)
- Both apps use Fly's built-in load balancer with HTTPS termination
- Volume mount `/data` on API for session/uploads persistence
- `auto_rollback = true` reverts to previous release on failed health check

## Troubleshooting

```bash
# SSH into running container
flyctl ssh issue --app ccec-api

# Check secrets
flyctl secrets list --app ccec-api

# Scale VMs
flyctl scale count 2 --app ccec-api

# View metrics
flyctl metrics --app ccec-api

# Rollback to previous release
flyctl deploy --config infra/fly/fly.toml.api --image previous --strategy immediate
```