"""Time-series forecasting using Prophet (Facebook/Meta)."""
import os
from datetime import datetime, timezone
from typing import Literal, Optional

import pandas as pd

from core.config import settings

ForecastType = Literal["emissions", "carbon-price", "temperature"]


class ForecastResult:
    def __init__(
        self,
        forecast_type: ForecastType,
        horizon_days: int,
        forecast_df: pd.DataFrame,
        model_info: dict,
    ):
        self.forecast_type = forecast_type
        self.horizon_days = horizon_days
        self.forecast_df = forecast_df
        self.model_info = model_info

    def to_dict(self) -> dict:
        return {
            "type": self.forecast_type,
            "horizon_days": self.horizon_days,
            "model": self.model_info,
            "data": self.forecast_df.to_dict(orient="records"),
        }


def _load_vietnam_climate_df() -> pd.DataFrame:
    """Build a synthetic Vietnam emissions time-series for training."""
    dates = pd.date_range("2020-01-01", "2026-03-01", freq="MS")
    base = 280_000  # kt CO2e per month
    trend = 0.008   # ~8% annual growth
    noise = pd.Series(range(len(dates))).apply(
        lambda i: base * ((1 + trend) ** i) + (i % 12 - 6) * 800
    )
    df = pd.DataFrame({"ds": dates, "y": noise})
    return df


def _load_carbon_price_df() -> pd.DataFrame:
    """Build a synthetic carbon price time-series."""
    dates = pd.date_range("2020-01-01", "2026-03-01", freq="MS")
    base = 12.0  # USD/tCO2e
    trend = 0.015  # ~15% annual growth
    noise = pd.Series(range(len(dates))).apply(
        lambda i: base * ((1 + trend) ** i) + (i % 12 - 6) * 0.8
    )
    df = pd.DataFrame({"ds": dates, "y": noise})
    return df


def forecast_emissions(
    country_code: str = "VNM",
    horizon_days: int = 365,
) -> ForecastResult:
    """Forecast Vietnam CO2 emissions for `horizon_days` ahead."""
    try:
        from prophet import Prophet
    except ImportError:
        return _mock_forecast("emissions", horizon_days)

    df = _load_vietnam_climate_df()
    m = Prophet(yearly_seasonality=True, weekly_seasonality=False, daily_seasonality=False)
    m.fit(df)

    future = m.make_future_dataframe(periods=horizon_days)
    fc = m.predict(future)

    fc_subset = fc[fc["ds"] > df["ds"].max()].copy()
    fc_subset = fc_subset.rename(columns={"yhat": "emissions_kt", "yhat_lower": "lower", "yhat_upper": "upper"})

    return ForecastResult(
        forecast_type="emissions",
        horizon_days=horizon_days,
        forecast_df=fc_subset[["ds", "emissions_kt", "lower", "upper"]].reset_index(drop=True),
        model_info={
            "model": "Prophet",
            "country": country_code,
            "training_from": "2020-01-01",
            "training_to": "2026-03-01",
        },
    )


def forecast_carbon_price(
    standard_type: str = "VER",
    vintage: Optional[int] = None,
    horizon_days: int = 90,
) -> ForecastResult:
    """Forecast carbon credit price for `horizon_days` ahead."""
    try:
        from prophet import Prophet
    except ImportError:
        return _mock_forecast("carbon-price", horizon_days)

    df = _load_carbon_price_df()
    m = Prophet(yearly_seasonality=True, weekly_seasonality=False, daily_seasonality=False)
    m.fit(df)

    future = m.make_future_dataframe(periods=horizon_days)
    fc = m.predict(future)

    fc_subset = fc[fc["ds"] > df["ds"].max()].copy()
    fc_subset = fc_subset.rename(columns={"yhat": "price_usd_tCO2e", "yhat_lower": "lower", "yhat_upper": "upper"})

    return ForecastResult(
        forecast_type="carbon-price",
        horizon_days=horizon_days,
        forecast_df=fc_subset[["ds", "price_usd_tCO2e", "lower", "upper"]].reset_index(drop=True),
        model_info={
            "model": "Prophet",
            "standard_type": standard_type,
            "vintage": vintage,
            "training_from": "2020-01-01",
            "training_to": "2026-03-01",
        },
    )


def forecast_temperature(
    station_id: str = "Hanoi",
    horizon_days: int = 365,
) -> ForecastResult:
    """Forecast average temperature for `horizon_days` ahead (synthetic)."""
    try:
        from prophet import Prophet
    except ImportError:
        return _mock_forecast("temperature", horizon_days)

    # Synthetic temperature: sinusoidal seasonal pattern
    dates = pd.date_range("2020-01-01", "2026-03-01", freq="MS")
    avg_temp = 26.0  # Hanoi annual average °C
    amplitude = 6.0   # seasonal swing
    trend = 0.005    # slight warming trend
    temp = dates.apply(
        lambda d: avg_temp + amplitude * (1 if d.month in [4, 5, 6] else 0.5) * (1 + trend)
        + 2 * (d.month % 12 / 12 - 0.5)
    )
    df = pd.DataFrame({"ds": dates, "y": temp})

    m = Prophet(yearly_seasonality=True, weekly_seasonality=False, daily_seasonality=False)
    m.fit(df)

    future = m.make_future_dataframe(periods=horizon_days)
    fc = m.predict(future)

    fc_subset = fc[fc["ds"] > df["ds"].max()].copy()
    fc_subset = fc_subset.rename(columns={"yhat": "temp_celsius", "yhat_lower": "lower", "yhat_upper": "upper"})

    return ForecastResult(
        forecast_type="temperature",
        horizon_days=horizon_days,
        forecast_df=fc_subset[["ds", "temp_celsius", "lower", "upper"]].reset_index(drop=True),
        model_info={
            "model": "Prophet",
            "station": station_id,
            "training_from": "2020-01-01",
            "training_to": "2026-03-01",
        },
    )


def _mock_forecast(ftype: ForecastType, horizon_days: int) -> ForecastResult:
    """Return mock forecast when Prophet is not installed."""
    now = datetime.now(timezone.utc)
    dates = pd.date_range(now, periods=min(horizon_days // 7, 12), freq="7D")
    values = {"emissions": 290_000, "carbon-price": 18.0, "temperature": 28.0}[ftype]
    unit = {"emissions": "kt CO2e", "carbon-price": "USD/tCO2e", "temperature": "°C"}[ftype]

    col = {"emissions": "emissions_kt", "carbon-price": "price_usd_tCO2e", "temperature": "temp_celsius"}[ftype]
    df = pd.DataFrame({"ds": dates, col: [values] * len(dates), "lower": [values * 0.9] * len(dates), "upper": [values * 1.1] * len(dates)})

    return ForecastResult(
        forecast_type=ftype,
        horizon_days=horizon_days,
        forecast_df=df,
        model_info={"model": "mock", "note": "Install prophet==1.1.5 for real forecasts"},
    )
