# MAR-859 Final Status — 2026-05-12

## What Was Fixed

| Fix | Status |
|-----|--------|
| `_routes.json` at `dist/functions/_routes.json` | ✅ |
| `_redirects` removed from `dist/` | ✅ |
| `[[path]].js` proxy code correct (1160 bytes) | ✅ |
| CI Build Web: vite lockfile `8.0.12` → `8.0.6` | ✅ |
| CI Build Web: command aligned with deploy.yml | ✅ |
| CI Copy Functions: source changed to `public/_functions/` | ✅ |
| GitHub Secret `CLOUDFLARE_API_TOKEN` updated | ✅ |

## CI Pipeline Status (Current)

| Step | Status |
|------|--------|
| Checkout | ✅ |
| Install deps | ✅ |
| Build Web | ✅ |
| Copy Functions | ✅ |
| Install Wrangler | ✅ |
| Deploy to CF Pages | ❌ Token auth fails |

## Root Cause: Token Missing "Cloudflare Pages: Edit" Permission

The `cfat_dbe447...` token is an **Account Token** but does NOT have the required permission:

**Required:** `Account → Cloudflare Pages → Edit`

**What the token has:** Unknown (likely blank or insufficient)

**Evidence:**
```
wrangler pages project list → Authentication error [code: 10000]
wrangler whoami             → Invalid access token [code: 9109]
CF REST API /accounts/{id}/pages/... → Authentication error [code: 10000]
```

**Both wrangler and CF REST API fail** because they use the same auth mechanism.

## Solution: Board Must Create New Token with Correct Scope

Board creates new token at https://dash.cloudflare.com/profile/api-tokens:

1. **"Create Token"** → **"Create Custom Token"** → **"Create More"**
2. **Account permissions:**
   - `Cloudflare Pages` → **Edit** ✅ (CRITICAL)
   - `Account Settings` → Read ✅ (optional, for `whoami`)
3. **Account resources:** Include → select CCEC account
4. **Create Token** → copy immediately
5. Send token to this agent to update GitHub Secret

## After New Token

CI will automatically deploy on next push. Expected result:
- `curl https://ccec-web.pages.dev/api/v1/health` → `{"status":"ok"}`

## Why Fly.io Backend Is Fine

| Component | URL | Status |
|-----------|-----|--------|
| Backend API | `ccec-api.fly.dev` | ✅ Running |
| Frontend | `ccec-web.pages.dev` | ✅ Serving static |
| `/api/*` proxy | CF Pages Function | ❌ Never deployed |

Once CI deploys, the proxy at `[[path]].js` will forward `/api/*` to Fly.io.

## Manual Upload Option (Temporary Fix)

Board can upload `apps/web/dist/` via CF Dashboard → ccec-web → Upload assets.
This provides a one-time deploy while waiting for new token.
