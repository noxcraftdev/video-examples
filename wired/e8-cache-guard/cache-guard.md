# Cache Guard Rule

A PreToolUse hook blocks edits to cache-sensitive files (CLAUDE.md, settings.json, rules/).
Editing these mid-session invalidates the prompt cache prefix.

## When the hook blocks

1. **User explicitly requested the edit** (e.g., "update CLAUDE.md", "add a rule"):
   bypass immediately and proceed.
   Run the bypass command from the hook output, then retry the edit.

2. **Incidental edit** (you decided to update CLAUDE.md as a side effect):
   defer. Note what needs changing and do it at the very end of the session,
   or suggest the user do it in the next session.
