#!/usr/bin/env python3
"""Trim empty upper padding from the independent EVE animation, preserving all motion."""
from pathlib import Path
from PIL import Image, ImageChops

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
OLD = "eve-robot-v18-red"
NEW = "eve-robot-v19-upper-red"
SIZE = (504, 392)

def find_top(frame, theme):
    rgb = frame.convert("RGB")
    bg = Image.new("RGB", rgb.size, (13,17,23) if theme == "dark" else (255,255,255))
    diff = ImageChops.difference(rgb, bg)
    r,g,b = diff.split()
    mask = ImageChops.lighter(ImageChops.lighter(r,g),b).point(lambda x: 255 if x > 20 else 0)
    bounds = mask.getbbox()
    return bounds[1] if bounds else rgb.height

def validate_shell(frame):
    assert sum(r > 65 and r > 1.5*g and r > 1.25*b for r,g,b in frame.convert("RGB").getdata()) > 2000

def render(theme):
    with Image.open(ASSETS / f"{OLD}-{theme}-still.png") as still:
        top = find_top(still, theme)
    with Image.open(ASSETS / f"{OLD}-{theme}.gif") as source:
        assert source.size == SIZE and source.n_frames > 1
        loop = source.info.get("loop",0)
        for i in range(source.n_frames):
            source.seek(i)
            top = min(top, find_top(source, theme))
        top = max(0, min(80, top - 10))
        crop = (0, top, SIZE[0], SIZE[1])
        source.seek(0)
        palette = source.copy()
        assert palette.mode == "P"
        frames, durations = [], []
        for i in range(source.n_frames):
            source.seek(i)
            durations.append(source.info.get("duration",40))
            frames.append(source.convert("RGB").crop(crop).quantize(palette=palette, dither=Image.Dither.NONE))
        dest = ASSETS / f"{NEW}-{theme}.gif"
        frames[0].save(dest, save_all=True, append_images=frames[1:], duration=durations, loop=loop, optimize=True, disposal=1)
    with Image.open(dest) as result:
        assert result.size == (SIZE[0],SIZE[1]-top) and result.n_frames > 1
        assert result.info.get("loop",0) == loop
        first = result.convert("RGB")
        validate_shell(first)
        total, changed = 0, False
        for i in range(result.n_frames):
            result.seek(i)
            total += result.info.get("duration",0)
            if not changed:
                changed = ImageChops.difference(first,result.convert("RGB")).getbbox() is not None
        assert total == sum(durations) and changed
    with Image.open(ASSETS / f"{OLD}-{theme}-still.png") as still:
        image = still.convert("RGB").crop(crop)
        validate_shell(image)
        image.save(ASSETS / f"{NEW}-{theme}-still.png",optimize=True)
    print(f"{theme}: removed {top}px of upper padding; validated {total}ms animation",flush=True)

CURRENT = """<!-- Native profile identity beside independent red EVE animation -->
<picture>
  <source media="(prefers-reduced-motion: reduce) and (prefers-color-scheme: dark)" srcset="./assets/eve-robot-v18-red-dark-still.png" />
  <source media="(prefers-reduced-motion: reduce)" srcset="./assets/eve-robot-v18-red-light-still.png" />
  <source media="(prefers-color-scheme: dark)" srcset="./assets/eve-robot-v18-red-dark.gif" />
  <img align="right" src="./assets/eve-robot-v18-red-light.gif" width="300" alt="Red EVE robot waving and pointing." />
</picture>

<h3>Pranay Kadu</h3>
<h4>Backend Software Engineer</h4>
<p><strong>Java · Spring Boot · Distributed Systems · AWS</strong></p>
<h3>Hey, I am EVE.</h3>

<br clear="all" />"""
HEADER = """<!-- Native profile identity beside independent red EVE animation -->
<picture>
  <source media="(prefers-reduced-motion: reduce) and (prefers-color-scheme: dark)" srcset="./assets/eve-robot-v19-upper-red-dark-still.png" />
  <source media="(prefers-reduced-motion: reduce)" srcset="./assets/eve-robot-v19-upper-red-light-still.png" />
  <source media="(prefers-color-scheme: dark)" srcset="./assets/eve-robot-v19-upper-red-dark.gif" />
  <img align="right" src="./assets/eve-robot-v19-upper-red-light.gif" width="300" alt="Red EVE robot waving and pointing." />
</picture>

<h3>Pranay Kadu</h3>
<h4>Backend Software Engineer</h4>
<p><strong>Java · Spring Boot · Distributed Systems · AWS</strong></p>
<h3>Hey, I am EVE.</h3>

<br clear="all" />"""
BOUNDARY = '<p align="center"><strong>PROJECTS · SKILLS · CONTRIBUTIONS</strong></p>'

def update_readme():
    path = ROOT / "README.md"
    before = path.read_text(encoding="utf-8")
    if HEADER in before:
        return
    assert before.count(CURRENT) == 1
    updated = before.replace(CURRENT,HEADER,1)
    assert before.split(BOUNDARY,1)[1] == updated.split(BOUNDARY,1)[1]
    path.write_text(updated,encoding="utf-8")

if __name__ == "__main__":
    for theme in ("dark","light"):
        render(theme)
    update_readme()
