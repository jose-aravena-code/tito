"""Informe reproducible; no cambia permisos, no usa cuentas ni genera audio."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime,timezone
import importlib.util
import json
from pathlib import Path
import shutil
import urllib.error
import urllib.request

ROOT=Path(__file__).resolve().parents[1]
URLS={
 'github_documentacion':'https://raw.githubusercontent.com/QwenLM/Qwen3-TTS/main/README.md',
 'youtube_blog':'https://blog.youtube/culture-and-trends/',
 'tiktok_creative':'https://ads.tiktok.com/business/creativecenter/',
 'google_trends':'https://trends.google.com/trends/',
 'elevenlabs':'https://elevenlabs.io/pricing',
 'modelo_qwen':'https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign/raw/main/config.json',
 'minimax':'https://www.minimax.io/',
 'instagram':'https://www.instagram.com/reel/DfNxUfkJZu_/' }

def consultar(item):
 nombre,url=item
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=12) as r:
   r.read(100);return nombre,{'url':url,'http':r.status,'resultado':'respuesta recibida'}
 except urllib.error.HTTPError as e:
  return nombre,{'url':url,'http':e.code,'resultado':'respuesta HTTP de error; causa no determinada'}
 except urllib.error.URLError as e:
  estado='proxy rechaza CONNECT con 403' if 'Tunnel connection failed: 403' in str(e.reason) else 'fallo de conexión; causa no determinada'
  return nombre,{'url':url,'resultado':estado}
 except Exception as e:return nombre,{'url':url,'resultado':type(e).__name__}

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--red',action='store_true')
 p.add_argument('--salida',type=Path,default=ROOT/'registros/diagnostico_actual.json');args=p.parse_args()
 report={'observado_utc':datetime.now(timezone.utc).isoformat(),
  'programas_encontrados':{n:bool(shutil.which(n)) for n in ['ffmpeg','ffprobe','blender']},
  'modulos_en_este_python':{n:importlib.util.find_spec(n) is not None for n in ['numpy','PIL','edge_tts','kokoro_onnx']},
  'modelos_locales':{'kokoro':Path('/workspace/modelos/kokoro/kokoro-v1.0.onnx').is_file(),
   'qwen_config':Path('/workspace/modelos/qwen-voicedesign/config.json').is_file()},
  'nota':'Encontrar un programa/configuración no certifica inferencia; respuestas web no prueban publicación del entorno.'}
 policy=Path('/etc/codex/network-policy.json')
 if policy.is_file():
  data=json.loads(policy.read_text());report['politica_archivo_arranque']={
   'tipo':data.get('http_network_policy',{}).get('type'),
   'nota':'Instantánea de arranque; consultar la herramienta de estado para configuración observada actual.'}
 if args.red:
  with ThreadPoolExecutor(max_workers=4) as pool:report['consultas']=dict(pool.map(consultar,URLS.items()))
 args.salida.parent.mkdir(parents=True,exist_ok=True)
 args.salida.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
 print(json.dumps(report,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
