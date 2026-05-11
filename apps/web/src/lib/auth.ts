// Auth store for JWT token management
// Stores access/refresh tokens in localStorage with expiry tracking

export interface AuthTokens {
  access_token: string;
  refresh_token: string;
  expires_at?: number; // ms timestamp
}

export interface CurrentUser {
  id: number;
  email: string;
  full_name: string;
}

const TOKEN_KEY = 'ccec_tokens';
const USER_KEY = 'ccec_user';

// ---- Token storage ----

export function storeTokens(tokens: AuthTokens): void {
  // Store with expiry: access token expires in 15 min
  const expires_at = Date.now() + 15 * 60 * 1000;
  localStorage.setItem(TOKEN_KEY, JSON.stringify({ ...tokens, expires_at }));
}

export function getTokens(): AuthTokens | null {
  try {
    const raw = localStorage.getItem(TOKEN_KEY);
    if (!raw) return null;
    const tokens: AuthTokens = JSON.parse(raw);
    // Check if expired (with 30s buffer)
    if (tokens.expires_at && Date.now() > tokens.expires_at - 30_000) {
      // Token expired — trigger silent refresh but return null so caller re-auths
      if (tokens.refresh_token) {
        refreshTokens(tokens.refresh_token).catch(() => {/* swallow — caller will redirect */});
      }
      return null;
    }
    return tokens;
  } catch {
    return null;
  }
}

export function clearTokens(): void {
  localStorage.removeItem(TOKEN_KEY);
  localStorage.removeItem(USER_KEY);
}

// ---- User storage ----

export function storeUser(user: CurrentUser): void {
  localStorage.setItem(USER_KEY, JSON.stringify(user));
}

export function getStoredUser(): CurrentUser | null {
  try {
    const raw = localStorage.getItem(USER_KEY);
    return raw ? JSON.parse(raw) : null;
  } catch {
    return null;
  }
}

// ---- API calls ----

export async function login(email: string, password: string): Promise<CurrentUser> {
  const res = await fetch(`${import.meta.env.PUBLIC_API_URL}/api/v1/auth/login/json`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || 'Login failed');
  }
  const tokens: AuthTokens = await res.json();
  storeTokens(tokens);
  // Decode user from token (sub only, fetch /me for full profile)
  const meRes = await fetch(`${import.meta.env.PUBLIC_API_URL}/api/v1/users/me`, {
    headers: { Authorization: `Bearer ${tokens.access_token}` },
  });
  if (meRes.ok) {
    const user = await meRes.json();
    storeUser(user as CurrentUser);
    return user as CurrentUser;
  }
  // Fallback: parse email from login form
  const fallback: CurrentUser = { id: 0, email, full_name: email.split('@')[0] };
  storeUser(fallback);
  return fallback;
}

export async function refreshTokens(refresh_token: string): Promise<AuthTokens | null> {
  try {
    const res = await fetch(`${import.meta.env.PUBLIC_API_URL}/api/v1/auth/refresh`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ refresh_token }),
    });
    if (!res.ok) {
      clearTokens();
      return null;
    }
    const tokens: AuthTokens = await res.json();
    storeTokens(tokens);
    return tokens;
  } catch {
    clearTokens();
    return null;
  }
}

export async function register(email: string, password: string, full_name: string): Promise<void> {
  const res = await fetch(`${import.meta.env.PUBLIC_API_URL}/api/v1/auth/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password, full_name }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || 'Registration failed');
  }
}

export async function logout(): Promise<void> {
  clearTokens();
}

// ---- Authenticated fetch helper ----

export async function apiFetch(path: string, options: RequestInit = {}): Promise<Response> {
  const tokens = getTokens();
  const headers = {
    'Content-Type': 'application/json',
    ...(options.headers || {}),
  };
  if (tokens?.access_token) {
    (headers as Record<string, string>)['Authorization'] = `Bearer ${tokens.access_token}`;
  }
  const res = await fetch(`${import.meta.env.PUBLIC_API_URL}${path}`, { ...options, headers });
  // Auto-refresh on 401
  if (res.status === 401 && tokens?.refresh_token) {
    const refreshed = await refreshTokens(tokens.refresh_token);
    if (refreshed) {
      (headers as Record<string, string>)['Authorization'] = `Bearer ${refreshed.access_token}`;
      return fetch(`${import.meta.env.PUBLIC_API_URL}${path}`, { ...options, headers });
    }
  }
  return res;
}

// ---- State helpers ----

export function isAuthenticated(): boolean {
  return getTokens() !== null;
}