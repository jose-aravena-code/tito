"""Funciones comunes sin servicios externos ni dependencias adicionales."""
import json
import os
from pathlib import Path
import shutil
import subprocess

def herramienta(nombre):
    valor=os.environ.get(nombre.upper()) or shutil.which(nombre)
    if not valor:raise RuntimeError(f'No se encuentra {nombre}; configura su ruta antes de continuar')
    return valor

def audios_locales(manifiesto,requeridos):
    p=Path(manifiesto).expanduser().resolve()
    datos=json.loads(p.read_text(encoding='utf-8'))
    if not isinstance(datos,dict):raise ValueError('El manifiesto debe relacionar identificadores con archivos')
    faltan=set(requeridos)-set(datos);sobran=set(datos)-set(requeridos)
    if faltan or sobran:raise ValueError(f'Identificadores incorrectos. Faltan: {sorted(faltan)}; sobran: {sorted(sobran)}')
    resultado={}
    for clave,valor in datos.items():
        if not isinstance(valor,str) or not valor.strip():raise ValueError(f'Ruta vacía para {clave}')
        archivo=Path(valor).expanduser()
        if not archivo.is_absolute():archivo=p.parent/archivo
        archivo=archivo.resolve()
        if not archivo.is_file() or archivo.stat().st_size==0:raise ValueError(f'Audio ausente o vacío: {clave}')
        resultado[clave]=archivo
    return resultado

def tiempos_legibles(eventos,escenas,total):
    """Amplía lectura conservando el inicio de voz y sin invadir otra frase/escena."""
    resultado=[]
    for i,d in enumerate(eventos):
        inicio=float(d['inicio']);fin=float(d['fin'])
        if not 0<=inicio<fin<=total:raise ValueError('Intervalo de voz inválido')
        siguiente=float(eventos[i+1]['inicio']) if i+1<len(eventos) else total
        if siguiente<fin:raise ValueError('Diálogos solapados')
        escena=next((s for s in escenas if s['inicio']<=inicio<s['inicio']+s['duracion']),None)
        if escena is None:raise ValueError('Diálogo fuera de escena')
        if fin>escena['inicio']+escena['duracion']:raise ValueError('La voz rebasa el final de su escena')
        limite_siguiente=siguiente-.05 if i+1<len(eventos) else total
        limite=min(total,limite_siguiente,escena['inicio']+escena['duracion'])
        lectura=max(1.2,len(d['texto'].split())/3.3)
        fin_sub=max(fin,min(limite,max(fin+.15,inicio+lectura)))
        resultado.append(dict(d,fin_subtitulo=fin_sub))
    return resultado

def exportar_ligero(origen,destino,ancho=360,sobrescribir=False):
    origen=Path(origen).resolve();destino=Path(destino).resolve()
    if origen==destino:raise ValueError('La copia ligera debe ser un archivo distinto del original')
    if not origen.is_file():raise ValueError('No existe el vídeo de origen')
    if destino.suffix.lower()!='.mp4':raise ValueError('La salida debe terminar en .mp4')
    if destino.exists() and not sobrescribir:raise FileExistsError('La salida ya existe; usa --sobrescribir para reemplazarla')
    if ancho<120 or ancho%2:raise ValueError('El ancho debe ser par y al menos 120')
    destino.parent.mkdir(parents=True,exist_ok=True)
    # Mantiene proporciones, no amplía vídeos pequeños y usa solo dos hilos.
    subprocess.run([herramienta('ffmpeg'),'-y' if sobrescribir else '-n','-v','error',
        '-i',str(origen),'-map','0:v:0','-map','0:a:0?',
        '-vf',f'scale=min({ancho}\\,iw):-2','-c:v','libx264','-preset','fast',
        '-crf','28','-threads','2','-pix_fmt','yuv420p','-c:a','aac','-b:a','80k',
        '-movflags','+faststart',str(destino)],check=True)
    subprocess.run([herramienta('ffmpeg'),'-v','error','-xerror','-i',str(destino),'-f','null','-'],check=True)
    return destino
