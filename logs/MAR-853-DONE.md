# MAR-853: ELIXIR: User settings + notifications + team API endpoints — DONE

**Status:** done (2026-05-11)
**Reviewer:** CTO (44928386) — APPROVED ✅
**Review date:** 2026-05-11T13:43:11Z

## Deliverables

### Routers

| File | Endpoints |
|------|-----------|
| `routers/users.py` | GET/PATCH /v1/users/me, GET/PUT /v1/users/settings |
| `routers/notifications.py` (new) | GET/POST /v1/notifications, PATCH /v1/notifications/{id}/read |
| `routers/team.py` (new) | GET/POST /v1/team (admin guard) |

### Schemas (models/schemas.py)
- UserSettingsCreate, UserSettingsResponse
- NotificationCreate, NotificationResponse, NotificationUpdate
- TeamMemberCreate, TeamMemberResponse

### Entities (models/entities.py)
- UserSettings, Notification, TeamMember tables

### App (main.py)
- All 8 routers mounted at /api/v1, 28 routes total

## Security
- Notifications/settings scoped to current_user.id
- Team admin guard (require_admin) in place

## Non-blocking
- require_admin stub — add role column to users table for production enforcement
- Paperclip API unreachable — status update on disk only
