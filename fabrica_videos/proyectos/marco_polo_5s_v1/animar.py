"""Prototipo reproducible y portable. Pillow/NumPy+FFmpeg; sin red ni modelos."""
from pathlib import Path
import json,math,subprocess,shutil,sys
from PIL import Image,ImageDraw
import dibujo_base as B
P=Path(__file__).resolve().parent;O=P/'salida';O.mkdir(exist_ok=True);B.FONT=str(P/'recursos/DejaVuSans-Bold.ttf');B.REG=str(P/'recursos/DejaVuSans.ttf');W,H,FPS=720,1280,24
features=json.loads((P/'recursos/paises.geojson').read_text())['features'];INK=B.INK;GOLD=B.GOLD;WHITE=B.WHITE
CAPS=[(0,1.1,'Marco Polo'),(1.1,2.4,'viajó a China…'),(2.4,5,'¡y volvió veinticuatro años después!')]
def txt(d,s,x,y,n=40,col=WHITE):B.txt(d,s,x,y,n,col,True,2)
def marco(t,old=False):
 sp=B.character(t+.25,'community','walk' if t<3 else 'read','surprise' if not old else 'smile',3);d=ImageDraw.Draw(sp);bob=2*math.sin((t+.25)*2.1)
 d.polygon([(108,171+bob),(112,122+bob),(148,96+bob),(237,107+bob),(288,143+bob),(293,174+bob)],fill='#aa3944',outline=INK,width=5);d.rounded_rectangle((103,165+bob,296,189+bob),radius=6,fill='#d05a52',outline=INK,width=5)
 if old:d.arc((133,226+bob,269,308+bob),0,180,fill='#543c36',width=10)
 return sp

def venice(t):
 im=B.BGS['warm'].copy();d=ImageDraw.Draw(im);d.ellipse((495,210,650,365),fill='#fff0bf')
 for i in range(6):
  x=i*140-30;top=345+(i%3)*36;d.rectangle((x,top,x+122,820),fill=['#d99c76','#ebc79b','#b18d91'][i%3],outline=INK,width=3);d.polygon([(x-5,top),(x+60,top-47),(x+129,top)],fill='#9a4f4c',outline=INK)
  for y in range(top+50,780,100):d.rounded_rectangle((x+38,y,x+77,y+47),radius=17,fill='#385e70')
 d.rectangle((0,830,W,H),fill='#4c99ac');d.rectangle((0,804,490,899),fill='#c7bc93',outline=INK,width=4)
 for j in range(8):
  y=931+j*39;x=45+30*math.sin(t*2+j);d.arc((x,y,x+550,y+26),0,180,fill='#9dd7d3',width=4)
 sp=marco(t);B.paste(im,sp,65,252,430);return im

def map_scene(t):
 im=B.BGS['paper'].copy();tile=Image.new('RGB',(650,708),'#407e95');d=ImageDraw.Draw(tile)
 def q(lon,lat):return ((lon+18)/158*650,(69-lat)/65*708)
 for ft in features:
  g=ft['geometry'];polys=[g['coordinates']] if g['type']=='Polygon' else g['coordinates'] if g['type']=='MultiPolygon' else []
  for poly in polys:
   ring=poly[0]
   if not any(-18<=lon<=140 and 4<=lat<=69 for lon,lat,*_ in ring):continue
   pts=[q(v[0],v[1]) for v in ring];d.polygon(pts,fill='#d8b888',outline='#977a59',width=1)
 route=[(12.33,45.44),(35.2,32.9),(54,32),(75.9,39.5),(116.4,39.9)];pts=[q(*v) for v in route];d.line(pts,fill='#a77a52',width=6,joint='curve');u=B.clamp((t-1.1)/1.9)*(len(pts)-1);j=min(len(pts)-2,int(u));f=u-j;xy=(B.mix(pts[j][0],pts[j+1][0],f),B.mix(pts[j][1],pts[j+1][1],f));d.line(pts[:j+1]+[xy],fill=GOLD,width=7,joint='curve')
 for x,y in [pts[0],pts[-1]]:d.ellipse((x-9,y-9,x+9,y+9),fill='#e5735a',outline=INK,width=3)
 B.paste(tile,marco(t),xy[0]-40,xy[1]-124,80)
 im.paste(tile,(35,285));d=ImageDraw.Draw(im);txt(d,'VENECIA',145,303,23);txt(d,'CHINA',576,611,25);txt(d,'Ruta simbólica · Natural Earth',360,1004,17);return im

def frame(t):
 if t<1.1:im=venice(t);title='24 AÑOS DE VIAJE';label='VENECIA · 1271'
 elif t<3.2:im=map_scene(t);title='RUMBO A ASIA';label='MARCO POLO'
 else:
  im=B.BGS['sun'].copy();d=ImageDraw.Draw(im);d.rounded_rectangle((45,293,675,992),radius=35,fill='#f7e5ba',outline=INK,width=5);txt(d,'1271 → 1295',360,340,50,INK);txt(d,'24 AÑOS',360,431,81,INK);B.paste(im,marco(t,True),180,462,350);title='EL REGRESO A VENECIA';label='EL VIAJE COMPLETO'
 d=ImageDraw.Draw(im);B.tag(d,label,35,55,n=23);txt(d,title,360,155,B.fit(d,title,660,47),INK)
 cap=next(z for a,b,z in CAPS if a<=t<b)
 lines={'Marco Polo':['MARCO POLO'],'viajó a China…':['VIAJÓ A CHINA…'],'¡y volvió veinticuatro años después!':['¡Y VOLVIÓ','VEINTICUATRO AÑOS','DESPUÉS!']}[cap]
 for i,line in enumerate(lines):txt(d,line,360,1060+i*59,B.fit(d,line,650,43),GOLD if i==1 else WHITE)
 return im
if __name__=='__main__':
 if not shutil.which('ffmpeg'):raise SystemExit('Falta FFmpeg en PATH. No se descargará automáticamente.')
 for t in [.5,2.2,4.1]:frame(t).save(O/f'fotograma_{t}.jpg')
 out=O/'marco_polo_5s_sin_audio.mp4';p=subprocess.Popen(['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s','720x1280','-r','24','-i','pipe:0','-an','-c:v','libx264','-threads','2','-preset','fast','-crf','20','-pix_fmt','yuv420p','-movflags','+faststart',str(out)],stdin=subprocess.PIPE)
 for i in range(120):p.stdin.write(frame(i/24).tobytes())
 p.stdin.close();assert p.wait()==0
 audio=O/'voz_m1_5s.wav'
 if audio.exists():subprocess.run(['ffmpeg','-y','-v','error','-i',str(out),'-i',str(audio),'-c:v','copy','-c:a','aac','-b:a','160k','-t','5','-movflags','+faststart',str(O/'marco_polo_5s_con_M1.mp4')],check=True)
 (O/'subtitulos.srt').write_text('1\n00:00:00,000 --> 00:00:01,100\nMarco Polo\n\n2\n00:00:01,100 --> 00:00:02,400\nviajó a China…\n\n3\n00:00:02,400 --> 00:00:05,000\n¡y volvió veinticuatro años después!\n',encoding='utf8');print('Prueba5s renderizada',flush=True)
