<div align="center">

# PHILIXA 6.0
### An AI-assisted CRM workbench for relationship managers and wealth advisors

[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL_+_pgvector-316192?style=for-the-badge&logo=postgresql)](https://github.com/pgvector/pgvector)
[![LangGraph](https://img.shields.io/badge/AI-LangGraph-blueviolet?style=for-the-badge)](https://langchain-ai.github.io/langgraph/)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

**PHILIXA turns meeting notes, voice input, and audio into reviewable CRM updates, commitments, client context, and follow-up drafts.**

[Project site](https://philixa.me) · [Run locally](#run-locally) · [Architecture](ARCHITECTURE.md) · [Project notes](PROJECT.md) · [Repository](https://github.com/shouryasingh-codes/philixa-6.0)

</div>

---

## Portfolio quick view

**The problem:** Relationship teams lose context between meetings and spend too much time transcribing notes, updating records, and preparing follow-ups.

**The workflow:** Capture text, a recording, or a browser voice note → transcribe and extract clients, commitments, risks, products, and talking points → review and edit the proposed changes → sync approved updates → ask the copilot for grounded client context or draft a reminder.

**The build:** A FastAPI service and vanilla-JS workbench backed by PostgreSQL + pgvector, Redis/ARQ workers, MinIO object storage, LangGraph routing, transcription providers, and optional WhatsApp/email adapters. The implementation includes tenant-scoped RBAC, JWT/CSRF protections, rate limits, audit logging, background jobs, and a Vapi-compatible voice gateway.

**The important boundary:** AI proposes structured changes; a human reviews and confirms client creation and extracted updates before they are persisted. This reduces repetitive entry without claiming that data entry or operational review disappears.

**View it:** Visit the [PHILIXA project site](https://philixa.me) for the public showcase. The local app and API documentation are available through the setup below; they are not external demo links.

![PHILIXA dashboard preview](app/web/premium_dashboard.jpg)

## Why PHILIXA?

- **Four intake modes:** paste notes, upload audio/video up to 10 MB, record in the browser, or dictate with Web Speech.
- **Review-first extraction:** source quotes, inline edits, category filters, transcript correction, and batch sync make the proposed CRM changes inspectable.
- **Grounded copilot:** LangGraph routes questions and actions through tenant-scoped SQL and pgvector retrieval.
- **Follow-up assistance:** voice or text can draft WhatsApp/email reminders; sending remains confirmation-based.
- **Operational foundations:** workspace isolation, Owner/Admin/Member RBAC, secure cookies, CSRF protection, rate limiting, audit logs, and ARQ jobs.

## Run locally

The repository's recommended development path uses Docker Compose. It starts the app, PostgreSQL with pgvector, Redis, MinIO, and an ARQ worker.

```bash
git clone https://github.com/shouryasingh-codes/philixa-6.0.git
cd philixa-6.0
cp .env.example .env
# Add the AI key(s) needed for the features you want to exercise.
docker compose up -d --build
```

Open the **local** app at [http://localhost:8000](http://localhost:8000). Local API references are available at [http://localhost:8000/docs](http://localhost:8000/docs) and [http://localhost:8000/redoc](http://localhost:8000/redoc).

For a non-Docker setup, see the Python, PostgreSQL 16 + pgvector, Redis 7, FFmpeg, and MinIO requirements in [ARCHITECTURE.md](ARCHITECTURE.md). The full environment variable list is in [`.env.example`](.env.example).

> **Development-only credentials:** Compose uses the example MinIO account `philixa_minio` / `philixa_secret` and the placeholder PostgreSQL password from `.env.example`. Do not reuse these credentials in a shared or production environment.

### Local service links

| Service | Local URL | Purpose |
| --- | --- | --- |
| Web app | [localhost:8000](http://localhost:8000) | CRM workbench |
| Swagger | [localhost:8000/docs](http://localhost:8000/docs) | Interactive local API docs |
| ReDoc | [localhost:8000/redoc](http://localhost:8000/redoc) | Local API reference |
| MinIO console | [localhost:9001](http://localhost:9001) | Local object-storage console |
| Health check | [localhost:8000/health](http://localhost:8000/health) | Local service health |

## Technical deep dive

- [ARCHITECTURE.md](ARCHITECTURE.md) covers the system topology, ingestion/audio pipeline, LangGraph copilot, HITL policies, endpoint catalog, security controls, and deployment notes.
- [PROJECT.md](PROJECT.md) documents the isolated Vapi voice-gateway integration and its interface contracts.
- [tests/](tests/) contains unit, integration, and end-to-end coverage organized by test scope.

## Validation and tests

```bash
pytest
```

Run focused suites while developing with `pytest tests/unit/`, `pytest tests/integration/`, or `pytest tests/e2e/`.

## Roadmap

- [x] Multi-tenant workspaces, RBAC, and hardened security
- [x] Multi-modal intake with human-in-the-loop review
- [x] LangGraph copilot and voice assistant
- [x] ARQ background jobs and scheduled sweeps
- [ ] React / Next.js frontend
- [ ] Stripe billing
- [ ] Kubernetes Helm charts

## Contact and hiring

PHILIXA is an open-source portfolio project by [Shourya Singh](https://github.com/shouryasingh-codes). For collaboration, implementation work, or hiring conversations, use the [GitHub profile](https://github.com/shouryasingh-codes) or open a [repository issue](https://github.com/shouryasingh-codes/philixa-6.0/issues) with the context you would like to discuss.

## License

Distributed under the [MIT License](LICENSE).
