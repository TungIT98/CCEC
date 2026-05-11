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