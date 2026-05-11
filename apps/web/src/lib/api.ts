// API client — wraps fetch with auth token injection
// All calls go through PUBLIC_API_URL env variable

export const API_BASE = import.meta.env.PUBLIC_API_URL ?? 'http://localhost:8000';

export interface ClimatePoint {
  timestamp: string;
  temperature: number;
  rainfall: number;
  humidity: number;
  co2_level: number;
}

export interface ForecastPoint {
  date: string;
  temp_min: number;
  temp_max: number;
  rainfall_prob: number;
}

export interface ChatResponse {
  message: string;
  conversation_id: string;
  sources: string[];
}

// Map API response to frontend field names (API uses snake_case, frontend uses camelCase)
function mapPoint(p: any): ClimatePoint {
  return {
    timestamp: p.timestamp,
    temperature: p.temperature,
    rainfall: p.precipitation ?? p.rainfall ?? 0,
    humidity: p.humidity,
    co2_level: p.co2_concentration ?? p.co2_level ?? 420,
  };
}

// Map forecast API response to frontend field names
function mapForecast(f: any): ForecastPoint {
  return {
    date: f.date,
    temp_min: f.temperature_low ?? f.temp_min ?? 0,
    temp_max: f.temperature_high ?? f.temp_max ?? 0,
    rainfall_prob: f.precipitation_probability ?? f.rainfall_prob ?? 0,
  };
}

// ---- Climate data ----

export async function fetchClimateData(lat: number, lng: number, limit = 100): Promise<ClimatePoint[]> {
  const params = new URLSearchParams({ lat: String(lat), lng: String(lng), limit: String(limit) });
  const res = await fetch(`${API_BASE}/api/v1/climate/data?${params}`, {
    headers: authHeaders(),
  });
  if (!res.ok) throw new Error(`Climate API error: ${res.status}`);
  const raw: any[] = await res.json();
  return raw.map(mapPoint);
}

export async function fetchForecast(location: string, days = 7): Promise<ForecastPoint[]> {
  const params = new URLSearchParams({ location, days: String(days) });
  const res = await fetch(`${API_BASE}/api/v1/climate/forecast?${params}`, {
    headers: authHeaders(),
  });
  if (!res.ok) throw new Error(`Forecast API error: ${res.status}`);
  const raw: any[] = await res.json();
  return raw.map(mapForecast);
}

// ---- Auth headers ----

function authHeaders(): Record<string, string> {
  // Read token from localStorage at call time to pick up latest value
  try {
    const raw = localStorage.getItem('ccec_tokens');
    if (raw) {
      const tokens = JSON.parse(raw);
      return { Authorization: `Bearer ${tokens.access_token}` };
    }
  } catch {}
  return {};
}

// ---- Emissions (public — no auth required) ----

export interface ProvinceEmissions {
  name: string;
  code: string;
  lat: number;
  lng: number;
  emissions_kt: number;
  per_capita_t: number;
  sectors: { name: string; emissions_kt: number }[];
}

export interface EmissionsSummary {
  year: number;
  total_emissions_kt: number;
  unit: string;
  source: string;
  provinces: ProvinceEmissions[];
}

export interface EmissionTrend {
  year: number;
  total_emissions_kt: number;
  change_pct: number;
  main_sector: string;
}

export async function fetchEmissionsSummary(year = 2024): Promise<EmissionsSummary> {
  const res = await fetch(`${API_BASE}/api/v1/emissions?year=${year}`);
  if (!res.ok) throw new Error(`Emissions API error: ${res.status}`);
  return res.json();
}

export async function fetchEmissionTrends(country = 'VNM', years = 6): Promise<{ country: string; trends: EmissionTrend[] }> {
  const res = await fetch(`${API_BASE}/api/v1/emissions/trends?country=${country}&years=${years}`);
  if (!res.ok) throw new Error(`Trends API error: ${res.status}`);
  return res.json();
}

export async function fetchCarbonCredits(lat = 21.0285, lng = 105.8542): Promise<{ credits: { id: string; project: string; location: string; lat: number; lng: number; credits_issued: number; credits_sold: number; price_usd: number; status: string; verification: string }[]; total_registered: number; total_sold: number; market_price_usd: number }> {
  const res = await fetch(`${API_BASE}/api/v1/emissions/carbon-credits?lat=${lat}&lng=${lng}`);
  if (!res.ok) throw new Error(`Carbon credits API error: ${res.status}`);
  return res.json();
}

// ---- Chat ----

export async function sendChat(message: string, conversation_id?: string): Promise<ChatResponse> {
  const res = await fetch(`${API_BASE}/api/v1/chat`, {
    method: 'POST',
    headers: { ...authHeaders(), 'Content-Type': 'application/json' },
    body: JSON.stringify({ message, conversation_id }),
  });
  if (!res.ok) throw new Error(`Chat API error: ${res.status}`);
  return res.json();
}