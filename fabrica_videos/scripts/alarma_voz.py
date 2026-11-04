"""Genera los dos diálogos de la prueba; conserva los archivos completos."""
import asyncio
import os
from pathlib import Path
import edge_tts
import edge_tts.communicate as provider

ROOT=Path(__file__).resolve().parents[1]

async def main():
 ca=os.environ.get('SSL_CERT_FILE')
 if ca and Path(ca).is_file():provider._SSL_CTX.load_verify_locations(cafile=ca)
 for name,text,voice in [
  ('alarma_humano','Cinco minutitos...','es-MX-JorgeNeural'),
  ('alarma_reloj','¡Eso dijiste ayer!','es-MX-DaliaNeural')]:
  path=ROOT/'recursos/audios'/(name+'.mp3')
  if path.exists() and path.stat().st_size>1000:continue
  temporary=path.with_suffix('.partial.mp3')
  for attempt in range(3):
   try:
    await edge_tts.Communicate(text,voice=voice,rate='+10%',
      proxy=os.environ.get('HTTPS_PROXY')).save(str(temporary))
    if temporary.stat().st_size<1000:raise RuntimeError('Audio insuficiente')
    temporary.replace(path);break
   except edge_tts.exceptions.NoAudioReceived:
    temporary.unlink(missing_ok=True)
    if attempt==2:raise
    await asyncio.sleep(1)

if __name__=='__main__':asyncio.run(main())
