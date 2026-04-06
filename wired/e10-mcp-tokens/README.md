# MCP Token Bloat: The Fix

Every MCP server registers its tools into Claude Code's system prompt. More servers = more tokens per turn, even when you don't use those tools.

## The problem

4 MCP servers can add ~67K tokens to every turn. You pay for all of them on every API call.

## The fix

Add `"toolSearch": true` to your `~/.claude/settings.json`. This enables lazy loading: Claude only injects tool schemas when they're relevant to the current prompt.

## Result

67K tokens down to ~3.5K. 95% reduction. Same servers, same tools, same capability.

## Before vs After

- `settings-before.json` -- standard MCP config (all tools loaded every turn)
- `settings-after.json` -- with `toolSearch: true` (lazy loading)
