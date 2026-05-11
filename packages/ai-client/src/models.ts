/**
 * Unified AI client interfaces — OpenAI-compatible across Groq, DeepSeek, PortKey.
 * All providers implement the same ChatCompletion interface.
 */

export type Role = 'system' | 'user' | 'assistant' | 'tool';

export interface Message {
  role: Role;
  content: string;
  name?: string;
  tool_call_id?: string;
}

export interface ToolDefinition {
  name: string;
  description: string;
  parameters: Record<string, unknown>;
}

export interface ToolCall {
  id: string;
  type: 'function';
  function: { name: string; arguments: string };
}

export interface ChatCompletionChoice {
  index: number;
  message: Message;
  finish_reason: 'stop' | 'length' | 'content_filter' | 'tool_calls' | null;
  tool_calls?: ToolCall[];
}

export interface Usage {
  prompt_tokens: number;
  completion_tokens: number;
  total_tokens: number;
}

export interface ChatCompletionResponse {
  id: string;
  object: 'chat.completion';
  created: number;
  model: string;
  provider: ProviderName;
  choices: ChatCompletionChoice[];
  usage: Usage;
}

export type ProviderName = 'groq' | 'deepseek' | 'portkey' | 'minimax';

export interface AIProviderConfig {
  apiKey: string;
  baseURL?: string;
  timeout?: number;
  maxRetries?: number;
}

export interface ChatOptions {
  model: string;
  messages: Message[];
  temperature?: number;
  max_tokens?: number;
  top_p?: number;
  tools?: ToolDefinition[];
  tool_choice?: 'auto' | 'none' | { type: 'function'; function: { name: string } };
  stream?: boolean;
  response_format?: { type: 'json_object' };
}

export interface ModelInfo {
  id: string;
  provider: ProviderName;
  contextWindow: number;
  supportsTools: boolean;
  supportsVision: boolean;
  supportsJsonMode: boolean;
  description: string;
}

/** Supported models by provider */
export const MODELS: Record<ProviderName, ModelInfo[]> = {
  groq: [
    {
      id: 'llama-3.3-70b-versatile',
      provider: 'groq',
      contextWindow: 128_000,
      supportsTools: true,
      supportsVision: false,
      supportsJsonMode: true,
      description: 'Fast free LLM — primary for most tasks',
    },
    {
      id: 'mixtral-8x7b-32768',
      provider: 'groq',
      contextWindow: 32_768,
      supportsTools: true,
      supportsVision: false,
      supportsJsonMode: true,
      description: 'Fast Mixture-of-Experts model',
    },
    {
      id: 'gemma2-9b-it',
      provider: 'groq',
      contextWindow: 8_192,
      supportsTools: true,
      supportsVision: false,
      supportsJsonMode: false,
      description: 'Google Gemma instruction-tuned',
    },
  ],
  deepseek: [
    {
      id: 'deepseek-chat',
      provider: 'deepseek',
      contextWindow: 64_000,
      supportsTools: true,
      supportsVision: false,
      supportsJsonMode: true,
      description: 'DeepSeek V3 — cheap quality',
    },
    {
      id: 'deepseek-coder',
      provider: 'deepseek',
      contextWindow: 64_000,
      supportsTools: true,
      supportsVision: false,
      supportsJsonMode: true,
      description: 'DeepSeek Coder — code-specialized',
    },
  ],
  portkey: [
    {
      id: 'claude-opus-4-6',
      provider: 'portkey',
      contextWindow: 200_000,
      supportsTools: true,
      supportsVision: false,
      supportsJsonMode: false,
      description: 'Claude Opus 4.6 — best quality reasoning',
    },
  ],
  minimax: [
    {
      id: 'MiniMax-M2.7',
      provider: 'minimax',
      contextWindow: 1_000_000,
      supportsTools: false,
      supportsVision: false,
      supportsJsonMode: true,
      description: 'MiniMax M2.7 — fast, cost-effective',
    },
  ],
};

/** Default model per provider */
export const DEFAULT_MODELS: Record<ProviderName, string> = {
  groq: 'llama-3.3-70b-versatile',
  deepseek: 'deepseek-chat',
  portkey: 'claude-opus-4-6',
  minimax: 'MiniMax-M2.7',
};

// ─────────────────────────────────────────────────────────────────────────────
// Climate domain — tool definitions for CCEC Climate Platform
// ─────────────────────────────────────────────────────────────────────────────

export interface ClimateToolParams {
  location?: string;
  lat?: number;
  lng?: number;
  year?: number;
  scope?: 1 | 2 | 3;
  sector?: string;
  reporting_period?: string;
}

export const CLIMATE_TOOLS: ToolDefinition[] = [
  {
    name: 'get_emissions',
    description: 'Retrieve GHG emissions data by location, year, scope (1/2/3), and sector (energy|transport|industry|agriculture|waste|land_use). Returns CO2-equivalent tonnes.',
    parameters: {
      type: 'object',
      properties: {
        location: { type: 'string', description: 'Province or country name' },
        year: { type: 'integer', description: 'Reporting year, e.g. 2024' },
        scope: { type: 'integer', enum: [1, 2, 3], description: 'Emissions scope: 1=direct, 2=indirect, 3=supply chain' },
        sector: { type: 'string', enum: ['energy', 'transport', 'industry', 'agriculture', 'waste', 'land_use'] },
      },
      required: [],
    },
  },
  {
    name: 'get_esg_score',
    description: 'Query Environmental, Social, and Governance (ESG) scores and KPIs for a company or country over a reporting period.',
    parameters: {
      type: 'object',
      properties: {
        reporting_period: { type: 'string', description: 'Reporting period, e.g. "2025-Q1"' },
        category: { type: 'string', enum: ['E', 'S', 'G'], description: 'ESG category' },
      },
      required: [],
    },
  },
  {
    name: 'get_forecast',
    description: 'Get climate forecast (temperature, precipitation, CO2) for a location over the next N days.',
    parameters: {
      type: 'object',
      properties: {
        lat: { type: 'number', description: 'Latitude' },
        lng: { type: 'number', description: 'Longitude' },
        days: { type: 'integer', description: 'Number of forecast days (1-30)', default: 7 },
      },
      required: [],
    },
  },
  {
    name: 'get_climate_alerts',
    description: 'Return active threshold-based climate alerts (temperature, CO2, precipitation, wind speed breaches).',
    parameters: {
      type: 'object',
      properties: {},
      required: [],
    },
  },
];

// ─────────────────────────────────────────────────────────────────────────────
// Climate system prompt — inject into every chat session
// ─────────────────────────────────────────────────────────────────────────────

/**
 * Vietnam climate context for AI system prompts.
 * Inject as the first user/system message or prepend to conversation.
 */
export const VIETNAM_CLIMATE_CONTEXT = `You are an expert assistant for the CCEC Climate Platform (Chiến lược Khí hậu Việt Nam).

Vietnam climate context:
- Tropical monsoon climate with 3 regions: North (humid subtropical), Central (hot/typhoon-prone), South (tropical savanna)
- Key climate risks: typhoons (8–10 per year, mostly Central), sea-level rise (Mekong Delta), heat waves (>40°C in summer)
- National targets: NDC commitment to 9% emission reduction by 2030 (unconditional) → 27% (conditional, international support)
- NETs: Vietnam aims for net-zero by 2050, scaling solar/wind capacity to 50GW+
- Main data sources: MONRE weather stations, Global Climate Observing System (GCOS), FAOstat
- Common units: temperature (°C), precipitation (mm), CO2 (ppm or Mt CO2e), emissions (kt CO2e)

Always answer in Vietnamese when the user writes in Vietnamese. Prefer structured JSON for data requests.`;