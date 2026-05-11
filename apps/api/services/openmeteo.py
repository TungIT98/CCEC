"""
Open-Meteo Climate API Integration Service
==========================================
Fetches real climate data from Open-Meteo's Climate API.

API Docs: https://open-meteo.com/en/docs/climate-api
- Historical + projected climate data (1950-2050)
- Multiple climate models (CMCC, FGOALS, HiRAM, MRI, EC_Earth, MPI, NICAM)
- Daily aggregations: temperature, humidity, wind, precipitation, radiation, etc.
"""

import httpx
from datetime import datetime
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session

from models.entities import ClimateRecord
from models.schemas import ClimateDataPoint

# Open-Meteo Climate API base URL
OPEN_METEO_CLIMATE_URL = "https://climate-api.open-meteo.com/v1/climate"

# Open-Meteo Weather API (for current/recent data)
OPEN_METEO_WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

# Supported climate models
CLIMATE_MODELS = [
    "CMCC_CM2_VHR4",
    "FGOALS_f3_H",
    "HiRAM_SIT_HR",
    "MRI_AGCM3_2_S",
    "EC_Earth3P_HR",
    "MPI_ESM1_2_XR",
    "NICAM16_8S",
]

# Available daily variables
DAILY_VARIABLES = [
    "temperature_2m_max",
    "temperature_2m_min",
    "temperature_2m_mean",
    "relative_humidity_2m_max",
    "relative_humidity_2m_min",
    "relative_humidity_2m_mean",
    "wind_speed_10m_mean",
    "wind_speed_10m_max",
    "precipitation_sum",
    "rain_sum",
    "snowfall_sum",
    "cloud_cover_mean",
    "shortwave_radiation_sum",
    "pressure_msl_mean",
    "soil_moisture_0_to_10cm_mean",
    "et0_fao",
]


async def fetch_climate_data(
    lat: float,
    lng: float,
    start_date: str = "1950-01-01",
    end_date: str = "2050-12-31",
    models: Optional[List[str]] = None,
    variables: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """
    Fetch climate data from Open-Meteo Climate API.

    Args:
        lat: Latitude (WGS84)
        lng: Longitude (WGS84)
        start_date: Start date (ISO format yyyy-mm-dd)
        end_date: End date (ISO format yyyy-mm-dd)
        models: List of climate models to use (default: all 7 models)
        variables: List of daily variables to fetch (default: key variables)

    Returns:
        Dict with climate data from multiple models
    """
    if models is None:
        models = CLIMATE_MODELS

    if variables is None:
        variables = [
            "temperature_2m_max",
            "temperature_2m_min",
            "temperature_2m_mean",
            "precipitation_sum",
            "wind_speed_10m_max",
            "relative_humidity_2m_mean",
        ]

    params = {
        "latitude": lat,
        "longitude": lng,
        "start_date": start_date,
        "end_date": end_date,
        "models": ",".join(models),
        "daily": ",".join(variables),
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(OPEN_METEO_CLIMATE_URL, params=params)
        response.raise_for_status()
        return response.json()


async def fetch_current_weather(
    lat: float,
    lng: float,
    past_days: int = 7,
    forecast_days: int = 7,
) -> Dict[str, Any]:
    """
    Fetch current weather + recent history + forecast from Open-Meteo Weather API.

    Args:
        lat: Latitude
        lng: Longitude
        past_days: Days of historical data (0-92)
        forecast_days: Days of forecast (1-16)

    Returns:
        Dict with current, hourly, daily data
    """
    params = {
        "latitude": lat,
        "longitude": lng,
        "past_days": past_days,
        "forecast_days": forecast_days,
        "hourly": "temperature_2m,relative_humidity_2m,precipitation,windspeed_10m,weathercode",
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,precipitation_probability_max",
        "timezone": "auto",
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(OPEN_METEO_WEATHER_URL, params=params)
        response.raise_for_status()
        return response.json()


def parse_climate_response(data: Dict[str, Any]) -> List[ClimateDataPoint]:
    """
    Parse Open-Meteo Climate API response into ClimateDataPoint list.

    Args:
        data: JSON response from Open-Meteo Climate API

    Returns:
        List of ClimateDataPoint objects
    """
    daily = data.get("daily", {})
    times = daily.get("time", [])

    if not times:
        return []

    points = []
    for i, timestamp in enumerate(times):
        point = ClimateDataPoint(
            timestamp=datetime.fromisoformat(timestamp),
            temperature=daily.get("temperature_2m_mean", [None] * len(times))[i]
            if i < len(daily.get("temperature_2m_mean", []))
            else None,
            humidity=daily.get("relative_humidity_2m_mean", [None] * len(times))[i]
            if i < len(daily.get("relative_humidity_2m_mean", []))
            else None,
            precipitation=daily.get("precipitation_sum", [None] * len(times))[i]
            if i < len(daily.get("precipitation_sum", []))
            else None,
            wind_speed=daily.get("wind_speed_10m_max", [None] * len(times))[i]
            if i < len(daily.get("wind_speed_10m_max", []))
            else None,
            co2_concentration=None,  # Not available in Open-Meteo
            lat=data.get("latitude", 0),
            lng=data.get("longitude", 0),
        )
        points.append(point)

    return points


def save_climate_records(db: Session, records: List[ClimateRecord]) -> int:
    """
    Save climate records to database.

    Args:
        db: Database session
        records: List of ClimateRecord objects

    Returns:
        Number of records saved
    """
    count = 0
    for record in records:
        db.add(record)
        count += 1

    db.commit()
    return count


async def sync_climate_for_location(
    db: Session,
    lat: float,
    lng: float,
    location_name: str,
    start_date: str = "1950-01-01",
    end_date: str = "2050-12-31",
) -> Dict[str, Any]:
    """
    Sync climate data for a specific location.

    Args:
        db: Database session
        lat: Latitude
        lng: Longitude
        location_name: Name identifier for logging
        start_date: Start date
        end_date: End date

    Returns:
        Dict with sync results
    """
    try:
        # Fetch climate data
        data = await fetch_climate_data(
            lat=lat,
            lng=lng,
            start_date=start_date,
            end_date=end_date,
        )

        # Parse into ClimateDataPoints
        points = parse_climate_response(data)

        # Convert to ClimateRecord and save
        records = []
        for point in points:
            record = ClimateRecord(
                lat=point.lat,
                lng=point.lng,
                timestamp=point.timestamp,
                temperature=point.temperature,
                humidity=point.humidity,
                precipitation=point.precipitation,
                wind_speed=point.wind_speed,
                co2_concentration=point.co2_concentration,
                source="open-meteo",
            )
            records.append(record)

        # Batch save (commit every 1000 records to avoid memory issues)
        batch_size = 1000
        total_saved = 0
        for i in range(0, len(records), batch_size):
            batch = records[i : i + batch_size]
            for record in batch:
                db.add(record)
            db.commit()
            total_saved += len(batch)

        return {
            "status": "success",
            "location": location_name,
            "lat": lat,
            "lng": lng,
            "records_synced": total_saved,
            "date_range": f"{start_date} to {end_date}",
        }

    except httpx.HTTPError as e:
        return {
            "status": "error",
            "location": location_name,
            "error": f"HTTP Error: {str(e)}",
        }
    except Exception as e:
        return {
            "status": "error",
            "location": location_name,
            "error": f"Error: {str(e)}",
        }


async def get_climate_summary(
    lat: float,
    lng: float,
    start_date: str = "1991-01-01",
    end_date: str = "2020-12-31",
) -> Dict[str, Any]:
    """
    Get climate summary (averages) for a location using historical baseline period.

    Uses 1991-2020 as historical baseline (standard WMO reference period).

    Args:
        lat: Latitude
        lng: Longitude
        start_date: Start of baseline period
        end_date: End of baseline period

    Returns:
        Dict with climate summary statistics
    """
    try:
        data = await fetch_climate_data(
            lat=lat,
            lng=lng,
            start_date=start_date,
            end_date=end_date,
            variables=[
                "temperature_2m_max",
                "temperature_2m_min",
                "temperature_2m_mean",
                "precipitation_sum",
                "wind_speed_10m_max",
                "relative_humidity_2m_mean",
            ],
        )

        daily = data.get("daily", {})

        # Calculate averages
        def safe_avg(arr, idx):
            if idx < len(arr) and arr[idx] is not None:
                return round(sum(arr) / len(arr), 2) if arr else None
            return None

        return {
            "status": "success",
            "location": {"lat": lat, "lng": lng},
            "period": f"{start_date} to {end_date}",
            "climate_models": data.get("models", []),
            "daily": {
                "temperature_max_avg": safe_avg(daily.get("temperature_2m_max", []), 0),
                "temperature_min_avg": safe_avg(daily.get("temperature_2m_min", []), 0),
                "temperature_mean_avg": safe_avg(daily.get("temperature_2m_mean", []), 0),
                "precipitation_total": round(sum(daily.get("precipitation_sum", [0])), 2),
                "wind_speed_max_avg": safe_avg(daily.get("wind_speed_10m_max", []), 0),
                "humidity_mean_avg": safe_avg(daily.get("relative_humidity_2m_mean", []), 0),
            },
        }

    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
        }


# ─── Convenience functions for common locations ─────────────────────────────────

VIETNAM_BOUNDS = {
    "north": {"lat": 23.39, "lng": 108.33},  # Lang Son
    "south": {"lat": 8.41, "lng": 104.97},    # Ca Mau
    "central": {"lat": 16.0, "lng": 108.0},   # Da Nang
}

WORLD_CITIES = {
    "hanoi": {"lat": 21.0285, "lng": 105.8542, "name": "Hanoi, Vietnam"},
    "ho_chi_minh": {"lat": 10.8231, "lng": 106.6297, "name": "Ho Chi Minh City, Vietnam"},
    "bangkok": {"lat": 13.7563, "lng": 100.5018, "name": "Bangkok, Thailand"},
    "singapore": {"lat": 1.3521, "lng": 103.8198, "name": "Singapore"},
    "jakarta": {"lat": -6.2088, "lng": 106.8456, "name": "Jakarta, Indonesia"},
    "manila": {"lat": 14.5995, "lng": 120.9842, "name": "Manila, Philippines"},
    "tokyo": {"lat": 35.6762, "lng": 139.6503, "name": "Tokyo, Japan"},
    "beijing": {"lat": 39.9042, "lng": 116.4074, "name": "Beijing, China"},
    "london": {"lat": 51.5074, "lng": -0.1278, "name": "London, UK"},
    "new_york": {"lat": 40.7128, "lng": -74.0060, "name": "New York, USA"},
    "sydney": {"lat": -33.8688, "lng": 151.2093, "name": "Sydney, Australia"},
}