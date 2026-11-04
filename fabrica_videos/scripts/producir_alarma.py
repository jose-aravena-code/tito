"""Reanuda el episodio: render, voces, mezcla y validación. No publica."""
from pathlib import Path
import shutil
import subprocess
import sys
import argparse
import json
from utilidades_medios import audios_locales

ROOT=Path(__file__).resolve().parents[1]

def run(args):subprocess.run(args,cwd=ROOT,check=True)

def ready(folder,n):
 return all((folder/f'frame_{i:04}.png').exists() and
  (folder/f'frame_{i:04}.png').stat().st_size>1000 for i in range(1,n+1))

def main():
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--audios-locales',type=Path)
 args=parser.parse_args()
 if args.audios_locales:
  cfg=json.loads((ROOT/'configuracion/alarma_historia.json').read_text(encoding='utf-8'))
  args.audios_locales=args.audios_locales.resolve()
  audios_locales(args.audios_locales,[d['archivo'] for d in cfg['dialogos']])
 blender=shutil.which('blender')
 if not blender:raise RuntimeError('Blender no está disponible; este flujo se prepara en la nube')
 first=ROOT/'exportaciones/alarma_prueba'
 if not (first/'alarma.blend').exists() or not ready(first/'frames',96):
  run([blender,'-b','-t','4','--python',str(ROOT/'scripts/alarma_3d.py')])
 for shot,n in [(2,36),(3,36),(4,36),(5,48),(6,60)]:
  if not ready(ROOT/f'exportaciones/alarma_final/escena_{shot}/frames',n):
   run([blender,'-b','-t','4','--python',str(ROOT/'scripts/alarma_historia_3d.py'),'--','--shot',str(shot)])
 if not args.audios_locales:
  run([sys.executable,str(ROOT/'scripts/alarma_historia_voz.py')])
 montage=[sys.executable,str(ROOT/'scripts/alarma_historia_montar.py')]
 if args.audios_locales:montage+=['--audios-locales',str(args.audios_locales)]
 run(montage)
 run([sys.executable,str(ROOT/'scripts/alarma_historia_comprobar.py')])

if __name__=='__main__':main()
