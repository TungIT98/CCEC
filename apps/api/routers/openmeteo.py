"""
Open-Meteo Real Climate Data Endpoints
======================================
Fetches real climate data from Open-Meteo's Climate API.
"""

from datetime import datetime, timezone
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, Query, HTTPException
from pydantic import BaseModel

from services.openmeteo import (
    fetch_climate_data,
    fetch_current_weather,
    parse_climate_response,
    sync_climate_for_location,
    get_climate_summary,
    WORLD_CITIES,
    VIETNAM_BOUNDS,
)
from routers.auth import get_current_user

router = APIRouter(prefix="/climate/openmeteo", tags=["climate-openmeteo"])


class OpenMeteoResponse(BaseModel):
    status: str
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class ClimateSummaryResponse(BaseModel):
    status: str
    location: Dict[str, float]
    period: str
    temperature_max_avg: Optional[float] = None
    temperature_min_avg: Optional[float] = None
    temperature_mean_avg: Optional[float] = None
    precipitation_total: Optional[float] = None
    wind_speed_max_avg: Optional[float] = None
    humidity_mean_avg: Optional[float] = None


@router.get("/historical")
async def get_historical_climate(
    lat: float = Query(..., description="Latitude", ge=-90, le=90),
    lng: float = Query(..., description="Longitude", ge=-180, le=180),
    start_date: str = Query("1991-01-01", description="Start date (yyyy-mm-dd)"),
    end_date: str = Query("2020-12-31", description="End date (yyyy-mm-dd)"),
    _current_user=Depends(get_current_user),
) -> OpenMeteoResponse:
    """
    Fetch historical climate data from Open-Meteo Climate API.

    Uses 1991-2020 as default baseline period (WMO standard reference).
    Data available from 1950 to present.
    """
    try:
        data = await fetch_climate_data(
            lat=lat,
            lng=lng,
            start_date=start_date,
            end_date=end_date,
        )
        return OpenMeteoResponse(status="success", data=data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/current")
async def get_current_climate(
    lat: float = Query(..., description="Latitude", ge=-90, le=90),
    lng: float = Query(..., description="Longitude", ge=-180, le=180),
    past_days: int = Query(7, ge=0, le=92, description="Past days of history"),
    forecast_days: int = Query(7, ge=1, le=16, description="Forecast days"),
    _current_user=Depends(get_current_user),
) -> OpenMeteoResponse:
    """
    Fetch current weather + recent history + forecast.

    Combines real-time observations with forecast data.
    """
    try:
        data = await fetch_current_weather(
            lat=lat,
            lng=lng,
            past_days=past_days,
            forecast_days=forecast_days,
        )
        return OpenMeteoResponse(status="success", data=data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/summary", response_model=ClimateSummaryResponse)
async def get_climate_summary_endpoint(
    lat: float = Query(..., description="Latitude", ge=-90, le=90),
    lng: float = Query(..., description="Longitude", ge=-180, le=180),
    start_date: str = Query("1991-01-01", description="Start date (yyyy-mm-dd)"),
    end_date: str = Query("2020-12-31", description="End date (yyyy-mm-dd)"),
    _current_user=Depends(get_current_user),
) -> ClimateSummaryResponse:
    """
    Get climate summary (averages) for a location.

    Returns average temperature, precipitation totals, wind speed, and humidity
    for the specified period (default: 1991-2020 WMO baseline).
    """
    result = await get_climate_summary(
        lat=lat,
        lng=lng,
        start_date=start_date,
        end_date=end_date,
    )

    if result.get("status") == "error":
        raise HTTPException(status_code=500, detail=result.get("error"))

    daily = result.get("daily", {})

    return ClimateSummaryResponse(
        status="success",
        location=result.get("location", {}),
        period=result.get("period", ""),
        temperature_max_avg=daily.get("temperature_max_avg"),
        temperature_min_avg=daily.get("temperature_min_avg"),
        temperature_mean_avg=daily.get("temperature_mean_avg"),
        precipitation_total=daily.get("precipitation_total"),
        wind_speed_max_avg=daily.get("wind_speed_max_avg"),
        humidity_mean_avg=daily.get("humidity_mean_avg"),
    )


@router.get("/cities")
async def get_available_cities() -> Dict[str, Any]:
    """
    Get list of available world cities with coordinates.

    Returns a dictionary of city slugs with lat/lng/name.
    """
    return {
        "cities": WORLD_CITIES,
        "vietnam_bounds": VIETNAM_BOUNDS,
    }


@router.get("/vietnam")
async def get_vietnam_climate_summary(
    location: str = Query("hanoi", description="Location: hanoi, ho_chi_minh, central"),
    start_date: str = Query("1991-01-01", description="Start date"),
    end_date: str = Query("2020-12-31", description="End date"),
    _current_user=Depends(get_current_user),
) -> ClimateSummaryResponse:
    """
    Get climate summary for Vietnamese cities.

    Locations:
    - hanoi: Northern Vietnam (21.0285, 105.8542)
    - ho_chi_minh: Southern Vietnam (10.8231, 106.6297)
    - central: Central Vietnam (16.0, 108.0)
    """
    if location not in WORLD_CITIES:
        raise HTTPException(status_code=400, detail=f"Unknown location: {location}")

    city = WORLD_CITIES[location]
    return await get_climate_summary_endpoint(
        lat=city["lat"],
        lng=city["lng"],
        start_date=start_date,
        end_date=end_date,
    )


@router.get("/projections")
async def get_climate_projections(
    lat: float = Query(..., description="Latitude", ge=-90, le=90),
    lng: float = Query(..., description="Longitude", ge=-180, le=180),
    start_date: str = Query("2020-01-01", description="Start date (yyyy-mm-dd)"),
    end_date: str = Query("2050-12-31", description="End date (yyyy-mm-dd)"),
    _current_user=Depends(get_current_user),
) -> OpenMeteoResponse:
    """
    Get climate projections (future scenarios).

    Returns climate model projections for 2020-2050 period.
    """
    try:
        data = await fetch_climate_data(
            lat=lat,
            lng=lng,
            start_date=start_date,
            end_date=end_date,
        )
        return OpenMeteoResponse(status="success", data=data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))