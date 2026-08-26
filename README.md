<div align="center">

# 🚀 PHILIXA 6.0
### The Agentic AI-First CRM for Modern Relationship Managers & Wealth Advisors

[![FastAPI](https://img.shields.io/badge/Backend-FastAPI_0.137-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL_15_+_pgvector-316192?style=for-the-badge&logo=postgresql)](https://github.com/pgvector/pgvector)
[![LangGraph](https://img.shields.io/badge/AI_Orchestration-LangGraph_StateGraph-blueviolet?style=for-the-badge&logo=langchain)](https://langchain-ai.github.io/langgraph/)
[![Groq Cloud](https://img.shields.io/badge/Inference-Groq_Llama_3.3_70B-F55036?style=for-the-badge)](https://groq.com/)
[![Redis & ARQ](https://img.shields.io/badge/Task_Queue-Redis_7_+_ARQ_Worker-DC382D?style=for-the-badge&logo=redis)](https://arq-docs.helpmanual.io/)
[![MinIO S3](https://img.shields.io/badge/Object_Storage-MinIO_S3-C72C48?style=for-the-badge&logo=minio)](https://min.io/)
[![Docker](https://img.shields.io/badge/Containers-5_Service_Compose-2496ED?style=for-the-badge&logo=docker)](https://www.docker.com/)
[![Deepgram](https://img.shields.io/badge/STT-Deepgram_Nova--2-13EF93?style=for-the-badge)](https://deepgram.com/)
[![Sarvam AI](https://img.shields.io/badge/Voice_TTS-Sarvam_AI_Hinglish-6842FF?style=for-the-badge)](https://www.sarvam.ai/)
[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](https://opensource.org/licenses/MIT)

<br/>

**[ [🌐 Web App](http://localhost:8000) ] · [ [📖 API Docs (Swagger)](http://localhost:8000/docs) ] · [ [📚 ReDoc Reference](http://localhost:8000/redoc) ] · [ [🗄️ MinIO Console](http://localhost:9001) ] · [ [🏗 System Architecture](#-system-architecture) ] · [ [🚀 Quickstart](#-quickstart--deployment-guide) ] · [ [💬 WhatsApp Webhook](#29-notification-preferences--whatsapp-webhooks) ]**

</div>

---

## 📑 Table of Contents

- [Executive Overview](#-executive-overview)
- [Why Philixa 6.0?](#-why-philixa-60)
- [System Architecture](#-system-architecture)
  - [High-Level Architecture Topology](#high-level-architecture-topology)
  - [End-to-End Component Flowchart](#end-to-end-component-flowchart)
  - [LangGraph Agentic Copilot Routing](#langgraph-agentic-copilot-routing)
- [Deep Dive: Core Subsystems](#-deep-dive-core-subsystems)
  - [1. Multi-Tenant Workspace & Hardened Auth Core](#1-multi-tenant-workspace--hardened-auth-core)
  - [2. Multi-Modal Meeting Ingestion & Voice Pipelines](#2-multi-modal-meeting-ingestion--voice-pipelines)
  - [3. Stateful Agentic Copilot & Vector RAG Pipeline](#3-stateful-agentic-copilot--vector-rag-pipeline)
  - [4. Distributed ARQ Worker & Scheduled Sweeps](#4-distributed-arq-worker--scheduled-sweeps)
  - [5. Dual-Channel Notification Engine](#5-dual-channel-notification-engine)
- [Interactive Developer & Management Portals](#-interactive-developer--management-portals)
- [Complete 48-Endpoint API Catalog](#-complete-48-endpoint-api-catalog)
- [Database Entity Relationship & 17 Relational Models](#-database-entity-relationship--17-relational-models)
- [Master Configuration Matrix](#-master-configuration-matrix)
- [Quickstart & Deployment Guide](#-quickstart--deployment-guide)
  - [Option A: 5-Container Docker Compose (Recommended)](#option-a-5-container-docker-compose-recommended)
  - [Option B: Bare-Metal Virtualenv Setup](#option-b-bare-metal-virtualenv-setup)
  - [One-Click Demo Sandbox Evaluation](#one-click-demo-sandbox-evaluation)
- [Verified cURL Workflows](#-verified-curl-workflows)
- [Testing & Quality Assurance](#-testing--quality-assurance)
- [Roadmap & Engineering Milestones](#-roadmap--engineering-milestones)
- [Contributing & License](#-contributing--license)

---

## 🎯 Executive Overview

**PHILIXA 6.0** is an enterprise-grade, agentic AI-first Customer Relationship Management (CRM) platform engineered specifically for **Relationship Managers (RMs), Private Wealth Advisors, Corporate Bankers, and B2B Account Executives**. 

Traditional CRMs turn client-facing professionals into manual data-entry clerks, resulting in stale client context, unfulfilled commitments, and lost revenue. Philixa 6.0 eliminates manual administrative overhead by transforming **unstructured client interactions**—including dictated voice notes, multipart audio recordings, live meeting audio streams, and raw pasted notes—into structured CRM entities, automated commitment logs, and proactive relationship briefings.

### Architectural Pillars for Systems Architects & Hiring Managers
- 🛡️ **Enterprise Multi-Tenancy & Hardened Session Security**: Strict tenant isolation across all entities via `TenantMixin`, Bcrypt password hashing (`cost >= 12`), HttpOnly + SameSite=Lax JWT cookie pairs, single-flight 401 refresh token rotation, double-submit CSRF protection (`X-CSRF-Token`), and single-use Redis-backed WebSocket ticket replay defense.
- 🎙️ **Multi-Modal Meeting Capture**: Four specialized ingestion pipelines supporting direct raw text (`MeetingSourceType.PASTED_NOTE`), MinIO S3 multipart audio uploads (`AUDIO_UPLOAD`), live 16kHz Int16 PCM WebSocket streaming (`LIVE_BROWSER`), and zero-latency browser dictation in Indian English (`en-IN`).
- 🧠 **Hybrid LangGraph State Machine & Vector RAG**: A stateful LangGraph execution graph orchestrating natural language-to-SQL generation with automatic multi-tenant RBAC injection, deterministic fast-path routing, and hybrid cosine similarity search over 1024-dimensional `BAAI/bge-m3` vectors in PostgreSQL `pgvector`.
- ⚡ **Asynchronous Background Processing & Distributed Cron**: Powered by ARQ (`asyncio` + Redis) workers handling offline Whisper transcription with specialized Indian banking prompts, Pyannote diarization, vector embedding generation, and daily automated cron sweeps (07:00 UTC morning RM briefings and 08:00 UTC overdue commitment sweeps).
- 📱 **Dual-Channel Notification Architecture**: Strict architectural decoupling between isolated transactional SMTP email (`aiosmtplib`) for authentication workflows and Meta WhatsApp Cloud API v25.0 for proactive RM alerts with quiet-hours enforcement and delivery receipt tracking.

---

## 💡 Why Philixa 6.0?

| Capability / Architectural Dimension | Traditional Legacy CRMs (Salesforce / HubSpot) | Generic AI Wrapper CRMs | **Philixa 6.0 Enterprise Platform** |
|---|---|---|---|
| **Data Ingestion Paradigm** | Manual forms, rigid dropdowns, tedious manual data entry | Single text box with generic prompt wrapper | **4 Ingestion Modes**: Text Paste, MinIO Audio Upload, Live PCM Streaming, and Web Speech Dictation |
| **Meeting Intelligence & Extraction** | None (Requires third-party recorder extensions) | Basic OpenAI call with generic unstructured summary | **Hinglish-Tuned Multi-Stage AI Pipeline**: Whisper + Deepgram STT, Groq Llama 3.3 70B extraction, and Gemini fallback |
| **Human-in-the-Loop (HITL) Triage** | Manual duplicate merging | Full blind AI auto-creation (causes data pollution) | **Dedicated HITL Modals**: Ambiguous client confirmation (`#confirmPanel`) and noisy transcript correction (`#editTranscriptPanel`) |
| **Portfolio Querying & Copilot** | Complex SQL/SOQL or static reports | Vector-only semantic search or ungrounded SQL | **Hybrid LangGraph StateGraph**: Deterministic fast-paths, safe read-only SQL with auto RBAC filters, and pgvector cosine search |
| **Tenant & Data Isolation** | Organization-level tables with high licensing cost | Single-tenant or software-level user filtering | **Strict Multi-Tenant Model**: Composite memberships (`owner`, `admin`, `member`), repository-level scoping, and cascade deletion |
| **Session Security & Defense** | Standard session cookies | Insecure Bearer tokens in `localStorage` | **Hardened Security**: HttpOnly JWT cookies, single-flight refresh rotation, double-submit CSRF, and single-use signed WS tickets |
| **Background Queue & Automation** | Expensive Enterprise schedulers | Synchronous request blocking or toy threading | **Distributed ARQ + Redis Workers**: Async STT queues and automated 07:00/08:00 UTC daily cron sweeps |
| **Proactive RM Notification** | Generic email digests | In-app notification popups only | **Meta WhatsApp Cloud API v25.0** + isolated SMTP with timezone-aware quiet hours and delivery tracking |

---

## 🏗 System Architecture

### High-Level Architecture Topology

```
+-----------------------------------------------------------------------------------------------------------------------------------+
|                                                 PHILIXA 6.0 DISTRIBUTED ARCHITECTURE                                              |
+-----------------------------------------------------------------------------------------------------------------------------------+

      [ Single-Page Application (SPA) ]               [ External Channels ]                 [ AI & Cloud Microservices ]
     /        |               |        \                        |                                        |
+-------+ +-------+       +-------+ +-------+           +---------------+              +-----------------------------------+
| Paste | | Audio |       | Live  | | Voice |           | Meta WhatsApp |              |  Groq Cloud (Llama 3.3 70B Vers)  |
| Notes | | Drag  |       | Audio | | Brain |           |  Cloud v25.0  |              |  Google Gemini (2.5/3.6 Flash)    |
| (Raw) | | (S3)  |       | (PCM) | | (FAB) |           |  (Webhooks)   |              |  Deepgram Nova-2 / Sarvam AI TTS  |
+-------+ +-------+       +-------+ +-------+           +---------------+              |  BAAI/bge-m3 (SentenceTransf.)    |
    |         |               |         |                       |                      +-----------------------------------+
    |         |               |         |                       |                                        ^
    +---------+---------------+---------+                       |                                        |
                      |                                         |                                        |
                      v                                         v                                        v
+-----------------------------------------------------------------------------------------------------------------------------------+
|                                          FASTAPI ASYNC APPLICATION CORE (Port :8000)                                              |
|                                                                                                                                   |
|  [ Middlewares ]                                                                                                                  |
|  * CORS Policy (Allowed Origins)                                                                                                  |
|  * CSRFProtectionMiddleware (Double-Submit X-CSRF-Token Verification)                                                             |
|                                                                                                                                   |
|  [ Security & Multi-Tenant Context ]                                                                                              |
|  * Bcrypt Hashing (Cost 12)  * HttpOnly JWT Cookies (Access 15m / Refresh 30d)  * WS Single-Use Tickets (60s TTL + Replay Guard)   |
|  * CurrentPrincipal Injection: User ID, Active Organization ID, Canonical Role (owner | admin | member)                            |
|                                                                                                                                   |
|  [ API Router Subsystems (48 Distinct Operations) ]                                                                               |
|  * /auth           * /workspaces        * /api/v1/clients       * /api/v1/meeting-notes   * /api/v1/commitments                   |
|  * /audio          * /live/transcribe   * /api/v1/voice         * /api/v1/dashboard       * /api/v1/preferences                   |
|  * /api/v1/webhooks/whatsapp            * /api/v1/jobs          * /health                 * /docs & /redoc                        |
|                                                                                                                                   |
|  [ Hybrid LangGraph Agentic Copilot Service ]                                                                                     |
|  * Fast-Paths: Greeting / Asia/Kolkata Meeting Calendar / Client Lookup                                                           |
|  * StateGraph: planner_node --> (sql_generator_node [Safe RBAC SQL] | semantic_node [pgvector]) --> synthesizer_node             |
+-----------------------------------------------------------------------------------------------------------------------------------+
           |                                     |                                         |
           v                                     v                                         v
+-----------------------+             +-----------------------+                 +-----------------------+
|  POSTGRESQL + PGVECTOR|             |     REDIS 7 CACHE     |                 |  MINIO S3 OBJECT STR  |
|      (Port :5432)     |             |      (Port :6379)     |                 |  (API :9000 | UI :9001)|
+-----------------------+             +-----------------------+                 +-----------------------+
| * 17 Relational Tables|             | * ARQ Job Queues      |                 | * Bucket: philixa-audio|
| * Multi-Tenant Scoping|             | * WS Replay Guard Keys|                 | * Tenant Namespaces:  |
| * 1024-dim BAAI/bge-m3|             | * User Session State  |                 |   {org}/{user}/{meet} |
|   Cosine Index (<=>)  |             |                       |                 | * Presigned URL Auth  |
+-----------------------+             +-----------------------+                 +-----------------------+
           ^                                     ^                                         ^
           |                                     |                                         |
           +-------------------------------------+-----------------------------------------+
                                                 |
                                                 v
+-----------------------------------------------------------------------------------------------------------------------------------+
|                                            ARQ ASYNCHRONOUS BACKGROUND WORKER CONTAINER                                           |
|                                                                                                                                   |
|  [ Async Jobs ]                                              [ Distributed Cron Sweeps ]                                          |
|  * process_meeting_transcription (Whisper + Pyannote Diarize)|  * 07:00 UTC: send_pre_interaction_briefs (Daily Morning RM Brief) |
|  * generate_meeting_embeddings (1024-dim BAAI/bge-m3 pgvect) |  * 08:00 UTC: send_client_followups (Overdue Commitment Sweep)     |
|  * AI Entity Extraction & Rolling Client Summary Synthesizer |  * Every 15m: retry_failed_notifications (Exp. Backoff Retry)      |
+-----------------------------------------------------------------------------------------------------------------------------------+
```

---

### End-to-End Component Flowchart

```mermaid
flowchart TD
    subgraph Clients["Client Presentation Tier"]
        UI["SPA Web Application\n(app/web/index.html)"]
        VoiceFAB["Philixa Brain Voice FAB\n(philixa-voice.js)"]
        Dictation["Fast Dictation\n(en-IN Web Speech)"]
        WhatsAppUser["RM on WhatsApp\n(Mobile Device)"]
    end

    subgraph Gateway["FastAPI Application Gateway (:8000)"]
        CSRF["CSRF Protection Middleware\n(X-CSRF-Token == Cookie)"]
        AuthContext["Auth Context Injection\n(CurrentPrincipal: Org, User, Role)"]
        APIRouters["48 Rest & WS Endpoints\n(/auth, /workspaces, /clients, /meetings, etc.)"]
    end

    subgraph AI_Engine["Hybrid Intelligence & RAG Core"]
        LangGraph["LangGraph StateGraph Router\n(Planner -> SQL/Semantic -> Synthesizer)"]
        FastPaths{"Deterministic\nFast-Path?"}
        Groq["Groq Cloud API\n(Llama 3.3 70B Versatile)"]
        Gemini["Google Gemini\n(2.5/3.6 Flash Fallback)"]
        Sarvam["Sarvam AI / Deepgram\n(Voice TTS & Real-Time STT)"]
        BGE["BAAI/bge-m3\n(1024-dim Embeddings)"]
    end

    subgraph Storage["Storage & Caching Tier"]
        PG[("PostgreSQL 15 + pgvector\n17 Multi-Tenant Tables")]
        Redis[("Redis 7\nJob Queues & WS Tickets")]
        MinIO[("MinIO S3 Storage\nTenant-Namespaced Audio")]
    end

    subgraph Worker["ARQ Asynchronous Background Worker"]
        TranscriptionJob["process_meeting_transcription\n(Faster-Whisper + Pyannote)"]
        EmbeddingJob["generate_meeting_embeddings\n(1024-dim pgvector chunks)"]
        CronMorning["07:00 UTC Cron\nPre-Interaction Briefs"]
        CronFollowup["08:00 UTC Cron\nOverdue Commitment Alerts"]
    end

    UI -->|HTTP + Cookies| CSRF
    VoiceFAB -->|POST /voice/chat & speak| CSRF
    Dictation -->|Populates Note Form| UI
    CSRF --> AuthContext --> APIRouters

    APIRouters -->|Copilot Query| FastPaths
    FastPaths -->|Yes: Direct Lookup| PG
    FastPaths -->|No: Agent Routing| LangGraph
    LangGraph --> Groq & Gemini & PG
    APIRouters -->|Audio Upload| MinIO
    APIRouters -->|Enqueue STT/Embeddings| Redis

    Redis --> Worker
    Worker --> MinIO & PG & BGE & Groq
    CronMorning & CronFollowup -->|Meta Graph v25.0| WhatsAppUser
```

---

### LangGraph Agentic Copilot Routing

```mermaid
stateDiagram-v2
    [*] --> InboundQuery: User sends natural language query
    InboundQuery --> FastPathCheck: Evaluate heuristics

    state FastPathCheck {
        [*] --> GreetingMatch
        GreetingMatch --> CalendarLookup: Not a greeting
        CalendarLookup --> ClientDirectLookup: Not calendar lookup
        ClientDirectLookup --> LLMPlanner: No fast-path match
    }

    GreetingMatch --> ReturnFastAnswer: Greeting detected
    CalendarLookup --> QueryCalendarSQL: Asia/Kolkata schedule query
    ClientDirectLookup --> QueryClientDirectSQL: "Who is [Client]?"
    QueryCalendarSQL --> ReturnFastAnswer
    QueryClientDirectSQL --> ReturnFastAnswer

    state LangGraph_StateGraph {
        LLMPlanner --> SQL_Route: Analytical / Aggregation Query
        LLMPlanner --> Semantic_Route: Unstructured Narrative Query
        
        SQL_Route --> GenerateSQL: Groq Llama 3.3 70B
        GenerateSQL --> InjectRBAC: Append 'AND user_id = :user_id' for members
        InjectRBAC --> ExecuteSafeSQL: Read-only SELECT execution
        ExecuteSafeSQL --> Synthesizer: Tabular DB Results
        
        Semantic_Route --> EmbedQuery: BAAI/bge-m3 1024-dim vector
        EmbedQuery --> CosineSearch: PostgreSQL pgvector '<=>'
        CosineSearch --> Synthesizer: Top-K Meeting Evidence Chunks
        
        Synthesizer --> SynthesizeResponse: Final grounded response generation
    }

    Synthesizer --> [*]: HTTP 200 JSON {answer, citations, sql}
    ReturnFastAnswer --> [*]: HTTP 200 JSON Fast-Path
```

---

## 🔬 Deep Dive: Core Subsystems

### 1. Multi-Tenant Workspace & Hardened Auth Core

Philixa 6.0 implements an enterprise-grade multi-tenancy model backed by a battle-tested security architecture.

```
                           +-----------------------------------------------+
                           |               USERS (Global Table)            |
                           |  id | email | password_hash | is_verified    |
                           +-----------------------------------------------+
                                                  |
                         +------------------------+------------------------+
                         |                                                 |
                         v                                                 v
    +-----------------------------------------+       +-----------------------------------------+
    |       ORGANIZATION_MEMBERSHIPS          |       |              USER_SESSIONS              |
    | org_id | user_id | role (owner/admin/m) |       | session_id | user_id | refresh_hash     |
    +-----------------------------------------+       +-----------------------------------------+
                         |
                         v
    +-------------------------------------------------------------------------------------------+
    |                           TENANT-SCOPED ENTITIES (TenantMixin)                            |
    | organizations | clients | meetings | commitments | meeting_evidence | follow_up_tasks     |
    +-------------------------------------------------------------------------------------------+
```

- **Tenancy Partitioning (`TenantMixin`)**: All domain models inherit `organization_id` and `user_id`. Queries are strictly partitioned at the repository layer (`ClientRepository`, `MeetingRepository`, `CommitmentRepository`).
- **Role-Based Access Control (RBAC)**:
  - `UserRole.OWNER` (`owner`): Full workspace administration, member role modification, workspace invite dispatch, billing, and team performance analytics.
  - `UserRole.ADMIN` (`admin`): Workspace member invitation, member removal, and team-wide CRM analytics.
  - `UserRole.MEMBER` (`member`): Access strictly isolated to personally assigned clients, meetings, and commitments.
- **Session & Cookie Security**:
  - Bcrypt password hashing (`cost >= 12`).
  - Dual JWT HS256 cookies: `access_token` (15-minute lifespan) and `refresh_token` (30-day lifespan).
  - Single-flight token rotation via `POST /auth/refresh` preventing concurrency race conditions.
  - Anti-replay defense: Refresh tokens are SHA-256 hashed and matched against `user_sessions.refresh_token_hash`.
- **Double-Submit CSRF Protection**: `CSRFProtectionMiddleware` (`app/core/csrf.py`) verifies the `X-CSRF-Token` HTTP header against the `csrf_token` cookie for all mutating HTTP methods (`POST`, `PUT`, `PATCH`, `DELETE`).
- **Single-Use WebSocket Tickets**: Prevents passing JWTs over WebSocket query strings. Clients mint a 60-second signed ticket (`POST /ws-ticket`). Upon connection to `WS /live/transcribe`, Redis key `philixa:ws_ticket_used:{jti}` is written with a 60-second TTL to guarantee single-use replay defense.
- **Demo Sandbox Mode**: Instant one-click workspace evaluation (`POST /auth/demo-login`) provisioning a pre-seeded workspace with realistic Indian wealth management clients, overdue commitments, and portfolio meetings.

---

### 2. Multi-Modal Meeting Ingestion & Voice Pipelines

Philixa 6.0 handles the full spectrum of meeting ingestion formats across asynchronous and real-time paths:

```
[ Ingestion Modes ] ──────────────► [ Processing Pipeline ] ──────────────► [ CRM Output ]
1. PASTED_NOTE (Raw Text)  ───────► Direct LLM Extraction  ──────────────► Structured Brief
2. AUDIO_UPLOAD (MinIO S3) ───────► ARQ Queue -> Whisper STT ───────────► Entities & Tasks
3. LIVE_BROWSER (16kHz PCM)──────► WebSocket -> Deepgram Nova-2 ────────► Live Transcript
4. Fast Dictation (Web Speech) ──► Client-Side Low-Latency en-IN ────────► Note Input Form
```

1. **Pasted Notes (`MeetingSourceType.PASTED_NOTE`)**: Direct text ingestion via `POST /api/v1/meeting-notes/process`. Directly triggers AI entity extraction, client resolution, commitment tracking, and risk signal detection.
2. **Audio Upload (`MeetingSourceType.AUDIO_UPLOAD`)**: Multipart audio upload (`.mp3`, `.m4a`, `.wav`) via `POST /audio/upload`. Streams the file to MinIO under tenant-isolated paths (`{org_id}/{user_id}/{meeting_id}/{filename}`) and enqueues the `process_meeting_transcription` ARQ background task.
3. **Live Diarized PCM Streaming (`MeetingSourceType.LIVE_BROWSER`)**: Captures browser microphone audio via an `AudioWorklet` (`pcm-processor.js`), streaming 16kHz Int16 raw PCM frames over `WS /live/transcribe` with ticket replay protection and real-time Deepgram STT transcription.
4. **Fast Browser Dictation (`en-IN`)**: Client-side speech-to-text using the browser's native Web Speech API (`fast-dictation.js`), tuned specifically for Indian English financial terminology.
5. **Human-in-the-Loop (HITL) Triage Modals**:
   - **Client Confirmation Modal (`#confirmPanel`)**: Surfaced when AI client identification confidence is low or ambiguous; allows the advisor to assign the meeting to an existing client or create a new one (`POST /api/v1/meeting-notes/{id}/confirm-client`).
   - **Transcript Review Modal (`#editTranscriptPanel`)**: Allows advisors to review, correct acoustic errors in audio transcripts, and trigger re-extraction (`PATCH /api/v1/meeting-notes/{id}/transcript`).
6. **Philixa Brain Conversational Voice Assistant**: Floating action button (FAB) assistant (`philixa-voice.js`) with 3000ms silence detection, conversational reasoning (`POST /api/v1/voice/chat`), and streaming TTS via Sarvam AI (`bulbul:v3`) or Deepgram Aura (`POST /api/v1/voice/speak`).

---

### 3. Stateful Agentic Copilot & Vector RAG Pipeline

The Copilot subsystem (`app/services/portfolio_copilot_service.py`) combines deterministic fast-paths with a compiled LangGraph state machine:

```
                                  [ User Query ]
                                         |
                                         v
                         +-------------------------------+
                         |   Deterministic Fast-Paths    |
                         | - Greetings                   |
                         | - Asia/Kolkata Calendar Check |
                         | - Direct Client Lookups       |
                         +-------------------------------+
                                         | (If no match)
                                         v
                         +-------------------------------+
                         |   LangGraph: planner_node     |
                         +-------------------------------+
                                  /             \
                                 /               \
                                v                 v
               +----------------------+     +----------------------+
               |  sql_generator_node  |     |    semantic_node     |
               | - Read-Only SELECT   |     | - BAAI/bge-m3 Embed  |
               | - Auto RBAC Injection|     | - pgvector Cosine    |
               +----------------------+     +----------------------+
                                 \               /
                                  \             /
                                   v           v
                         +-------------------------------+
                         |       synthesizer_node        |
                         | Grounded Answer with Evidence |
                         +-------------------------------+
```

- **Deterministic Fast-Paths**:
  - `_is_greeting(query)`: Immediate conversational greeting without LLM latency.
  - `_meeting_schedule_date(query)`: Calculates weekday calendar schedules in `Asia/Kolkata` timezone (e.g., "milna", "Monday meetings").
  - `_extract_client_lookup_name(query)`: Direct SQL profile retrieval for queries like "Who is Vikram Malhotra?" or "Vikram kaun hai".
- **Safe Read-Only NL-to-SQL**: Generates PostgreSQL queries with system prompt guardrails preventing mutating operations. For `member` roles, automatically appends tenant RBAC constraints (`AND user_id = :user_id`).
- **Semantic Evidence Retrieval (`pgvector`)**:
  - Transcripts are chunked and embedded into 1024-dimensional vectors using `BAAI/bge-m3`.
  - Stored in the `meeting_evidence` table with Cosine Distance indexing (`<=>`).
- **Multi-Tier AI Routing**:
  - Primary Extraction: Groq Cloud (`llama-3.3-70b-versatile`).
  - Review / Fallback: Google Gemini (`gemini-2.5-flash` / `gemini-3.6-flash`).
  - Copilot Reasoning: LiteLLM threaded execution preventing event loop starvation.

---

### 4. Distributed ARQ Worker & Scheduled Sweeps

Background execution is handled by an asynchronous ARQ worker container (`app/worker.py`) sharing Redis connection pools and database sessions:

- **Registered Asynchronous Tasks**:
  - `process_meeting_transcription`: Downloads audio from MinIO, executes Whisper transcription with Hinglish banking terminology prompts, runs LLM entity extraction, updates rolling client narratives, and enqueues embedding generation.
  - `generate_meeting_embeddings`: Splits transcripts into semantic chunks, generates 1024-dim `BAAI/bge-m3` vectors, and persists them into `meeting_evidence`.
- **Registered Distributed Cron Jobs**:
  - `send_pre_interaction_briefs` (**07:00 UTC Daily**): Aggregates upcoming meetings for the day and sends executive briefings to RMs.
  - `send_client_followups` (**08:00 UTC Daily**): Identifies overdue commitments and pending client follow-up tasks and dispatches alerts.
  - `retry_failed_notifications` (**Every 15 Minutes**): Retries failed WhatsApp and email dispatches with exponential backoff.

---

### 5. Dual-Channel Notification Engine

Philixa 6.0 strictly separates transactional authentication messaging from operational CRM alerts:

```
[ Notification Intent ] ────────────────► [ Routing Adapter ] ──────────────► [ Delivery Target ]
Auth / Invite / Reset   ────────────────► aiosmtplib (SMTP)   ──────────────► User Email Inbox
Daily Briefs / Overdue  ────────────────► WhatsAppAdapter      ──────────────► Meta Graph API v25.0
```

1. **Isolated Transactional Email (`EmailAdapter` via `aiosmtplib`)**:
   - Exclusively handles user email verification, password reset links, and workspace member invitations.
   - Operates independently of the global notification channel preference.
2. **Meta WhatsApp Cloud API Adapter (`WhatsAppAdapter`)**:
   - Integrates with Meta Graph API `v25.0` (`https://graph.facebook.com/v25.0/{phone_number_id}/messages`).
   - Evaluates per-user quiet hours (`quiet_hours_start`, `quiet_hours_end`) and timezone settings.
   - Tracks delivery receipts (`SENT`, `DELIVERED`, `READ`, `FAILED`) in `notification_deliveries`.
   - Exposes webhook endpoints for Hub challenge verification (`GET`) and inbound delivery status processing (`POST`).

---

## 🖥 Interactive Developer & Management Portals

Once the Philixa infrastructure is running, the following portals are accessible:

| Service / Interface | URL | Default Credentials / Port | Description |
|---|---|---|---|
| **Single-Page Application (SPA)** | `http://localhost:8000/` | Interactive Web UI | Full CRM dashboard, Voice FAB, Ingestion Tabs, and HITL panels. |
| **Interactive Swagger API Docs** | `http://localhost:8000/docs` | Public / Open | OpenAPI interactive documentation for testing all 48 endpoints. |
| **ReDoc API Reference** | `http://localhost:8000/redoc` | Public / Open | Comprehensive, human-readable API specification and schemas. |
| **OpenAPI Schema JSON** | `http://localhost:8000/openapi.json` | Public / Open | Raw JSON schema for SDK generation and contract testing. |
| **MinIO Object Storage Console** | `http://localhost:9001` | `philixa_minio` / `philixa_secret` | Web interface to inspect audio buckets and tenant namespaces. |
| **System Health Check** | `http://localhost:8000/health` | Public | JSON status of PostgreSQL, Redis, and overall backend health. |

---

## 📖 Complete 48-Endpoint API Catalog

The backend exposes **48 distinct API operations** across 14 router modules (all accessible under `/api/v1` and dual-mounted for auth and workspaces):

### 2.1 Authentication & Session Management (`app/api/v1/routes_auth.py`)

| # | Method | Endpoint | Security / Auth | Description |
|---|:---:|---|---|---|
| 1 | `POST` | `/auth/register` | Public | Onboard new user, create primary organization, and send verification email. |
| 2 | `POST` | `/auth/verify-email` | Token Query | Verify user email with 24-hour SHA-256 token. |
| 3 | `POST` | `/auth/login` | Public | Verify credentials (bcrypt), create user session, and issue HttpOnly JWT cookies. |
| 4 | `POST` | `/auth/demo-login` | Public | Instant one-click sandbox workspace provisioning with pre-seeded CRM data. |
| 5 | `GET` | `/auth/me` | JWT Cookie / Bearer | Retrieve active user profile, memberships, active workspace context, and role. |
| 6 | `POST` | `/auth/refresh` | Cookie `refresh_token` | Single-flight token rotation; issues fresh access token and rotates refresh token hash. |
| 7 | `POST` | `/auth/logout` | JWT Cookie / Bearer | Revoke active user session in database and clear session cookies. |
| 8 | `POST` | `/auth/forgot-password` | Public | Send 1-hour password reset email link with secure token. |
| 9 | `POST` | `/auth/reset-password` | Token Query | Reset password using valid token. |
| 10 | `DELETE` | `/auth/me` | JWT Cookie / Bearer | Account deletion cascade (purges sessions, memberships, and owned records). |
| 11 | `POST` | `/ws-ticket` | JWT Cookie / Bearer | Mint a 60-second single-use signed ticket for WebSocket audio streaming. |

### 2.2 Multi-Tenant Workspace & Team Management (`app/api/v1/routes_workspace.py`)

| # | Method | Endpoint | Security / RBAC | Description |
|---|:---:|---|---|---|
| 12 | `GET` | `/workspaces` | Authenticated | List all organizations/workspaces the authenticated user belongs to. |
| 13 | `POST` | `/workspaces/switch` | Authenticated (Member) | Switch active workspace context and issue updated session cookies. |
| 14 | `POST` | `/workspaces/invite` | Owner / Admin | Send 7-day email invitation to onboard a new team member. |
| 15 | `POST` | `/workspaces/invite/accept` | Public / Token | Accept workspace invite token and set user password. |
| 16 | `GET` | `/workspaces/members` | Authenticated | List all members and roles in the active workspace. |
| 17 | `PATCH` | `/workspaces/members/{id}/role` | Owner Only | Update member role (`admin`, `member`). Last owner cannot be demoted. |
| 18 | `DELETE` | `/workspaces/members/{id}` | Owner / Admin | Remove user from active workspace. Last owner cannot be removed. |

### 2.3 Client Relationship & Memory Management (`app/api/v1/routes_clients.py`)

| # | Method | Endpoint | Security / RBAC | Description |
|---|:---:|---|---|---|
| 19 | `POST` | `/api/v1/clients` | Authenticated | Create a new tenant-scoped client profile. |
| 20 | `GET` | `/api/v1/clients` | Authenticated | List clients with pending commitment counts (supports `?scope=team` vs `?scope=me`). |
| 21 | `GET` | `/api/v1/clients/{id}` | Tenant-Scoped | Retrieve client profile, contact details, products owned, and rolling narrative. |
| 22 | `PUT` | `/api/v1/clients/{id}` | Tenant-Scoped | Update client metadata, products owned JSON, and relationship notes. |
| 23 | `DELETE` | `/api/v1/clients/{id}` | Tenant-Scoped | Cascade delete client and all dependent meetings, commitments, and vectors. |
| 24 | `GET` | `/api/v1/clients/{id}/memory` | Tenant-Scoped | Retrieve structured rolling brief, open commitments, and top historical concerns. |
| 25 | `POST` | `/api/v1/clients/{id}/ask` | Tenant-Scoped | Natural language Q&A over a specific client's history with meeting citations. |
| 26 | `GET` | `/api/v1/clients/{id}/meetings` | Tenant-Scoped | List chronological meeting records for a specific client. |

### 2.4 Meeting Intelligence & Human-in-the-Loop (`app/api/v1/routes_meeting_notes.py`)

| # | Method | Endpoint | Security / RBAC | Description |
|---|:---:|---|---|---|
| 27 | `POST` | `/api/v1/meeting-notes/process` | Authenticated | Ingest raw notes (`PASTED_NOTE`), run LLM extraction, match client, extract tasks. |
| 28 | `GET` | `/api/v1/meeting-notes/{id}` | Tenant-Scoped | Retrieve meeting summary, raw notes, discussion points, concerns, and status. |
| 29 | `POST` | `/api/v1/meeting-notes/{id}/confirm-client` | HITL Scoped | Manually assign an ambiguous meeting to an existing client or trigger auto-creation. |
| 30 | `PATCH` | `/api/v1/meeting-notes/{id}/transcript` | HITL Scoped | Correct noisy audio transcript and trigger re-extraction and vector generation. |

### 2.5 Commitment Tracking (`app/api/v1/routes_commitments.py`)

| # | Method | Endpoint | Security / RBAC | Description |
|---|:---:|---|---|---|
| 31 | `GET` | `/api/v1/commitments` | Authenticated | List commitments with filtering (`status`, `client_id`, `due_before`, `scope`). |
| 32 | `PATCH` | `/api/v1/commitments/{id}/status` | Tenant-Scoped | Toggle commitment status between `pending`, `completed`, and `cancelled`. |

### 2.6 Audio Storage & Live Streaming (`app/api/v1/routes_audio.py`, `routes_live.py`)

| # | Method | Endpoint | Security / RBAC | Description |
|---|:---:|---|---|---|
| 33 | `POST` | `/audio/upload` | Authenticated | Upload multipart audio to MinIO (`philixa-audio`), enqueue ARQ transcription. |
| 34 | `GET` | `/audio/{id}/url` | Tenant-Scoped | Generate temporary presigned MinIO S3 download URL (1-hour expiry). |
| 35 | `WS` | `/live/transcribe` | Single-Use Ticket | Real-time WebSocket PCM audio streaming with Redis ticket replay protection. |

### 2.7 Conversational Voice Assistant (`app/api/v1/routes_voice.py`)

| # | Method | Endpoint | Security / RBAC | Description |
|---|:---:|---|---|---|
| 36 | `POST` | `/api/v1/voice/speak` | Authenticated | Text-to-Speech audio streaming via Sarvam AI (`bulbul:v3`) or Deepgram Aura. |
| 37 | `POST` | `/api/v1/voice/chat` | Authenticated | Conversational voice agent reasoning with portfolio memory context. |

### 2.8 Dashboard Analytics & Agentic Copilot (`app/api/v1/routes_dashboard.py`)

| # | Method | Endpoint | Security / RBAC | Description |
|---|:---:|---|---|---|
| 38 | `GET` | `/api/v1/dashboard/priorities` | Authenticated | Daily actionable priorities: overdue commitments and client risk signals. |
| 39 | `GET` | `/api/v1/dashboard/metrics` | Authenticated | High-level summary metrics (total clients, meetings processed, open tasks). |
| 40 | `GET` | `/api/v1/dashboard/team-performance` | Owner / Admin | Per-advisor CRM workload, meeting velocity, and commitment resolution stats. |
| 41 | `POST` | `/api/v1/dashboard/copilot/ask` | Authenticated | Hybrid LangGraph natural language Copilot (NL-to-SQL + pgvector semantic search). |

### 2.9 Notification Preferences & WhatsApp Webhooks (`app/api/v1/routes_preferences.py`, `routes_webhooks.py`)

| # | Method | Endpoint | Security / RBAC | Description |
|---|:---:|---|---|---|
| 42 | `GET` | `/api/v1/preferences` | Authenticated | Retrieve user notification settings (WhatsApp number, quiet hours, timezone). |
| 43 | `PUT` | `/api/v1/preferences` | Authenticated | Update user notification preferences. |
| 44 | `GET` | `/api/v1/webhooks/whatsapp` | Hub Verify | Meta WhatsApp Cloud API webhook hub challenge verification (`hub.challenge`). |
| 45 | `POST` | `/api/v1/webhooks/whatsapp` | Meta Webhook | Inbound WhatsApp messages and real-time message delivery status processing. |

### 2.10 Background Jobs & System Health (`app/api/v1/routes_jobs.py`, `routes_health.py`, `app/main.py`)

| # | Method | Endpoint | Security / RBAC | Description |
|---|:---:|---|---|---|
| 46 | `GET` | `/api/v1/jobs/{job_id}` | Authenticated | Poll ARQ background transcription/embedding job progress and completion status. |
| 47 | `GET` | `/health` | Public | Comprehensive health check verifying PostgreSQL connection and Redis pool. |
| 48 | `GET` | `/` | Public | Serves static Single-Page Application (SPA) HTML shell (`app/web/index.html`). |

---

## 🗄 Database Entity Relationship & 17 Relational Models

The relational schema is managed by **16 sequential Alembic migrations** up to `h5c3d4e5f6g7_multi_tenant_auth_and_workspaces.py`. All 17 SQLAlchemy models map directly to physical PostgreSQL tables:

```
+-------------------------------------------------------------------------------------------------------------------------------+
|                                                17 PHYSICAL DATABASE TABLES & ROLES                                            |
+-------------------------------------------------------------------------------------------------------------------------------+
| #  | Table Name                 | Primary Key | Scoping Columns        | Foreign Key References & Architectural Purpose       |
+----+----------------------------+-------------+------------------------+------------------------------------------------------+
| 1  | organizations              | id (UUID)   | Root Tenant            | Multi-tenant workspaces with plans (free/pro) & types|
| 2  | organization_memberships   | id (UUID)   | org_id, user_id        | Maps users to workspaces with roles (owner/admin/mem)|
| 3  | users                      | id (UUID)   | Global Table           | User accounts, bcrypt password hash, verified flag   |
| 4  | user_sessions              | id (UUID)   | user_id, org_id        | Active sessions, refresh token SHA-256 hash, expiry  |
| 5  | email_verification_tokens  | id (UUID)   | user_id                | 24-hour verification token hashes                    |
| 6  | password_reset_tokens      | id (UUID)   | user_id                | 1-hour password reset token hashes                   |
| 7  | workspace_invites          | id (UUID)   | org_id, invited_by     | 7-day token-based team member invitation links       |
| 8  | clients                    | id (UUID)   | organization_id, user_id| Client CRM profiles, contact metadata, rolling brief |
| 9  | meetings                   | id (Int)    | organization_id, user_id| Meeting transcripts, audio S3 URLs, extraction state |
| 10 | meeting_evidence           | id (Int)    | meeting_id, org_id     | 1024-dim pgvector embeddings (BAAI/bge-m3) with <=>  |
| 11 | commitments                | id (Int)    | organization_id, user_id| Actionable tasks with due dates and status lifecycle |
| 12 | commitment_meeting_links   | id (Int)    | commitment_id, meet_id | Many-to-many join linking commitments to meetings    |
| 13 | follow_up_tasks            | id (Int)    | organization_id, user_id| Priority follow-up items surfaced on RM dashboard     |
| 14 | risk_signals               | id (Int)    | organization_id, user_id| Deal and client churn risk flags detected by AI      |
| 15 | notification_preferences   | id (Int)    | user_id                | Quiet hours, timezone, and preferred channel settings|
| 16 | notification_deliveries    | id (Int)    | user_id, org_id        | Idempotent delivery logs with Meta message IDs       |
| 17 | ai_extraction_logs         | id (Int)    | meeting_id             | Token counts, latencies, model fallbacks audit log   |
+-------------------------------------------------------------------------------------------------------------------------------+
```

---

## ⚙️ Master Configuration Matrix

Philixa 6.0 configures **47 parameters** via Pydantic `BaseSettings` (`app/core/config.py`), with the primary production variables defined in `.env.example`:

| Category | Environment Variable | Default / Example Value | Description |
|---|---|---|---|
| **App Core** | `PHILIXA_ENV` / `APP_ENV` | `development` | Runtime environment (`development` vs `production`). Enables strict CSRF. |
| | `PHILIXA_APP_NAME` | `PHILIXA 6.0 V1-MVP` | Human-readable application title. |
| | `PHILIXA_APP_VERSION` | `1.0.0` | Semantic version string. |
| | `PHILIXA_SKIP_STARTUP_CHECKS` | `0` | Set to `1` to bypass pre-flight DB connection checks in test environments. |
| **Database & Cache** | `PHILIXA_DATABASE_URL` | `postgresql+psycopg://postgres:dev_only_password@localhost:5432/philixa` | Async PostgreSQL connection string using `psycopg` driver. |
| | `PHILIXA_REDIS_URL` | `redis://localhost:6379/0` | Redis instance for ARQ background queues and WebSocket tickets. |
| **Auth & Security** | `PHILIXA_JWT_SECRET` | *(32+ char hex string)* | Cryptographic secret for signing HS256 JWT access and refresh tokens. |
| | `PHILIXA_CSRF_SECRET` | *(32+ char hex string)* | Cryptographic secret for generating double-submit CSRF tokens. |
| | `PHILIXA_JWT_ACCESS_TOKEN_EXPIRE_MINUTES` | `15` | Access token lifespan. |
| | `PHILIXA_JWT_REFRESH_TOKEN_EXPIRE_DAYS` | `30` | Refresh token lifespan. |
| | `PHILIXA_COOKIE_SECURE` | `False` (`True` in prod) | Flag requiring HTTPS for session cookies. |
| | `PHILIXA_ALLOWED_ORIGINS` | `http://localhost:8000` | Comma-separated CORS whitelist origins. |
| **AI LLM Inference** | `PHILIXA_GROQ_API_KEY` | `gsk_...` | High-speed LLM inference key for meeting extraction and Copilot. |
| | `PHILIXA_AI_MODEL` | `llama-3.3-70b-versatile` | Primary Groq LLM model identifier. |
| | `PHILIXA_GEMINI_API_KEY` | `AIzaSy...` | Google Gemini API key for Tier 2 extraction review fallback. |
| | `PHILIXA_AI_REVIEW_MODEL` | `gemini-2.5-flash` | Review LLM model identifier. |
| **Voice & Embeddings** | `PHILIXA_EMBEDDING_MODEL` | `BAAI/bge-m3` | SentenceTransformers model for 1024-dim `pgvector` embeddings. |
| | `PHILIXA_DEEPGRAM_API_KEY` | *(Secret Token)* | Real-time Deepgram Nova-2 speech-to-text API key. |
| | `PHILIXA_SARVAM_API_KEY` | *(Secret Token)* | Sarvam AI Hinglish voice synthesis API key (`bulbul:v3`). |
| | `PHILIXA_TRANSCRIPTION_MODE` | `local` | STT engine mode (`local` via faster-whisper vs `cloud`). |
| | `PHILIXA_HF_TOKEN` | `hf_...` | Hugging Face token required for Pyannote speaker diarization models. |
| **Object Storage** | `PHILIXA_MINIO_URL` | `localhost:9000` (`minio:9000` in Docker) | MinIO S3 API endpoint. |
| | `PHILIXA_MINIO_ACCESS_KEY` | `philixa_minio` | MinIO admin access username. |
| | `PHILIXA_MINIO_SECRET_KEY` | `philixa_secret` | MinIO admin secret password. |
| | `PHILIXA_MINIO_BUCKET_NAME` | `philixa-audio` | Default S3 bucket for meeting audio storage. |
| **Dual Notifications** | `PHILIXA_NOTIFICATION_MODE` | `email` (or `whatsapp`) | Default notification dispatch channel. |
| | `PHILIXA_SMTP_HOSTNAME` | `smtp.gmail.com` | SMTP host for transactional authentication emails. |
| | `PHILIXA_SMTP_PORT` | `587` | SMTP port (STARTTLS). |
| | `PHILIXA_SMTP_USERNAME` | `your_email@gmail.com` | SMTP username. |
| | `PHILIXA_SMTP_PASSWORD` | `your_app_password` | SMTP app password. |
| | `WHATSAPP_PHONE_NUMBER_ID` | `...` | Meta WhatsApp Cloud API Phone Number ID. |
| | `WHATSAPP_ACCESS_TOKEN` | `EAAG...` | Meta Graph API System User permanent access token. |
| | `WHATSAPP_VERIFY_TOKEN` | `...` | Webhook verification token string for Meta challenge handshake. |

---

## 🚀 Quickstart & Deployment Guide

### Option A: 5-Container Docker Compose (Recommended)

The easiest way to run the entire Philixa 6.0 stack—including database, caching, object storage, API gateway, and background worker—is via Docker Compose.

```bash
# 1. Clone the repository
git clone https://github.com/shouryasingh-codes/philixa-6.0.git
cd philixa-6.0

# 2. Configure environment variables
cp .env.example .env
# Edit .env and supply your PHILIXA_GROQ_API_KEY and other credentials

# 3. Boot all 5 services (db, redis, minio, app, worker)
docker compose up -d --build

# 4. View container logs
docker compose logs -f
```

The 5 booted services:
1. `db`: PostgreSQL 15 with `pgvector` extension on port `5432`.
2. `redis`: Redis 7 Alpine cache and task broker on port `6379`.
3. `minio`: MinIO S3 Object Storage on ports `9000` (API) and `9001` (Console).
4. `app`: FastAPI web application on port `8000` (runs migrations on boot).
5. `worker`: ARQ background worker executing transcription, embeddings, and cron sweeps.

---

### Option B: Bare-Metal Virtualenv Setup

For local backend development, run the services on bare metal:

#### Prerequisites
- **Python 3.12+**
- **FFmpeg** installed and in system `PATH` (required for audio slicing and Whisper)
- **PostgreSQL 15+** with `pgvector` extension
- **Redis 7+** running locally on port `6379`
- **MinIO** running on port `9000`

```bash
# 1. Create and activate Python 3.12 virtual environment
python -m venv .venv

# On Linux / macOS:
source .venv/bin/activate
# On Windows (PowerShell):
.venv\Scripts\Activate.ps1

# 2. Install dependencies (including authentication crypto libraries)
pip install -r requirements.txt
pip install python-jose[cryptography] passlib[bcrypt] itsdangerous bcrypt

# 3. Configure environment
cp .env.example .env
# Ensure PHILIXA_DATABASE_URL and PHILIXA_REDIS_URL match your local setup

# 4. Apply database migrations
alembic upgrade head

# 5. Start the FastAPI Web Server (Terminal 1)
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# 6. Start the ARQ Background Worker (Terminal 2)
arq app.worker.WorkerSettings
```

---

### One-Click Demo Sandbox Evaluation

To immediately explore the CRM platform without manually registering and verifying emails:

1. Open `http://localhost:8000` in your web browser.
2. Click **"Try Demo Workspace"** on the login overlay.
3. The platform will instantly execute `POST /auth/demo-login`, provisioning a sandboxed organization populated with sample Indian wealth management clients, overdue commitments, and meeting notes!

---

## 💻 Verified cURL Workflows

### 1. One-Click Sandbox Demo Login & Session Capture

```bash
# Provision a demo sandbox workspace and save session cookies
curl -X POST "http://localhost:8000/auth/demo-login" \
     -H "Content-Type: application/json" \
     -c cookies.txt
```

### 2. Standard User Registration & Login

```bash
# 1. Register a new user account and organization
curl -X POST "http://localhost:8000/auth/register" \
     -H "Content-Type: application/json" \
     -d '{
       "email": "advisor@apexwealth.com",
       "password": "SecurePassword123!",
       "workspace_name": "Apex Wealth Advisory",
       "workspace_type": "company"
     }'

# 2. Login, verify credentials, and capture HttpOnly JWT cookies
curl -X POST "http://localhost:8000/auth/login" \
     -H "Content-Type: application/json" \
     -c cookies.txt \
     -d '{
       "email": "advisor@apexwealth.com",
       "password": "SecurePassword123!"
     }'
```

### 3. Querying the Agentic Copilot (Verified Fixed Schema)

> ⚠️ **Schema Requirement**: The Copilot endpoint expects `"query"` (using `"question"` results in an HTTP 422 error). In production, provide the `X-CSRF-Token` from your session cookie.

```bash
# Query the Copilot using captured cookies and CSRF token
curl -X POST "http://localhost:8000/api/v1/dashboard/copilot/ask" \
     -b cookies.txt \
     -H "Content-Type: application/json" \
     -H "X-CSRF-Token: <csrf_token_from_cookie>" \
     -d '{
       "query": "Show me all clients with pending follow-ups due this week",
       "chat_history": []
     }'
```

### 4. Minting Single-Use WebSocket Ticket for Live Streaming

```bash
curl -X POST "http://localhost:8000/ws-ticket" \
     -b cookies.txt \
     -H "Content-Type: application/json" \
     -H "X-CSRF-Token: <csrf_token_from_cookie>"
```

*Response*:
```json
{
  "ticket": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "expires_in": 60
}
```
*Connect to Live Audio WebSocket*: `ws://localhost:8000/live/transcribe?ticket=<ticket>`

### 5. Ingesting Meeting Notes & Resolving Clients (HITL)

```bash
# Ingest raw meeting text
curl -X POST "http://localhost:8000/api/v1/meeting-notes/process" \
     -b cookies.txt \
     -H "Content-Type: application/json" \
     -H "X-CSRF-Token: <csrf_token_from_cookie>" \
     -d '{
       "raw_notes": "Met with Vikram Malhotra at Starbucks. Discussed diversifying 2 Cr portfolio into debt funds. Action: Send debt mutual fund comparison by Friday.",
       "meeting_date": "2026-08-26T10:00:00Z"
     }'
```

---

## 🧪 Testing & Quality Assurance

Philixa 6.0 includes comprehensive automated test suites covering authentication, multi-tenancy, LangGraph routing, repository scoping, and API endpoints.

```bash
# Run full test suite
pytest

# Run tests with verbose output and coverage
pytest -v --tb=short

# Run specific domain test modules
pytest tests/test_auth.py
pytest tests/test_copilot.py
pytest tests/test_multitenant_routing.py
```

---

## 🗺️ Roadmap & Engineering Milestones

- [x] **Multi-Tenant Workspace & Role-Based Access Control (RBAC)** (`owner`, `admin`, `member`)
- [x] **Hardened Web Security Core** (HttpOnly JWT cookies, single-flight refresh rotation, double-submit CSRF)
- [x] **Single-Use WebSocket Tickets with Redis Replay Defense**
- [x] **Multi-Modal Ingestion Pipelines** (Pasted Notes, MinIO S3 Multipart Upload, Live PCM Streaming, Fast Dictation)
- [x] **Human-in-the-Loop (HITL) Triage Panels** (Ambiguous client confirmation and transcript correction)
- [x] **LangGraph Agentic Copilot with PostgreSQL pgvector RAG** (`BAAI/bge-m3` 1024-dim embeddings)
- [x] **Distributed ARQ Background Worker** (Offline Whisper STT, Pyannote diarization, embedding generation)
- [x] **Scheduled Cron Automation** (07:00 UTC morning RM briefings and 08:00 UTC overdue commitment sweeps)
- [x] **Dual-Channel Notification Engine** (Isolated SMTP email + Meta WhatsApp Cloud API v25.0)
- [x] **One-Click Sandbox Demo Login for Rapid Evaluation**
- [ ] **React / Next.js Enterprise Frontend Migration**
- [ ] **Stripe Subscription Billing & Metered Usage Webhooks**
- [ ] **Multi-Region Kubernetes (EKS) Helm Chart Deployment**

---

## 🤝 Contributing & License

Contributions are what make the open source community such an empowering environment to build, iterate, and innovate. Any contributions you make are **greatly appreciated**.

1. Fork the Project (`git clone https://github.com/shouryasingh-codes/philixa-6.0.git`)
2. Create your Feature Branch (`git checkout -b feature/EnterpriseFeature`)
3. Commit your Changes (`git commit -m 'feat: Add enterprise capability'`)
4. Push to the Branch (`git push origin feature/EnterpriseFeature`)
5. Open a Pull Request

### License
Distributed under the **MIT License**. See `LICENSE` for details.

### Contact & Links
- **Repository**: [https://github.com/shouryasingh-codes/philixa-6.0](https://github.com/shouryasingh-codes/philixa-6.0)
- **Interactive Documentation**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Author**: Shourya Singh & Philixa Core Engineering Team
