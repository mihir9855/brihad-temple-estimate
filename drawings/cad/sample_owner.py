"""Sample: one prasad of the twin temple drawn with the owner's own CAD lines (Ambaji elevation, vector PDF),
mirrored about the centre and fitted to this temple's sizes."""
import math, ezdxf, pymupdf as fitz
from shapely.geometry import LineString, Polygon, box
from shapely.affinity import scale as sscale
SRC='/root/.claude/uploads/b113044e-3600-59b5-a6ad-4d97fce82858/316f08ea-ambaji_chotulal_Elevation.pdf'
pg=fitz.open(SRC)[0]; dr=pg.get_drawings()
def flat(it,n=10):
    k=it[0]
    if k=='l': return [(it[1].x,it[1].y),(it[2].x,it[2].y)]
    if k=='c':
        p0,p1,p2,p3=it[1:5]; out=[]
        for i in range(n+1):
            t=i/n; a=(1-t)**3; b=3*t*(1-t)**2; c=3*t*t*(1-t); d=t**3
            out.append((a*p0.x+b*p1.x+c*p2.x+d*p3.x, a*p0.y+b*p1.y+c*p2.y+d*p3.y))
        return out
    if k=='re': r=it[1]; return [(r.x0,r.y0),(r.x1,r.y0),(r.x1,r.y1),(r.x0,r.y1),(r.x0,r.y0)]
    if k=='qu': q=it[1]; return [(q.ul.x,q.ul.y),(q.ur.x,q.ur.y),(q.lr.x,q.lr.y),(q.ll.x,q.ll.y),(q.ul.x,q.ul.y)]
    return []
lines=[];fills=[]
for d in dr:
    if d.get('color') and d['color'][0]>.5: continue          # orange dimension lines
    pts=[flat(it) for it in d['items']]
    if d.get('fill') is not None:
        ring=[p for s in pts for p in s]
        if len(ring)>=3: fills.append(ring)
    if d.get('color') is not None:
        lines+= [s for s in pts if len(s)>=2]
# centre axis from the top kalash
xs=[x for s in lines for x,y in s if 133<=y<=150 and 118<=x<=138]; CX=(min(xs)+max(xs))/2
YCUT=290.0
UP=box(CX,131.2,192,YCUT); LO=box(71,YCUT,CX,415.5)
# our sizes (inch)
Y0=148; TOTAL=328
def mapy(y):
    knots=[(415.0,0),(407.1,9),(312.4,Y0-9),(303.0,Y0),(133.0,TOTAL)]
    for (a,A),(b,B) in zip(knots,knots[1:]):
        if b<=y<=a or (y>a and a==knots[0][0]) or (y<b and b==knots[-1][0]): return A+(y-a)*(B-A)/(b-a)
    return 0
left_edge=min(x for s in lines for x,y in s if 330<y<400 and x>71)
SX=58/(CX-left_edge)
def T(x,y,mirror): return ((2*CX-x-CX if mirror else x-CX)*SX, mapy(y))
OUT=[];OUTF=[]
for s in lines:
    g=LineString(s)
    for reg,src_right in ((UP,True),(LO,False)):
        if not g.intersects(reg): continue
        c=g.intersection(reg)
        for seg in getattr(c,'geoms',[c]):
            if seg.geom_type!='LineString' or seg.length<.01: continue
            P=list(seg.coords)
            for mir in (False,True): OUT.append([T(x,y,mir) for x,y in P])
for r in fills:
    try: g=Polygon(r).buffer(0)
    except Exception: continue
    for reg in (UP,LO):
        c=g.intersection(reg)
        for pp in getattr(c,'geoms',[c]):
            if pp.geom_type!='Polygon' or pp.area<1e-3: continue
            P=list(pp.exterior.coords)
            for mir in (False,True): OUTF.append([T(x,y,mir) for x,y in P])
print('centre',round(CX,2),'scale x',round(SX,3),'lines',len(OUT),'fills',len(OUTF))
# DXF
doc=ezdxf.new('R2018',setup=True); doc.units=1; m=doc.modelspace(); doc.layers.add('0-OWNER',color=7)
for p in OUT: m.add_lwpolyline(p,dxfattribs={'layer':'0-OWNER'})
for p in OUTF:
    h=m.add_hatch(color=7,dxfattribs={'layer':'0-OWNER'}); h.paths.add_polyline_path(p,is_closed=True)
doc.saveas('Sample-Prasad-Owner-Lines.dxf')
# PDF sheet (A3 portrait-ish landscape)
k=0.68; X0=210; GY=268
M=lambda x,y:(X0+x*k,GY-y*k)
d=' '.join('M'+' '.join(f'{a:.2f},{b:.2f}' for a,b in (M(x,y) for x,y in p)) for p in OUT)
f=' '.join('M'+' '.join(f'{a:.2f},{b:.2f}' for a,b in (M(x,y) for x,y in p))+'Z' for p in OUTF)
def fi(i): i=int(math.ceil(i-1e-9)); return f"{i//12}′-{i%12}″"
def dimv(y1,y2,x,t):
    X,Y1=M(x,y1);_,Y2=M(x,y2); return f'<line x1="{X}" y1="{Y1}" x2="{X}" y2="{Y2}" stroke="#0a3d91" stroke-width=".15"/><line x1="{X-1.3}" y1="{Y1}" x2="{X+1.3}" y2="{Y1}" stroke="#0a3d91" stroke-width=".15"/><line x1="{X-1.3}" y1="{Y2}" x2="{X+1.3}" y2="{Y2}" stroke="#0a3d91" stroke-width=".15"/><text x="{X+1.6}" y="{(Y1+Y2)/2+1}" class="dim">{t}</text>'
svg=f'''<svg viewBox="0 0 420 297" xmlns="http://www.w3.org/2000/svg"><style>text{{font-family:'Noto Sans Gujarati',sans-serif}}.dim{{font-size:3px;fill:#0a3d91}}.h{{font-size:5.5px;font-weight:700}}.t{{font-size:3px}}</style>
<rect x="8" y="8" width="404" height="281" fill="none" stroke="#111" stroke-width=".45"/>
<text x="16" y="20" class="h">નમૂનો — એક પ્રાસાદ, તમારી અંબાજી ડ્રોઇંગ ની જ રેખા માંથી</text>
<text x="16" y="28" class="t">ડાબી બાજુ ની રેખા લઈ જમણી બાજુ અરીસા માં (ધજા ન આવે એટલે શિખર જમણી બાજુ થી). માપ આ મંદિર ના: પ્રાસાદ 9′-0″, મંડોવર 12′-4″, કુલ 27′-4″ (અંદાજી).</text>
<path d="{f}" fill="#111" stroke="none"/><path d="{d}" fill="none" stroke="#111" stroke-width=".2" stroke-linejoin="round"/>
<line x1="{M(-110,0)[0]}" y1="{GY}" x2="{M(110,0)[0]}" y2="{GY}" stroke="#111" stroke-width=".4"/>
{dimv(0,Y0,95,"મંડોવર + પીઠ "+fi(Y0))}{dimv(Y0,TOTAL,95,"શિખર "+fi(TOTAL-Y0))}{dimv(0,TOTAL,125,"કુલ "+fi(TOTAL))}
</svg>'''
open('sample.html','w').write('<!doctype html><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?family=Noto+Sans+Gujarati:wght@400;700&display=swap" rel="stylesheet"><style>@page{size:420mm 297mm;margin:0}body{margin:0}.pg{width:420mm;height:297mm;position:relative}.pg svg{position:absolute;inset:0;width:420mm;height:297mm}</style><div class="pg">'+svg+'</div>')
