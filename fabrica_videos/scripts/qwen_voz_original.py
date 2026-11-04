"""Diseño original por texto, en CPU. No usa una muestra de ElevenLabs."""
import argparse
import json
import os
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
CFG=json.loads((ROOT/'configuracion/qwen_voces_originales.json').read_text(encoding='utf-8'))
MODEL=Path('/workspace/modelos/qwen-voicedesign')

def main():
 p=argparse.ArgumentParser();p.add_argument('--descargar',action='store_true');p.add_argument('--solo-comprobar',action='store_true')
 args=p.parse_args()
 if args.descargar:
  from huggingface_hub import snapshot_download
  # Solo repositorio público oficial y tensores seguros, sin código remoto.
  snapshot_download(CFG['modelo'],local_dir=MODEL,
   ignore_patterns=['*.bin','*.pt','*.pth','*.onnx','*.gguf'])
 config=MODEL/'config.json'
 if not config.exists():
  raise SystemExit('Falta el modelo oficial. No se ha generado audio. Aplicar permiso de huggingface.co antes de descargar.')
 if not any(MODEL.glob('*.safetensors')):
  raise SystemExit('No están completos los pesos safetensors del modelo.')
 if args.solo_comprobar:
  print('Configuración y pesos locales presentes. La inferencia todavía debe probarse.');return
 import torch
 import soundfile as sf
 import numpy as np
 from qwen_tts import Qwen3TTSModel
 torch.set_num_threads(4)
 model=Qwen3TTSModel.from_pretrained(str(MODEL),device_map='cpu',
  dtype=torch.float32,attn_implementation='eager')
 out=ROOT/'exportaciones/qwen_voces_originales';out.mkdir(parents=True,exist_ok=True)
 for i,v in enumerate(CFG['perfiles'],start=1):
  torch.manual_seed(v['semilla'])
  waves,sr=model.generate_voice_design(text=CFG['texto'],language=CFG['idioma'],
   instruct=v['instruccion'],max_new_tokens=256)
  a=np.asarray(waves[0],dtype=np.float32)
  if len(a)<sr or not np.isfinite(a).all():raise RuntimeError('Audio inválido')
  sf.write(out/f'{i}_{v["nombre"]}.wav',a,sr)
  print(v['nombre'],len(a)/sr,'segundos',flush=True)

if __name__=='__main__':main()
