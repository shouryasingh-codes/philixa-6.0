# Original User Request

## Initial Request — 2026-08-23T11:04:27Z

Task Description:
Refactor the PHILIXA 6.0 notification architecture to separate transactional authentication emails (using SMTP) from general application alerts (using WhatsApp).

Requirements:
1. R1. Separate Transactional Auth Notifications: Update backend dependency injection to provide an explicit `EmailAdapter` for auth-related routes (email verification, password resets, workspace invites). This must bypass the global `PHILIXA_NOTIFICATION_MODE` so that auth tokens are always sent via email.
2. R2. Preserve Application Alerts: Ensure that general application alerts (like Audio Upload reminders) continue to use the global notification adapter (which evaluates `PHILIXA_NOTIFICATION_MODE` from the `.env` file to use WhatsApp).
3. Acceptance Criteria / Verification:
- The backend E2E test suite (`tests/e2e/test_real_world_saas_scenarios.py`) must pass completely without errors.
- The registration endpoint must successfully use the `EmailAdapter` and not trigger a WhatsApp API `400 Bad Request` error when an email address is provided.

Note: Use `.venv\Scripts\python.exe -m pytest` for running tests.
