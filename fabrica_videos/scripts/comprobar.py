"""Validación técnica del MP4. No reemplaza la escucha/revisión humana."""
import argparse
import json
import math
from pathlib import Path
import re
import subprocess

import numpy as np

from montar import ROOT, tool


def check(path, preview=False):
    info=json.loads(subprocess.check_output([
        tool('ffprobe'),'-v','error','-show_format','-show_streams','-of','json',str(path)],text=True))
    video=next(s for s in info['streams'] if s['codec_type']=='video')
    audio=next(s for s in info['streams'] if s['codec_type']=='audio')
    duration=float(info['format']['duration'])
    results={
        'archivo':str(path),'bytes':path.stat().st_size,'duracion':duration,
        'resolucion':[video['width'],video['height']],
        'video':video['codec_name'],'audio':audio['codec_name'],
        'narracion_incluida':not preview,
    }
    assert (video['width'],video['height'])==(720,1280)
    assert video['codec_name']=='h264' and audio['codec_name']=='aac'
    assert video['pix_fmt']=='yuv420p'
    assert 15<=duration<=20
    # Decodifica todo el vídeo y todo el audio, no solo el encabezado.
    subprocess.run([tool('ffmpeg'),'-v','error','-xerror','-i',str(path),
                    '-map','0:v:0','-map','0:a:0','-f','null','-'],check=True)
    results['decodificacion_completa']='correcta'
    scan=subprocess.run([tool('ffmpeg'),'-hide_banner','-i',str(path),'-an',
                         '-vf','blackdetect=d=0.04:pix_th=0.08:pic_th=0.98',
                         '-f','null','-'],capture_output=True,text=True,check=True)
    black=[tuple(map(float,m)) for m in re.findall(
        r'black_start:([\d.]+) black_end:([\d.]+) black_duration:([\d.]+)',scan.stderr)]
    assert all(start>=duration-.25 for start,end,length in black),black
    results['intervalos_negros']=black
    results['negro_permitido']='solo corte final de hasta 0.25 s'
    pcm=subprocess.check_output([tool('ffmpeg'),'-v','error','-i',str(path),
                                 '-vn','-ac','1','-ar','16000','-f','f32le','-'])
    samples=np.frombuffer(pcm,dtype='<f4')
    rms=float(np.sqrt(np.mean(samples**2)))
    peak=float(np.max(np.abs(samples)))
    assert rms>.002 and peak<1.0,(rms,peak)
    results['audio_rms_dbfs']=20*math.log10(rms)
    results['audio_peak_dbfs']=20*math.log10(max(peak,1e-12))
    timeline=json.loads((ROOT/'registros/timeline_usada.json').read_text(encoding='utf-8'))
    assert len(timeline)==5
    for i,s in enumerate(timeline):
        assert 0<=s['start']<s['speech_end']<=s['end']<=duration+.05
        if i:assert abs(s['start']-timeline[i-1]['end'])<.001
    # Comprueba que cada escena cambia de imagen: detectaría una diapositiva fija.
    movement=[]
    for s in timeline:
        frames=[]
        middle=(s['start']+s['end'])/2
        for at in [middle-.2,middle+.2]:
            raw=subprocess.check_output([
                tool('ffmpeg'),'-v','error','-ss',str(at),'-i',str(path),
                '-frames:v','1','-vf','scale=180:320','-pix_fmt','rgb24','-f','rawvideo','-'])
            frames.append(np.frombuffer(raw,dtype=np.uint8).astype(np.float32))
        difference=float(np.mean(np.abs(frames[0]-frames[1])))
        assert difference>.05,('Escena sin movimiento apreciable',difference)
        movement.append(round(difference,3))
    results['movimiento_por_escena_diferencia_media']=movement
    results['subtitulos']='5 bloques; tiempos de escenas provisionales' if preview else '5 bloques ligados a los WAV de narración por escena'
    results['revision_humana_pendiente']=['naturalidad de voz','inteligibilidad de mezcla','aprobacion editorial']
    target=ROOT/'registros'/('validacion_previa.json' if preview else 'validacion_final.json')
    target.write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(results,ensure_ascii=False,indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--preview',action='store_true');args=p.parse_args()
    check(ROOT/'exportaciones'/('wow_PREVIA_SIN_VOZ.mp4' if args.preview else 'wow_final.mp4'),args.preview)
