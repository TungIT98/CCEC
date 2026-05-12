# MAR-859: Board Directive — Consolidate to Cloudflare

**Date:** 2026-05-12  
**Board Directive:** "Cứ quằn mãi chỗ này thế nhỉ. Tập trung chuyển về hết Cloudflare. Nếu FastAPI ko biên dịch được thì đập đi xây dựng lại bằng ngôn ngữ khác cho phù hợp."

## Current Status (as of 2026-05-12)

| Component | Location | Status |
|-----------|----------|--------|
| Frontend | CF Pages (ccec-web.pages.dev) | ✅ Running |
| Backend API | Fly.io (ccec-api.fly.dev) | ✅ Running |
| `/api/*` proxy | CF Pages Functions | ❌ Broken (dead token, never deployed) |
| GitHub CI deploy | `.github/workflows/cloudflare-pages.yml` | ❌ Blocked (dead token) |

## Root Cause of Proxy Failure

Two things are wrong in the current live deployment:
1. `_routes.json` was at `dist/_functions/_routes.json` instead of `dist/functions/_routes.json` — CF couldn't route `/api/*` to the function
2. `_redirects` file (`/* → /index.html`) was present in dist — CF processed it BEFORE the function, intercepting `/api/*` requests

**Both are fixed in `dist/` now.** The proxy code in `[[path]].js` is correct.

## Immediate Fix (Manual — 2 min)

Board uploads `apps/web/dist/` via CF Dashboard:
1. Go to https://dash.cloudflare.com/pages/view/ccec-web
2. Click "Upload assets" (direct deploy without GitHub)
3. Drag-and-drop the `dist/` folder (or zip upload)
4. Wait 30s → test `curl https://ccec-web.pages.dev/api/v1/health`

Expected result: `{"status":"ok","version":"0.1.0"}`

---

## Long-term: Consolidate to Cloudflare

The board wants everything on Cloudflare. Here's the honest assessment:

### Option A: CF Workers (Node.js/TypeScript) — CLEAN ✅
**Pros:** 100% Cloudflare, global edge, free tier, fast cold start  
**Cons:** Must rewrite FastAPI in TypeScript (30 source files)  
**Effort:** ~2-3 days  
**Languages:** TypeScript (Node.js), Python via Worker add-ons (paid)

### Option B: Keep Fly.io + CF Pages (Current Architecture) ✅
**Pros:** Works now, Fly.io already running, minimal change  
**Cons:** Two cloud providers, Fly.io free tier limitations  
**Effort:** 0 (just fix the CF token)  
**Verdict:** Fastest to fix, reliable

### Option C: Cloudflare Pages + R2 + Durable Objects
**Pros:** Full CF ecosystem  
**Cons:** Durable Objects are stateful single-instance, not good for REST API  
**Verdict:** Not suitable for FastAPI-style backend

### Option D: Vercel (Node.js) or Railway
**Cons:** New vendor, migration cost, not "Cloudflare"

## Recommended Path

1. **Immediate:** Manual CF Dashboard upload → verify proxy works
2. **If proxy works:** Architecture is sound. Fix CF token → GitHub CI resumes
3. **If proxy still fails:** Track down why, then consider Option A (rewrite to TypeScript)

## Why NOT rewrite FastAPI right now

- Fly.io backend is running and healthy
- The proxy fix (manual upload) should resolve the issue
- Rewriting 30 Python files to TypeScript is 2-3 days of work for uncertain benefit
- CF Workers can't run Python natively anyway — would need Workers for AI or similar paid product

**Decision point:** Let's first see if the manual upload fixes the proxy. If yes, we have a working system. If no, we have a specific technical problem to solve, not a migration.

## Verification After Manual Upload

```bash
curl https://ccec-web.pages.dev/api/v1/health
# Expected: {"status":"ok","version":"0.1.0"}

curl https://ccec-web.pages.dev/
# Expected: HTML homepage (200)

curl -X POST https://ccec-web.pages.dev/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"test"}'
# Expected: JSON error or auth response
```
# Trigger CF deploy Tue May 12 18:28:55 SEAST 2026
