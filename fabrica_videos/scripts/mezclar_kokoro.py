"""Mezcla estilos de Kokoro antes de sintetizar; no superpone audios."""
from pathlib import Path
import json
import subprocess
import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro
import comparar_voces as comparison

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'exportaciones/mezclas_kokoro'

def main():
 OUT.mkdir(parents=True,exist_ok=True)
 model=Kokoro('/workspace/modelos/kokoro/kokoro-v1.0.onnx','/workspace/modelos/kokoro/voices-v1.0.bin')
 alex=model.get_voice_style('em_alex');santa=model.get_voice_style('em_santa')
 assert alex.shape==santa.shape
 rows=[];manifest=[]
 for i,weight in enumerate([.75,.50,.25],start=1):
  code=f'mezcla_{i}'
  style=(weight*alex+(1-weight)*santa).astype(np.float32)
  samples,sr=model.create(comparison.PHRASE,voice=style,speed=1.0,lang='es')
  assert np.isfinite(samples).all() and len(samples)>sr
  wav=OUT/f'{code}.wav';sf.write(wav,samples,sr)
  subprocess.run(['ffmpeg','-y','-v','error','-i',str(wav),'-c:a','libmp3lame','-q:a','2',
   str(OUT/f'{i:02}_{code}.mp3')],check=True)
  label=f'{round(weight*100)}% Alex + {round((1-weight)*100)}% Santa'
  rows.append((f'Mezcla {i}',label,'Masculina',code))
  manifest.append({'numero':i,'alex':weight,'santa':1-weight,'duracion_voz':len(samples)/sr})
  print(label,round(len(samples)/sr,2),'segundos',flush=True)
 comparison.OUT=OUT;comparison.FINAL=Path('/workspace/mezclas_alex_santa.mp4')
 comparison.VOICES=rows;comparison.ENGINE_LABELS=['KOKORO · MEZCLA']*3
 comparison.main()
 (OUT/'mezclas.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')

if __name__=='__main__':main()
