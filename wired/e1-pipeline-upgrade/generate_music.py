#!/usr/bin/env python3
"""MusicGen background music generator from Wired E1.

Generates lo-fi background music locally using facebook/musicgen-small.
No API keys. VRAM: ~2 GB. RTX 2070 generates 60s in ~10s.

Usage:
    python generate_music.py --prompt "lo-fi chill ambient" --duration 60 --out background.wav
"""

import argparse

import scipy.io.wavfile
import torch
from transformers import AutoProcessor, MusicgenForConditionalGeneration


def generate(prompt, duration_seconds, out_path, device="cuda"):
    print(f"Loading facebook/musicgen-small...")
    processor = AutoProcessor.from_pretrained("facebook/musicgen-small")
    model = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-small")
    model = model.to(device)

    sampling_rate = model.config.audio_encoder.sampling_rate
    # musicgen-small generates 50 tokens/s at 32kHz
    max_new_tokens = int(duration_seconds * 50)

    inputs = processor(text=[prompt], padding=True, return_tensors="pt").to(device)

    print(f"Generating {duration_seconds}s of audio...")
    with torch.no_grad():
        audio_values = model.generate(**inputs, max_new_tokens=max_new_tokens)

    audio = audio_values[0, 0].cpu().numpy()

    scipy.io.wavfile.write(out_path, rate=sampling_rate, data=audio)
    print(f"  {duration_seconds}s -> {out_path}")


def main():
    parser = argparse.ArgumentParser(description="MusicGen background music generator")
    parser.add_argument("--prompt", default="lo-fi chill ambient", help="Music style prompt")
    parser.add_argument("--duration", type=int, default=60, help="Duration in seconds")
    parser.add_argument("--out", required=True, help="Output WAV file")
    parser.add_argument("--device", default="cuda", help="Device: cuda or cpu")
    args = parser.parse_args()

    generate(args.prompt, args.duration, args.out, device=args.device)


if __name__ == "__main__":
    main()
