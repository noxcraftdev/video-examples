#!/usr/bin/env python3
"""
my-widget: shows session phase and running cost in one field.
Reads Claude Code status JSON on stdin, prints one line on stdout.
That's the whole interface.
"""
import json, sys

data = json.load(sys.stdin)

cost = (data.get("cost") or {}).get("total_cost_usd", 0)
ctx  = data.get("context_window", {}).get("used_percentage", 0)

if ctx < 40:
    phase = "early"
elif ctx < 75:
    phase = "mid"
else:
    phase = "late"

print(f"{phase} · ${cost:.3f}")
