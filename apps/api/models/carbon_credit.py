from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.sql import func

from .database import Base


class CarbonCredit(Base):
    __tablename__ = "carbon_credits"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    standard_type = Column(String(20), nullable=False, index=True)  # VER | CER | GOLD
    project_type = Column(String(100), nullable=False, index=True)
    vintage = Column(Integer, nullable=False, index=True)
    unit_price = Column(Float, nullable=False)
    currency = Column(String(10), default="USD", nullable=False)
    registry = Column(String(100), nullable=True, index=True)
    project_url = Column(String(500), nullable=True)
    credit_class = Column(String(100), nullable=True, index=True)
    methodology = Column(String(255), nullable=True)
    estimated_ERt = Column(Float, nullable=True)
    verified_ERt = Column(Float, nullable=True)
    issued_at = Column(DateTime(timezone=True), nullable=True)
    expired_at = Column(DateTime(timezone=True), nullable=True)
    is_retired = Column(Boolean, default=False, nullable=False, index=True)
    country_code = Column(String(3), nullable=True, index=True)
    country_name = Column(String(100), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    model_config = {"from_attributes": True}


class CarbonPrice(Base):
    __tablename__ = "carbon_prices"

    id = Column(Integer, primary_key=True, index=True)
    standard_type = Column(String(20), nullable=False, index=True)
    vintage = Column(Integer, nullable=False, index=True)
    price_per_tCO2e = Column(Float, nullable=False)
    currency = Column(String(10), default="USD", nullable=False)
    source_url = Column(String(500), nullable=True)
    fetched_at = Column(DateTime(timezone=True), nullable=False, index=True)

    model_config = {"from_attributes": True}


class Policy(Base):
    __tablename__ = "policies"

    id = Column(Integer, primary_key=True, index=True)
    country_name = Column(String(100), nullable=False, index=True)
    country_code = Column(String(3), nullable=False, index=True)
    policy_name = Column(String(255), nullable=False, index=True)
    policy_type = Column(String(50), nullable=False, index=True)
    instrument_type = Column(String(100), nullable=True)
    sector = Column(String(100), nullable=True, index=True)
    coverage = Column(String(100), nullable=True)
    economy_wide = Column(String(10), nullable=True)
    carbon_pricing_existence = Column(String(20), nullable=True, index=True)
    pricing_existence_notes = Column(String(500), nullable=True)
    carbon_price_min_tCO2e = Column(Float, nullable=True)
    carbon_price_max_tCO2e = Column(Float, nullable=True)
    currency = Column(String(10), default="USD", nullable=True)
    link_source = Column(String(500), nullable=True)
    fetched_at = Column(DateTime(timezone=True), nullable=False, index=True)

    model_config = {"from_attributes": True}


class NdcTracking(Base):
    __tablename__ = "ndc_tracking"

    id = Column(Integer, primary_key=True, index=True)
    country_name = Column(String(100), nullable=False, index=True)
    country_code = Column(String(3), nullable=False, index=True)
    submission_type = Column(String(50), nullable=True, index=True)
    status = Column(String(30), nullable=False, index=True)
    latest_submission_date = Column(DateTime(timezone=True), nullable=True)
    link_NDC = Column(String(500), nullable=True)
    fetch_link = Column(String(500), nullable=True)
    fetched_at = Column(DateTime(timezone=True), nullable=False, index=True)

    model_config = {"from_attributes": True}