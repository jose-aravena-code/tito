"""Paquete descargable explícito, sin cachés, entornos ni credenciales."""
from pathlib import Path
import zipfile

ROOT=Path(__file__).resolve().parents[1]

def main():
 target=Path('/workspace/fabrica_alarma_proyecto.zip')
 scripts=['alarma_3d.py','alarma_montar.py','alarma_historia_3d.py',
  'alarma_historia_voz.py','alarma_historia_montar.py','alarma_historia_comprobar.py',
  'producir_alarma.py','empaquetar_alarma.py']
 files=[ROOT/'ALARMA.md',ROOT/'requirements.txt',ROOT/'configuracion/alarma_historia.json',
  ROOT/'subtitulos/alarma_final.srt',ROOT/'subtitulos/alarma_final.ass',
  ROOT/'registros/alarma_historia_validacion.json',ROOT/'exportaciones/alarma_prueba/alarma.blend']
 files += [ROOT/'scripts'/s for s in scripts]
 files += list((ROOT/'recursos/audios').glob('alarma_full_*.mp3'))
 files += [ROOT/'recursos/audios'/s for s in ['alarma_humano.mp3','alarma_reloj.mp3']]
 files += [ROOT/f'exportaciones/alarma_final/escena_{i}/escena.blend' for i in range(2,7)]
 if not all(p.is_file() for p in files):raise RuntimeError('Faltan archivos; terminar y validar antes de empaquetar')
 with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED) as z:
  for p in files:z.write(p,'fabrica_videos/'+p.relative_to(ROOT).as_posix())
  z.write('/workspace/la_alarma_cobra_vida_ligera.mp4','la_alarma_cobra_vida_ligera.mp4')
  z.writestr('LEEME.txt','Proyecto de microcomedia: La alarma cobra vida.\n'
   'Abre el MP4 para ver el episodio. Las instrucciones están en fabrica_videos/ALARMA.md.\n'
   'El código fue probado en la nube. No necesitas instalar Blender en tu PC para ver el vídeo.\n'
   'Las carpetas de fotogramas y los programas instalados no se incluyen; se generan con los scripts.\n')
 with zipfile.ZipFile(target) as z:
  bad=z.testzip()
  if bad:raise RuntimeError('Error en el ZIP: '+bad)
 print(target,target.stat().st_size,'bytes')

if __name__=='__main__':main()
