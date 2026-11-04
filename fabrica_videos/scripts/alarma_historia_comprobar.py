"""Validación del episodio completo y de su copia ligera."""
import json
from pathlib import Path
import subprocess
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'exportaciones/alarma_final'
CFG=json.loads((ROOT/'configuracion/alarma_historia.json').read_text(encoding='utf-8'))

def inspect(path,width,height):
 d=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(path)],text=True))
 v=next(s for s in d['streams'] if s['codec_type']=='video')
 a=next(s for s in d['streams'] if s['codec_type']=='audio')
 assert (v['width'],v['height'])==(width,height)
 assert v['codec_name']=='h264' and a['codec_name']=='aac'
 assert v['pix_fmt']=='yuv420p' and int(v['nb_frames'])==528
 assert abs(float(d['format']['duration'])-22)<.05
 subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(path),'-f','null','-'],check=True)
 scan=subprocess.run(['ffmpeg','-hide_banner','-i',str(path),'-vf','blackdetect=d=0.05:pix_th=0.08:pic_th=0.98',
  '-an','-f','null','-'],capture_output=True,text=True,check=True)
 assert 'black_start:' not in scan.stderr
 pcm=subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-vn','-ac','1','-ar','16000','-f','f32le','-'])
 samples=np.frombuffer(pcm,dtype='<f4');rms=float(np.sqrt(np.mean(samples*samples)))
 peak=float(np.max(np.abs(samples)));assert rms>.01 and peak<1
 differences=[]
 for s in CFG['escenas']:
  middle=s['inicio']+s['duracion']/2;frames=[]
  for at in [middle-.25,middle+.25]:
   raw=subprocess.check_output(['ffmpeg','-v','error','-ss',str(at),'-i',str(path),'-frames:v','1',
    '-vf','scale=90:160','-pix_fmt','rgb24','-f','rawvideo','-'])
   frames.append(np.frombuffer(raw,dtype=np.uint8).astype(float))
  delta=float(np.mean(np.abs(frames[0]-frames[1])));assert delta>.1
  differences.append(round(delta,3))
 return {'archivo':str(path),'bytes':path.stat().st_size,'duracion':float(d['format']['duration']),
  'resolucion':[width,height],'fps_salida':24,'codecs':['h264','aac'],
  'decodificacion_completa':'correcta','negros_accidentales_detectados':False,
  'audio_rms_dbfs':round(float(20*np.log10(rms)),2),'audio_peak_dbfs':round(float(20*np.log10(peak)),2),
  'movimiento_por_escena':differences}

def main():
 events=json.loads((OUT/'dialogos_finales.json').read_text(encoding='utf-8'))
 assert len(events)==12
 for i,d in enumerate(events):
  assert 0<=d['inicio']<d['fin']<=22
  assert d['fin']<=d.get('fin_subtitulo',d['fin'])<=22
  if i:assert d['inicio']>=events[i-1]['fin']
  if i:assert d['inicio']>=events[i-1].get('fin_subtitulo',events[i-1]['fin'])
 srt=(ROOT/'subtitulos/alarma_final.srt').read_text(encoding='utf-8')
 for d in events:assert d['texto'] in srt
 reports=[inspect(OUT/'la_alarma_cobra_vida.mp4',720,1280),
  inspect(Path('/workspace/la_alarma_cobra_vida_ligera.mp4'),360,640)]
 report={'resultados':reports,'dialogos_y_bloques_subtitulos':12,
  'render_nativo':[360,640],'animacion':{'introduccion':24,'escenas_nuevas':12},
  'revision_humana_pendiente':['interpretacion de voces','calidad artistica','aprobacion antes de publicar']}
 (ROOT/'registros/alarma_historia_validacion.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
 print(json.dumps(report,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
