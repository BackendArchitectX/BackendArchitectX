#!/usr/bin/env python3
"""Restore the original multilingual greeting above the standalone red EVE."""
from pathlib import Path
from PIL import Image, ImageChops

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
SOURCE = "eve-readme-v17-crimson-titanium"
CURRENT = "eve-robot-v19-upper-red"
NEW = "eve-robot-v20-multilingual-red"
SIZE = (1120, 480)
ROBOT = (594, 0, 1098, 392)
GREETING = (28, 210, 576, 330)
WIDTH = 504
TEXT_HEIGHT = 76
BOUNDARY = '<p align="center"><strong>PROJECTS · SKILLS · CONTRIBUTIONS</strong></p>'

def background(theme):
    return (13, 17, 23) if theme == "dark" else (255, 255, 255)

def bounds(image, bg):
    diff = ImageChops.difference(image, Image.new("RGB", image.size, bg))
    r, g, b = diff.split()
    return ImageChops.lighter(ImageChops.lighter(r,g),b).point(
        lambda v: 255 if v > 35 else 0).getbbox()

def parts(frame):
    assert frame.size == SIZE, frame.size
    rgb = frame.convert("RGB")
    return rgb.crop(ROBOT), rgb.crop(GREETING)

def compose(frame, theme, top):
    robot, greeting = parts(frame)
    bg = background(theme)
    rect = bounds(greeting, bg)
    assert rect, "Original multilingual greeting missing"
    glyph = greeting.crop(rect)
    ratio = min(1.0, (WIDTH-24)/glyph.width, (TEXT_HEIGHT-16)/glyph.height)
    glyph = glyph.resize((max(1,round(glyph.width*ratio)),max(1,round(glyph.height*ratio))), Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", (WIDTH, TEXT_HEIGHT + robot.height - top), bg)
    canvas.paste(glyph, ((WIDTH-glyph.width)//2, (TEXT_HEIGHT-glyph.height)//2))
    canvas.paste(robot.crop((0,top,robot.width,robot.height)),(0,TEXT_HEIGHT))
    return canvas

def signature(frame, theme):
    cropped = frame.convert("RGB").crop((0,0,WIDTH,TEXT_HEIGHT))
    box = bounds(cropped,background(theme))
    assert box, "Greeting disappeared"
    return cropped.crop(box).resize((64,16)).tobytes()

def render(theme):
    bg = background(theme)
    dest = ASSETS / f"{NEW}-{theme}.gif"
    with Image.open(ASSETS / f"{SOURCE}-{theme}.gif") as original:
        assert original.n_frames > 1
        loop = original.info.get("loop",0)
        top = 80
        for i in range(original.n_frames):
            original.seek(i)
            robot,_ = parts(original)
            box = bounds(robot,bg)
            assert box
            top = min(top,max(0,box[1]-10))
        with Image.open(ASSETS / f"{SOURCE}-{theme}-still.png") as still:
            robot,_ = parts(still)
            box = bounds(robot,bg)
            assert box
            top = min(top,max(0,box[1]-10))
            still_frame = compose(still,theme,top)
            still_frame.save(ASSETS / f"{NEW}-{theme}-still.png",optimize=True)
        original.seek(0)
        palette = original.copy()
        assert palette.mode == "P"
        frames, durations = [], []
        for i in range(original.n_frames):
            original.seek(i)
            durations.append(original.info.get("duration",40))
            frames.append(compose(original,theme,top).quantize(palette=palette,dither=Image.Dither.NONE))
        frames[0].save(dest,save_all=True,append_images=frames[1:],duration=durations,
                       loop=loop,optimize=True,disposal=1)
    with Image.open(dest) as result:
        assert result.size == still_frame.size and result.n_frames > 1
        assert result.info.get("loop",0) == loop
        total, signatures, changed = 0,set(),False
        first_robot = result.convert("RGB").crop((0,TEXT_HEIGHT,WIDTH,result.height))
        assert sum(r>65 and r>1.5*g and r>1.25*b for r,g,b in first_robot.getdata())>2000
        for i in range(result.n_frames):
            result.seek(i)
            duration = result.info.get("duration",0)
            signatures.add(signature(result,theme))
            if not changed:
                current = result.convert("RGB").crop((0,TEXT_HEIGHT,WIDTH,result.height))
                changed = ImageChops.difference(first_robot,current).getbbox() is not None
            total += duration
        assert total == sum(durations) == 30000 and changed
        assert len(signatures) >= 5, ("Missing multilingual changes",len(signatures))
    print(f"{theme}: validated {total}ms loop with animated robot and multilingual greetings",flush=True)

def update_readme():
    path = ROOT / "README.md"
    before = path.read_text(encoding="utf-8")
    start = before.index("<!-- Native profile identity")
    end = before.index(BOUNDARY,start)
    header = before[start:end]
    assert "Hey, I am EVE.</h2>" not in header
    for theme in ("dark","light"):
        for suffix in (".gif","-still.png"):
            old = f"{CURRENT}-{theme}{suffix}"
            new = f"{NEW}-{theme}{suffix}"
            assert (ASSETS/new).is_file()
            assert header.count(old)+header.count(new)==1
            header = header.replace(old,new)
    header = header.replace('alt="Red EVE robot waving and pointing."',
        'alt="Red EVE robot waving and greeting in English, Chinese, Hindi, Spanish and French."')
    updated = before[:start]+header+before[end:]
    assert before.split(BOUNDARY,1)[1] == updated.split(BOUNDARY,1)[1]
    path.write_text(updated,encoding="utf-8")

if __name__ == "__main__":
    for theme in ("dark","light"):
        render(theme)
    update_readme()
