"""Exporta la historia completa: imagen 3D, diálogos, subtítulos y audio propio."""
import json
import math
import os
from pathlib import Path
import subprocess
import wave
import numpy as np
from alarma_montar import speech, SR

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'exportaciones/alarma_final'
CFG=json.loads((ROOT/'configuracion/alarma_historia.json').read_text(encoding='utf-8'))

def call(args):subprocess.run(args,check=True)

def stamp(t,ass=False):
 if ass:
  cs=round(t*100);return f'{cs//360000}:{cs//6000%60:02}:{cs//100%60:02}.{cs%100:02}'
 ms=round(t*1000);return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}'

def main():
 OUT.mkdir(exist_ok=True,parents=True)
 cache=ROOT/'registros/cache';cache.mkdir(exist_ok=True,parents=True)
 os.environ.setdefault('XDG_CACHE_HOME',str(cache))
 parts=[]
 for scene in CFG['escenas']:
  i=scene['numero'];fps=scene['fps_origen'];n=scene['duracion']*fps
  frames=(ROOT/'exportaciones/alarma_prueba/frames') if i==1 else OUT/f'escena_{i}/frames'
  missing=[f for f in range(1,n+1) if not (frames/f'frame_{f:04}.png').exists()]
  if missing:raise RuntimeError(f'Escena {i}: faltan {len(missing)} fotogramas')
  part=OUT/f'parte_{i}.mp4'
  call(['ffmpeg','-y','-v','error','-framerate',str(fps),'-start_number','1',
   '-i',str(frames/'frame_%04d.png'),'-vf','hqdn3d=5:4:6:5,fps=24',
   '-c:v','libx264','-preset','fast','-crf','18','-threads','2','-pix_fmt','yuv420p',
   '-an','-t',str(scene['duracion']),str(part)])
  parts.append(part)
 concat=OUT/'partes.txt';concat.write_text(''.join(f"file '{p.name}'\n" for p in parts),encoding='utf-8')
 silent=OUT/'historia_sin_audio.mp4'
 call(['ffmpeg','-y','-v','error','-f','concat','-safe','0','-i',str(concat),'-c','copy',str(silent)])

 total=CFG['duracion'];t=np.arange(total*SR)/SR;rng=np.random.default_rng(81)
 bed=np.zeros(len(t));voices=np.zeros(len(t));events=[]
 # Música sencilla de comedia, compuesta por el programa.
 notes=[220,277.18,329.63,277.18,196,246.94,293.66,246.94]
 for j,start in enumerate(np.arange(0,total,.375)):
  x=t-start;env=np.exp(-np.maximum(x,0)*12)*(x>=0)*(x<.32)
  note=notes[j%len(notes)]
  bed+=env*(.022*np.sin(2*np.pi*note*x)+.006*np.sin(2*np.pi*2*note*x))
 for start in np.arange(4.1,6.9,.21).tolist()+np.arange(10.1,12.9,.23).tolist()+np.arange(17.5,19.1,.24).tolist():
  x=t-start;env=np.exp(-np.maximum(x,0)*65)*(x>=0)*(x<.12)
  bed+=env*(.025*rng.normal(0,1,len(t))+.025*np.sin(2*np.pi*110*x))
 for start,freq in [(.7,1200),(1.15,650),(2.45,180),(6.8,160),(8.6,650),(12.8,120),(17.1,85),(19.4,115)]:
  x=t-start;env=np.exp(-np.maximum(x,0)*14)*(x>=0)*(x<.45)
  bed+=env*.055*np.sin(2*np.pi*(freq*x+30*x*x))
 bed[(t>16.75)&(t<17.45)]*=.15
 duck=np.ones(len(t))
 for d in CFG['dialogos']:
  a=speech(d['archivo'],d['maximo']);start=d['inicio'];end=start+len(a)/SR
  if end>total:raise RuntimeError('Voz fuera de duración')
  k=round(start*SR);voices[k:k+len(a)]+=a
  duck[max(0,k-int(.03*SR)):min(len(t),k+len(a)+int(.10*SR))]=.45
  events.append(dict(d,fin=end))
 mix=(voices+bed*duck)*np.minimum(1,t/.025)*np.clip((total-t)/.12,0,1)
 # Margen para los picos entre muestras introducidos por la compresión AAC.
 mix=np.tanh(mix*1.15)*.75
 wav=OUT/'mezcla_final.wav'
 with wave.open(str(wav),'wb') as w:
  w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR)
  w.writeframes((np.stack([mix,mix],axis=1)*32767).astype('<i2').tobytes())
 (OUT/'dialogos_finales.json').write_text(json.dumps(events,ensure_ascii=False,indent=2),encoding='utf-8')
 subtitle=ROOT/'subtitulos/alarma_final.srt'
 subtitle.write_text('\n\n'.join(f'{i+1}\n{stamp(d["inicio"])} --> {stamp(d["fin"])}\n{d["texto"]}' for i,d in enumerate(events))+'\n',encoding='utf-8')
 ass=ROOT/'subtitulos/alarma_final.ass'
 header='''[Script Info]
ScriptType: v4.00+
PlayResX: 720
PlayResY: 1280
WrapStyle: 0
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,DejaVu Sans,44,&H00FFFFFF,&H000000FF,&H00201810,&H80000000,-1,0,0,0,100,100,0,0,1,3,1,2,55,70,170,1
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
'''
 ass.write_text(header+''.join(f'Dialogue: 0,{stamp(d["inicio"],True)},{stamp(d["fin"],True)},Default,,0,0,0,,{d["texto"]}\n' for d in events),encoding='utf-8')
 font='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
 filters=['scale=720:1280:flags=lanczos',f'ass={ass}']
 for s in CFG['escenas']:
  p=OUT/f'titulo_{s["numero"]}.txt';p.write_text(s['texto'],encoding='utf-8')
  end=min(s['inicio']+s['duracion'],21)
  filters.append(f"drawtext=fontfile={font}:textfile={p}:fontsize=31:fontcolor=white:x=(w-tw)/2:y=95:box=1:boxcolor=0x102333@0.85:boxborderw=14:enable='gte(t,{s['inicio']})*lt(t,{end})'")
 p=OUT/'cierre.txt';p.write_text('¿CUÁNTAS VECES POSPONES TÚ?',encoding='utf-8')
 filters.append(f"drawtext=fontfile={font}:textfile={p}:fontsize=30:fontcolor=0xffd477:x=(w-tw)/2:y=95:box=1:boxcolor=0x102333@0.9:boxborderw=14:enable='gte(t,21)'")
 final=OUT/'la_alarma_cobra_vida.mp4'
 call(['ffmpeg','-y','-v','warning','-i',str(silent),'-i',str(wav),'-vf',','.join(filters),
  '-map','0:v:0','-map','1:a:0','-c:v','libx264','-preset','fast','-crf','23','-threads','2',
  '-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-ac','2','-t',str(total),'-movflags','+faststart',str(final)])
 light=Path('/workspace/la_alarma_cobra_vida_ligera.mp4')
 call(['ffmpeg','-y','-v','error','-i',str(final),'-vf','scale=360:640','-c:v','libx264',
  '-preset','fast','-crf','28','-threads','2','-pix_fmt','yuv420p','-c:a','aac','-b:a','80k','-movflags','+faststart',str(light)])
 print(final);print(light)

if __name__=='__main__':main()
