# MAR-834 Fix Status — 2026-05-11 17:47 UTC

## Issue
Board báo lỗi khi deploy xong nhưng chưa hoàn tất.

## Root Cause
HTTPS không hoạt động trên ccec-web.fly.dev và ccec-api.fly.dev.
- Fly.io ACME certificate registration thất bại (tên miền chưa được xác minh)
- Port 443 trả về TLS handshake error ("packet length too long")
- Port 80 hoạt động bình thường

## Fixes Applied

### 1. API URL: HTTPS → HTTP
Frontend build với `PUBLIC_API_URL=http://ccec-api.fly.dev`
- Fly.io redirect HTTP→HTTPS ở layer proxy
- Web → API call: HTTP port 80 → proxy upgrades to HTTPS
- Files: `infra/docker/Dockerfile.web`, `.github/workflows/deploy.yml`

### 2. Root Redirect trong API
`apps/api/main.py` thêm route:
```
GET / → redirect https://ccec-web.fly.dev
```
Người dùng truy cập root được chuyển đến frontend.

### 3. Dockerfile Path Resolution
`infra/fly/fly.toml.web`: sửa `../docker/Dockerfile.web` → `infra/docker/Dockerfile.web`
Build context resolution đúng trên cả local và GitHub Actions.

### 4. GitHub Actions CI Build
`.github/workflows/deploy.yml`: Thêm `PUBLIC_API_URL=http://ccec-api.fly.dev`
khi build web trong CI pipeline.

## Deployment Status (2026-05-11 17:47 UTC)

| Service | Status | Notes |
|---------|--------|-------|
| ccec-api | ✅ Deployed | Root redirect working, health OK |
| ccec-web | ✅ Deployed | HTTP API URL embedded, login page OK |
| HTTP port 80 | ✅ Working | All endpoints respond |
| HTTPS port 443 | ❌ Broken | TLS handshake fails, cert not issued |

## Verified Working
- Register: `POST /api/v1/auth/register` → 201 Created ✅
- Login: `POST /api/v1/auth/login/json` → 200 + JWT ✅
- API Health: `GET /health` → 200 OK ✅
- Web root: `GET /` → 200 HTML (27KB) ✅
- Login page: contains `http://ccec-api.fly.dev` ✅

## Files Changed
- `apps/api/main.py`
- `infra/fly/fly.toml.web`
- `infra/docker/Dockerfile.web`
- `.github/workflows/deploy.yml`
- `apps/web/` (rebuilt with correct env var)

## Remaining Issue: HTTPS/SSL
Port 443 requires domain ownership verification in Fly.io dashboard.
Users accessing https:// URLs will see TLS error.
Fix: Verify domain ownership in Fly.io dashboard, or use custom domain already verified.

Note: Paperclip API unreachable — status written to disk only.