# Claude Code Statusline

A minimal Python script that turns on Claude Code's built-in status bar.

## What it shows

```
ctx 47% | $0.180 | claude-sonnet-4-6
```

- **ctx %** -- how full your context window is
- **$cost** -- running session cost in USD
- **model name** -- which model is actually running
- **↩Nk cache** -- cache read tokens (appears after the first cached turn)

## Setup

1. Copy `statusline.py` to `~/.claude/statusline.py`
2. Add this to `~/.claude/settings.json`:

```json
{
  "statusLine": {
    "command": "python3 ~/.claude/statusline.py"
  }
}
```

3. Restart Claude Code. The bar appears at the bottom of every session.

## How it works

Claude Code pipes a JSON blob to your `statusLine.command` on every turn.
The script reads it from stdin and prints one line of text.
That line becomes the status bar.

Full JSON schema: [Claude Code docs -- statusLine](https://docs.anthropic.com/en/docs/claude-code/settings)
