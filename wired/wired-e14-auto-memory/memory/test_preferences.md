---
name: Integration test preferences
description: User wants real database in tests, not mocks. Prior incident with mock/prod divergence.
type: feedback
---

Integration tests must hit a real database, not mocks.

**Why:** A mocked test suite passed while a production migration failed.
The mock diverged from actual database behavior and masked the bug.

**How to apply:** When writing tests that touch data persistence,
use the test database container defined in `docker-compose.test.yml`.
Reserve mocks for external third-party APIs only.
