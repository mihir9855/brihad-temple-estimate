exec(open('build.py').read())
SHEETS=5
CSS="""@page{size:420mm 297mm;margin:0}*{box-sizing:border-box}body{margin:0;font-family:'Noto Sans Gujarati',sans-serif;color:#111}
.pg{width:420mm;height:297mm;position:relative;page-break-after:always;overflow:hidden}.pg>svg{position:absolute;inset:0;width:420mm;height:297mm}
text{font-family:'Noto Sans Gujarati',sans-serif;fill:#111}.t{font-size:2.6px}.s{font-size:2.1px}.b{font-size:3.3px;font-weight:700}.h{font-size:5.2px;font-weight:700}
.dim{font-size:2.4px;fill:#0a3d91}.red{fill:#b3261e}.kk{stroke:#111;fill:none;stroke-width:.45}.th{stroke:#111;fill:none;stroke-width:.12}.f{stroke:#111;fill:#fff;stroke-width:.25}.dl{stroke:#0a3d91;fill:none;stroke-width:.12}
.L-DETAIL{stroke:#111;fill:none;stroke-width:.13;stroke-linejoin:round}.L-A-WALL{stroke:#000;fill:none;stroke-width:.32}.L-MURTI{stroke:#111;fill:none;stroke-width:.07}
.L-NEW{stroke:#b3261e;fill:none;stroke-width:.18}.L-CHECK{stroke:#666;fill:none;stroke-width:.2;stroke-dasharray:1.6 1}.L-CENTER{stroke:#777;fill:none;stroke-width:.12;stroke-dasharray:2 .8 .4 .8}
.L-FILL{fill:#111;stroke:none}.L-HAT{fill:url(#hat);stroke:none}
.txt{position:absolute;left:18mm;top:30mm;right:18mm;font-size:11pt;line-height:1.45}.txt h2{font-size:13.5pt;margin:4mm 0 2mm;border-bottom:.3mm solid #111}
table{border-collapse:collapse;width:100%}td,th{border:.25mm solid #333;padding:1mm 2mm;text-align:left;vertical-align:top;font-size:10pt}th{background:#eee}.cols{display:grid;grid-template-columns:1.2fr 1fr;gap:8mm}"""
def frame(title,sheet,scale):
    return f'''<rect x="8" y="8" width="404" height="281" class="kk"/><rect x="10" y="10" width="400" height="277" class="th"/>
<rect x="290" y="259" width="120" height="28" class="f"/><line x1="290" y1="269" x2="410" y2="269" class="th"/><line x1="290" y1="278" x2="410" y2="278" class="th"/><line x1="370" y1="269" x2="370" y2="287" class="th"/>
<text x="293" y="266" class="b">જોડિયા મંદિર · મંદર પ્રાસાદ (25 અંડક)</text><text x="293" y="275" class="t">{title}</text><text x="373" y="275" class="t">શીટ {sheet} / {SHEETS}</text>
<text x="293" y="284" class="s">⚠ અંદાજી માપ — ફોટા પરથી (માણસ = 6′-0″)</text><text x="373" y="284" class="s">{scale}</text>
<defs><pattern id="hat" width="1.3" height="1.3" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="1.3" stroke="#555" stroke-width=".12"/></pattern>
<marker id="ar" viewBox="0 0 6 6" refX="3" refY="3" markerWidth="4" markerHeight="4" orient="auto"><path d="M1,5 L5,1" stroke="#0a3d91" stroke-width="1"/></marker></defs>'''
class Win:
    def __init__(s,v,wx0,wy0,wx1,wy1,X0,Y0,W,H):
        s.v=v; s.wx0,s.wy0,s.wx1,s.wy1=wx0,wy0,wx1,wy1; s.k=min(W/(wx1-wx0),H/(wy1-wy0))
        s.X0=X0+(W-(wx1-wx0)*s.k)/2; s.Y0=Y0+(H-(wy1-wy0)*s.k)/2
    def M(s,x,y): return (s.X0+(x-s.wx0)*s.k, s.Y0+(s.wy1-y)*s.k)
    def svg(s,cid):
        d={}; v=s.v; dist=.025
        def add(cls,pts,close=False):
            if len(pts)<2: return
            q=[s.M(p[0]-v.ox,p[1]-v.oy) for p in pts]
            d.setdefault(cls,[]).append('M'+' '.join(f'{a:.2f},{b:.2f}' for a,b in q)+('Z' if close else ''))
        for hd in v.h:
            e=doc.entitydb.get(hd)
            if e is None: continue
            prims=disassemble.recursive_decompose([e]) if e.dxftype()=='INSERT' else [e]
            for p in prims:
                t=p.dxftype()
                if t in ('TEXT','MTEXT','ATTRIB','ATTDEF','POINT','DIMENSION','SOLID','3DFACE','INSERT'): continue
                lay=p.dxf.layer if p.dxf.layer in ('DETAIL','A-WALL','NEW','CHECK','CENTER','HATCH') else 'MURTI'
                if t=='HATCH':
                    cls='L-HAT' if lay=='HATCH' else 'L-FILL'
                    for ph in zp.from_hatch(p): add(cls,list(ph.flattening(dist)),True)
                    continue
                try: ph=zp.make_path(p)
                except Exception: continue
                if len(ph)==0 and t!='LINE': continue
                add('L-'+lay,list(ph.flattening(dist)))
        x0,y0=s.M(s.wx0,s.wy1); x1,y1=s.M(s.wx1,s.wy0)
        out=f'<clipPath id="{cid}"><rect x="{x0:.2f}" y="{y0:.2f}" width="{x1-x0:.2f}" height="{y1-y0:.2f}"/></clipPath><g clip-path="url(#{cid})">'
        for cls in ('L-HAT','L-FILL','L-MURTI','L-DETAIL','L-A-WALL','L-CENTER','L-CHECK','L-NEW'):
            if cls in d: out+=f'<path class="{cls}" fill-rule="evenodd" d="{" ".join(d[cls])}"/>'
        return out+'</g>'
    def ann(s):
        o=''; v=s.v
        for a in v.ann:
            if a[0]=='text':
                _,x,y,t,mm,anc,cls=a; X,Y=s.M(x,y); o+=f'<text x="{X:.2f}" y="{Y:.2f}" text-anchor="{anc}" class="{cls}">{t}</text>'
                msp.add_mtext(t,dxfattribs={'style':'GUJ','char_height':mm/s.k,'layer':'TEXT','insert':v.P(x,y),'attachment_point':{'start':7,'middle':8,'end':9}[anc]})
            elif a[0]=='leader':
                _,pts,t,mm,anc,cls=a; q=[s.M(x,y) for x,y in pts]
                o+='<polyline class="dl" points="'+' '.join(f'{X:.2f},{Y:.2f}' for X,Y in q)+f'"/><circle cx="{q[-1][0]:.2f}" cy="{q[-1][1]:.2f}" r=".35" fill="#0a3d91"/>'
                X,Y=q[0]; o+=f'<text x="{X+(-1 if anc=="end" else 1):.2f}" y="{Y+.9:.2f}" text-anchor="{anc}" class="{cls}">{t}</text>'
                msp.add_lwpolyline([v.P(x,y) for x,y in pts],dxfattribs={'layer':'DIM'})
                msp.add_mtext(t,dxfattribs={'style':'GUJ','char_height':mm/s.k,'layer':'TEXT','insert':v.P(*pts[0]),'attachment_point':9 if anc=='end' else 7})
            elif a[0]=='dimh':
                _,x1,x2,y,t,cls=a; X1,Y=s.M(x1,y); X2,_=s.M(x2,y)
                o+=f'<line x1="{X1:.2f}" y1="{Y:.2f}" x2="{X2:.2f}" y2="{Y:.2f}" class="dl" marker-start="url(#ar)" marker-end="url(#ar)"/><line x1="{X1:.2f}" y1="{Y-1.3:.2f}" x2="{X1:.2f}" y2="{Y+1.3:.2f}" class="dl"/><line x1="{X2:.2f}" y1="{Y-1.3:.2f}" x2="{X2:.2f}" y2="{Y+1.3:.2f}" class="dl"/><text x="{(X1+X2)/2:.2f}" y="{Y-.9:.2f}" text-anchor="middle" class="{cls}">{t}</text>'
                msp.add_linear_dim(base=v.P(x1,y),p1=v.P(x1,y),p2=v.P(x2,y),dimstyle='MAHADEV',dxfattribs={'layer':'DIM'}).render()
            elif a[0]=='dimv':
                _,y1,y2,x,t,cls,left=a; X,Y1=s.M(x,y1); _,Y2=s.M(x,y2)
                o+=f'<line x1="{X:.2f}" y1="{Y1:.2f}" x2="{X:.2f}" y2="{Y2:.2f}" class="dl" marker-start="url(#ar)" marker-end="url(#ar)"/><line x1="{X-1.3:.2f}" y1="{Y1:.2f}" x2="{X+1.3:.2f}" y2="{Y1:.2f}" class="dl"/><line x1="{X-1.3:.2f}" y1="{Y2:.2f}" x2="{X+1.3:.2f}" y2="{Y2:.2f}" class="dl"/><text x="{X+(-1.4 if left else 1.4):.2f}" y="{(Y1+Y2)/2+.9:.2f}" text-anchor="{'end' if left else 'start'}" class="{cls}">{t}</text>'
                msp.add_linear_dim(base=v.P(x,y1),p1=v.P(x,y1),p2=v.P(x,y2),angle=90,dimstyle='MAHADEV',dxfattribs={'layer':'DIM'}).render()
        v.ann=[]
        return o
def note(lines,x=16,y=32):
    return ''.join(f'<text x="{x}" y="{y+i*5}" class="{"b" if i==0 else "t"}">{t}</text>' for i,t in enumerate(lines))

# ---------- sheet 1: plan ----------
m=MAND/2; v=V1
v.text(0,D+12,'ગર્ભગૃહ 1',3,'middle'); v.text(-D,12,'ગર્ભગૃહ 2',3,'middle'); v.text(D,0,'ત્રીજો પ્રાસાદ ? ⚠',2.6,'middle','s'); v.text(D,-8,'(સાઇટ પર તપાસો)',2.3,'middle','s')
v.text(0,4,'મંડપ',3.4,'middle','b'); v.text(0,-6,'8 હાંસ · 12 સ્તંભ',2.4,'middle','s'); v.text(0,-12,'(છત પડી ગઈ છે)',2.2,'middle','s')
v.text(0,-m-70,'પગથિયાં · પ્રવેશ',2.6,'middle'); v.text(0,72,'ચોકી',2.4,'middle','s'); v.text(-75,10,'ચોકી',2.4,'middle','s')
v.leader([(95,-95),(36,-56)],'વેદિકા (કક્ષાસન)',2.5,'start')
y=D+54+9; v.dimh(-54,54,y+26,f'પ્રાસાદ (રેખા થી રેખા) {fi(P)}')
xs=[-54,-36,-18,18,36,54]; nm=['કર્ણ','પઢરો','ભદ્ર','પઢરો','કર્ણ']
for i in range(5): v.dimh(xs[i],xs[i+1],y+12,f'{nm[i]} {xs[i+1]-xs[i]}″','dim s')
v.dimv(D-27,D+27,54+9+12,f'ગર્ભગૃહ {fi(GARBH)}'); v.dimv(D-54,D-27,54+9+12,f'દીવાલ {fi(WALL)}'); v.dimv(m,D-54-9,54+9+12,f'ચોકી {fi(CHOK)}')
v.dimv(-m,m,D+54+28,f'મંડપ {fi(MAND)}'); v.dimh(-D-63,D+63,-m-85,f'કુલ પહોળાઈ (ત્રણ પ્રાસાદ હોય તો) {fi(2*D+126)}')
v.dimh(-DOORW/2,DOORW/2,D-54-16,f'દ્વાર {fi(DOORW)}','dim s')
W1=Win(V1,-250,-150,265,250,12,22,396,236)
s1=W1.svg('c1')+W1.ann()+note(['નોંધ','• પ્રાસાદ : મંદર — તલ 12 ભાગ, 1 ભાગ = 9″','• કર્ણ 2 · પઢરો 2 · અર્ધ ભદ્ર 2 ભાગ','• ભદ્ર નો નીકાળો 9″, પઢરા નો 4″','• ત્રણ ભદ્રે ગવાક્ષ, દ્વાર આગળ ચોકી','• મંડપ : 12 સ્તંભ, વચ્ચે અષ્ટકોણ','• તૂટક લીટી = ત્રીજો પ્રાસાદ હોઈ શકે ⚠','▨ દીવાલ (ANSI31 હેચ)'])

# ---------- sheet 2: front elevation of the group ----------
v=V2
v.leader([(-95,372),(-105,372),(-D+10,Y0+HS-10)],'ગર્ભગૃહ 2 — દક્ષિણ બાજુ',2.6,'start')
v.leader([(120,330),(10,Y0+HS-20)],'ગર્ભગૃહ 1 નું શિખર (પાછળ)',2.6,'start')
v.leader([(120,270),(30,top-20)],'મંડપ નું સામરણ (6 થર)',2.6,'start')
v.leader([(120,240),(14,HP+90)],'તોરણ',2.6,'start'); v.leader([(120,225),(40,HP+30)],'વેદિકા (કક્ષાસન)',2.6,'start')
v.leader([(120,210),(54,HP+60)],'મંડપ ના સ્તંભ',2.6,'start'); v.leader([(-75,-26),(-44,15)],'હાથી (સવાર સાથે)',2.6,'end')
v.text(D,Y0+40,'ત્રીજો પ્રાસાદ ? ⚠',2.8,'middle','s')
v.dimv(0,HP,-D-80,f'પીઠ {fi(HP)}',left=True); v.dimv(HP,Y0,-D-80,f'મંડોવર {fi(HM)}',left=True); v.dimv(Y0,Y0+HS,-D-80,f'શિખર {fi(HS)}',left=True); v.dimv(Y0+HS,TOTAL,-D-80,f'{fi(HA+HK)}',left=True)
v.dimv(0,TOTAL,-D-128,f'કુલ ઊંચાઈ {fi(TOTAL)}',left=True); v.dimh(-D-63,D+63,-14,f'કુલ પહોળાઈ {fi(2*D+126)}',); v.dimv(0,top,90,f'મંડપ {fi(top)}')
W2=Win(V2,-330,-24,260,385,12,22,396,236)
s2=W2.svg('c2')+W2.ann()+note(['નોંધ','• કાળી લીટી = હાલ નું કામ','• લાલ લીટી = નવું બનાવવાનું','• તૂટક = ત્રીજો પ્રાસાદ ⚠','• મૂર્તિઓ તમારી DXF ના બ્લોક'])

# ---------- sheet 3: side elevation with names ----------
v=V3; lx=-130
ys=[h+i/2 for g,n,b,i,pr,h in ROWS]; lab=ys[:]
for k in range(1,len(lab)):
    if lab[k]<lab[k-1]+7.2: lab[k]=lab[k-1]+7.2
sh=(sum(ys)-sum(lab))/len(ys)*.5; lab=[q+sh for q in lab]
for (g,n,b,i,pr,h),yy,ly in zip(ROWS,ys,lab):
    off=max(o for _,o in pr); v.leader([(lx,ly),(lx+10,ly),(-54-off-1,yy)],f'{n}{" · "+str(b)+" ભાગ" if b else ""} — {i}″',2.5,'end')
v.text(lx,lab[-1]+10,'મંડોવર 144 ભાગ ↑',3.2,'end','b'); v.text(lx-62,lab[5]-2,'પીઠ ↑',3.2,'end','b')
SL=[('મૂળ શિખર (રેખા)',-25,Y0+118),('ઉરુશૃંગ 2',-6,Y0+92),('તિલક',-25.5,Y0+56),('કર્ણ શૃંગ 2',-39,Y0+48),('ઉરુશૃંગ 1 (ભદ્રે)',0,Y0+50),('પઢરા નું શૃંગ',-27,Y0+22),('રથિકા (ગવાક્ષ)',0,Y0+24),('કર્ણ શૃંગ 1',-47,Y0+12)]
for k,(t,x,h) in enumerate(sorted(SL,key=lambda q:-q[2])): v.leader([(lx,Y0+150-k*10),(lx+10,Y0+150-k*10),(x,h)],t,2.5,'end')
ky=Y0+HS
for t,h in (('ધ્વજદંડ · ધજા (નવું)',ky+HA+30),('કલશ (નવો)',ky+HA+8),('આમલસારો · ચંદ્રિકા (નવો)',ky+12),('સ્કંધ (બંધન)',ky)):
    v.leader([(95,h),(85,h),(22 if 'સ્કંધ' not in t else 30,h)],t,2.5,'start','t red' if 'નવ' in t else 't')
jg=row('જંઘા'); hj=jg[5]+jg[3]/2
v.text(0,-30,'જંઘા ની મૂર્તિ, ડાબે થી : યમ (દિક્પાળ) · અપ્સરા · વિષ્ણુ (ભદ્ર ગવાક્ષ) · અપ્સરા · અગ્નિ (દિક્પાળ)',2.6,'middle')
gj=row('ગજથર'); v.leader([(95,gj[5]-6),(85,gj[5]-6),(46,gj[5]+3)],'હાથી ની જોડ (ગજથર)',2.5,'start')
dx=150
for a,b,t in ((0,9,'ભીત 9″'),(9,HP,f'પીઠ {fi(HP-9)}'),(HP,Y0,f'મંડોવર {fi(HM)}'),(Y0,Y0+HS,f'શિખર {fi(HS)}'),(Y0+HS,Y0+HS+HA,f'આમલસારો {HA}″'),(Y0+HS+HA,TOTAL,f'કલશ {HK}″')): v.dimv(a,b,dx,t)
v.dimv(0,TOTAL,dx+36,f'કુલ ઊંચાઈ {fi(TOTAL)}')
v.dimh(-54,54,-17,f'પ્રાસાદ {fi(P)}')
for i in range(5): v.dimh(xs[i],xs[i+1],-8,f'{nm[i]} {xs[i+1]-xs[i]}″','dim s')
W3=Win(V3,-215,-36,205,380,12,22,396,236)
s3=W3.svg('c3')+W3.ann()+note(['નોંધ','• દક્ષિણ બાજુ નું દર્શન','• અંડક : 1 + કર્ણ 8 + પઢરા 8 + ઉરુશૃંગ 8 = 25','• કર્ણે દિક્પાળ — દક્ષિણ બાજુ : યમ, અગ્નિ ⚠','• લાલ = નવું બનાવવાનું'],x=300,y=32)

# ---------- sheet 4: section + half elevation ----------
v=V4
for g,n,b,i,pr,h in ROWS:
    off=max(o for _,o in pr); v.text(-off-2,h+i/2-1,f'{n} {i}″',2.1,'end','s')
v.text(1,Y0+3,'દીવાલ ની રેખા',2.1,'start','s')
v.dimv(0,HP,-48,f'પીઠ {fi(HP)}'); v.dimv(HP,Y0,-48,f'મંડોવર {fi(HM)}')
W4a=Win(V4,-62,-6,40,Y0+8,14,22,95,236); W4b=Win(V3,-76,-6,2,Y0+8,108,22,135,236)
tb='<text x="262" y="25" class="b">થર ની યાદી — ઉપર થી નીચે</text>'; ty=28; rh=9.2
cols=[('નં',0),('થર નું નામ',9),('ભાગ',60),('ઊંચાઈ',80),('નીકાળો',104)]
tb+=f'<rect x="262" y="{ty}" width="140" height="{rh}" fill="#eee" stroke="#333" stroke-width=".25"/>'+''.join(f'<text x="{264+c}" y="{ty+6}" class="t" font-weight="700">{t}</text>' for t,c in cols)
yy=ty+rh; num=len(ROWS)
for g,n,b,i,pr,h in ROWS[::-1]:
    if n=='નરથર':
        tb+=f'<rect x="262" y="{yy}" width="140" height="{rh}" fill="#f4f4f4" stroke="#333" stroke-width=".25"/><text x="273" y="{yy+6}" class="t" font-weight="700">મંડોવર કુલ</text><text x="324" y="{yy+6}" class="t" font-weight="700">144</text><text x="344" y="{yy+6}" class="t" font-weight="700">{HM}″ · {fi(HM)}</text>'; yy+=rh
    tb+=f'<rect x="262" y="{yy}" width="140" height="{rh}" fill="#fff" stroke="#333" stroke-width=".25"/><text x="264" y="{yy+6}" class="t">{num}</text><text x="273" y="{yy+6}" class="t">{n}</text><text x="324" y="{yy+6}" class="t">{b or "—"}</text><text x="344" y="{yy+6}" class="t" font-weight="700">{i}″</text><text x="368" y="{yy+6}" class="t">{math.ceil(max(o for _,o in pr))}″</text>'
    yy+=rh; num-=1
tb+=f'<rect x="262" y="{yy}" width="140" height="{rh}" fill="#f4f4f4" stroke="#333" stroke-width=".25"/><text x="273" y="{yy+6}" class="t" font-weight="700">પીઠ + ભીત કુલ</text><text x="344" y="{yy+6}" class="t" font-weight="700">{HP}″ · {fi(HP)}</text>'
tb+=f'<text x="262" y="{yy+rh+5}" class="s">મંડોવર : 1 ભાગ = 0.69″, દરેક થર આખા ઇંચ માં ઉપર ગોળ.</text>'
s4=W4a.svg('c4a')+W4a.ann()+W4b.svg('c4b')+'<text x="20" y="20" class="h">છેદ (સેક્શન)</text><text x="112" y="20" class="h">કર્ણ + પઢરો + અર્ધ ભદ્ર</text>'+tb

# ---------- sheet 5: notes ----------
R=[("જગતી · મંડપ ની પીઠ","વિખેરાઈ ગઈ છે","પથ્થર ને નંબર આપી ફરી ગોઠવવા; ખૂટતા નવા ઘડવા"),("મંડોવર","ઊભો છે; ડાબા પ્રાસાદ માં પથ્થર ખસ્યા છે","ખસેલા સીધા કરવા; તૂટેલા થર શીટ 4 ના માપે નવા"),
 ("છજ્જું","ઘણી જગ્યા એ તૂટેલું","9″ ઊંચું, 13″ નીકળતું નવું"),("શિખર · શૃંગ","કેટલાક શૃંગ પડી ગયા, ઝાડ ઊગ્યા","ઝાડ-મૂળ કાઢવા; 25 અંડક પૂરા કરવા"),
 ("શુકનાસ + સિંહ","બંને માં બાકોરું","નવો શુકનાસ, ઉપર સિંહ (તમારો બ્લોક)"),("આમલસારો · કલશ · ધ્વજ","નથી / અડધો","નવા — શીટ 3 મુજબ"),("ચોકી · મંડપ","સ્તંભ-પાટ ઊભા, છત નથી","સ્તંભ, વેદિકા, તોરણ, સામરણ પૂરા કરવા")]
MU=[("કર્ણ (જંઘા)","અષ્ટ દિક્પાળ — દિશા મુજબ (દક્ષિણ બાજુ : યમ, અગ્નિ)","પેજ 23"),("પઢરો (જંઘા)","અપ્સરા","પેજ 4"),("ભદ્ર ગવાક્ષ","વિષ્ણુ","પેજ 4"),("ગજથર","હાથી ની જોડ","પેજ 21"),("શુકનાસ","સિંહ","પેજ 21"),("પગથિયાં","સવાર સાથે હાથી","ત્રિકૂટ ડ્રોઇંગ")]
h5='<div class="txt"><div class="cols"><div><h2>કયો ભાગ કેવો છે અને શું કરવું</h2><table><tr><th>ભાગ</th><th>હાલ</th><th>શું કરવું</th></tr>'+''.join(f'<tr><td><b>{a}</b></td><td>{b}</td><td>{c}</td></tr>' for a,b,c in R)+'</table>'
h5+='<h2>મૂર્તિ ક્યાં (તમારી DXF માંથી)</h2><table><tr><th>જગ્યા</th><th>મૂર્તિ</th><th>ફાઇલ</th></tr>'+''.join(f'<tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>' for a,b,c in MU)+'</table></div>'
h5+='<div><h2>કામ નો ક્રમ</h2><ol><li><b>પરવાનગી</b> — પુરાતત્વ ખાતા / ટ્રસ્ટ ની લેખિત મંજૂરી</li><li><b>માપણી</b> — સાચા માપ લઈ આ ડ્રોઇંગ સુધારવી</li><li><b>નોંધણી</b> — દરેક પથ્થર નો ફોટો અને નંબર</li><li><b>સફાઈ</b> — ઝાડ, મૂળ, માટી કાઢવા</li><li><b>પીઠ</b> સમતલ, પછી <b>મંડોવર</b> નીચે થી ઉપર</li><li><b>શિખર</b> — શૃંગ, શુકનાસ, આમલસારો, કલશ</li><li><b>મંડપ</b> — સ્તંભ, વેદિકા, સામરણ</li><li><b>પ્રતિષ્ઠા</b> — કલશ અને ધજા</li></ol>'
h5+=f'<h2>અંદાજી માપ</h2><table><tr><th>ભાગ</th><th>માપ</th></tr><tr><td>પ્રાસાદ</td><td><b>{fi(P)}</b></td></tr><tr><td>ગર્ભગૃહ / દીવાલ</td><td><b>{fi(GARBH)} / {fi(WALL)}</b> ⚠</td></tr><tr><td>પીઠ + ભીત</td><td><b>{fi(HP)}</b></td></tr><tr><td>મંડોવર</td><td><b>{fi(HM)}</b></td></tr><tr><td>શિખર</td><td><b>{fi(HS)}</b></td></tr><tr><td>કુલ ઊંચાઈ</td><td><b>{fi(TOTAL)}</b></td></tr><tr><td>મંડપ</td><td><b>{fi(MAND)}</b> ⚠</td></tr></table><p style="font-size:9.5pt">⚠ ફોટા પરથી અંદાજ (± 10%). AutoCAD ફાઇલ : Mandir-CAD.dxf (લેયર : A-WALL, DETAIL, MURTI, HATCH, DIM, TEXT, NEW, CHECK).</p></div></div></div>'
pages=[(s1,'પ્લાન (તલ દર્શન)','1 : 60 આશરે'),(s2,'સામે નું એલિવેશન — આખું મંદિર','1 : 60 આશરે'),(s3,'બાજુ નું એલિવેશન — એક પ્રાસાદ','1 : 60 આશરે'),(s4,'પીઠ + મંડોવર ની વિગત','1 : 25 આશરે')]
heads=['પ્લાન — બે પ્રાસાદ, ચોકી અને મંડપ','સામે નું એલિવેશન (દક્ષિણ થી)','બાજુ નું એલિવેશન — થર, શૃંગ અને મૂર્તિ ના નામ','']
html='<!doctype html><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?family=Noto+Sans+Gujarati:wght@400;700&display=swap" rel="stylesheet"><style>'+CSS+'</style>'
for n,((body,title,scale),hd) in enumerate(zip(pages,heads),1):
    html+=f'<div class="pg"><svg viewBox="0 0 420 297">{frame(title,n,scale)}<text x="16" y="19" class="h">{hd}</text>{body}</svg></div>'
html+=f'<div class="pg"><svg viewBox="0 0 420 297">{frame("પૂરું કરવાની રીત",5,"")}<text x="16" y="19" class="h">મંદિર પૂરું કરવાની રીત</text></svg>{h5}</div>'
open('mandir-cad.html','w').write(html)
doc.saveas('Mandir-CAD.dxf'); print('saved')
