#!/usr/bin/env python3
import json, sys

d     = json.load(sys.stdin)
cw    = d.get("context_window") or {}
ctx   = cw.get("used_percentage") or 0
cost  = (d.get("cost") or {}).get("total_cost_usd") or 0
name  = (d.get("model") or {}).get("display_name") or "?"

usage     = cw.get("current_usage") or {}
cr        = usage.get("cache_read_input_tokens") or 0
cn        = usage.get("cache_creation_input_tokens") or 0
hit_rate  = cr / (cr + cn) if (cr + cn) else None

parts = [f"ctx {ctx:.0f}%", f"${cost:.3f}", name]
if hit_rate is not None: parts.append(f"\u21a9{hit_rate*100:.0f}% hit")
print(" | ".join(parts))

