# Project: PHILIXA 6.0 Multi-Tenant SaaS Authentication & Workspace System

## Architecture
- **Web Layer (FastAPI)**: Session cookie authentication (`access_token`, `refresh_token`), CSRF validation (`X-CSRF-Token` header vs `csrf_token` cookie), WebSocket ticket exchange (`POST /api/v1/ws-ticket`), namespaced audio endpoints (`GET /api/v1/audio/{meeting_id}/url`).
- **Core Security & Auth**: `CurrentPrincipal` dependency resolves authenticated user, active organization, role (`owner` | `admin` | `member`), and session ID. Cryptographic password hashing (bcrypt >= 12) and JWT token creation/validation (HS256).
- **Data & Repository Layer (`app/repositories/`)**: Encapsulates all database queries with mandatory multi-tenant scoping (`organization_id`) and role-based ownership (`user_id` for `member` role). Inaccessible IDs return HTTP 404 to prevent ID enumeration.
- **Relational Storage (PostgreSQL & SQLAlchemy 2.0)**: Multi-organization membership (`organization_memberships`), active sessions (`user_sessions`), verification/reset tokens, workspace invites, and composite FK constraints on tenant tables (`clients`, `meetings`, `commitments`).
- **Asynchronous Jobs (ARQ & Redis)**: Job payloads carry `organization_id` and `user_id`; worker tasks query meetings strictly scoped to `(id, organization_id, user_id)`. Redis tracks one-time WebSocket ticket tokens with 60s TTL.
- **Object Storage (MinIO)**: Audio files namespaced under `{organization_id}/{user_id}/{meeting_id}/{filename}` with presigned URL validation.
- **Frontend SPA (Vanilla JS)**: Multi-view auth state machine (Login, Register with individual/company toggle, Verify Email, Reset Password, Workspace Switcher, Member Management), fetch wrapper with `credentials: "include"`, CSRF headers, and transparent token refresh retry.

## Feature Inventory
| # | Feature | Description | Milestone | Source |
|---|---------|-------------|-----------|--------|
| 1 | Multi-Org Identity & Membership | `OrganizationMembership` model with composite PK `(user_id, organization_id)`, roles `owner`/`admin`/`member`, status, inviter tracking | M1 | R1.1 |
| 2 | Workspace Metadata & Slugs | `Organization` extended with `workspace_type`, unique `slug`, and `plan` | M1 | R1.2 |
| 3 | User Model Decoupling | Remove `organization_id` and `role` from `User`, add `is_verified` boolean | M1 | R1.3 |
| 4 | Tenant Scoping & Composite FKs | Add `organization_id` and `user_id` to `Client`, `Meeting`, `Commitment` with composite FK to `OrganizationMembership` | M1 | R1.4 |
| 5 | Safe Legacy Migration & Backfill | Single Alembic migration (`down_revision = 'b0da14c0bddb'`) with safe legacy backfill, user check guard, reversible downgrade, and dropped server defaults | M1 | R1.5 |
| 6 | User Session Management | `UserSession` model tracking active org, refresh token hash, device info, and revocation | M1 | R1.6 |
| 7 | Verification & Reset Tokens | `EmailVerificationToken` and `PasswordResetToken` models with expiring token hashes | M1 | R1.7 |
| 8 | Workspace Invitations Model | `WorkspaceInvite` model with expiring token hash and inviter tracking | M1 | R1.8 |
| 9 | Centralized Principal Dependency | `CurrentPrincipal` / `get_current_principal` validating JWT + DB session + active org membership, returning `Principal` dataclass | M2 | R2.1 |
| 10 | Route Security Transition | Replace all `require_api_key` with `get_current_principal`, retire legacy `DEMO_API_KEY` | M2 | R2.2 |
| 11 | Tenant-Scoped Repositories | `ClientRepository`, `MeetingRepository`, `CommitmentRepository` with anti-enumeration 404 security | M2 | R2.3 |
| 12 | ARQ Job Auth Threading | `job_auth_context` utility, worker jobs scoping queries by `meeting_id + org_id + user_id` | M2 | R2.4 |
| 13 | Hardcoded String Eradication | Purge `"org_1"`, `"SYSTEM"`, `"default"`, `"philixa-demo-secret-123"` from all runtime business logic | M2 | R2.5 |
| 14 | Public Auth Endpoints | `/auth/register`, `/auth/verify-email`, `/auth/login`, `/auth/refresh`, `/auth/logout`, `/auth/forgot-password`, `/auth/reset-password` | M3 | R3 |
| 15 | Authenticated Workspace Endpoints | `/auth/me`, `/workspaces`, `/workspaces/switch`, `/workspaces/invite`, `/workspaces/invite/accept`, `/workspaces/members/{id}`, `/workspaces/members/{id}/role` | M3 | R3 |
| 16 | Cookie & CSRF Security | HttpOnly SameSite cookies, CSRF token cookie + header validation middleware on mutating endpoints | M3 | R3 |
| 17 | Production Startup Guardrails | Fail startup on weak `JWT_SECRET`, wildcard `ALLOWED_ORIGINS`, unconfigured SMTP, or non-secure cookies when `PHILIXA_ENV=production` | M3 | R3 |
| 18 | WebSocket Ticket Auth | `POST /api/v1/ws-ticket` (60s TTL) and WebSocket handshake verification with Redis replay prevention in `routes_live.py` | M4 | R4.1 |
| 19 | Namespaced MinIO Audio Storage | Audio stored at `{org_id}/{user_id}/{meeting_id}/{filename}`, `GET /api/v1/audio/{meeting_id}/url` verifies tenant ownership | M4 | R4.2 |
| 20 | Frontend Auth Views & State Machine | Auth overlay with Login, Register (individual vs company), Verify Pending, Forgot/Reset Password, and Invite Accept | M5 | R5.1, R5.2, R5.3 |
| 21 | Frontend API Client & CSRF | Fetch wrapper with `credentials: "include"`, `X-CSRF-Token` header, 401 refresh token retry, and WebSocket ticket flow | M5 | R5.4, R5.7 |
| 22 | Frontend Workspace Switcher & RBAC | Nav workspace dropdown, active role badge, role-based UI action visibility | M5 | R5.5, R5.6 |
| 23 | E2E Test Suite (Tiers 1-4) | Comprehensive test suite covering cryptography, auth flows, multi-tenant 404 isolation, WebSockets, MinIO audio, workspaces | Final | AC |
| 24 | Adversarial Hardening (Tier 5) | White-box coverage analysis and adversarial test cases | Final | AC |

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| M1 | Multi-Org Data Models & Migration | `app/models/`, `alembic/versions/`, `app/database/` (Features 1-8) | none | DONE |
| M2 | Centralized Auth Dependency & Repositories | `app/core/`, `app/repositories/`, `app/jobs/`, string cleanup (Features 9-13) | M1 | DONE |
| M3 | Production Auth & Workspace Endpoints | `app/api/v1/routes_auth.py`, `routes_workspace.py`, CSRF, startup checks (Features 14-17) | M1, M2 | DONE |
| M4 | WebSocket Tickets & Audio Namespacing | `routes_live.py`, `routes_audio.py`, `minio_service.py`, Redis ticket cache (Features 18-19) | M2, M3 | DONE |
| M5 | Frontend Auth UX & Integration | `app/web/index.html`, `app/web/app.js`, `philixa-voice.js` (Features 20-22) | M3, M4 | DONE |
| Final | E2E Verification & Adversarial Hardening | 100% test pass on Tiers 1-4 + Tier 5 adversarial testing (Features 23-24) | M1, M2, M3, M4, M5, TEST_READY | IN_PROGRESS |

## Interface Contracts
### `app/core/dependencies.py` -> All Routes & Services
```python
@dataclass(frozen=True)
class Principal:
    user: User
    organization: Organization
    role: str  # "owner" | "admin" | "member"
    session_id: str

    @property
    def user_id(self) -> str:
        return self.user.id

    @property
    def organization_id(self) -> str:
        return self.organization.id

async def get_current_principal(request: Request, db: AsyncSession = Depends(get_db)) -> Principal:
    ...
```

### `app/repositories/`
```python
class ClientRepository:
    async def list(self, db: AsyncSession, principal: Principal) -> list[Client]: ...
    async def get_by_id(self, db: AsyncSession, principal: Principal, client_id: int) -> Client | None: ...
    async def create(self, db: AsyncSession, principal: Principal, data: dict) -> Client: ...
    async def delete(self, db: AsyncSession, principal: Principal, client_id: int) -> bool: ...

class MeetingRepository:
    async def list(self, db: AsyncSession, principal: Principal, client_id: int | None = None) -> list[Meeting]: ...
    async def get_by_id(self, db: AsyncSession, principal: Principal, meeting_id: int) -> Meeting | None: ...
    async def create(self, db: AsyncSession, principal: Principal, data: dict) -> Meeting: ...

class CommitmentRepository:
    async def list(self, db: AsyncSession, principal: Principal, status: str | None = None, client_id: int | None = None) -> list[Commitment]: ...
    async def get_by_id(self, db: AsyncSession, principal: Principal, commitment_id: int) -> Commitment | None: ...
    async def update_status(self, db: AsyncSession, principal: Principal, commitment_id: int, status: str) -> Commitment | None: ...
```

## Code Layout
- `app/models/`: `enums.py`, `organization.py`, `organization_membership.py`, `user.py`, `user_session.py`, `auth_tokens.py`, `workspace_invite.py`, `client.py`, `meeting.py`, `commitment.py`
- `alembic/versions/`: Existing 13 migrations + `h5c3d4e5f6g7_multi_tenant_auth_and_workspaces.py`
- `app/core/`: `security.py` (password hashing, JWT), `dependencies.py` (`Principal`, `get_current_principal`), `config.py` (auth settings, production validation), `csrf.py` (CSRF validation)
- `app/repositories/`: `client_repository.py`, `meeting_repository.py`, `commitment_repository.py`
- `app/api/v1/`: `routes_auth.py`, `routes_workspace.py`, `routes_clients.py`, `routes_meeting_notes.py`, `routes_commitments.py`, `routes_dashboard.py`, `routes_audio.py`, `routes_live.py`, `routes_voice.py`, `routes_jobs.py`
- `app/jobs/`: `embedding_jobs.py`, `transcription_jobs.py`
- `app/services/`: `minio_service.py`, `ask_client_service.py`, `meeting_processing_service.py`
- `app/web/`: `index.html`, `app.js`, `philixa-voice.js`
- `tests/`: `conftest.py`, `unit/`, `integration/`
