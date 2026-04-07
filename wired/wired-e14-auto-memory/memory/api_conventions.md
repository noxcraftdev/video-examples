---
name: API naming conventions
description: User prefers snake_case for all REST API endpoints and response fields
type: feedback
---

Use snake_case for all API endpoint paths and JSON response field names.

**Why:** User corrected camelCase output twice in early sessions.
Established pattern across the entire API surface.

**How to apply:** When generating API routes, response types, or request schemas,
always use snake_case. This applies to path segments (`/user_profile`),
query params (`?sort_by=`), and JSON keys (`{ "created_at": "..." }`).
