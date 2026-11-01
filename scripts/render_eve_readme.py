#!/usr/bin/env python3
"""Render a real, animated 3D floating EVE-style robot into GitHub-friendly GIFs.
Procedural 3D meshes echo the user-supplied EVE reference; the uploaded 3D-print
STL collection is not embedded in the repository.
"""
from pathlib import Path
import math, os, re
import vtk
import numpy as np
from vtk.util.numpy_support import vtk_to_numpy
from PIL import Image, ImageDraw, ImageFont

ASSETS=Path(__file__).resolve().parents[1]/"assets"
ASSETS.mkdir(exist_ok=True)
WIDTH,HEIGHT=1120,545
FPS=4
SECONDS=6
LANG=[
 ("Hey, I am EVE.","latin"),
 ("你好，我是 EVE。","chinese"),
 ("नमस्ते, मैं EVE हूँ।","hindi"),
 ("¡Hola! Soy EVE.","latin"),
 ("Salut, je suis EVE.","latin"),
]
FONTS={
 "latin":"/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
 "chinese":"/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
 "hindi":"/usr/share/fonts/truetype/noto/NotoSansDevanagari-Bold.ttf",
}
def font(kind,size):
 return ImageFont.truetype(FONTS[kind],size,layout_engine=ImageFont.Layout.RAQM)

def mesh_actor(mapper,color,spec=.28,ambient=.20):
 # Softer satin-polymer finish rather than hard plastic hotspots.
 actor=vtk.vtkActor()
 actor.SetMapper(mapper)
 prop=actor.GetProperty()
 prop.SetColor(*color)
 prop.SetDiffuse(.82);prop.SetAmbient(ambient)
 prop.SetSpecular(spec);prop.SetSpecularPower(22)
 prop.SetInterpolationToPhong()
 return actor

def ellipsoid(center,radii,color,spec=.5):
 sphere=vtk.vtkSphereSource()
 sphere.SetThetaResolution(92);sphere.SetPhiResolution(70)
 mapper=vtk.vtkPolyDataMapper()
 mapper.SetInputConnection(sphere.GetOutputPort())
 actor=mesh_actor(mapper,color,spec)
 # The VTK sphere primitive has radius 0.5.
 actor.SetScale(*(r*2 for r in radii))
 actor.SetPosition(*center)
 return actor

def teardrop():
 pts=vtk.vtkPoints();cells=vtk.vtkCellArray()
 rings=65;sides=80
 for i in range(rings):
  t=(i+.001)/(rings-.999)
  z=.26+2.02*t
  envelope=math.sin(math.pi*t)**.64
  rx=.82*envelope*(.84+.26*t)
  ry=.56*envelope*(.86+.18*t)
  for j in range(sides):
   ang=2*math.pi*j/sides
   pts.InsertNextPoint(rx*math.cos(ang),ry*math.sin(ang),z)
 for i in range(rings-1):
  for j in range(sides):
   ids=[i*sides+j,i*sides+(j+1)%sides,(i+1)*sides+(j+1)%sides,(i+1)*sides+j]
   quad=vtk.vtkQuad()
   for k,idx in enumerate(ids):quad.GetPointIds().SetId(k,idx)
   cells.InsertNextCell(quad)
 poly=vtk.vtkPolyData();poly.SetPoints(pts);poly.SetPolys(cells)
 normals=vtk.vtkPolyDataNormals()
 normals.SetInputData(poly);normals.ConsistencyOn()
 normals.AutoOrientNormalsOn();normals.SplittingOff()
 mapper=vtk.vtkPolyDataMapper()
 mapper.SetInputConnection(normals.GetOutputPort())
 return mesh_actor(mapper,(.965,.975,1),.24)

def glowing_eye(cx):
 pts=vtk.vtkPoints();lines=vtk.vtkCellArray()
 n=24
 for i in range(n):
  t=-1+2*i/(n-1)
  pts.InsertNextPoint(cx+.17*t,-.765+.026*t*t,2.988+.075*(1-t*t))
 lines.InsertNextCell(n)
 for i in range(n):lines.InsertCellPoint(i)
 poly=vtk.vtkPolyData();poly.SetPoints(pts);poly.SetLines(lines)
 tube=vtk.vtkTubeFilter()
 tube.SetInputData(poly);tube.SetRadius(.028)
 tube.SetNumberOfSides(14);tube.CappingOn()
 mapper=vtk.vtkPolyDataMapper();mapper.SetInputConnection(tube.GetOutputPort())
 return mesh_actor(mapper,(.10,.82,1),.08,.92)

class EVE:
 def __init__(self,theme):
  self.renderer=vtk.vtkRenderer()
  self.renderer.SetBackground(*((.051,.067,.09) if theme=="dark" else (1,1,1)))
  self.window=vtk.vtkRenderWindow()
  self.window.SetSize(400,405)
  self.window.SetOffScreenRendering(True)
  self.window.AddRenderer(self.renderer)
  self.window.SetMultiSamples(4)
  self.root=vtk.vtkAssembly()
  self.renderer.AddActor(self.root)
  self.root.AddPart(teardrop())
  self.head=ellipsoid((0,0,2.93),(.9,.66,.63),(.972,.98,1),.24)
  self.root.AddPart(self.head)
  self.root.AddPart(ellipsoid((0,-.568,2.965),(.725,.155,.385),(.012,.021,.038),.37))
  self.eyes=[glowing_eye(-.28),glowing_eye(.28)]
  for eye in self.eyes:self.root.AddPart(eye)
  self.arms={}
  for side in (-1,1):
   assembly=vtk.vtkAssembly()
   arm=ellipsoid((side*.20,0,-.59),(.205,.265,.83),(.968,.976,1),.22)
   arm.SetOrientation(0,-6*side,-15*side)
   assembly.SetPosition(.79*side,0,1.90)
   assembly.AddPart(arm);self.root.AddPart(assembly)
   self.arms[side]=assembly
  for position,intensity,color in [
   ((4,-6,8),.92,(1,1,1)),
   ((-4,-3,4),.42,(.78,.86,1)),
   ((1,4,6),.36,(.78,.90,1)),
   ((0,-2,10),.24,(.92,.96,1)),
  ]:
   light=vtk.vtkLight()
   light.SetPosition(*position);light.SetFocalPoint(0,0,1.8)
   light.SetIntensity(intensity);light.SetColor(*color)
   self.renderer.AddLight(light)
  cam=self.renderer.GetActiveCamera()
  cam.SetPosition(0,-11,2.12);cam.SetFocalPoint(0,0,1.96)
  cam.SetViewUp(0,0,1);cam.ParallelProjectionOn()
  cam.SetParallelScale(2.24)
  self.filter=vtk.vtkWindowToImageFilter()
  self.filter.SetInput(self.window)
  self.filter.SetInputBufferTypeToRGB()
  self.filter.ReadFrontBufferOff()
 @staticmethod
 def ease(t,start,end):
  """Cubic ease with finite ramps: readable in a 4 FPS GIF."""
  v=min(1.0,max(0.0,(t-start)/(end-start)))
  return v*v*(3-2*v)

 def frame(self,t):
  # Only ONE fin is ever animated: the screen-left fin (side=-1).
  # It waves hello and later points left toward Pranay's profile details.
  # Screen-right fin (side=+1) and the root assembly remain absolutely
  # stationary throughout the 30-second looping GIF. This avoids the
  # appearance that both hands are waving or moving.
  wave=self.ease(t,.12,.55)*(1-self.ease(t,1.75,2.18))
  point=self.ease(t,2.45,2.98)*(1-self.ease(t,4.95,5.82))
  self.root.SetPosition(0,0,0)
  self.root.SetOrientation(0,0,0)
  self.head.SetOrientation(0,0,-4.5*point+.6*math.sin(2*math.pi*t/4.5))

  # One fin handles both actions; the other fin is never transformed.
  # A slow 1 Hz wobble remains readable when exported at 4 fps.
  waving_angle=98+17*math.sin(2*math.pi*1.05*t)
  single_fin_angle=(wave*waving_angle)+(point*104)
  self.arms[-1].SetOrientation(0,4+single_fin_angle,0)

  for eye in self.eyes:
   eye.SetVisibility(not abs(t%5-3.85)<.13)
  self.window.Render()
  self.filter.Modified();self.filter.Update()
  data=self.filter.GetOutput()
  w,h,_=data.GetDimensions()
  pixels=vtk_to_numpy(data.GetPointData().GetScalars()).reshape(h,w,3)
  return Image.fromarray(np.flipud(pixels).copy(),"RGB")

def greeting(draw,text,kind,fill):
 left=42;baseline=350;max_width=520
 if kind=="hindi":
  parts=re.split(r"([A-Za-z]+)",text)
  for size in range(62,29,-1):
   runs=[(p,font("latin" if re.fullmatch("[A-Za-z]+",p) else "hindi",size)) for p in parts if p]
   width=sum(f.getlength(p) for p,f in runs)
   if width<=max_width:break
  if width>max_width:raise ValueError("Hindi text too wide")
  x=left
  for p,f in runs:
   draw.text((round(x),baseline),p,font=f,fill=fill,anchor="ls")
   x+=f.getlength(p)
 else:
  for size in range(62,29,-1):
   f=font(kind,size)
   if f.getlength(text)<=max_width:break
  if f.getlength(text)>max_width:raise ValueError("Greeting too wide")
  draw.text((left,baseline),text,font=f,fill=fill,anchor="ls")

def composite(theme,sprite,language,t):
 dark=theme=="dark"
 bg=(13,17,23) if dark else (255,255,255)
 fg=(246,248,252) if dark else (26,31,41)
 muted=(185,196,211) if dark else (76,88,105)
 blue=(21,189,255) if dark else (10,117,205)
 output=Image.new("RGB",(WIDTH,HEIGHT),bg)
 d=ImageDraw.Draw(output)
 d.text((35,69),"Pranay Kadu",font=font("latin",65),fill=fg,anchor="ls")
 d.text((38,111),"Backend Software Engineer",font=font("latin",27),fill=muted,anchor="ls")
 d.text((38,149),"Java · Spring Boot · Distributed Systems · AWS",font=font("latin",17),fill=muted,anchor="ls")
 d.line([(38,174),(568,174)],fill=blue,width=3)
 greeting(d,*LANG[language],fg)
 output.paste(sprite,(646,10))
 d=ImageDraw.Draw(output)
 # Exactly one arrow, close to EVE, matching the blue eyes.
 ax=1008;top=309+int(4*math.sin(2*math.pi*t/3.2))
 d.line([(ax,top),(ax,top+57)],fill=blue,width=8,joint="curve")
 d.line([(ax-18,top+39),(ax,top+58),(ax+18,top+39)],fill=blue,width=8,joint="curve")
 d.line([(42,474),(1078,474)],fill=(52,63,79) if dark else (210,219,228),width=1)
 d.text((560,514),"PROJECTS · SKILLS · CONTRIBUTIONS",font=font("latin",19),fill=muted,anchor="mm")
 return output

def build(theme):
 print("Rendering EVE",theme,flush=True)
 scene=EVE(theme)
 # Render all 24 motion samples once; replay the same gesture with each language.
 # Capture the non-gesturing fin's transform and verify it never changes.
 stationary_fin=scene.arms[1]
 initial_orientation=stationary_fin.GetOrientation()
 initial_position=stationary_fin.GetPosition()
 initial_root=scene.root.GetPosition()
 sprites=[scene.frame(i/FPS) for i in range(SECONDS*FPS)]
 assert tuple(stationary_fin.GetOrientation())==tuple(initial_orientation), "Other fin must not rotate"
 assert tuple(stationary_fin.GetPosition())==tuple(initial_position), "Other fin must not move"
 assert tuple(scene.root.GetPosition())==tuple(initial_root), "Root hover must not move both fins"
 # Both gestures must have visible motion from their own resting pose.
 from PIL import ImageChops
 assert ImageChops.difference(sprites[0],sprites[4]).getbbox() is not None
 assert ImageChops.difference(sprites[8],sprites[14]).getbbox() is not None
 frames=[composite(theme,sprites[i],language,i/FPS) for language in range(5) for i in range(SECONDS*FPS)]
 # Static accessibility fallback shows a welcoming raised fin in English.
 frames[3].save(ASSETS/f"eve-readme-v4-{theme}-still.png",optimize=True)
 if theme=="dark":
  # Exact animation poses for reviewer-visible quality assurance.
  frames[4].save(ASSETS/"eve-readme-v4-wave.png",optimize=True)
  frames[14].save(ASSETS/"eve-readme-v4-point.png",optimize=True)
 montage=Image.new("RGB",(WIDTH,HEIGHT*5))
 for k in range(5):montage.paste(frames[k*SECONDS*FPS],(0,k*HEIGHT))
 pal=montage.quantize(colors=256,method=Image.Quantize.MEDIANCUT)
 indexed=[f.quantize(palette=pal,dither=Image.Dither.NONE) for f in frames]
 out=ASSETS/f"eve-readme-v4-{theme}.gif"
 indexed[0].save(out,save_all=True,append_images=indexed[1:],loop=0,duration=250,optimize=True,disposal=2)
 with Image.open(out) as result:
  total=0
  for i in range(result.n_frames):
   result.seek(i);total+=result.info.get("duration",0)
  assert total==30000,(total,theme)
 print("Wrote",out,out.stat().st_size,flush=True)

if __name__=="__main__":
 for mode in ("dark","light"):build(mode)
