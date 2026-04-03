#!/usr/bin/env python3
import json, sys

d = json.load(sys.stdin)
ctx   = d.get("context_window", {}).get("used_percentage", 0)
cost  = d.get("cost", {}).get("total_cost_usd", 0)
name  = d.get("model", {}).get("display_name", "?")
cache = d.get("context_window", {}).get("current_usage", {}).get("cache_read_input_tokens", 0)

parts = [f"ctx {ctx:.0f}%", f"${cost:.3f}", name]
if cache:
    parts.append(f"\u21a9{cache // 1000}k cache")
print(" | ".join(parts))
