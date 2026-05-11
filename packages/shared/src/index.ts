/**
 * Shared TypeScript types for CCEC Climate Platform.
 * Used by both web frontend and ai-client package.
 */

// ============================================================
// Climate Data Types
// ============================================================

export interface GeoPoint {
  lat: number;
  lng: number;
}

export interface ClimateDataPoint {
  timestamp: string; // ISO 8601
  temperature: number; // Celsius
  humidity: number; // percentage 0-100
  precipitation: number; // mm
  windSpeed: number; // km/h
  pressure: number; // hPa
  uvIndex: number;
  airQuality: number; // AQI
}

export interface ClimateZone {
  id: string;
  name: string;
  description: string;
  bounds: {
    north: number;
    south: number;
    east: number;
    west: number;
  };
  color: string;
  weatherStats: {
    avgTemp: number;
    avgHumidity: number;
    avgPrecipitation: number;
    extremeWeatherDays: number;
  };
}

export interface ForecastDay {
  date: string; // ISO date
  tempMin: number;
  tempMax: number;
  humidity: number;
  precipitation: number;
  windSpeed: number;
  condition: WeatherCondition;
  icon: string;
  uvIndex: number;
  sunrise: string;
  sunset: string;
}

export type WeatherCondition =
  | 'sunny'
  | 'partly_cloudy'
  | 'cloudy'
  | 'rainy'
  | 'stormy'
  | 'snow'
  | 'foggy';

// ============================================================
// User / Auth Types
// ============================================================

export interface User {
  id: string;
  email: string;
  name: string;
  role: UserRole;
  organization?: string;
  createdAt: string;
}

export type UserRole = 'admin' | 'researcher' | 'viewer';

export interface AuthToken {
  accessToken: string;
  refreshToken: string;
  expiresAt: number;
}

// ============================================================
// API Response Types
// ============================================================

export interface ApiResponse<T> {
  data: T;
  meta?: {
    total?: number;
    page?: number;
    perPage?: number;
  };
}

export interface ApiError {
  error: string;
  detail?: string;
  code?: string;
}

// ============================================================
// Map Types
// ============================================================

export interface MapMarker {
  id: string;
  position: GeoPoint;
  type: MarkerType;
  label: string;
  description?: string;
}

export type MarkerType =
  | 'weather_station'
  | 'research_center'
  | 'flood_zone'
  | 'drought_zone'
  | 'climate_refuge';

// ============================================================
// Chat / AI Types
// ============================================================

export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: string;
  attachments?: ChatAttachment[];
}

export interface ChatAttachment {
  type: 'image' | 'file' | 'chart';
  url: string;
  name: string;
}

// ============================================================
// Dashboard Types
// ============================================================

export interface DashboardMetric {
  label: string;
  value: number;
  unit: string;
  change: number; // percentage
  trend: 'up' | 'down' | 'neutral';
}

export interface TimeSeriesDataPoint {
  timestamp: string;
  value: number;
}

// AI client types — import directly from @ccec/ai-client for type access
// Re-exports intentionally omitted to avoid circular dependency