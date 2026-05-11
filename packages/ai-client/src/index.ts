/**
 * CCEC Climate Platform — OpenAI-compatible AI client.
 * Unified interface across Groq, DeepSeek, Portkey.
 * Climate-domain customization: tools, system prompts, MiniMax primary.
 *
 * Usage:
 *   import { createAI, createClimateAI } from '@ccec/ai-client';
 *
 *   // Generic
 *   const ai = createAI({ provider: 'groq', apiKey: process.env.GROQ_API_KEY });
 *
 *   // Climate-domain (MiniMax primary, Vietnam context, climate tools)
 *   const climateAI = createClimateAI({ apiKey: process.env.MINIMAX_API_KEY });
 *   const res = await climateAI.chat({ messages: [{ role: 'user', content: '...' }] });
 */

export * from './models.js';
export {
  chat as groqChat, stream as groqStream,
} from './providers/groq.js';
export {
  chat as deepseekChat, stream as deepseekStream,
} from './providers/deepseek.js';
export {
  chat as portkeyChat, stream as portkeyStream,
} from './providers/portkey.js';
export {
  chat as minimaxChat, stream as minimaxStream,
} from './providers/minimax.js';

// ---------------------------------------------------------------------------
// Unified client factory
// ---------------------------------------------------------------------------

import {
  MODELS,
  VIETNAM_CLIMATE_CONTEXT,
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
export { CLIMATE_TOOLS } from './models.js';

// ─────────────────────────────────────────────────────────────────────────────
// Climate-domain factory — MiniMax primary, Groq fallback
// ─────────────────────────────────────────────────────────────────────────────

export interface ClimateAIOptions {
  apiKey?: string;
  groqApiKey?: string;
  minimaxApiKey?: string;
  defaultModel?: string;
  temperature?: number;
}

/**
 * Climate-domain AI client.
 * Auto-selects MiniMax (primary, 1M context) → Groq (fast fallback).
 * Injects VIETNAM_CLIMATE_CONTEXT as system prompt.
 * Registers CLIMATE_TOOLS for structured climate tasks.
 */
export function createClimateAI(options: ClimateAIOptions): AIClient {
  const miniKey = options.minimaxApiKey ?? options.apiKey;
  const groqKey = options.groqApiKey ?? options.apiKey;

  // Primary: MiniMax
  const primary = createAI({
    provider: 'minimax',
    apiKey: miniKey ?? '',
    defaultModel: options.defaultModel ?? 'MiniMax-M2.7',
  });

  // Fallback: Groq
  const fallback = createAI({
    provider: 'groq',
    apiKey: groqKey ?? '',
    defaultModel: 'llama-3.3-70b-versatile',
  });

  const systemMsg = {
    role: 'system' as const,
    content: VIETNAM_CLIMATE_CONTEXT,
  };

  const injectedChat = (
    opts: Omit<ChatOptions, 'model'>,
    client: AIClient,
  ): Promise<ChatCompletionResponse> => {
    const messages = [systemMsg, ...opts.messages];
    return client.chat({ ...opts, messages });
  };

  return {
    provider: 'minimax',
    defaultModel: primary.defaultModel,

    async chat(opts: Omit<ChatOptions, 'model'>): Promise<ChatCompletionResponse> {
      try {
        return await injectedChat(opts, primary);
      } catch {
        // Groq fallback
        return await injectedChat(opts, fallback);
      }
    },

    stream(opts: Omit<ChatOptions, 'model'>): AsyncGenerator<string> {
      // eslint-disable-next-line @typescript-eslint/no-use-before-define
      return climateStream(opts, primary, fallback);
    },

    listModels(): ModelInfo[] {
      return [...MODELS.minimax, ...MODELS.groq];
    },
  };
}

async function* climateStream(
  opts: Omit<ChatOptions, 'model'>,
  primary: AIClient,
  fallback: AIClient,
): AsyncGenerator<string> {
  try {
    yield* primary.stream(opts);
  } catch {
    yield* fallback.stream(opts);
  }
}