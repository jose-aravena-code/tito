"""Comparación de seis voces Edge TTS; sin música, efectos ni cambio de tono."""
import argparse
import asyncio
import json
import os
from pathlib import Path
import subprocess
import wave
import numpy as np
from PIL import Image,ImageDraw,ImageFont
import edge_tts
import edge_tts.communicate as provider

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'exportaciones/comparacion_voces'
FINAL=Path('/workspace/comparacion_voces.mp4')
ENGINE_LABELS=None
PHRASE='¿Cinco minutitos más? ¡Eso dijiste ayer! Vamos, que llegamos tarde.'
VOICES=[('Jorge','México','Masculina','es-MX-JorgeNeural'),
 ('Álvaro','España','Masculina','es-ES-AlvaroNeural'),
 ('Lorenzo','Chile','Masculina','es-CL-LorenzoNeural'),
 ('Dalia','México','Femenina','es-MX-DaliaNeural'),
 ('Elvira','España','Femenina','es-ES-ElviraNeural'),
 ('Catalina','Chile','Femenina','es-CL-CatalinaNeural')]

async def generate():
 ca=os.environ.get('SSL_CERT_FILE')
 if ca and Path(ca).is_file():provider._SSL_CTX.load_verify_locations(cafile=ca)
 OUT.mkdir(parents=True,exist_ok=True)
 for i,(name,country,gender,voice) in enumerate(VOICES):
  p=OUT/f'{i+1:02}_{voice}.mp3'
  if p.exists() and p.stat().st_size>1000:continue
  tmp=p.with_suffix('.partial.mp3')
  for attempt in range(3):
   try:
    await edge_tts.Communicate(PHRASE,voice=voice,rate='+0%',pitch='+0Hz',
      proxy=os.environ.get('HTTPS_PROXY'),connect_timeout=15,receive_timeout=30).save(str(tmp))
    if tmp.stat().st_size<1000:raise RuntimeError('Audio vacío')
    tmp.replace(p);print(name,'generado',flush=True);break
   except edge_tts.exceptions.NoAudioReceived:
    tmp.unlink(missing_ok=True)
    if attempt==2:raise
    await asyncio.sleep(1+attempt)

def call(args):subprocess.run(args,check=True)

def font(n):return ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',n)

def center(d,text,y,n,color):
 f=font(n);d.text(((360-d.textlength(text,font=f))/2,y),text,font=f,fill=color)

def main():
 p=argparse.ArgumentParser();p.add_argument('--generar',action='store_true');args=p.parse_args()
 if args.generar:asyncio.run(generate())
 OUT.mkdir(parents=True,exist_ok=True)
 parts=[];timeline=[];start=0;audio_parts=[]
 colors=['#53c8ed','#ffba6a','#80dda7','#ffa7cb','#cab5ff','#f3d56a']
 for i,(name,country,gender,voice) in enumerate(VOICES):
  mp3=OUT/f'{i+1:02}_{voice}.mp3'
  raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(mp3),'-ar','48000','-ac','1','-f','f32le','-'])
  a=np.frombuffer(raw,dtype='<f4').copy()
  rms=float(np.sqrt(np.mean(a*a)));peak=float(np.max(np.abs(a)))
  if rms<.001:raise RuntimeError('Voz vacía')
  a*=min(.11/rms,.75/peak)
  a=np.concatenate([np.zeros(19200),a,np.zeros(28800)])
  # Ajuste solo de silencio para que la duración sea múltiplo de fotograma.
  n=int(np.ceil(len(a)/48000*24));a=np.pad(a,(0,n*2000-len(a)))
  length=len(a)/48000
  audio_parts.append(a)
  wav=OUT/f'voz_{i+1}.wav'
  with wave.open(str(wav),'wb') as w:
   w.setnchannels(1);w.setsampwidth(2);w.setframerate(48000);w.writeframes((a*32767).astype('<i2').tobytes())
  im=Image.new('RGB',(360,640),'#101b2b');d=ImageDraw.Draw(im);accent=colors[i]
  d.rounded_rectangle((22,26,338,614),radius=22,outline=accent,width=2)
  center(d,'COMPARACIÓN DE VOCES',53,20,'#edf4fc')
  engine=ENGINE_LABELS[i] if ENGINE_LABELS else 'EDGE TTS'
  center(d,f'{i+1} / {len(VOICES)}  ·  {engine}',96,17,accent)
  center(d,name,166,43,accent);center(d,country,225,25,'white')
  center(d,gender+' · tono normal',265,16,'#c3cede')
  d.rounded_rectangle((39,319,321,487),radius=14,fill='#1d2e44')
  for j,line in enumerate(['¿Cinco minutitos más?','¡Eso dijiste ayer!','Vamos, que llegamos','tarde.']):
   center(d,line,340+j*32,20,'white')
  center(d,'Misma frase · sin música',526,17,accent)
  center(d,'Elige por nombre o número',562,16,'#c3cede')
  image=OUT/f'tarjeta_{i+1}.png';im.save(image)
  part=OUT/f'muestra_{i+1}.mp4'
  call(['ffmpeg','-y','-v','error','-loop','1','-framerate','24','-i',str(image),'-i',str(wav),
   '-c:v','libx264','-preset','fast','-crf','27','-tune','stillimage','-threads','2','-pix_fmt','yuv420p',
   '-c:a','aac','-b:a','96k','-ac','2','-t',str(length),'-movflags','+faststart',str(part)])
  timeline.append({'numero':i+1,'nombre':name,'pais':country,'motor':engine,'voz':voice,'inicio':start,'fin':start+length})
  start+=length;parts.append(part)
 listing=OUT/'partes.txt';listing.write_text(''.join(f"file '{p.name}'\nduration {s['fin']-s['inicio']:.9f}\n" for p,s in zip(parts,timeline)),encoding='utf-8')
 # Codificar el audio una sola vez evita discontinuidades AAC entre muestras.
 joined=OUT/'comparacion.wav'
 with wave.open(str(joined),'wb') as w:
  w.setnchannels(1);w.setsampwidth(2);w.setframerate(48000)
  w.writeframes((np.concatenate(audio_parts)*32767).astype('<i2').tobytes())
 final=FINAL
 call(['ffmpeg','-y','-v','error','-f','concat','-safe','0','-i',str(listing),'-i',str(joined),
  '-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','96k','-ac','2',
  '-t',str(start),'-movflags','+faststart',str(final)])
 call(['ffmpeg','-v','error','-xerror','-i',str(final),'-f','null','-'])
 (OUT/'indice.json').write_text(json.dumps({'frase':PHRASE,'velocidad':'normal','tono':'normal','musica':False,'voces':timeline},ensure_ascii=False,indent=2),encoding='utf-8')
 print(final,final.stat().st_size,'bytes',flush=True)

if __name__=='__main__':main()
