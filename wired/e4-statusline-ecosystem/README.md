# Wired E4 — The statusline ecosystem

Companion files for [Wired E4](https://youtube.com/@noxcraftdev).

## The ceiling

`statusline.py` is the hand-rolled statusline from E3:
color bar, cache hit rate, session cost.
One file. Maintained by hand.
You can't share it — everyone starts from scratch.

## The answer

[Soffit](https://github.com/noxcraftdev/soffit) — a statusline manager for Claude Code.

Install:

```bash
curl -fsSL https://raw.githubusercontent.com/noxcraftdev/soffit/main/install.sh | sh
soffit setup
```

Install a community plugin:

```bash
soffit install noxcraftdev/soffit-marketplace/cache-health
```

Browse available plugins:

```bash
soffit widgets
```

## Writing your own plugin

A plugin is a shell script.
It receives Claude's session JSON on stdin and prints one line.

```bash
#!/usr/bin/env bash
INPUT=$(cat)
COST=$(echo "$INPUT" | python3 -c "
import json,sys; d=json.load(sys.stdin)
print(f'\${(d.get(\"cost\") or {}).get(\"total_cost_usd\", 0):.4f}')
")
echo "cost: $COST"
```

Drop it in `~/.config/soffit/plugins/` or publish it to GitHub and share the install command.
