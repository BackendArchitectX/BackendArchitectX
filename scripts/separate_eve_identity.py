#!/usr/bin/env python3
"""Separate the static identity from the original EVE animation, without re-rendering EVE."""
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
OLD = "eve-readme-v13"
NEW = "eve-readme-v14-separated"
SIZE = (1120, 545)

def separate(frame, theme):
    assert frame.size == SIZE, frame.size
    result = frame.convert("RGB")
    greeting = result.crop((0, 245, 594, 405))
    bg = (13, 17, 23) if theme == "dark" else (255, 255, 255)
    ImageDraw.Draw(result).rectangle((0, 0, 593, 404), fill=bg)
    result.paste(greeting, (0, 135))
    # The right-hand robot, work prompt, lower divider and navigation caption
    # are untouched. The original multilingual greeting remains animated.
    return result

def render(theme):
    source = ASSETS / f"{OLD}-{theme}.gif"
    dest = ASSETS / f"{NEW}-{theme}.gif"
    with Image.open(source) as original:
        palette = original.copy()
        assert palette.mode == "P"
        durations = []
        frames = []
        loop = original.info.get("loop", 0)
        for i in range(original.n_frames):
            original.seek(i)
            durations.append(original.info.get("duration", 40))
            frames.append(separate(original, theme).quantize(
                palette=palette, dither=Image.Dither.NONE))
        frames[0].save(dest, save_all=True, append_images=frames[1:],
                       duration=durations, loop=loop, optimize=True, disposal=1)
        expected = sum(durations)
    with Image.open(dest) as generated:
        actual = 0
        for i in range(generated.n_frames):
            generated.seek(i)
            actual += generated.info.get("duration", 0)
        assert actual == expected, (theme, actual, expected)
        assert generated.size == SIZE
    with Image.open(ASSETS / f"{OLD}-{theme}-still.png") as still:
        separate(still, theme).save(ASSETS / f"{NEW}-{theme}-still.png", optimize=True)

def update_readme():
    path = ROOT / "README.md"
    before = path.read_text(encoding="utf-8")
    marker = "<!-- Animated 3D EVE header with reduced-motion and color-scheme fallbacks -->"
    identity = '<p><picture><source media="(prefers-color-scheme: dark)" srcset="./assets/eve-identity-v1-dark.svg" /><img src="./assets/eve-identity-v1-light.svg" width="100%" alt="Pranay Kadu — Backend Software Engineer — Java · Spring Boot · Distributed Systems · AWS" /></picture></p>'
    assert before.count(marker) == 1
    updated = before
    for theme in ("dark", "light"):
        assert (ASSETS / f"eve-identity-v1-{theme}.svg").is_file()
        for suffix in (".gif", "-still.png"):
            old = f"./assets/{OLD}-{theme}{suffix}"
            new = f"./assets/{NEW}-{theme}{suffix}"
            assert updated.count(old) + updated.count(new) == 1, (old, new)
            assert (ROOT / new).is_file()
            updated = updated.replace(old, new)
    if identity not in updated:
        updated = updated.replace(marker, identity + "\n\n" + marker)
    path.write_text(updated, encoding="utf-8")

if __name__ == "__main__":
    for theme in ("dark", "light"):
        render(theme)
    update_readme()
