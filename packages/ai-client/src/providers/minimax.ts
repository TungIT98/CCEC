/**
 * MiniMax provider — OpenAI-compatible.
 * Base URL: https://api.minimax.io
 * Model: MiniMax-M2.7 (supports text only).
 */

import type { ChatOptions, ChatCompletionResponse, Message } from '../models.js';

export interface MiniMaxConfig {
  apiKey: string;
  baseURL?: string;
  timeout?: number;
}

function buildHeaders(config: MiniMaxConfig) {
  return {
    'Authorization': `Bearer ${config.apiKey}`,
    'Content-Type': 'application/json',
  };
}

function toOpenAIMessages(messages: Message[]) {
  return messages.map(m => ({ role: m.role, content: m.content }));
}

export async function chat(
  config: MiniMaxConfig,
  options: ChatOptions
): Promise<ChatCompletionResponse> {
  const baseURL = config.baseURL ?? 'https://api.minimax.io';
  const url = `${baseURL}/v1/chat/completions`;

  const body = {
    model: options.model,
    messages: toOpenAIMessages(options.messages),
    temperature: options.temperature ?? 0.7,
    max_tokens: options.max_tokens ?? 4096,
    ...(options.stream ? { stream: true } : {}),
  };

  const response = await fetch(url, {
    method: 'POST',
    headers: buildHeaders(config),
    body: JSON.stringify(body),
    signal: config.timeout ? AbortSignal.timeout(config.timeout) : undefined,
  });

  if (!response.ok) {
    const text = await response.text().catch(() => '');
    throw new Error(`MiniMax error ${response.status}: ${text}`);
  }

  if (options.stream) {
    // For streaming, return a fake structured response — caller uses stream() instead
    throw new Error('Use stream() for streaming; chat() is for non-streaming only');
  }

  const data = await response.json() as {
    id: string;
    model: string;
    choices: Array<{
      message: { role: string; content: string };
      finish_reason: string;
    }>;
    usage: { prompt_tokens: number; completion_tokens: number; total_tokens: number };
  };

  return {
    id: data.id,
    object: 'chat.completion',
    created: Math.floor(Date.now() / 1000),
    model: data.model,
    provider: 'minimax',
    choices: data.choices.map((c, i) => ({
      index: i,
      message: { role: c.message.role as Message['role'], content: c.message.content },
      finish_reason: c.finish_reason as ChatCompletionResponse['choices'][0]['finish_reason'],
    })),
    usage: data.usage,
  };
}

export async function* stream(
  config: MiniMaxConfig,
  options: ChatOptions
): AsyncGenerator<string> {
  const baseURL = config.baseURL ?? 'https://api.minimax.io';
  const url = `${baseURL}/v1/chat/completions`;

  const body = {
    model: options.model,
    messages: toOpenAIMessages(options.messages),
    temperature: options.temperature ?? 0.7,
    max_tokens: options.max_tokens ?? 4096,
    stream: true,
  };

  const response = await fetch(url, {
    method: 'POST',
    headers: buildHeaders(config),
    body: JSON.stringify(body),
    signal: config.timeout ? AbortSignal.timeout(config.timeout) : undefined,
  });

  if (!response.ok) {
    const text = await response.text().catch(() => '');
    throw new Error(`MiniMax stream error ${response.status}: ${text}`);
  }

  if (!response.body) throw new Error('MiniMax: empty response body');

  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer = '';

  try {
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split('\n');
      buffer = lines.pop() ?? '';
      for (const line of lines) {
        const trimmed = line.trim();
        if (!trimmed || trimmed === 'data: [DONE]' || trimmed.startsWith('data: ')) {
          if (trimmed === 'data: [DONE]') continue;
          const jsonStr = trimmed.startsWith('data: ') ? trimmed.slice(6) : trimmed;
          if (!jsonStr) continue;
          try {
            const parsed = JSON.parse(jsonStr);
            const content = parsed.choices?.[0]?.delta?.content;
            if (content) yield content;
          } catch { /* skip malformed */ }
        }
      }
    }
  } finally {
    reader.releaseLock();
  }
}