# power-statusline

A ~40-line Python statusline for Claude Code.
Builds on the [hidden-statusbar](../e2-hidden-statusbar/) example from Wired E2.

## What it shows

```
[████░░░░] 47% │ $0.041 │ claude-sonnet-4-6 │ ↩82% │ ◷ 34% · resets 14m
```

| field | source |
|-------|--------|
| Context bar | `context_window.used_percentage` — green → yellow (70%) → red (90%) |
| Cost | `cost.total_cost_usd` |
| Model | `model.display_name` |
| Cache hit rate | `cache_read / (cache_read + cache_creation)` — hidden if zero |
| Rate limit | `rate_limits.five_hour.used_percentage` + time until `resets_at` |

## Install

```bash
cp statusline.py ~/.claude/statusline.py
```

Add to `~/.claude/settings.json`:

```json
{
  "statusLine": {
    "type": "command",
    "command": "python3 ~/.claude/statusline.py"
  }
}
```

## Test offline

```bash
cat sample_payload.json | python3 statusline.py
```
