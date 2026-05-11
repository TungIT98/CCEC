import time
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

from core.config import settings
from models.database import init_db
from routers import auth, users, climate_data, chat, maps, emissions

# --- Prometheus metrics ---
REQUEST_COUNT = Counter(
    "ccec_http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status_code"],
)
REQUEST_LATENCY = Histogram(
    "ccec_http_request_duration_seconds",
    "HTTP request latency",
    ["method", "endpoint"],
    buckets=(0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0),
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: initialize DB tables
    try:
        await init_db()
    except Exception:
        pass  # DB may not be available in dev without Docker
    yield
    # Shutdown


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="CCEC Climate Platform — Chiến lược Khí hậu Việt Nam",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Prometheus metrics middleware — registered after app is created
@app.middleware("http")
async def prometheus_middleware(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    duration = time.perf_counter() - start
    # Skip metrics endpoint to avoid recursion
    if request.url.path != "/metrics":
        REQUEST_COUNT.labels(
            method=request.method,
            endpoint=request.url.path,
            status_code=response.status_code,
        ).inc()
        REQUEST_LATENCY.labels(
            method=request.method,
            endpoint=request.url.path,
        ).observe(duration)
    return response


# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")
app.include_router(climate_data.router, prefix="/api/v1")
app.include_router(chat.router, prefix="/api/v1")
app.include_router(maps.router, prefix="/api/v1")
app.include_router(emissions.router, prefix="/api/v1")


@app.get("/health", tags=["health"])
async def health():
    return {"status": "ok", "version": settings.APP_VERSION}


@app.get("/api/v1/health", tags=["health"])
async def health_v1():
    return {"status": "ok", "version": settings.APP_VERSION}


@app.get("/metrics", tags=["monitoring"])
async def metrics():
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)