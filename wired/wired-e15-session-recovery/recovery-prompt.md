# Session Recovery Prompt

When a Claude Code session crashes, use this prompt in a new session:

```
Read this session file and continue where I left off:
~/.claude/projects/<project-hash>/sessions/<session-id>.jsonl
```

## Finding the right file

```bash
# List recent sessions, newest first
ls -lt ~/.claude/projects/*/sessions/*.jsonl | head -5

# Check the last few lines to confirm it's the right session
tail -3 ~/.claude/projects/<project-hash>/sessions/<session-id>.jsonl
```

## What's in the file

Each line is a JSON object representing one conversation turn:
- `type: "human"` -- your messages
- `type: "assistant"` -- Claude's responses and tool calls
- `type: "tool_result"` -- results from file reads, edits, bash commands

The file contains everything: your instructions, Claude's plan, which files were read/modified, and where the work stopped.
