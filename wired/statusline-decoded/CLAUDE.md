# statusline-decoded

Example from Wired E3: The Claude Code Statusline, Decoded.

## What this does

Wires a SessionStart hook that reads the current context fill %
and echoes a status summary at the start of every session.

## Hook setup

Add this to your `~/.claude/settings.json`:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash /path/to/startup_hook.sh"
          }
        ]
      }
    ]
  }
}
```

## What the statusline shows

The bar at the bottom of every Claude Code session tracks:

- **Context fill %** -- how full the active window is.
  At 80%, auto-handoff rules trigger -- starting fresh is cheaper.
- **Session cost** -- real spend in USD, updated every turn.
- **Model** -- which model is active. Switches silently with /fast or subagents.
- **Hooks** -- count of active hooks. Non-zero means something runs on every tool call.
