# E2E Test Infra: PHILIXA 6.0 Multi-Tenant SaaS Auth & Workspaces

## Test Philosophy
- **Opaque-box & Requirement-driven**: Tests derive from user requirements in `ORIGINAL_REQUEST.md`, not internal implementation details.
- **Methodology**: Systematic Category-Partition, Boundary Value Analysis (BVA), Pairwise Cross-Feature Matrix, and Real-World SaaS Workload Scenarios.
- **Database Backend**: Real PostgreSQL async test client (`pytest-asyncio` + `httpx.AsyncClient`). Zero reliance on SQLite for tenant isolation verification.

## Feature Inventory & Test Coverage Mapping
| # | Feature Area | Requirement | Tier 1 (Unit) | Tier 2 (Boundary) | Tier 3 (Cross-Feature) | Tier 4 (Scenario) |
|---|--------------|-------------|:-------------:|:-----------------:|:----------------------:|:-----------------:|
| 1 | Cryptography & Passwords | R3, Security | ≥5 | ≥5 | ✓ | ✓ |
| 2 | JWT HS256 & Session Claims | R3, Security | ≥5 | ≥5 | ✓ | ✓ |
| 3 | CSRF Protection & Cookies | R3, Security | ≥5 | ≥5 | ✓ | ✓ |
| 4 | Production Startup Validation | R3, Config | ≥5 | ≥5 | ✓ | ✓ |
| 5 | Registration & Email Verify | R3, Auth | ≥5 | ≥5 | ✓ | ✓ |
| 6 | Login & Session Lifecycle | R3, Auth | ≥5 | ≥5 | ✓ | ✓ |
| 7 | Password Reset & Token Hash | R3, Auth | ≥5 | ≥5 | ✓ | ✓ |
| 8 | Workspace Management & Invites | R3, Workspaces | ≥5 | ≥5 | ✓ | ✓ |
| 9 | Multi-Tenant Data Isolation (404) | R2, Repositories | ≥5 | ≥5 | ✓ | ✓ |
| 10 | Role-Based Record Scoping | R2, RBAC | ≥5 | ≥5 | ✓ | ✓ |
| 11 | WebSocket Ticket & Replay | R4, WS | ≥5 | ≥5 | ✓ | ✓ |
| 12 | Namespaced MinIO Audio Storage | R4, Audio | ≥5 | ≥5 | ✓ | ✓ |

## Test Architecture
- **Test Runner**: `python -m pytest tests/ -v`
- **Fixtures (`tests/conftest.py`)**:
  - `db_session`: Async SQLAlchemy session connected to PostgreSQL test database.
  - `async_client`: `httpx.AsyncClient(app=app, base_url="http://test")` with cookie jar support.
  - `mock_smtp`: In-memory email sink intercepting verification tokens and invite links.
  - `mock_redis`: In-memory or test Redis instance for token/ticket TTL and replay tests.
  - `tenant_matrix`: Pre-configured Org A (Owner A1, Member A2) and Org B (Owner B1) test fixtures.
- **Directory Layout**:
  - `tests/unit/test_security_crypto.py`: Bcrypt cost factor, JWT HS256 claims/tampering, CSRF validation, production startup config checks.
  - `tests/integration/test_auth_flow.py`: Registration, email verification, login, cookie setting, refresh rotation, logout, password reset.
  - `tests/integration/test_workspace_management.py`: Workspace switcher, member invitations, invite acceptance, role changes, member revocation.
  - `tests/integration/test_tenant_isolation.py`: Cross-tenant 404 security across clients, meetings, commitments, dashboard, search, and ARQ background jobs.
  - `tests/integration/test_websocket_audio_security.py`: WebSocket ticket issuance, handshake, Redis replay rejection, MinIO namespaced audio presigned URLs.
  - `tests/e2e/test_real_world_saas_scenarios.py`: End-to-end multi-tenant lifecycle scenarios.

## Real-World Application Scenarios (Tier 4)
| # | Scenario | Features Exercised | Complexity |
|---|----------|--------------------|------------|
| 1 | Company Multi-User Onboarding | Register Company Org -> Invite Admin & Member -> Accept Invites -> Verify Member Scoping vs Admin View | High |
| 2 | Multi-Tenant Cross-Contamination Attack | Org B user attempts to read, modify, and delete Org A clients, meetings, audio files, and commitments | High |
| 3 | Session Revocation & Concurrent Devices | Login on Device 1 & Device 2 -> Revoke Device 1 Session -> Verify Device 1 gets 401 while Device 2 remains active | Medium |
| 4 | Token Refresh & Replay Defense | Active user session refreshes -> Attempt reuse of old refresh token -> Verify old token fails and is revoked | Medium |
| 5 | End-to-End WebSocket Meeting Transcription | Login -> Request WS ticket -> Connect live WebSocket -> Send audio/transcribe -> Disconnect -> Replay ticket rejected | High |
| 6 | Workspace Switching & Context Scoping | User with multiple memberships switches active workspace -> Verify subsequent queries scope strictly to new workspace | Medium |

## Coverage Thresholds
- Tier 1: ≥60 unit test cases (≥5 per feature area)
- Tier 2: ≥60 boundary/error test cases (≥5 per feature area)
- Tier 3: ≥20 pairwise cross-feature integration test cases
- Tier 4: ≥6 realistic multi-tenant SaaS application scenarios
- **Total Minimum Target**: ≥146 automated test cases
