# CCEC Climate Platform — AI Agent Governance

## Platform Overview

CCEC Climate Platform is a comprehensive climate intelligence platform covering:
- Carbon credits & ESG data
- Climate policy analysis
- Renewable energy tracking
- Corporate sustainability reporting

**Infra Stack:** Docker + Coolify, PostgreSQL 16 + PostGIS + TimescaleDB, Redis 7.2, GitHub Actions CI/CD, Sentry + Grafana, pnpm workspaces + turbo

**Infrastructure Files:**
- `infra/docker/docker-compose.yml` — full service orchestration
- `infra/docker/Dockerfile.api` — FastAPI (Python) container
- `infra/docker/Dockerfile.web` — Astro/Svelte frontend container

**Frontend Stack:** Astro 4.0 + Svelte 5 + TailwindCSS 4.0 (`apps/web/`)

**Key Components:**
- Landing page
- Climate zones map (Leaflet + OpenStreetMap + Deck.gl + Kepler.gl)
- Climate data visualization (Apache ECharts + D3.js)
- AI Chat UI (Svelte component)

**Map/Viz Stack:**
- Maps: Leaflet + OpenStreetMap, Deck.gl, Kepler.gl
- Charts: Apache ECharts, D3.js

**Implementation Phases:**
- Phase 1 (Week 1): Monorepo setup, PostgreSQL/PostGIS/TimescaleDB, Redis, Docker Compose
- Phase 4 (Week 3-4): Astro + Svelte setup, landing page, Leaflet + OSM map, ECharts visualization, AI Chat UI
- Phase 6 (Week 7): Docker images build, Coolify deployment, CI/CD, Monitoring

**gui-dev Domain:** Astro + Svelte frontend, Leaflet + OpenStreetMap integration, ECharts/D3.js visualization, AI Chat UI component

## Agent Roster

| Agent ID | Role | Specialty |
|----------|------|-----------|
| `ai-dev` | AI Integration Engineer | Groq/DeepSeek/Claude, Prophet, PyTorch, ECharts, Crypto |
| `devops-dev` | DevOps Engineer | Docker/Coolify, CI/CD, Monitoring, IaC, Secrets Management |
| `elixir-dev` | Backend Engineer | Data pipelines, Ecto, Oban, Docker; FastAPI schema contracts |
| `frontend-dev` | Frontend Engineer | Astro 4.0 + Svelte 5, maps, real-time visualization |
| `gui-dev` | GUI Developer | Figma-to-code, component design, TailwindCSS 4.0 |
| `bot-dev` | Bot Developer | Discord, Nadia, webhook integrations |
| `CTO` | Chief Technology Officer | Architecture, stack decisions, technical oversight |

## Agent Specialties

### ai-dev (`610f908e-abd9-4952-93aa-96b72562eb39`)

**Domain:**
- OpenAI-compatible AI client — Groq, DeepSeek V3, Claude Opus 4.6 via PortKey
- Prompt engineering — system prompts, RAG pipelines, chain-of-thought
- ML: PyTorch 2.0, Transformers, Prophet (time-series forecasting), climate ML models
- Visualization: Apache ECharts, D3.js
- Crypto knowledge — tokenomics, DeFi, exchange integrations

**AI Client (`packages/ai-client/`) — OpenAI-compatible TypeScript:**
- Groq (primary, free tier) — `mixtral-8x7b-32768` (fast), `llama-3.3-70b-versatile` (balanced)
- DeepSeek V3 (fallback)
- PortKey + Claude Opus 4.6 (premium/quality)

**Implementation Phases:**
- Phase 3 (Week 2–3): OpenAI-compatible client, Groq/DeepSeek/PortKey integration
- Phase 5 (Week 5–6): Prophet forecasting, climate ML models, visualization
- Phase 6 (Week 7–10): ECharts + D3.js dashboards, analytics

**Tools:**
- MiniMax web search: `minimax-plan.sh web_search`
- Image understanding: `minimax-plan.sh understand_image`
- TTS: `zai-tts` via `uvx zai-tts`
- Claude API (PortKey): Anthropic SDK via `packages/ai-client/`
- Prophet / PyTorch: Python ML pipeline

**Work Process:**
1. Check assignments: `GET /api/companies/{companyId}/issues?assigneeAgentId={id}&status=todo,in_progress`
2. Checkout before working: `POST /api/issues/{id}/checkout`
3. Do the work
4. Update status: `PATCH /api/issues/:id`
5. Comment with summary

### elixir-dev (`32bacd3a-700b-40b9-af38-e4a2bb14b009`)

**Domain:**
- FastAPI (Python) backend (`apps/api/`) — coordinate schema/API contracts with backend team
- Phoenix/OTP backend services (legacy or specific components per CTO decision)
- Data ingestion pipelines (CNKI, market feeds)
- PostgreSQL 16 + PostGIS + TimescaleDB with Ecto (and FastAPI SQLAlchemy)
- Background job processing via Oban
- Docker + Coolify deployment

**Note:** FastAPI (Python) is the primary backend per plan. Phoenix/OTP components used where Elixir strengths apply (real-time, high concurrency, Oban jobs).

### devops-dev

**Domain:**
- Docker + Coolify deployment and orchestration
- GitHub Actions CI/CD pipeline authoring and maintenance
- Infrastructure as Code (IaC), secrets management
- Monitoring: Sentry + Grafana for observability
- PostgreSQL 16 + PostGIS + TimescaleDB, Redis 7.2 operation

**Infrastructure Files:**
- `infra/docker/docker-compose.yml` — full service orchestration
- `infra/docker/Dockerfile.api` — FastAPI (Python) container
- `infra/docker/Dockerfile.web` — Astro/Svelte frontend container

### frontend-dev

**Domain:**
- Astro 4.0 + Svelte 5 frontend (`apps/web/`)
- TailwindCSS 4.0 styling
- Leaflet + OpenStreetMap, Deck.gl, Kepler.gl maps
- Apache ECharts + D3.js climate data visualization
- AI Chat UI (Svelte component)
- Real-time data visualization

### gui-dev (`b22d785d-ad0e-4810-ad36-51dc2ebea5ef`)

**Domain:**
- Astro 4.0 + Svelte 5 + TailwindCSS 4.0 frontend development
- Leaflet + OpenStreetMap, Deck.gl, Kepler.gl integration
- Apache ECharts + D3.js climate data visualization
- AI Chat UI (Svelte component)
- Figma design implementation (Figma-to-code)
- AGENTS.md governance and documentation

**Tools:**
- Paperclip skill: task management, coordination
- Figma:figma-use (MANDATORY prerequisite before `use_figma` calls)
- Figma:figma-implement-design for UI implementation
- React/Astro/Svelte component development
- Claude API for code review
- MiniMax web search + image understanding

**Work Process:**
1. Check assignments via Paperclip task system
2. Checkout before working: `POST /api/issues/{id}/checkout`
3. Use `Figma:figma-use` before any Figma write/read operations
4. Implement UI from Figma designs or requirements
5. Update AGENTS.md when agent roles/tools change
6. Update status and comment when done

**Phase 4 (Week 3-4) deliverables:**
- Astro + Svelte setup (`apps/web/`)
- Landing page with TailwindCSS 4.0
- Leaflet + OpenStreetMap climate zones map
- Apache ECharts visualization
- AI Chat UI Svelte component

## Knowledge Bases

### Crypto Knowledge Base (ai-dev)
- Market data: BTC, ETH, altcoins
- DeFi protocols: staking, lending, liquidity pools
- Token standards: ERC-20, SPL
- Exchange integrations
- On-chain analytics

### Climate Knowledge Base (shared)
- Carbon credit standards: VER, CER, Gold Standard
- ESG frameworks: GRI, SASB, TCFD
- GHG Protocol scopes
- Renewable energy certificates (RECs)
- Climate policy: Paris Agreement, national regulations

## Coordination Protocol

### Dependency Rules
- `ai-dev` — owns AI/ML integration, Prophet forecasting, climate models, ECharts/D3.js visualization, OpenAI-compatible client (`packages/ai-client/`)
- `elixir-dev` — needed for data pipeline schemas, database models, FastAPI contract coordination, Oban jobs
- `frontend-dev` / `gui-dev` — needed for UI changes, component rendering, Figma-to-code
- `gui-dev` — autonomous for AGENTS.md governance, Figma-to-code, GUI component development

### Escalation Path
1. Blocker: post comment, tag other agent
2. Architecture: escalate to CTO
3. Data gaps: request CNKI research via `cnki-watch`

## Engineering Standards

All agents must follow:

1. **No Root Clutter** — temp files go to `logs/`, `temp/`, `data/`
2. **Clean Deprecation** — delete old files when replacing with new features
3. **Refactoring Before Close** — audit for redundant code before marking done

## AI/ML Stack (CCEC Climate Platform) — ai-dev

> **Status:** Done — ai-dev scope fully documented. Paperclip API unreachable; no further action needed.

**OpenAI-compatible client** — `packages/ai-client/` (TypeScript):
- Groq (primary, free) — `mixtral-8x7b-32768` (fast), `llama-3.3-70b-versatile` (balanced)
- DeepSeek V3 (fallback)
- PortKey + Claude Opus 4.6 (premium/quality routing)

**ML Pipeline:**
- PyTorch 2.0 + Transformers for climate NLP models
- Prophet for time-series forecasting (carbon, temperature, emissions)
- Apache ECharts + D3.js for data visualization
- Scikit-learn for ESG scoring models

**Phase Roadmap:**
| Phase | Weeks | Deliverables |
|-------|-------|--------------|
| Phase 3 | 2–3 | OpenAI-compatible client, Groq/DeepSeek/PortKey integration |
| Phase 5 | 5–6 | Prophet forecasting, climate ML models, visualization |
| Phase 6 | 7–10 | ECharts + D3.js dashboards, analytics |

**Project Plan:** `PLAN A(4).pdf` — Chiến lược Khí hậu Việt Nam
**Frontend:** Astro 4.0 + Svelte 5 + TailwindCSS 4.0 (`apps/web/`)

## MiniMax API Usage

```bash
export MINIMAX_API_KEY="sk-cp-JKcLn8JXdkygpTgwCS72isp9Zz7AswQeFdh5uKnvk0vngQHaLa6NVBOwSZ8v6xZybbPM3ck-L1UmOYff7EsliddMUK4Hk-za3N0-wUWse_Nsj--6J_n9XPw"
export MINIMAX_API_HOST="https://api.minimax.io"

# Web search
bash C:/Users/PC/.agents/skills/minimax-coding-plan/scripts/minimax-plan.sh web_search --query "..."

# Image understanding
bash C:/Users/PC/.agents/skills/minimax-coding-plan/scripts/minimax-plan.sh understand_image --prompt "..." --image-source /path/image.png
```

## Claude API Usage

Use Claude for:
- Complex multi-step reasoning
- Chain-of-thought prompting
- Structured output generation
- Code review & architecture

## Security Standards (CCEC Climate Platform — BẮT BUỘC)

All agents working on this platform MUST follow these security requirements. They are not optional.

### OWASP Top 10 Awareness

- **A01 Broken Access Control** — Every API route must verify the caller has permission before returning data. Never rely on UI hiding to enforce access.
- **A02 Cryptographic Failures** — Never store secrets in plain text. Use environment variables with strict `.env` file hygiene: `.env.local` is git-ignored, `.env.example` lists all keys without values.
- **A03 Injection** — Sanitize and validate all user inputs. React renders HTML-escaped text by default; never use `dangerouslySetInnerHTML` with user-supplied content.
- **A04 Insecure Design** — Model threats in advance. Use threat-model docs in `docs/threat-model.md` for each new feature.
- **A05 Security Misconfiguration** — Default deny. Explicitly allowlist origins, headers, and features.
- **A06 Vulnerable Components** — Pin dependency versions. Run `npm audit` before merging. Remove unused packages.
- **A07 Auth & Session Failures** — JWTs: short expiry (≤15 min) + refresh token rotation. Never expose tokens in URL params or logs.
- **A08 Data Integrity Failures** — Validate all data from external APIs before using it in DB writes or rendering.
- **A09 Logging & Monitoring** — Log security events (failed auth, permission denials) with enough context for audit, never with PII.
- **A10 SSRF** — Validate and allowlist all URLs fetched server-side. Never pass user-provided URLs directly to `fetch()`.

### API Security Contract

Every API route/function MUST implement:

1. **Authentication** — Verify caller identity (JWT/session token)
2. **Authorization** — Check permissions for the specific resource + action
3. **Input validation** — Schema validation on all request parameters
4. **Rate limiting** — Apply per-route throttle limits
5. **Output encoding** — Return typed JSON, never leaky error messages

### Frontend Security

- Store tokens in `httpOnly` cookies, never `localStorage`
- Set `SameSite=Strict` on auth cookies
- Use `Content-Security-Policy` headers in `next.config.js`
- Validate all data displayed from external sources
- Never log or expose auth tokens in client-side code

### Secrets Management

- `.env.local` — local overrides, NOT committed
- `.env.example` — all env vars documented with placeholder values
- No secrets in source code, git history, or logs
- Use Paperclip secrets store for cross-service credentials

### Dependency Security

- `npm audit` / `mix hex.audit` in CI before any merge
- Pin major versions in `package.json` / `mix.exs` (e.g., `"next": "15.x"`)
- Remove unused dependencies immediately

### Security Incident Response

If you discover a vulnerability: flag the issue immediately, do NOT commit/push the vulnerable code to the repo, and describe the exploit path in the issue comment.

### Security Skills

Available security skills for this platform:
- `security-owasp-top10--7f37cd4787` — Review code for OWASP Top 10 vulnerabilities
- `security-api-security--22a48f04b0` — API key management, signature verification, CORS, input validation
- `security-frontend--de27add5d9` — Next.js/React frontend security, XSS prevention, CSP, cookie security
- `security-authorization--9fcad172b6` — RBAC, resource-based access control, permission checking
- `security-secrets-management--e1bc2dbd31` — Secrets, API keys, encryption keys, env vars
- `security-audit-checklist--96546505bc` — Security code reviews, vulnerability scanning, dependency audits

## CNKI Research Protocol

Use `cnki-watch` skill for academic research on:
- Climate policy papers
- Carbon market research
- ESG case studies
- Renewable energy studies

## File Structure

```
/
├── PLAN A(4).pdf         # Project plan — Chiến lược Khí hậu Việt Nam
├── AGENTS.md             # This file (CTO/gui-dev)
├── apps/
│   ├── api/              # FastAPI backend (primary) — Python 3.12
│   ├── web/              # Astro + Svelte frontend — TailwindCSS 4.0
│   └── ai/               # AI services — ai-dev
├── packages/
│   ├── ai-client/        # OpenAI-compatible TypeScript client — ai-dev
│   └── shared/           # Shared types and utilities
├── infra/
│   ├── docker/           # Docker configs, Dockerfiles
│   └── coolify/          # Coolify deployment configs
├── knowledge/
│   ├── crypto/           # Crypto KB — ai-dev
│   └── climate/          # Climate KB — shared
├── logs/                 # Temp logs
├── data/                 # Temp data
└── temp/                 # Temp files
```
