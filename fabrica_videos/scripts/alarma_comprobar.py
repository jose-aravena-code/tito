"""Comprueba el archivo completo de la prueba; no juzga calidad artística."""
import json
from pathlib import Path
import re
import subprocess
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'exportaciones/alarma_prueba'

def main():
 p=OUT/'alarma_prueba_4s.mp4'
 data=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(p)],text=True))
 v=next(s for s in data['streams'] if s['codec_type']=='video')
 a=next(s for s in data['streams'] if s['codec_type']=='audio')
 assert (v['width'],v['height'])==(720,1280)
 assert v['codec_name']=='h264' and a['codec_name']=='aac'
 assert abs(float(data['format']['duration'])-4)<.05
 assert v['nb_frames']=='96'
 subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(p),'-f','null','-'],check=True)
 scan=subprocess.run(['ffmpeg','-hide_banner','-i',str(p),'-vf','blackdetect=d=0.05:pix_th=0.08:pic_th=0.98','-an','-f','null','-'],capture_output=True,text=True,check=True)
 assert 'black_start:' not in scan.stderr
 raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-vn','-ac','1','-ar','16000','-f','f32le','-'])
 samples=np.frombuffer(raw,dtype='<f4')
 rms=float(np.sqrt(np.mean(samples*samples)));peak=float(np.max(np.abs(samples)))
 assert rms>.01 and peak<1
 frames=[]
 for at in [.25,1.25,2.5,3.5]:
  raw=subprocess.check_output(['ffmpeg','-v','error','-ss',str(at),'-i',str(p),'-frames:v','1','-vf','scale=180:320','-pix_fmt','rgb24','-f','rawvideo','-'])
  frames.append(np.frombuffer(raw,dtype=np.uint8).astype(float))
 differences=[float(np.mean(np.abs(x-y))) for x,y in zip(frames[:-1],frames[1:])]
 assert min(differences)>1
 dialogs=json.loads((OUT/'dialogos.json').read_text(encoding='utf-8'))
 for d in dialogs:assert 0<=d['inicio']<d['fin']<=4
 result={'duracion':float(data['format']['duration']),'resolucion':[720,1280],
  'render_nativo':[360,640],'fps':24,'fotogramas':96,'codecs':['h264','aac'],
  'decodificacion_completa':'correcta','intervalos_negros_detectados':False,
  'audio_rms_dbfs':20*np.log10(rms),'audio_peak_dbfs':20*np.log10(peak),
  'movimiento_diferencia_media':differences,'dialogos':dialogs,
  'revision_humana_pendiente':['naturalidad de voces','estilo de personajes','fluidez percibida']}
 (ROOT/'registros/alarma_validacion.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
 print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
