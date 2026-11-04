#!/usr/bin/env python3
"""Render a real, animated 3D floating EVE-style robot into GitHub-friendly GIFs.
Procedural 3D meshes echo the user-supplied EVE reference; the uploaded 3D-print
STL collection is not embedded in the repository.
"""
from functools import cache
from pathlib import Path
import math, re
import vtk
import numpy as np
from vtk.util.numpy_support import numpy_to_vtk, vtk_to_numpy
from PIL import Image, ImageDraw, ImageFont

ASSETS=Path(__file__).resolve().parents[1]/"assets"
ASSETS.mkdir(exist_ok=True)
WIDTH,HEIGHT=1120,545
FPS=25
SECONDS=6
ASSET_PREFIX="eve-readme-v7"
WORK_PROMPT="Explore Pranay’s work"
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
@cache
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

def articulated_hand():
 hand=vtk.vtkAssembly()
 hand.SetPosition(-.255,-.070,-1.065)
 shell=(.968,.976,1)
 hand.AddPart(ellipsoid((0,0,-.155),(.203,.105,.191),shell,.19))
 fingers=[]
 for x,z,length in ((-.135,-.284,.235),(0,-.284,.296),(.135,-.284,.313),(.171,-.115,.212)):
  joint=vtk.vtkAssembly()
  joint.SetPosition(x,-.030,z)
  joint.AddPart(ellipsoid((0,0,-.40*length),(.053,.052,.56*length),shell,.18))
  hand.AddPart(joint)
  fingers.append(joint)
 return hand,fingers

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

def eye_lens():
 sphere=vtk.vtkSphereSource()
 sphere.SetRadius(1)
 sphere.SetThetaResolution(48);sphere.SetPhiResolution(32)
 sphere.Update()
 mesh=sphere.GetOutput()
 unit=vtk_to_numpy(mesh.GetPoints().GetData()).copy()
 # A dim cyan rim and a brighter center are built into the lens, without glare.
 facing=np.maximum(0,-unit[:,1:2])
 rim=np.array([8,126,174])
 center=np.array([44,235,255])
 mesh.GetPointData().SetScalars(numpy_to_vtk((rim+facing*(center-rim)).astype(np.uint8),deep=True))
 mapper=vtk.vtkPolyDataMapper()
 mapper.SetInputData(mesh)
 mapper.SetColorModeToDirectScalars()
 return mesh.GetPoints(),unit,mapper

class EVE:
 def __init__(self,theme):
  self.renderer=vtk.vtkRenderer()
  self.renderer.SetBackground(*((.051,.067,.09) if theme=="dark" else (1,1,1)))
  self.window=vtk.vtkRenderWindow()
  self.window.SetSize(504,405)
  self.window.SetOffScreenRendering(True)
  self.window.AddRenderer(self.renderer)
  self.window.SetMultiSamples(4)
  self.root=vtk.vtkAssembly()
  self.renderer.AddActor(self.root)
  self.root.AddPart(teardrop())
  self.head=vtk.vtkAssembly()
  self.head.SetPosition(0,0,2.93)
  self.head.AddPart(ellipsoid((0,0,0),(.9,.66,.63),(.972,.98,1),.24))
  self.head.AddPart(ellipsoid((0,-.568,.035),(.725,.155,.385),(.012,.021,.038),.37))
  self.root.AddPart(self.head)
  self.eye_points,self.eye_shape,eye_mapper=eye_lens()
  self.eyes=[]
  for side in (-1,1):
   eye=vtk.vtkActor()
   eye.SetMapper(eye_mapper)
   eye.GetProperty().LightingOff()
   eye.SetOrientation(0,-6*side,0)
   self.head.AddPart(eye)
   self.eyes.append(eye)
  self.arms={}
  for side in (-1,1):
   assembly=vtk.vtkAssembly()
   arm=ellipsoid((side*.20,0,-.59),(.205,.265,.83),(.968,.976,1),.22)
   arm.SetOrientation(0,-6*side,-15*side)
   assembly.SetPosition(.79*side,0,1.90)
   assembly.AddPart(arm);self.root.AddPart(assembly)
   self.arms[side]=assembly
   if side==-1:
    self.active_fin=arm
  self.hand,self.fingers=articulated_hand()
  self.arms[-1].AddPart(self.hand)
  lighting=1 if theme=="dark" else .78
  for position,intensity,color in [
   ((4,-6,8),.92,(1,1,1)),
   ((-4,-3,4),.42,(.78,.86,1)),
   ((1,4,6),.36,(.78,.90,1)),
   ((0,-2,10),.24,(.92,.96,1)),
  ]:
   light=vtk.vtkLight()
   light.SetPosition(*position);light.SetFocalPoint(0,0,1.8)
   light.SetIntensity(lighting*intensity);light.SetColor(*color)
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
  """Ease in and out with zero velocity and acceleration at both ends."""
  v=min(1.0,max(0.0,(t-start)/(end-start)))
  return v**3*(10+v*(-15+6*v))

 def frame(self,t):
  # EVE's right hand appears on screen left. Keep the root and other fin still.
  lift=self.ease(t,.08,.95)*(1-self.ease(t,1.94,2.68))
  sway=self.ease(t,.58,.94)*(1-self.ease(t,1.78,2.10))
  phase=math.tau*1.4*(t-.82)
  point=self.ease(t,2.63,3.46)*(1-self.ease(t,4.88,5.80))
  sweep=self.ease(t,3.23,5.09)
  self.arms[-1].SetOrientation(0,4+124*lift+15*sway*math.sin(phase)+(29-10*sweep)*point,
                               6*sway*math.cos(phase))

  # The palm slides out of the shell. Only the index finger stays extended to point.
  open_palm=self.ease(t,.32,.87)*(1-self.ease(t,1.98,2.58))
  point_palm=self.ease(t,2.88,3.43)*(1-self.ease(t,4.91,5.62))
  extension=open_palm+point_palm
  curl=self.ease(t,2.82,3.22)*(1-self.ease(t,5.19,5.64))
  self.active_fin.SetScale(.410,.530,1.66-.28*extension)
  self.active_fin.SetPosition(-.20,0,-.59+.04*extension)
  self.hand.SetVisibility(extension>0)
  size=max(.001,extension)
  self.hand.SetScale(size,size,size)
  self.hand.SetOrientation(0,point*(-3+18*sweep)+4*sway*math.sin(phase),0)
  for finger,spread,fold in zip(self.fingers,(11,0,-9,-43),(112,105,0,98)):
   finger.SetOrientation(-fold*curl,spread*(1-curl),0)

  glance=self.ease(t,2.50,3.23)*(1-self.ease(t,4.82,5.66))
  idle_phase=math.tau*t/SECONDS
  self.head.SetPosition(0,0,2.93+.037*math.sin(2*idle_phase))
  self.head.SetOrientation((4+3*sweep)*glance,-4*lift-4*glance+.6*math.sin(idle_phase),0)
  smile=self.ease(t,.18,.86)*(1-self.ease(t,1.98,2.63))
  blink=self.ease(t,2.30,2.44)*(1-self.ease(t,2.48,2.64))
  openness=1-.94*blink
  x,y,z=self.eye_shape.T
  lens=vtk_to_numpy(self.eye_points.GetData())
  lens[:,0]=(.124+.043*smile)*x
  lens[:,1]=.020*y+.025*x*x
  lens[:,2]=openness*((.094-.066*smile)*z+.068*smile*(1-x*x))
  self.eye_points.GetData().Modified()
  self.eye_points.Modified()
  for side,eye in zip((-1,1),self.eyes):
   eye.SetPosition(side*.268-.070*glance,-.760,.061-(.078+.032*sweep)*glance)
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
 output.paste(sprite,(594,10))
 d=ImageDraw.Draw(output)
 reveal=EVE.ease(t,3.24,3.67)*(1-EVE.ease(t,4.99,5.42))
 if reveal>0:
  prompt=tuple(round(a+(b-a)*reveal) for a,b in zip(bg,fg))
  arrow=tuple(round(a+(b-a)*reveal) for a,b in zip(bg,blue))
  d.text((679,434),WORK_PROMPT,font=font("latin",27),fill=prompt,anchor="ls")
  ax,top=652,406+round(2*math.sin(math.tau*t/SECONDS))
  d.line([(ax,top),(ax,top+32)],fill=arrow,width=5)
  d.line([(ax-10,top+22),(ax,top+32),(ax+10,top+22)],fill=arrow,width=5,joint="curve")
 d.line([(42,474),(1078,474)],fill=(52,63,79) if dark else (210,219,228),width=1)
 d.text((560,514),"PROJECTS · SKILLS · CONTRIBUTIONS",font=font("latin",19),fill=muted,anchor="mm")
 return output

def build(theme):
 print("Rendering EVE",theme,flush=True)
 scene=EVE(theme)
 # Render one six-second cycle, then replay it with each greeting.
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
 wave_frame=round(1.15*FPS)
 point_frame=round(4.12*FPS)
 assert ImageChops.difference(sprites[0],sprites[wave_frame]).getbbox() is not None
 assert ImageChops.difference(sprites[0],sprites[point_frame]).getbbox() is not None
 # Show the work prompt in the English reduced-motion fallback.
 composite(theme,sprites[point_frame],0,point_frame/FPS).save(ASSETS/f"{ASSET_PREFIX}-{theme}-still.png",optimize=True)
 montage=Image.new("RGB",(WIDTH,HEIGHT*len(LANG)))
 for language,i in enumerate((0,wave_frame,point_frame,0,wave_frame)):
  montage.paste(composite(theme,sprites[i],language,i/FPS),(0,language*HEIGHT))
 pal=montage.quantize(colors=256,method=Image.Quantize.MEDIANCUT)
 indexed=(composite(theme,sprite,language,i/FPS).quantize(palette=pal,dither=Image.Dither.NONE)
          for language in range(len(LANG)) for i,sprite in enumerate(sprites))
 out=ASSETS/f"{ASSET_PREFIX}-{theme}.gif"
 next(indexed).save(out,save_all=True,append_images=indexed,loop=0,duration=1000//FPS,optimize=True,disposal=1)
 with Image.open(out) as result:
  total=0
  for i in range(result.n_frames):
   result.seek(i);total+=result.info.get("duration",0)
  assert total==1000*SECONDS*len(LANG),(total,theme)
 print("Wrote",out,out.stat().st_size,flush=True)

if __name__=="__main__":
 for mode in ("dark","light"):build(mode)
