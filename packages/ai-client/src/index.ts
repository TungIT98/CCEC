/**
 * CCEC Climate Platform — OpenAI-compatible AI client.
 * Unified interface across Groq, DeepSeek, Portkey.
 *
 * Usage:
 *   import { createAI, AIProvider } from '@ccec/ai-client';
 *
 *   const ai = createAI({ provider: 'groq', apiKey: process.env.GROQ_API_KEY });
 *   const res = await ai.chat({ model: 'llama-3.3-70b-versatile', messages: [...] });
 */

export * from './models.js';
export { chat as groqChat, stream as groqStream } from './providers/groq.js';
export { chat as deepseekChat, stream as deepseekStream } from './providers/deepseek.js';
export { chat as portkeyChat, stream as portkeyStream } from './providers/portkey.js';
export { chat as minimaxChat, stream as minimaxStream } from './providers/minimax.js';

// ---------------------------------------------------------------------------
// Unified client factory
// ---------------------------------------------------------------------------

import {
  MODELS,
  type ChatCompletionResponse,
  type ChatOptions,
  type ModelInfo,
  type ProviderName,
} from './models.js';

import {
  chat as groqChat,
  stream as groqStream,
  type GroqConfig,
} from './providers/groq.js';

import {
  chat as deepseekChat,
  stream as deepseekStream,
  type DeepSeekConfig,
} from './providers/deepseek.js';

import {
  chat as portkeyChat,
  stream as portkeyStream,
  type PortKeyConfig,
} from './providers/portkey.js';

import {
  chat as minimaxChat,
  stream as minimaxStream,
  type MiniMaxConfig,
} from './providers/minimax.js';

export interface AIClientOptions {
  provider: ProviderName;
  apiKey: string;
  baseURL?: string;
  timeout?: number;
  maxRetries?: number;
  defaultModel?: string;
}

export interface AIClient {
  provider: ProviderName;
  defaultModel: string;
  chat(options: Omit<ChatOptions, 'model'>): Promise<ChatCompletionResponse>;
  stream(options: Omit<ChatOptions, 'model'>): AsyncGenerator<string>;
  listModels(): ModelInfo[];
}

/** Factory — returns the right chat/stream function for the chosen provider */
function getProviderFns(provider: ProviderName) {
  switch (provider) {
    case 'groq': return { chat: groqChat, stream: groqStream };
    case 'deepseek': return { chat: deepseekChat, stream: deepseekStream };
    case 'portkey': return { chat: portkeyChat, stream: portkeyStream };
    case 'minimax': return { chat: minimaxChat, stream: minimaxStream };
  }
}

function getDefaultModel(provider: ProviderName, override?: string): string {
  if (override) return override;
  const defaults: Record<ProviderName, string> = {
    groq: 'llama-3.3-70b-versatile',
    deepseek: 'deepseek-chat',
    portkey: 'claude-opus-4-6',
    minimax: 'MiniMax-M2.7',
  };
  return defaults[provider];
}

function buildConfig(
  provider: ProviderName,
  apiKey: string,
  baseURL?: string,
  timeout?: number,
): GroqConfig | DeepSeekConfig | { apiKey: string; baseURL?: string; timeout?: number; traceId?: string; metadata?: Record<string, string> } | MiniMaxConfig {
  const base = { apiKey, baseURL, timeout };
  if (provider === 'portkey') {
    return { ...base, traceId: undefined, metadata: undefined };
  }
  return base;
}

/**
 * Create a unified AI client for the specified provider.
 *
 * @example
 * const ai = createAI({ provider: 'groq', apiKey: 'gsk_...' });
 * const res = await ai.chat({ messages: [{ role: 'user', content: 'Hello!' }] });
 */
export function createAI(options: AIClientOptions): AIClient {
  const { provider, apiKey, baseURL, timeout, defaultModel } = options;
  const fns = getProviderFns(provider);
  const resolvedDefaultModel = getDefaultModel(provider, defaultModel);

  return {
    provider,
    defaultModel: resolvedDefaultModel,

    async chat(chatOptions: Omit<ChatOptions, 'model'>): Promise<ChatCompletionResponse> {
      const model = (chatOptions as { model?: string }).model ?? resolvedDefaultModel;
      const config = buildConfig(provider, apiKey, baseURL, timeout);
      if (provider === 'groq') {
        return fns.chat(config as GroqConfig, { ...chatOptions, model });
      } else if (provider === 'deepseek') {
        return fns.chat(config as DeepSeekConfig, { ...chatOptions, model });
      } else if (provider === 'minimax') {
        return fns.chat(config as MiniMaxConfig, { ...chatOptions, model });
      } else {
        return fns.chat(config as Parameters<typeof portkeyChat>[0], { ...chatOptions, model });
      }
    },

    stream(chatOptions: Omit<ChatOptions, 'model'>): AsyncGenerator<string> {
      const model = (chatOptions as { model?: string }).model ?? resolvedDefaultModel;
      const config = buildConfig(provider, apiKey, baseURL, timeout);
      if (provider === 'groq') {
        return fns.stream(config as GroqConfig, { ...chatOptions, model });
      } else if (provider === 'deepseek') {
        return fns.stream(config as DeepSeekConfig, { ...chatOptions, model });
      } else if (provider === 'minimax') {
        return fns.stream(config as MiniMaxConfig, { ...chatOptions, model });
      } else {
        return fns.stream(config as Parameters<typeof portkeyStream>[0], { ...chatOptions, model });
      }
    },

    listModels(): ModelInfo[] {
      return MODELS[provider] as ModelInfo[];
    },
  };
}

// Re-export named exports for convenience
export { createAI as ai };
export type { GroqConfig } from './providers/groq.js';
export type { DeepSeekConfig } from './providers/deepseek.js';
export type { PortKeyConfig } from './providers/portkey.js';
export type { MiniMaxConfig } from './providers/minimax.js';