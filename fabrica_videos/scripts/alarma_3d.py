"""Ejecutar con blender -b -t 4 --python scripts/alarma_3d.py -- [--still]."""
import math
from pathlib import Path
import sys
import bpy
from mathutils import Vector

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'exportaciones/alarma_prueba'
OUT.mkdir(parents=True,exist_ok=True)
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
scene=bpy.context.scene
scene.render.engine='CYCLES'
scene.cycles.device='CPU';scene.cycles.samples=8
# Esta compilación no incluye OpenImageDenoise; se renderiza sin ese módulo.
scene.cycles.use_denoising=False
scene.cycles.max_bounces=3
scene.render.resolution_x=360;scene.render.resolution_y=640
scene.render.resolution_percentage=100
scene.render.fps=24;scene.frame_start=1;scene.frame_end=96
scene.render.image_settings.file_format='PNG'
scene.world.color=(.16,.16,.16)
scene.view_settings.view_transform='AgX'

def mat(name,color):
 m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);return m

skin=mat('piel',(.68,.36,.19));hair=mat('pelo',(.055,.025,.02))
blue=mat('pijama azul',(.04,.25,.65));navy=mat('pantalon',(.025,.07,.17))
red=mat('alarma coral',(.9,.065,.065));cream=mat('marfil',(.95,.86,.65))
white=mat('ojos blancos',(.98,.98,.98));black=mat('pupilas',(.012,.018,.026))
wood=mat('madera',(.38,.17,.07));wall=mat('pared azul',(.10,.21,.31))
floor=mat('suelo',(.13,.16,.20));blanket=mat('manta',(.08,.43,.43))

def empty(name,loc=(0,0,0)):
 o=bpy.data.objects.new(name,None);scene.collection.objects.link(o);o.location=loc;return o

def box(name,loc,scale,material,parent=None,bevel=.06):
 bpy.ops.mesh.primitive_cube_add(size=1,location=(0,0,0));o=bpy.context.object
 o.name=name;o.parent=parent;o.location=loc;o.dimensions=scale
 bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
 o.data.materials.append(material)
 if bevel:
  mod=o.modifiers.new('bordes suaves','BEVEL');mod.width=bevel;mod.segments=3
  o.modifiers.new('normales','WEIGHTED_NORMAL')
 return o

def ball(name,loc,scale,material,parent=None):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=16,ring_count=8)
 o=bpy.context.object;o.name=name;o.parent=parent;o.location=loc;o.scale=scale
 o.data.materials.append(material)
 for p in o.data.polygons:p.use_smooth=True
 return o

def key(o,frame,loc=None,rot=None,scale=None):
 if loc is not None:o.location=loc;o.keyframe_insert('location',frame=frame)
 if rot is not None:o.rotation_euler=rot;o.keyframe_insert('rotation_euler',frame=frame)
 if scale is not None:o.scale=scale;o.keyframe_insert('scale',frame=frame)

box('suelo',(0,0,-.10),(200,200,.2),floor)
box('pared',(0,2.3,2.2),(12,.15,5),wall)
box('cama',(-1.0,1.0,.45),(2.5,1.65,.65),wood)
box('colchon',(-1.0,.95,.83),(2.55,1.7,.3),cream)
box('manta',(-1.0,.75,1.02),(2.56,1.05,.12),blanket)
box('almohada',(-1.0,1.5,1.04),(1.1,.4,.19),white)
box('mesa',(1.15,.12,1.1),(1.05,.8,.16),wood)
for x in [.75,1.55]:
 for y in [-.15,.4]:box('pata mesa',(x,y,.54),(.1,.1,1.05),wood)
# Ventana nocturna, sin texturas externas.
box('ventana marco',(-1.1,2.17,2.8),(1.5,.1,1.45),cream)
box('ventana noche',(-1.1,2.10,2.8),(1.3,.04,1.25),navy)
box('ventana cruz vertical',(-1.1,2.05,2.8),(.05,.04,1.25),cream)
box('ventana cruz horizontal',(-1.1,2.05,2.8),(1.3,.04,.05),cream)

hero=empty('PROTAGONISTA',(-.8,-.25,0))
box('torso',(0,0,1.30),(.72,.42,.82),blue,hero)
box('cuello',(0,0,1.85),(.22,.24,.22),skin,hero)
head=box('cabeza',(0,-.02,2.2),(.85,.65,.85),skin,hero,.13)
box('pelo',(0,.02,2.57),(.88,.67,.24),hair,hero)
for x,z in [(-.28,2.72),(.02,2.77),(.30,2.70)]:
 tuft=box('mechon',(x,.0,z),(.29,.5,.26),hair,hero)
 tuft.rotation_euler[1]=x*.8
eyes=[]
for x in [-.19,.19]:
 box('ojo blanco',(x,-.36,2.24),(.25,.055,.3),white,hero,.035)
 eye=ball('pupila',(x+.02,-.407,2.23),(.065,.025,.09),black,hero);eyes.append(eye)
 brow=box('ceja',(x,-.40,2.47),(.28,.05,.065),hair,hero,.02)
 brow.rotation_euler[1]=-.15 if x<0 else .15
mouth=box('boca',(0,-.371,2.00),(.22,.04,.065),black,hero,.02)
for x in [-.20,.20]:
 box('pierna',(x,0,.59),(.27,.3,.65),navy,hero)
 box('zapatilla',(x,-.10,.21),(.32,.50,.19),cream,hero)
arms=[]
for x in [-.46,.46]:
 pivot=empty('brazo articulado');pivot.parent=hero;pivot.location=(x,0,1.64)
 box('manga',(0,0,-.27),(.22,.30,.58),blue,pivot)
 ball('mano',(0,-.02,-.63),(.13,.13,.14),skin,pivot);arms.append(pivot)
for o in eyes:
 key(o,1,scale=(.065,.025,.03));key(o,49,scale=(.065,.025,.03))
 key(o,59,scale=(.075,.03,.12))
key(mouth,1,scale=(1,1,1));key(mouth,59,scale=(1,1,3))
key(arms[1],1,rot=(0,0,0));key(arms[1],15,rot=(-.1,-2.15,0))
key(arms[1],29,rot=(0,0,0));key(arms[1],60,rot=(0,-2.6,0))
key(arms[0],1,rot=(0,0,0));key(arms[0],60,rot=(0,2.6,0))
key(hero,1,loc=(-.8,-.25,0));key(hero,15,loc=(.15,-.08,.03))
key(hero,29,loc=(-.5,-.25,0));key(hero,40,loc=(-.8,-.25,0));key(hero,51,loc=(-.8,-.25,0))
key(hero,63,loc=(-.95,-.28,.27));key(hero,77,loc=(-1.0,-.28,0))
key(hero,86,loc=(-1.0,-.28,.045));key(hero,96,loc=(-1.0,-.28,0))

alarm=empty('ALARMA',(1.15,.07,1.68))
box('cuerpo reloj',(0,0,0),(.84,.36,.70),red,alarm,.15)
box('cara',(0,-.201,0),(.69,.04,.53),cream,alarm,.08)
for x in [-.21,.21]:
 ball('campana',(x,0,.43),(.21,.18,.14),red,alarm)
 box('pata reloj',(x,0,-.43),(.1,.12,.21),red,alarm,.02)
button=box('boton posponer',(0,0,.43),(.29,.18,.12),white,alarm,.03)
clockeyes=[];brows=[]
for x in [-.16,.16]:
 clockeyes.append(ball('ojo alarma',(x,-.25,.075),(.06,.025,.10),black,alarm))
 brows.append(box('ceja alarma',(x,-.25,.24),(.21,.035,.035),red,alarm,.01))
box('boca alarma',(0,-.25,-.15),(.22,.035,.05),black,alarm,.01)
for o in clockeyes:
 key(o,1,scale=(.06,.025,.014));key(o,23,scale=(.06,.025,.014))
 key(o,30,scale=(.065,.025,.11))
for i,o in enumerate(brows):
 key(o,1,rot=(0,0,0));key(o,34,rot=(0,(-.35 if i==0 else .35),0))
key(button,1,loc=(0,0,.43));key(button,17,loc=(0,0,.38));key(button,23,loc=(0,0,.43))
key(alarm,1,loc=(1.15,.07,1.68));key(alarm,48,loc=(1.15,.07,1.68))
key(alarm,59,loc=(1.13,-.07,2.02),rot=(0,-.15,-.10))
key(alarm,72,loc=(1.10,-.07,1.68),rot=(0,0,0))
key(alarm,80,loc=(1.10,-.07,1.76));key(alarm,89,loc=(1.10,-.07,1.68))

target=empty('mirada camara',(1.05,0,1.78))
bpy.ops.object.camera_add(location=(2.15,-3.5,2.45))
cam=bpy.context.object;scene.camera=cam;cam.data.lens=45
track=cam.constraints.new(type='TRACK_TO');track.target=target;track.track_axis='TRACK_NEGATIVE_Z';track.up_axis='UP_Y'
key(cam,1,loc=(2.15,-3.5,2.45));key(cam,36,loc=(2.0,-3.25,2.4))
key(cam,60,loc=(3.6,-8.2,3.5));key(cam,96,loc=(3.45,-7.8,3.4))
key(target,1,loc=(1.05,0,1.78));key(target,36,loc=(1.05,0,1.78))
key(target,60,loc=(0,0,1.45));key(target,96,loc=(0,0,1.5))

def light(name,loc,power,size,color):
 bpy.ops.object.light_add(type='AREA',location=loc);o=bpy.context.object;o.name=name
 o.data.energy=power;o.data.shape='DISK';o.data.size=size;o.data.color=color
 o.rotation_euler=(Vector((0,0,1.4))-o.location).to_track_quat('-Z','Y').to_euler()
light('principal',(0,-4,6),650,5,(1,.84,.69))
light('relleno',(-4,-1,3),380,4,(.55,.75,1))
light('contraluz',(2,2,5),800,3,(.5,.8,1))
scene.render.filepath=str(OUT/'frames/frame_')
(OUT/'frames').mkdir(exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'alarma.blend'))
if '--still' in sys.argv:
 scene.frame_set(72);scene.render.filepath=str(OUT/'diseno.png')
 bpy.ops.render.render(write_still=True)
else:
 bpy.ops.render.render(animation=True)
