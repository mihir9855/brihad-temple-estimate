"""Twin temple (Mandar prasad) as a real DXF in the owner's style + PDF sheets rendered from that DXF.
World unit = inch. Sizes are estimates from site photos (man = 6 ft); proportions per Shilp Ratnakar."""
import math, ezdxf
from ezdxf import disassemble, path as zp, bbox
from ezdxf.addons import Importer
from shapely.geometry import LineString, Polygon, box, Point
from shapely.ops import unary_union

P=108; GARBH=54; WALL=27; DOORW=28; DOORH=60; CHOK=30; MAND=120
PEETH=[("ભીત",None,9,[(0,18),(1,18)]),
 ("જાડ્યકુંભ",9,7,[(0,17),(.25,17),(.45,15.5),(.7,12),(1,10.5)]),
 ("કર્ણિકા",7,6,[(0,9.5),(.5,11.5),(1,9.5)]),
 ("ગ્રાસપટ્ટી",7,6,[(0,8.5),(1,8.5)]),
 ("ગજથર",12,9,[(0,7.5),(1,7.5)]),
 ("નરથર",8,6,[(0,6.5),(1,6.5)])]
def bulge(lo,hi,n=12): return [(k/n, lo+(hi-lo)*math.sin(math.pi*k/n)) for k in range(n+1)]
MANDO=[("ખુરો",5,4,[(0,5.5),(.6,5.5),(1,4.5)]),
 ("કુંભો",20,14,[(0,4.5),(.72,4.5),(.86,3.6),(1,2)]),
 ("કલશ",8,6,bulge(1.5,4)),
 ("અંતરાલ",2.5,2,[(0,.6),(1,.6)]),
 ("કેવાળ",8,6,[(0,1.2),(.35,3.6),(.6,3.6),(1,1.5)]),
 ("મંચી",9,7,[(0,1),(.45,3),(1,3.6)]),
 ("જંઘા",35,25,[(0,.6),(1,.6)]),
 ("ઉદ્ગમ",15,11,[(0,2.2),(.15,2.2),(1,.6)]),
 ("ભરણી",8,6,bulge(1.2,3.6)),
 ("શિરાવટી",10,7,[(0,2),(.3,2),(1,3.2)]),
 ("કપોતાલી",8,6,[(0,2),(.5,4.2),(1,3)]),
 ("અંતરાલ ",2.5,2,[(0,1),(1,1)]),
 ("છજ્જું",13,9,[(0,3),(.22,12.5),(.4,12.5),(1,2.5)])]
ROWS=[];_h=0
for _g,_l in (("p",PEETH),("m",MANDO)):
    for n,b,i,pr in _l: ROWS.append((_g,n,b,i,pr,_h)); _h+=i
HP=sum(r[3] for r in ROWS if r[0]=="p"); HM=sum(r[3] for r in ROWS if r[0]=="m")
Y0=HP+HM; HS=135; HA=24; HK=21; TOTAL=Y0+HS+HA+HK
def row(n): return next(r for r in ROWS if r[1]==n)
def fi(i):
    i=int(math.ceil(i-1e-9)); return f"{i//12}′-{i%12}″"

# ---------------- DXF document in the owner's style ----------------
doc=ezdxf.new('R2018',setup=True); doc.units=1; msp=doc.modelspace()
for n,c,lt,lw in (('A-WALL',7,'Continuous',35),('DETAIL',7,'Continuous',13),('MURTI',7,'Continuous',9),('HATCH',8,'Continuous',9),
                  ('DIM',5,'Continuous',13),('TEXT',7,'Continuous',13),('NEW',1,'Continuous',18),('CHECK',8,'DASHED',13),('CENTER',8,'DASHED',9),('FRAME',7,'Continuous',50)):
    doc.layers.add(n,color=c,linetype=lt,lineweight=lw)
doc.styles.add('GUJ',font='shruti.ttf'); doc.styles.add('ARCH 110',font='archstyl.shx')
ds=doc.dimstyles.new('MAHADEV'); ds.dxf.dimblk='ARCHTICK'; ds.dxf.dimtxt=4; ds.dxf.dimasz=3; ds.dxf.dimlunit=4; ds.dxf.dimtxsty='ARCH 110'
ds.dxf.dimclrd=5; ds.dxf.dimclre=5; ds.dxf.dimclrt=5; ds.dxf.dimexo=2; ds.dxf.dimexe=2; ds.dxf.dimgap=1.5; ds.dxf.dimtad=1; ds.dxf.dimdec=0; ds.dxf.dimrnd=1
lib=ezdxf.readfile('murti_lib.dxf'); imp=Importer(lib,doc); BH={}
for b in lib.blocks:
    if b.name.startswith('*') : continue
    imp.import_block(b.name); ex=bbox.extents(b); BH[b.name]=(ex.size.y,ex.size.x)
imp.finalize()

class View:
    def __init__(s,ox,oy): s.ox=ox; s.oy=oy; s.occ=None; s.h=[]; s.ann=[]
    def P(s,x,y): return (x+s.ox,y+s.oy)
    def item(s,lines,sil=None,layer='DETAIL',clip=True):
        for pts in lines:
            if len(pts)<2: continue
            g=LineString(pts)
            if clip and s.occ is not None and g.intersects(s.occ): g=g.difference(s.occ)
            for seg in getattr(g,'geoms',[g]):
                if seg.geom_type!='LineString' or seg.length<0.05: continue
                e=msp.add_lwpolyline([s.P(x,y) for x,y in seg.coords],dxfattribs={'layer':layer}); s.h.append(e.dxf.handle)
        if sil is not None: s.occlude(sil)
    def occlude(s,sil):
        sil=sil.buffer(0.03); s.occ=sil if s.occ is None else s.occ.union(sil)
    def block(s,name,x,y,h,mirror=False,occl=False,maxw=None):
        bh,bw=BH[name]; k=h/bh
        if s.occ is not None and s.occ.contains(Point(x,y+h/2)): return
        if maxw and bw*k>maxw: k=maxw/bw
        e=msp.add_blockref(name,s.P(x,y),dxfattribs={'xscale':-k if mirror else k,'yscale':k,'layer':'MURTI'}); s.h.append(e.dxf.handle)
        if occl: s.occlude(box(x-bw*k*.42,y,x+bw*k*.42,y+bh*k*.92))
    def hatch(s,poly,layer='HATCH',solid=False):
        hh=msp.add_hatch(color=8 if not solid else 7,dxfattribs={'layer':layer})
        if not solid: hh.set_pattern_fill('ANSI31',scale=8)
        hh.paths.add_polyline_path([s.P(x,y) for x,y in poly.exterior.coords[:-1]],is_closed=True,flags=1)
        for ring in poly.interiors: hh.paths.add_polyline_path([s.P(x,y) for x,y in ring.coords[:-1]],is_closed=True,flags=16)
        s.h.append(hh.dxf.handle)
    # annotations: kept for the PDF and written to the DXF
    def text(s,x,y,t,mm=2.7,anchor='start',cls='t'): s.ann.append(('text',x,y,t,mm,anchor,cls))
    def dimh(s,x1,x2,y,t,cls='dim'): s.ann.append(('dimh',x1,x2,y,t,cls))
    def dimv(s,y1,y2,x,t,cls='dim',left=False): s.ann.append(('dimv',y1,y2,x,t,cls,left))
    def leader(s,pts,t,mm=2.7,anchor='end',cls='t'): s.ann.append(('leader',pts,t,mm,anchor,cls))

def circ(cx,cy,r,n=28): return [(cx+r*math.cos(2*math.pi*k/n),cy+r*math.sin(2*math.pi*k/n)) for k in range(n+1)]
def rect(x0,y0,x1,y1): return [(x0,y0),(x1,y0),(x1,y1),(x0,y1),(x0,y0)]
def ell(cx,cy,rx,ry,n=28): return [(cx+rx*math.cos(2*math.pi*k/n),cy+ry*math.sin(2*math.pi*k/n)) for k in range(n+1)]

# ---------------- prasad elevation (one face, front = bhadra) ----------------
ANGAS=[('bh',-18,18),('pa',-36,-18),('pa',18,36),('ka',-54,-36),('ka',36,54)]
def thar_lines(a,c,h,i,pr):
    L=[(a-o,h+t*i) for t,o in pr]; R=[(c+o,h+t*i) for t,o in pr]
    lines=[L,R,[L[0],R[0]],[L[-1],R[-1]]]
    if len(pr)<=5: lines+= [[L[k],R[k]] for k in range(1,len(pr)-1)]
    return lines,Polygon(L+R[::-1])
def ornaments(v,kind,a,c,cx,dik,door):
    w=c-a; xm=(a+c)/2; out=[]
    g,n,b,i,pr,h=row("કુંભો")
    out.append(rect(a+2.5,h+1.5,c-2.5,h+i*.66))
    for k in range(1 if w<20 else 3):
        x=a+w*(k+.5)/(1 if w<20 else 3); out.append([(x-3,h+2.5),(x-3,h+6)]+[(x+3*math.cos(math.pi*(1-q/10)),h+6+3*math.sin(math.pi*(1-q/10))) for q in range(11)]+[(x+3,h+2.5)])
    g,n,b,i,pr,h=row("ગ્રાસપટ્ટી"); q=a+3
    while q<c-1: out.append(circ(q,h+i/2,1.6,16)); q+=5
    g,n,b,i,pr,h=row("નરથર"); q=a+2
    while q<c-1.5: out.append(rect(q,h+1,q+2.6,h+i-1)); q+=4
    g,n,b,i,pr,h=row("ગજથર")
    nh=max(1,int(w//17))
    for k in range(nh): v.block('HATHI_JODU',a+w*(k+.5)/nh,h+.7,i-1.4,maxw=w/nh-1)
    g,n,b,i,pr,h=row("જંઘા")
    if kind=='bh' and door: pass
    elif kind=='bh':
        for px in (a+3.5,c-6):
            out.append(rect(px,h+1,px+2.5,h+i-3))
            for yy in (h+5,h+i/2,h+i-7): out.append([(px-.5,yy),(px+3,yy)])
        out.append(rect(a+2.5,h+i-3,c-2.5,h+i-.8)); out.append(rect(a+7,h+1.5,c-7,h+i-3.5))
        v.block('VISHNU',xm,h+1.8,i-6)
    else:
        out.append(rect(a+1.2,h+.8,c-1.2,h+i-.8))
        if kind=='ka': v.block(dik,xm,h+1.4,i-2.8,maxw=w-3)
        else: v.block('APSARA',xm,h+1.4,i-2.8,mirror=a>cx,maxw=w-3)
    g,n,b,i,pr,h=row("ઉદ્ગમ")
    if kind=='bh' and not door:
        for fw,f0,f1 in ((.46,0,.36),(.32,.33,.68),(.17,.66,1)):
            out.append([(xm-w*fw,h+i*f0),(xm-w*fw,h+i*f1-.5),(xm-w*fw*.6,h+i*f1),(xm+w*fw*.6,h+i*f1),(xm+w*fw,h+i*f1-.5),(xm+w*fw,h+i*f0)])
        out.append(circ(xm,h+i*.5,2.2,20))
    else:
        out.append([(xm-w*.3,h+1),(xm-w*.3,h+i*.45),(xm,h+i*.8),(xm+w*.3,h+i*.45),(xm+w*.3,h+1)])
    v.item(out)
def rekha(hh,w0,H,top=.6): return w0*(1-(1-top)*(hh/H)**1.9)
def shrung(v,xc,hb,w,H,tiers=5.5,cap=True,layer='DETAIL'):
    w0=w/2; n=24
    L=[(xc-rekha(H*k/n,w0,H),hb+H*k/n) for k in range(n+1)]; R=[(xc+rekha(H*k/n,w0,H),hb+H*k/n) for k in range(n+1)]
    lines=[L,R]; sil=L+R[::-1]
    for fr in (-1/3,1/3): lines.append([(xc+fr*2*rekha(H*k/n,w0,H),hb+H*k/n) for k in range(n+1)])
    k=tiers
    while k<H-1:
        ww=rekha(k,w0,H); lines.append([(xc-ww,hb+k),(xc+ww,hb+k)]); lines.append([(xc-ww,hb+k-.8),(xc+ww,hb+k-.8)]); k+=tiers
    if cap:
        t=rekha(H,w0,H); hh=hb+H; g=t*.62; a=t*1.0; ar=w*.055
        lines.append([L[-1],R[-1]]); lines.append(rect(xc-g,hh,xc+g,hh+w*.05))
        am=ell(xc,hh+w*.05+ar,a,ar); lines.append(am)
        for q in range(-4,5): lines.append([(xc+q*a/5,hh+w*.05+ar*.25),(xc+q*a/5,hh+w*.05+ar*1.75)])
        top=hh+w*.05+2*ar; kk=[(xc-g*.55,top),(xc-g*.7,top+w*.05),(xc-g*.45,top+w*.12),(xc-g*.15,top+w*.14),(xc,top+w*.22),(xc+g*.15,top+w*.14),(xc+g*.45,top+w*.12),(xc+g*.7,top+w*.05),(xc+g*.55,top)]
        lines.append(kk); sil=L+[(xc-g,hh),(xc-a,hh+w*.05+ar),(xc-g*.7,top+w*.05),(xc,top+w*.22),(xc+g*.7,top+w*.05),(xc+a,hh+w*.05+ar),(xc+g,hh)]+R[::-1]
    else: lines.append([L[-1],R[-1]])
    v.item(lines,Polygon(sil),layer)
def main_cap(v,cx):
    y=Y0+HS; out=[rect(cx-20,y,cx+20,y+5)]
    out.append([(cx-22,y+5),(cx-27,y+6.5),(cx-29,y+8.5),(cx-27,y+10.5),(cx-22,y+12),(cx+22,y+12),(cx+27,y+10.5),(cx+29,y+8.5),(cx+27,y+6.5),(cx+22,y+5),(cx-22,y+5)])
    for k in range(-6,7): out.append([(cx+k*3.6,y+5.4),(cx+k*3.6,y+11.6)])
    out.append([(cx-19,y+12),(cx-15,y+18),(cx+15,y+18),(cx+19,y+12)])
    out.append([(cx-12,y+18),(cx-14,y+21),(cx-9,y+24),(cx+9,y+24),(cx+14,y+21),(cx+12,y+18)])
    k=y+HA; out.append([(cx-4.5,k),(cx-3,k+2.3),(cx-8,k+4),(cx-9.5,k+7),(cx-7.5,k+9.7),(cx-3.5,k+10.5),(cx-5,k+11.8),(cx-2.5,k+13.5),(cx-1.6,k+15),(cx,k+21),(cx+1.6,k+15),(cx+2.5,k+13.5),(cx+5,k+11.8),(cx+3.5,k+10.5),(cx+7.5,k+9.7),(cx+9.5,k+7),(cx+8,k+4),(cx+3,k+2.3),(cx+4.5,k)])
    px=cx+24; out.append(rect(px,y-40,px+2.2,k+34)); out.append([(px+2.2,k+33),(px+32,k+26),(px+2.2,k+18)])
    v.item(out,Polygon([(cx-29,y),(cx+29,y),(cx+29,k+21),(cx-29,k+21)]),'NEW')
def shukanas(v,cx):
    v.block('SINH',cx,Y0+70,19,occl=True)
    o=[(cx-27,Y0),(cx-25,Y0+30),(cx-20,Y0+55),(cx-15,Y0+70),(cx+15,Y0+70),(cx+20,Y0+55),(cx+25,Y0+30),(cx+27,Y0)]
    lines=[o,[(cx-15,Y0+70),(cx+15,Y0+70)],[(cx-16,Y0+66),(cx+16,Y0+66)]]
    lines+= [circ(cx,Y0+30,12,40),circ(cx,Y0+30,9,40),rect(cx-6,Y0+16,cx+6,Y0+36)]
    for k in (8,48): lines.append([(cx-25+k*.07,Y0+k),(cx+25-k*.07,Y0+k)])
    v.item(lines,Polygon(o),'NEW')
def prasad_elev(v,cx,dikL,dikR,door=False):
    gy=0
    for kind,a,c in ANGAS:
        a+=cx; c+=cx
        if door and kind=='bh':
            h0=HP; fr=[rect(cx-22,h0,cx+22,h0+74)]
            for k in (2.5,5,7.5): fr.append(rect(cx-22+k,h0+4,cx+22-k,h0+74-k))
            fr.append(rect(cx-26,h0,cx+26,h0+4)); fr.append(rect(cx-14,h0+4,cx+14,h0+4+DOORH))
            for sx in (-1,1): v.block('APSARA',cx+sx*18.2,h0+4.5,16,mirror=sx>0,maxw=5)
            v.item(fr,Polygon(rect(cx-26,h0,cx+26,h0+74)),'DETAIL')
        ornaments(v,kind,a,c,cx,dikL if a<cx else dikR,door)
        for g,n,b,i,pr,h in ROWS:
            ls,sil=thar_lines(a,c,h,i,pr); v.item(ls,sil)
    if door: shukanas(v,cx)
    else:
        shrung(v,cx,Y0,36,58)
        v.item([rect(cx-8,Y0+16,cx+8,Y0+33),rect(cx-5,Y0+18,cx+5,Y0+30)],Polygon(rect(cx-8,Y0+16,cx+8,Y0+33)))
    for sx in (-1,1): shrung(v,cx+sx*27,Y0,18,30)
    for sx in (-1,1): shrung(v,cx+sx*45,Y0,18,30)
    if not door: shrung(v,cx,Y0+38,32,64)
    for sx in (-1,1):
        x=cx+sx*25.5; v.item([rect(x-6,Y0+48,x+6,Y0+61),[(x-7,Y0+61),(x,Y0+69),(x+7,Y0+61),(x-7,Y0+61)]],Polygon([(x-7,Y0+48),(x+7,Y0+48),(x+7,Y0+61),(x,Y0+69),(x-7,Y0+61)]))
    for sx in (-1,1): shrung(v,cx+sx*39,Y0+31,15,27)
    main_cap(v,cx)
    shrung(v,cx,Y0,P-4,HS,tiers=7.5,cap=False)

# ---------------- mandap front ----------------
def stambh(v,x,y0,H):
    o=[]; segs=[(0,12,7),(12,14,6),(14,H-26,5),(H-26,H-14,6.5),(H-14,H-9,5.5),(H-9,H,9)]
    sil=[]
    for a,b,w in segs: o.append(rect(x-w,y0+a,x+w,y0+b))
    for yy in range(int(y0+20),int(y0+H-30),12): o.append([(x-5,yy),(x+5,yy)]); o.append([(x-5,yy+1.2),(x+5,yy+1.2)])
    o.append(ell(x,y0+H-20,6.5,4)); o.append([(x-5,y0+3),(x-2,y0+9),(x+2,y0+9),(x+5,y0+3)])
    v.item(o,Polygon(rect(x-9,y0,x+9,y0+H)).union(Polygon(rect(x-7,y0,x+7,y0+12))))
def mandap_front(v):
    y=HP; Hs=HM; xs=(-54,-18,18,54)
    # steps + elephants (front)
    for sx in (-1,1):
        v.block('HATHI_SAVAR',sx*44,8,46,mirror=sx>0,occl=True)
        v.item([rect(sx*44-20,0,sx*44+20,8)],Polygon(rect(sx*44-20,0,sx*44+20,8)))
    st=[]; n=6; th=HP/n
    peeth_band_later=True
    for k in range(n): st.append([(-24,k*th),(24,k*th)])
    st+=[[(-24,0),(-24,HP)],[(24,0),(24,HP)]]
    v.item(st,Polygon(rect(-24,0,24,HP)))
    peeth_band(v,-62,62)
    # toran in the entrance
    t=[]; base=y+70; top=y+Hs-12; pts=[]
    for k in range(5):
        a0=-18+7+k*(22/5); a1=a0+22/5; r=(a1-a0)/2; mx=(a0+a1)/2
        yb=base+(top-base-8)*math.sin(math.pi*(k+.5)/5)
        pts+=[(mx+r*math.cos(math.pi*(1-q/8)),yb+r*math.sin(math.pi*(1-q/8))) for q in range(9)]
    t.append([(-11,y),(-11,base)]+pts+[(11,base),(11,y)])
    v.item(t)
    for x in xs: stambh(v,x,y,Hs)
    for a,b in ((-54,-18),(18,54)):
        a2=a+9; b2=b-9; vd=[rect(a2,y,b2,y+12),rect(a2,y+12,b2,y+28),rect(a2-1,y+28,b2+1,y+32),[(a2-1,y+32),(a2+1,y+46),(b2-1,y+46),(b2+1,y+32)]]
        q=a2+3
        while q<b2-4: vd.append(rect(q,y+14,q+6,y+26)); q+=8
        v.item(vd,Polygon([(a2-1,y),(b2+1,y),(b2+1,y+32),(b2-1,y+46),(a2+1,y+46),(a2-1,y+32)]))
    bm=y+Hs; v.item([rect(-62,bm,62,bm+10),[(-62,bm+3),(62,bm+3)]],Polygon(rect(-62,bm,62,bm+10)))
    ch=bm+10; v.item([[(-62,ch),(-72,ch+5),(-72,ch+7),(72,ch+7),(72,ch+5),(62,ch)],[(-62,ch),(62,ch)]],Polygon([(-62,ch),(-72,ch+5),(-72,ch+7),(72,ch+7),(72,ch+5),(62,ch)]))
    # samran: flat tiers with curled ends (owner's design)
    yy=ch+7; w=64; sil=[]
    for k in range(6):
        hh=7.5; ww=w-k*7.5
        o=[rect(-ww,yy,ww,yy+hh)]
        for sx in (-1,1): o.append([(sx*ww,yy+hh),(sx*(ww+3),yy+hh+1.5),(sx*(ww+4.5),yy+hh-1),(sx*(ww+2.5),yy+hh-2.5),(sx*(ww+1.5),yy+hh-.8)])
        v.item(o,Polygon(rect(-ww-4.5,yy,ww+4.5,yy+hh+1.5))); yy+=hh
    o=[[(-16,yy),(-10,yy+9),(10,yy+9),(16,yy)],ell(0,yy+13,14,4.5),rect(-6,yy+17.5,6,yy+20)]
    k=yy+20; o.append([(-4,k),(-8,k+4),(-7.5,k+8),(-3,k+9.5),(-1.5,k+12),(0,k+17),(1.5,k+12),(3,k+9.5),(7.5,k+8),(8,k+4),(4,k)])
    v.item(o,Polygon(rect(-16,yy,16,yy+37)),'NEW')
    # the whole front bay is solid except the openings between pillars
    v.occlude(Polygon(rect(-80,0,80,HP)))
    v.occlude(Polygon(rect(-72,bm,72,yy+37)))
    for x in xs: v.occlude(Polygon(rect(x-9,y,x+9,bm)))
    for a,b in ((-54,-18),(18,54)): v.occlude(Polygon(rect(a,y,b,y+46)))
    return yy+37
def peeth_band(v,a,c):
    for g,n,b,i,pr,h in ROWS:
        if g=='p': ls,sil=thar_lines(a,c,h,i,pr); v.item(ls,sil)

# ---------------- build views ----------------
D=MAND/2+CHOK+9+P/2      # mandap centre to prasad centre = 153
V1=View(0,0); V2=View(2000,0); V3=View(4000,0); V4=View(6000,0)

# V1 plan
def outline():
    h=P/2; half=[(-h,0),(-h+18,0),(-h+18,4),(-h+36,4),(-h+36,9),(h-36,9),(h-36,4),(h-18,4),(h-18,0),(h,0)]; pts=[]
    for r in range(4):
        for a,o in half:
            x,y=a,-h-o
            for _ in range(r): x,y=-y,x
            pts.append((x,y))
    return pts
def rot(pts,ang,cx,cy):
    c,s=math.cos(math.radians(ang)),math.sin(math.radians(ang)); return [(cx+x*c-y*s,cy+x*s+y*c) for x,y in pts]
def prasad_plan(v,cx,cy,ang,dashed=False):
    o=rot(outline(),ang,cx,cy); g=GARBH/2
    if dashed:
        v.item([o+[o[0]],rot(rect(-g,-g,g,g),ang,cx,cy)],layer='CHECK'); return
    door=rot([(-DOORW/2,0),(DOORW/2,0),(DOORW/2,P/2+10),(-DOORW/2,P/2+10)],ang,cx,cy)
    wall=Polygon(o).difference(Polygon(rot(rect(-g,-g,g,g)[:-1],ang,cx,cy)).union(Polygon(door)))
    v.hatch(wall); v.item([list(wall.exterior.coords)]+[list(r.coords) for r in wall.interiors],layer='A-WALL',clip=False)
    for r in (0,90,270):
        n=rot(rot(rect(-7,-P/2-9.2,7,-P/2-4)[:-1],r,0,0),ang,cx,cy); v.item([n+[n[0]]],clip=False)
    for k in (4,7): v.item([rot([(-DOORW/2,P/2+k),(DOORW/2,P/2+k)],ang,cx,cy)],clip=False)
    v.item([rot(circ(0,0,5),ang,cx,cy),rot(circ(0,0,2.2),ang,cx,cy)],clip=False)
    for sx in (-1,1):
        q=rot(rect(sx*18-6,P/2+9+CHOK-14,sx*18+6,P/2+9+CHOK-2),ang,cx,cy); q2=rot(rect(sx*18-3.5,P/2+9+CHOK-11.5,sx*18+3.5,P/2+9+CHOK-4.5),ang,cx,cy)
        v.item([q,q2],layer='A-WALL',clip=False)
def plan(v):
    prasad_plan(v,0,D,180); prasad_plan(v,-D,0,270); prasad_plan(v,D,0,90,True)
    m=MAND/2; v.item([rect(-m,-m,m,m)],layer='A-WALL',clip=False); v.item([rect(-m-6,-m-6,m+6,m+6)],clip=False)
    ring=[(x,y) for x in (-54,-18,18,54) for y in (-54,-18,18,54) if abs(x)==54 or abs(y)==54]
    for x,y in ring: v.item([rect(x-7,y-7,x+7,y+7),rect(x-4.5,y-4.5,x+4.5,y+4.5)],layer='A-WALL',clip=False)
    v.item([rect(-54,-54,54,54)],layer='CENTER',clip=False)
    v.item([[(-18,54),(-54,18),(-54,-18),(-18,-54),(18,-54),(54,-18),(54,18),(18,54),(-18,54)]],layer='CENTER',clip=False)
    for a,b in ((-54,-18),(18,54)):
        for sy in (-1,):
            p=Polygon(rect(a+7,sy*54-3.5,b-7,sy*54+3.5)); v.hatch(p); v.item([list(p.exterior.coords)],clip=False)
    for a,b in ((-54,-18),(18,54)):
        p=Polygon(rect(54-3.5,a+7,54+3.5,b-7)); v.hatch(p); v.item([list(p.exterior.coords)],clip=False)
    for k in range(7): v.item([[(-24,-m-6-k*9),(24,-m-6-k*9)]],clip=False)
    v.item([[(-24,-m-6),(-24,-m-60)],[(24,-m-6),(24,-m-60)]],clip=False)
plan(V1)

# V2 front elevation of the group (front to back)
top=mandap_front(V2)
for sx in (-1,):   # chokki pillar + beam of the west shrine
    x=-60-CHOK/2-4; stambh(V2,x,HP,HM); V2.item([rect(-60-CHOK-9,HP+HM,-60,HP+HM+10)],Polygon(rect(-60-CHOK-9,HP+HM,-60,HP+HM+10)))
    V2.item([rect(-112,0,-60,HP)],None)
    peeth_band(V2,-108,-62)
prasad_elev(V2,-D,'DIK_YAM','DIK_AGNI')
mark=len(V2.h)
prasad_elev(V2,0,'DIK_YAM','DIK_AGNI',door=True)
# third shrine: dashed outline only
ghost=View(0,0); prasad_elev(ghost,D,'DIK_YAM','DIK_AGNI')
for hd in ghost.h: msp.delete_entity(doc.entitydb[hd])
sil=max(getattr(ghost.occ,'geoms',[ghost.occ]),key=lambda g:g.area).simplify(.3)
V2.item([list(sil.exterior.coords)],layer='CHECK')
V2.item([[(-260,0),(260,0)]],layer='A-WALL',clip=False)

# V3 side elevation of one shrine (south face)
prasad_elev(V3,0,'DIK_YAM','DIK_AGNI')
V3.item([[(-90,0),(90,0)]],layer='A-WALL',clip=False)

# V4 section of peeth + mandovar
pts=[]
for g,n,b,i,pr,h in ROWS:
    for t,o in pr: pts.append((-o,h+t*i))
sec=Polygon(pts+[(34,Y0),(34,0)]).buffer(0)
V4.hatch(sec); V4.item([list(sec.exterior.coords)],layer='A-WALL',clip=False)
V4.item([[(0,-3),(0,Y0+6)]],layer='CENTER',clip=False); V4.item([[(-40,0),(50,0)]],layer='A-WALL',clip=False)
for g,n,b,i,pr,h in ROWS: V4.item([[(-max(o for _,o in pr),h),(0,h)]],clip=False)
