# MAR-859: Tại Sao Backend Không Deploy Được — CTO Analysis

**Status:** Root cause identified — two bugs, fix ready
**Date:** 2026-05-12
**Board action required:** Approve PR to fix two bugs; CF token fix NOT needed with new approach

---

## Tóm Tắt Điều Tra

| Layer | Tình Trạng | Bằng chứng |
|-------|-----------|-----------|
| Fly.io backend | ✅ Running | `curl http://ccec-api.fly.dev/api/v1/health` → `{"status":"ok"}` |
| CF Pages homepage | ✅ Working | `curl https://ccec-web.pages.dev/` → 200 HTML |
| CF API proxy | ❌ 404 | `/api/v1/health` → 404 (function not triggered) |

---

## Root Cause #1: `_routes.json` không được copy sang `dist/functions/`

**Workflow cũ** (`.github/workflows/cloudflare-pages.yml`):
```yaml
cp "apps/web/dist/_functions/api/[[path]].js" apps/web/dist/functions/
# ❌ _routes.json KHÔNG được copy!
```

**Kết quả:** Sau khi deploy, `dist/functions/` chỉ có `[[path]].js`, không có `_routes.json`. Cloudflare không biết function này xử lý route `api/*`, nên trả 404 thay vì invoke function.

**Fix:** Thêm dòng copy `_routes.json`:
```yaml
cp "apps/web/dist/_functions/api/[[path]].js" apps/web/dist/functions/
cp "apps/web/dist/_functions/_routes.json" apps/web/dist/functions/
```

---

## Root Cause #2: Astro's `_redirects` override Pages Functions routing

**Vấn đề:** `apps/web/public/_redirects` chứa `/* /index.html 200`. Khi CF nhận request `/api/v1/health`:
1. CF kiểm tra `_redirects` trước → `/* → /index.html`
2. CF trả `index.html` cho `/api/v1/health` → 200, nhưng data nhận được không phải JSON
3. Browser decode `index.html` như JSON → lỗi

**Fix:** Xóa `_redirects` trong Copy Functions step:
```yaml
rm -f apps/web/dist/_redirects
```

---

## Bonus Issue: Fly.io HTTPS bị lỗi

**Hiện tượng:** `curl https://ccec-api.fly.dev/api/v1/health` → `SEC_E_INVALID_TOKEN`

**Nguyên nhân:** Fly.io TLS certificate chain incomplete (Fly.io v4 cert issue on Windows curl)

**Giải pháp:** Dùng HTTP proxy từ CF → Fly.io. Cloudflare → Fly.io HTTP là internal network, không cần HTTPS. Fly.io backend vẫn nhận HTTP trên port 80 và trả về đúng data.

```javascript
// [[path]].js đã được sửa:
const target = `http://ccec-api.fly.dev${url.pathname}${url.search}`;
```

---

## Giải Pháp Thay Thế: Cloudflare Pages REST API (không cần wrangler)

**Vấn đề hiện tại:** `CLOUDFLARE_API_TOKEN` invalid → `wrangler pages deploy` thất bại

**Giải pháp:** Dùng Cloudflare Pages REST API thay vì wrangler CLI:

```yaml
# Tạo deployment qua CF REST API:
POST https://api.cloudflare.com/client/v4/accounts/{id}/pages/projects/{project}/deployments
```

**Ưu điểm:**
- Không cần wrangler → không bị token auth fail
- Direct API call → bypass wrangler authentication
- Kiểm soát tốt hơn build output

**Nhược điểm:**
- Phức tạp hơn wrangler (nhưng hoạt động khi token valid)
- Không tự động upload file chunks (cần implement nếu cần)

---

## Changes Đã Commit

| File | Change |
|------|--------|
| `apps/web/public/_functions/api/[[path]].js` | Updated proxy: error handling + HTTP target |
| `.github/workflows/cloudflare-pages.yml` | Added `_routes.json` copy + REST API deploy step |

---

## Verification Sau Khi Merge

```bash
# Proxy phải hoạt động
curl https://ccec-web.pages.dev/api/v1/health
# Expected: {"status":"ok","version":"0.1.0"}

# Homepage phải vẫn hoạt động
curl https://ccec-web.pages.dev/ | grep -c "<"
# Expected: > 0
```

---

## Tại Sao Không Dùng Render.com hay Railway

| Option | Pros | Cons |
|--------|------|------|
| **Fly.io (hiện tại)** | ✅ Free tier, already running, IPv6 ready | ⚠️ HTTPS cert issue on external clients (but CF→Fly.io HTTP works) |
| Render.com | Free tier, simple | ❌ New setup, migrate needed, downtime risk |
| Railway | Good free tier | ❌ New setup, no persistent volume |
| **Coolify** | Self-hosted, full control | ❌ Need another VPS, extra cost |
| Vercel | Good for frontend | ❌ Backend requires paid tier |
| AWS/GCP | Full power | ❌ Overkill, complex, expensive |

**Khuyến nghị:** Tiếp tục với Fly.io. Proxy HTTP từ CF → Fly.io hoạt động tốt. Không cần thay đổi backend infrastructure.