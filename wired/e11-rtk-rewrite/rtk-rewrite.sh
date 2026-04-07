#!/usr/bin/env bash
# PreToolUse hook: transparently rewrite commands through rtk.
# Requires: rtk (https://github.com/rtk-ai/rtk), jq

command -v rtk &>/dev/null || exit 0
command -v jq &>/dev/null || exit 0

INPUT=$(cat)
CMD=$(echo "$INPUT" | jq -r '.tool_input.command // empty')
[ -z "$CMD" ] && exit 0

REWRITTEN=$(rtk rewrite "$CMD" 2>/dev/null) || exit 0
[ "$CMD" = "$REWRITTEN" ] && exit 0

UPDATED=$(echo "$INPUT" | jq -c --arg cmd "$REWRITTEN" '.tool_input.command = $cmd | .tool_input')

jq -n --argjson updated "$UPDATED" '{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow",
    "permissionDecisionReason": "RTK auto-rewrite",
    "updatedInput": $updated
  }
}'
