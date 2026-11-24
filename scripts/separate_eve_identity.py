#!/usr/bin/env python3
"""Compose the editable SVG identity into the original compact EVE header."""
from io import BytesIO
from pathlib import Path
import re
import cairosvg
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
OLD = "eve-readme-v13"
PREVIOUS = "eve-readme-v14-separated"
NEW = "eve-readme-v15-compact"
SIZE = (1120, 545)
NAVY = (20, 43, 96)

def identity(theme):
    source = ASSETS / f"eve-identity-v2-{theme}.svg"
    bg = (13, 17, 23) if theme == "dark" else (255, 255, 255)
    raw = cairosvg.svg2png(url=str(source))
    with Image.open(BytesIO(raw)) as overlay:
        assert overlay.size == (594, 173)
        patch = Image.new("RGB", overlay.size, bg)
        patch.paste(overlay, (0, 0), overlay.getchannel("A"))
    return patch

def compose(frame, patch):
    assert frame.size == SIZE, frame.size
    result = frame.convert("RGB")
    result.paste(patch, (0, 0))
    return result

def render(theme):
    patch = identity(theme)
    highlight = (199, 216, 245) if theme == "dark" else (224, 233, 250)
    dest = ASSETS / f"{NEW}-{theme}.gif"
    with Image.open(ASSETS / f"{OLD}-{theme}.gif") as original:
        assert original.n_frames > 1
        loop = original.info.get("loop", 0)
        sample_indices = sorted({0, original.n_frames//10, original.n_frames//3,
                                 original.n_frames//2, original.n_frames-1})
        montage = Image.new("RGB", (SIZE[0], SIZE[1]*len(sample_indices)))
        for index, frame_index in enumerate(sample_indices):
            original.seek(frame_index)
            montage.paste(compose(original, patch), (0, index*SIZE[1]))
        palette = montage.quantize(colors=254, method=Image.Quantize.MEDIANCUT)
        colors = palette.getpalette()[:254*3] + list(NAVY) + list(highlight)
        palette.putpalette(colors)
        durations = []
        frames = []
        for i in range(original.n_frames):
            original.seek(i)
            durations.append(original.info.get("duration", 40))
            frames.append(compose(original, patch).quantize(
                palette=palette, dither=Image.Dither.NONE))
        frames[0].save(dest, save_all=True, append_images=frames[1:],
                       duration=durations, loop=loop, optimize=True, disposal=1)
        expected = sum(durations)
    with Image.open(dest) as generated:
        assert generated.size == SIZE
        assert generated.n_frames > 1
        assert generated.info.get("loop", 0) == loop
        rgb = generated.convert("RGB")
        assert rgb.getpixel((40, 30)) == highlight
        assert NAVY in set(rgb.crop((35, 8, 524, 85)).getdata())
        actual = 0
        for i in range(generated.n_frames):
            generated.seek(i)
            actual += generated.info.get("duration", 0)
        assert actual == expected, (theme, actual, expected)
    with Image.open(ASSETS / f"{OLD}-{theme}-still.png") as still:
        compose(still, patch).save(ASSETS / f"{NEW}-{theme}-still.png", optimize=True)
    print(f"Verified {theme}: {expected}ms, {SIZE}, highlighted identity", flush=True)

def update_readme():
    path = ROOT / "README.md"
    before = path.read_text(encoding="utf-8")
    updated = re.sub(r'(?m)^<p><picture><source media="\(prefers-color-scheme: dark\)" srcset="\./assets/eve-identity-v1-dark\.svg"[^\n]*</picture></p>\n\n', '', before)
    assert "eve-identity-v1-dark.svg" not in updated
    for theme in ("dark", "light"):
        for suffix in (".gif", "-still.png"):
            old = f"./assets/{PREVIOUS}-{theme}{suffix}"
            new = f"./assets/{NEW}-{theme}{suffix}"
            assert updated.count(old) + updated.count(new) == 1, (old, new)
            assert (ROOT / new).is_file(), new
            updated = updated.replace(old, new)
    path.write_text(updated, encoding="utf-8")

if __name__ == "__main__":
    for theme in ("dark", "light"):
        render(theme)
    update_readme()
