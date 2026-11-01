#!/usr/bin/env python3
"""Build GitHub-compatible 3D-rendered Pawny GIFs, with one readable greeting at a time."""
from pathlib import Path
import math
import os
import re
from PIL import Image, ImageDraw, ImageEnhance, ImageFont

ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/"assets"
W,H=1120,640
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
   ImageDraw.Draw(frame).rectangle((195,238,255,311),fill=(0,0,0,0))
   frame=brighten(frame)
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
 # All writing uses the same baseline; no extra red language label is shown.
 # Fit the complete greeting inside the independent 470px-wide banner header.
 cx=860
 baseline=121
 max_width=454
 if kind=="hindi":
  parts=re.split(r"([A-Za-z]+)",greeting)
  for size in range(60,30,-1):
   runs=[(part,font("latin" if re.fullmatch(r"[A-Za-z]+",part) else "hindi",size)) for part in parts if part]
   total=sum(f.getlength(part) for part,f in runs)
   if total<=max_width:break
  x=cx-total/2
  for part,f in runs:
   d.text((round(x),baseline),part,font=f,fill=fg,anchor="ls")
   x+=f.getlength(part)
 else:
  for size in range(60,30,-1):
   f=font(kind,size)
   if f.getlength(greeting)<=max_width:break
  d.text((cx,baseline),greeting,font=f,anchor="ms",fill=fg)

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
 d.text((38,269),"A friendly hello.",font=font("latin",31),fill=accent,anchor="ls")
 d.text((38,312),"Then, explore my work.",font=font("latin",31),fill=fg,anchor="ls")
 d.text((40,470),"FIVE LANGUAGES · ONE FRIENDLY GUIDE",font=font("latin",16),fill=muted,anchor="ls")
 _,greeting,kind=LANG[language]
 multiline_text(d,greeting,kind,fg)
 out.alpha_composite(sprite,(704,184))
 # Large 60px down arrow, with a subtle secondary chevron.
 ax=1061
 top=432+int(5*math.sin((step/FPS)*math.tau/2.8))
 d.line([(ax,top),(ax,top+58)],fill=accent,width=9,joint="curve")
 d.line([(ax-20,top+41),(ax,top+61),(ax+20,top+41)],fill=accent,width=9,joint="curve")
 d.line([(ax-14,top+83),(ax,top+96),(ax+14,top+83)],fill=accent,width=5)
 d.text((858,610),"PROJECTS · SKILLS · CONTRIBUTIONS",font=font("latin",18),fill=muted,anchor="mm")
 return out.convert("RGB")

def build(theme):
 src=ASSETS/("spawny-readme-v16-"+theme+".gif")
 sprites=read_motions(src)
 frames=[render(theme,sprites[i],language,i) for language in range(5) for i in range(SLOT*FPS)]
 still=ASSETS/("pawny-readme-v19-"+theme+"-still.png")
 frames[0].save(still,optimize=True)
 pal=frames[0].quantize(colors=256,method=Image.Quantize.MEDIANCUT)
 indexed=[f.quantize(palette=pal,dither=Image.Dither.NONE) for f in frames]
 dest=ASSETS/("pawny-readme-v19-"+theme+".gif")
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
