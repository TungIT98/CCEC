/**
 * PortKey provider — Claude Opus 4.6 via OpenAI-compatible gateway.
 * API: https://portkey.ai/docs/api
 */

import type {
  AIProviderConfig,
  ChatCompletionResponse,
  ChatOptions,
  Message,
} from '../models.js';

const PORTKEY_BASE_URL = 'https://api.portkey.ai/v1';

export interface PortKeyConfig extends AIProviderConfig {
  baseURL?: string;
  /** Optional: trace ID for observability */
  traceId?: string;
  /** Optional: metadata attached to requests */
  metadata?: Record<string, string>;
}

function buildHeaders(config: PortKeyConfig): Record<string, string> {
  const headers: Record<string, string> = {
    'Authorization': `Bearer ${config.apiKey}`,
    'Content-Type': 'application/json',
    'X-PortKey-Provider': 'anthropic',
  };
  if (config.traceId) headers['X-PortKey-Trace-Id'] = config.traceId;
  if (config.metadata) {
    headers['X-PortKey-Metadata'] = JSON.stringify(config.metadata);
  }
  return headers;
}

function toApiMessages(msgs: Message[]): Array<Record<string, unknown>> {
  return msgs.map(({ role, content, name, tool_call_id }) => {
    const msg: Record<string, unknown> = { role, content };
    if (name) msg.name = name;
    if (tool_call_id) msg.tool_call_id = tool_call_id;
    return msg;
  });
}

export async function chat(
  config: PortKeyConfig,
  options: ChatOptions,
): Promise<ChatCompletionResponse> {
  const baseURL = config.baseURL ?? PORTKEY_BASE_URL;
  const url = `${baseURL}/chat/completions`;

  const body: Record<string, unknown> = {
    model: options.model,
    messages: toApiMessages(options.messages),
    temperature: options.temperature ?? 0.7,
    max_tokens: options.max_tokens ?? 4096,
  };

  if (options.top_p !== undefined) body.top_p = options.top_p;
  if (options.tools) body.tools = options.tools;
  if (options.tool_choice) body.tool_choice = options.tool_choice;
  if (options.stream) body.stream = true;
  if (options.response_format) body.response_format = options.response_format;

  const response = await fetch(url, {
    method: 'POST',
    headers: buildHeaders(config),
    body: JSON.stringify(body),
    signal: config.timeout
      ? AbortSignal.timeout(config.timeout)
      : undefined,
  });

  if (!response.ok) {
    const error = await response.text();
    throw new Error(`PortKey API error ${response.status}: ${error}`);
  }

  const data = await response.json() as Record<string, unknown>;
  return {
    ...(data as Record<string, unknown>),
    provider: 'portkey',
  } as ChatCompletionResponse;
}

export async function* stream(
  config: PortKeyConfig,
  options: ChatOptions,
): AsyncGenerator<string> {
  const baseURL = config.baseURL ?? PORTKEY_BASE_URL;
  const url = `${baseURL}/chat/completions`;

  const body: Record<string, unknown> = {
    model: options.model,
    messages: toApiMessages(options.messages),
    temperature: options.temperature ?? 0.7,
    max_tokens: options.max_tokens ?? 4096,
    stream: true,
  };

  if (options.tools) body.tools = options.tools;
  if (options.tool_choice) body.tool_choice = options.tool_choice;

  const response = await fetch(url, {
    method: 'POST',
    headers: buildHeaders(config),
    body: JSON.stringify(body),
    signal: config.timeout
      ? AbortSignal.timeout(config.timeout)
      : undefined,
  });

  if (!response.ok) {
    const error = await response.text();
    throw new Error(`PortKey API error ${response.status}: ${error}`);
  }

  if (!response.body) throw new Error('PortKey: empty response body');

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
        if (line.startsWith('data: ')) {
          const payload = line.slice(6).trim();
          if (payload === '[DONE]') return;
          try {
            const json = JSON.parse(payload) as Record<string, unknown>;
            const delta = (json.choices as Array<Record<string, unknown>>)?.[0];
            const content = (delta?.delta as Record<string, string>)?.content;
            if (content) yield content;
          } catch {
            // skip malformed
          }
        }
      }
    }
  } finally {
    reader.releaseLock();
  }
}