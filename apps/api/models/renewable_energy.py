from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func

from .database import Base


class RenewableEnergy(Base):
    __tablename__ = "renewable_energy"

    id = Column(Integer, primary_key=True, index=True)
    country_name = Column(String(100), nullable=False, index=True)
    country_code = Column(String(3), nullable=False, index=True)
    energy_type = Column(String(20), nullable=False, index=True)
    capacity_mw = Column(Float, nullable=False)
    generation_gwh = Column(Float, nullable=True)
    installed_year = Column(Integer, nullable=False, index=True)
    source = Column(String(255), nullable=True)
    fetched_at = Column(DateTime(timezone=True), nullable=False, index=True)

    model_config = {"from_attributes": True}