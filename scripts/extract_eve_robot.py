#!/usr/bin/env python3
"""Extract the original animated red EVE sprite and use native README header text."""
from pathlib import Path
import re
from PIL import Image, ImageChops

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
OLD = "eve-readme-v17-crimson-titanium"
NEW = "eve-robot-v18-red"
# The original compositor places the 504px-wide sprite at x=594.
# Exclude the work prompt and divider drawn below the robot.
CROP = (594, 0, 1098, 392)
SIZE = (504, 392)

def robot(frame):
    assert frame.size == (1120, 480), frame.size
    return frame.convert("RGB").crop(CROP)

def validate_shell(frame):
    pixels = frame.convert("RGB").getdata()
    red_pixels = sum(r > 65 and r > 1.5*g and r > 1.25*b for r,g,b in pixels)
    assert red_pixels > 2000, ("Red EVE shell missing", red_pixels)

def render(theme):
    dest = ASSETS / f"{NEW}-{theme}.gif"
    with Image.open(ASSETS / f"{OLD}-{theme}.gif") as source:
        assert source.n_frames > 1
        loop = source.info.get("loop", 0)
        indices = sorted({0, source.n_frames//20, source.n_frames//10,
                          source.n_frames//5, source.n_frames//2})
        montage = Image.new("RGB", (SIZE[0], SIZE[1]*len(indices)))
        for j, i in enumerate(indices):
            source.seek(i)
            montage.paste(robot(source), (0, j*SIZE[1]))
        palette = montage.quantize(colors=256, method=Image.Quantize.MEDIANCUT)
        frames, durations = [], []
        for i in range(source.n_frames):
            source.seek(i)
            durations.append(source.info.get("duration", 40))
            frames.append(robot(source).quantize(palette=palette, dither=Image.Dither.NONE))
        frames[0].save(dest, save_all=True, append_images=frames[1:],
                       duration=durations, loop=loop, optimize=True, disposal=1)
        expected = sum(durations)
    with Image.open(dest) as generated:
        assert generated.size == SIZE
        assert generated.n_frames > 1
        assert generated.info.get("loop", 0) == loop
        first = generated.convert("RGB")
        validate_shell(first)
        changed, total = False, 0
        for i in range(generated.n_frames):
            generated.seek(i)
            total += generated.info.get("duration", 0)
            if not changed:
                changed = ImageChops.difference(first, generated.convert("RGB")).getbbox() is not None
        assert changed, "No animated movement"
        assert total == expected, (total, expected)
    with Image.open(ASSETS / f"{OLD}-{theme}-still.png") as still:
        frame = robot(still)
        validate_shell(frame)
        frame.save(ASSETS / f"{NEW}-{theme}-still.png", optimize=True)
    print(f"Verified {theme} robot-only animation: {SIZE}, {expected}ms", flush=True)

HEADER = """<!-- Native profile identity beside independent red EVE animation -->
<picture>
  <source media="(prefers-reduced-motion: reduce) and (prefers-color-scheme: dark)" srcset="./assets/eve-robot-v18-red-dark-still.png" />
  <source media="(prefers-reduced-motion: reduce)" srcset="./assets/eve-robot-v18-red-light-still.png" />
  <source media="(prefers-color-scheme: dark)" srcset="./assets/eve-robot-v18-red-dark.gif" />
  <img align="right" src="./assets/eve-robot-v18-red-light.gif" width="340" alt="Red EVE robot waving and pointing." />
</picture>

<p><strong>Pranay Kadu</strong></p>
<p><strong>Backend Software Engineer</strong></p>
<p><strong>Java · Spring Boot · Distributed Systems · AWS</strong></p>
<p><strong>Hey, I am EVE.</strong></p>

<br clear="all" />

<p align="center"><strong>PROJECTS · SKILLS · CONTRIBUTIONS</strong></p>"""

def update_readme():
    path = ROOT / "README.md"
    before = path.read_text(encoding="utf-8")
    for theme in ("dark", "light"):
        for suffix in (".gif", "-still.png"):
            assert (ASSETS / f"{NEW}-{theme}{suffix}").is_file()
    if HEADER in before:
        return
    marker = "<!-- Animated 3D EVE header with reduced-motion and color-scheme fallbacks -->"
    start = before.index(marker)
    end = before.index("</picture>", start) + len("</picture>")
    assert OLD in before[start:end]
    updated = before[:start] + HEADER + before[end:]
    # The header is now real text, so avoid repeating the same identity below it.
    duplicate = re.compile(r'<h1><picture>[^\n]*readme-text-crimson-titanium-name-dark\.svg[^\n]*</picture></h1>\n\n<p><picture>[^\n]*readme-text-crimson-titanium-role-dark\.svg[^\n]*</picture></p>\n\n\*\*Java · Spring Boot · Distributed Systems · AWS\*\*\n\n')
    updated, count = duplicate.subn("", updated, count=1)
    assert count == 1, "Expected duplicate identity not found"
    assert OLD not in updated
    assert updated.count("<p><strong>Pranay Kadu</strong></p>") == 1
    path.write_text(updated, encoding="utf-8")

if __name__ == "__main__":
    for theme in ("dark", "light"):
        render(theme)
    update_readme()
