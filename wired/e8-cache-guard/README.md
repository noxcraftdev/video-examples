# Cache Guard: Protect Your Prompt Cache

A Claude Code PreToolUse hook that blocks mid-session edits to cache-sensitive files (CLAUDE.md, settings.json, rules/).

## Why

These files are baked into the prompt cache prefix. Editing one mid-session forces a full cache rebuild -- roughly $0.34 per invalidation on Opus with a 20K token prefix. This hook catches it before it happens.

## How it works

1. Every Edit/Write tool call is checked against a sensitive file list
2. Match? The edit is blocked and a one-time bypass key is printed
3. Run the printed `touch` command to create the bypass, then retry
4. The bypass is consumed (single-use) and the event is logged to JSONL

## Install

1. Copy `cache-guard.py` somewhere on your PATH
2. Add the hook entry to `~/.claude/settings.json` (see `settings-snippet.json`)
3. Optionally, copy `cache-guard.md` to `.claude/rules/` so Claude knows when to bypass vs defer
4. Run `python3 cache-guard-stats.py` to see cumulative savings
