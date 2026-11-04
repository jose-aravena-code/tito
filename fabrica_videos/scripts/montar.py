"""Cinco escenas animadas y audio original. No descarga recursos."""
import argparse
import json
import math
import os
from pathlib import Path
import random
import shutil
import subprocess
import wave

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
CFG = json.loads((ROOT / 'configuracion/wow.json').read_text(encoding='utf-8'))
W, H = 720, 1280
CYAN = (112, 228, 243)
GOLD = (255, 209, 110)
WHITE = (239, 244, 250)


def tool(name):
    return os.environ.get(name.upper()) or shutil.which(name) or name


def font(size, mono=False):
    supplied = os.environ.get('WOW_FONT_MONO' if mono else 'WOW_FONT')
    candidates = [supplied] if supplied else []
    candidates += ([r'C:\Windows\Fonts\consola.ttf', '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf']
                   if mono else [r'C:\Windows\Fonts\arial.ttf', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'])
    for path in candidates:
        if path and Path(path).is_file():
            return ImageFont.truetype(path, size)
    raise RuntimeError('Falta una fuente: configura WOW_FONT y WOW_FONT_MONO')


FONTS = {s: font(s) for s in [22, 25, 30, 36, 40, 46, 64, 84]}
MONO = font(60, True)
rng = random.Random(1977)
STARS = [(rng.random()*360, rng.random()*640, rng.uniform(.15, 1), rng.random()*6.28) for _ in range(310)]
PARTICLES = [(rng.uniform(-1, 1), rng.uniform(-1, 1), rng.uniform(0, 6.28)) for _ in range(300)]


def background():
    yy, xx = np.mgrid[:640, :360]
    glow = np.exp(-(((xx-240)/210)**2 + ((yy-230)/210)**2))
    cloud = np.sin(xx/65 + yy/130)*np.sin(yy/83)*.5+.5
    a = np.zeros((640, 360, 3), dtype=np.uint8)
    for c, base, scale in [(0, 3, 10), (1, 6, 20), (2, 15, 40)]:
        a[:, :, c] = np.clip(base + scale*glow*(.5+.5*cloud), 0, 255)
    return Image.fromarray(a)


BG = background()


def wrap(text, draw, f, width):
    lines, current = [], ''
    for word in text.split():
        candidate = (current+' '+word).strip()
        if current and draw.textlength(candidate, font=f) > width:
            lines.append(current)
            current = word
        else:
            current = candidate
    if current:
        lines.append(current)
    return lines


def centered(draw, text, y, f, fill=WHITE):
    draw.text(((W-draw.textlength(text, font=f))/2, y), text, font=f, fill=fill)


def telescope(d, p, t):
    # Esquema: reflector plano alto, reflector curvo fijo y plano de tierra.
    d.polygon([(0, 370), (360, 330), (360, 640), (0, 640)], fill=(5, 13, 20))
    d.polygon([(25, 390), (239, 361), (341, 420), (101, 471)], fill=(42, 55, 65), outline=(80, 103, 111))
    flat = [(27, 239), (133, 219), (137, 338), (31, 358)]
    d.polygon(flat, fill=(36, 49, 59), outline=(145, 171, 180), width=2)
    for n in range(1, 9):
        u=n/9
        d.line([(27+106*u, 239-20*u), (31+106*u, 358-20*u)], fill=(80, 104, 116))
    for n in range(1, 7):
        u=n/7
        d.line([(27+4*u, 239+119*u), (133+4*u, 219+119*u)], fill=(80, 104, 116))
    for x, y in [(31, 358), (137, 338)]:
        d.line([(x,y), (x-10,y+51)], fill=(94, 114, 125), width=3)
    # Un reflector rectangular curvado, no un plato parabólico de seguimiento.
    curve = [(222+i*12, 287+int((i-4)**2*1.2)) for i in range(9)]
    d.polygon(curve+[(318, 393), (222, 414)], fill=(54, 70, 80), outline=(144, 172, 182))
    for i in range(9):
        x,y=curve[i]
        d.line([(x,y), (x,414-(x-222)*.22)], fill=(120, 145, 155))
    for n in range(6):
        yy=330+n*12
        d.line([(222,yy+10), (318,yy-10)], fill=(87, 113, 125))
    for n in range(4):
        r=25+((t*24+n*34)%140)
        d.arc((171-r, 155-r*.6,171+r,155+r*.6), 20, 160,
              fill=(45, int(100+100*(1-r/170)), 190), width=2)
    d.line([(166, 370), (180, 357), (188, 374)], fill=CYAN, width=2)


def scene_image(i, t, p):
    im=BG.copy()
    d=ImageDraw.Draw(im)
    for x,y,z,phase in STARS:
        expansion=p*(.30 if i==0 else .16)
        xx=(x+(x-180)*expansion+t*z*2.8)%360
        yy=(y+(y-260)*expansion+t*z*.9)%640
        b=int(100+130*z*(.65+.35*math.sin(t*.7+phase)))
        if i==0 and p<.16:
            # Breve acercamiento inicial; después el movimiento se suaviza.
            trail=(1-p/.16)*.07*z
            d.line((xx-(xx-180)*trail,yy-(yy-280)*trail,xx,yy),
                   fill=(b//2,b//2,min(255,b//2+45)),width=1)
        d.ellipse((xx,yy,xx+(.5+z),yy+(.5+z)), fill=(b,b,min(255,b+20)))
    if i in (0, 3):
        signal = max(0,1-p*1.4) if i==3 else 1
        points=[]
        for x in range(10,351):
            amp=math.exp(-((x-180)/48)**2)*signal
            y=283+math.sin(x*.4-t*9)*amp*55
            points.append((x,y))
        halo=Image.new('RGB',im.size)
        ImageDraw.Draw(halo).line(points,fill=(15,int(70*signal),int(95*signal)),width=8)
        halo=halo.filter(ImageFilter.GaussianBlur(5))
        im=Image.fromarray(np.minimum(255,np.array(im,dtype=np.uint16)+np.array(halo,dtype=np.uint16)).astype('uint8'))
        d=ImageDraw.Draw(im)
        d.line(points, fill=(45,int(90+130*signal),int(130+100*signal)), width=2)
        glow=Image.new('RGB', im.size)
        gd=ImageDraw.Draw(glow)
        for n in range(3):
            r=12+((t*22+n*47)%160)
            a=max(0,1-r/180)*signal
            gd.ellipse((180-r,280-r,180+r,280+r),outline=(int(20*a),int(70*a),int(95*a)),width=2)
        im=Image.fromarray(np.clip(np.array(im,dtype=np.uint16)+np.array(glow,dtype=np.uint16),0,255).astype('uint8'))
    elif i==1:
        telescope(d,p,t)
        # Barrido de recepción sobre el esquema, no una medida histórica.
        sweep=Image.new('RGBA',im.size)
        sd=ImageDraw.Draw(sweep)
        sy=230+int(p*190)
        sd.polygon([(10,sy),(340,sy-55),(340,sy-45),(10,sy+10)],fill=(75,210,230,38))
        im=Image.alpha_composite(im.convert('RGBA'),sweep).convert('RGB')
    elif i==2:
        # El documento se compone después a resolución de salida.
        pass
    else:
        # Galaxia espiral estilizada: partículas en brazos que se desplazan.
        for n in range(700):
            r=5+(n/700)**.7*155
            a=n*2.39996+t*.07
            arm=2.8*math.log(r/8)+((n%3)*2*math.pi/3)
            a=arm+math.sin(n*7)*.18+t*.07
            x=180+math.cos(a)*r
            y=267+math.sin(a)*r*.55
            v=int(60+130*(1-r/180))
            d.ellipse((x,y,x+1.1,y+1.1), fill=(v,min(255,v+30),min(255,v+55)))
        haze=Image.new('RGB',im.size)
        hd=ImageDraw.Draw(haze)
        hd.ellipse((160,253,200,281),fill=(130,103,87))
        haze=haze.filter(ImageFilter.GaussianBlur(14))
        im=Image.fromarray(np.minimum(255,np.array(im,dtype=np.uint16)+np.array(haze,dtype=np.uint16)).astype('uint8'))
    # Acercamiento de cámara continuo, conservando textos y subtítulos estables.
    zoom=1.025+.055*p
    cw,ch=round(360/zoom),round(640/zoom)
    cx=180+3*math.sin(t*.7)
    cy=300+3*math.cos(t*.6)
    left=max(0,min(360-cw,round(cx-cw/2)))
    top=max(0,min(640-ch,round(cy-ch/2)))
    return im.crop((left,top,left+cw,top+ch)).resize((W,H),Image.Resampling.LANCZOS)


def frame(t, timeline, total):
    i=next((j for j,s in enumerate(timeline) if t<s['end']),4)
    seg=timeline[i]
    local=t-seg['start'];p=local/(seg['end']-seg['start'])
    im=scene_image(i,t,p).convert('RGBA')
    overlay=Image.new('RGBA',(W,H))
    d=ImageDraw.Draw(overlay)
    d.rounded_rectangle((46,70,674,122), radius=15, fill=(3,10,20,190), outline=(76,134,150,150))
    centered(d,'ARCHIVO CÓSMICO  /  LA SEÑAL WOW!',82,FONTS[22],CYAN)
    titles=['15 AGOSTO · 1977','BIG EAR · OHIO','6EQUJ5','LA SEÑAL DESAPARECE','¿ESTAMOS SOLOS?']
    centered(d,titles[i],164,FONTS[36],GOLD if i==2 else WHITE)
    if i==0:
        centered(d,'72 SEGUNDOS DE MISTERIO',228,FONTS[22],CYAN)
    if i==1:
        centered(d,'72 SEGUNDOS',755,FONTS[46],GOLD)
        centered(d,'Esquema animado del instrumento',827,FONTS[22],WHITE)
    if i==2:
        # Se reproduce la columna famosa, no se inventan otras lecturas.
        shift=int(18*math.sin(p*1.6))
        y0=282+shift
        d.rounded_rectangle((160,y0,560,y0+500),radius=7,fill=(223,216,194,255))
        for y in range(y0+20,y0+480,12):
            d.line((178,y,540,y), fill=(167,164,149,45))
        for k,ch in enumerate('6EQUJ5'):
            centered(d,ch,y0+22+k*62,MONO,(38,42,37))
        # Destaca cada lectura sucesivamente sin alterar el orden del registro.
        selected=min(5,int(p*6))
        yy=y0+22+selected*62
        d.rounded_rectangle((330,yy,394,yy+62),radius=5,outline=(174,35,38,190),width=2)
        # Anotación roja: recreación, sin atribuir nueva evidencia al papel.
        angle=min(360,max(0,(p-.1)*650))
        d.arc((292,y0+18,431,y0+399),start=-85,end=-85+angle,fill=(174,35,38),width=5)
        if p>.35:
            d.text((433,y0+185),'Wow!',font=FONTS[40],fill=(174,35,38),stroke_width=1)
        centered(d,'Jerry Ehman · anotación «Wow!»',813,FONTS[25],GOLD)
    if i==3:
        centered(d,'SIN REPETICIÓN CONCLUYENTE',760,FONTS[25],CYAN)
    if i==4:
        centered(d,'ORIGEN DESCONOCIDO',740,FONTS[30],GOLD)
        centered(d,'No demuestra contacto extraterrestre',792,FONTS[22],WHITE)
    # Subtítulos por escena: el intervalo se deriva del audio de esa escena.
    if t < seg.get('speech_end',seg['end']):
        lines=wrap(seg['display'],d,FONTS[40],590)
        box_h=len(lines)*53+42
        top=1150-box_h
        d.rounded_rectangle((44,top,676,1150),radius=18,fill=(0,4,12,225))
        for j,line in enumerate(lines):
            # Resaltado de las líneas con las palabras clave solicitadas.
            color=GOLD if any(word in line for word in ['1977','72','WOW']) else WHITE
            centered(d,line,top+17+j*53,FONTS[40],color)
    centered(d,'RECREACIÓN VISUAL · SONIDO DE AMBIENTACIÓN',1190,FONTS[22],(153,172,187))
    # Transiciones muy breves con brillo azul; la única oscuridad total es final.
    if i>0 and local<.14:
        d.rectangle((0,0,W,H), fill=(70,145,170,int(65*(1-local/.14))))
        # Estela horizontal muy breve para marcar el cambio de escena.
        sy=int(local/.14*H)
        d.rectangle((0,sy,W,min(H,sy+7)),fill=(100,220,240,100))
    im=Image.alpha_composite(im,overlay).convert('RGB')
    if t>total-.18:
        im=Image.blend(im,Image.new('RGB',(W,H)),min(1,(t-(total-.18))/.13))
    return im


def score(total,timeline):
    sr=48000
    x=np.arange(round(total*sr))/sr
    rng=np.random.default_rng(1977)
    # Dron y pulsos originales; no se usa ninguna canción o grabación externa.
    a=(.018*np.sin(2*np.pi*55*x)+.012*np.sin(2*np.pi*82.41*x)+
       .007*np.sin(2*np.pi*110.4*x))
    a*=.65+.35*np.sin(2*np.pi*.16*x)**2
    for k,s in enumerate(timeline):
        center=s['start']+.12
        env=np.exp(-np.maximum(0,x-center)*9)*(x>=center)*(x<center+.7)
        a+=env*(.025*rng.normal(0,1,len(x))+.018*np.sin(2*np.pi*(620*x+50*x*x)))
    # Descenso de tensión antes de la pregunta, sin silencio accidental.
    q=timeline[4]['start']
    a*=np.where((x>q-.24)&(x<q+.05),.2,1)
    a*=np.minimum(1,x/.3)*np.clip((total-x)/.22,0,1)
    stereo=np.stack([a,a*.96+.003*np.sin(2*np.pi*55.2*x)],axis=1)
    path=ROOT/'recursos/musica/ambiente_original.wav'
    with wave.open(str(path),'wb') as w:
        w.setnchannels(2);w.setsampwidth(2);w.setframerate(sr)
        w.writeframes((np.clip(stereo,-1,1)*32767).astype('<i2').tobytes())
    return path


def srt_time(t):
    ms=round(t*1000)
    return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}'


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--preview',action='store_true',help='Previsualización SIN voz, no resultado final')
    args=parser.parse_args()
    if args.preview:
        timeline=[];start=0
        for s in CFG['segments']:
            end=start+s['preview_duration']
            timeline.append(dict(s,start=start,end=end,speech_end=end-.1));start=end
    else:
        path=ROOT/'recursos/audios/timeline.json'
        if not path.exists():
            raise RuntimeError('Falta narración real. Ejecuta voz.py o usa --preview explícitamente.')
        timeline=json.loads(path.read_text(encoding='utf-8'))
    total=timeline[-1]['end']
    if not 15 <= total <= 20:
        raise RuntimeError(f'Duración fuera de objetivo: {total}')
    out=ROOT/'exportaciones';out.mkdir(exist_ok=True)
    log=ROOT/'registros';log.mkdir(exist_ok=True)
    silent=out/'animacion_sin_audio.mp4'
    for i,s in enumerate(timeline):
        frame((s['start']+s['end'])/2,timeline,total).save(out/f'escena_{i+1}.jpg')
    with (log/'render.log').open('w') as lf:
        cmd=[tool('ffmpeg'),'-y','-v','warning','-f','rawvideo','-pix_fmt','rgb24',
             '-s',f'{W}x{H}','-r',str(CFG['fps']),'-i','pipe:0','-an',
             '-c:v','libx264','-preset','veryfast','-crf','20','-threads','2',
             '-pix_fmt','yuv420p','-movflags','+faststart',str(silent)]
        with subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=lf) as process:
            for n in range(math.ceil(total*CFG['fps'])):
                process.stdin.write(frame(n/CFG['fps'],timeline,total).tobytes())
                if n%90==0:print(f'Fotograma {n}/{math.ceil(total*CFG["fps"])}',flush=True)
            process.stdin.close()
            if process.wait()!=0:raise RuntimeError('Falló FFmpeg; consultar render.log')
    music=score(total,timeline)
    output=out/('wow_PREVIA_SIN_VOZ.mp4' if args.preview else 'wow_final.mp4')
    cmd=[tool('ffmpeg'),'-y','-v','warning','-i',str(silent),'-i',str(music)]
    if args.preview:
        cmd+=['-map','0:v:0','-map','1:a:0']
    else:
        cmd+=['-i',str(ROOT/'recursos/audios/narracion.wav'),'-filter_complex',
              '[2:a]volume=1.5,asplit=2[voice][key];'
              '[1:a][key]sidechaincompress=threshold=0.02:ratio=6:attack=10:release=180[bed];'
              '[voice][bed]amix=inputs=2:normalize=0,alimiter=limit=0.92:level=false[a]',
              '-map','0:v:0','-map','[a]']
    cmd+=['-c:v','copy','-c:a','aac','-b:a','160k','-ar','48000','-ac','2',
          '-t',f'{total:.6f}','-movflags','+faststart',str(output)]
    subprocess.run(cmd,check=True)
    srt='\n\n'.join(f'{i+1}\n{srt_time(s["start"])} --> {srt_time(s.get("speech_end",s["end"]))}\n{s["display"]}'
                     for i,s in enumerate(timeline))+'\n'
    (ROOT/'subtitulos'/('wow_previa.srt' if args.preview else 'wow.srt')).write_text(srt,encoding='utf-8')
    (log/'timeline_usada.json').write_text(json.dumps(timeline,ensure_ascii=False,indent=2),encoding='utf-8')
    print(output)


if __name__=='__main__':main()
