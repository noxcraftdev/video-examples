#!/usr/bin/env python3
"""Kokoro + OpenVoice voice pipeline from Wired E1.

Stage 1: Kokoro TTS generates a neutral base narration.
Stage 2: OpenVoice transfers your voice timbre onto it.

Usage:
    python generate_voice.py --ref my_voice.wav --text "Hello world." --out output.wav

Requirements:
    pip install -r requirements.txt
    OpenVoice v2 checkpoints in ~/.cache/openvoice/checkpoints_v2/
"""

import argparse
import os
import tempfile

import numpy as np
import soundfile as sf
import torch

# OpenVoice uses torchaudio.load internally; patch it to use soundfile
# so it works without libsndfile version mismatches.
import torchaudio


def _sf_load(path, **kwargs):
    data, sr = sf.read(str(path), dtype="float32")
    if data.ndim == 1:
        data = data[np.newaxis, :]
    else:
        data = data.T
    return torch.from_numpy(data), sr


torchaudio.load = _sf_load

# Pre-trust silero-vad so OpenVoice's VAD step doesn't prompt interactively.
torch.hub.load("snakers4/silero-vad", model="silero_vad", trust_repo=True)

from kokoro import KPipeline
from openvoice import se_extractor
from openvoice.api import ToneColorConverter


CKPT = os.path.expanduser("~/.cache/openvoice/checkpoints_v2")


def load_models(device="cuda"):
    kokoro = KPipeline(lang_code="a", repo_id="hexgrad/Kokoro-82M")
    converter = ToneColorConverter(f"{CKPT}/converter/config.json", device=device)
    converter.load_ckpt(f"{CKPT}/converter/checkpoint.pth")
    return kokoro, converter


def generate(kokoro, converter, text, ref_audio, out_path, tau=0.7, speed=1.05):
    # Stage 1: Kokoro base narration
    chunks = []
    for _gs, _ps, audio in kokoro(text, voice="af_heart", speed=speed):
        chunks.append(audio)
    base_wav = torch.cat(chunks).numpy()
    base_dur = len(base_wav) / 24000

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        base_path = tmp.name

    # OpenVoice VAD needs at least ~4s; pad with silence if shorter.
    if base_dur < 4.0:
        pad = np.zeros(int((4.0 - base_dur) * 24000))
        sf.write(base_path, np.concatenate([base_wav, pad]), 24000)
    else:
        sf.write(base_path, base_wav, 24000)

    # Stage 2: OpenVoice timbre transfer
    target_se, _ = se_extractor.get_se(ref_audio, converter, vad=True)
    source_se, _ = se_extractor.get_se(base_path, converter, vad=True)

    converter.convert(
        audio_src_path=base_path,
        src_se=source_se,
        tgt_se=target_se,
        output_path=out_path,
        tau=tau,
    )
    os.unlink(base_path)

    # Trim back to original duration if we padded.
    if base_dur < 4.0:
        data, sr = sf.read(out_path)
        sf.write(out_path, data[: int(base_dur * sr)], sr)

    print(f"  {base_dur:.1f}s -> {out_path}")


def main():
    parser = argparse.ArgumentParser(description="Kokoro + OpenVoice voice pipeline")
    parser.add_argument("--ref", required=True, help="Reference audio file (your voice)")
    parser.add_argument("--text", required=True, help="Text to synthesize")
    parser.add_argument("--out", required=True, help="Output WAV file")
    parser.add_argument("--tau", type=float, default=0.7, help="Timbre strength (0-1, default 0.7)")
    parser.add_argument("--device", default="cuda", help="Device: cuda or cpu")
    args = parser.parse_args()

    print("Loading Kokoro...")
    kokoro, converter = load_models(device=args.device)

    print(f"Extracting timbre from {args.ref}...")
    generate(kokoro, converter, args.text, args.ref, args.out, tau=args.tau)


if __name__ == "__main__":
    main()
