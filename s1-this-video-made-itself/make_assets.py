#!/usr/bin/env python3
"""
Generate visual assets for a YouTube Short.

Renders title cards and terminal frames at 1080x1920 using Pillow.
Dracula color palette. No external dependencies beyond Pillow.

Usage:
    python make_assets.py --output-dir ./assets

Expects to be customized per video -- edit the functions below
to change text, layout, and terminal content.
"""
import argparse
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920

# Dracula palette
BG_DARK = (10, 10, 18)
PINK = (255, 80, 160)
PURPLE = (160, 80, 255)
CYAN = (80, 220, 255)
GREEN = (80, 230, 130)
YELLOW = (255, 220, 60)
ORANGE = (255, 160, 50)
WHITE = (255, 255, 255)
GRAY = (160, 160, 180)
TERM_BG = (20, 22, 30)
TERM_BORDER = (60, 60, 90)

# Fonts (DejaVu is standard on most Linux distros)
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REGULAR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
FONT_MONO_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"


def gradient_bg(draw, w, h, top=(10, 10, 25), bottom=(5, 5, 15)):
    """Draw a vertical gradient background."""
    for y in range(h):
        t = y / h
        r = int(top[0] + (bottom[0] - top[0]) * t)
        g = int(top[1] + (bottom[1] - top[1]) * t)
        b = int(top[2] + (bottom[2] - top[2]) * t)
        draw.line([(0, y), (w, y)], fill=(r, g, b))


def wrap_text(text, font, max_width, draw):
    """Wrap text to fit within max_width pixels."""
    words = text.split()
    lines = []
    current = []
    for word in words:
        test = " ".join(current + [word])
        bbox = draw.textbbox((0, 0), test, font=font)
        if bbox[2] - bbox[0] <= max_width:
            current.append(word)
        else:
            if current:
                lines.append(" ".join(current))
            current = [word]
    if current:
        lines.append(" ".join(current))
    return lines


def draw_centered_lines(draw, lines, font, y, color, line_gap=8):
    """Draw multiple lines of text, centered horizontally."""
    line_h = draw.textbbox((0, 0), "Ag", font=font)[3] + line_gap
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        tw = bbox[2] - bbox[0]
        x = (W - tw) // 2
        draw.text((x + 2, y + 2), line, font=font, fill=(0, 0, 0))
        draw.text((x, y), line, font=font, fill=color)
        y += line_h
    return y


def make_title_card(text, accent_color, output_path, subtitle=None):
    """Render a title card with centered text and accent bars."""
    img = Image.new("RGB", (W, H), BG_DARK)
    draw = ImageDraw.Draw(img)
    gradient_bg(draw, W, H, (15, 5, 25), (5, 5, 15))

    draw.rectangle([0, 0, W, 8], fill=accent_color)
    draw.rectangle([0, H - 8, W, H], fill=accent_color)

    font_big = ImageFont.truetype(FONT_BOLD, 72)
    lines = wrap_text(text, font_big, 900, draw)
    total_h = len(lines) * 90
    start_y = (H - total_h) // 2 - 40
    draw_centered_lines(draw, lines, font_big, start_y, accent_color, line_gap=18)

    if subtitle:
        font_sub = ImageFont.truetype(FONT_REGULAR, 38)
        bbox = draw.textbbox((0, 0), subtitle, font=font_sub)
        sx = (W - (bbox[2] - bbox[0])) // 2
        draw.text((sx, start_y + total_h + 60), subtitle, font=font_sub, fill=GRAY)

    img.save(output_path)


def make_terminal_card(lines, accent_color, output_path, title_bar_text="terminal"):
    """
    Render a terminal frame with colored lines.

    Each entry in `lines` is a tuple of (text, color).
    Colors are applied per-line using Dracula conventions:
      - Prompt lines ($): GRAY
      - Errors/blocked: (255, 80, 80)
      - Success: GREEN
      - Keywords: CYAN or PINK
      - Default: WHITE
    """
    img = Image.new("RGB", (W, H), BG_DARK)
    draw = ImageDraw.Draw(img)
    gradient_bg(draw, W, H, (10, 12, 22), (5, 5, 15))

    draw.rectangle([0, 0, W, 8], fill=accent_color)

    font_mono = ImageFont.truetype(FONT_MONO, 28)

    # Terminal window
    pad = 60
    line_h = 34
    block_h = len(lines) * line_h + 80
    t_y = max((H - block_h) // 2 - 40, 120)
    t_w = W - 2 * pad

    draw.rounded_rectangle(
        [pad, t_y, pad + t_w, t_y + block_h],
        radius=12, fill=TERM_BG, outline=TERM_BORDER, width=2,
    )

    # Title bar
    draw.rounded_rectangle(
        [pad, t_y, pad + t_w, t_y + 44], radius=12, fill=(30, 32, 48),
    )
    draw.rectangle([pad, t_y + 28, pad + t_w, t_y + 44], fill=(30, 32, 48))
    for xi, col in [(30, (255, 90, 90)), (62, (255, 200, 50)), (94, (50, 210, 100))]:
        draw.ellipse(
            [pad + xi, t_y + 12, pad + xi + 18, t_y + 30], fill=col,
        )
    font_title = ImageFont.truetype(FONT_MONO, 24)
    draw.text((pad + 130, t_y + 12), title_bar_text, font=font_title, fill=GRAY)

    # Lines
    ly = t_y + 58
    for text, color in lines:
        if text:
            draw.text((pad + 24, ly), text, font=font_mono, fill=color)
        ly += line_h

    draw.rectangle([0, H - 8, W, H], fill=accent_color)
    img.save(output_path)


# ── Per-video asset definitions ──────────────────────────────────────────────
# Edit these functions to generate assets for your specific video.

def generate_all(output_dir):
    os.makedirs(output_dir, exist_ok=True)

    # Hook title card
    make_title_card(
        "This Video Made Itself",
        PINK,
        os.path.join(output_dir, "hook.png"),
        subtitle="Nox Craft",
    )

    # Show segment -- terminal showing video output
    make_terminal_card(
        [
            ("$ /video --script s1.md", GRAY),
            ("", WHITE),
            ("Generating audio...", CYAN),
            ("  audio/show.mp3          (8.2s)", WHITE),
            ("  audio/pipeline.mp3      (17.6s)", WHITE),
            ("  audio/why.mp3           (21.4s)", WHITE),
            ("", WHITE),
            ("Rendering assets...", CYAN),
            ("  assets/hook.png         1080x1920", WHITE),
            ("  assets/show.png         1080x1920", WHITE),
            ("  assets/pipeline.png     1080x1920", WHITE),
            ("  assets/why.png          1080x1920", WHITE),
            ("  assets/outro.png        1080x1920", WHITE),
            ("", WHITE),
            ("Assembling video...", GREEN),
            ("  output: s1.mp4 (54.8s, 1.7MB)", GREEN),
            ("", WHITE),
            ("Done.", GREEN),
        ],
        CYAN,
        os.path.join(output_dir, "show.png"),
        title_bar_text="claude-code",
    )

    # Pipeline segment -- the three tools
    make_terminal_card(
        [
            ("Video Production Pipeline", PINK),
            ("", WHITE),
            ("1. edge-tts", CYAN),
            ("   Text  ->  Narration (.mp3 + .srt)", WHITE),
            ("   Voice: en-US-AndrewMultilingualNeural", GRAY),
            ("", WHITE),
            ("2. Pillow", CYAN),
            ("   Code  ->  Terminal frames (.png)", WHITE),
            ("   Text  ->  Title cards (.png)", WHITE),
            ("   Palette: Dracula", GRAY),
            ("", WHITE),
            ("3. MoviePy", CYAN),
            ("   Images + Audio  ->  Short (.mp4)", WHITE),
            ("   Subtitles burned in from .srt", WHITE),
            ("", WHITE),
            ("Total cost: $0", GREEN),
            ("Dependencies: pip install -r requirements.txt", GRAY),
        ],
        GREEN,
        os.path.join(output_dir, "pipeline.png"),
        title_bar_text="pipeline",
    )

    # Why segment -- title card
    make_title_card(
        "Every technique. Every tool. Every real experience.",
        PURPLE,
        os.path.join(output_dir, "why.png"),
        subtitle="Wired — coming next",
    )

    # Outro
    make_title_card(
        "github.com/noxcraftdev/video-examples",
        PURPLE,
        os.path.join(output_dir, "outro.png"),
        subtitle="@noxcraftdev",
    )

    print(f"Generated {len(os.listdir(output_dir))} assets in {output_dir}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate video assets")
    parser.add_argument("--output-dir", default="./assets", help="Output directory for PNGs")
    args = parser.parse_args()
    generate_all(args.output_dir)
