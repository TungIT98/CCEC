import { describe, it, expect, vi, beforeEach } from 'vitest';
import { MODELS, DEFAULT_MODELS, type ProviderName } from '../src/models.js';

// ---------------------------------------------------------------------------
// models.ts
// ---------------------------------------------------------------------------

describe('models.ts', () => {
  describe('MODELS', () => {
    it('includes groq models', () => {
      const groqModels = MODELS.groq;
      expect(groqModels.length).toBeGreaterThan(0);
      const llama = groqModels.find(m => m.id === 'llama-3.3-70b-versatile');
      expect(llama).toBeDefined();
      expect(llama!.supportsTools).toBe(true);
    });

    it('includes deepseek models', () => {
      const dsModels = MODELS.deepseek;
      expect(dsModels.length).toBeGreaterThan(0);
      expect(dsModels.some(m => m.id === 'deepseek-chat')).toBe(true);
    });

    it('includes portkey models', () => {
      const pkModels = MODELS.portkey;
      expect(pkModels.length).toBeGreaterThan(0);
    });

    it('has context window and capability flags for all models', () => {
      for (const provider of ['groq', 'deepseek', 'portkey'] as ProviderName[]) {
        for (const model of MODELS[provider]) {
          expect(model.contextWindow).toBeGreaterThan(0);
          expect(typeof model.supportsTools).toBe('boolean');
          expect(typeof model.supportsVision).toBe('boolean');
          expect(typeof model.supportsJsonMode).toBe('boolean');
        }
      }
    });
  });

  describe('DEFAULT_MODELS', () => {
    it('has defaults for all providers', () => {
      for (const provider of ['groq', 'deepseek', 'portkey'] as ProviderName[]) {
        expect(DEFAULT_MODELS[provider]).toBeTruthy();
        const defaults = Object.values(DEFAULT_MODELS);
        expect(defaults).toContain(DEFAULT_MODELS[provider]);
      }
    });
  });
});

// ---------------------------------------------------------------------------
// createAI factory
// ---------------------------------------------------------------------------

import { createAI } from '../src/index.js';

describe('createAI', () => {
  it('creates a groq client with correct defaults', () => {
    const ai = createAI({ provider: 'groq', apiKey: 'test-key' });
    expect(ai.provider).toBe('groq');
    expect(ai.defaultModel).toBe('llama-3.3-70b-versatile');
  });

  it('creates a deepseek client with correct defaults', () => {
    const ai = createAI({ provider: 'deepseek', apiKey: 'test-key' });
    expect(ai.provider).toBe('deepseek');
    expect(ai.defaultModel).toBe('deepseek-chat');
  });

  it('creates a portkey client with correct defaults', () => {
    const ai = createAI({ provider: 'portkey', apiKey: 'test-key' });
    expect(ai.provider).toBe('portkey');
    expect(ai.defaultModel).toBe('claude-opus-4-6');
  });

  it('allows overriding default model', () => {
    const ai = createAI({
      provider: 'groq',
      apiKey: 'test-key',
      defaultModel: 'mixtral-8x7b-32768',
    });
    expect(ai.defaultModel).toBe('mixtral-8x7b-32768');
  });

  it('listModels returns models for the provider', () => {
    const ai = createAI({ provider: 'groq', apiKey: 'test-key' });
    const models = ai.listModels();
    expect(models.length).toBeGreaterThan(0);
    expect(models.every(m => m.provider === 'groq')).toBe(true);
  });

  it('chat uses the provided model when specified', async () => {
    const ai = createAI({ provider: 'groq', apiKey: 'test-key' });
    // Intercept fetch to verify the model sent
    const mockResponse = {
      id: 'chat-1',
      object: 'chat.completion',
      created: Date.now(),
      model: 'mixtral-8x7b-32768',
      provider: 'groq',
      choices: [{ index: 0, message: { role: 'assistant', content: 'hi' }, finish_reason: 'stop' }],
      usage: { prompt_tokens: 10, completion_tokens: 5, total_tokens: 15 },
    };

    const fetchMock = vi.fn().mockResolvedValue({
      ok: true,
      json: () => Promise.resolve(mockResponse),
    });
    global.fetch = fetchMock;

    await ai.chat({
      model: 'mixtral-8x7b-32768',
      messages: [{ role: 'user', content: 'hi' }],
    });

    expect(fetchMock).toHaveBeenCalled();
    const [, opts] = fetchMock.mock.calls[0] as [string, RequestInit];
    const body = JSON.parse(opts.body as string);
    expect(body.model).toBe('mixtral-8x7b-32768');

    global.fetch = vi.fn();
  });
});

// ---------------------------------------------------------------------------
// Provider streaming implementations
// ---------------------------------------------------------------------------

import { stream as groqStream } from '../src/providers/groq.js';
import { stream as deepseekStream } from '../src/providers/deepseek.js';
import { stream as portkeyStream } from '../src/providers/portkey.js';

describe('Provider streaming', () => {
  beforeEach(() => {
    vi.restoreAllMocks();
  });

  it('groqStream yields content chunks from SSE', async () => {
    const mockBody = new ReadableStream({
      start(controller) {
        const lines = [
          'data: {"choices":[{"delta":{"content":"hello"}}]}',
          'data: {"choices":[{"delta":{"content":" world"}}]}',
          'data: [DONE]',
        ];
        for (const line of lines) controller.enqueue(new TextEncoder().encode(line + '\n'));
        controller.close();
      },
    });

    global.fetch = vi.fn().mockResolvedValue({
      ok: true,
      body: mockBody,
    });

    const chunks: string[] = [];
    for await (const chunk of groqStream(
      { apiKey: 'test-key' },
      { model: 'llama-3.3-70b-versatile', messages: [{ role: 'user', content: 'hi' }] },
    )) {
      chunks.push(chunk);
    }

    expect(chunks).toEqual(['hello', ' world']);
  });

  it('deepseekStream yields content chunks from SSE', async () => {
    const mockBody = new ReadableStream({
      start(controller) {
        const lines = [
          'data: {"choices":[{"delta":{"content":"hi"}}]}',
          'data: [DONE]',
        ];
        for (const line of lines) controller.enqueue(new TextEncoder().encode(line + '\n'));
        controller.close();
      },
    });

    global.fetch = vi.fn().mockResolvedValue({
      ok: true,
      body: mockBody,
    });

    const chunks: string[] = [];
    for await (const chunk of deepseekStream(
      { apiKey: 'test-key' },
      { model: 'deepseek-chat', messages: [{ role: 'user', content: 'hi' }] },
    )) {
      chunks.push(chunk);
    }

    expect(chunks).toEqual(['hi']);
  });

  it('portkeyStream yields content chunks from SSE', async () => {
    const mockBody = new ReadableStream({
      start(controller) {
        const lines = [
          'data: {"choices":[{"delta":{"content":"claude"}}]}',
          'data: [DONE]',
        ];
        for (const line of lines) controller.enqueue(new TextEncoder().encode(line + '\n'));
        controller.close();
      },
    });

    global.fetch = vi.fn().mockResolvedValue({
      ok: true,
      body: mockBody,
    });

    const chunks: string[] = [];
    for await (const chunk of portkeyStream(
      { apiKey: 'test-key' },
      { model: 'claude-opus-4-6', messages: [{ role: 'user', content: 'hi' }] },
    )) {
      chunks.push(chunk);
    }

    expect(chunks).toEqual(['claude']);
  });

  it('provider chat throws on non-200 response', async () => {
    global.fetch = vi.fn().mockResolvedValue({
      ok: false,
      status: 401,
      text: () => Promise.resolve('Unauthorized'),
    });

    await expect(
      groqStream(
        { apiKey: 'bad-key' },
        { model: 'llama-3.3-70b-versatile', messages: [{ role: 'user', content: 'hi' }] },
      ).next(),
    ).rejects.toThrow('Groq API error 401: Unauthorized');
  });
});