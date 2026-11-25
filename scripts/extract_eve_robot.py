#!/usr/bin/env python3
"""Render full-color lossless EVE animation without GIF palette banding."""
from pathlib import Path
from PIL import Image, ImageChops, features
from render_eve_red import EVE, FPS, SECONDS, LANG, composite as full_composite

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
CURRENT = "eve-robot-v22-pointing-red"
NEW = "eve-robot-v23-smooth-red"
SIZE = (1120, 480)
ROBOT = (594, 0, 1098, 392)
CUE = (594, 392, 1098, 439)
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
    cue = frame.convert("RGB").crop(CUE)
    canvas = Image.new("RGB", (WIDTH, TEXT_HEIGHT + robot.height - top + cue.height), bg)
    canvas.paste(glyph, ((WIDTH-glyph.width)//2, (TEXT_HEIGHT-glyph.height)//2))
    canvas.paste(robot.crop((0,top,robot.width,robot.height)),(0,TEXT_HEIGHT))
    canvas.paste(cue, (0, TEXT_HEIGHT + robot.height - top))
    return canvas

def arrow_pixels(frame, theme):
    # The original arrow is centered at x=652; relative to the crop it is x=58.
    region = frame.convert("RGB").crop((45, frame.height-47, 72, frame.height))
    bg = background(theme)
    return sum(max(abs(r-bg[0]),abs(g-bg[1]),abs(b-bg[2]))>55
               for r,g,b in region.getdata())

def signature(frame, theme):
    cropped = frame.convert("RGB").crop((0,0,WIDTH,TEXT_HEIGHT))
    box = bounds(cropped,background(theme))
    assert box, "Greeting disappeared"
    return cropped.crop(box).resize((64,16)).tobytes()

def render(theme):
    bg = background(theme)
    assert features.check("webp"), "Pillow must support WebP"
    dest = ASSETS / f"{NEW}-{theme}.webp"
    scene = EVE(theme)
    sprites = [scene.frame(i/FPS) for i in range(SECONDS*FPS)]
    # Preserve the exact compact crop used by the currently published GIF.
    # Reading only its dimensions does not reuse any quantized pixel data.
    with Image.open(ASSETS / f"{CURRENT}-{theme}-still.png") as previous:
        top = TEXT_HEIGHT + (ROBOT[3]-ROBOT[1]) + (CUE[3]-CUE[1]) - previous.height
        assert previous.width == WIDTH and 0 <= top <= 80
    point_frame = round(4.12*FPS)
    still_frame = compose(full_composite(theme,sprites[point_frame],0,point_frame/FPS),theme,top)
    still_frame.save(ASSETS / f"{NEW}-{theme}-still.png",optimize=True)
    frames = [compose(full_composite(theme,sprite,language,i/FPS),theme,top)
              for language in range(len(LANG)) for i,sprite in enumerate(sprites)]
    durations = [1000//FPS] * len(frames)
    loop = 0
    frames[0].save(dest,format="WEBP",save_all=True,append_images=frames[1:],
                   duration=durations,loop=loop,lossless=True,quality=85,method=4)
    with Image.open(dest) as result:
        assert result.size == still_frame.size and result.n_frames == len(frames)
        assert result.info.get("loop",0) == loop
        total, signatures, changed = 0,set(),False
        pointing_cycles, quiet_cycles = set(), set()
        first_robot = result.convert("RGB").crop((0,TEXT_HEIGHT,WIDTH,result.height))
        assert sum(r>65 and r>1.5*g and r>1.25*b for r,g,b in first_robot.getdata())>2000
        for i in range(result.n_frames):
            result.seek(i)
            result.load()  # WebP exposes duration after decoding the frame.
            duration = result.info.get("duration",0)
            assert ImageChops.difference(result.convert("RGB"),frames[i]).getbbox() is None, ("Lossless frame mismatch",i)
            signatures.add(signature(result,theme))
            if not changed:
                current = result.convert("RGB").crop((0,TEXT_HEIGHT,WIDTH,result.height))
                changed = ImageChops.difference(first_robot,current).getbbox() is not None
            cycle, phase = divmod(total,6000)
            visible = arrow_pixels(result,theme)
            if 3800 <= phase <= 4700 and visible > 20:
                pointing_cycles.add(cycle)
            if 0 <= phase <= 2200 and visible < 10:
                quiet_cycles.add(cycle)
            total += duration
        assert total == sum(durations) == 30000 and changed
        assert len(signatures) >= 5, ("Missing multilingual changes",len(signatures))
        assert pointing_cycles == quiet_cycles == set(range(5)), (pointing_cycles,quiet_cycles)
        assert arrow_pixels(still_frame,theme)>20, "Still fallback missing downward cue"
    print(f"{theme}: validated {total}ms loop, multilingual greetings and synchronized downward arrows in all five cycles",flush=True)

def update_readme():
    path = ROOT / "README.md"
    before = path.read_text(encoding="utf-8")
    start = before.index("<!-- Native profile identity")
    end = before.index(BOUNDARY,start)
    header = before[start:end]
    assert "Hey, I am EVE.</h2>" not in header
    for theme in ("dark","light"):
        for old_suffix,new_suffix in ((".gif",".webp"),("-still.png","-still.png")):
            old = f"{CURRENT}-{theme}{old_suffix}"
            new = f"{NEW}-{theme}{new_suffix}"
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
