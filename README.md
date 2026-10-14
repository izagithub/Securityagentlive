# Live Security Agent (working name) — AI security agent for live commerce

This project is an AI agent that detects fraud **before** and **during** live commerce drops.
The demo client is **Atelier Live**, a (fictional) platform that sells fractional shares of fine art on livestream.

> Concept portfolio project. Atelier Live, its artworks and its users are fictional.

## Why

Live selling breaks classic fraud tools: claims are spoken (not written), buyers decide in seconds,
and evidence disappears when the stream ends. The agent moves checks **left** (before the stream)
and keeps watching **during** it.

## How it works

```
client app ─▶ event stream ─▶ Layer 1: rules (ms) ─▶ Layer 2: AI agent (s) ─▶ actions
                                                                     ├─ auto: hide · hold · nudge · pause
                                                                     └─ human queue: refund · ban · report
```

Two phases:

| Phase | What the agent checks |
|---|---|
| **Pre-flight** (before live) | artwork provenance & gaps, stolen-art signals, seller verification, host script claims, buyer pre-registration |
| **Live** (during) | host claims vs. real data, bot chat, linked accounts / shill buying, payment & AML patterns |

## Roadmap

- [x] **Stage 0** — project skeleton, real artwork data source (Art Institute of Chicago API)
- [ ] **Stage 1** — Pre-flight agent (Claude API + tools) → `Go live: yes/no, because…`
- [ ] **Stage 2** — Evals: 30–50 labeled scenarios, accuracy & false-positive report
- [ ] **Stage 3** — Event simulator + rules + live agent, stored in Supabase
- [ ] **Stage 4** — Analyst console (Next.js, realtime)
- [ ] **Stage 5** — Atelier Live demo app (buyer + host studio)
- [ ] **Stage 6** — Product site, demo video, deploy

## Stack

| Part | Tool |
|---|---|
| Agent, simulator, evals | Python · FastAPI · Claude API |
| Database & realtime | Supabase |
| Console, demo app, site | Next.js |
| Hosting | Vercel (frontend) · Railway / Render (backend) |

## Run locally

Requirements: Python 3.11+.

```bash
cd backend
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp ../.env.example ../.env       # then paste your keys into .env
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000/docs to try the API:

- `GET /health` — is the service up
- `GET /artworks/search?q=monet` — real artworks with provenance text from the Art Institute of Chicago

Run tests:

```bash
pytest
```

## Repository layout

```
backend/
  app/
    main.py            API entry point
    models.py          data shapes (artwork, report…)
    sources/artic.py   Art Institute of Chicago client (real data)
  tests/
frontend/              (Stage 4)
```

## Security notes

- Secrets live only in `.env` (ignored by git). Never commit API keys.
- The agent can act on its own only for reversible actions (hide, hold, pause).
  Refunds, bans and reports always need a human.
