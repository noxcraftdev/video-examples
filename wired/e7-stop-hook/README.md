# Stop Hook: Verification by Default

A Claude Code Stop hook that blocks the session from ending when code has changed but no build or test commands ran.

## How it works

The hook reads the session transcript and checks three things:

1. Are there uncommitted git changes?
2. Does the repo have a build system (Cargo.toml, package.json, etc.)?
3. Did the transcript contain any test/build commands?

If changes exist but no verification ran, the hook blocks the exit and tells Claude to run tests first.

## Install

1. Copy `stop-verify.sh` somewhere on your PATH (or any fixed location)
2. Make it executable: `chmod +x stop-verify.sh`
3. Add the hook entry to `~/.claude/settings.json` (see `settings-snippet.json`)
4. Requires `jq` for JSON parsing

## Escape hatch

For research, planning, or docs-only sessions, say "non-code session" in the conversation. The hook detects it and allows the exit.
