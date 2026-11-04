"""Copia MP4 pequeña de cualquier vídeo; funciona sin conexión."""
import argparse
from pathlib import Path
from utilidades_medios import exportar_ligero

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('video',type=Path);p.add_argument('--salida',type=Path)
    p.add_argument('--ancho',type=int,default=360);p.add_argument('--sobrescribir',action='store_true')
    a=p.parse_args();salida=a.salida or a.video.with_name(a.video.stem+'_ligero.mp4')
    resultado=exportar_ligero(a.video,salida,a.ancho,a.sobrescribir)
    print(resultado,resultado.stat().st_size,'bytes')

if __name__=='__main__':main()
