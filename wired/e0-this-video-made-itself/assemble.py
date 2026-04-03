#!/usr/bin/env python3
"""
Assemble a YouTube Short from pre-rendered assets.

Input:  A directory with PNGs (visuals) and MP3s (narration) per segment.
Output: A single MP4 file (1080x1920, 30fps).

Usage:
    python assemble.py --assets-dir ./assets --audio-dir ./audio --srt-dir ./srt --output ./output.mp4

Each segment is defined in the SEGMENTS list below. Edit it to match your video.
Segments with audio_file=None get silent duration instead.
"""
import argparse
import os
import re
import sys

import numpy as np
from moviepy import (
    AudioFileClip,
    CompositeVideoClip,
    ImageClip,
    TextClip,
    concatenate_videoclips,
)
from moviepy.audio.AudioClip import AudioArrayClip

W, H = 1080, 1920
FPS = 30


# ── Segment definitions ─────────────────────────────────────────────────────
# Edit this list for your video. Each segment needs:
#   name:        used to find <name>.png, <name>.mp3, <name>.srt
#   silent_dur:  if set, use silence instead of audio (for title cards)

SEGMENTS = [
    {"name": "hook",     "silent_dur": 3.0},
    {"name": "show",     "silent_dur": None},
    {"name": "pipeline", "silent_dur": None},
    {"name": "why",      "silent_dur": None},
    {"name": "outro",    "silent_dur": 4.0},
]


def make_silence(duration):
    fps = 44100
    n = int(fps * duration)
    arr = np.zeros((n, 2), dtype=np.float32)
    return AudioArrayClip(arr, fps=fps)


def parse_srt(path):
    with open(path) as f:
        content = f.read()
    entries = []
    for block in re.split(r"\n\s*\n", content.strip()):
        lines = block.strip().split("\n")
        if len(lines) < 3:
            continue
        for i, line in enumerate(lines):
            m = re.match(
                r"(\d{2}):(\d{2}):(\d{2})[,.](\d{3})\s*-->\s*"
                r"(\d{2}):(\d{2}):(\d{2})[,.](\d{3})",
                line,
            )
            if m:
                start = (
                    int(m.group(1)) * 3600
                    + int(m.group(2)) * 60
                    + int(m.group(3))
                    + int(m.group(4)) / 1000
                )
                end = (
                    int(m.group(5)) * 3600
                    + int(m.group(6)) * 60
                    + int(m.group(7))
                    + int(m.group(8)) / 1000
                )
                text = " ".join(lines[i + 1 :]).strip()
                entries.append((start, end, text))
                break
    return entries


def make_subtitle_clips(srt_path, clip_duration):
    entries = parse_srt(srt_path)
    clips = []
    for start, end, text in entries:
        if not text:
            continue
        dur = end - start
        if dur <= 0 or start >= clip_duration:
            continue
        dur = min(dur, clip_duration - start)
        txt = TextClip(
            text=text,
            font_size=36,
            color="white",
            stroke_color="black",
            stroke_width=2,
            font="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            method="caption",
            size=(900, None),
        )
        y_pos = int(H * 0.82)
        txt = txt.with_duration(dur).with_start(start).with_position(("center", y_pos))
        clips.append(txt)
    return clips


def build_segment(seg, assets_dir, audio_dir, srt_dir):
    name = seg["name"]
    image_path = os.path.join(assets_dir, f"{name}.png")

    if seg["silent_dur"] is not None:
        audio = make_silence(seg["silent_dur"])
        duration = seg["silent_dur"]
    else:
        audio_path = os.path.join(audio_dir, f"{name}.mp3")
        audio = AudioFileClip(audio_path)
        duration = audio.duration

    img = ImageClip(image_path).with_duration(duration).resized((W, H)).with_audio(audio)

    srt_path = os.path.join(srt_dir, f"{name}.srt")
    if os.path.exists(srt_path):
        sub_clips = make_subtitle_clips(srt_path, duration)
        if sub_clips:
            composite = CompositeVideoClip([img] + sub_clips, size=(W, H))
            return composite.with_duration(duration).with_audio(audio)

    return img


def main():
    parser = argparse.ArgumentParser(description="Assemble a YouTube Short from assets")
    parser.add_argument("--assets-dir", default="./assets", help="Directory with PNGs")
    parser.add_argument("--audio-dir", default="./audio", help="Directory with MP3s + SRTs")
    parser.add_argument("--srt-dir", default="./srt", help="Directory with SRT subtitle files")
    parser.add_argument("--output", default="./output.mp4", help="Output MP4 path")
    args = parser.parse_args()

    print("Building segments...")
    segments = []
    for seg in SEGMENTS:
        print(f"  {seg['name']}...")
        clip = build_segment(seg, args.assets_dir, args.audio_dir, args.srt_dir)
        segments.append(clip)

    total = sum(s.duration for s in segments)
    print(f"\nTotal duration: {total:.1f}s")

    print("Concatenating...")
    final = concatenate_videoclips(segments, method="compose")

    print(f"Writing to {args.output}...")
    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
    final.write_videofile(
        args.output,
        fps=FPS,
        codec="libx264",
        audio_codec="aac",
        audio_bitrate="192k",
        preset="fast",
        threads=4,
        logger="bar",
    )

    size = os.path.getsize(args.output) / (1024 * 1024)
    print(f"\nDone! {args.output}")
    print(f"Duration: {total:.1f}s | Size: {size:.1f} MB")


if __name__ == "__main__":
    main()
