from datetime import datetime, timezone
from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from models.database import get_db
from models.schemas import ClimateDataPoint, ForecastPoint, ForecastRequest
from services.climate import generate_climate_data, generate_forecast
from routers.auth import get_current_user

router = APIRouter(prefix="/climate", tags=["climate"])


@router.get("/data", response_model=List[ClimateDataPoint])
async def get_climate_data(
    lat: float = Query(..., description="Latitude"),
    lng: float = Query(..., description="Longitude"),
    start: Optional[datetime] = Query(None, description="Start datetime (ISO 8601)"),
    end: Optional[datetime] = Query(None, description="End datetime (ISO 8601)"),
    limit: int = Query(100, ge=1, le=1000, description="Max records to return"),
    _current_user=Depends(get_current_user),
):
    return generate_climate_data(lat=lat, lng=lng, start=start, end=end, limit=limit)


@router.get("/forecast", response_model=List[ForecastPoint])
async def get_forecast(
    location: str = Query(..., description="Location name"),
    lat: Optional[float] = Query(None, description="Latitude override"),
    lng: Optional[float] = Query(None, description="Longitude override"),
    days: int = Query(7, ge=1, le=30, description="Forecast days"),
    _current_user=Depends(get_current_user),
):
    return generate_forecast(location=location, lat=lat, lng=lng, days=days)
