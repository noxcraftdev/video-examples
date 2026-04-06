#!/usr/bin/env python3
import json, sys, os, time

json.load(sys.stdin)
state = "/tmp/soffit-cache-timer"

if not os.path.exists(state):
    open(state, "w").write(str(time.time()))

mins = int((time.time() - float(open(state).read())) / 60)
cold = mins >= 5
color = "\033[38;5;203m" if cold else "\033[38;5;114m"
label = "COLD" if cold else "warm"
print(f"{color}{label}\033[0m · {mins}m")
