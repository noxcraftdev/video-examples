#!/usr/bin/env python3
import json, sys
from datetime import datetime, timezone

# ── ANSI color helpers ────────────────────────────────────────────────────────
R = "\033[31m"
Y = "\033[33m"
G = "\033[32m"
C = "\033[36m"
D = "\033[2m"
X = "\033[0m"

def bar(pct, width=8):
    filled = round(pct / 100 * width)
    b = "█" * filled + "░" * (width - filled)
    if pct >= 90: color = R
    elif pct >= 70: color = Y
    else: color = G
    return f"{color}[{b}]{X}"

def color_pct(pct):
    if pct >= 90: return f"{R}{pct:.0f}%{X}"
    elif pct >= 70: return f"{Y}{pct:.0f}%{X}"
    return f"{G}{pct:.0f}%{X}"

# ── Parse payload ─────────────────────────────────────────────────────────────
d    = json.load(sys.stdin)
cw   = d.get("context_window") or {}
ctx  = cw.get("used_percentage") or 0
cost = (d.get("cost") or {}).get("total_cost_usd") or 0
name = (d.get("model") or {}).get("display_name") or "?"

usage = cw.get("current_usage") or {}
cache_read = usage.get("cache_read_input_tokens") or 0
cache_new  = usage.get("cache_creation_input_tokens") or 0
cache_total = cache_read + cache_new
cache_hit = cache_read / cache_total if cache_total else None

rl      = (d.get("rate_limits") or {}).get("five_hour") or {}
rl_pct  = rl.get("used_percentage") or 0
resets  = rl.get("resets_at")

# ── Format resets_at → "Xm" ──────────────────────────────────────────────────
resets_str = ""
if resets:
    try:
        t = datetime.fromisoformat(resets.replace("Z", "+00:00"))
        mins = max(0, int((t - datetime.now(timezone.utc)).total_seconds() / 60))
        resets_str = f" · resets {mins}m"
    except Exception:
        pass

# ── Assemble parts ────────────────────────────────────────────────────────────
parts = [f"{bar(ctx)} {color_pct(ctx)}", f"{D}${cost:.3f}{X}", f"{C}{name}{X}"]

if cache_hit is not None:
    parts.append(f"↩{cache_hit*100:.0f}%")

if rl_pct:
    rl_color = R if rl_pct >= 90 else Y if rl_pct >= 70 else D
    parts.append(f"{rl_color}◷ {rl_pct:.0f}%{resets_str}{X}")

print(" │ ".join(parts))
