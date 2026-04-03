#!/usr/bin/env bash
# startup_hook.sh -- print Claude Code statusline summary on session start
# Reads context fill % from the session file Claude Code writes.
# Wire this up in settings.json as a SessionStart hook.

SESSION_ID="${CLAUDE_SESSION_ID:-}"
CONTEXT_FILE="/tmp/claude-context-pct-${SESSION_ID}"

if [ -z "$SESSION_ID" ]; then
    echo "[statusline] No session ID -- skipping context summary."
    exit 0
fi

if [ -f "$CONTEXT_FILE" ]; then
    CTX=$(cat "$CONTEXT_FILE")
    if [ "$CTX" -ge 80 ]; then
        STATUS="WARNING: context at ${CTX}% -- consider /handoff"
    elif [ "$CTX" -ge 60 ]; then
        STATUS="context at ${CTX}% -- approaching handoff territory"
    else
        STATUS="context at ${CTX}% -- plenty of room"
    fi
    echo "[statusline] $STATUS"
else
    echo "[statusline] Context file not found (session just started)."
fi
