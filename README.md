<div align="center">

# 🚀 PHILIXA 6.0
### The Agentic AI-First CRM for Modern Relationship Managers & Wealth Advisors

[![FastAPI](https://img.shields.io/badge/Backend-FastAPI_0.137-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL_16_+_pgvector-316192?style=for-the-badge&logo=postgresql)](https://github.com/pgvector/pgvector)
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
  - [1. Multi-Tenant Workspace, Hardened Auth & Gateway Security](#1-multi-tenant-workspace-hardened-auth--gateway-security)
  - [2. Multi-Modal Ingestion & Audio DSP Pipeline](#2-multi-modal-ingestion--audio-dsp-pipeline)
  - [3. Stateful Agentic Copilot, Vector RAG & Action Engine](#3-stateful-agentic-copilot-vector-rag--action-engine)
  - [4. Conversational Voice Assistant & Intent Engine](#4-conversational-voice-assistant--intent-engine)
  - [5. Automated Rules Engine, Risk Scoring & CRM Intelligence](#5-automated-rules-engine-risk-scoring--crm-intelligence)
  - [6. Distributed ARQ Worker & Scheduled Sweeps](#6-distributed-arq-worker--scheduled-sweeps)
  - [7. Dual-Channel Notification Engine](#7-dual-channel-notification-engine)
- [Frontend Single-Page Application (SPA) Architecture](#-frontend-single-page-application-spa-architecture)
  - [1. 6-View Fullscreen Auth Modal & State Machine](#1-6-view-fullscreen-auth-modal--state-machine)
  - [2. Google Identity Services (GSI) One-Tap SSO Integration](#2-google-identity-services-gsi-one-tap-sso-integration)
  - [3. Multi-Tenant Workspace Context Switcher & Plan Badge](#3-multi-tenant-workspace-context-switcher--plan-badge)
  - [4. Workspace Team Member Management & Dynamic RBAC Modal](#4-workspace-team-member-management--dynamic-rbac-modal)
  - [5. User Profile Avatar Dropdown, Initials Badges & Account Deletion](#5-user-profile-avatar-dropdown-initials-badges--account-deletion)
  - [6. Responsive App Shell, Collapsible 72px Icon-Rail & Mobile Drawer](#6-responsive-app-shell-collapsible-72px-icon-rail--mobile-drawer)
  - [7. Dark / Light Theme System with WCAG AAA Contrast Tokens](#7-dark--light-theme-system-with-wcag-aaa-contrast-tokens)
  - [8. Homogeneous 4-Card Verdict Strip Metrics with Jump Navigation](#8-homogeneous-4-card-verdict-strip-metrics-with-jump-navigation)
  - [9. Tablet / Mobile Responsive Segmented Tab Switcher (< 1024px)](#9-tablet--mobile-responsive-segmented-tab-switcher--1024px)
  - [10. 4-Tab Smart Intake Editor](#10-4-tab-smart-intake-editor)
  - [11. Structured Diff Review Workbench (60/40 Split Master-Detail)](#11-structured-diff-review-workbench-6040-split-master-detail)
  - [12. Global Client Filter Omnibar & Cascade Delete Action](#12-global-client-filter-omnibar--cascade-delete-action)
  - [13. Client Memory Dossier Accordion & Pre-Meeting Brief Card](#13-client-memory-dossier-accordion--pre-meeting-brief-card)
  - [14. In-Dossier Client Q&A with Speech Recognition Voice Input](#14-in-dossier-client-qa-with-speech-recognition-voice-input)
  - [15. Interactive Commitment Ledger Table & Optimistic Status Toggling](#15-interactive-commitment-ledger-table--optimistic-status-toggling)
  - [16. Daily Priorities List & Dynamic False-Alarm Safe Risk Monitor](#16-daily-priorities-list--dynamic-false-alarm-safe-risk-monitor)
  - [17. Team Performance Overview Dashboard Table](#17-team-performance-overview-dashboard-table)
  - [18. Workspace Scope Toggle (Team Workspace vs My Workspace)](#18-workspace-scope-toggle-team-workspace-vs-my-workspace)
  - [19. Persistent 380px AI Copilot Sidecar with Live Token Budget Meter](#19-persistent-380px-ai-copilot-sidecar-with-live-token-budget-meter)
  - [20. Philixa Brain Voice Assistant 4-State Visual State Machine](#20-philixa-brain-voice-assistant-4-state-visual-state-machine)
  - [21. Notification Preferences Modal & Quiet Hours Configuration](#21-notification-preferences-modal--quiet-hours-configuration)
  - [22. Client-Side Single-Flight Refresh Queue & Double-Submit CSRF Guard](#22-client-side-single-flight-refresh-queue--double-submit-csrf-guard)
  - [23. Toast Notification System](#23-toast-notification-system)
  - [24. Comprehensive Keyboard Shortcuts & WCAG 2.2 AAA Accessibility](#24-comprehensive-keyboard-shortcuts--wcag-22-aaa-accessibility)
- [Interactive Developer & Management Portals](#-interactive-developer--management-portals)
- [Complete 49-Endpoint API Catalog](#-complete-49-endpoint-api-catalog)
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
- 🛡️ **Enterprise Multi-Tenancy & Hardened Session Security**: Strict tenant isolation across all entities via `TenantMixin`, Bcrypt password hashing (`cost >= 12`), Google OAuth 2.0 (`POST /auth/google`) with automatic workspace provisioning, HttpOnly + SameSite=Lax JWT cookie pairs, single-flight 401 refresh token rotation, double-submit CSRF protection (`X-CSRF-Token`), 10MB payload limiters (`enforce_payload_size_limit`), production security validation (`validate_production_settings`), and single-use Redis-backed WebSocket ticket replay defense.
- 🎙️ **Multi-Modal Meeting Capture & Audio DSP**: Four specialized ingestion pipelines supporting direct raw text (`MeetingSourceType.PASTED_NOTE`), MinIO S3 multipart audio uploads (`AUDIO_UPLOAD`), live 16kHz Int16 PCM WebSocket streaming (`LIVE_BROWSER`), and zero-latency browser dictation in Indian English (`en-IN`). Powered by FFmpeg audio filter chains, dynamic Whisper client-name prompt injection, Solo/Meeting PyAnnote 3.1 diarization, ASR Hinglish translation normalization (`translate_transcript`), and automated MinIO storage purging (`PHILIXA_RETAIN_AUDIO`).
- 🧠 **Hybrid LangGraph State Machine, Vector RAG & Action Engine**: A stateful LangGraph execution graph orchestrating natural language-to-SQL generation with automatic multi-tenant RBAC injection, deterministic fast-path routing, heuristic sentiment/concern interceptors (`_requires_evidence_search`), hybrid cosine similarity search over 1024-dimensional `BAAI/bge-m3` vectors in PostgreSQL `pgvector`, and an automated `action_node` triggering multi-channel email/WhatsApp reminders via `ReminderService`.
- 🗣️ **Conversational Voice Assistant with 4-Intent Routing**: Philixa Brain voice assistant featuring 4-way intent classification (`QUERY`, `SAVE_MEETING`, `SEND_REMINDER`, `GENERAL_CHAT`), asynchronous background meeting ingestion via FastAPI `BackgroundTasks`, Hindi name phonetic translation, and streaming TTS via Sarvam AI and Deepgram Aura.
- ⚡ **Asynchronous Background Processing & Distributed Cron**: Powered by ARQ (`asyncio` + Redis) workers handling offline Whisper transcription with specialized Indian banking prompts, Pyannote diarization, vector embedding generation, automated business rules synchronization (`RulesEngineService`), real-time meeting completion alerts, and 4 distributed cron sweeps (07:00 UTC morning RM briefings, 08:00 UTC overdue commitment sweeps, every 15m notification retries, and hourly demo sandbox account purging).
- 🖥️ **Full-Featured Modern Frontend SPA**: 60/40 Split Structured Diff Review Workbench, 380px Persistent Copilot Sidecar Dock with live token meter, 4-state visual voice assistant, Google One-Tap SSO UI, 4-card verdict strip, dark/light theme engine with WCAG 2.2 AAA tokens, and client-side single-flight refresh queue.
- 📱 **Dual-Channel Notification Architecture**: Strict architectural decoupling between isolated transactional SMTP email (`aiosmtplib`) for authentication workflows and Meta WhatsApp Cloud API v25.0 for proactive RM alerts with quiet-hours enforcement and delivery receipt tracking.

---

## 💡 Why Philixa 6.0?

| Capability / Architectural Dimension | Traditional Legacy CRMs (Salesforce / HubSpot) | Generic AI Wrapper CRMs | **Philixa 6.0 Enterprise Platform** |
|---|---|---|---|
| **Data Ingestion Paradigm** | Manual forms, rigid dropdowns, tedious manual data entry | Single text box with generic prompt wrapper | **4 Ingestion Modes**: Text Paste, MinIO Audio Drag-and-Drop, Live PCM Streaming (Solo/Meeting), and Fast Web Speech Dictation |
| **Meeting Intelligence & Audio DSP** | None (Requires third-party recorder extensions) | Basic OpenAI call with generic unstructured summary | **Hinglish-Tuned Multi-Stage AI Pipeline**: FFmpeg DSP, dynamic client-name Whisper prompt injection, ASR Hinglish translation normalization, PyAnnote 3.1 diarization, Groq Llama 3.3 70B extraction, and Gemini fallback |
| **Human-in-the-Loop (HITL) Triage** | Manual duplicate merging | Full blind AI auto-creation (causes data pollution) | **60/40 Structured Diff Review Workbench**: Category filter pills, interactive diff cards, inline editing, source quote attribution, micro-dismissal, batch sync (`Cmd+Shift+Enter`), client confirmation (`#confirmPanel`), and transcript correction (`#editTranscriptPanel`) |
| **Portfolio Querying & Copilot** | Complex SQL/SOQL or static reports | Vector-only semantic search or ungrounded SQL | **Hybrid LangGraph StateGraph**: Deterministic fast-paths, heuristic evidence interceptor (`_requires_evidence_search`), safe read-only SQL with auto RBAC filters, pgvector cosine search, and `action_node` reminder dispatch |
| **Voice & Action Capabilities** | None / Add-on plugins | Passive chatbot replies | **4-Intent Conversational Voice Assistant**: `QUERY`, `SAVE_MEETING` (async background save), `SEND_REMINDER` (`ReminderService`), `GENERAL_CHAT`, with streaming TTS and 4-state visual UI |
| **Tenant & Data Isolation** | Organization-level tables with high licensing cost | Single-tenant or software-level user filtering | **Strict Multi-Tenant Model**: Composite memberships (`owner`, `admin`, `member`), repository-level scoping, Google OAuth2 SSO, decoupled products (`products_owned_json` vs `products_interested_json`), and cascade deletion |
| **Session Security & Defense** | Standard session cookies | Insecure Bearer tokens in `localStorage` | **Hardened Security**: HttpOnly JWT cookies, single-flight refresh rotation (`fetchWithAuth`), double-submit CSRF, 10MB payload limiter, production settings validator, and single-use signed WS tickets |
| **Background Queue & Automation** | Expensive Enterprise schedulers | Synchronous request blocking or toy threading | **Distributed ARQ + Redis Workers**: Async STT queues, event-driven meeting completion alerts, and 4 automated cron sweeps (07:00 UTC morning brief, 08:00 UTC overdue follow-up, 15m retry, hourly demo purge) |
| **Proactive RM Notification** | Generic email digests | In-app notification popups only | **Meta WhatsApp Cloud API v25.0** + isolated SMTP with timezone-aware quiet hours, multi-channel `ReminderService`, and delivery tracking |

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
|  [ Gateway Security & Middlewares ]                                                                                               |
|  * 10MB Global Request Payload Limiter (enforce_payload_size_limit -> HTTP 413)                                                   |
|  * Production Settings Security Validator (validate_production_settings: JWT entropy, CORS rules, SMTP, Cookie HTTPS)             |
|  * CSRFProtectionMiddleware (Double-Submit X-CSRF-Token Verification against csrf_token cookie)                                    |
|  * CORS Policy & Security Headers                                                                                                 |
|                                                                                                                                   |
|  [ Security & Multi-Tenant Context ]                                                                                              |
|  * Bcrypt Hashing (Cost 12)  * Google OAuth2 One-Tap Sign-In (/auth/google)  * HttpOnly JWT Cookies (Access 15m / Refresh 30d)     |
|  * WS Single-Use Tickets (60s TTL + Replay Guard)  * Demo Sandbox Quotas (2-Meeting Limit, 1d Expiry)                                 |
|  * CurrentPrincipal Injection: User ID, Active Organization ID, Canonical Role (owner | admin | member)                            |
|                                                                                                                                   |
|  [ API Router Subsystems (49 Distinct Operations, Dual-Mounted at / and /api/v1/) ]                                                |
|  * /auth (12 ops)   * /workspaces (7 ops)  * /api/v1/clients (8 ops)      * /api/v1/meeting-notes (4 ops) * /api/v1/commitments (2 ops)|
|  * /audio (2 ops)   * /live/transcribe     * /api/v1/voice (2 ops)        * /api/v1/dashboard (4 ops)    * /api/v1/preferences (2 ops)|
|  * /api/v1/webhooks/whatsapp (2 ops)       * /api/v1/jobs (1 op)          * /health (1 op)               * / (1 op static SPA)        |
|                                                                                                                                   |
|  [ Hybrid LangGraph Agentic Copilot & Voice Engine ]                                                                             |
|  * Deterministic Fast-Paths: Greeting / Asia/Kolkata Meeting Calendar / Client Direct Profile Lookup                              |
|  * Heuristic Interceptor (_requires_evidence_search): Forces vector route for sentiment/discount/complaint queries                 |
|  * StateGraph: planner_node --> (sql_generator_node | semantic_node [pgvector] | action_node [ReminderService]) --> synthesizer_node|
|  * VoiceAssistantService: 4-Intent Routing (QUERY, SAVE_MEETING [BackgroundTasks], SEND_REMINDER, GENERAL_CHAT)                   |
|  * ASR Hinglish Translation & Normalization Layer (Phonetic error correction & Indian name preservation)                         |
+-----------------------------------------------------------------------------------------------------------------------------------+
           |                                     |                                         |
           v                                     v                                         v
+-----------------------+             +-----------------------+                 +-----------------------+
|  POSTGRESQL + PGVECTOR|             |     REDIS 7 CACHE     |                 |  MINIO S3 OBJECT STR  |
|      (Port :5432)     |             |      (Port :6379)     |                 |  (API :9000 | UI :9001)|
+-----------------------+             +-----------------------+                 +-----------------------+
| * 17 Relational Tables|             | * ARQ Job Queues      |                 | * Bucket: philixa-audio|
| * Multi-Tenant Scoping|             | * WS Replay Guard Keys|                 | * Tenant Namespaces:  |
| * Decoupled Products  |             | * User Session State  |                 |   {org}/{user}/{meet} |
|   (owned vs interested)|            | * Single-Flight Queue |                 | * Auto-Purge Lifecycle|
| * 1024-dim BAAI/bge-m3|             |                       |                 |   (PHILIXA_RETAIN_    |
|   Cosine Index (<=>)  |             |                       |                 |    AUDIO=0)           |
+-----------------------+             +-----------------------+                 +-----------------------+
           ^                                     ^                                         ^
           |                                     |                                         |
           +-------------------------------------+-----------------------------------------+
                                                 |
                                                 v
+-----------------------------------------------------------------------------------------------------------------------------------+
|                                            ARQ ASYNCHRONOUS BACKGROUND WORKER CONTAINER                                           |
|                                                                                                                                   |
|  [ Async Jobs ]                                              [ Distributed Cron Sweeps (4 Total) ]                                |
|  * process_meeting_transcription (DSP + Whisper + Pyannote) |  * 07:00 UTC: send_pre_interaction_briefs (Daily Morning RM Brief) |
|  * generate_meeting_embeddings (1024-dim BAAI/bge-m3 pgvect) |  * 08:00 UTC: send_client_followups (Overdue Commitment Sweep)     |
|  * RulesEngineService (Auto Task & Risk Signal Scoring)      |  * Every 15m: retry_failed_notifications (Exp. Backoff Retry)      |
|  * _notify_meeting_processed (Instant Post-Meeting Alert)    |  * Hourly (Min 0): cleanup_demo_accounts (Demo Sandbox Purge)      |
+-----------------------------------------------------------------------------------------------------------------------------------+
```

---

### End-to-End Component Flowchart

```mermaid
flowchart TD
    subgraph Clients["Client Presentation Tier (SPA & Omnichannel)"]
        UI["SPA Web Application\n(app/web/index.html & app.js)"]
        DiffWorkbench["60/40 Diff Review Workbench\n(Interactive Staging & Inline Edit)"]
        CopilotSidecar["380px Copilot Sidecar Dock\n(Token Meter & Evidence Badges)"]
        VoiceFAB["Philixa Brain Voice Assistant\n(4-State Visual Machine: philixa-voice.js)"]
        Dictation["Fast Dictation\n(en-IN Web Speech API)"]
        GoogleSSO["Google One-Tap SSO\n(Google Identity Services SDK)"]
        WhatsAppUser["RM on WhatsApp\n(Meta Graph API v25.0 Mobile)"]
    end

    subgraph Gateway["FastAPI Application Gateway (:8000)"]
        PayloadLimiter["10MB Payload Size Limiter\n(enforce_payload_size_limit)"]
        CSRF["CSRF Protection Middleware\n(Double-Submit X-CSRF-Token Verification)"]
        AuthContext["Auth Context & RBAC Injection\n(CurrentPrincipal: Org, User, Role)"]
        APIRouters["49 Rest & WS Endpoints\n(Dual-Mounted / and /api/v1/)"]
    end

    subgraph AI_Engine["Hybrid Intelligence, Voice & RAG Core"]
        LangGraph["LangGraph StateGraph Router\n(Planner -> SQL / Semantic / Action -> Synthesizer)"]
        EvidenceInterceptor{"_requires_evidence_search\nHeuristic Interceptor?"}
        FastPaths{"Deterministic\nFast-Path?"}
        ReminderEngine["ReminderService Engine\n(Multi-Channel Email & WhatsApp Dispatch)"]
        VoiceRouter["VoiceAssistantService (4 Intents)\n(QUERY, SAVE_MEETING, SEND_REMINDER, CHAT)"]
        HinglishLayer["ASR Hinglish Translation & Normalization\n(Phonetic Fixes & Indian Entity Preservation)"]
        Groq["Groq Cloud API\n(Llama 3.3 70B Versatile)"]
        Gemini["Google Gemini\n(2.5/3.6 Flash Fallback)"]
        Sarvam["Sarvam AI / Deepgram\n(Voice TTS & Real-Time STT)"]
        BGE["BAAI/bge-m3\n(1024-dim Dense Embeddings)"]
    end

    subgraph Storage["Storage & Caching Tier"]
        PG[("PostgreSQL 15/16 + pgvector\n17 Multi-Tenant Tables & Decoupled Products")]
        Redis[("Redis 7 Cache & Broker\nARQ Queues & WS Replay Guard")]
        MinIO[("MinIO S3 Storage\nTenant Audio & Auto-Purging")]
    end

    subgraph Worker["ARQ Asynchronous Background Worker"]
        TranscriptionJob["process_meeting_transcription\n(FFmpeg DSP + Whisper + Pyannote 3.1)"]
        EmbeddingJob["generate_meeting_embeddings\n(1024-dim pgvector chunks)"]
        RulesEngine["RulesEngineService\n(Dynamic Task & Risk Scoring)"]
        CronMorning["07:00 UTC Cron\nPre-Interaction Briefs"]
        CronFollowup["08:00 UTC Cron\nOverdue Commitment Alerts"]
        CronRetry["Every 15m Cron\nNotification Retry Backoff"]
        CronDemoPurge["Hourly (Min 0) Cron\nDemo Account Cascade Purge"]
        RealtimeNotify["_notify_meeting_processed\nEvent-Driven Meeting Alerts"]
    end

    UI -->|HTTP + Cookies| PayloadLimiter
    GoogleSSO -->|id_token| PayloadLimiter
    VoiceFAB -->|POST /voice/chat & speak| PayloadLimiter
    Dictation -->|Populates Smart Intake| UI
    UI --> DiffWorkbench
    UI --> CopilotSidecar
    PayloadLimiter --> CSRF --> AuthContext --> APIRouters

    APIRouters -->|Copilot Query| EvidenceInterceptor
    EvidenceInterceptor -->|Sentiment/Discount/Concern| LangGraph
    EvidenceInterceptor -->|Standard Query| FastPaths
    FastPaths -->|Yes: Direct Lookup| PG
    FastPaths -->|No: Agent Routing| LangGraph
    LangGraph -->|Action Route| ReminderEngine
    ReminderEngine -->|Concurrent Dispatch| Worker
    APIRouters -->|Voice Chat / Dictate| VoiceRouter
    VoiceRouter -->|SAVE_MEETING| BackgroundSave["FastAPI BackgroundTasks\nMeetingProcessingService"]
    BackgroundSave --> PG
    VoiceRouter -->|SEND_REMINDER| ReminderEngine
    LangGraph --> Groq & Gemini & PG
    APIRouters -->|Audio Upload| MinIO
    APIRouters -->|Enqueue STT/Embeddings| Redis

    Redis --> Worker
    Worker --> MinIO & PG & BGE & Groq & RulesEngine
    Worker --> RealtimeNotify
    RealtimeNotify -->|WhatsApp / Email| WhatsAppUser
    CronMorning & CronFollowup -->|Meta Graph v25.0| WhatsAppUser
```

---

### LangGraph Agentic Copilot Routing

```mermaid
stateDiagram-v2
    [*] --> InboundQuery: User sends natural language query
    InboundQuery --> EvidenceCheck: Evaluate _requires_evidence_search()
    
    EvidenceCheck --> Semantic_Route: Matches sentiment/discount/concern keywords
    EvidenceCheck --> FastPathCheck: Standard query flow

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
        LLMPlanner --> Action_Route: Client Reminder / Follow-up Action
        
        SQL_Route --> GenerateSQL: Groq Llama 3.3 70B
        GenerateSQL --> InjectRBAC: Append 'AND user_id = :user_id' for members
        InjectRBAC --> ExecuteSafeSQL: Read-only SELECT execution
        ExecuteSafeSQL --> Synthesizer: Tabular DB Results
        
        Semantic_Route --> EmbedQuery: BAAI/bge-m3 1024-dim vector
        EmbedQuery --> CosineSearch: PostgreSQL pgvector '<=>'
        CosineSearch --> Synthesizer: Top-K Meeting Evidence Chunks

        Action_Route --> ReminderService: Extract Client, Channel & Instruction
        ReminderService --> DispatchReminders: Concurrent Email & WhatsApp Send
        DispatchReminders --> Synthesizer: Delivery Report & Message Drafts
        
        Synthesizer --> SynthesizeResponse: Final grounded response generation
    }

    Synthesizer --> [*]: HTTP 200 JSON {answer, citations, sql/deliveries}
    ReturnFastAnswer --> [*]: HTTP 200 JSON Fast-Path
```

---

## 🔬 Deep Dive: Core Subsystems

### 1. Multi-Tenant Workspace, Hardened Auth & Gateway Security

Philixa 6.0 implements an enterprise-grade multi-tenancy model backed by a multi-layered defense-in-depth security architecture.

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
- **Google OAuth2 One-Tap Sign-In (`POST /auth/google`)**:
  - Verifies Google ID tokens cryptographically using `google.oauth2.id_token.verify_oauth2_token` against the configured Google Client ID.
  - Automatically provisions a verified user profile and creates an individual workspace (e.g., `"{given_name}'s Workspace"`) with Owner privileges on first login.
  - Issues full HttpOnly session cookies (`access_token`, `refresh_token`, `csrf_token`) and is explicitly exempt from CSRF validation.
- **Dual-Mounted Route Architecture**: Core authentication and workspace endpoints (`/auth`, `/workspaces`, `/audio`, `/live`, `/ws-ticket`) are dual-mounted at both the root `/` and `/api/v1/` for seamless client compatibility and backward integration.
- **10MB Global Request Payload Limiter (`enforce_payload_size_limit`)**: Middleware in `app/main.py` intercepts all incoming HTTP requests and enforces `MAX_CONTENT_LENGTH = 10 * 1024 * 1024` (10MB). Requests exceeding this ceiling are immediately rejected with `HTTP 413 Payload Too Large` without consuming downstream application or memory resources.
- **Production Settings Security Validator (`validate_production_settings`)**: Pre-flight security audit executed during FastAPI lifespan startup (`app/core/lifespan.py`). When `APP_ENV=production`, it enforces:
  1. `PHILIXA_JWT_SECRET` must be $\ge 32$ characters and cannot contain insecure default/demo strings.
  2. `PHILIXA_ALLOWED_ORIGINS` cannot contain wildcards (`*`).
  3. `PHILIXA_SMTP_USERNAME` and SMTP credentials must be configured.
  4. `PHILIXA_COOKIE_SECURE` must be set to `True` (HTTPS enforcement).
- **Session & Cookie Security**:
  - Bcrypt password hashing (`cost >= 12`).
  - Dual JWT HS256 cookies: `access_token` (15-minute lifespan) and `refresh_token` (30-day lifespan).
  - Single-flight token rotation via `POST /auth/refresh` preventing concurrency race conditions.
  - Anti-replay defense: Refresh tokens are SHA-256 hashed and matched against `user_sessions.refresh_token_hash`.
- **Double-Submit CSRF Protection**: `CSRFProtectionMiddleware` (`app/core/csrf.py`) verifies the `X-CSRF-Token` HTTP header against the `csrf_token` cookie for all mutating HTTP methods (`POST`, `PUT`, `PATCH`, `DELETE`).
- **Single-Use WebSocket Tickets**: Prevents passing JWTs over WebSocket query strings. Clients mint a 60-second signed ticket (`POST /ws-ticket`). Upon connection to `WS /live/transcribe`, Redis key `philixa:ws_ticket_used:{jti}` is written with a 60-second TTL to guarantee single-use replay defense.
- **Demo Sandbox Mode & Quotas**: Instant one-click workspace evaluation (`POST /auth/demo-login`) provisioning a pre-seeded workspace with realistic Indian wealth management clients, overdue commitments, and portfolio meetings.
  - **Quotas**: Demo guest accounts (`demo_guest_*`) are restricted to a maximum of **2 meeting note processings** (`HTTP 403 Forbidden`) and have an accelerated **1-day session expiry** (vs 30 days for standard accounts).

---

### 2. Multi-Modal Ingestion & Audio DSP Pipeline

Philixa 6.0 handles the full spectrum of meeting ingestion formats across asynchronous and real-time paths:

```
[ Ingestion Modes ] ──────────────► [ Processing Pipeline ] ──────────────► [ CRM Output ]
1. PASTED_NOTE (Raw Text)  ───────► Direct LLM Extraction  ──────────────► Structured Brief
2. AUDIO_UPLOAD (MinIO S3) ───────► FFmpeg DSP -> Whisper STT ───────────► Entities & Tasks
3. LIVE_BROWSER (16kHz PCM)──────► WebSocket -> Deepgram Nova-2 ────────► Live Transcript
4. Fast Dictation (Web Speech) ──► Client-Side Low-Latency en-IN ────────► Note Input Form
```

1. **Pasted Notes (`MeetingSourceType.PASTED_NOTE`)**: Direct text ingestion via `POST /api/v1/meeting-notes/process`. Directly triggers AI entity extraction, client resolution, commitment tracking, and risk signal detection.
2. **Audio Upload (`MeetingSourceType.AUDIO_UPLOAD`)**: Multipart audio upload (`.mp3`, `.m4a`, `.wav`) via `POST /audio/upload` (up to 50MB).
   - **Atomic Two-Phase Rollback**: If MinIO upload or database record allocation succeeds but ARQ background task enqueueing fails, an automated rollback handler purges the S3 object and deletes the database record, returning HTTP 500.
3. **Audio Digital Signal Processing (DSP) & Noise Filtering**:
   - Audio tracks are extracted and normalized via an FFmpeg filter chain: `ffmpeg -i input -af afftdn=nf=-30,highpass=f=200,lowpass=f=3000 -vn -ac 1 -ar 16000 -c:a pcm_s16le`.
   - Dynamic Whisper Prompt Injection (`_build_initial_prompt`): Injects active tenant client names into Whisper's initial decoding prompt to prevent phonetic hallucinations of Indian names.
   - Dual Diarization Modes: PyAnnote 3.1 speaker diarization supports **Solo Mode** (`diarize=False` for ~20s single-speaker voice memos) and **Meeting Mode** (`diarize=True` for multi-party advisory calls).
   - Voice Activity Detection (VAD) & Hallucination Suppression: Filters silent or degraded audio chunks (`no_speech_prob > 0.6 and avg_logprob < -1.0`, `compression_ratio > 2.4`).
4. **ASR Hinglish Translation & Normalization Layer (`translate_transcript`)**:
   - Pre-extraction AI translation layer (`app/services/ai_routing_service.py`, `app/ai/provider.py`) translates colloquial Hinglish speech into polished professional English.
   - Automatically repairs common Indian English / Hinglish ASR phonetic corruptions (e.g., `"Dil"` $\rightarrow$ `"Deal"`, `"Mande"` $\rightarrow$ `"Monday"`).
   - Enforces strict entity preservation rules: maintains Indian names in standard English transliteration (e.g., `'मनोज'` / `'Daksh'`, not phonetic approximations) and preserves competitor financial product names.
5. **MinIO Storage Purging Lifecycle (`PHILIXA_RETAIN_AUDIO`)**:
   - To respect client privacy and optimize storage quotas, audio files uploaded to MinIO are automatically purged post-transcription when `PHILIXA_RETAIN_AUDIO=0` (default), retaining only structured transcripts and embeddings.
6. **Live Diarized PCM Streaming (`MeetingSourceType.LIVE_BROWSER`)**: Captures browser microphone audio via an `AudioWorklet` (`pcm-processor.js`), streaming 16kHz Int16 raw PCM frames over `WS /live/transcribe` with ticket replay protection and real-time Deepgram STT transcription. Enforces a minimum 1.0s audio duration check to prevent transcription pipeline faults.
7. **Fast Browser Dictation (`en-IN`)**: Client-side speech-to-text using the browser's native Web Speech API (`fast-dictation.js`), tuned specifically for Indian English financial terminology with automated Android restart handling.
8. **Human-in-the-Loop (HITL) Triage Modals**:
   - **Client Confirmation Modal (`#confirmPanel`)**: Surfaced when AI client identification confidence is low or ambiguous; allows the advisor to assign the meeting to an existing client or create a new one (`POST /api/v1/meeting-notes/{id}/confirm-client`).
   - **Transcript Review Modal (`#editTranscriptPanel`)**: Allows advisors to review, correct acoustic errors in audio transcripts, and trigger re-extraction (`PATCH /api/v1/meeting-notes/{id}/transcript`).

---

### 3. Stateful Agentic Copilot, Vector RAG & Action Engine

The Copilot subsystem (`app/services/portfolio_copilot_service.py`) combines deterministic fast-paths, heuristic query interception, and a compiled LangGraph state machine:

```
                                      [ User Query ]
                                             |
                                             v
                             +-------------------------------+
                             | _requires_evidence_search()?  |
                             +-------------------------------+
                                     /               \
                          (Yes: Sentiment)        (No: Standard)
                                   /                   \
                                  v                     v
                 +----------------------+    +-------------------------------+
                 | Direct Vector Route  |    |   Deterministic Fast-Paths    |
                 | (Bypasses Broken SQL)|    | - Greetings                   |
                 +----------------------+    | - Asia/Kolkata Calendar Check |
                                  |          | - Direct Client Lookups       |
                                  |          +-------------------------------+
                                  |                     | (If no match)
                                  |                     v
                                  |          +-------------------------------+
                                  |          |    LangGraph: planner_node    |
                                  |          +-------------------------------+
                                  |                   /        |        \
                                  |                  /         |         \
                                  |                 v          v          v
                                  |         +-----------+ +-----------+ +-----------+
                                  |         | sql_gen_  | | semantic_ | |  action_  |
                                  |         |   node    | |   node    | |   node    |
                                  |         +-----------+ +-----------+ +-----------+
                                  |               \            |            /
                                  +--------------> \           |           /
                                                    v          v          v
                                             +-------------------------------+
                                             |       synthesizer_node        |
                                             | Grounded Answer with Evidence |
                                             +-------------------------------+
```

- **Unstructured Evidence Query Interceptor (`_requires_evidence_search`)**:
  - Deterministic regex interceptor scanning inbound queries for unstructured sentiment and qualitative terms (`discount`, `concern`, `complaint`, `issue`, `problem`, `sentiment`, `mood`, `interested`, `manga`, `chinta`, `pareshan`).
  - Directly forces routing to `semantic_node` (pgvector cosine search), preventing the LLM from hallucinating invalid SQL queries on nonexistent relational columns.
- **Deterministic Fast-Paths**:
  - `_is_greeting(query)`: Immediate conversational greeting without LLM latency.
  - `_meeting_schedule_date(query)`: Calculates weekday calendar schedules in `Asia/Kolkata` timezone (e.g., "milna", "Monday meetings").
  - `_extract_client_lookup_name(query)`: Direct SQL profile retrieval for queries like "Who is Vikram Malhotra?" or "Vikram kaun hai".
- **Safe Read-Only NL-to-SQL (`sql_generator_node`)**: Generates PostgreSQL queries with system prompt guardrails preventing mutating operations. For `member` roles, automatically appends tenant RBAC constraints (`AND user_id = :user_id`).
- **Semantic Evidence Retrieval (`semantic_node`)**:
  - Transcripts are chunked and embedded into 1024-dimensional vectors using `BAAI/bge-m3`.
  - Stored in the `meeting_evidence` table with Cosine Distance indexing (`<=>`).
- **LangGraph Action Node (`action_node`) & AI Reminder Engine (`ReminderService`)**:
  - When an advisor issues an actionable natural language command (e.g., *"Send a reminder to Vikram about Friday's mutual fund allocation"*), the `planner_node` selects the `"action"` route.
  - The `action_node` extracts the target client name, instruction payload, and communication channel (`email`, `whatsapp`, `both`), delegating to `ReminderService`.
  - `ReminderService` generates professional JSON message drafts (`email_subject`, `email_body`, and concise `whatsapp_body` $< 700$ chars) and executes concurrent async dispatches via `asyncio.gather` across `EmailAdapter` and `WhatsAppAdapter`.
  - Returns structured execution reports with granular delivery status per channel (`sent`, `failed`, `skipped`).

> 🔔 **Multi-Modal, Multi-Channel Client Reminder Scheduling**:
> Relationship Managers can trigger client reminders through **EITHER** modality:
> 1. **Conversational Voice (Philixa Brain FAB)**: Speak naturally in English or Hinglish (e.g., *"Philixa, WhatsApp Manoj that I will call him tomorrow at 10 AM"* or *"Email Vikram the debt mutual fund comparison"*). The voice assistant classifies the `SEND_REMINDER` intent and immediately executes `ReminderService`.
> 2. **Copilot Text & Chat (380px Sidecar Dock & REST API)**: Type into the Copilot chat sidecar or submit to `POST /api/v1/dashboard/copilot/ask` (e.g., *"Send an email and WhatsApp reminder to Priya about our portfolio review"*). The LangGraph state machine selects `action_node` and triggers `ReminderService`.
> 
> In both modalities, `ReminderService` generates channel-tailored copy and dispatches concurrently across Meta WhatsApp Cloud API v25.0 and transactional SMTP email.

- **Multi-Tier AI Routing**:
  - Primary Extraction & Planning: Groq Cloud (`llama-3.3-70b-versatile`).
  - Review / Fallback: Google Gemini (`gemini-2.5-flash` / `gemini-3.6-flash`).
  - Copilot Reasoning: Threaded execution preventing event loop starvation.

---

### 4. Conversational Voice Assistant & Intent Engine

Philixa Brain (`app/services/voice_assistant.py`) is a full-duplex conversational voice agent tailored for mobile and desktop advisors:

- **4-Way Intent Classification**:
  - `VoiceAssistantService.chat` evaluates spoken input and classifies it into one of four discrete operational intents:
    1. `QUERY`: Natural language question regarding CRM data or client history (delegates to Copilot).
    2. `SAVE_MEETING`: Dictation of meeting notes or interaction summary.
    3. `SEND_REMINDER`: Request to follow up or message a client via WhatsApp or Email (delegates to `ReminderService` to generate copy and dispatch across channels).
    4. `GENERAL_CHAT`: Conversational advisory assistance.
- **Asynchronous Background Meeting Ingestion**:
  - When the `SAVE_MEETING` intent is classified, the service immediately creates a `Meeting` database record with `source_type="voice"` and dispatches an asynchronous background task via FastAPI `BackgroundTasks` calling `MeetingProcessingService.process_existing_meeting`.
  - Returns an instant audio/text acknowledgment to the advisor while entity extraction, commitment tracking, and risk analysis run in the background.
- **Hindi Name & Phonetic Normalization**: Translates spoken Devanagari names to standard English representations (e.g., `'मनोज'` $\rightarrow$ `'Manoj'`).
- **Streaming TTS Voice Synthesis**: Streams low-latency natural speech responses via Sarvam AI (`bulbul:v3` in Hinglish) or Deepgram Aura (`POST /api/v1/voice/speak`).

---

### 5. Automated Rules Engine, Risk Scoring & CRM Intelligence

Philixa 6.0 features automated business intelligence services managing client lifecycles and proactive risk scoring:

- **Automated Rules Engine (`RulesEngineService`)**:
  - `sync_client_tasks_and_risks`: Synchronizes extracted meeting commitments into `FollowUpTask` items, dynamically calculating status flags (`is_completed`, `is_overdue`, and `is_due_today`) based on current UTC time and configured due date thresholds (`PHILIXA_DUE_DATE_THRESHOLD`).
  - **Deterministic Risk Signal Scoring**: Evaluates extracted meeting concerns and creates `RiskSignal` records. Sets `is_high_risk = True` and `requires_review = True` if:
    $$\text{severity} \in \{\text{"high"}, \text{"critical"}\} \quad \lor \quad (\text{severity} == \text{"medium"} \land \text{confidence} > 0.85)$$
- **Ask-Client Timeline Query Parser & Semantic Search (`AskClientService`)**:
  - `POST /api/v1/clients/{id}/ask` utilizes `_parse_query` to extract structured JSON metadata (`start_date`, `end_date`, `exact_keywords`, `optimized_query`) from natural language queries.
  - Executes date-bounded pgvector hybrid semantic search over `meeting_evidence`, generating synthesized answers with exact meeting citations (e.g., `Sources: Meetings 12, 15`).
- **Fuzzy Commitment Deduplication**:
  - Normalizes task strings and computes text similarity (`app/utils/text_normalization.py`). Commitments with similarity $\ge 0.72$ against existing open tasks for the same client are deduplicated, updating status lifecycles rather than creating duplicate clutter.
- **Pre-Meeting Briefing & Talking Point Synthesis (`MemoryService`)**:
  - Generates executive pre-meeting dossiers summarizing the last interaction, open commitments, owned banking products, primary client concerns, and AI-suggested conversational talking points.
- **Decoupled Client Product Tracking**:
  - Decouples `products_owned_json` (active banking/investment products held by client) from `products_interested_json` (prospective upsell interest noted during discussions).
- **Cascade Client Deletion (`ClientRepository`)**:
  - Deleting a client (`DELETE /api/v1/clients/{id}`) safely cascades deletion across all meetings, commitments, tasks, risk signals, and vector embeddings in `meeting_evidence`.

---

### 6. Distributed ARQ Worker & Scheduled Sweeps

Background execution is handled by an asynchronous ARQ worker container (`app/worker.py`) sharing Redis connection pools and database sessions:

- **Registered Asynchronous Tasks**:
  - `process_meeting_transcription`: Downloads audio from MinIO, executes FFmpeg filtering, Whisper transcription with Hinglish banking prompts, PyAnnote diarization, LLM entity extraction, rules engine synchronization, and enqueues embedding generation.
  - `generate_meeting_embeddings`: Splits transcripts into semantic chunks, generates 1024-dim `BAAI/bge-m3` vectors, and persists them into `meeting_evidence`.
  - `_notify_meeting_processed`: Real-time post-meeting notification dispatch sending immediate bilingual WhatsApp/Email alerts to the RM upon processing completion or failure.
- **Registered Distributed Cron Jobs (4 Total Sweeps)**:
  - `send_pre_interaction_briefs` (**07:00 UTC Daily**): Aggregates upcoming meetings for the day and sends executive briefings to RMs.
  - `send_client_followups` (**08:00 UTC Daily**): Identifies overdue commitments and pending client follow-up tasks and dispatches alerts.
  - `retry_failed_notifications` (**Every 15 Minutes**): Retries failed WhatsApp and email dispatches with exponential backoff.
  - `cleanup_demo_accounts` (**Hourly at Minute 0**): Purges expired `demo_guest_*` sandbox users and cascade-deletes all associated temporary organizations, meetings, commitments, and vectors (`scripts/cleanup_demo_accounts.py`).

---

### 7. Dual-Channel Notification Engine

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

## 🎨 Frontend Single-Page Application (SPA) Architecture

Philixa 6.0 features a responsive, accessible, full-featured Single-Page Application (SPA) built with vanilla modern JavaScript (`app/web/app.js`), semantic HTML5 (`app/web/index.html`), and a bespoke CSS design system (`app/web/styles.css`).

```
+-------------------------------------------------------------------------------------------------------------------------------+
|                                            PHILIXA 6.0 SPA WORKBENCH INTERACTION MAP                                          |
+-------------------------------------------------------------------------------------------------------------------------------+

  [ Topbar: Workspace Switcher Dropdown | Scope Toggle (Team/Me) | Copilot Sidecar Trigger | Avatar Profile & Settings ]
  +---------------------------------------------------------------------------------------------------------------------------+
  |  [ 4-Card Verdict Strip: Active Clients (#) | Pending Tasks (#) | Meetings Logged (#) | Risk Alerts (Status Badge) ]      |
  +---------------------------------------------------------------------------------------------------------------------------+
  |                                                  DESKTOP 60 / 40 WORKBENCH                                                |
  |  +-----------------------------------------------------+  +------------------------------------------------------------+  |
  |  | LEFT PANE (60%): 4-Tab Smart Intake Editor          |  | RIGHT PANE (40%): Structured Diff Review Workbench         |  |
  |  | * Tab 1: Paste Notes (Cmd+Enter Process)            |  | * Category Filter Pills (All / Commitments / Risks / Memory)|  |
  |  | * Tab 2: S3 Audio Drag-and-Drop (50MB Limit)        |  | * Interactive Diff Cards (Spacebar / Click Selection)      |  |
  |  | * Tab 3: Live Audio Hub (Solo vs Meeting Diarize)   |  | * Inline Title Edit (✎) & Due Date Pickers                 |  |
  |  | * Tab 4: Fast Dictation (en-IN Web Speech API)      |  | * Batch Action Bar (Cmd+Shift+Enter / Cmd+S Batch Sync)    |  |
  |  +-----------------------------------------------------+  +------------------------------------------------------------+  |
  +---------------------------------------------------------------------------------------------------------------------------+
  |  [ Daily Priorities & Risk Monitor ]  [ Client Memory Dossier Accordion & Q&A ]  [ Interactive Commitment Ledger Table ]  |
  +---------------------------------------------------------------------------------------------------------------------------+
  |  [ Persistent 380px AI Copilot Sidecar Dock (Cmd+Shift+L) with Grounded Client Pill & Live Token Budget Progress Meter ]  |
  |  [ Philixa Brain Floating Action Voice Agent (4-State Visual Machine: Idle / Listening / Thinking / Speaking) ]          |
  +---------------------------------------------------------------------------------------------------------------------------+
```

### 1. 6-View Fullscreen Auth Modal & State Machine
The client authentication layer (`#authModal`) operates as a complete 6-state machine managing onboarding and recovery flows:
- **State 1: Login (`#viewLogin`)**: Email and password authentication with demo workspace shortcut.
- **State 2: Registration (`#viewRegister`)**: Account creation with a toggle between **Company Workspace** (team collaboration) and **Individual Workspace** (solo advisor).
- **State 3: Email OTP Verification (`#viewVerifyEmail`)**: 6-digit OTP entry view with resend countdown.
- **State 4: Forgot Password Request (`#viewForgotPassword`)**: Email submission for password recovery links.
- **State 5: Password Reset Confirmation (`#viewResetPassword`)**: Token-authenticated password reset with client-side password matching validation.
- **State 6: Workspace Invite Acceptance (`#viewInviteAccept`)**: Allows invited team members to accept invites and establish credentials.
- **Deep-Linking & FOAC Prevention**: Supports URL deep-linking (`?action=verify-email`, `?action=reset-password`, `?invite=...`) and uses `.not-logged-in` CSS gating to eliminate Flash of Unauthenticated Content (FOAC). Left panel highlights CRM value propositions with `/static/premium_dashboard.jpg`.

### 2. Google Identity Services (GSI) One-Tap SSO Integration
Integrated Google Sign-In SDK (`https://accounts.google.com/gsi/client`) providing one-tap authentication (`#g_id_onload`, `.g_id_signin`). Captures Google ID tokens and submits them to `POST /api/v1/auth/google` via `handleGoogleCredentialResponse()`.

### 3. Multi-Tenant Workspace Context Switcher & Plan Badge
Sidebar dropdown selector (`#workspaceSelect`) populated with user's active organization memberships. Switching triggers `POST /workspaces/switch`, updates CSRF and session state, and re-renders the dashboard. Topbar displays dynamic subscription plan badge (`#topbarPlanBadge` e.g., "Free", "Pro").

### 4. Workspace Team Member Management & Dynamic RBAC Modal
Interactive modal (`#memberModal`) accessible to Owners/Admins via avatar dropdown. Displays member count badge (`#memberCountBadge`) and active roster table (User/Email, Role, Status, Joined date). Includes:
- **In-App Invitation Form (`#inviteMemberForm`)**: Invites members by email and role.
- **In-Place Role Selector (`.member-role-select`)**: Allows Owners to promote/demote members (`PATCH /workspaces/members/{id}/role`).
- **Member Removal Action (`.btn-remove-member`)**: Removes users with confirmation safeguards (`DELETE /workspaces/members/{id}`).

### 5. User Profile Avatar Dropdown, Initials Badges & Account Deletion
Circular avatar button (`#avatarBtn`) displaying computed 1-2 letter uppercase initials based on user name/email. Opens dropdown menu (`#avatarMenu`) containing display name, email, shortcuts for Member Management, Preferences, Theme Toggle, and Sign Out. In Settings Modal, features a "Danger Zone" with a "Permanently Delete Account" button (`#deleteAccountBtn`) issuing `DELETE /auth/me` with double-confirmation prompt.

### 6. Responsive App Shell, Collapsible 72px Icon-Rail & Mobile Drawer
Dual-state sidebar navigation (260px expanded vs 72px collapsed icon rail) togglable via header hamburger (`#sidebarToggleBtn`), logo click (`#logoToggleBtn`), or `Cmd+[` / `Ctrl+[` shortcut. On mobile viewports ($\le 980\text{px}$), collapses into a slide-over mobile drawer with dark backdrop overlay (`#mobileSidebarBackdrop`, `#mobileNavToggleBtn`). Includes Zoho-style loading splash screen (`#contentLoader`) with pulsing "P6" logo.

### 7. Dark / Light Theme System with WCAG AAA Contrast Tokens
Complete dark/light semantic design system (`.dark-theme`) mapped to zinc palettes and WCAG AAA contrast tokens (`--bg`, `--panel`, `--ink`, `--muted`, `--line`, `--accent`, `--success-*`, `--warning-*`, `--danger-*`, `--primary-*`, `--ai-*`). Theme toggle button in avatar menu (`#themeToggleBtn`) dynamically switches theme and saves to `localStorage.getItem("theme")`, loaded synchronously in `<head>` to prevent theme flash.

### 8. Homogeneous 4-Card Verdict Strip Metrics with Jump Navigation
Modern 4-card metric strip replacing legacy asymmetrical cards:
1. **Active Clients Card (`#verdictCardClients`)**: Shows client count; clicking/Enter focuses the Global Client Filter.
2. **Pending Commitments Card (`#verdictCardPending`)**: Shows pending count; clicking/Enter smooth-scrolls to the Commitments table.
3. **Meetings Logged Card (`#verdictCardMeetings`)**: Shows real monthly meetings logged count from `/api/v1/dashboard/metrics`; clicking/Enter focuses the note editor.
4. **Risk Alerts Card (`#verdictCardRisks`)**: Shows active risk count and dynamic status badge ("All clear" green vs "N Active" rose); clicking/Enter smooth-scrolls to Daily Priorities.

### 9. Tablet / Mobile Responsive Segmented Tab Switcher (< 1024px)
On displays $< 1024\text{px}$, transforms desktop 60/40 horizontal split into full-width segmented tab switcher between "📝 Meeting Note Intake" (`#tabMobileIntake`) and "✨ Extracted Diffs (N)" (`#tabMobileDiffs`). Automatically switches to Extracted Diffs tab upon completion of note extraction.

### 10. 4-Tab Smart Intake Editor
Master smart intake editor with 4 tabs:
- **Paste Notes (`#viewText`)**: Textarea with spellcheck, meeting date picker, and "✨ Process with AI" CTA (`Cmd+↵`).
- **Upload Audio (`#viewAudio`)**: Drag-and-drop zone (`#uploadBox`) for `.mp3, .m4a, .wav` (up to 50MB), filename preview, and status box with pulsating dot and automated 5-second polling loop.
- **Live Record Hub (`#viewLive`)**: Solo Record (~20s single speaker) vs Meeting Record (multi-speaker with diarization) and Stop & Save.
- **⚡ Fast Dictation (`#viewFastDictation`)**: Web Speech API in `en-IN`, interim + final transcript streaming display, Android bug auto-restart handling, and auto-paste to note editor.
- **Pre-selection Client Dropdown (`#knownClient`)**.

### 11. Structured Diff Review Workbench (60/40 Split Master-Detail)
Right-pane 40% interactive staging workbench for reviewing extracted entities before synchronizing to client memory:
- **Category Filter Pills**: Real-time filtering with badge counters for `All`, `Commitments`, `Risks`, `Memory`.
- **Interactive Diff Cards**: Full-card click or spacebar to toggle selection (`role="checkbox"`, `aria-checked`).
- **Inline Editing**: Inline editable Title (`✎` button) and Due Date input (`<input type="date">`).
- **Source Quote Attribution**: Verbatim quotes linking extracted points to transcript text.
- **Micro-Dismiss Action**: `✕` button to discard specific hallucinations or invalid items.
- **Batch Diff Action Bar**: `Discard All` and `✓ Sync Selected (N)` (`<kbd>⌘⇧↵</kbd>` / `Cmd+S`).
- **Focus Trapping**: Automatically shifts focus to the first diff card when extraction finishes.

### 12. Global Client Filter Omnibar & Cascade Delete Action
Sidebar client filter dropdown (`#topClientSelect`) that filters all views and dossier memory. When a specific client is selected, a delete button (`#deleteSelectedClientBtn` 🗑️) dynamically appears with a confirmation dialog to delete the client profile and cascade-delete all associated meetings and commitments (`DELETE /api/v1/clients/{id}`).

### 13. Client Memory Dossier Accordion & Pre-Meeting Brief Card
Collapsible accordion interface (`#memoryPanel`) rendering a rich **AI Pre-Meeting Executive Brief Card** (Last Meeting recap, Pending commitments list, Products owned tags, Primary client concern, and Suggested Talking Points for the advisor). Includes a nested collapsible "Detailed History" sub-accordion showing the rolling narrative, meeting summaries, historical concerns, and relationship notes.

### 14. In-Dossier Client Q&A with Speech Recognition Voice Input
Interactive Q&A bar inside Client Memory (`#askClientInput`, `#askClientBtn`) allowing advisors to ask natural language questions about a specific client. Features a dedicated microphone button (`#askClientVoiceBtn`) powered by Web Speech API (`en-IN`) that transcribes spoken questions and auto-submits them, displaying formatted answers with source meeting citations (`Sources: Meetings 12, 15`).

### 15. Interactive Commitment Ledger Table & Optimistic Status Toggling
Commitment table with Client Name, Task Description, Owner, Extraction Confidence percentage (`Confidence: 95%`), Due Date, Urgency badge (`high`, `medium`, `low`), Status badge (`pending`, `completed`), and Quick-action toggle link (`Complete` / `Reopen`). Supports status filtering (`#commitmentFilter`: All/Pending/Completed) and optimistic UI updates calling `PATCH /api/v1/commitments/{id}/status`.

### 16. Daily Priorities List & Dynamic False-Alarm Safe Risk Monitor
Dual-panel daily workbench:
- **Follow-up Tasks List (`#taskList`)**: Categorizes tasks into `Overdue` (red badge), `Due Today` (amber badge), and `Upcoming` (blue badge).
- **Risk Signals List (`#riskList`)**: False-alarm-safe header with dynamic badge (`#riskSignalsBadge`): green "0 Active Risks - All Clear" when 0 risks vs rose pulsing badge "${N} Action Required" when risks exist. Cards display severity badge (`high`, `medium`, `low`), review state badge ("Review needed" vs "Monitoring"), and AI confidence percentage score.

### 17. Team Performance Overview Dashboard Table
Performance dashboard table (`#teamPerformanceSection`) dynamically shown only to workspace Owners and Admins in "Team Workspace" scope. Displays employee email, total clients owned, total meetings logged, and an interactive colored commitment completion progress bar (Green $\ge 80\%$, Amber $\ge 50\%$, Red $< 50\%$) with completed vs pending counts.

### 18. Workspace Scope Toggle (Team Workspace vs My Workspace)
Scope dropdown (`#scopeSelect`) in the sidebar for Owners and Admins to toggle between "Team Workspace" (organization-wide aggregation) and "My Workspace" (individual RM assignment mode). Automatically refetches clients, commitments, and team performance metrics.

### 19. Persistent 380px AI Copilot Sidecar with Live Token Budget Meter
Persistent 380px slide-out sidecar dock (`#copilotSidecar`) accessible from topbar (`#topbarCopilotBtn`) or shortcuts (`Cmd+Shift+L`, `Cmd+/`, `Cmd+J`). Features:
- **Grounded Client Pill (`#copilotGroundedClient`)**: Displays active client context dossier.
- **Live Token Budget Meter (`#copilotTokenText`, `#copilotTokenFill`)**: Visual progress bar tracking token consumption (`1,420 / 8,192 tokens`).
- **Chat Stream & Provenance Badges**: Chat bubbles, "Thinking..." indicator, and search provenance tags ("✨ Generated via Database Search" vs "✨ Generated via Vector Search").

### 20. Philixa Brain Voice Assistant 4-State Visual State Machine
Voice assistant FAB button (`#philixaVoiceBtn`) featuring a 4-state visual state machine:
1. `idle` (🎙️ PHILIXA)
2. `listening` (🔴 LISTENING...)
3. `thinking` (🤔 THINKING...)
4. `speaking` (💬 SPEAKING...)
- **4000ms Silence Detection Timer (`SILENCE_LIMIT_MS`)** with auto-stop.
- **10-Turn Rolling Conversation Memory Array**.
- **Auto-Continuation**: Detects questions in AI speech ("?", "save", "karein", "bataiye") and automatically re-activates microphone listening.
- **Streaming TTS Playback** with automatic audio blob memory cleanup.
- **Background Meeting Polling**: When notes are saved via voice, automatically polls status and pops up client confirmation modal if ambiguous.

### 21. Notification Preferences Modal & Quiet Hours Configuration
Preferences modal dialog (`#settingsModal`) accessible via avatar dropdown. Allows advisors to configure notification opt-in (`#prefOptIn`), WhatsApp phone number or email (`#prefContact`), and quiet hours time pickers (`#prefQuietStart`, `#prefQuietEnd`) to enforce disturbance-free periods (`PUT /api/v1/preferences`).

### 22. Client-Side Single-Flight Refresh Queue & Double-Submit CSRF Guard
Universal `fetchWithAuth()` client-side security wrapper (`app/web/app.js:221-326`):
- Automatic `X-CSRF-Token` header injection extracted from `csrf_token` cookie for mutating HTTP requests.
- Single-flight token refresh queue (`isRefreshing`, `refreshQueue`, `processRefreshQueue`) that catches 401s, pauses concurrent API calls, executes a single refresh call to `/api/v1/auth/refresh`, updates CSRF token, and replays all queued requests seamlessly.
- Single-use signed WebSocket ticket generation (`mintWsTicket()`, `POST /api/v1/ws-ticket`).

### 23. Toast Notification System
Toast notification banner (`#toast`, `.toast.show`, `.toast.error`) providing real-time feedback for background tasks, save events, error alerts, and status changes with automatic 2.8-second auto-dismiss.

### 24. Comprehensive Keyboard Shortcuts & WCAG 2.2 AAA Accessibility
Global keyboard shortcut system:
- `Cmd+Enter` / `Ctrl+Enter`: Exclusively triggers Meeting Notes AI Intake.
- `Cmd+Shift+Enter` / `Ctrl+Shift+Enter` (or `Cmd+S`): Exclusively triggers Batch Diff Synchronization.
- `Cmd+Shift+L` / `Ctrl+Shift+L` (also `Cmd+/`, `Cmd+J`): Toggles AI Copilot Sidecar Dock.
- `Cmd+[` / `Ctrl+[`: Toggles Navigation Sidebar collapse.
- `Esc`: Closes Copilot Sidecar, Settings Modal, Member Modal, or exits diff inline editing.
- `Spacebar`: Toggles selection of focused Diff Card (`role="checkbox"`).
- `Enter`: Saves inline diff title edit; activates verdict card navigation.
- Unified WCAG 2.2 Level AAA Focus Ring system (`outline: 2px solid var(--accent) !important; outline-offset: 2px !important;`).

---

## 🖥 Interactive Developer & Management Portals

Once the Philixa infrastructure is running, the following portals are accessible:

| Service / Interface | URL | Default Credentials / Port | Description |
|---|---|---|---|
| **Single-Page Application (SPA)** | `http://localhost:8000/` | Interactive Web UI | Full CRM dashboard, 60/40 Diff Review Workbench, Copilot Sidecar, Voice FAB, Ingestion Tabs, and HITL panels. |
| **Interactive Swagger API Docs** | `http://localhost:8000/docs` | Public / Open | OpenAPI interactive documentation for testing all 49 endpoints. |
| **ReDoc API Reference** | `http://localhost:8000/redoc` | Public / Open | Comprehensive, human-readable API specification and schemas. |
| **OpenAPI Schema JSON** | `http://localhost:8000/openapi.json` | Public / Open | Raw JSON schema for SDK generation and contract testing. |
| **MinIO Object Storage Console** | `http://localhost:9001` | `philixa_minio` / `philixa_secret` | Web interface to inspect audio buckets and tenant namespaces. |
| **System Health Check** | `http://localhost:8000/health` | Public | JSON status: `{"status": "ok", "app_version": "1.0.0", "database": "ok", "enable_audio_upload": false}`. |

---

## 📖 Complete 49-Endpoint API Catalog

The backend exposes **49 distinct API operations** across 11 route modules (accessible under `/api/v1` and dual-mounted for `/auth`, `/workspaces`, `/audio`, `/live`, and `/ws-ticket`):

### 2.1 Authentication & Session Management (`app/api/v1/routes_auth.py`)

| # | Method | Endpoint | Security / Auth | Description |
|---|:---:|---|---|---|
| 1 | `POST` | `/auth/register` | Public | Onboard new user, create primary organization, and send verification email. |
| 2 | `POST` | `/auth/verify-email` | Token Query | Verify user email with 24-hour SHA-256 token. |
| 3 | `POST` | `/auth/login` | Public | Verify credentials (bcrypt), create user session, and issue HttpOnly JWT cookies. |
| 4 | `POST` | `/auth/google` | Public | Verify Google OAuth2 ID token, auto-provision user and workspace, issue session cookies. |
| 5 | `POST` | `/auth/demo-login` | Public | Instant one-click sandbox workspace provisioning with pre-seeded CRM data. |
| 6 | `GET` | `/auth/me` | JWT Cookie / Bearer | Retrieve active user profile, memberships, active workspace context, and role. |
| 7 | `POST` | `/auth/refresh` | Cookie `refresh_token` | Single-flight token rotation; issues fresh access token and rotates refresh token hash. |
| 8 | `POST` | `/auth/logout` | JWT Cookie / Bearer | Revoke active user session in database and clear session cookies. |
| 9 | `POST` | `/auth/forgot-password` | Public | Send 1-hour password reset email link with secure token. |
| 10 | `POST` | `/auth/reset-password` | Token Query | Reset password using valid token. |
| 11 | `DELETE` | `/auth/me` | JWT Cookie / Bearer | Account deletion cascade (purges sessions, memberships, and owned records). |
| 12 | `POST` | `/ws-ticket` | JWT Cookie / Bearer | Mint a 60-second single-use signed ticket for WebSocket audio streaming. |

### 2.2 Multi-Tenant Workspace & Team Management (`app/api/v1/routes_workspace.py`)

| # | Method | Endpoint | Security / RBAC | Description |
|---|:---:|---|---|---|
| 13 | `GET` | `/workspaces` | Authenticated | List all organizations/workspaces the authenticated user belongs to. |
| 14 | `POST` | `/workspaces/switch` | Authenticated (Member) | Switch active workspace context and issue updated session cookies. |
| 15 | `POST` | `/workspaces/invite` | Owner / Admin | Send 7-day email invitation to onboard a new team member. |
| 16 | `POST` | `/workspaces/invite/accept` | Public / Token | Accept workspace invite token and set user password. |
| 17 | `GET` | `/workspaces/members` | Authenticated | List all members and roles in the active workspace. |
| 18 | `PATCH` | `/workspaces/members/{id}/role` | Owner Only | Update member role (`admin`, `member`). Last owner cannot be demoted. |
| 19 | `DELETE` | `/workspaces/members/{id}` | Owner / Admin | Remove user from active workspace. Last owner cannot be removed. |

### 2.3 Client Relationship & Memory Management (`app/api/v1/routes_clients.py`)

| # | Method | Endpoint | Security / RBAC | Description |
|---|:---:|---|---|---|
| 20 | `POST` | `/api/v1/clients` | Authenticated | Create a new tenant-scoped client profile. |
| 21 | `GET` | `/api/v1/clients` | Authenticated | List clients with pending commitment counts (supports `?scope=team` vs `?scope=me`). |
| 22 | `GET` | `/api/v1/clients/{id}` | Tenant-Scoped | Retrieve client profile, contact details, products owned/interested, and rolling narrative. |
| 23 | `PUT` | `/api/v1/clients/{id}` | Tenant-Scoped | Update client metadata, decoupled products owned/interested JSON, and relationship notes. |
| 24 | `DELETE` | `/api/v1/clients/{id}` | Tenant-Scoped | Cascade delete client and all dependent meetings, commitments, and vectors. |
| 25 | `GET` | `/api/v1/clients/{id}/memory` | Tenant-Scoped | Retrieve structured rolling brief, open commitments, and top historical concerns. |
| 26 | `POST` | `/api/v1/clients/{id}/ask` | Tenant-Scoped | Natural language Q&A over a specific client's history with meeting citations. |
| 27 | `GET` | `/api/v1/clients/{id}/meetings` | Tenant-Scoped | List chronological meeting records for a specific client. |

### 2.4 Meeting Intelligence & Human-in-the-Loop (`app/api/v1/routes_meeting_notes.py`)

| # | Method | Endpoint | Security / RBAC | Description |
|---|:---:|---|---|---|
| 28 | `POST` | `/api/v1/meeting-notes/process` | Authenticated | Ingest raw notes (`PASTED_NOTE`), run LLM extraction, match client, extract tasks (demo max 2). |
| 29 | `GET` | `/api/v1/meeting-notes/{id}` | Tenant-Scoped | Retrieve meeting summary, raw notes, discussion points, concerns, and status. |
| 30 | `POST` | `/api/v1/meeting-notes/{id}/confirm-client` | HITL Scoped | Manually assign an ambiguous meeting to an existing client or trigger auto-creation. |
| 31 | `PATCH` | `/api/v1/meeting-notes/{id}/transcript` | HITL Scoped | Correct noisy audio transcript and trigger re-extraction and vector generation. |

### 2.5 Commitment Tracking (`app/api/v1/routes_commitments.py`)

| # | Method | Endpoint | Security / RBAC | Description |
|---|:---:|---|---|---|
| 32 | `GET` | `/api/v1/commitments` | Authenticated | List commitments with filtering (`status`, `client_id`, `due_before`, `scope`). |
| 33 | `PATCH` | `/api/v1/commitments/{id}/status` | Tenant-Scoped | Toggle commitment status between `pending`, `completed`, and `cancelled`. |

### 2.6 Audio Storage & Live Streaming (`app/api/v1/routes_audio.py`, `routes_live.py`)

| # | Method | Endpoint | Security / RBAC | Description |
|---|:---:|---|---|---|
| 34 | `POST` | `/audio/upload` | Authenticated | Upload multipart audio to MinIO (`philixa-audio`), enqueue ARQ transcription. |
| 35 | `GET` | `/audio/{id}/url` | Tenant-Scoped | Generate temporary presigned MinIO S3 download URL (1-hour expiry). |
| 36 | `WS` | `/live/transcribe` | Single-Use Ticket | Real-time WebSocket PCM audio streaming with Redis ticket replay protection. |

### 2.7 Conversational Voice Assistant (`app/api/v1/routes_voice.py`)

| # | Method | Endpoint | Security / RBAC | Description |
|---|:---:|---|---|---|
| 37 | `POST` | `/api/v1/voice/speak` | Authenticated | Text-to-Speech audio streaming via Sarvam AI (`bulbul:v3`) or Deepgram Aura. |
| 38 | `POST` | `/api/v1/voice/chat` | Authenticated | 4-intent conversational voice agent reasoning with async background note creation. |

### 2.8 Dashboard Analytics & Agentic Copilot (`app/api/v1/routes_dashboard.py`)

| # | Method | Endpoint | Security / RBAC | Description |
|---|:---:|---|---|---|
| 39 | `GET` | `/api/v1/dashboard/priorities` | Authenticated | Daily actionable priorities: overdue commitments and client risk signals. |
| 40 | `GET` | `/api/v1/dashboard/metrics` | Authenticated | High-level summary metrics (total clients, meetings processed, open tasks). |
| 41 | `GET` | `/api/v1/dashboard/team-performance` | Owner / Admin | Per-advisor CRM workload, meeting velocity, and commitment resolution stats. |
| 42 | `POST` | `/api/v1/dashboard/copilot/ask` | Authenticated | Hybrid LangGraph natural language Copilot (NL-to-SQL + pgvector + Action reminders). |

### 2.9 Notification Preferences & WhatsApp Webhooks (`app/api/v1/routes_preferences.py`, `routes_webhooks.py`)

| # | Method | Endpoint | Security / RBAC | Description |
|---|:---:|---|---|---|
| 43 | `GET` | `/api/v1/preferences` | Authenticated | Retrieve user notification settings (WhatsApp number, quiet hours, timezone). |
| 44 | `PUT` | `/api/v1/preferences` | Authenticated | Update user notification preferences. |
| 45 | `GET` | `/api/v1/webhooks/whatsapp` | Hub Verify | Meta WhatsApp Cloud API webhook hub challenge verification (`hub.challenge`). |
| 46 | `POST` | `/api/v1/webhooks/whatsapp` | Meta Webhook | Inbound WhatsApp messages and real-time message delivery status processing. |

### 2.10 Background Jobs & System Health (`app/api/v1/routes_jobs.py`, `routes_health.py`, `app/main.py`)

| # | Method | Endpoint | Security / RBAC | Description |
|---|:---:|---|---|---|
| 47 | `GET` | `/api/v1/jobs/{job_id}` | Authenticated | Poll ARQ background transcription/embedding job progress and completion status. |
| 48 | `GET` | `/health` | Public | Real-time health check returning database status, app version, and audio upload flag. |
| 49 | `GET` | `/` | Public | Serves static Single-Page Application (SPA) HTML shell (`app/web/index.html`). |

---

## 🗄 Database Entity Relationship & 17 Relational Models

The relational schema is managed by **19 sequential Alembic migrations** up to `h5c3d4e5f6g7_multi_tenant_auth_and_workspaces.py` and `9a1b2c3d4e5f_decouple_products_owned_and_products_interested.py`. All 17 SQLAlchemy models map directly to physical PostgreSQL tables:

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
| 8  | clients                    | id (UUID)   | organization_id, user_id| Client CRM profiles, decoupled products_owned_json &  |
|    |                            |             |                        | products_interested_json, rolling narrative          |
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

Philixa 6.0 configures **59 parameters** via Pydantic `BaseSettings` (`app/core/config.py`), with pre-flight security evaluation (`validate_production_settings`) on boot:

| Category | Environment Variable | Default / Example Value | Description |
|---|---|---|---|
| **App Core** | `PHILIXA_ENV` / `APP_ENV` | `development` | Runtime environment (`development` vs `production`). Enables strict CSRF & security validation. |
| | `PHILIXA_APP_NAME` | `PHILIXA 6.0 V1-MVP` | Human-readable application title. |
| | `PHILIXA_APP_VERSION` | `1.0.0` | Semantic version string. |
| | `PHILIXA_SKIP_STARTUP_CHECKS` | `0` | Set to `1` to bypass pre-flight DB connection checks in test environments. |
| | `PHILIXA_ENABLE_AUDIO_UPLOAD` | `0` (`false`) | Feature flag enabling or disabling audio upload capabilities. |
| **Database & Cache** | `PHILIXA_DATABASE_URL` | `postgresql+psycopg://postgres:dev_only_password@localhost:5432/philixa` | Async PostgreSQL connection string using `psycopg` driver. |
| | `PHILIXA_REDIS_URL` | `redis://localhost:6379/0` | Redis instance for ARQ background queues and WebSocket tickets. |
| | `db_pool_size` | `15` | SQLAlchemy async connection pool base size. |
| | `db_max_overflow` | `5` | Maximum overflow connections allowed beyond base pool size. |
| | `db_pool_timeout` | `30` | Seconds to wait before timing out on connection pool exhaustion. |
| | `db_pool_pre_ping` | `True` | Tests connection liveliness before checkout to avoid stale socket disconnects. |
| **Auth & Security** | `PHILIXA_JWT_SECRET` | *(32+ char hex string)* | Cryptographic secret for signing HS256 JWT access and refresh tokens. |
| | `PHILIXA_JWT_ALGORITHM` | `HS256` | JWT signing algorithm. |
| | `PHILIXA_CSRF_SECRET` | *(32+ char hex string)* | Cryptographic secret for generating double-submit CSRF tokens. |
| | `PHILIXA_JWT_ACCESS_TOKEN_EXPIRE_MINUTES` | `15` | Access token lifespan. |
| | `PHILIXA_JWT_REFRESH_TOKEN_EXPIRE_DAYS` | `30` | Refresh token lifespan. |
| | `PHILIXA_COOKIE_SECURE` | `False` (`True` in prod) | Flag requiring HTTPS for session cookies. |
| | `PHILIXA_COOKIE_DOMAIN` | `None` | Optional domain scoping for auth cookies. |
| | `PHILIXA_COOKIE_SAMESITE` | `lax` | SameSite cookie attribute (`lax` / `strict` / `none`). |
| | `PHILIXA_ALLOWED_ORIGINS` | `http://localhost:8000` | Comma-separated CORS whitelist origins. Disallows `*` in production. |
| | `google_client_id` | `401674766048-...apps.googleusercontent.com` | Google Identity Services OAuth 2.0 Client ID for One-Tap sign-in. |
| | `PHILIXA_DEMO_API_KEY` | `""` | Optional API key for programmatic demo provisioning. |
| **Thresholds & Limits** | `PHILIXA_CLIENT_NAME_MAX_CHARS` | `120` | Maximum character length permitted for client names. |
| | `PHILIXA_COMMITMENT_DESCRIPTION_MAX_CHARS` | `500` | Maximum character length permitted for commitment descriptions. |
| | `PHILIXA_CLIENT_AUTO_CREATE_THRESHOLD` | `0.80` | Minimum confidence score required to auto-create client without HITL modal. |
| | `PHILIXA_DUE_DATE_THRESHOLD` | `0.75` | Minimum confidence score required to accept AI extracted due dates. |
| | `PHILIXA_RETAIN_AUDIO` | `0` | Storage lifecycle flag (`0` purges MinIO audio post-transcription; `1` retains audio). |
| **AI LLM Inference** | `PHILIXA_GROQ_API_KEY` | `gsk_...` | High-speed LLM inference key for meeting extraction and Copilot. |
| | `PHILIXA_AI_MODEL` | `llama-3.3-70b-versatile` | Primary Groq LLM model identifier. |
| | `PHILIXA_GEMINI_API_KEY` | `AIzaSy...` | Google Gemini API key for Tier 2 extraction review fallback. |
| | `PHILIXA_AI_REVIEW_MODEL` | `gemini-2.5-flash` | Review LLM model identifier. |
| | `PHILIXA_AI_BASE_URL` | `None` | Custom base URL for OpenAI-compatible LLM gateways. |
| | `PHILIXA_AI_API_KEY` | `""` | Optional generic AI provider API key. |
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
| | `WHATSAPP_BUSINESS_ACCOUNT_ID`| `...` | Meta WhatsApp Cloud API Business Account ID. |
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
1. `db`: PostgreSQL 16 with `pgvector` extension on port `5432`.
2. `redis`: Redis 7 Alpine cache and task broker on port `6379`.
3. `minio`: MinIO S3 Object Storage on ports `9000` (API) and `9001` (Console).
4. `app`: FastAPI web application on port `8000` (runs migrations and production security validation on boot).
5. `worker`: ARQ background worker executing transcription, embeddings, rules engine scoring, and 4 cron sweeps.

---

### Option B: Bare-Metal Virtualenv Setup

For local backend development, run the services on bare metal:

#### Prerequisites
- **Python 3.12+**
- **FFmpeg** installed and in system `PATH` (required for audio slicing, DSP filter chains, and Whisper)
- **PostgreSQL 15/16+** with `pgvector` extension
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
4. *Sandbox Boundaries*: Demo sessions expire in 1 day and are quota-restricted to 2 meeting note extractions. Temporary accounts are automatically purged every hour by the background cleanup cron.

---

## 💻 Verified cURL Workflows

### 1. One-Click Sandbox Demo Login & Session Capture

```bash
# Provision a demo sandbox workspace and save session cookies
curl -X POST "http://localhost:8000/auth/demo-login" \
     -H "Content-Type: application/json" \
     -c cookies.txt
```

### 2. Standard User Registration & Google SSO Login

```bash
# 1. Register a standard company workspace
curl -X POST "http://localhost:8000/auth/register" \
     -H "Content-Type: application/json" \
     -d '{
       "email": "advisor@apexwealth.com",
       "password": "SecurePassword123!",
       "workspace_name": "Apex Wealth Advisory",
       "workspace_type": "company"
     }'

# 2. Login with Google OAuth2 ID Token
curl -X POST "http://localhost:8000/auth/google" \
     -H "Content-Type: application/json" \
     -c cookies.txt \
     -d '{
       "id_token": "eyJhbGciOiJSUzI1NiIsImtpZCI6Ij..."
     }'
```

### 3. Querying the Agentic Copilot (Verified Fixed Schema & Actions)

> ⚠️ **Schema Requirement**: The Copilot endpoint expects `"query"` (using `"question"` results in an HTTP 422 error). In production, provide the `X-CSRF-Token` from your session cookie.

```bash
# Query the Copilot using captured cookies and CSRF token
curl -X POST "http://localhost:8000/api/v1/dashboard/copilot/ask" \
     -b cookies.txt \
     -H "Content-Type: application/json" \
     -H "X-CSRF-Token: <csrf_token_from_cookie>" \
     -d '{
       "query": "Send a reminder to Vikram about the debt mutual fund comparison by Friday",
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

Philixa 6.0 maintains a structured, robust automated test suite catalog partitioned into Unit, Integration, and End-to-End (E2E) suites:

```
tests/
├── unit/                                   # Isolated logic, crypto, rules, and model tests
│   ├── test_security_crypto.py             # Bcrypt, JWT tokens, CSRF validation
│   ├── test_worker_cron.py                 # ARQ cron schedules & demo cleanup execution
│   ├── test_products_decoupling.py         # products_owned vs products_interested schemas
│   ├── test_m1_data_models_and_migration.py# Schema verification & migration validation
│   ├── test_m5_frontend_rbac_stress.py     # UI RBAC permission guards & role transitions
│   └── test_verification_suite.py          # Regression & core assertions
├── integration/                            # Multi-component & API integration tests
│   ├── test_auth_flow.py                   # Register, login, Google SSO, token refresh
│   ├── test_workspace_management.py        # Workspace switching, member invitations, RBAC
│   ├── test_tenant_isolation.py            # Multi-tenant scoping & repository isolation
│   ├── test_websocket_audio_security.py    # WS ticket replay defense & duration checks
│   └── test_m3_workspace_rbac_csrf_stress.py# CSRF token enforcement & RBAC boundaries
├── e2e/                                    # Real-world user journey simulations
│   └── test_real_world_saas_scenarios.py   # Multi-turn CRM workflows, note intake to brief
└── conftest.py                             # Pytest fixtures, test DB session, async test client
```

### Running the Test Suites

```bash
# Run full test suite
pytest

# Run tests with verbose output and short tracebacks
pytest -v --tb=short

# Run Unit Test Suite
pytest tests/unit/

# Run Integration Test Suite
pytest tests/integration/

# Run End-to-End Test Suite
pytest tests/e2e/

# Run specific domain test files
pytest tests/integration/test_auth_flow.py
pytest tests/integration/test_tenant_isolation.py
pytest tests/unit/test_worker_cron.py
pytest tests/unit/test_products_decoupling.py
```

---

## 🗺️ Roadmap & Engineering Milestones

- [x] **Multi-Tenant Workspace & Role-Based Access Control (RBAC)** (`owner`, `admin`, `member`)
- [x] **Hardened Web Security Core** (HttpOnly JWT cookies, single-flight refresh rotation, double-submit CSRF, 10MB payload limit)
- [x] **Google OAuth2 One-Tap SSO Authentication** (`POST /auth/google` + Google Identity Services SDK)
- [x] **Single-Use WebSocket Tickets with Redis Replay Defense**
- [x] **Multi-Modal Ingestion Pipelines** (Pasted Notes, MinIO S3 Multipart Drag-and-Drop, Live PCM Streaming, Fast Dictation)
- [x] **Audio DSP & Hinglish Normalization** (FFmpeg filter chain, client-name prompt injection, ASR Hinglish translation layer)
- [x] **60/40 Structured Diff Review Workbench & HITL Triage Modals** (Diff cards, inline edit, batch sync, client confirmation)
- [x] **LangGraph Agentic Copilot with PostgreSQL pgvector RAG** (`BAAI/bge-m3` 1024-dim embeddings)
- [x] **Copilot Action Node & AI Reminder Engine** (`ReminderService` multi-channel email/WhatsApp dispatch)
- [x] **Conversational Voice Assistant (4-State Visual Machine & 4-Intent Classifier)**
- [x] **Distributed ARQ Background Worker & 4 Scheduled Cron Sweeps** (Morning briefs, overdue alerts, 15m retry, hourly demo purge)
- [x] **Automated Business Rules Engine** (Task status calculation & deterministic risk signal scoring)
- [x] **Decoupled Client Product Tracking** (`products_owned_json` vs `products_interested_json`)
- [x] **One-Click Sandbox Demo Mode with Quota Safeguards**
- [x] **Comprehensive Keyboard Shortcuts & WCAG 2.2 AAA Design System**
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
