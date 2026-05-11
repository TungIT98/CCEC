import random
from datetime import datetime, timedelta, timezone
from typing import List, Optional
from models.schemas import ClimateDataPoint, ForecastPoint


def generate_climate_data(
    lat: float,
    lng: float,
    start: Optional[datetime] = None,
    end: Optional[datetime] = None,
    limit: int = 100,
) -> List[ClimateDataPoint]:
    """Generate simulated climate data for a bounding box / time range."""
    if end is None:
        end = datetime.now(timezone.utc)
    if start is None:
        start = end - timedelta(days=30)

    points = []
    current = start
    step = (end - start) / min(limit, 100) if limit > 0 else timedelta(hours=6)
    step = max(step, timedelta(hours=1))

    # Vietnam-centered defaults
    lat = lat if lat else 16.0
    lng = lng if lng else 108.0

    while current <= end and len(points) < limit:
        month = current.month
        # Tropical seasonal temps (°C)
        base_temp = 22.0 + 8.0 * abs(lat) / 90.0
        seasonal = 4.0 * (1 if month in [4, 5, 6, 7, 8, 9] else -1)
        temperature = round(base_temp + seasonal + random.uniform(-3, 3), 2)

        points.append(
            ClimateDataPoint(
                timestamp=current,
                temperature=temperature,
                humidity=round(random.uniform(60, 95), 1),
                precipitation=round(random.uniform(0, 25) if month in [6, 7, 8, 9, 10] else random.uniform(0, 5), 2),
                wind_speed=round(random.uniform(0, 20), 1),
                co2_concentration=round(420 + random.uniform(-5, 15), 1),
                lat=round(lat + random.uniform(-0.5, 0.5), 4),
                lng=round(lng + random.uniform(-0.5, 0.5), 4),
            )
        )
        current += step

    return points


def generate_forecast(location: str, lat: Optional[float], lng: Optional[float], days: int = 7) -> List[ForecastPoint]:
    """Generate simulated forecast data."""
    results = []
    base_date = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    base_temp = 22.0 + 8.0 * (abs(lat or 16.0) / 90.0)

    for i in range(days):
        date = base_date + timedelta(days=i)
        is_wet = date.month in [6, 7, 8, 9, 10]
        results.append(
            ForecastPoint(
                date=date.strftime("%Y-%m-%d"),
                temperature_high=round(base_temp + random.uniform(5, 12), 1),
                temperature_low=round(base_temp + random.uniform(0, 5), 1),
                precipitation_probability=round(random.uniform(0.3, 0.9), 2) if is_wet else round(random.uniform(0.0, 0.3), 2),
                co2_forecast=round(420 + i * 0.2 + random.uniform(-2, 2), 1),
            )
        )

    return results
