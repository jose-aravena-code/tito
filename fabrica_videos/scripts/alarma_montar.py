"""Mezcla la prueba 3D de 4 segundos con diálogos y efectos propios."""
from pathlib import Path
import json
import subprocess
import wave
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'exportaciones/alarma_prueba'
AUDIO=ROOT/'recursos/audios'
SR=48000

def speech(name,maximum):
 p=AUDIO/(name+'.mp3')
 # Quita únicamente silencio exterior, no pausas dentro de las palabras.
 trim='silenceremove=start_periods=1:start_duration=0.02:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_duration=0.02:start_threshold=-45dB,areverse'
 args=['ffmpeg','-v','error','-i',str(p),'-af',trim,'-ar',str(SR),'-ac','1','-f','f32le','-']
 a=np.frombuffer(subprocess.check_output(args),dtype='<f4').copy()
 if len(a)/SR>maximum:
  speed=len(a)/SR/maximum
  if speed>1.3:raise RuntimeError('El diálogo no cabe de forma natural')
  args[args.index('-af')+1]=trim+f',atempo={speed}'
  a=np.frombuffer(subprocess.check_output(args),dtype='<f4').copy()
 rms=np.sqrt(np.mean(a*a));a*=.15/max(rms,.001)
 return a

def main():
 frames=OUT/'frames'
 missing=[i for i in range(1,97) if not (frames/f'frame_{i:04}.png').exists()]
 if missing:raise RuntimeError(f'Faltan {len(missing)} fotogramas; el render aún no termina')
 t=np.arange(4*SR)/SR
 rng=np.random.default_rng(7)
 mix=np.zeros(len(t))
 # Notas cortas originales, sin canciones ni bibliotecas de audio externas.
 for start,note in [(0,220),(.5,277), (1,330),(1.5,220),(2.3,440),(2.8,330),(3.4,277)]:
  x=t-start;env=np.exp(-np.maximum(x,0)*9)*(x>=0)*(x<.4)
  mix+=.035*env*np.sin(2*np.pi*note*x)
 for start,freq in [(.70,1200),(1.15,650),(2.45,180),(3.05,120)]:
  x=t-start;env=np.exp(-np.maximum(x,0)*35)*(x>=0)*(x<.18)
  mix+=env*(.05*np.sin(2*np.pi*freq*x)+.012*rng.normal(0,1,len(t)))
 intervals=[]
 for name,text,start,maximum in [
  ('alarma_humano','Cinco minutitos…',.04,1.48),
  ('alarma_reloj','¡Eso dijiste ayer!',1.68,1.62)]:
  a=speech(name,maximum);k=round(start*SR)
  mix[k:k+len(a)]+=a
  intervals.append({'texto':text,'inicio':start,'fin':start+len(a)/SR})
 mix*=np.clip((4-t)/.08,0,1)
 mix=np.tanh(mix*1.15)*.92
 with wave.open(str(OUT/'mezcla.wav'),'wb') as w:
  w.setnchannels(1);w.setsampwidth(2);w.setframerate(SR)
  w.writeframes((mix*32767).astype('<i2').tobytes())
 (OUT/'dialogos.json').write_text(json.dumps(intervals,ensure_ascii=False,indent=2),encoding='utf-8')
 f='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
 filters=['hqdn3d=3:3:4:4','scale=720:1280:flags=lanczos',
          f"drawtext=fontfile={f}:text='MI ALARMA SE CANSÓ DE MÍ':fontsize=32:fontcolor=white:x=(w-tw)/2:y=100:box=1:boxcolor=0x102333@0.8:boxborderw=14"]
 for s in intervals:
  filters.append(f"drawtext=fontfile={f}:text='{s['texto']}':fontsize=40:fontcolor=white:x=(w-tw)/2:y=1080:box=1:boxcolor=0x102333@0.9:boxborderw=16:enable='between(t,{s['inicio']},{s['fin']})'")
 subprocess.run(['ffmpeg','-y','-v','warning','-framerate','24','-start_number','1',
  '-i',str(frames/'frame_%04d.png'),'-i',str(OUT/'mezcla.wav'),'-vf',','.join(filters),
  '-c:v','libx264','-preset','veryfast','-crf','19','-threads','2','-pix_fmt','yuv420p',
  '-c:a','aac','-b:a','160k','-ac','2','-t','4','-movflags','+faststart',
  str(OUT/'alarma_prueba_4s.mp4')],check=True)
 print(OUT/'alarma_prueba_4s.mp4')

if __name__=='__main__':main()
