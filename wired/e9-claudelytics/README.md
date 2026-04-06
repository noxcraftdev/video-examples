# claudelytics: Where Your Claude Budget Goes

A Rust CLI that parses Claude Code's local JSONL session files and breaks down token usage by cache behavior.

## Install

```bash
cargo install claudelytics
```

## Key commands

```bash
claudelytics                     # Today's usage
claudelytics cache               # Cache write breakdown (cold start, TTL miss, churn)
claudelytics cache --top 20      # Top 20 sessions by write cost
claudelytics session             # Per-session usage
claudelytics tui                 # Interactive terminal UI
claudelytics billing-blocks      # 5-hour billing block view
```

## What `cache` shows

- **Cold start**: First turn of every session, unavoidable
- **5m TTL miss**: Short idle, cache expired at 5-minute mark
- **60m TTL miss**: Long idle, cache expired at 60-minute mark
- **Normal churn**: Context changes as conversation grows (~80% of writes)

All data comes from `~/.claude/projects/` JSONL files. No API keys, no cloud, fully local.
