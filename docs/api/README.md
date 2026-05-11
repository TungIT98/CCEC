# @ccec/ai-client

OpenAI-compatible AI client for CCEC Climate Platform.

Supports **Groq** (primary, free), **DeepSeek** (cheap), and **PortKey/Claude Opus 4.6** (premium).

## Install

```bash
pnpm install
```

## Usage

```ts
import { createAI } from '@ccec/ai-client';

// Groq (fast + free)
const ai = createAI({ provider: 'groq', apiKey: process.env.GROQ_API_KEY });
const res = await ai.chat({
  messages: [{ role: 'user', content: 'Summarize Vietnam climate trends' }],
});

// DeepSeek (cheap quality)
const ai2 = createAI({ provider: 'deepseek', apiKey: process.env.DEEPSEEK_API_KEY });

// Claude Opus 4.6 via PortKey (best reasoning)
const ai3 = createAI({ provider: 'portkey', apiKey: process.env.PORTKEY_API_KEY });

// Streaming
for await (const token of ai.stream({ messages: [...] })) {
  process.stdout.write(token);
}
```

## Environment Variables

```bash
cp .env.example .env
# Fill in GROQ_API_KEY, DEEPSEEK_API_KEY, PORTKEY_API_KEY
```

## Supported Models

| Provider | Model | Context | Best For |
|----------|-------|--------|----------|
| Groq | llama-3.3-70b-versatile | 128k | Fast general tasks |
| Groq | mixtral-8x7b-32768 | 32k | Fast MoE |
| DeepSeek | deepseek-chat | 64k | Cheap quality |
| PortKey | claude-opus-4-6 | 200k | Complex reasoning |

## Testing

```bash
pnpm test       # run once
pnpm test:watch # watch mode
```