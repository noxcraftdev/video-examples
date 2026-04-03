# statusline-decoded

Example from **Wired E3** by [@noxcraftdev](https://github.com/noxcraftdev).

The Claude Code statusline shows context fill %, session cost, active model,
and hook count at the bottom of every session.
This example adds a SessionStart hook that echoes a plain-language summary
of what the statusline is telling you.

## Files

- `CLAUDE.md` -- explains what the statusline shows + hook setup instructions
- `startup_hook.sh` -- reads context fill % and prints a status summary

## Quick start

```bash
git clone https://github.com/noxcraftdev/video-examples
cd video-examples/wired/statusline-decoded
bash startup_hook.sh
```

Then wire `startup_hook.sh` into your `settings.json` as a `SessionStart` hook
(see `CLAUDE.md` for the exact config).

## What you get

Every Claude Code session starts with:

```
[statusline] context at 47% -- plenty of room
```

or, when you're getting close:

```
[statusline] WARNING: context at 83% -- consider /handoff
```
