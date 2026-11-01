#!/usr/bin/env python3
"""Build GitHub-compatible 3D-rendered Pawny GIFs, with one readable greeting at a time."""
from pathlib import Path
import math
import os
import re
from PIL import Image, ImageDraw, ImageEnhance, ImageFont

ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/"assets"
W,H=1120,545
FPS=6
SLOT=6
LANG=[
 ("ENGLISH","Hey, I am Pawny.","latin"),
 ("MANDARIN CHINESE","你好，我是 Pawny。","chinese"),
 ("HINDI","नमस्ते, मैं Pawny हूँ।","hindi"),
 ("SPANISH","¡Hola! Soy Pawny.","latin"),
 ("FRENCH","Salut, je suis Pawny.","latin"),
]
FONTS={
 "latin":["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf","/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"],
 "chinese":["/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"],
 "hindi":["/usr/share/fonts/truetype/noto/NotoSansDevanagari-Bold.ttf","/usr/share/fonts/truetype/lohit-devanagari/Lohit-Devanagari.ttf"]
}
def font(kind,size):
 for path in FONTS.get(kind,[])+FONTS["latin"]:
  if os.path.exists(path):
   return ImageFont.truetype(path,size,layout_engine=ImageFont.Layout.RAQM)
 raise RuntimeError("Install Noto Sans fonts")

def brighten(frame):
 frame=ImageEnhance.Color(frame).enhance(1.2).convert("RGBA")
 px=frame.load()
 for y in range(frame.height):
  for x in range(frame.width):
   r,g,b,a=px[x,y]
   if a and r>90 and r>g*1.55 and r>b*1.35:
    px[x,y]=(min(255,int(r*1.13)),min(255,int(g*1.08)),min(255,int(b*1.06)),a)
 return frame

def soften_pawny_reflections(frame):
 # Locate red helmet and torso regions independently in each source frame.
 # A fixed rectangular paint mask can hit Pawny's WHITE FACE when he moves.
 # Detect actual red armor at this frame, then recolor only its pale highlights.
 source=frame.convert("RGBA")
 out=source.copy()
 px=source.load()
 dest=out.load()
 width,height=source.size
 def is_red(x,y):
  if x<0 or y<0 or x>=width or y>=height:
   return False
  r,g,b,a=px[x,y]
  return a>120 and r>145 and r>g*1.55 and r>b*1.43
 # Per-column helmet base; guarantees no paint below the red dome.
 helmet_base={}
 for x in range(89,min(width,191)):
  rows=[y for y in range(min(90,height)) if is_red(x,y)]
  if len(rows)>=10:
   helmet_base[x]=max(rows)-4
 # Per-row torso support; the face alone does not contain enough red pixels.
 torso_rows=set()
 for y in range(145,min(240,height)):
  if sum(is_red(x,y) for x in range(90,min(186,width)))>=27:
   torso_rows.add(y)
 for y in range(min(240,height)):
  for x in range(89,min(width,191)):
   r,g,b,a=px[x,y]
   if a<120 or r<155 or g<65 or b<58:
    continue
   helmet=(x in helmet_base and 5<=y<=helmet_base[x])
   # The central white heart and both white gloves are outside this mask.
   torso=(y in torso_rows and 103<=x<=166
          and not (118<=x<=145))
   if not (helmet or torso):
    continue
   weight=min(1.0,max(0.0,(max(g,b)-55)/120))
   if torso and not helmet:
    # Feather the correction near the heart and torso borders.
    # This avoids hard vertical retouch edges in the animated chest.
    taper=(min(1.0,(x-103)/7,(118-x)/7) if x<118
           else min(1.0,(x-145)/7,(166-x)/7))
    if torso_rows:
     lower=min(torso_rows)
     upper=max(torso_rows)
     taper*=max(0.0,min(1.0,(y-lower)/11,(upper-y)/11))
    weight*=max(0.0,taper)*0.85
   dest[x,y]=(
    min(248,max(210,int(r*.98))),
    round(g*(1-weight)+min(68,30+g*.14)*weight),
    round(b*(1-weight)+min(75,40+b*.14)*weight),
    a)
 return out

def read_motions(path):
 out=[]
 with Image.open(path) as im:
  if im.width<1000 or im.height<450:
   raise RuntimeError("Unexpected source size "+str(im.size))
  elapsed=0
  for i in range(im.n_frames):
   im.seek(i)
   frame=im.convert("RGBA").crop((770,98,1068,439))
   # Remove the old tiny pointing arrows while preserving 3D character.
   # The legacy GIF has two tiny chevrons around x=945, y=375.
   # They sit at x=175..184, y=277..291 in this extracted crop.
   # Clear only that non-character region; the large single arrow is drawn later.
   ImageDraw.Draw(frame).rectangle((166,259,194,308),fill=(0,0,0,0))
   frame=brighten(frame)
   frame=soften_pawny_reflections(frame)
   frame=frame.resize((int(frame.width*1.08),int(frame.height*1.08)),Image.Resampling.LANCZOS)
   out.append((elapsed,frame))
   elapsed+=max(20,int(im.info.get("duration") or 100))
   if elapsed>=6300:break
 print(path,"sampled source frames",len(out))
 chosen=[]
 j=0
 for i in range(SLOT*FPS):
  t=i*1000/FPS
  while j+1<len(out) and out[j+1][0]<=t:j+=1
  chosen.append(out[j][1])
 return chosen

def multiline_text(d, greeting, kind, fg):
 # The rotating greeting lives entirely in the LEFT column, below the identity.
 # One row, one language, no secondary language labels. Never overlap Pawny.
 left=42
 baseline=351
 max_width=520
 if kind=="hindi":
  parts=re.split(r"([A-Za-z]+)",greeting)
  for size in range(64,32,-1):
   runs=[(part,font("latin" if re.fullmatch(r"[A-Za-z]+",part) else "hindi",size)) for part in parts if part]
   width=sum(f.getlength(part) for part,f in runs)
   if width<=max_width:break
  if width>max_width:raise ValueError("Hindi greeting exceeds left column")
  x=left
  for part,f in runs:
   d.text((round(x),baseline),part,font=f,fill=fg,anchor="ls")
   x+=f.getlength(part)
 else:
  for size in range(64,32,-1):
   f=font(kind,size)
   if f.getlength(greeting)<=max_width:break
  if f.getlength(greeting)>max_width:raise ValueError("Greeting exceeds left column")
  d.text((left,baseline),greeting,font=f,anchor="ls",fill=fg)

def render(theme,sprite,language,step):
 dark=theme=="dark"
 bg=(13,17,23) if dark else (255,255,255)
 fg=(245,248,252) if dark else (24,30,41)
 muted=(187,199,215) if dark else (76,88,104)
 accent=(255,96,120) if dark else (201,33,72)
 out=Image.new("RGBA",(W,H),bg+(255,))
 d=ImageDraw.Draw(out)
 d.text((35,69),"Pranay Kadu",font=font("latin",65),fill=fg,anchor="ls")
 d.text((38,111),"Backend Software Engineer",font=font("latin",27),fill=muted,anchor="ls")
 d.text((38,149),"Java · Spring Boot · Distributed Systems · AWS",font=font("latin",17),fill=muted,anchor="ls")
 d.line([(38,174),(570,174)],fill=accent,width=3)
 _,greeting,kind=LANG[language]
 multiline_text(d,greeting,kind,fg)
 out.alpha_composite(sprite,(704,28))
 # The single arrow is next to Pawny and matches his vivid red armor.
 pawny_red=(231,38,48)
 ax=999
 top=317+int(5*math.sin((step/FPS)*math.tau/2.8))
 d.line([(ax,top),(ax,top+58)],fill=pawny_red,width=9,joint="curve")
 d.line([(ax-20,top+41),(ax,top+61),(ax+20,top+41)],fill=pawny_red,width=9,joint="curve")
 # A shared bottom rail centers the footer across both columns, clear of Pawny.
 d.line([(42,475),(1078,475)],fill=(50,62,76) if dark else (210,218,229),width=1)
 d.text((560,514),"PROJECTS · SKILLS · CONTRIBUTIONS",font=font("latin",19),fill=muted,anchor="mm")
 return out.convert("RGB")

def build(theme):
 src=ASSETS/("spawny-readme-v16-"+theme+".gif")
 sprites=read_motions(src)
 frames=[render(theme,sprites[i],language,i) for language in range(5) for i in range(SLOT*FPS)]
 still=ASSETS/("pawny-readme-v25-"+theme+"-still.png")
 frames[0].save(still,optimize=True)
 pal=frames[0].quantize(colors=256,method=Image.Quantize.MEDIANCUT)
 indexed=[f.quantize(palette=pal,dither=Image.Dither.NONE) for f in frames]
 dest=ASSETS/("pawny-readme-v25-"+theme+".gif")
 indexed[0].save(dest,save_all=True,append_images=indexed[1:],duration=[170 if i%3!=2 else 160 for i in range(len(indexed))],loop=0,optimize=True,disposal=2)
 # Verify animation contains enough frames/time for all five language slots.
 with Image.open(dest) as result:
  total=0
  for i in range(result.n_frames):
   result.seek(i)
   total+=result.info.get("duration",0)
  assert abs(total-30000)<=50,(theme,total)
 print("Generated",dest,dest.stat().st_size,"bytes",total,"ms")

if __name__=="__main__":
 for theme in ("dark","light"):build(theme)
