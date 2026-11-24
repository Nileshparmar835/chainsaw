"""Original portrait set, cast and acting for The People v. One Hungry Guy."""
from math import sin, cos, pi
from ink import INK, PAPER, smooth

RED='#ec5142'; GOLD='#f9bf4c'; TEAL='#51c9bf'; WOOD='#aa684e'
def backdrop(c,top,bottom):
    c.box((-100,-90,460,740),top,None)
    c.poly([(-50,365),(420,280),(430,750),(-80,750)],bottom,None)
    for n in range(14):
        x=n*36-60
        c.line([(x,360),(x-95,690)],'#5c3939',1)
    for y in (400,460,550,663):
        c.line([(-40,y+38),(400,y-24)],'#704444',2)

def sun(c,x,y,r,color):
    for i in range(12):
        a=i*pi/6
        c.line([(x+cos(a)*r,y+sin(a)*r),(x+cos(a)*(r+10),y+sin(a)*(r+10))],color,3)

def store(c,t):
    backdrop(c,'#30565c','#915443')
    c.box((20,68,340,305),'#182e42',INK,5,12)
    for i in range(14):
        x=26+i*24;h=(i*37)%70
        c.box((x,173-h,x+18,281),'#294458',None)
        c.box((x+4,181-h,x+7,187-h),GOLD,None)
    c.box((32,96,158,142),'#533747','#e9796e',2,8)
    c.text((94,119),'OPEN LATE',15,'#ffa193')
    for x in (49,178,299):c.line([(x,69),(x,303)],INK,4)
    for i in range(11):c.poly([(i*37-12,30),(i*37+29,30),(i*37+23,75),(i*37-22,75)],PAPER if i%2 else RED,INK,2)
    # Neon reflections are attached to the window, behind the actors.
    c.line([(188,158),(225,105)],'#4d7380',2)
    c.line([(198,157),(220,125)],'#4d7380',1)
    c.box((-25,383,385,405),'#efbf83',INK,4)
    c.box((-20,405,380,460),'#b66849',INK,4)

def dex(c,x,y,t,startled=False):
    lift=5*sin(t*2.5)
    c.line([(x-9,y+39),(x-18,y+70),(x-30,y+81)],INK,8)
    c.line([(x+4,y+38),(x+16,y+67),(x+12,y+84)],INK,8)
    c.poly([(x-23,y+6),(x+9,y+3),(x+22,y+50),(x-30,y+50)],'#eb8053',INK,4)
    c.line([(x+9,y+15),(x+31,y+24-lift),(x+49,y+7-lift)],INK,6)
    c.oval((x+44,y+1-lift,x+56,y+13-lift),PAPER,INK,2)
    c.oval((x-25,y-39,x+26,y+10),PAPER,INK,4)
    c.oval((x-29,y-48,x+19,y-24),TEAL,INK,4)
    c.box((x-30,y-31,x+32,y-24),TEAL,INK,2,3)
    for dx in (1,14):c.oval((x+dx,y-17,x+dx+4,y-10),INK,None)
    c.line([(x+6,y-2),(x+13,y-4 if startled else y-1),(x+19,y-2)],INK,2)

def pizza(c,x,y,t,anger=True):
    wiggle=3*sin(t*5)
    c.line([(x-13,y+34),(x-22,y+50),(x-34,y+51)],INK,6)
    c.line([(x+8,y+34),(x+24,y+47),(x+34,y+45)],INK,6)
    c.line([(x-23,y-5),(x-43,y+wiggle),(x-57,y-13+wiggle)],INK,5)
    c.line([(x+22,y-5),(x+44,y-17-wiggle),(x+53,y-28-wiggle)],INK,5)
    c.poly([(x-47,y-49),(x+48,y-47),(x+8,y+46),(x-2,y+53)],GOLD,INK,4)
    c.box((x-49,y-55,x+49,y-38),'#d58b4b',INK,4,8)
    for dx,dy,r in [(-26,-26,8),(24,-21,8),(-6,24,5),(6,-27,6)]:
        c.oval((x+dx-r,y+dy-r,x+dx+r,y+dy+r),RED,'#873543',2)
    for dx in (-12,10):
        c.oval((x+dx,y-17,x+dx+9,y-3),PAPER,INK,2)
        c.oval((x+dx+1,y-13,x+dx+4,y-6),INK,None)
    c.line([(x-16,y-19),(x-4,y-15)],INK,3)
    c.line([(x+8,y-16),(x+20,y-22)],INK,3)
    c.oval((x-3,y+3,x+10,y+8+abs(5*sin(t*7))),INK,None)
    c.poly([(x+9,y+14),(x+15,y+16),(x+15,y+30),(x+9,y+34),(x+7,y+23)],'#419c74',INK,1)

def summons(c,x,y,word='SUMMONS'):
    c.poly([(x-40,y-21),(x+36,y-25),(x+42,y+20),(x-35,y+24)],PAPER,INK,3)
    c.text((x,y-5),word,9,'#a13e41')
    c.line([(x-24,y+6),(x+18,y+4)],'#86675a',2)

def opening(c,q):
    store(c,q.t);dex(c,79,312,q.t,True)
    c.poly([(103,345),(238,323),(320,362),(176,393)],'#f4c78c')
    c.poly([(103,345),(176,393),(176,403),(103,357)],'#cf8455')
    c.poly([(176,393),(320,362),(320,373),(176,403)],'#df9864')
    v=smooth(0,.38,q.scene_t)
    c.poly([(112,342),(233,324),(228,324-89*v),(109,340-85*v)],'#d0a173')
    pizza(c,221,322-24*v+2*sin(q.t*3),q.t)
    summons(c,219-61*smooth(0,.7,q.scene_t),359)
    c.oval((30,361,57,378),GOLD,INK,2)
    c.box((27,376,61,382),INK,None,r=3)

def evidence(c,q):
    backdrop(c,'#ad6955','#874a40')
    for i in range(12):
        y=85+i*31;c.line([(-30,y+9),(120,y),(252,y+13),(394,y-7)],'#c18768',2)
    c.oval((40,191,325,426),'#56303a',None)
    c.oval((34,181,319,413),'#b5d5c5',INK,5)
    c.oval((56,200,296,394),PAPER,'#779d93',3)
    c.poly([(99,249),(243,220),(196,356)],'#f5d18a','#ddb26f',2)
    for i in range(13):
        x=138+i*7%54;y=254+i*17%52
        c.oval((x,y,x+3,y+2),'#c29769',None)
    summons(c,72-55*(1-smooth(0,.32,q.scene_t)),169,'EXHIBIT A')
    x=99+88*smooth(.15,2.8,q.scene_t);y=292-6*sin(q.scene_t*2)
    c.line([(x+22,y+23),(x+67,y+65)],INK,15)
    c.line([(x+22,y+23),(x+64,y+62)],TEAL,7)
    c.oval((x-33,y-33,x+33,y+33),'#e2dbb3',INK,5)
    if q.id=='plate' or q.u<.6:
        for i in range(4):
            c.line([(x-15+i*3,y+11),(x-19+i*3,y-3),(x-11+i*2,y-13+i*2),(x+4,y-16+i*3),(x+13-i*2,y-6)],'#a77872',2)
    c.line([(x-22,y-7),(x-13,y-20)],'#fff9dd',3)

def jury(c,q):
    backdrop(c,'#406771','#815247')
    c.box((56,90,304,152),INK,GOLD,3,9);c.text((180,121),'THE JURY',29,PAPER)
    for row in range(3):
        by=226+row*65
        c.box((10,by+4,350,by+33),'#714843',INK,3,4)
        for j in range(4):
            i=row*4+j;x=62+j*77
            rise=10*smooth(i*.075,i*.075+.25,q.scene_t) if q.id=='peers' else 22
            if q.id=='knots':rise=10+16*smooth(i*.06,i*.06+.28,q.local)
            y=by-rise+1.5*sin(q.t*3+i)
            recoil=6*smooth(.10+i*.03,.45+i*.03,q.local) if q.id=='garlic' else 0
            x+=recoil
            c.oval((x-24,y-12,x+25,y+14),'#d89d61',INK,3)
            c.oval((x-19,y-19,x+7,y+4),'#f2c683',INK,2)
            c.oval((x-3,y-16,x+19,y+3),'#e5aa68',INK,2)
            c.poly([(x+5,y-14),(x+6,y-22),(x+13,y-25),(x+11,y-17)],'#6a9c65',INK,1)
            for dx in (-8,5):c.oval((x+dx,y+1,x+dx+3,y+6),INK,None)
            c.line([(x-11,y-2),(x-4,y)],INK,2)
        c.box((6,by+12,354,by+33),'#d99b6a',INK,3,4)
    if q.id=='garlic':
        v=smooth(0,.78,q.u)
        for i in range(3):
            x=21+v*125+i*9;c.line([(x,379-i*6),(x+12,372-i*6),(x+4,362-i*6),(x+15,355-i*6)],'#b5d27a',3)

def oven(c,q):
    backdrop(c,'#55465d','#74494b')
    for x in (24,307):c.box((x,45,x+29,369),'#847080',INK,3,6)
    c.poly([(74,325),(289,325),(324,418),(43,418)],'#36303f',INK,5)
    c.box((63,162,298,365),'#d28664',INK,6,16)
    c.box((74,177,284,223),'#503c49',INK,3,9)
    for x in (97,262):
        c.oval((x-12,185,x+12,208),GOLD,INK,3)
        c.line([(x,197),(x+4*sin(q.t*3),188)],INK,2)
    c.text((179,199),'31:00' if q.id=='wait' and q.u>.22 else '30:00',23,TEAL)
    glow=round(89+24*(1+sin(q.t*7)))
    c.box((82,236,277,335),(glow,59,51),INK,5,8)
    for i in range(3):
        y=261+i*22
        c.line([(90+j*9,y+5*sin(j*.8+q.t*3)) for j in range(21)],'#ffab53',3)
    opening=16*smooth(0,.35,q.scene_t)
    c.poly([(82,319),(277,319),(285,337+opening),(78,337+opening)],'#a77764',INK,4)
    c.text((180,390),'OVEN COURT',20,GOLD)
    if q.id=='wait':sun(c,181,197,49,'#ffe589')

def guarantee(c,q):
    backdrop(c,'#73675b','#80513f')
    y=10*(1-smooth(0,.4,q.scene_t))
    c.poly([(35,157+y),(298,136+y),(331,365+y),(65,391+y)],'#e6ae76',INK,5)
    c.poly([(50,173+y),(284,155+y),(314,348+y),(77,372+y)],'#f5ce94','#bd8259',2)
    c.text((178,212+y),'DELIVERY',32,INK);c.text((179,251+y),'30 MINUTES',25,'#9a433d')
    c.line([(90,275+y),(275,263+y)],INK,2)
    c.text((182,306+y),'OR IT’S FREE',24,INK)
    if q.id in ('free','case'):
        v=smooth(.25,.65,q.u) if q.id=='free' else 1.
        summons(c,262-29*v,371-12*v,'RECEIPT')
        if q.id=='case' or q.u>.52:
            z=6*(1-smooth(.52,.68,q.u)) if q.id=='free' else 0
            c.box((71-z,336-z,214+z,375+z),'#216456',INK,3,5)
            c.text((143,356),'RELEASED',17,'#e0f6ae')
    else:
        c.line([(294,331),(265,317),(235,315+3*sin(q.t*7))],INK,7)
        c.oval((227,308,241,322),PAPER,INK,2)

def closing(c,q):
    store(c,q.t);dex(c,74,308,q.t)
    v=smooth(.30,.57,q.u) if q.id=='bite' else 1.
    c.poly([(144,359),(280,344),(309,367),(167,391)],'#f7d2a1')
    for i in range(5):
        x=159+i*23;c.line([(x,361),(x+13,378)],RED,3)
    c.box((124-9*v,301-10*v,177-9*v,323-10*v),'#e8ac66',INK,3,10)
    c.box((174+7*v,297+5*v,257+7*v,321+5*v),'#efb96e',INK,3,10)
    for i in range(3):c.line([(198+i*18,304),(194+i*18,310)],'#a56d43',3)
    if q.id=='lawyer':
        a=smooth(.04,.42,q.u)
        c.line([(240,314),(261,321-20*a),(271,313-24*a)],INK,5)
        c.box((261,300-30*a,282,313-30*a),None,INK,3,4)
        c.box((252,307-30*a,293,331-30*a),'#65434c',INK,3,4)
        c.box((270,316-30*a,276,321-30*a),GOLD,None)
        summons(c,307-142*smooth(.44,.84,q.u),359)
    elif v>0:sun(c,176,306,20+v*6,GOLD)

SETS=[opening,evidence,jury,oven,guarantee,closing]
def draw(c,q):
    zoom=1+.046*smooth(0,.95,q.scene_u)
    impact=max(0,1-abs(q.u-q.direction.get('hit',0))/.10)
    shake=1.8*impact*sin(q.local*58) if q.direction.get('sfx') in ('stamp','thump','crunch') else 0
    c.camera(zoom,(180,295),(shake,0))
    SETS[q.scene](c,q)
