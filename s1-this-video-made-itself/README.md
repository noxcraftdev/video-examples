# S1: This Video Made Itself

A zero-cost video production pipeline for YouTube Shorts.
Renders terminal frames and title cards with Pillow, generates narration with edge-tts, and assembles everything into an MP4 with MoviePy.

## What's here

| File | Purpose |
|------|---------|
| `make_assets.py` | Renders PNGs -- terminal frames (Dracula palette) and title cards |
| `assemble.py` | Stitches PNGs + MP3s + SRTs into a final MP4 with burned subtitles |
| `requirements.txt` | Python dependencies |

## Quick start

```bash
# Set up
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Generate visuals
python make_assets.py --output-dir ./assets

# Generate narration (replace with your own text)
edge-tts --voice en-US-AndrewMultilingualNeural --rate "+5%" \
  --text "Your narration here." \
  --write-media ./audio/segment.mp3 \
  --write-subtitles ./srt/segment.srt

# Assemble
python assemble.py \
  --assets-dir ./assets \
  --audio-dir ./audio \
  --srt-dir ./srt \
  --output ./output.mp4
```

## Customization

- Edit `make_assets.py` to change text, colors, and layout per segment
- Edit the `SEGMENTS` list in `assemble.py` to match your segment names
- Swap voices: `edge-tts --list-voices` to see all available options
- Change resolution: modify `W, H` in both scripts (default: 1080x1920 for Shorts)

## Dependencies

- **edge-tts**: Free text-to-speech via Microsoft Edge (no API key needed)
- **Pillow**: Image rendering for terminal frames and title cards
- **MoviePy 2.x**: Video assembly with subtitle compositing
- **ffmpeg**: Required by MoviePy (install via `apt install ffmpeg` or `brew install ffmpeg`)
- **DejaVu fonts**: Used for terminal rendering (standard on most Linux distros)

## Cost

$0. Edge-tts is free. Pillow and MoviePy are open source. No API keys, no subscriptions.
