# CCEC Climate Platform — Chiến lược Khí hậu Việt Nam

Open climate data intelligence platform for Vietnam's carbon markets, NDC tracking, and climate policy analysis.

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│  apps/web/         Astro 4.0 + Svelte 5 + TailwindCSS  │
│  (Frontend)        Port 3000                           │
└──────────────────────────┬──────────────────────────────┘
                           │ REST / WebSocket
┌──────────────────────────▼──────────────────────────────┐
│  apps/api/         FastAPI (Python 3.12)                │
│  (Backend)          Port 8000 /docs (Swagger UI)        │
│                     - Auth (JWT)                         │
│                     - Climate data + forecast            │
│                     - AI chat (Groq/DeepSeek/PortKey)    │
│                     - Map tile proxy (Mapbox)            │
└──────┬─────────────────┬──────────────────┬──────────────┘
       │                 │                  │
  ┌────▼────┐     ┌─────▼─────┐     ┌──────▼──────┐
  │PostgreSQL│     │  Redis    │     │ AI Gateway  │
  │+PostGIS  │     │  7.2      │     │ Groq/DeepSeek│
  │+TimescaleDB│   │  Port 5432│     │ Port 6379   │
  └─────────┘     └───────────┘     └─────────────┘
```

## Tech Stack

| Layer      | Technology                               |
|------------|-------------------------------------------|
| Frontend   | Astro 4.0 + Svelte 5 + TailwindCSS 4.0   |
| Backend    | FastAPI (Python 3.12)                     |
| AI         | Groq (primary), DeepSeek (fallback), Claude (PortKey) |
| Database   | PostgreSQL 16 + PostGIS + TimescaleDB    |
| Cache      | Redis 7.2                                 |
| Maps       | Mapbox GL JS + Deck.gl + Kepler.gl       |
| Charts     | Apache ECharts + D3.js                    |
| ML         | PyTorch 2.0 + Transformers + Prophet     |
| Deploy     | Docker + Coolify                          |

## Quick Start

### Prerequisites

- Node.js 20+ with pnpm
- Python 3.12+
- Docker & Docker Compose

### 1. Clone & install

```bash
git clone <repo-url>
cd ccec-climate-platform
pnpm install
```

### 2. Environment

```bash
cp .env.example .env
# Edit .env — at minimum set JWT_SECRET_KEY and DATABASE_URL
```

### 3. Start infrastructure

```bash
docker compose -f infra/docker/docker-compose.yml up -d
```

### 4. Start API

```bash
pnpm dev:api
# → http://localhost:8000/docs  (Swagger UI)
# → http://localhost:8000/health → {"status":"ok"}
```

### 5. Start frontend

```bash
pnpm dev:web
# → http://localhost:3000
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL async connection string | `postgresql+asyncpg://...` |
| `DATABASE_URL_SYNC` | PostgreSQL sync connection string | `postgresql+psycopg2://...` |
| `REDIS_URL` | Redis connection string | `redis://localhost:6379/0` |
| `JWT_SECRET_KEY` | **Required.** Sign JWT tokens — use 32+ random chars | `CHANGE_ME_IN_PRODUCTION` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | JWT access token TTL | `15` |
| `REFRESH_TOKEN_EXPIRE_DAYS` | JWT refresh token TTL | `7` |
| `OPENAI_API_KEY` | Groq API key | - |
| `OPENAI_BASE_URL` | Groq endpoint | `https://api.groq.com/openai/v1` |
| `OPENAI_MODEL` | Groq model | `llama-3.3-70b-versatile` |
| `DEEPSEEK_API_KEY` | DeepSeek API key (fallback) | - |
| `DEEPSEEK_BASE_URL` | DeepSeek endpoint | `https://api.deepseek.com/v1` |
| `DEEPSEEK_MODEL` | DeepSeek model | `deepseek-chat` |
| `PORTKEY_API_KEY` | PortKey API key (Claude via PortKey) | - |
| `PORTKEY_BASE_URL` | PortKey endpoint | `https://api.portkey.ai/v1` |
| `AI_PROVIDER` | Primary AI provider | `groq` |
| `MAPBOX_ACCESS_TOKEN` | Mapbox token for satellite tiles | - |
| `DEBUG` | Enable debug mode | `false` |

## API Endpoints

All endpoints prefixed with `/api/v1`. See full docs at `/docs` (Swagger UI) or `/redoc`.

### Auth
- `POST /api/v1/auth/register` — Register new user
- `POST /api/v1/auth/login` — Login (OAuth2 password flow)
- `POST /api/v1/auth/login/json` — Login (JSON body)
- `POST /api/v1/auth/refresh` — Refresh access token

### Users
- `GET /api/v1/users/me` — Current user profile
- `PUT /api/v1/users/me` — Update profile
- `GET /api/v1/users` — List users (admin)

### Climate Data
- `GET /api/v1/climate/data` — Historical climate data (lat/lng required)
- `GET /api/v1/climate/forecast` — Climate forecast (location required)

### AI Chat
- `POST /api/v1/chat` — Chat with AI assistant (authenticated)

### Maps
- `GET /api/v1/maps/tiles/{z}/{x}/{y}` — Map tile proxy (authenticated)

### Health
- `GET /health` → `{"status":"ok"}`
- `GET /api/v1/health` → `{"status":"ok"}`
- `GET /metrics` → Prometheus metrics

## Docker Deployment

```bash
# Build and run full stack
docker compose -f infra/docker/docker-compose.yml up --build

# Run in background
docker compose -f infra/docker/docker-compose.yml up -d

# Stop
docker compose -f infra/docker/docker-compose.yml down
```

### Services

| Service | Port | Description |
|---------|------|-------------|
| `api` | 8000 | FastAPI backend |
| `web` | 3000 | Astro frontend |
| `postgres` | 5432 | PostgreSQL 16 + PostGIS |
| `redis` | 6379 | Redis 7.2 |
| `prometheus` | 9090 | Metrics collection |
| `grafana` | 3001 | Dashboards |

## Coolify Deployment

See `infra/coolify/` for Coolify deployment configurations.

## Monitoring

- **Prometheus**: `http://localhost:9090` — metrics collection
- **Grafana**: `http://localhost:3001` — dashboards (admin/admin)
- **Health**: `GET /health` — returns `{"status":"ok"}`
- **Metrics**: `GET /metrics` — Prometheus-format metrics

## Project Structure

```
ccec-climate-platform/
├── apps/
│   ├── api/                  # FastAPI backend (Python 3.12)
│   │   ├── core/             # Config, settings
│   │   ├── models/           # SQLAlchemy entities + Pydantic schemas
│   │   ├── routers/          # API route modules
│   │   ├── services/         # Business logic (auth, AI, climate)
│   │   └── src/main.py       # App entry point
│   └── web/                  # Astro + Svelte frontend
│       └── astro.config.mjs  # Astro config
├── packages/
│   ├── ai-client/            # OpenAI-compatible TypeScript client
│   └── shared/               # Shared types and utilities
├── infra/
│   ├── docker/               # Dockerfiles + docker-compose.yml
│   └── coolify/              # Coolify deployment configs
├── knowledge/
│   ├── climate/              # Climate policy & carbon market KB
│   └── crypto/               # Crypto knowledge base
└── .env.example              # Environment variable template
```

## Development

```bash
# Install dependencies
pnpm install

# Run all services (requires Docker)
docker compose -f infra/docker/docker-compose.yml up -d

# Run API only
pnpm dev:api

# Run frontend only
pnpm dev:web

# Build all
pnpm build

# Lint all
pnpm lint
```

## Security

- JWT access tokens expire in 15 minutes
- Refresh tokens rotate on each use
- All secrets via environment variables — never committed
- CORS: restrict `allow_origins` in production
- Input validation via Pydantic on all endpoints

## License

Proprietary — CCEC Climate Platform