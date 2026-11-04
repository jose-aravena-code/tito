"""Comparación real de Edge TTS y Kokoro, sin APIs de pago."""
from pathlib import Path
import shutil
import subprocess
import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro
import comparar_voces as comparison

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'exportaciones/comparacion_motores'

def main():
 OUT.mkdir(parents=True,exist_ok=True)
 for i,name in enumerate(['es-ES-AlvaroNeural','es-CL-LorenzoNeural']):
  old=ROOT/'exportaciones/comparacion_voces'/f'{i+2:02}_{name}.mp3'
  shutil.copyfile(old,OUT/f'{i+1:02}_{name}.mp3')
 k=Kokoro('/workspace/modelos/kokoro/kokoro-v1.0.onnx','/workspace/modelos/kokoro/voices-v1.0.bin')
 available=k.get_voices()
 for i,voice in enumerate(['em_alex','em_santa'],start=3):
  if voice not in available:raise RuntimeError('Voz no disponible: '+voice)
  wav=OUT/f'{voice}.wav'
  if not wav.exists():
   samples,sr=k.create(comparison.PHRASE,voice=voice,speed=1.0,lang='es')
   if not np.isfinite(samples).all() or len(samples)<sr:raise RuntimeError('Síntesis inválida')
   sf.write(wav,samples,sr)
   print(voice,round(len(samples)/sr,2),'segundos',flush=True)
  subprocess.run(['ffmpeg','-y','-v','error','-i',str(wav),'-c:a','libmp3lame',
   '-q:a','2',str(OUT/f'{i:02}_{voice}.mp3')],check=True)
 comparison.OUT=OUT
 comparison.FINAL=Path('/workspace/comparacion_edge_kokoro.mp4')
 comparison.VOICES=[('Álvaro','España','Masculina','es-ES-AlvaroNeural'),
  ('Lorenzo','Chile','Masculina','es-CL-LorenzoNeural'),
  ('Alex','Español','Masculina','em_alex'),('Santa','Español','Masculina','em_santa')]
 comparison.ENGINE_LABELS=['EDGE TTS','EDGE TTS','KOKORO ONNX','KOKORO ONNX']
 comparison.main()

if __name__=='__main__':main()
