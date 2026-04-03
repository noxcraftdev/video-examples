# e1-pipeline-upgrade

Example from **Wired E1** by [@noxcraftdev](https://github.com/noxcraftdev):
*I Rebuilt My Video Pipeline With Free AI*.

Replace edge-tts with a two-stage local pipeline:
Kokoro generates the base narration, OpenVoice transfers your voice timbre onto it.
Add MusicGen for background tracks.
Everything runs on a gaming GPU. Zero API keys.

## Files

- `generate_voice.py` -- Kokoro + OpenVoice voice pipeline
- `generate_music.py` -- MusicGen background music
- `requirements.txt` -- Python dependencies

## Setup

```bash
pip install -r requirements.txt
```

Download the OpenVoice v2 checkpoints:

```bash
mkdir -p ~/.cache/openvoice
git clone https://huggingface.co/myshell-ai/OpenVoice ~/.cache/openvoice/checkpoints_v2
```

Record a 10-30 second reference clip of your voice (WAV, 16kHz mono works best):

```bash
# Example using sox
rec -r 16000 -c 1 my_voice.wav
```

## Voice generation

```bash
python generate_voice.py \
    --ref my_voice.wav \
    --text "Your narration text here." \
    --out segment.wav
```

This runs two stages:

1. **Kokoro** (`hexgrad/Kokoro-82M`, 82M params) generates a neutral base narration
2. **OpenVoice** transfers your voice timbre onto it at `tau=0.7`

VRAM: ~4 GB. Generation: ~3s per segment on an RTX 2070.

## Music generation

```bash
python generate_music.py \
    --prompt "lo-fi chill ambient" \
    --duration 60 \
    --out background.wav
```

Uses `facebook/musicgen-small` (~300M params).
VRAM: ~2 GB. Generation: ~10s for 60 seconds of audio.

## Stack

| Tool | Role | License |
|------|------|---------|
| [Kokoro](https://github.com/hexgrad/kokoro) | TTS base | Apache 2.0 |
| [OpenVoice](https://github.com/myshell-ai/OpenVoice) | Voice timbre | MIT |
| [asciinema](https://asciinema.org/) | Terminal recording | GPL-3.0 |
| [MusicGen](https://github.com/facebookresearch/audiocraft) | Background music | MIT |
| [MoviePy](https://zulko.github.io/moviepy/) | Assembly | MIT |
