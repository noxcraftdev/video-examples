# Auto-Memory Example

Claude Code automatically writes observations about your project to a memory directory.
Each file captures one thing: a preference, a decision, project context.

## How it works

1. You mention something during a session ("we use snake_case for endpoints")
2. Claude writes a memory file to `~/.claude/projects/<project>/memory/`
3. `MEMORY.md` indexes all memory files with one-line summaries
4. Next session, Claude reads the index on startup and recalls what matters

## Structure

```
memory/
  api_conventions.md      # feedback: snake_case preference
  test_preferences.md     # feedback: real DB, no mocks
  project_auth_rewrite.md # project: compliance context
MEMORY.md                 # index loaded every session
```

## Memory types

- **user** -- role, preferences, expertise level
- **feedback** -- corrections and confirmed approaches
- **project** -- ongoing work, decisions, deadlines
- **reference** -- pointers to external systems

## What it doesn't save

- Code patterns (read the code)
- Git history (use git log)
- Debug fixes (the fix is in the commit)
- Anything in CLAUDE.md (already loaded)
