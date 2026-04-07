# RTK Rewrite Hook

A PreToolUse hook that transparently rewrites Claude Code's bash commands through [rtk](https://github.com/rtk-ai/rtk).

RTK strips noise from command output, reducing token usage by 60-90% without changing behavior.

## How it works

1. Claude issues a bash command (e.g., `git status`)
2. The PreToolUse hook intercepts it before execution
3. The hook rewrites it to `rtk git status`
4. RTK runs the command, strips boilerplate, returns compressed output
5. Claude sees clean, compact output and responds normally

## Setup

1. Install rtk: `cargo install rtk` or see [installation docs](https://github.com/rtk-ai/rtk#installation)
2. Install jq: `sudo apt install jq`
3. Copy `rtk-rewrite.sh` to `~/.claude/hooks/`
4. Add the hook entry from `settings-snippet.json` to your `~/.claude/settings.json`
5. Check savings: `rtk gain`
