# Session Recovery

When a Claude Code session crashes (rate limit, API error, OOM), your work isn't lost.
Every session is saved as a JSONL file on disk.

## How it works

1. Claude Code writes every conversation turn to a JSONL file
2. Files live at `~/.claude/projects/<hash>/sessions/<id>.jsonl`
3. When a session crashes, the file stays on disk
4. New session + one prompt = full context recovery

## Recovery in 30 seconds

```bash
# Find the crashed session
ls -lt ~/.claude/projects/*/sessions/*.jsonl | head -5

# Start a new Claude Code session, then:
# "Read this file and continue where I left off: <path>"
```

## What's saved

- Your messages and instructions
- Claude's responses and reasoning
- Every tool call (file reads, edits, bash commands)
- Tool results (file contents, command output)

## Example

See `sample-session.jsonl` for a sanitized example of what a session file looks like.
See `recovery-prompt.md` for the exact prompt pattern.
