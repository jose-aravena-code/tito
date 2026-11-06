"""Adaptador del flujo M1 existente de tito. Nunca descarga modelos ni llama API."""
from pathlib import Path
import os,sys,json,subprocess
P=Path(__file__).resolve().parent;M=Path(os.getenv('SUPERTONIC_MODEL','/workspace/modelos/supertonic3'));SRC=Path(os.getenv('SUPERTONIC_SOURCE','/workspace/supertonic3_fuente'));O=P/'salida';O.mkdir(exist_ok=True)
missing=[str(p) for p in [M/'onnx',M/'voice_styles/M1.json',SRC/'helper.py'] if not p.exists()]
if missing:raise SystemExit('Faltan recursos locales: '+', '.join(missing)+'. No se descargarán automáticamente. Usa el audio incluido o configura SUPERTONIC_MODEL/SUPERTONIC_SOURCE.')
if '--comprobar' in sys.argv:
 print('Modelo, estilo M1 y helper locales presentes. La inferencia se comprueba al generar.');sys.exit(0)
import numpy as np,soundfile as sf,onnxruntime as ort
sys.path.insert(0,str(SRC));from helper import load_cfgs,load_onnx_all,load_text_processor,TextToSpeech,load_voice_style
if (O/'voz_m1_5s.wav').exists():raise SystemExit('Existe audio: usa otra carpeta/version antes de repetir.')
opts=ort.SessionOptions();opts.intra_op_num_threads=3;opts.inter_op_num_threads=1
tts=TextToSpeech(load_cfgs(str(M/'onnx')),load_text_processor(str(M/'onnx')),*load_onnx_all(str(M/'onnx'),opts,['CPUExecutionProvider']));np.random.seed(1271295);style=load_voice_style([str(M/'voice_styles/M1.json')]);text=(P/'narracion.txt').read_text().strip();w,d=tts(text,'es',style,total_step=24,speed=1.1,silence_duration=.08);sr=tts.sample_rate;x=w[0,:round(float(d[0])*sr)];sf.write(O/'voz_m1_original.wav',x,sr,subtype='PCM_16');idx=np.flatnonzero(abs(x)>10**(-44/20));assert len(idx);x=x[max(0,idx[0]-round(.055*sr)):min(len(x),idx[-1]+round(.075*sr))];sf.write(O/'voz_m1_limpia.wav',x,sr);dur=len(x)/sr;tempo=max(1,dur/4.85);assert tempo<1.3,(dur,'No cabe naturalmente en5s: revisar toma, nunca cortar palabras')
af=f'atempo={tempo:.8f},loudnorm=I=-17:TP=-2:LRA=9,aresample=48000,apad,atrim=duration=5'
subprocess.run(['ffmpeg','-y','-v','error','-i',str(O/'voz_m1_limpia.wav'),'-af',af,'-ar','48000','-c:a','pcm_s16le',str(O/'voz_m1_5s.wav')],check=True)
(O/'voz.json').write_text(json.dumps({'modelo':'Supertonic3 M1 local, mismo helper/estilo de tito','texto':text,'velocidad_generacion':1.1,'pasos':24,'duracion_sin_pausas_extremas':dur,'atempo':tempo,'duracion_entrega':5,'descargas':False,'api':False,'coste_servicios':0,'transcripcion':'No requerida para sintetizar. Subtítulos editoriales de prueba; escucha humana pendiente.'},ensure_ascii=False,indent=2));print('VozM1 lista,',dur,'s antes del ajuste',flush=True)
