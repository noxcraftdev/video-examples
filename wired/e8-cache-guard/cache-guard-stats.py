#!/usr/bin/env python3
"""Show cache guard statistics and estimated savings."""

import json
from collections import Counter
from pathlib import Path

LOG_FILE = Path.home() / ".claude" / "logs" / "cache-guard.jsonl"

# Opus pricing per MTok
CACHE_WRITE = 18.75
CACHE_READ = 1.875
COST_DIFF_PER_MTOK = CACHE_WRITE - CACHE_READ

# Conservative estimate of cached system prompt size
ESTIMATED_PREFIX_TOKENS = 20_000


def main() -> None:
    if not LOG_FILE.exists():
        print("No cache guard events yet.")
        return

    events = [json.loads(line) for line in LOG_FILE.read_text().splitlines() if line.strip()]
    if not events:
        print("No cache guard events yet.")
        return

    blocked = [e for e in events if e["action"] == "blocked"]
    bypassed = [e for e in events if e["action"] == "bypassed"]
    prevented = len(blocked) - len(bypassed)

    file_counts = Counter(e["file"].rsplit("/", 1)[-1] for e in events)
    session_counts = Counter(e.get("session", "unknown") for e in events)

    savings = max(0, prevented) * ESTIMATED_PREFIX_TOKENS * COST_DIFF_PER_MTOK / 1_000_000

    print("Cache Guard Stats")
    print("=" * 40)
    print(f"Total events:  {len(events)}")
    print(f"  Blocked:     {len(blocked)}")
    print(f"  Bypassed:    {len(bypassed)}")
    print(f"  Prevented:   {prevented}")
    print()
    print("By file:")
    for name, count in file_counts.most_common():
        print(f"  {name}: {count}")
    print()
    print(f"Across {len(session_counts)} session(s)")
    print()
    print(f"Estimated savings: ${savings:.2f}")
    print(f"  ({ESTIMATED_PREFIX_TOKENS:,} tok prefix x ${COST_DIFF_PER_MTOK}/MTok x {prevented} prevented)")


if __name__ == "__main__":
    main()
