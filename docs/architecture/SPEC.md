# MAR-834 — Precise Task Split
## 2026-05-11 | Exactly what exists vs what needs to be built

---

## EXISTING CODE (không cần làm lại)

### Backend — có đủ:
- `routers/users.py` → GET /users/me, PATCH /users/me ✅
- `routers/auth.py` → login, register, refresh ✅
- `routers/chat.py` → AI chat ✅
- `routers/climate_data.py`, `emissions.py`, `maps.py` → data ✅
- `models/schemas.py` → UserResponse, UserUpdate ✅

### Frontend — có đủ:
- `global.css` → CSS vars design system
- `Layout.astro` → base layout
- `BaseLayout.astro` → base
- `lib/api.ts` → API client
- `lib/auth.ts` → auth helpers
- `components/ui/` → Button, Card, Badge ✅
- Navbar, Hero, Features, Footer, HowItWorks, Pricing, Roadmap, Team ✅
- ChatWidget, MapWidget ✅
- LoginForm, AuthGuard ✅
- Dashboard, Emissions, ESG, Maps, Chat pages ✅

---

## BACKEND — việc cần làm (elixir-dev)

### 1. extensions: notifications + settings + team
**File:** `apps/api/models/entities.py`
→ Thêm: `Notification(id, user_id, title, body, is_read, created_at)`
→ Thêm: `UserSettings(id, user_id, language, theme, timezone, email_notifications, app_notifications, weekly_digest, decimal_places, date_format)`

**File:** `apps/api/models/database.py`
→ Thêm 2 bảng: `notifications`, `user_settings`
→ Thêm `get_user_settings(user_id)` helper

**File:** `apps/api/models/schemas.py`
→ Thêm: `NotificationResponse`, `NotificationCreate`
→ Thêm: `UserSettingsResponse`, `UserSettingsUpdate`

### 2. routers: notifications + settings + team
**File:** `apps/api/routers/notifications.py` (MỚI)
→ GET /notifications → list của user
→ POST /notifications → create (system)
→ PATCH /notifications/{id}/read → mark read
→ PATCH /notifications/read-all → mark all read

**File:** `apps/api/routers/settings.py` (MỚI)
→ GET /settings → get user settings
→ PUT /settings → update user settings (language, theme, timezone, notifications, etc.)

**File:** `apps/api/routers/team.py` (MỚI)
→ GET /team → list team members (admin only)
→ POST /team/invite → invite member (admin only)
→ DELETE /team/{user_id} → remove member (admin only)

**File:** `apps/api/routers/users.py` (SỬA)
→ PATCH /users/me: thêm phone, organization fields nếu chưa có
→ Thêm POST /users/me/password → change password (validate old password)
→ Thêm GET /users/me/activity → activity log

**File:** `apps/api/main.py` (SỬA)
→ Thêm: `router.include_router(notifications.router)`
→ Thêm: `router.include_router(settings.router)`
→ Thêm: `router.include_router(team.router)`

---

## FRONTEND — việc cần làm (frontend-dev)

### 1. Bee color theme — MÀU DUY NHẤT cần sửa
**File:** `apps/web/src/styles/global.css`
```
--color-primary:       #F59E0B  ← thay #0D9488 (teal)
--color-primary-light: #FBBF24  ← thay #14B8A6
--color-primary-dark:  #D97706  ← thay #0F766E
--color-accent:        #92400E  ← amber-800 thay blue-800
--color-accent-light:  #F59E0B  ← amber-500
--color-bg:            #FFFBEB  ← cream thay white
--color-surface-alt:   #FFEDD5  ← warm peach thay slate-50
--color-text-primary:  #78350F  ← brown thay slate-900
```
→ KHÔNG sửa shadow, spacing, border-radius

**Files cần kiểm tra:** Nếu có hardcoded hex mã màu cũ (#0D9488, #14B8A6, #1E40AF, #3B82F6, teal, blue), thay bằng CSS var.

### 2. Pages mới
| File | Nội dung | Ghi chú |
|------|----------|---------|
| `pages/register.astro` | Register form như login nhưng cho signup | CHƯA CÓ |
| `pages/settings.astro` | Settings với 6 tabs | CHƯA CÓ |
| `pages/profile.astro` | User profile page | CHƯA CÓ |

### 3. Components mới trong `components/ui/`
| File | Mô tả | Phụ thuộc |
|------|-------|-----------|
| `Modal.svelte` | Reusable modal dialog | Settings, Dashboard |
| `Tabs.svelte` | Tab navigation | Settings (6 tabs) |
| `Toast.svelte` | Notification toast | Global |
| `Toggle.svelte` | On/off switch | Settings notifications |
| `Input.svelte` | Styled input field | Settings, Register |
| `Avatar.svelte` | User avatar | Navbar, Profile, Settings |
| `DataTable.svelte` | Sortable data table | Emissions, ESG |
| `ExportButton.svelte` | CSV/PDF export | Emissions, ESG |
| `ThemeToggle.svelte` | Light/dark toggle | Navbar |
| `LangSwitcher.svelte` | VN/EN toggle | Navbar |

### 4. Sửa pages hiện có
| File | Thay đổi |
|------|----------|
| `pages/index.astro` | Thêm link Đăng ký, Bee color |
| `pages/login.astro` | Thêm link Đăng ký, Bee color |
| `pages/dashboard.astro` | Thêm drag-drop widget layout (dùng CSS grid sortable) |
| `pages/emissions.astro` | Thêm DataTable, ExportButton, Bee color |
| `pages/esg.astro` | Thêm DataTable, ExportButton, KPIs grid, Bee color |
| `pages/chat.astro` | Bee color accents |

### 5. Navbar upgrade
- Thêm: Avatar dropdown (profile, settings, logout)
- Thêm: NotificationBell (số thông báo chưa đọc)
- Thêm: ThemeToggle, LangSwitcher
- Sửa màu: Bee color theme

### 6. lib/api.ts — thêm endpoints
```typescript
// Thêm vào api.ts
export const getSettings = () => api.get('/settings')
export const updateSettings = (data) => api.put('/settings', data)
export const getNotifications = () => api.get('/notifications')
export const markNotificationRead = (id) => api.patch(`/notifications/${id}/read`)
export const getTeamMembers = () => api.get('/team')
export const inviteTeamMember = (email, role) => api.post('/team/invite', {email, role})
export const removeTeamMember = (id) => api.delete(`/team/${id}`)
export const exportData = (format, params) => api.post('/data/export', {format, ...params})
export const changePassword = (old, new_) => api.post('/users/me/password', {old_password: old, new_password: new_})
```

### 7. lib/auth.ts — thêm
```typescript
export const logout = () => { clearTokens(); window.location.href = '/login' }
export const getUser = () => { /* return current user from token */ }
```

---

## FILE COUNT CHÍNH XÁC

### Backend (elixir-dev):
1. `apps/api/models/entities.py` — thêm Notification, UserSettings
2. `apps/api/models/database.py` — thêm 2 bảng
3. `apps/api/models/schemas.py` — thêm schemas
4. `apps/api/routers/notifications.py` — MỚI (4 endpoints)
5. `apps/api/routers/settings.py` — MỚI (2 endpoints)
6. `apps/api/routers/team.py` — MỚI (3 endpoints)
7. `apps/api/routers/users.py` — SỬA (thêm password change, activity)
8. `apps/api/main.py` — SỬA (thêm 3 router)

### Frontend (frontend-dev):
1. `apps/web/src/styles/global.css` — SỬA (bee color vars)
2. `apps/web/src/pages/register.astro` — MỚI
3. `apps/web/src/pages/settings.astro` — MỚI (6 tabs)
4. `apps/web/src/pages/profile.astro` — MỚI
5. `apps/web/src/components/ui/Modal.svelte` — MỚI
6. `apps/web/src/components/ui/Tabs.svelte` — MỚI
7. `apps/web/src/components/ui/Toast.svelte` — MỚI
8. `apps/web/src/components/ui/Toggle.svelte` — MỚI
9. `apps/web/src/components/ui/Input.svelte` — MỚI
10. `apps/web/src/components/ui/Avatar.svelte` — MỚI
11. `apps/web/src/components/ui/DataTable.svelte` — MỚI
12. `apps/web/src/components/ui/ExportButton.svelte` — MỚI
13. `apps/web/src/components/ui/ThemeToggle.svelte` — MỚI
14. `apps/web/src/components/ui/LangSwitcher.svelte` — MỚI
15. `apps/web/src/components/Navbar.svelte` — SỬA (dropdown, bell, toggles)
16. `apps/web/src/components/ChatWidget.svelte` — SỬA (bee color)
17. `apps/web/src/components/MapWidget.svelte` — SỬA (bee color controls)
18. `apps/web/src/components/Hero.svelte` — SỬA (bee color)
19. `apps/web/src/components/Features.svelte` — SỬA (bee color)
20. `apps/web/src/components/Footer.svelte` — SỬA (bee color)
21. `apps/web/src/components/Pricing.svelte` — SỬA (bee color)
22. `apps/web/src/components/Roadmap.svelte` — SỬA (bee color)
23. `apps/web/src/components/Team.svelte` — SỬA (bee color)
24. `apps/web/src/pages/index.astro` — SỬA (bee color, register link)
25. `apps/web/src/pages/login.astro` — SỬA (bee color, register link)
26. `apps/web/src/pages/dashboard.astro` — SỬA (drag-drop, bee color)
27. `apps/web/src/pages/emissions.astro` — SỬA (DataTable, Export, bee color)
28. `apps/web/src/pages/esg.astro` — SỬA (DataTable, KPIs, Export, bee color)
29. `apps/web/src/pages/chat.astro` — SỬA (bee color)
30. `apps/web/src/pages/maps.astro` — SỬA (bee color)
31. `apps/web/src/lib/api.ts` — SỬA (thêm 8 endpoint helpers)

**Tổng: 8 backend files + 31 frontend files = 39 files**

---

## BLOCKER
- elixir-dev: không blocked
- frontend-dev: blocked by elixir-dev on MAR-853 (API endpoints cần cho Settings page)

## DEPENDENCY ORDER
1. elixir-dev bắt đầu MAR-853 (backend) — 1-2h
2. frontend-dev bắt đầu MAR-850 (bee color) — song song, không cần API
3. frontend-dev bắt đầu MAR-852 (UI components) — song song, không cần API
4. frontend-dev bắt đầu MAR-851 (Settings page) — sau khi MAR-853 xong (API sẵn sàng) + MAR-852 xong (components)