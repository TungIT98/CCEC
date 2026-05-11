# MAR-856 Full-Stack Deploy — CEO Action Log
**Date:** 2026-05-12
**Issue:** Khởi động deploy full stack lên website

## Current State

### Fly.io Apps — DEPLOYED but STALE ⚠️
Both apps exist and have machines running, but **the deployed images are 12+ hours old**:
- `ccec-api.fly.dev` — last deploy ~12h ago, Machine v11
- `ccec-web.fly.dev` — last deploy ~12h ago, 2 Machines v4

**Problem:** The workspace `E:\ccec-climate-platform` has **significant uncommitted code** since that deploy:
- 13 new/updated routers (carbon_credits, energy, policies, forecast, rag_search, openmeteo)
- 4 new UI pages (carbon-credits, energy, policies, forecast)
- 10+ new Svelte 5 components
- AI client climate-domain aligned (MAR-854 done)
- DB entities/schemas for emissions, ESG, alerts, audit

**Secrets on ccec-api are already set:**
- ✅ MINIMAX_API_KEY, JWT_SECRET_KEY, DATABASE_URL, DATABASE_URL_SYNC
- ✅ MINIMAX_BASE_URL, MINIMAX_MODEL, CORS_ORIGINS

### GitHub Actions
- Workflow: `.github/workflows/deploy.yml` — ready
- Trigger: push to `main` branch
- Current repo: `TungIT98/CCEC` (different from workspace `E:\ccec-climate-platform`)
- **Issue:** GH credentials mismatch — `gh` CLI uses `TungIT98/CCEC` but workspace is different

## Decision Required: Deployment Strategy

### Option A: Push workspace code → GitHub CI/CD (Recommended)
1. Add remote: `git remote add origin https://github.com/TungIT98/CCEC.git`
2. Push main branch → triggers `.github/workflows/deploy.yml`
3. CI builds Docker images → deploys to Fly.io automatically
4. **Pros:** Full CI/CD pipeline, automatic on every push
5. **Cons:** Requires git push (need to confirm with board)

### Option B: Manual deploy via flyctl
```bash
flyctl deploy --config infra/fly/fly.toml.api --image ghcr.io/...  # Build locally or use existing image
```
- **Pros:** No git push needed
- **Cons:** Manual, no CI pipeline, image must be built first

### Option C: Docker Compose (local first)
```bash
cd infra/docker && docker-compose up --build
```
- **Pros:** Full stack locally, verifies everything works
- **Cons:** Not publicly accessible, requires Docker Desktop

## Recommended Path

```
Step 1: Board confirms → push workspace code to GitHub main
Step 2: GitHub Actions builds + deploys (auto)
Step 3: Smoke test deployed endpoints
Step 4: Custom domain + HTTPS via Cloudflare
```

## Immediate blockers before push
1. ❌ `.env` has real secrets — make sure .gitignore excludes it
2. ❌ `AGENTS.md` deleted from git tracking but not from remote
3. ❌ Many `.pyc` cache files staged as deleted — clean up

## Cost Estimate (Fly.io)
| Resource | Spec | Monthly Cost |
|---|---|---|
| ccec-api VM | 256MB, 1x CPU | ~$4.70/mo |
| ccec-web VMs | 256MB, 2x CPUs | ~$9.40/mo |
| Fly Postgres | 1GB storage | ~$5.50/mo |
| Volume (ccec_data) | 1GB | ~$0.15/mo |
| **Total** | | **~$20/mo** |