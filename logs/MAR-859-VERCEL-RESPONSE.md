# MAR-859 Board Response — Backend trên Vercel?

**Comment from:** local-board
**Comment:** "vậy sử dụng bên khác triển khai backend thì có được không ví dụ như vercel"
**Date:** 2026-05-12

---

## TL;DR: Vercel không phù hợp cho FastAPI backend

### Tại sao Vercel không tốt cho FastAPI

| Hạn chế | Chi tiết |
|---------|----------|
| Serverless only | Vercel chỉ hỗ trợ serverless functions — FastAPI cần persistent uvicorn process |
| Timeout limit | Vercel serverless max 10s (free tier) — API requests sẽ timeout |
| No persistent state | Không giữ database connection pool, không có persistent volume |
| Cần refactor | Phải đổi FastAPI app → Vercel serverless handler function |
| PostgreSQL | Không có built-in PostgreSQL — cần external service như Supabase/Neon |

### Lựa chọn tốt hơn nếu rời Fly.io

| Provider | Free Tier | Persistent VPS | FastAPI | Migration Effort |
|----------|-----------|----------------|---------|-----------------|
| **Railway** | $5/tháng credit | ✅ | ✅ Native Docker | **Thấp** |
| **Render** | Free (cold start) | ✅ | ✅ | Trung bình |
| **Coolify** | Tự host (VPS) | ✅ | ✅ | Cao — cần VPS mới |
| **Vercel** | Limited | ❌ Serverless | ⚠️ Refactor cần | Cao |
| **AWS/GCP** | Trial | ✅ | ✅ | Rất cao |

### Railway là lựa chọn tốt nhất nếu muốn rời Fly.io

**Ưu điểm:**
- Persistent VPS (không phải serverless)
- Native Docker deploy — Dockerfile hiện tại dùng được
- PostgreSQL built-in với persistent storage
- Không có ACME/SIN region bug như Fly.io

**Deploy nhanh:**
```bash
npm i -g @railway/cli
railway login
railway init
# Add Dockerfile.api, set port=8000
railway up
```

---

## NHƯNG: Không cần thay đổi backend

**Backend Fly.io đang chạy hoàn hảo:**
```
curl http://ccec-api.fly.dev/api/v1/health
→ {"status":"ok","version":"0.1.0"} ✅
```

**Vấn đề DUY NHẤT:** CF Pages token không deploy được. Fix token = done.

---

## Tóm tắt hành động

| Ưu tiên | Hành động | Thời gian |
|---------|-----------|-----------|
| **1 (Ngay)** | Deploy thủ công qua CF Dashboard | 2 phút |
| **2 (Fix CI)** | Tạo CF API token mới → update GitHub Secret | 5 phút |
| **3 (Không cần)** | Migrate sang Railway/Vercel | Không cần thiết |

**Kết luận:** Không cần Vercel hay Railway. Chỉ cần fix CF API token.