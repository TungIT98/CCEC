from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class RenewableEnergyResponse(BaseModel):
    id: int
    country_name: str
    country_code: str
    energy_type: str
    capacity_mw: float
    generation_gwh: Optional[float] = None
    installed_year: int
    source: Optional[str] = None
    fetched_at: datetime

    model_config = {"from_attributes": True}


class RenewableEnergyQuery(BaseModel):
    country_code: Optional[str] = None
    energy_type: Optional[str] = None  # solar | wind | hydro | geothermal | biomass
    year_min: Optional[int] = None
    year_max: Optional[int] = None
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=50, ge=1, le=200)


class CapacityByEnergyType(BaseModel):
    energy_type: str
    total_capacity_mw: float
    count_records: int


class CapacityResponse(BaseModel):
    records: list[RenewableEnergyResponse]
    by_energy_type: list[CapacityByEnergyType]
    total_count: int


class TrendsResponse(BaseModel):
    country_code: str
    country_name: str
    energy_type: str
    yearly_generation_gwh: float
    year: int


class CountryEnergyDetail(BaseModel):
    country_code: str
    country_name: str
    records: list[RenewableEnergyResponse]
    total_capacity_mw: float
    by_energy_type: dict[str, float]  # energy_type → total capacity