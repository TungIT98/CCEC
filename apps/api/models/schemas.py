from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    password: Optional[str] = None


class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenRefresh(BaseModel):
    refresh_token: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class ClimateDataQuery(BaseModel):
    lat: float
    lng: float
    start: Optional[datetime] = None
    end: Optional[datetime] = None


class ClimateDataPoint(BaseModel):
    timestamp: datetime
    temperature: Optional[float] = None
    humidity: Optional[float] = None
    precipitation: Optional[float] = None
    wind_speed: Optional[float] = None
    co2_concentration: Optional[float] = None
    lat: float
    lng: float


class ForecastRequest(BaseModel):
    location: str
    lat: Optional[float] = None
    lng: Optional[float] = None
    days: int = 7


class ForecastPoint(BaseModel):
    date: str
    temperature_high: float
    temperature_low: float
    precipitation_probability: float
    co2_forecast: Optional[float] = None


class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None


class ChatResponse(BaseModel):
    message: str
    conversation_id: str
    sources: list[str] = []


class HealthResponse(BaseModel):
    status: str
    version: str
    database: str = "unknown"


# ── User Settings ─────────────────────────────────────────────────────────────

class UserSettingsBase(BaseModel):
    language: Optional[str] = "vi"
    timezone: Optional[str] = "Asia/Ho_Chi_Minh"
    email_notifications: Optional[bool] = True
    push_notifications: Optional[bool] = True
    data_alerts: Optional[bool] = True
    marketing_emails: Optional[bool] = False


class UserSettingsCreate(UserSettingsBase):
    user_id: int


class UserSettingsResponse(UserSettingsBase):
    id: int
    user_id: int
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


# ── Notifications ─────────────────────────────────────────────────────────────

class NotificationBase(BaseModel):
    type: str  # "info" | "warning" | "alert" | "system"
    title: str
    message: str


class NotificationCreate(NotificationBase):
    pass


class NotificationResponse(NotificationBase):
    id: int
    user_id: int
    is_read: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class NotificationUpdate(BaseModel):
    is_read: Optional[bool] = None


# ── Team ───────────────────────────────────────────────────────────────────────

class TeamMemberBase(BaseModel):
    email: EmailStr
    role: str  # "admin" | "member" | "viewer"


class TeamMemberCreate(TeamMemberBase):
    pass


class TeamMemberResponse(TeamMemberBase):
    id: int
    user_id: int
    created_at: datetime

    model_config = {"from_attributes": True}


# ── Emissions ─────────────────────────────────────────────────────────────────

class EmissionsRecordBase(BaseModel):
    scope: int  # 1 | 2 | 3
    gas_type: str  # "CO2" | "CH4" | "N2O"
    co2e_tonnage: float
    sector: str
    source: Optional[str] = None
    reporting_year: int


class EmissionsRecordCreate(EmissionsRecordBase):
    pass


class EmissionsRecordResponse(EmissionsRecordBase):
    id: int
    user_id: int
    created_at: datetime

    model_config = {"from_attributes": True}


# ── ESG Metrics ─────────────────────────────────────────────────────────────────

class ESGMetricBase(BaseModel):
    category: str  # "E" | "S" | "G"
    metric_name: str
    value: float
    unit: Optional[str] = None
    score: Optional[float] = None
    reporting_period: str  # e.g. "2025-Q1"


class ESGMetricCreate(ESGMetricBase):
    pass


class ESGMetricResponse(ESGMetricBase):
    id: int
    user_id: int
    created_at: datetime

    model_config = {"from_attributes": True}


# ── Alerts ──────────────────────────────────────────────────────────────────────

class AlertBase(BaseModel):
    metric: str  # "temperature" | "co2" | "precipitation" | "wind_speed"
    operator: str  # ">" | "<" | ">=" | "<="
    threshold_value: float
    actual_value: float
    location_lat: Optional[float] = None
    location_lng: Optional[float] = None


class AlertCreate(AlertBase):
    pass


class AlertResponse(AlertBase):
    id: int
    user_id: int
    is_resolved: bool
    created_at: datetime
    resolved_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class AlertUpdate(BaseModel):
    is_resolved: Optional[bool] = None


# ── Audit Log ───────────────────────────────────────────────────────────────────

class AuditLogResponse(BaseModel):
    id: int
    user_id: Optional[int] = None
    action: str
    entity_type: str
    entity_id: Optional[int] = None
    changes: Optional[str] = None
    ip_address: Optional[str] = None
    created_at: datetime

    model_config = {"from_attributes": True}
