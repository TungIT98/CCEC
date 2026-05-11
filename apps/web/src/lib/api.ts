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

async function apiFetch(path: string, opts?: RequestInit): Promise<Response> {
  return fetch(API_BASE + path, { ...opts, headers: { ...authHeaders(), ...(opts?.headers as Record<string, string> || {}) } });
}
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

// ---- Settings ----

export interface UserSettings {
  language: string;
  theme: string;
  timezone: string;
  email_notifications: boolean;
  app_notifications: boolean;
  weekly_digest: boolean;
  decimal_places: number;
  date_format: string;
}

export async function getSettings(): Promise<UserSettings> {
  const res = await apiFetch('/api/v1/settings');
  if (!res.ok) throw new Error(`Settings error: ${res.status}`);
  return res.json();
}

export async function updateSettings(data: Partial<UserSettings>): Promise<UserSettings> {
  const res = await apiFetch('/api/v1/settings', { method: 'PUT', body: JSON.stringify(data) });
  if (!res.ok) throw new Error(`Settings error: ${res.status}`);
  return res.json();
}

// ---- Notifications ----

export interface Notification {
  id: number;
  title: string;
  body: string;
  is_read: boolean;
  created_at: string;
}

export async function getNotifications(): Promise<{ notifications: Notification[]; unread: number }> {
  const res = await apiFetch('/api/v1/notifications');
  if (!res.ok) throw new Error(`Notifications error: ${res.status}`);
  return res.json();
}

export async function markNotificationRead(id: number): Promise<void> {
  await apiFetch(`/api/v1/notifications/${id}/read`, { method: 'PATCH' });
}

// ---- Team ----

export interface TeamMember {
  id: number;
  email: string;
  full_name: string;
  role: string;
  is_active: boolean;
}

export async function getTeamMembers(): Promise<TeamMember[]> {
  const res = await apiFetch('/api/v1/team');
  if (!res.ok) throw new Error(`Team error: ${res.status}`);
  return res.json();
}

export async function inviteTeamMember(email: string, role: string): Promise<void> {
  const res = await apiFetch('/api/v1/team/invite', {
    method: 'POST',
    body: JSON.stringify({ email, role }),
  });
  if (!res.ok) throw new Error(`Invite failed: ${res.status}`);
}

export async function removeTeamMember(id: number): Promise<void> {
  const res = await apiFetch(`/api/v1/team/${id}`, { method: 'DELETE' });
  if (!res.ok) throw new Error(`Remove member error: ${res.status}`);
}

// ---- Password ----

export async function changePassword(old_password: string, new_password: string): Promise<void> {
  const res = await apiFetch('/api/v1/users/me/password', {
    method: 'POST',
    body: JSON.stringify({ old_password, new_password }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || 'Password change failed');
  }
}

// ---- Carbon Credits ----

export interface CarbonCredit {
  id: number;
  name: string;
  standard_type: string;
  project_type: string;
  vintage: number;
  unit_price: number;
  currency: string;
  registry: string;
  verified_ERt: number | null;
  is_retired: boolean;
  country_code: string;
  country_name: string;
  created_at: string;
}

export interface CarbonPrice {
  id: number;
  standard_type: string;
  vintage: number;
  price_per_tCO2e: number;
  currency: string;
  source_url: string;
  fetched_at: string;
}

export async function fetchCarbonCreditsPage(params?: {
  standard_type?: string;
  vintage_min?: number;
  vintage_max?: number;
  project_type?: string;
  country_code?: string;
  page?: number;
  page_size?: number;
}): Promise<{ credits: CarbonCredit[]; total: number }> {
  const sp = new URLSearchParams();
  if (params?.standard_type) sp.set('standard_type', params.standard_type);
  if (params?.vintage_min) sp.set('vintage_min', String(params.vintage_min));
  if (params?.vintage_max) sp.set('vintage_max', String(params.vintage_max));
  if (params?.project_type) sp.set('project_type', params.project_type);
  if (params?.country_code) sp.set('country_code', params.country_code);
  sp.set('page', String(params?.page ?? 1));
  sp.set('page_size', String(params?.page_size ?? 20));
  const res = await apiFetch(`/api/v1/carbon-credits?${sp}`);
  if (!res.ok) throw new Error(`Carbon credits error: ${res.status}`);
  return res.json();
}

export async function fetchCarbonPrices(standard_type?: string): Promise<CarbonPrice[]> {
  const sp = standard_type ? `?standard_type=${standard_type}` : '';
  const res = await apiFetch(`/api/v1/carbon-credits/prices${sp}`);
  if (!res.ok) throw new Error(`Carbon prices error: ${res.status}`);
  return res.json();
}

export async function fetchCarbonPricesHistory(standard_type?: string, limit = 50): Promise<CarbonPrice[]> {
  const sp = new URLSearchParams();
  if (standard_type) sp.set('standard_type', standard_type);
  sp.set('limit', String(limit));
  const res = await apiFetch(`/api/v1/carbon-credits/prices/history?${sp}`);
  if (!res.ok) throw new Error(`Carbon prices history error: ${res.status}`);
  return res.json();
}

// ---- Renewable Energy ----

export interface RenewableEnergyRecord {
  id: number;
  country_name: string;
  country_code: string;
  energy_type: string;
  capacity_mw: number;
  generation_gwh: number | null;
  installed_year: number;
  source: string;
  fetched_at: string;
}

export interface CountryEnergyDetail {
  country_code: string;
  country_name: string;
  records: RenewableEnergyRecord[];
  total_capacity_mw: number;
  by_energy_type: Record<string, number>;
}

export async function fetchRenewableEnergy(params?: {
  country_code?: string;
  energy_type?: string;
  year_min?: number;
  year_max?: number;
  page?: number;
  page_size?: number;
}): Promise<RenewableEnergyRecord[]> {
  const sp = new URLSearchParams();
  if (params?.country_code) sp.set('country_code', params.country_code);
  if (params?.energy_type) sp.set('energy_type', params.energy_type);
  if (params?.year_min) sp.set('year_min', String(params.year_min));
  if (params?.year_max) sp.set('year_max', String(params.year_max));
  sp.set('page', String(params?.page ?? 1));
  sp.set('page_size', String(params?.page_size ?? 50));
  const res = await apiFetch(`/api/v1/energy/renewable?${sp}`);
  if (!res.ok) throw new Error(`Energy API error: ${res.status}`);
  return res.json();
}

export async function fetchCountryEnergy(code: string): Promise<CountryEnergyDetail> {
  const res = await apiFetch(`/api/v1/energy/country/${code}`);
  if (!res.ok) throw new Error(`Country energy error: ${res.status}`);
  return res.json();
}

// ---- Climate Policies ----

export interface ClimatePolicy {
  id: number;
  country_name: string;
  country_code: string;
  policy_name: string;
  policy_type: string;
  instrument_type: string;
  sector: string;
  coverage: string;
  economy_wide: string;
  carbon_pricing_existence: string;
  carbon_price_min_tCO2e: number | null;
  carbon_price_max_tCO2e: number | null;
  currency: string;
  link_source: string;
  fetched_at: string;
}

export interface NdcTracking {
  id: number;
  country_name: string;
  country_code: string;
  submission_type: string;
  status: string;
  latest_submission_date: string;
  link_NDC: string;
  fetch_link: string;
  fetched_at: string;
}

export async function fetchPolicies(params?: {
  country_code?: string;
  policy_type?: string;
  sector?: string;
  page?: number;
  page_size?: number;
}): Promise<ClimatePolicy[]> {
  const sp = new URLSearchParams();
  if (params?.country_code) sp.set('country_code', params.country_code);
  if (params?.policy_type) sp.set('policy_type', params.policy_type);
  if (params?.sector) sp.set('sector', params.sector);
  sp.set('page', String(params?.page ?? 1));
  sp.set('page_size', String(params?.page_size ?? 20));
  const res = await apiFetch(`/api/v1/policies?${sp}`);
  if (!res.ok) throw new Error(`Policies API error: ${res.status}`);
  return res.json();
}

export async function fetchNdcTracking(): Promise<NdcTracking[]> {
  const res = await apiFetch('/api/v1/policies/ndc');
  if (!res.ok) throw new Error(`NDC API error: ${res.status}`);
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

// ---- AI Streaming Chat ----
// Callback `onChunk(text)` is called for each token.
export async function streamChat(
  message: string,
  onChunk: (chunk: string) => void,
): Promise<void> {
  const res = await fetch(`${API_BASE}/api/v1/chat/stream`, {
    method: 'POST',
    headers: { ...authHeaders(), 'Content-Type': 'application/json' },
    body: JSON.stringify({ message }),
  });
  if (!res.ok) throw new Error(`Stream error: ${res.status}`);

  const reader = res.body?.getReader();
  if (!reader) throw new Error('ReadableStream not available');
  const decoder = new TextDecoder();

  try {
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      const chunk = decoder.decode(value, { stream: true });
      for (const line of chunk.split('\n')) {
        const m = line.match(/data:\s*(\{.*\})/);
        if (!m) continue;
        try {
          const obj = JSON.parse(m[1]);
          if (obj.event === 'token' && obj.data) onChunk(obj.data);
        } catch {}
      }
    }
  } catch {
    // Stream ended
  }
}

// ---- Prophet Forecast ----

export interface ForecastResponse {
  type: string;
  horizon_days: number;
  model: Record<string, unknown>;
  data: Array<Record<string, unknown>>;
}

export async function forecastEmissions(
  country_code = 'VNM',
  horizon_days = 365,
): Promise<ForecastResponse> {
  const res = await apiFetch('/api/v1/ai/forecast/emissions', {
    method: 'POST',
    body: JSON.stringify({ country_code, horizon_days }),
  });
  if (!res.ok) throw new Error(`Emissions forecast error: ${res.status}`);
  return res.json();
}

export async function forecastCarbonPrice(
  standard_type = 'VER',
  horizon_days = 90,
): Promise<ForecastResponse> {
  const res = await apiFetch('/api/v1/ai/forecast/carbon-price', {
    method: 'POST',
    body: JSON.stringify({ standard_type, horizon_days }),
  });
  if (!res.ok) throw new Error(`Carbon price forecast error: ${res.status}`);
  return res.json();
}

export async function forecastTemperature(
  station_id = 'Hanoi',
  horizon_days = 365,
): Promise<ForecastResponse> {
  const res = await apiFetch('/api/v1/ai/forecast/temperature', {
    method: 'POST',
    body: JSON.stringify({ station_id, horizon_days }),
  });
  if (!res.ok) throw new Error(`Temperature forecast error: ${res.status}`);
  return res.json();
}