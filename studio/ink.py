"""Portrait drawing helpers. Stage coordinates are 360 by 640 at every resolution."""
from functools import lru_cache
from pathlib import Path
import math
import sys
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'vendor/kaomei'))
from b6_space import smooth
INK='#231b2c'
PAPER='#fff3d5'

@lru_cache(maxsize=160)
def font(size):
    return ImageFont.truetype(str(ROOT/'fonts/ArchivoBlack-Regular.ttf'),max(1,size))

class Canvas:
    def __init__(self,width,bg=INK):
        self.width=width
        self.k=width/360
        self.image=Image.new('RGB',(width,width*16//9),bg)
        self.draw=ImageDraw.Draw(self.image)
        self.zoom=1.; self.x=0.; self.y=0.
    def camera(self,zoom=1.,focus=(180,300),shake=(0,0)):
        self.zoom=zoom
        self.x=focus[0]*(1-zoom)+shake[0];self.y=focus[1]*(1-zoom)+shake[1]
    def pt(self,p):
        return (round(self.k*(self.x+self.zoom*p[0])),round(self.k*(self.y+self.zoom*p[1])))
    def stroke(self,w):
        return max(1,round(w*self.k*self.zoom))
    def poly(self,points,fill,edge=INK,w=3):
        points=list(points);p=[self.pt(v) for v in points]
        self.draw.polygon(p,fill)
        if edge:self.draw.line(p+[p[0]],edge,width=self.stroke(w),joint='curve')
    def line(self,points,color=INK,w=3):
        self.draw.line([self.pt(v) for v in points],color,width=self.stroke(w),joint='curve')
    def box(self,xy,fill,edge=INK,w=3,r=0):
        x,y,X,Y=xy
        self.draw.rounded_rectangle([self.pt((x,y)),self.pt((X,Y))],radius=max(0,round(r*self.k*self.zoom)),fill=fill,outline=edge,width=self.stroke(w))
    def oval(self,xy,fill,edge=INK,w=3):
        x,y,X,Y=xy
        self.draw.ellipse([self.pt((x,y)),self.pt((X,Y))],fill,outline=edge,width=self.stroke(w))
    def text(self,xy,text,size,color=PAPER,edge=None,stroke=1,anchor='mm'):
        self.draw.text(self.pt(xy),text,font=font(self.stroke(size)),fill=color,anchor=anchor,
                       stroke_width=self.stroke(stroke) if edge else 0,stroke_fill=edge)
    def caption(self,text):
        self.camera()
        words=text.split();size=21
        while size>=13:
            f=font(self.stroke(size)); lines=['']
            for word in words:
                candidate=(lines[-1]+' '+word).strip()
                if lines[-1] and f.getlength(candidate)>self.k*295:lines.append(word)
                else:lines[-1]=candidate
            if len(lines)<=2 and all(f.getlength(x)<=self.k*295 for x in lines):break
            size-=1
        else:raise ValueError('Caption too long; split the spoken cue: '+text)
        for i,line in enumerate(lines):
            y=493+(i-(len(lines)-1)/2)*(size+7)
            w=f.getlength(line)/self.k
            self.box((180-w/2-8,y-size*.68-1,180+w/2+8,y+size*.76+1),INK,None,r=6)
            self.text((180,y),line,size,'#ffeb9c')
