# CCEC Climate Platform — Local PostgreSQL Setup

## What was done

PostgreSQL 17 (from Paperclip embedded Postgres) was initialized as a standalone server for the CCEC platform.

- **Data dir:** `C:\Users\PC\ccec-pg-data`
- **Port:** 5432
- **Database:** `ccec`
- **User:** `postgres` (no password — trust auth)
- **Tables:** `users`

## Start/Stop Commands

```powershell
# Start
& "C:/Users/PC/AppData/Roaming/npm/node_modules/paperclipai/node_modules/@embedded-postgres/windows-x64/native/bin/pg_ctl.exe" -D "C:/Users/PC/ccec-pg-data" -l "C:/Users/PC/ccec-pg-data/logfile" -o "-p 5432" start

# Stop
& "C:/Users/PC/AppData/Roaming/npm/node_modules/paperclipai/node_modules/@embedded-postgres/windows-x64/native/bin/pg_ctl.exe" -D "C:/Users/PC/ccec-pg-data" stop
```

## Auth API — Verified Working

- `POST /api/v1/auth/register` → 201, creates user
- `POST /api/v1/auth/login/json` → 200, returns JWT tokens (60min expiry)
- `POST /api/v1/auth/login` (form) → 200, returns JWT tokens
- `POST /api/v1/auth/refresh` → 200, returns new token pair

## Persistence

Server stops on computer restart. Re-run the start command above to bring it back.

## Alternative: Docker (recommended for production)

```powershell
cd E:/ccec-climate-platform/infra/docker
docker compose up -d postgres
```

Then update `apps/api/core/config.py` `DATABASE_URL` to point to the Docker service.

## Root Cause

No PostgreSQL instance was listening on port 5432. The only running PostgreSQL was Paperclip's embedded instance on port 54329, which uses internal credentials and is not accessible from external clients.