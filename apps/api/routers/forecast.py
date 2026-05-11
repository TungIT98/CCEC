"""Prophet forecasting endpoints."""
from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from typing import Optional, Literal

from services.forecast import forecast_emissions, forecast_carbon_price, forecast_temperature
from routers.auth import get_current_user

router = APIRouter(prefix="/ai/forecast", tags=["ai-forecast"])


class EmissionsForecastRequest(BaseModel):
    country_code: str = Field(default="VNM", max_length=3)
    horizon_days: int = Field(default=365, ge=7, le=730)


class CarbonPriceForecastRequest(BaseModel):
    standard_type: str = Field(default="VER")
    vintage: Optional[int] = Field(default=None)
    horizon_days: int = Field(default=90, ge=7, le=365)


class TemperatureForecastRequest(BaseModel):
    station_id: str = Field(default="Hanoi")
    horizon_days: int = Field(default=365, ge=7, le=730)


@router.post("/emissions")
async def forecast_emissions_endpoint(
    body: EmissionsForecastRequest,
    _: None = Depends(get_current_user),
):
    """Forecast CO2 emissions for `horizon_days` ahead."""
    result = forecast_emissions(
        country_code=body.country_code,
        horizon_days=body.horizon_days,
    )
    return result.to_dict()


@router.post("/carbon-price")
async def forecast_carbon_price_endpoint(
    body: CarbonPriceForecastRequest,
    _: None = Depends(get_current_user),
):
    """Forecast carbon credit price for `horizon_days` ahead."""
    result = forecast_carbon_price(
        standard_type=body.standard_type,
        vintage=body.vintage,
        horizon_days=body.horizon_days,
    )
    return result.to_dict()


@router.post("/temperature")
async def forecast_temperature_endpoint(
    body: TemperatureForecastRequest,
    _: None = Depends(get_current_user),
):
    """Forecast average temperature for `horizon_days` ahead."""
    result = forecast_temperature(
        station_id=body.station_id,
        horizon_days=body.horizon_days,
    )
    return result.to_dict()