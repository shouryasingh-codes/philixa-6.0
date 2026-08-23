# PHILIXA 6.0 — Multi-Tenant SaaS Test Suite (E2E & Integration Ready)

## Overview
The automated test infrastructure for **PHILIXA 6.0** is fully configured and ready for multi-tier verification. It enforces strict opaque-box requirement validation across all security, authentication, workspace management, tenant isolation, and streaming media capabilities.

---

## Test Architecture & Tier Breakdown

### Tier 1: Security & Cryptography Unit Tests
- **Location**: `tests/unit/test_security_crypto.py`
- **Features Tested**:
  - Bcrypt password hashing: cost factor $\ge 12$, unique salt per hash, correct/incorrect verification, plaintext rejection, Unicode & emoji resilience.
  - JWT HS256 token operations: header verification (`alg=HS256`, `typ=JWT`), mandatory claims validation (`sub`, `sid`, `org_id`, `role`, `iat`, `exp`, `jti`), expired token rejection, tampered payload rejection, tampered signature rejection, wrong secret key rejection, alg "none" attack rejection.
  - CSRF protection: cryptographic token entropy, double-submit cookie validation, mutating methods (`POST`, `PUT`, `PATCH`, `DELETE`) enforcement, safe methods (`GET`, `HEAD`, `OPTIONS`) bypass.
  - Production startup guardrails (`PHILIXA_ENV=production`): fails on missing/weak `JWT_SECRET`, fails on wildcard CORS (`*`), fails on missing `SMTP_USERNAME`, passes when all constraints are satisfied.

### Tier 2: Authentication & Workspace Lifecycle Integration Tests
- **Location**: `tests/integration/test_auth_flow.py`, `tests/integration/test_workspace_management.py`
- **Features Tested**:
  - Registration: `POST /auth/register` creating User, Organization, Owner membership, and single-use `EmailVerificationToken`. Rejects duplicate emails and invalid workspace types.
  - Verification: `POST /auth/verify-email?token=...` marking user verified, rejecting expired, reused, or invalid tokens.
  - Login: `POST /auth/login` setting HttpOnly cookies (`access_token`, `refresh_token`), non-HttpOnly `csrf_token` cookie, rejecting unverified or incorrect password attempts.
  - Session Profile: `GET /auth/me` returning authenticated user profile, active workspace, and memberships list.
  - Refresh Token Rotation: `POST /auth/refresh` revoking previous session, issuing new token pair, detecting and blocking replay attacks.
  - Logout: `POST /auth/logout` revoking session in DB and clearing cookie state.
  - Password Reset: `POST /auth/forgot-password` and `POST /auth/reset-password` token handling, password rotation, anti-enumeration.
  - Workspace Listing & Switching: `GET /workspaces`, `POST /workspaces/switch` with session updates and unauthorized switch defense.
  - Workspace Invitations: `POST /workspaces/invite` (owner/admin only, member blocked), `POST /workspaces/invite/accept`, single-use expiring invite tokens.
  - Member Role & Access Control: `PATCH /workspaces/members/{id}/role` (owner only), `DELETE /workspaces/members/{id}`.

### Tier 3: Multi-Tenant Data Isolation Tests
- **Location**: `tests/integration/test_tenant_isolation.py`
- **Features Tested**:
  - Strict Cross-Tenant Anti-Enumeration (HTTP 404): Org A users querying, updating, or deleting Org B clients, meetings, memory summaries, or commitments receive HTTP 404 with zero information leakage.
  - Role-Based Record Ownership (RBAC within same org): Member A2 querying Owner A1's records receives HTTP 404. Owner A1 querying Member A2's records receives HTTP 200 OK.
  - Tenant Scoping on Listings & Aggregations: `GET /api/v1/clients`, `GET /api/v1/commitments`, `GET /api/v1/dashboard/metrics` filtered strictly by active organization ID and user ID.
  - Client Auto-Matching Isolation: Meeting processing in Org A never auto-matches or updates records in Org B.

### Tier 4: WebSocket, Audio & Real-World E2E Scenarios
- **Location**: `tests/integration/test_websocket_audio_security.py`, `tests/e2e/test_real_world_saas_scenarios.py`
- **Features Tested**:
  - WebSocket Ticket Authentication: `POST /api/v1/ws-ticket` 60s TTL ticket issuance, unauthenticated rejection.
  - Redis Replay Prevention: Single-use ticket redemption in Redis, second connection attempt blocked.
  - MinIO Audio Storage Namespacing: Objects stored under `{organization_id}/{user_id}/{meeting_id}/{filename}` format; presigned URL generation enforces tenant ownership (404 for cross-tenant).
  - Scenario 1: Multi-user company onboarding and role-based isolation.
  - Scenario 2: Multi-tenant cross-contamination IDOR attack defense.
  - Scenario 3: Session revocation and multi-device concurrency.
  - Scenario 4: Refresh token rotation and replay defense.
  - Scenario 5: WebSocket meeting processing and memory scoping.
  - Scenario 6: Workspace switching and context scoping.

---

## Test Execution Commands

### Run Full Test Suite
```bash
python -m pytest tests/ -v
```

### Run Tier 1 (Security & Crypto Unit Tests)
```bash
python -m pytest tests/unit/test_security_crypto.py -v
```

### Run Tier 2 (Auth & Workspace Integration Tests)
```bash
python -m pytest tests/integration/test_auth_flow.py tests/integration/test_workspace_management.py -v
```

### Run Tier 3 (Multi-Tenant Isolation Tests)
```bash
python -m pytest tests/integration/test_tenant_isolation.py -v
```

### Run Tier 4 (WebSocket, Audio & Real-World Scenarios)
```bash
python -m pytest tests/integration/test_websocket_audio_security.py tests/e2e/test_real_world_saas_scenarios.py -v
```

---

## Fixture Inventory (`tests/conftest.py`)
- `async_db_session`: Async SQLAlchemy session connected to async test engine with automatic schema creation and teardown.
- `async_client`: `httpx.AsyncClient` with ASGI transport, cookie jar support, and automatic cookie preservation.
- `mock_smtp`: In-memory email sink intercepting verification tokens, invite links, and password reset tokens.
- `mock_redis`: In-memory async Redis simulator tracking token TTLs, ticket redemptions, and replay prevention.
- `tenant_matrix`: Standardized matrix for Org A (Owner A1, Member A2) and Org B (Owner B1, Member B2).
- `auth_factory`: Utility for minting pre-authenticated clients for any user/role.
- `client_app` & `api_headers`: Backward compatibility fixtures ensuring legacy tests continue to pass.
