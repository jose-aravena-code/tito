"""Reanuda el episodio: render, voces, mezcla y validación. No publica."""
from pathlib import Path
import shutil
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]

def run(args):subprocess.run(args,cwd=ROOT,check=True)

def ready(folder,n):
 return all((folder/f'frame_{i:04}.png').exists() and
  (folder/f'frame_{i:04}.png').stat().st_size>1000 for i in range(1,n+1))

def main():
 blender=shutil.which('blender')
 if not blender:raise RuntimeError('Blender no está disponible; este flujo se prepara en la nube')
 first=ROOT/'exportaciones/alarma_prueba'
 if not (first/'alarma.blend').exists() or not ready(first/'frames',96):
  run([blender,'-b','-t','4','--python',str(ROOT/'scripts/alarma_3d.py')])
 for shot,n in [(2,36),(3,36),(4,36),(5,48),(6,60)]:
  if not ready(ROOT/f'exportaciones/alarma_final/escena_{shot}/frames',n):
   run([blender,'-b','-t','4','--python',str(ROOT/'scripts/alarma_historia_3d.py'),'--','--shot',str(shot)])
 run([sys.executable,str(ROOT/'scripts/alarma_historia_voz.py')])
 run([sys.executable,str(ROOT/'scripts/alarma_historia_montar.py')])
 run([sys.executable,str(ROOT/'scripts/alarma_historia_comprobar.py')])

if __name__=='__main__':main()
