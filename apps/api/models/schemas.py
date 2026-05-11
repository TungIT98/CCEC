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
