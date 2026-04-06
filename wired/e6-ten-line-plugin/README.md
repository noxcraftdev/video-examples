# my-widget — session phase + cost tracker

A 10-line soffit plugin that shows your session phase (early/mid/late) and running cost.

## Install

```bash
cp my-widget.py ~/.config/soffit/plugins/
chmod +x ~/.config/soffit/plugins/my-widget.py
```

Or via soffit:

```bash
soffit install noxcraftdev/video-examples/wired/e6-ten-line-plugin/my-widget
```

## How it works

Soffit sends JSON to stdin with session data (cost, context window %, model, etc.).
The script reads it, picks a phase based on context fill, and prints one line to stdout.
That line appears in the Claude Code status bar.

## The interface

- **Input**: JSON on stdin (see [soffit docs](https://github.com/noxcraftdev/soffit))
- **Output**: plain text to stdout (or JSON with `{"output": "..."}`)
- **Timeout**: 200ms — keep it fast
