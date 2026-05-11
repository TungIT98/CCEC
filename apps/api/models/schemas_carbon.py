from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class CarbonCreditBase(BaseModel):
    name: str
    standard_type: str  # VER | CER | GOLD
    project_type: str
    vintage: int
    unit_price: float
    currency: str = "USD"
    registry: Optional[str] = None
    project_url: Optional[str] = None
    credit_class: Optional[str] = None
    methodology: Optional[str] = None
    estimated_ERt: Optional[float] = None
    verified_ERt: Optional[float] = None
    issued_at: Optional[datetime] = None
    expired_at: Optional[datetime] = None
    is_retired: bool = False
    country_code: Optional[str] = None
    country_name: Optional[str] = None


class CarbonCreditCreate(CarbonCreditBase):
    pass


class CarbonCreditResponse(CarbonCreditBase):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}


class CarbonPriceBase(BaseModel):
    standard_type: str
    vintage: int
    price_per_tCO2e: float
    currency: str = "USD"
    source_url: Optional[str] = None


class CarbonPriceCreate(CarbonPriceBase):
    pass


class CarbonPriceResponse(CarbonPriceBase):
    id: int
    fetched_at: datetime

    model_config = {"from_attributes": True}


class CarbonPriceHistoryResponse(BaseModel):
    id: int
    standard_type: str
    vintage: int
    price_per_tCO2e: float
    currency: str
    source_url: Optional[str] = None
    fetched_at: datetime

    model_config = {"from_attributes": True}


# ── Query ──────────────────────────────────────────────────────────────────────

class CarbonCreditsQuery(BaseModel):
    standard_type: Optional[str] = None
    vintage_min: Optional[int] = None
    vintage_max: Optional[int] = None
    project_type: Optional[str] = None
    country_code: Optional[str] = None
    unit_price_min: Optional[float] = None
    unit_price_max: Optional[float] = None
    is_retired: Optional[bool] = None
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)


class CarbonPricesQuery(BaseModel):
    standard_type: Optional[str] = None
    vintage: Optional[int] = None
    source_url: Optional[str] = None
    after: Optional[datetime] = None
    limit: int = Field(default=50, ge=1, le=200)


# ── Policies ───────────────────────────────────────────────────────────────────

class PolicyBase(BaseModel):
    country_name: str
    country_code: str
    policy_name: str
    policy_type: str
    instrument_type: Optional[str] = None
    sector: Optional[str] = None
    coverage: Optional[str] = None
    economy_wide: Optional[str] = None
    carbon_pricing_existence: Optional[str] = None
    pricing_existence_notes: Optional[str] = None
    carbon_price_min_tCO2e: Optional[float] = None
    carbon_price_max_tCO2e: Optional[float] = None
    currency: str = "USD"
    link_source: Optional[str] = None


class PolicyCreate(PolicyBase):
    pass


class PolicyResponse(PolicyBase):
    id: int
    fetched_at: datetime

    model_config = {"from_attributes": True}


class PolicyQuery(BaseModel):
    country_code: Optional[str] = None
    policy_type: Optional[str] = None
    sector: Optional[str] = None
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)


# ── NDC ────────────────────────────────────────────────────────────────────────

class NdcTrackingBase(BaseModel):
    country_name: str
    country_code: str
    submission_type: Optional[str] = None
    status: str
    latest_submission_date: Optional[datetime] = None
    link_NDC: Optional[str] = None
    fetch_link: Optional[str] = None


class NdcTrackingCreate(NdcTrackingBase):
    pass


class NdcTrackingResponse(NdcTrackingBase):
    id: int
    fetched_at: datetime

    model_config = {"from_attributes": True}