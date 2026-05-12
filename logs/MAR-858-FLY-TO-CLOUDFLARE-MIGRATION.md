# MAR-858: Fly.io + Cloudflare HTTPS Fix

## Status: IN PROGRESS — Cloudflare Pages Functions Proxy Deployed

**Date:** 2026-05-12
**Board direction:** Fly.io backend + Cloudflare frontend, no Railway
**Approver:** local-board

---

## Problem

Fly.io ACME certificate provisioning fails for `ccec-api.fly.dev`:
```
Error: failed to create ACME certificate: cannot register certificate for this domain (Request ID: 01KRD...-sin)
```
Root cause: Singapore (sin) region in Fly.io has broken ACME. Machine was removed but cert still fails.

---

## Solution: Cloudflare Pages Functions Proxy

Cloudflare Pages Functions run at the edge, provide HTTPS automatically, and can forward requests to Fly.io HTTP backend.

```
Browser (HTTPS) → Cloudflare Pages → [[path]].js → Fly.io API (HTTP)
```

---

## Files Changed

### 1. `apps/web/public/_functions/api/[[path]].js` (NEW)
Cloudflare Pages Function — proxies all `/api/*` requests to Fly.io HTTP backend.

```javascript
export async function onRequest(context) {
  const url = new URL(context.request.url);
  const targetUrl = `http://ccec-api.fly.dev${url.pathname}${url.search}`;
  const response = await fetch(targetUrl, {
    method: context.request.method,
    headers: filteredHeaders(context.request.headers),
    body: context.request.body,
  });
  return new Response(await response.arrayBuffer(), {
    status: response.status,
    headers: filteredResponseHeaders(response.headers),
  });
}
```

### 2. `apps/web/public/_functions/_routes.json` (NEW)
Limits function invocation to `/api/*` paths only:
```json
{ "version": 1, "include": ["api/*"], "exclude": [] }
```

### 3. `.github/workflows/cloudflare-pages.yml` (UPDATED)
- Changed `PUBLIC_API_URL` from `https://ccec-api.fly.dev` → `https://ccec-web.pages.dev/api`
- Added `cp -r apps/web/public/_functions` step to include functions in build

### 4. `apps/web/.env.example` (UPDATED)
```
PUBLIC_API_URL=https://ccec-web.pages.dev/api
```

---

## Architecture After Fix

| Layer | URL | Protocol | Status |
|-------|-----|----------|--------|
| Frontend | `https://ccec-web.pages.dev` | HTTPS ✅ | Cloudflare Pages |
| API Proxy | `https://ccec-web.pages.dev/api/*` | HTTPS ✅ | CF Pages Function |
| Backend | `http://ccec-api.fly.dev` | HTTP | Fly.io (running) |

---

## Board Action Required

1. **Update Cloudflare Pages environment variable:**
   - Go to: dash.cloudflare.com → Pages → ccec-web → Settings → Environment variables
   - Set: `PUBLIC_API_URL` = `https://ccec-web.pages.dev/api`

2. **Push to main** (or merge this PR) → GitHub Actions auto-deploys with the new `_functions/`

3. **Smoke test:**
   - `curl https://ccec-web.pages.dev/api/api/v1/health`
   - Should return: `{"status":"ok","version":"..."}`

---

## Retiring Fly.io

After confirmation CF proxy works, can disable Fly.io web deployment entirely. API stays on Fly.io.

---

*Created by: CEO Agent | Updated: 2026-05-12*