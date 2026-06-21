# PHILIXA 6.0 V1-MVP

Commitment and Memory Copilot for Banking Relationship Managers.

Licensed under the [MIT License](LICENSE).

V1 is intentionally scoped to a paste-notes workflow:

- RM pastes raw meeting notes.
- PHILIXA extracts meeting summary, client identity, concerns, action items, commitments, and due dates.
- Clear client notes update memory automatically.
- Ambiguous client notes are saved as "client identification required" instead of being guessed.
- Pending commitments are deduplicated per client.
- Client memory returns the latest context in a concise briefing.

V1 does not include voice recording, reminders, manager escalation, coaching, revenue intelligence, or bank statement analysis.

## Quick Start

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

Open Swagger:

```text
http://127.0.0.1:8000/docs
```

Open the dashboard UI:

```text
http://127.0.0.1:8000/
```

Protected endpoints require:

```text
X-API-Key: dev-api-key
```

Create `.env` from `.env.example` before changing configuration.

## Main Workflow

```http
POST /api/v1/meeting-notes/process
X-API-Key: dev-api-key
```

```json
{
  "raw_notes": "Met Rajesh Sharma today. Interested in business loan. Concerned about processing time. Promised documents by Friday.",
  "meeting_date": "2026-06-19"
}
```

Then fetch memory:

```http
GET /api/v1/clients/1/memory
X-API-Key: dev-api-key
```

## Environment

| Variable | Default | Purpose |
| --- | --- | --- |
| `PHILIXA_API_KEY` | `dev-api-key` | API key for protected endpoints |
| `PHILIXA_DATABASE_URL` | `sqlite:///./data/philixa.db` | SQLite database URL |
| `PHILIXA_AI_PROVIDER` | `local` | `local`, `gemini`, or `groq` |
| `PHILIXA_AI_MODEL` | `local-heuristic-v1` | AI model name |
| `PHILIXA_AI_API_KEY` | empty | Provider API key |
| `PHILIXA_AI_BASE_URL` | empty | Optional provider endpoint override |

The default `local` provider is deterministic and works without network access. It is useful for demos and tests. Gemini/Groq provider adapters are isolated behind the AI provider interface.

## Tests

```powershell
.\.venv\Scripts\python.exe -m pytest
```

## Docker

```powershell
docker build -t philixa-v1 .
docker run --rm -p 8000:8000 -e PHILIXA_API_KEY=dev-api-key philixa-v1
```
