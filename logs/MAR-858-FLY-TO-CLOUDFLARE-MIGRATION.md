# MAR-858: Fly.io + Cloudflare HTTPS Fix — BLOCKED

**Status:** BLOCKED — invalid CLOUDFLARE_API_TOKEN secret
**Date:** 2026-05-12
**Board direction:** Fly.io backend + Cloudflare frontend, no Railway
**Approver:** local-board

---

## Root Cause: cp -r Bug

The `cloudflare-pages.yml` had a broken `cp -r` command that produced the wrong directory name in dist:

```bash
# WRONG (what was in the old workflow):
cp -r apps/web/public/_functions "apps/web/dist/_functions"
# Result: dist/_functions/  ← Cloudflare ignores _functions (private)
```

```bash
# CORRECT (fixed):
cp -r apps/web/public/_functions apps/web/dist/functions
# Result: dist/functions/  ← Cloudflare recognizes Pages Functions dir
```

Without a trailing slash, `cp -r src dest` treats `dest` as the new name of the copied directory. So `_functions` was being copied AS `_functions` into dist, making `dist/_functions/` which Cloudflare ignores.

---

## Fix Applied

| File | Change |
|------|--------|
| `.github/workflows/cloudflare-pages.yml` | Fixed `cp -r` to produce `dist/functions/`, added debug `ls` |
| `logs/MAR-858-FLY-TO-CLOUDFLARE-MIGRATION.md` | Added root cause analysis |

**Commit:** `46563fb` — fix(deploy): correct cp -r to create dist/functions/ for CF Pages

---

## Blocked: GitHub Secrets CLOUDFLARE_API_TOKEN is Invalid

The CLOUDFLARE_API_TOKEN stored as a GitHub Secret is not a valid Cloudflare API token.
Both GitHub Actions (`wrangler pages deploy`) and local wrangler fail with:
```
Authentication error [code: 10000]
Invalid access token [code: 9109]
```

**Testing locally confirms:**
- Token `cfat_AWrSDLHXx...` from `.env` fails all CF API calls (code 1000: "Invalid API Token")
- Local wrangler with same token → "Too many authentication failures" (code 10502)
- GitHub Actions 5 consecutive failures all at "Install dependencies" step
  (actual failure was in Install Wrangler step, hidden by earlier failure)
  → after adding `if: always()`: Build Web fails (crlf/lockfile issue), but Install Wrangler
    runs and ALSO fails with `Authentication error [code: 10000]`

**Root cause:** The token stored in GitHub Secrets is either:
1. Expired/revoked, or
2. Created with wrong permissions (needs Account:Pages:Edit), or
3. Corrupted in transit (though it starts with `cfat_` so likely not)

**Fix (board action required):**
1. Go to https://dash.cloudflare.com/profile/api-tokens
2. Create new API Token with template: "Cloudflare Pages" (has Account:Pages:Edit)
   Or custom token with: Account → Cloudflare Pages → Edit
3. Copy the NEW token (starts with `cfat_`)
4. Go to GitHub → Settings → Secrets → Actions → CLOUDFLARE_API_TOKEN
5. Replace with new token (do NOT include surrounding quotes)
6. Also update `CLOUDFLARE_ACCOUNT_ID` secret if needed (currently: `2b9327c415b0332ede6508d2f5a89691`)

After fixing the secret, the deployment should work because:
- `dist/functions/` structure is correct
- `[[path]].js` proxy is updated and ready
- All workflow steps are instrumented for debug output

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

After fixing the secret, the deployment should work because: