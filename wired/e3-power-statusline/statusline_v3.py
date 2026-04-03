#!/usr/bin/env python3
import json, sys
from datetime import datetime, timezone

R = "\033[31m" Y = "\033[33m" G = "\033[32m"
C = "\033[36m" D = "\033[2m"  X = "\033[0m"

def bar(pct, width=8):
    filled = round(pct / 100 * width)
    b = "\u2588" * filled + "\u2591" * (width - filled)
    color = R if pct >= 90 else Y if pct >= 70 else G
    return f"{color}[{b}]{X}"

d    = json.load(sys.stdin)
cw   = d.get("context_window") or {}
ctx  = cw.get("used_percentage") or 0
cost = (d.get("cost") or {}).get("total_cost_usd") or 0
name = (d.get("model") or {}).get("display_name") or "?"

usage = cw.get("current_usage") or {}
cr    = usage.get("cache_read_input_tokens") or 0
cn    = usage.get("cache_creation_input_tokens") or 0
hit   = cr / (cr + cn) if (cr + cn) else None

rl     = (d.get("rate_limits") or {}).get("five_hour") or {}
rl_pct = rl.get("used_percentage") or 0
resets = rl.get("resets_at")
rs = ""
if resets:
    try:
        t = datetime.fromisoformat(resets.replace("Z","+00:00"))
        m = max(0,int((t-datetime.now(timezone.utc)).total_seconds()/60))
        rs = f" \u00b7 resets {m}m"
    except: pass

c_pct = R if ctx>=90 else Y if ctx>=70 else G
parts = [f"{bar(ctx)} {c_pct}{ctx:.0f}%{X}", f"{D}\${cost:.3f}{X}", f"{C}{name}{X}"]
if hit: parts.append(f"\u21a9{hit*100:.0f}%")
if rl_pct:
    rc = R if rl_pct>=90 else Y if rl_pct>=70 else D
    parts.append(f"{rc}\u25f7 {rl_pct:.0f}%{rs}{X}")
print(" \u2502 ".join(parts))

