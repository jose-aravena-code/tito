"""Voces de la historia completa. No regenera fragmentos existentes válidos."""
import asyncio
import json
import os
from pathlib import Path
import edge_tts
import edge_tts.communicate as provider

ROOT=Path(__file__).resolve().parents[1]

async def main():
 ca=os.environ.get('SSL_CERT_FILE')
 if ca and Path(ca).is_file():provider._SSL_CTX.load_verify_locations(cafile=ca)
 cfg=json.loads((ROOT/'configuracion/alarma_historia.json').read_text(encoding='utf-8'))
 for d in cfg['dialogos']:
  p=ROOT/'recursos/audios'/(d['archivo']+'.mp3')
  if p.exists() and p.stat().st_size>1000:continue
  temp=p.with_suffix('.partial.mp3')
  for attempt in range(3):
   try:
    await edge_tts.Communicate(d['texto'],voice=d['voz'],rate='+10%',
      proxy=os.environ.get('HTTPS_PROXY'),connect_timeout=15,receive_timeout=30).save(str(temp))
    if temp.stat().st_size<1000:raise RuntimeError('Audio insuficiente')
    temp.replace(p);print(d['archivo'],'generado',flush=True);break
   except edge_tts.exceptions.NoAudioReceived:
    temp.unlink(missing_ok=True)
    if attempt==2:raise
    print(d['archivo'],'respuesta vacía; reintento',attempt+1,flush=True)
    await asyncio.sleep(1+attempt)

if __name__=='__main__':asyncio.run(main())
