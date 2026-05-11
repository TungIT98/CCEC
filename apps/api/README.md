# CCEC Climate Platform — FastAPI Backend

## Setup

```bash
cd apps/api
uv sync
uv run fastapi dev main.py --port 8000
```

## API Base URL

`http://localhost:8000`

## Docs

`http://localhost:8000/docs` (Swagger UI)
`http://localhost:8000/redoc` (ReDoc)

## Docker

```bash
docker compose -f ../../infra/docker/docker-compose.yml up api
```