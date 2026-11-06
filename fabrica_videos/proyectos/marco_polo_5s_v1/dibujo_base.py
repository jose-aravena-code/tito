"""Dos cortos originales 2D sin audio, con tiempo editorial provisional.
Uso: python animar_dos_historias_v1.py san_marino|jack [--stills]
"""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import numpy as np, math,json,re,subprocess,sys,hashlib
R=Path(__file__).resolve().parents[1];W,H,FPS=720,1280,24
INK='#17273e';WHITE='#fff7df';GOLD='#ffd26a';TEAL='#68dfca';CORAL='#ff966b'
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf';REG='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf';FC={}
def f(n,b=True):
 k=(int(n),b)
 if k not in FC:FC[k]=ImageFont.truetype(FONT if b else REG,int(n))
 return FC[k]
def clamp(x):return max(0.,min(1.,float(x)))
def ease(x):x=clamp(x);return x*x*(3-2*x)
def mix(a,b,u):return a+(b-a)*u
def txt(d,s,x,y,n=32,c=WHITE,center=False,stroke=0):
 ff=f(n);bb=d.textbbox((0,0),s,font=ff)
 if center:x-=bb[2]/2
 d.text((x,y),s,font=ff,fill=c,stroke_width=stroke,stroke_fill=INK)
def fit(d,s,maxwidth,n=45):
 while d.textbbox((0,0),s,font=f(n))[2]>maxwidth:n-=1
 return n
def tag(d,s,x,y,col=INK,fg=WHITE,n=20):
 ww=d.textbbox((0,0),s,font=f(n))[2]+32;d.rounded_rectangle((x,y,x+ww,y+n+25),radius=16,fill=col);txt(d,s,x+16,y+7,n,fg)
def grad(a,b):
 a=np.array([int(a[i:i+2],16) for i in (1,3,5)]);b=np.array([int(b[i:i+2],16) for i in (1,3,5)]);u=np.linspace(0,1,H)[:,None,None]
 return Image.fromarray(np.broadcast_to(a*(1-u)+b*u,(H,W,3)).astype('uint8').copy())
BGS={'warm':grad('#88c7d3','#f4d4a2'),'sun':grad('#d89c76','#ffe8ad'),'paper':grad('#bc8b60','#f6dca8'),'night':grad('#111630','#3b3457'),'desk':grad('#182743','#41566a'),'modern':grad('#142343','#205a69')}
def paste(im,layer,x,y,w=None,angle=0):
 if w is not None:layer=layer.resize((max(1,int(w)),max(1,int(layer.height*w/layer.width))),Image.Resampling.BICUBIC)
 if angle:layer=layer.rotate(angle,resample=Image.Resampling.BICUBIC,expand=True)
 im.paste(layer,(int(x),int(y)),layer)
def star(d,x,y,r,c=GOLD):
 p=[(x+math.sin(i*math.pi/5)*(r if i%2==0 else r*.44),y-math.cos(i*math.pi/5)*(r if i%2==0 else r*.44)) for i in range(10)];d.polygon(p,fill=c)
def character(t,kind='marino',pose='stand',mood='smile',variant=0):
 im=Image.new('RGBA',(400,650));d=ImageDraw.Draw(im);skin=['#f7c8a4','#d79f7e','#bc815f','#f2c3a2','#d59c79'][variant%5];hair=['#543c36','#352d37','#815c47','#b77742','#4d3b33'][variant%5]
 coat='#e9c899' if kind=='marino' else ('#293b62' if kind=='detective' else ['#9d6b91','#55998d','#bd8d55','#6c83a5','#986c65'][variant%5]);dark='#6b5345' if kind=='marino' else '#202e48'
 k=math.sin(t*9.5+variant);walk=pose=='walk';bob=(abs(math.sin(t*9.5))*6 if walk else math.sin(t*2.1)*2)
 # Legs with independent heel lift.
 for side in [-1,1]:
  ph=math.sin(t*9.5+(0 if side==1 else math.pi)+variant);a=26 if walk else 2
  hip=(200+side*31,464+bob);knee=(200+side*35+ph*a*.35,525+bob);foot=(200+side*41-ph*a,602-max(0,ph)*22 if walk else 604)
  d.line([hip,knee,foot],fill=INK,width=34,joint='curve');d.line([hip,knee,foot],fill=dark,width=24,joint='curve');d.ellipse((foot[0]-24,foot[1]-12,foot[0]+32,foot[1]+11),fill='#59433b' if kind=='marino' else INK,outline=INK,width=4)
 # Clothing differentiates the historical person and Victorian constable.
 if kind=='marino':
  d.polygon([(142,315+bob),(259,315+bob),(285,490+bob),(120,490+bob)],fill=coat,outline=INK,width=6);d.polygon([(135,338+bob),(164,323+bob),(255,478+bob),(224,489+bob)],fill='#9d7054');d.line((126,428+bob,275,428+bob),fill='#6b5345',width=12)
 elif kind=='detective':
  d.rounded_rectangle((135,314+bob,264,492+bob),radius=25,fill=coat,outline=INK,width=6);d.polygon([(137,365+bob),(121,520+bob),(279,520+bob),(264,365+bob)],fill=coat,outline=INK,width=6);d.line((201,340+bob,201,513+bob),fill='#65708e',width=3)
  for yy in [365,405,447]:d.ellipse((192,yy+bob,199,yy+7+bob),fill=GOLD)
 else:d.polygon([(143,316+bob),(258,316+bob),(286,511+bob),(115,511+bob)],fill=coat,outline=INK,width=6)
 # Arms and expressive gestures.
 for side in [-1,1]:
  shoulder=(200+side*58,342+bob)
  if pose=='pray':elbow=(200+side*64,395+bob);hand=(200+side*6,370+bob)
  elif pose=='point' and side==1:elbow=(295,326+bob);hand=(339,272+math.sin(t*3)*5)
  elif pose=='hammer' and side==1:
   swing=max(0,math.sin(t*7));elbow=(284,332-swing*53);hand=(299,292-swing*105)
  elif pose=='think' and side==1:elbow=(286,379);hand=(235,278)
  elif pose=='read':elbow=(200+side*85,388);hand=(200+side*75,420)
  else:
   sw=k*19*side if walk else k*3;elbow=(200+side*80+sw,402+bob);hand=(200+side*70+sw*1.5,452+bob)
  d.line([shoulder,elbow,hand],fill=INK,width=27,joint='curve');d.line([shoulder,elbow,hand],fill=coat,width=17,joint='curve');d.ellipse((hand[0]-13,hand[1]-13,hand[0]+13,hand[1]+13),fill=skin,outline=INK,width=4)
  if pose=='hammer' and side==1:
   d.line((hand[0],hand[1],hand[0]+24,hand[1]-52),fill='#75533d',width=11);d.rounded_rectangle((hand[0]-2,hand[1]-73,hand[0]+54,hand[1]-43),radius=5,fill='#7796a3',outline=INK,width=4)
 d.rounded_rectangle((180,278+bob,221,330+bob),radius=12,fill=skin,outline=INK,width=4)
 d.ellipse((105,127+bob,294,314+bob),fill=skin,outline=INK,width=6)
 for xx in [108,291]:d.ellipse((xx-12,214+bob,xx+12,243+bob),fill=skin,outline=INK,width=4)
 if kind=='detective':
  d.pieslice((105,77+bob,294,246+bob),180,360,fill='#263550',outline=INK,width=6);d.rounded_rectangle((93,159+bob,307,190+bob),radius=12,fill='#344866',outline=INK,width=5);star(d,200,136+bob,18,GOLD)
 elif kind=='marino':
  d.polygon([(109,203+bob),(104,161+bob),(128,119+bob),(157,132+bob),(185,107+bob),(224,122+bob),(262,116+bob),(294,157+bob),(290,202+bob),(268,172+bob),(235,161+bob),(195,165+bob),(156,151+bob),(130,200+bob)],fill=hair,outline=INK,width=5)
  d.arc((131,208+bob,272,312+bob),0,180,fill=hair,width=18)
 else:
  d.pieslice((104,112+bob,296,276+bob),180,360,fill=hair,outline=INK,width=5);d.ellipse((260,151+bob,317,211+bob),fill=hair,outline=INK,width=4)
 blink=(int(t*24+variant*21)%101)<3
 for side in [-1,1]:
  x=200+side*43;y=220+bob
  if blink:d.line((x-15,y,x+15,y),fill=INK,width=5)
  else:
   d.ellipse((x-22,y-23,x+22,y+23),fill='#fffbed',outline=INK,width=4);look=side*2+math.sin(t*.8)*3;d.ellipse((x-7+look,y-12,x+8+look,y+16),fill=INK);d.ellipse((x-3+look,y-11,x+1+look,y-5),fill='white')
  off=-12 if mood=='surprise' else (4 if mood=='concern' else 0);d.line((x-19,y-35+off-side*3,x+17,y-35+off+side*3),fill=INK,width=5)
 d.arc((193,230+bob,216,254+bob),0,150,fill='#b47b60',width=3)
 if mood=='surprise':d.ellipse((184,262+bob,219,291+bob),fill=INK)
 elif mood=='concern':d.arc((181,277+bob,225,297+bob),190,345,fill=INK,width=4)
 else:d.arc((176,253+bob,227,291+bob),0,180,fill=INK,width=4)
 if pose=='read':d.polygon([(125,405),(200,422),(276,405),(278,465),(200,485),(123,465)],fill='#f5dfb7',outline=INK,width=5);d.line((200,423,200,483),fill='#ad8a67',width=3)
 return im

def actor(im,x,feet,t,kind='marino',scale=1,pose='stand',mood='smile',variant=0,angle=0):
 sp=character(t,kind,pose,mood,variant);ww=int(400*scale);hh=int(650*scale);paste(im,sp,x-ww/2,feet-hh,ww,angle)

def mountains(im,t,warm=True):
 d=ImageDraw.Draw(im);d.ellipse((490,150,685,345),fill='#fff0b8' if warm else '#cfd1df')
 for j,(col,yy) in enumerate([('#8fa68a',510),('#64897c',620),('#416c65',775)]):
  pts=[(-60,H),(W+60,H),(W+60,yy+160)]
  for x in range(W+60,-100,-70):pts.append((x,yy-120*math.sin(x*.006+j*.9)+40*math.sin(x*.013+j)))
  d.polygon(pts,fill=col)
 d.polygon([(-80,1070),(70,875),(230,835),(320,696),(430,664),(580,475),(760,459),(760,H),(-80,H)],fill='#9c9c75')
 d.line([(-30,1080),(160,944),(233,849),(355,799),(409,697),(540,662),(660,573)],fill='#e7cda0',width=42,joint='curve')
 # Golden diagonal rays are background sunlight, no sweeping transition.
 over=Image.new('RGBA',(W,H));od=ImageDraw.Draw(over)
 for q in range(3):od.polygon([(570+q*15,165),(110+q*150,1010),(260+q*140,1010),(630+q*20,205)],fill=(255,231,169,13))
 im.paste(over,(0,0),over)

def chapel(d,x,y,s=1):
 def p(a,b):return(x+a*s,y+b*s)
 d.polygon([p(0,80),p(85,5),p(170,80)],fill='#b86e50',outline=INK,width=max(2,int(5*s)));d.rectangle([p(12,78),p(158,210)],fill='#e2c49c',outline=INK,width=max(2,int(5*s)));d.rounded_rectangle([p(58,125),p(112,210)],radius=int(24*s),fill='#655344',outline=INK,width=max(1,int(3*s)))
 d.line([p(84,-25),p(84,20)],fill='#735340',width=max(2,int(9*s)));d.line([p(64,-10),p(104,-10)],fill='#735340',width=max(2,int(9*s)))
def towers(im,t,stage=1):
 d=ImageDraw.Draw(im)
 d.polygon([(-30,980),(120,700),(280,710),(420,530),(590,560),(760,410),(760,H),(-30,H)],fill='#567b73',outline=INK)
 for i,(xx,yy,ss) in enumerate([(132,720,.9),(375,610,1.1),(590,570,.8)]):
  y=yy+18*(1-ease((stage-i*.12)*1.8));ww=82*ss;hh=170*ss
  d.rectangle((xx,y-hh,xx+ww,y),fill='#e3d1ac',outline=INK,width=4)
  for k in range(4):d.rectangle((xx+k*ww/4,y-hh-24*ss,xx+k*ww/4+12*ss,y-hh+7),fill='#e3d1ac',outline=INK,width=3)
  d.rounded_rectangle((xx+ww*.35,y-73*ss,xx+ww*.65,y-19*ss),radius=12,fill='#50606a')
  for ly in range(3):d.line((xx+6,y-hh+40*ss+ly*34*ss,xx+ww-6,y-hh+40*ss+ly*34*ss),fill='#bea980',width=2)
 d.line((80,820,240,700,450,700,660,580),fill='#dfcdad',width=34,joint='curve')

def document(d,x,y,ww,hh,title='',subtitle='',angle=0):
 d.rounded_rectangle((x+10,y+12,x+ww+10,y+hh+12),radius=18,fill='#1b2435');d.rounded_rectangle((x,y,x+ww,y+hh),radius=15,fill='#f0dfb9',outline='#a87d59',width=4)
 if title:txt(d,title,x+ww/2,y+34,fit(d,title,ww-45,44),INK,True)
 if subtitle:txt(d,subtitle,x+ww/2,y+102,fit(d,subtitle,ww-30,24),'#765c52',True)
def letter(im,x,y,ww,t,mode='letter'):
 sp=Image.new('RGBA',(400,350));d=ImageDraw.Draw(sp);d.rounded_rectangle((7,8,390,335),radius=10,fill='#eedfbb',outline='#976e58',width=5)
 for j in range(5):d.line((35,55+j*36,337-(j%2)*45,55+j*36),fill='#8d786c',width=3)
 txt(d,'Jack the Ripper',200,246,29,'#745c54',True)
 if mode=='doubt':d.ellipse((270,213,362,305),fill='#633b6a',outline=GOLD,width=3);txt(d,'?',317,215,64,GOLD,True)
 paste(im,sp,x,y,ww,math.sin(t*1.4+x)*3)

def nightstreet(im,t):
 d=ImageDraw.Draw(im)
 d.ellipse((500,135,610,245),fill='#d8d4c0')
 for side in [-1,1]:
  for j in range(4):
   x=(-90+j*87) if side<0 else (430+j*87);y=310+(3-j)*35
   d.polygon([(x,y),(x+106,y-25),(x+106,900),(x,900)],fill=['#222b4c','#303453','#3e3d60'][j%3],outline='#101a32',width=4)
   for floor in range(4):
    for q in range(2):
     xx=x+15+q*44;yy=y+40+floor*106;d.rectangle((xx,yy,xx+23,yy+39),fill='#b59562' if (j+floor+q)%4==0 else '#48506b',outline='#142139',width=3)
 d.polygon([(310,600),(410,600),(720,H),(0,H)],fill='#465062')
 for j in range(9):
  yy=655+j*j*6;d.line((200-j*15,yy,520+j*20,yy),fill='#697079',width=2)
 for xx,yy,ss in [(145,660,1),(550,603,.7)]:
  d.line((xx,yy-270*ss,xx,yy+165*ss),fill=INK,width=int(12*ss));d.polygon([(xx-33*ss,yy-270*ss),(xx+33*ss,yy-270*ss),(xx+23*ss,yy-202*ss),(xx-23*ss,yy-202*ss)],fill='#ffda87',outline=INK,width=4)
  glow=Image.new('RGBA',(W,H));gd=ImageDraw.Draw(glow)
  for r,a in [(92,7),(63,11),(43,17)]:gd.ellipse((xx-r*ss,yy-235*ss-r*ss,xx+r*ss,yy-235*ss+r*ss),fill=(255,212,129,a))
  im.paste(glow,(0,0),glow)
 # Slow mist layers, not flashes.
 fog=Image.new('RGBA',(W,H));fd=ImageDraw.Draw(fog)
 for j in range(4):
  xx=((t*(12+j*5)+j*230)%1100)-380;yy=720+j*56
  fd.ellipse((xx,yy,xx+740,yy+130),fill=(146,167,192,13))
 im.paste(fog,(0,0),fog)

def villain(t):
 sp=Image.new('RGBA',(500,620));d=ImageDraw.Draw(sp)
 d.polygon([(250,195),(58,585),(445,585)],fill='#2a2145',outline=INK,width=7)
 d.ellipse((155,112,345,327),fill='#bb997f',outline=INK,width=7)
 d.polygon([(155,175),(170,117),(215,91),(280,98),(330,132),(344,179)],fill='#241e37')
 for xx in [204,287]:d.ellipse((xx-16,194,xx+16,216),fill=INK)
 d.arc((216,231,279,276),0,180,fill=INK,width=5)
 d.rectangle((143,18,352,136),fill='#22213a',outline=INK,width=7);d.rounded_rectangle((99,112,397,164),radius=20,fill='#36304b',outline=INK,width=6);d.rectangle((148,91,347,116),fill='#77576a')
 return sp

# Static original geography from Natural Earth, domain public.
