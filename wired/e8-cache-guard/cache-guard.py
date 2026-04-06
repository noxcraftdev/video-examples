#!/usr/bin/env python3
"""PreToolUse hook: blocks edits to cache-sensitive files mid-session.

Cache-sensitive files (CLAUDE.md, settings.json, rules/) are baked into the
prompt cache prefix. Editing them mid-session invalidates the cache, forcing
a full re-creation on the next API call (~$0.34 per invalidation for a 20k
token prefix on Opus).

Bypass: create /tmp/cache-guard-bypass/<key> where <key> is printed in the
blocked message. The bypass is single-use (deleted after consumption).
"""

import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

CACHE_SENSITIVE = [
    "CLAUDE.md",
    ".claude/settings.json",
    ".claude/settings.local.json",
    ".claude/rules/",
]

LOG_FILE = Path.home() / ".claude" / "logs" / "cache-guard.jsonl"
BYPASS_DIR = Path("/tmp/cache-guard-bypass")


def is_cache_sensitive(fp: str) -> bool:
    return any(p in fp for p in CACHE_SENSITIVE)


def bypass_key(fp: str) -> str:
    return hashlib.sha256(fp.encode()).hexdigest()[:16]


def check_bypass(fp: str) -> bool:
    key_file = BYPASS_DIR / bypass_key(fp)
    if key_file.exists():
        key_file.unlink()
        return True
    return False


def log_event(fp: str, action: str) -> None:
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    event = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "file": fp,
        "action": action,
        "session": os.environ.get("CLAUDE_SESSION_ID", "unknown"),
    }
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(event) + "\n")


def main() -> None:
    data = json.load(sys.stdin)
    fp = data.get("tool_input", {}).get("file_path", "")

    if not fp or not is_cache_sensitive(fp):
        return

    if check_bypass(fp):
        log_event(fp, "bypassed")
        return

    key = bypass_key(fp)
    log_event(fp, "blocked")
    print(f"CACHE GUARD: Editing `{fp}` invalidates the prompt cache for this session.")
    print(f"Bypass: `mkdir -p /tmp/cache-guard-bypass && touch /tmp/cache-guard-bypass/{key}`")
    sys.exit(1)


if __name__ == "__main__":
    main()
