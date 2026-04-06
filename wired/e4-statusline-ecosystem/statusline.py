#!/usr/bin/env python3
import json, sys

data = json.load(sys.stdin)
cw = data.get("context_window", {})
ctx_pct = cw.get("used_percentage", 0)
cost = (data.get("cost") or {}).get("total_cost_usd", 0)

usage = cw.get("current_usage", {})
cache_reads = usage.get("cache_read_input_tokens", 0)
cache_total = cache_reads + usage.get("cache_creation_input_tokens", 0)
hit = round(cache_reads / cache_total * 100) if cache_total else 0

color = "\033[32m" if ctx_pct < 70 else "\033[33m" if ctx_pct < 90 else "\033[31m"
reset = "\033[0m"
blocks = int(ctx_pct / 10)
bar = "█" * blocks + "░" * (10 - blocks)
print(f"{color}{bar}{reset} {ctx_pct}% | ↩{hit}% | ${cost:.3f}")
