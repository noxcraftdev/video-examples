---
name: Auth middleware rewrite context
description: Auth rewrite is compliance-driven (session token storage), not tech debt cleanup.
type: project
---

Auth middleware rewrite is driven by legal/compliance requirements
around session token storage, not tech-debt cleanup.

**Why:** Legal flagged the old middleware for storing session tokens
in a way that doesn't meet new compliance requirements.

**How to apply:** Scope decisions should favor compliance over ergonomics.
Don't expand the rewrite into general auth improvements unless they're
required for compliance.
