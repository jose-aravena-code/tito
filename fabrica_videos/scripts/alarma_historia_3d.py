"""Escenas adicionales de La alarma cobra vida. Blender, sin recursos externos."""
import argparse
import math
from pathlib import Path
import sys
import bpy
from mathutils import Vector

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'exportaciones/alarma_final'
BASE=ROOT/'exportaciones/alarma_prueba/alarma.blend'
SPECS={2:('persecucion',3),3:('almohada',3),4:('camino',3),5:('oficina',4),6:('jefe',5)}

def key(o,f,loc=None,rot=None,scale=None):
 for prop,value in [('location',loc),('rotation_euler',rot),('scale',scale)]:
  if value is not None:
   setattr(o,prop,value);o.keyframe_insert(prop,frame=f)

def box(name,loc,size,material):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=name
 o.dimensions=size;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
 o.data.materials.append(material)
 mod=o.modifiers.new('bordes','BEVEL');mod.width=.06;mod.segments=2
 o.modifiers.new('normales','WEIGHTED_NORMAL');return o

def material(name,c):
 m=bpy.data.materials.new(name);m.diffuse_color=(*c,1);return m

def text(label,loc,size,mat):
 bpy.ops.object.text_add(location=loc,rotation=(math.pi/2,0,0))
 o=bpy.context.object;o.data.body=label;o.data.align_x='CENTER';o.data.size=size
 o.data.extrude=.008;o.data.materials.append(mat);return o

def tree(o):
 return [o]+[z for c in o.children for z in tree(c)]

def clone(root,name):
 mapping={}
 for o in tree(root):
  c=o.copy()
  if o.data:c.data=o.data.copy()
  c.animation_data_clear();bpy.context.scene.collection.objects.link(c);mapping[o]=c
 for o,c in mapping.items():
  c.parent=mapping.get(o.parent);c.matrix_basis=o.matrix_basis.copy()
 mapping[root].name=name;return mapping[root]

def reset_camera(target,position,focus):
 cam=bpy.context.scene.camera;cam.location=position;target.location=focus;cam.data.lens=44

def rig(root):
 legs=[]
 shoes=sorted([o for o in root.children if o.name.startswith('zapatilla')],key=lambda o:o.location.x)
 for i,o in enumerate(sorted([o for o in root.children if o.name.startswith('pierna')],key=lambda o:o.location.x)):
  pivot=bpy.data.objects.new('cadera',None);bpy.context.scene.collection.objects.link(pivot)
  pivot.parent=root;pivot.location=(o.location.x,0,.9)
  o.parent=pivot;o.location=(0,0,-.31)
  shoes[i].parent=pivot;shoes[i].location=(0,-.1,-.69);legs.append(pivot)
 return legs

def run(root,legs,arms,start,end,n,angle=0):
 root.rotation_euler=(0,0,angle)
 for f in range(1,n+1,2):
  p=(f-1)/max(1,n-1);s=math.sin(p*math.pi*12)
  loc=Vector(start).lerp(Vector(end),p);loc.z+=abs(s)*.12
  key(root,f,loc=loc,rot=(.08*s,0,angle+.035*s))
  for i,leg in enumerate(legs):key(leg,f,rot=(s*.7*(-1 if i else 1),0,0))
  for i,arm in enumerate(arms):key(arm,f,rot=(-s*.9*(-1 if i else 1),0,.12*(-1 if i else 1)))

def build(shot):
 bpy.ops.wm.open_mainfile(filepath=str(BASE));s=bpy.context.scene;s.frame_set(72)
 for o in s.objects:o.animation_data_clear()
 hero=bpy.data.objects['PROTAGONISTA'];alarm=bpy.data.objects['ALARMA']
 target=bpy.data.objects['mirada camara']
 hero.location=(-.8,-.25,0);hero.rotation_euler=(0,0,0)
 alarm.location=(1.1,-.2,.55);alarm.rotation_euler=(0,0,0)
 arms=sorted([o for o in hero.children if o.name.startswith('brazo articulado')],key=lambda o:o.location.x)
 for o in arms:o.rotation_euler=(0,0,0)
 legs=rig(hero)
 for o in hero.children:
  if o.name.startswith('pupila'):o.scale=(.065,.025,.09)
  if o.name=='boca':o.scale=(1,1,1.5)
 # Cejas interiores hacia abajo: expresión de alarma impaciente.
 for o in alarm.children:
  if o.name.startswith('ceja alarma'):o.rotation_euler.y=.30 if o.location.x<0 else -.30
 white=bpy.data.materials['ojos blancos'];wood=bpy.data.materials['madera'];navy=bpy.data.materials['pantalon']
 n=SPECS[shot][1]*12
 if shot>=4:
  keep=set(tree(hero)+tree(alarm)+[target,s.camera])
  keep.update(o for o in s.objects if o.type=='LIGHT' or o.name=='suelo')
  for o in list(s.objects):
   if o not in keep:bpy.data.objects.remove(o,do_unlink=True)
 if shot==2:
  reset_camera(target,(3.3,-8.4,3.5),(0,-.8,1.3))
  run(hero,legs,arms,(-1.25,-1.2,0),(1.05,-1.2,0),n,1.05)
  for f in range(1,n+1,2):
   p=(f-1)/(n-1)
   key(alarm,f,loc=(-2.1+2.3*p,-1.2,.58+abs(math.sin(p*math.pi*7))*.35),rot=(0,math.sin(p*20)*.12,.7))
 elif shot==3:
  reset_camera(target,(2.4,-6.1,3.0),(-.15,-.5,1.6))
  hero.location=(-.8,-.4,0)
  pillow=box('almohada escudo',(-.8,-.95,1.05),(1.55,.28,1.25),white)
  key(pillow,1,loc=(-.8,-.95,1.05));key(pillow,9,loc=(-.8,-.95,2.0));key(pillow,n,loc=(-.8,-.95,2.0))
  for i,o in enumerate(arms):key(o,1,rot=(0,0,0));key(o,9,rot=(-1.5,0,(-.2 if i else .2)))
  for f in range(1,n+1,2):
   p=(f-1)/(n-1);key(alarm,f,loc=(.8,-1.35,.6+abs(math.sin(p*math.pi*3))*.55),rot=(0,0,-.2))
 elif shot==4:
  building=material('fachada',(.18,.31,.42))
  box('oficina exterior',(0,2.8,3.2),(12,.3,10),building)
  box('puerta',(1.4,2.59,1.1),(1.35,.08,2.2),navy)
  text('OFICINA',(0,2.55,3.1),.55,white)
  for x in [-2.5,-1,2.7]:box('ventana exterior',(x,2.57,2.2),(1.0,.06,.75),white)
  reset_camera(target,(3.9,-9.0,3.6),(0,0,1.7))
  run(hero,legs,arms,(-1.3,-.1,0),(.7,-.1,0),n,.9)
  for f in range(1,n+1,2):
   p=(f-1)/(n-1);key(alarm,f,loc=(-2+2*p,-.5,.55+abs(math.sin(p*20))*.15),rot=(0,0,.8))
 elif shot in (5,6):
  wall=material('pared oficina',(.24,.34,.39));box('pared oficina',(0,2.6,3.2),(12,.2,10),wall)
  text('REUNION  08:00',(0,2.43,3.1),.38,white)
  boss=clone(hero,'JEFE');boss.location=(1.1,.4,0)
  jacket=material('camisa jefe',(.55,.20,.09))
  for o in tree(boss):
   if o.type=='MESH':
    for slot in o.material_slots:
     if slot.material and slot.material.name=='pijama azul':slot.material=jacket
  tie=box('corbata',(0,0,0),(.10,.05,.45),navy);tie.parent=boss;tie.location=(0,-.24,1.45)
  blegs=[o for o in boss.children if o.name.startswith('cadera')]
  barms=sorted([o for o in boss.children if o.name.startswith('brazo articulado')],key=lambda o:o.location.x)
  hero.location=(-1.15,-.35,0);alarm.location=(-.25,-.7,.55)
  reset_camera(target,(3.5,-9.0,3.5),(0,0,1.5))
  if shot==5:
   box('escritorio',(1.15,1.0,1.05),(1.85,.9,.13),wood)
   for x in [.4,1.9]:box('pata escritorio',(x,1,.52),(.1,.5,1.0),wood)
   box('pantalla',(1.15,1.0,1.55),(.8,.1,.5),navy)
   key(arms[1],1,rot=(0,0,0));key(arms[1],15,rot=(-.8,-.6,0));key(arms[1],n,rot=(0,0,0))
   for f in range(1,n+1,3):
    key(hero,f,rot=(0,math.sin(f*.3)*.025,0))
    key(boss,f,rot=(0,.025*math.sin(f*.2),0))
  else:
   giant=clone(alarm,'ALARMA DEL JEFE');giant.scale=(3,3,3)
   purple=material('alarma gigante violeta',(.34,.08,.55))
   for o in tree(giant):
    if o.type=='MESH':
     for slot in o.material_slots:
      if slot.material and slot.material.name=='alarma coral':slot.material=purple
   reset_camera(target,(3.0,-11.6,4.1),(.1,.3,1.7))
   run(boss,blegs,barms,(.45,-.5,0),(-.1,-1.0,0),n,-.65)
   for f in range(1,n+1,2):
    p=(f-1)/(n-1)
    key(giant,f,loc=(1.1-.35*p,1.2,1.65+abs(math.sin(p*math.pi*5))*.18),rot=(0,.04*math.sin(p*20),-.10))
    key(hero,f,loc=(-1.2,-.7,abs(math.sin(p*18))*.035))
   for i,o in enumerate(arms):key(o,1,rot=(0,0,0));key(o,15,rot=(0,(-2.5 if i else 2.5),0));key(o,n,rot=(0,(-2.5 if i else 2.5),0))
 # Movimiento suave de cámara adicional, sin marear ni alterar los encuadres.
 cam=s.camera;start=cam.location.copy();key(cam,1,loc=start);key(cam,n,loc=start*Vector((.97,.97,1)))
 s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=4;s.cycles.use_denoising=False
 s.cycles.max_bounces=2;s.render.fps=12;s.frame_start=1;s.frame_end=n
 s.render.resolution_x=360;s.render.resolution_y=640;s.render.resolution_percentage=100
 path=OUT/f'escena_{shot}';(path/'frames').mkdir(parents=True,exist_ok=True)
 s.render.filepath=str(path/'frames/frame_');s.render.image_settings.file_format='PNG'
 bpy.ops.wm.save_as_mainfile(filepath=str(path/'escena.blend'))
 return s,path,n

def main():
 p=argparse.ArgumentParser();p.add_argument('--stills',action='store_true');p.add_argument('--shot',type=int)
 args=p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
 for shot in ([args.shot] if args.shot else SPECS):
  s,path,n=build(shot)
  if args.stills:
   s.frame_set(n//2);s.render.filepath=str(path/'diseno.png');bpy.ops.render.render(write_still=True)
  else:
   # Reanudar sin repetir los fotogramas completos de este mismo diseño.
   for f in range(1,n+1):
    image=path/'frames'/f'frame_{f:04}.png'
    if image.exists() and image.stat().st_size>1000:continue
    s.frame_set(f);s.render.filepath=str(image);bpy.ops.render.render(write_still=True)

if __name__=='__main__':main()
