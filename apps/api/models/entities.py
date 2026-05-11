from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float
from sqlalchemy.sql import func

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class ClimateRecord(Base):
    __tablename__ = "climate_records"

    id = Column(Integer, primary_key=True, index=True)
    lat = Column(Float, nullable=False, index=True)
    lng = Column(Float, nullable=False, index=True)
    timestamp = Column(DateTime(timezone=True), nullable=False, index=True)
    temperature = Column(Float, nullable=True)
    humidity = Column(Float, nullable=True)
    precipitation = Column(Float, nullable=True)
    wind_speed = Column(Float, nullable=True)
    co2_concentration = Column(Float, nullable=True)
    source = Column(String(100), default="simulated")


class UserSettings(Base):
    __tablename__ = "user_settings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, unique=True)
    language = Column(String(10), default="vi")
    timezone = Column(String(50), default="Asia/Ho_Chi_Minh")
    email_notifications = Column(Boolean, default=True)
    push_notifications = Column(Boolean, default=True)
    data_alerts = Column(Boolean, default=True)
    marketing_emails = Column(Boolean, default=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    type = Column(String(20), default="info")
    title = Column(String(255), nullable=False)
    message = Column(String(1000), nullable=False)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class TeamMember(Base):
    __tablename__ = "team_members"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    email = Column(String(255), nullable=False, index=True)
    role = Column(String(20), default="member")  # "admin" | "member" | "viewer"
    created_at = Column(DateTime(timezone=True), server_default=func.now())


# ── Emissions ─────────────────────────────────────────────────────────────────

class EmissionsRecord(Base):
    __tablename__ = "emissions_records"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    # Scope: 1=direct, 2=indirect, 3=supply chain
    scope = Column(Integer, nullable=False, index=True)
    # GHG type: CO2, CH4, N2O, etc.
    gas_type = Column(String(20), nullable=False)
    # CO2-equivalent tonnes
    co2e_tonnage = Column(Float, nullable=False)
    # Sector: energy, transport, agriculture, industry, waste, land_use
    sector = Column(String(50), nullable=False, index=True)
    source = Column(String(255), nullable=True)
    reporting_year = Column(Integer, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


# ── ESG Metrics ─────────────────────────────────────────────────────────────────

class ESGMetric(Base):
    __tablename__ = "esg_metrics"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    # E=Environmental, S=Social, G=Governance
    category = Column(String(1), nullable=False, index=True)  # "E" | "S" | "G"
    metric_name = Column(String(100), nullable=False)
    value = Column(Float, nullable=False)
    unit = Column(String(30), nullable=True)
    score = Column(Float, nullable=True)  # 0–100 ESG score
    reporting_period = Column(String(30), nullable=False, index=True)  # e.g. "2025-Q1"
    created_at = Column(DateTime(timezone=True), server_default=func.now())


# ── Alerts ──────────────────────────────────────────────────────────────────────

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    # Threshold breached: temperature | co2 | precipitation | wind_speed
    metric = Column(String(30), nullable=False, index=True)
    operator = Column(String(5), nullable=False)  # ">" | "<" | ">=" | "<="
    threshold_value = Column(Float, nullable=False)
    actual_value = Column(Float, nullable=False)
    location_lat = Column(Float, nullable=True)
    location_lng = Column(Float, nullable=True)
    is_resolved = Column(Boolean, default=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    resolved_at = Column(DateTime(timezone=True), nullable=True)


# ── Audit Log ───────────────────────────────────────────────────────────────────

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=True, index=True)
    # "user.create" | "emissions.update" | "settings.change" | etc.
    action = Column(String(50), nullable=False, index=True)
    entity_type = Column(String(50), nullable=False)  # "user" | "emissions" | "settings"
    entity_id = Column(Integer, nullable=True)
    changes = Column(String(2000), nullable=True)  # JSON diff summary
    ip_address = Column(String(45), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
