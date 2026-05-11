# MAR-834 SSL/Domain Fix — 2026-05-11

## Status: BLOCKED — needs board decision on domain + devops-dev

## Symptom
Board báo lỗi kèm screenshot (MAR-834 comment). Không load được trang, login/register fail.

## Root Cause Confirmed

HTTPS (port 443) trên ccec-web.fly.dev và ccec-api.fly.dev **KHÔNG có SSL certificate**.

| App | Port 80 HTTP | Port 443 HTTPS | SSL Cert |
|-----|-------------|----------------|----------|
| ccec-web.fly.dev | ✅ 200 OK | ❌ Connection timeout | ❌ Not provisioned |
| ccec-api.fly.dev | ✅ 200 OK | ❌ TLS error | ❌ Not provisioned |

## Why HTTPS is broken

Fly.io dịch vụ đã đúng:
- ccec-web: TCP 443→4321 (Force HTTPS ✅), TCP 80→4321
- ccec-api: TCP 443→8000 (Force HTTPS ✅), TCP 80→8000

Nhưng Fly.io **KHÔNG tự động cấp SSL** cho `*.fly.dev` — Let's Encrypt ACME bị blocked/rate-limit trên tài khoản này:

```
flyctl certs add -a ccec-web ccec-web.fly.dev
→ Error: cannot register certificate for this domain

flyctl certs add -a ccec-api ccec-api.fly.dev
→ Error: cannot register certificate for this domain
```

## Current Workaround (ĐANG DÙNG)

Frontend build với `PUBLIC_API_URL=http://ccec-api.fly.dev` (HTTP port 80):
- Register: 201 Created ✅
- Login: 200 OK + JWT tokens ✅
- Health: {"status":"ok"} ✅

Trình duyệt user vẫn thấy HTTPS trên frontend nhưng API call thực sự đi qua HTTP port 80.

## Fix Options

### Phương án A — Custom Domain (KHUYẾN NGHỊ)
Mua hoặc kiểm soát domain (VD: `ccec.vn`, `ccec-climate.com`):
1. Board quyết định domain
2. Devops-dev tạo DNS A record trỏ về `213.188.198.148` (ccec-web) và `213.188.198.47` (ccec-api)
3. Sau khi DNS propagate:
   ```bash
   flyctl certs add -a ccec-web ccec-climate.com
   flyctl certs add -a ccec-api api.ccec-climate.com
   ```
4. Update frontend PUBLIC_API_URL thành HTTPS

### Phương án B — Import Cert Thủ Công
Nếu đã có cert từ Cloudflare/Comodo:
```bash
flyctl certs import -a ccec-web --cert-file server.crt --key-file server.key
```

### Phương án C — Giữ nguyên HTTP (Không khuyến khích cho production)
Dùng `http://ccec-api.fly.dev` — đang hoạt động được nhưng không ideal.

## IP Addresses
- ccec-web: 213.188.198.148
- ccec-api: 213.188.198.47

## Next Actions
1. [ ] Board quyết định domain (custom domain)
2. [ ] Devops-dev configure DNS sau khi domain được chọn
3. [ ] Devops-dev run flyctl certs add sau DNS propagation
4. [ ] Update frontend PUBLIC_API_URL → HTTPS
5. [ ] Redeploy ccec-web và ccec-api

## Blocked by
- Board: quyết định domain name
- Devops-dev: DNS config + SSL certificate setup


## Paperclip API URL Discovery (2026-05-11)
Paperclip API chỉ reachable qua HTTPS qua TailScale:
- Old (broken): http://desktop-2i9344q.tail821e9a.ts.net:3100
- New (working): https://desktop-2i9344q.tail821e9a.ts.net (port 443, TailScale serve)


## Update 2026-05-11 11:15
Board chọn phương án Cloudflare SSL.
Không tìm thấy Cloudflare token trong memory CCEC project.
Cần Board cung cấp: domain, Cloudflare account email, API token.


## Update 2026-05-11 14:36
Board chỉ thị: tự làm, không cần hỏi.
Đã tự động hóa Cloudflare DNS setup trong GitHub Actions CI/CD.
File changed: .github/workflows/deploy.yml — added cloudflare-dns job
Board cần thêm GitHub Secrets: CLOUDFLARE_API_TOKEN + CLOUDFLARE_ZONE
Commit + push → DNS tự setup → HTTPS tự hoạt động
