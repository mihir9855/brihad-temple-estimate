# Twin temple (Mandar prasad, 25 andak) - plan, elevation, mandovar detail, completion notes.
# Sizes are estimates from photos (man taken as 6 ft); proportions follow Shilp Ratnakar.
import math
P=108; KAR=18; PAD=18; BH=36; GARBH=54; WALL=27; DOORW=28; DOORH=60; MAND=120; CHOK=30
def fi(i):
    i=int(math.ceil(i-1e-9)); return f"{i//12}′-{i%12}″"
def rnd(n=14,a=3.5): return [(k/n, 1.5+a*math.sin(math.pi*k/n)-1.5*0) for k in range(n+1)]
def bulge(lo,hi,n=12): return [(k/n, lo+(hi-lo)*math.sin(math.pi*k/n)) for k in range(n+1)]
# name, bhaag, inch, profile [(t, offset)]
PEETH=[("ભીત",None,9,[(0,18),(1,18)]),
 ("જાડ્યકુંભ (જાડંબો)",9,7,[(0,17),(.25,17),(.45,15.5),(.7,12),(1,10.5)]),
 ("કર્ણિકા (કણી)",7,6,[(0,9.5),(.5,11.5),(1,9.5)]),
 ("ગ્રાસપટ્ટી",7,6,[(0,8.5),(1,8.5)]),
 ("ગજથર",12,9,[(0,7.5),(1,7.5)]),
 ("નરથર",8,6,[(0,6.5),(1,6.5)])]
MANDO=[("ખુરો",5,4,[(0,5.5),(.6,5.5),(1,4.5)]),
 ("કુંભો",20,14,[(0,4.5),(.72,4.5),(.86,3.6),(1,2)]),
 ("કલશ",8,6,bulge(1.5,4)),
 ("અંતરાલ",2.5,2,[(0,.6),(1,.6)]),
 ("કેવાળ (કપોતિકા)",8,6,[(0,1.2),(.35,3.6),(.6,3.6),(1,1.5)]),
 ("મંચી",9,7,[(0,1),(.45,3),(1,3.6)]),
 ("જંઘા",35,25,[(0,.6),(1,.6)]),
 ("ઉદ્ગમ (દોઢિયો)",15,11,[(0,2.2),(.15,2.2),(1,.6)]),
 ("ભરણી",8,6,bulge(1.2,3.6)),
 ("શિરાવટી",10,7,[(0,2),(.3,2),(1,3.2)]),
 ("કપોતાલી (પુષ્પકંઠ)",8,6,[(0,2),(.5,4.2),(1,3)]),
 ("અંતરાલ",2.5,2,[(0,1),(1,1)]),
 ("છજ્જું (છાદ્ય)",13,9,[(0,3),(.22,12.5),(.4,12.5),(1,2.5)])]
HP=sum(t[2] for t in PEETH); HM=sum(t[2] for t in MANDO); HS=135; HA=24; HK=21
TOTAL=HP+HM+HS+HA+HK
CSS="""@page{size:420mm 297mm;margin:0}*{box-sizing:border-box}body{margin:0;font-family:'Noto Sans Gujarati','FreeSans',sans-serif;color:#111}
.pg{width:420mm;height:297mm;position:relative;page-break-after:always;overflow:hidden}svg{position:absolute;inset:0;width:420mm;height:297mm}
text{font-family:'Noto Sans Gujarati','FreeSans',sans-serif;fill:#111}.t{font-size:2.7px}.s{font-size:2.2px}.b{font-size:3.4px;font-weight:700}.h{font-size:5.2px;font-weight:700}
.dim{font-size:2.6px;fill:#0a3d91}.red{fill:#b3261e}.k{stroke:#111;fill:none;stroke-width:.25}.kk{stroke:#111;fill:none;stroke-width:.45}.f{stroke:#111;fill:#fff;stroke-width:.25}
.th{stroke:#111;fill:none;stroke-width:.12}.dl{stroke:#0a3d91;fill:none;stroke-width:.13}.new{stroke:#b3261e;fill:#fff;stroke-width:.3}.dash{stroke:#555;fill:none;stroke-width:.2;stroke-dasharray:1.5 1}
.txt{position:absolute;left:18mm;top:30mm;right:18mm;font-size:11.5pt;line-height:1.5}.txt h2{font-size:14pt;margin:5mm 0 2mm;border-bottom:.3mm solid #111}
table{border-collapse:collapse;width:100%}td,th{border:.25mm solid #333;padding:1.2mm 2mm;text-align:left;vertical-align:top;font-size:10.5pt}th{background:#eee}.cols{display:grid;grid-template-columns:1.25fr 1fr;gap:8mm}"""
def frame(title,sheet,scale):
    return f'''<rect x="8" y="8" width="404" height="281" class="kk"/><rect x="10" y="10" width="400" height="277" class="th"/>
<rect x="290" y="259" width="120" height="28" class="f"/><line x1="290" y1="269" x2="410" y2="269" class="th"/><line x1="290" y1="278" x2="410" y2="278" class="th"/><line x1="370" y1="269" x2="370" y2="287" class="th"/>
<text x="293" y="266" class="b">જોડિયા મંદિર · મંદર પ્રાસાદ (25 અંડક)</text><text x="293" y="275" class="t">{title}</text><text x="373" y="275" class="t">શીટ {sheet} / 4</text>
<text x="293" y="284" class="s">⚠ અંદાજી માપ — ફોટા પરથી (માણસ = 6′-0″). ભાગ શિલ્પ રત્નાકર મુજબ.</text><text x="373" y="284" class="s">{scale}</text>
<defs><pattern id="hat" width="1.6" height="1.6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="1.6" stroke="#444" stroke-width=".14"/></pattern>
<marker id="ar" viewBox="0 0 6 6" refX="5.6" refY="3" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M0,.8 L6,3 L0,5.2z" fill="#0a3d91"/></marker></defs>'''
def dimh(x1,x2,y,txt,up=True,cls="dim"):
    ty=y-1 if up else y+3
    return f'<line x1="{x1:.2f}" y1="{y:.2f}" x2="{x2:.2f}" y2="{y:.2f}" class="dl" marker-start="url(#ar)" marker-end="url(#ar)"/><line x1="{x1:.2f}" y1="{y-1.5:.2f}" x2="{x1:.2f}" y2="{y+1.5:.2f}" class="dl"/><line x1="{x2:.2f}" y1="{y-1.5:.2f}" x2="{x2:.2f}" y2="{y+1.5:.2f}" class="dl"/><text x="{(x1+x2)/2:.2f}" y="{ty:.2f}" text-anchor="middle" class="{cls}">{txt}</text>'
def dimv(y1,y2,x,txt,cls="dim"):
    m=(y1+y2)/2
    return f'<line x1="{x:.2f}" y1="{y1:.2f}" x2="{x:.2f}" y2="{y2:.2f}" class="dl" marker-start="url(#ar)" marker-end="url(#ar)"/><line x1="{x-1.5:.2f}" y1="{y1:.2f}" x2="{x+1.5:.2f}" y2="{y1:.2f}" class="dl"/><line x1="{x-1.5:.2f}" y1="{y2:.2f}" x2="{x+1.5:.2f}" y2="{y2:.2f}" class="dl"/><text x="{x+1.5:.2f}" y="{m+1:.2f}" class="{cls}">{txt}</text>'

# ---------------- Sheet 1: plan ----------------
def prasad_outline():
    h=P/2; pts=[]
    half=[(-h,0),(-h+KAR,0),(-h+KAR,4),(-h+KAR+PAD,4),(-h+KAR+PAD,9),(h-KAR-PAD,9),(h-KAR-PAD,4),(h-KAR,4),(h-KAR,0),(h,0)]
    for r in range(4):   # sides: top(-y), right, bottom, left
        for (a,o) in half:
            x,y=a,-h-o
            for _ in range(r): x,y=-y,x
            pts.append((x,y))
    return pts
def prasad_plan(s,cx,cy,rot,label,dash=False):
    o=prasad_outline(); pts=" ".join(f"{x*s:.2f},{y*s:.2f}" for x,y in o); g=GARBH/2*s
    if dash: return f'<g transform="translate({cx},{cy}) rotate({rot})"><polygon points="{pts}" class="dash"/><rect x="{-g}" y="{-g}" width="{2*g}" height="{2*g}" class="dash"/></g><text x="{cx}" y="{cy}" text-anchor="middle" class="s">ત્રીજો પ્રાસાદ ? ⚠</text><text x="{cx}" y="{cy+3.5}" text-anchor="middle" class="s">(સાઇટ પર તપાસો)</text>'
    h=P/2*s; dw=DOORW/2*s
    out=f'<g transform="translate({cx},{cy}) rotate({rot})"><polygon points="{pts}" class="kk" style="fill:url(#hat)"/><rect x="{-g}" y="{-g}" width="{2*g}" height="{2*g}" class="f"/>'
    out+=f'<rect x="{-dw}" y="{g-.3}" width="{2*dw}" height="{h+9*s-g+.8}" fill="#fff" stroke="none"/><line x1="{-dw}" y1="{g}" x2="{-dw}" y2="{h+9*s}" class="kk"/><line x1="{dw}" y1="{g}" x2="{dw}" y2="{h+9*s}" class="kk"/>'
    out+=f'<line x1="{-dw}" y1="{h+4*s}" x2="{dw}" y2="{h+4*s}" class="th"/><line x1="{-dw}" y1="{h+7*s}" x2="{dw}" y2="{h+7*s}" class="th"/>'
    for r in (0,90,270):   # gavaksh niches on three bhadra
        out+=f'<rect transform="rotate({r})" x="{-7*s}" y="{-h-9*s-.1}" width="{14*s}" height="{6*s}" class="f"/>'
    for sx in (-1,1):      # chokki stambh
        out+=f'<rect x="{sx*24*s-5*s}" y="{h+9*s+CHOK*s-10*s}" width="{10*s}" height="{10*s}" class="f" style="stroke-width:.4"/><rect x="{sx*24*s-3*s}" y="{h+9*s+CHOK*s-8*s}" width="{6*s}" height="{6*s}" class="th"/>'
    out+=f'<circle r="{5*s}" class="th"/><circle r="{2.2*s}" class="th"/></g>'
    out+=f'<text x="{cx}" y="{cy-g+4}" text-anchor="middle" class="t">{label}</text>'
    return out
def sheet_plan():
    s=.58; cx,cy=168,163; d=(MAND/2+CHOK+9+P/2)*s; m=MAND/2*s; h=P/2*s
    o=frame("પ્લાન (તલ દર્શન)","1","માપ : ફૂટ-ઇંચ")
    o+='<text x="16" y="20" class="h">પ્લાન — બે પ્રાસાદ, ચોકી અને સહિયારો મંડપ</text>'
    o+=prasad_plan(s,cx,cy-d,0,"ગર્ભગૃહ 1")+prasad_plan(s,cx-d,cy,270,"ગર્ભગૃહ 2")+prasad_plan(s,cx+d,cy,90,"",True)
    o+=f'<rect x="{cx-m}" y="{cy-m}" width="{2*m}" height="{2*m}" class="k"/><rect x="{cx-m-4*s}" y="{cy-m-4*s}" width="{2*m+8*s}" height="{2*m+8*s}" class="th"/>'
    for sx in (-1,1):
        for sy in (-1,1):
            o+=f'<rect x="{cx+sx*(m-6*s)-6*s}" y="{cy+sy*(m-6*s)-6*s}" width="{12*s}" height="{12*s}" class="f" style="stroke-width:.4"/>'
    # vedika (kakshasan) on the open front, entrance gap in the middle
    for sx in (-1,1):
        x1=cx+sx*(m-12*s); x2=cx+sx*24*s
        o+=f'<rect x="{min(x1,x2)}" y="{cy+m-7*s}" width="{abs(x2-x1)}" height="{7*s}" class="k" style="fill:url(#hat)"/>'
    o+=f'<rect x="{cx-m+12*s if False else cx+m-7*s}" y="{cy-m+12*s}" width="{7*s}" height="{2*m-24*s}" class="k" style="fill:url(#hat)"/>'
    for i in range(3): o+=f'<rect x="{cx-24*s-i*4*s}" y="{cy+m+i*10*s}" width="{48*s+i*8*s}" height="{10*s}" class="k"/>'
    o+=f'<text x="{cx}" y="{cy+1}" text-anchor="middle" class="b">મંડપ</text><text x="{cx}" y="{cy+5}" text-anchor="middle" class="s">(છત પડી ગઈ છે)</text>'
    o+=f'<text x="{cx}" y="{cy+m+36*s}" text-anchor="middle" class="t">પગથિયાં · પ્રવેશ</text>'
    o+=f'<text x="{cx-m-CHOK*s/2}" y="{cy-9}" text-anchor="middle" class="s" transform="rotate(-90 {cx-m-CHOK*s/2} {cy-9})">ચોકી</text>'
    o+=f'<text x="{cx+m+2}" y="{cy+m-12*s}" class="s">વેદિકા (કક્ષાસન)</text>'
    # dimensions on prasad 1
    ty=cy-d-h-9*s-9; x0=cx-h
    o+=dimh(x0,cx+h,ty-7,f"પ્રાસાદ (રેખા થી રેખા) {fi(P)}")
    xs=[0,KAR,KAR+PAD,KAR+PAD+BH,KAR+2*PAD+BH,P]; nm=["કર્ણ","પઢરો","ભદ્ર","પઢરો","કર્ણ"]
    for i in range(5): o+=dimh(x0+xs[i]*s,x0+xs[i+1]*s,ty,f"{nm[i]} {xs[i+1]-xs[i]}″",cls="dim s")
    xr=cx+h+9*s+6
    o+=dimv(cy-d-GARBH/2*s,cy-d+GARBH/2*s,xr,f"ગર્ભગૃહ {fi(GARBH)}")+dimv(cy-d+GARBH/2*s,cy-d+h,xr,f"દીવાલ {fi(WALL)}")+dimv(cy-d+h+9*s,cy-m,xr,f"ચોકી {fi(CHOK)}")
    o+=dimv(cy-m,cy+m,cx+d+h+9*s+10,f"મંડપ {fi(MAND)}")
    o+=dimh(cx-DOORW/2*s,cx+DOORW/2*s,cy-d+h+9*s+4,f"દ્વાર {fi(DOORW)}",up=False,cls="dim s")
    tot=2*(MAND/2+CHOK+9+P+9)
    o+=dimh(cx-d-h-9*s,cx+d+h+9*s,cy+m+30,f"કુલ પહોળાઈ (ત્રણ પ્રાસાદ હોય તો) {fi(tot)}",up=False)
    # legend
    lx=16; ly=34
    L=["નોંધ","• પ્રાસાદ : મંદર — તલ 12 ભાગ, 1 ભાગ = 9″","  કર્ણ 2 · પઢરો 2 · અર્ધ ભદ્ર 2 ભાગ","• ભદ્ર નો નીકાળો 9″, પઢરા નો 4″",f"• ગર્ભગૃહ {fi(GARBH)} ⚠, દીવાલ {fi(WALL)} ⚠ (અંદર માપવું)","• ત્રણ ભદ્રે ગવાક્ષ (ગોખલો)","• દ્વાર આગળ બે સ્તંભ ની ચોકી","• ગર્ભગૃહ 2 નું દ્વાર મંડપ તરફ (ફોટા પરથી) ⚠","• તૂટક લીટી = ત્રીજો પ્રાસાદ હોઈ શકે ⚠","▨ પથ્થર ની દીવાલ"]
    for i,t in enumerate(L): o+=f'<text x="{lx}" y="{ly+i*5.2}" class="{"b" if i==0 else "t"}">{t}</text>'
    return o

# ---------------- elevation helpers ----------------
def stack():
    rows=[];h=0
    for grp,lst in (("p",PEETH),("m",MANDO)):
        for n,b,i,pr in lst: rows.append((grp,n,b,i,pr,h)); h+=i
    return rows
def rekha(hh,w0,H,top=.6): return w0*(1-(1-top)*(hh/H)**1.9)
def shrung(X,Y,s,xc,hb,w,H,cap=True,tiers=5.5,fill="#fff"):
    w0=w/2; n=18; L=[];R=[]
    for k in range(n+1):
        hh=H*k/n; ww=rekha(hh,w0,H); L.append((xc-ww,hb+hh)); R.append((xc+ww,hb+hh))
    pts=L+R[::-1]; o=f'<polygon points="{" ".join(f"{X(a):.2f},{Y(b):.2f}" for a,b in pts)}" class="f" style="fill:{fill}"/>'
    for fr in (-1/3,1/3):
        o+='<polyline class="th" points="'+" ".join(f"{X(xc+fr*2*rekha(H*k/n,w0,H)):.2f},{Y(hb+H*k/n):.2f}" for k in range(n+1))+'"/>'
    k=tiers
    while k<H-1:
        ww=rekha(k,w0,H); o+=f'<line x1="{X(xc-ww):.2f}" y1="{Y(hb+k):.2f}" x2="{X(xc+ww):.2f}" y2="{Y(hb+k):.2f}" class="th"/>'; k+=tiers
    if cap:
        t=rekha(H,w0,H); g=t*.6; a=t*.95; hh=hb+H
        o+=f'<rect x="{X(xc-g):.2f}" y="{Y(hh+w*.05):.2f}" width="{2*g*s:.2f}" height="{w*.05*s:.2f}" class="f"/>'
        o+=f'<ellipse cx="{X(xc):.2f}" cy="{Y(hh+w*.1):.2f}" rx="{a*s:.2f}" ry="{w*.055*s:.2f}" class="f"/>'
        o+=f'<path d="M{X(xc-g*.5):.2f},{Y(hh+w*.15):.2f} Q{X(xc):.2f},{Y(hh+w*.36):.2f} {X(xc+g*.5):.2f},{Y(hh+w*.15):.2f}z" class="f"/>'
    return o
def elevation(X,Y,s,orn=True):
    rows=stack(); o=""; L=[];R=[]
    for grp,n,b,i,pr,h in rows:
        for t,off in pr: L.append((-(P/2+off),h+t*i)); R.append((P/2+off,h+t*i))
    o+=f'<polygon points="{" ".join(f"{X(a):.2f},{Y(b):.2f}" for a,b in L+R[::-1])}" class="f" style="stroke-width:.4"/>'
    for grp,n,b,i,pr,h in rows:
        prev=None
        for t,off in pr:
            if len(pr)>6 and prev is not None and 0<t<1: prev=off; continue
            o+=f'<line x1="{X(-(P/2+off)):.2f}" y1="{Y(h+t*i):.2f}" x2="{X(P/2+off):.2f}" y2="{Y(h+t*i):.2f}" class="th"/>'; prev=off
    angas=[(-54,-36),(-36,-18),(-18,18),(18,36),(36,54)]
    for x in (-36,-18,18,36): o+=f'<line x1="{X(x):.2f}" y1="{Y(0):.2f}" x2="{X(x):.2f}" y2="{Y(HP+HM-9):.2f}" class="k"/>'
    if orn:
        for grp,n,b,i,pr,h in rows:
            for (a,c) in angas:
                w=c-a
                if n=="કુંભો": o+=f'<rect x="{X(a+3):.2f}" y="{Y(h+i*.68):.2f}" width="{(w-6)*s:.2f}" height="{i*.56*s:.2f}" class="th"/><path d="M{X(a+w/2-2.5):.2f},{Y(h+i*.16):.2f} v{-5*s:.2f} a{2.5*s:.2f},{2.5*s:.2f} 0 0 1 {5*s:.2f},0 v{5*s:.2f}" class="th"/>'
                if n=="જંઘા":
                    if w>20:
                        o+=f'<rect x="{X(a+5):.2f}" y="{Y(h+i-2):.2f}" width="{(w-10)*s:.2f}" height="{(i-3)*s:.2f}" class="k"/><rect x="{X(a+11):.2f}" y="{Y(h+i-6):.2f}" width="{(w-22)*s:.2f}" height="{(i-8)*s:.2f}" fill="#333" class="k"/>'
                        for q in (7,w-9): o+=f'<rect x="{X(a+q):.2f}" y="{Y(h+i-4):.2f}" width="{2*s:.2f}" height="{(i-5)*s:.2f}" class="th"/>'
                    else:
                        o+=f'<rect x="{X(a+2.5):.2f}" y="{Y(h+i-2):.2f}" width="{(w-5)*s:.2f}" height="{(i-3.5)*s:.2f}" class="th"/>'
                        xm=a+w/2; o+=f'<circle cx="{X(xm):.2f}" cy="{Y(h+i-6):.2f}" r="{1.7*s:.2f}" class="th"/><path d="M{X(xm-2.6):.2f},{Y(h+i-8.5):.2f} L{X(xm+2.6):.2f},{Y(h+i-8.5):.2f} L{X(xm+1.6):.2f},{Y(h+i-15):.2f} L{X(xm+2.4):.2f},{Y(h+3):.2f} L{X(xm-2.4):.2f},{Y(h+3):.2f} L{X(xm-1.6):.2f},{Y(h+i-15):.2f}z" class="th"/>'
                if n.startswith("ઉદ્ગમ"):
                    xm=a+w/2
                    for k,(fw,fh) in enumerate(((.46,.34),(.3,.67),(.14,1))): o+=f'<path d="M{X(xm-w*fw):.2f},{Y(h+i*(fh-.33)):.2f} L{X(xm-w*fw):.2f},{Y(h+i*fh-1):.2f} L{X(xm+w*fw):.2f},{Y(h+i*fh-1):.2f} L{X(xm+w*fw):.2f},{Y(h+i*(fh-.33)):.2f}" class="th"/>'
                if n in("ગજથર","નરથર"):
                    q=a+2
                    while q<c-1: o+=f'<rect x="{X(q):.2f}" y="{Y(h+i-1.2):.2f}" width="{2.6*s:.2f}" height="{(i-2.4)*s:.2f}" class="th"/>'; q+=4
                if n=="ગ્રાસપટ્ટી":
                    q=a+3
                    while q<c-1: o+=f'<circle cx="{X(q):.2f}" cy="{Y(h+i/2):.2f}" r="{1.6*s:.2f}" class="th"/>'; q+=5
    # shikhar
    y0=HP+HM
    o+=shrung(X,Y,s,0,y0,P-4,HS,cap=False,tiers=7.5)
    o+=shrung(X,Y,s,0,y0+38,32,64)                    # urushrung 2
    for sx in (-1,1):
        o+=shrung(X,Y,s,sx*39,y0+31,15,27)             # karna shrung 2
        o+=f'<rect x="{X(sx*25.5-6):.2f}" y="{Y(y0+48):.2f}" width="{12*s:.2f}" height="{13*s:.2f}" class="f"/><path d="M{X(sx*25.5-7):.2f},{Y(y0+48):.2f} L{X(sx*25.5):.2f},{Y(y0+56):.2f} L{X(sx*25.5+7):.2f},{Y(y0+48):.2f}z" class="f"/>'  # tilak
        o+=shrung(X,Y,s,sx*27,y0,18,30)                # padhra shrung
        o+=shrung(X,Y,s,sx*45,y0,18,30)                # karna shrung 1
    o+=shrung(X,Y,s,0,y0,36,58)                        # urushrung 1
    o+=f'<rect x="{X(-7):.2f}" y="{Y(y0+17):.2f}" width="{14*s:.2f}" height="{15*s:.2f}" class="k"/><rect x="{X(-4):.2f}" y="{Y(y0+14):.2f}" width="{8*s:.2f}" height="{11*s:.2f}" class="th"/>'
    return o
def top_parts(X,Y,s):
    y=HP+HM+HS; t=rekha(HS,(P-4)/2,HS); o=""
    o+=f'<rect x="{X(-20):.2f}" y="{Y(y+5):.2f}" width="{40*s:.2f}" height="{5*s:.2f}" class="new"/>'
    o+=f'<path d="M{X(-22):.2f},{Y(y+5):.2f} Q{X(-31):.2f},{Y(y+8.5):.2f} {X(-22):.2f},{Y(y+12):.2f} L{X(22):.2f},{Y(y+12):.2f} Q{X(31):.2f},{Y(y+8.5):.2f} {X(22):.2f},{Y(y+5):.2f}z" class="new"/>'
    for k in range(-5,6): o+=f'<line x1="{X(k*4.2):.2f}" y1="{Y(y+5.3):.2f}" x2="{X(k*4.2):.2f}" y2="{Y(y+11.7):.2f}" stroke="#b3261e" stroke-width=".12"/>'
    o+=f'<path d="M{X(-19):.2f},{Y(y+12):.2f} L{X(-15):.2f},{Y(y+18):.2f} L{X(15):.2f},{Y(y+18):.2f} L{X(19):.2f},{Y(y+12):.2f}z" class="new"/>'
    o+=f'<path d="M{X(-12):.2f},{Y(y+18):.2f} Q{X(-15):.2f},{Y(y+21):.2f} {X(-9):.2f},{Y(y+24):.2f} L{X(9):.2f},{Y(y+24):.2f} Q{X(15):.2f},{Y(y+21):.2f} {X(12):.2f},{Y(y+18):.2f}z" class="new"/>'
    k=y+HA
    o+=f'<path d="M{X(-4.5):.2f},{Y(k):.2f} L{X(-3):.2f},{Y(k+2.3):.2f} C{X(-10):.2f},{Y(k+4):.2f} {X(-9):.2f},{Y(k+10):.2f} {X(-3.5):.2f},{Y(k+10.5):.2f} L{X(-5):.2f},{Y(k+11.8):.2f} L{X(-2.5):.2f},{Y(k+13.5):.2f} L{X(-1.6):.2f},{Y(k+15):.2f} L{X(0):.2f},{Y(k+21):.2f} L{X(1.6):.2f},{Y(k+15):.2f} L{X(2.5):.2f},{Y(k+13.5):.2f} L{X(5):.2f},{Y(k+11.8):.2f} L{X(3.5):.2f},{Y(k+10.5):.2f} C{X(9):.2f},{Y(k+10):.2f} {X(10):.2f},{Y(k+4):.2f} {X(3):.2f},{Y(k+2.3):.2f} L{X(4.5):.2f},{Y(k):.2f}z" class="new"/>'
    px=24
    o+=f'<rect x="{X(px):.2f}" y="{Y(k+34):.2f}" width="{2.2*s:.2f}" height="{(34+HA+8)*s:.2f}" class="new"/><path d="M{X(px+2.2):.2f},{Y(k+33):.2f} L{X(px+34):.2f},{Y(k+26):.2f} L{X(px+2.2):.2f},{Y(k+17):.2f}z" class="new"/>'
    return o

def sheet_elev():
    s=.685; cx=178; gy=262; X=lambda x:cx+x*s; Y=lambda h:gy-h*s
    o=frame("એલિવેશન (ઊભું દર્શન) — પૂરું મંદિર","2","માપ : ઇંચ / ફૂટ-ઇંચ")
    o+='<text x="16" y="20" class="h">એલિવેશન — બાજુ નું દર્શન (ભદ્ર ના ગવાક્ષ સાથે)</text>'
    o+=f'<line x1="{X(-110)}" y1="{gy}" x2="{X(110)}" y2="{gy}" class="kk"/>'
    for k in range(-108,110,5): o+=f'<line x1="{X(k)}" y1="{gy}" x2="{X(k-3)}" y2="{gy+2}" class="th"/>'
    o+=elevation(X,Y,s)+top_parts(X,Y,s)
    # left labels
    rows=stack(); lx=58; ys=[]
    for grp,n,b,i,pr,h in rows: ys.append(Y(h+i/2))
    lab=ys[:]; 
    for k in range(1,len(lab)):
        if lab[k]>lab[k-1]-4.3: lab[k]=lab[k-1]-4.3
    shift=(sum(ys)-sum(lab))/len(ys)*.6
    lab=[v+shift for v in lab]
    for (grp,n,b,i,pr,h),yy,ly in zip(rows,ys,lab):
        off=max(q for _,q in pr)
        o+=f'<polyline points="{lx+38},{ly-1} {lx+48},{ly-1} {X(-(P/2+off))-1:.2f},{yy:.2f}" class="dl"/><circle cx="{X(-(P/2+off))-1:.2f}" cy="{yy:.2f}" r=".35" fill="#0a3d91"/>'
        o+=f'<text x="{lx+37}" y="{ly}" text-anchor="end" class="t">{n}{" · "+str(b)+" ભાગ" if b else ""} — <tspan font-weight="700">{i}″</tspan></text>'
    o+=f'<text x="{lx+37}" y="{lab[-1]-7}" text-anchor="end" class="b">મંડોવર 144 ભાગ ↓</text><text x="{lx+37}" y="{lab[5]+ -0}" class="s"></text>'
    # shikhar labels
    y0=HP+HM
    SL=[("ઉરુશૃંગ 1 (ભદ્રે)",0,y0+50),("ઉરુશૃંગ 2",-6,y0+92),("કર્ણ શૃંગ 2",-39,y0+50),("કર્ણ શૃંગ 1",-47,y0+20),("પઢરા નું શૃંગ",-27,y0+33),("તિલક",-25.5,y0+54),("મૂળ શિખર (રેખા)",-22,y0+118),("રથિકા (ગવાક્ષ)",0,y0+22)]
    yy=Y(y0+128)
    for k,(t,x,h) in enumerate(sorted(SL,key=lambda q:-q[2])):
        ly=yy+k*6.2
        o+=f'<polyline points="{lx+38},{ly-1} {lx+46},{ly-1} {X(x):.2f},{Y(h):.2f}" class="dl"/><circle cx="{X(x):.2f}" cy="{Y(h):.2f}" r=".35" fill="#0a3d91"/><text x="{lx+37}" y="{ly}" text-anchor="end" class="t">{t}</text>'
    ky=y0+HS
    for t,h in (("ધ્વજદંડ · ધજા (નવું)",ky+HA+26),("કલશ (નવો)",ky+HA+8),("આમલસારી · ચંદ્રિકા (નવી)",ky+18),("આમલસારો (નવો)",ky+9),("ગ્રીવા",ky+2.5)):
        o+=f'<line x1="{X(30)}" y1="{Y(h)}" x2="{X(75)}" y2="{Y(h)}" stroke="#b3261e" stroke-width=".13"/><text x="{X(76)}" y="{Y(h)+1}" class="t red">{t}</text>'
    o+=f'<text x="{X(76)}" y="{Y(y0+HS-10)}" class="t">સ્કંધ (બંધન)</text><line x1="{X(34)}" y1="{Y(y0+HS)}" x2="{X(75)}" y2="{Y(y0+HS-9)}" class="dl"/>'
    # right dimension chains
    dx=X(150)
    segs=[(0,9,"ભીત 9″"),(9,HP,f"પીઠ {HP-9}″ · {fi(HP-9)}"),(HP,HP+HM,f"મંડોવર {HM}″ · {fi(HM)}"),(y0,y0+HS,f"શિખર {HS}″ · {fi(HS)}"),(y0+HS,y0+HS+HA,f"આમલસારો {HA}″"),(y0+HS+HA,TOTAL,f"કલશ {HK}″")]
    for a,b,t in segs: o+=dimv(Y(b),Y(a),dx,t)
    o+=dimv(Y(TOTAL),Y(0),dx+48,f"કુલ ઊંચાઈ {TOTAL}″ · {fi(TOTAL)}")
    o+=dimh(X(-54),X(54),gy+9,f"પ્રાસાદ {fi(P)} ({P}″)",up=False)
    xs=[-54,-36,-18,18,36,54]; nm=["કર્ણ","પઢરો","ભદ્ર","પઢરો","કર્ણ"]
    for i in range(5): o+=dimh(X(xs[i]),X(xs[i+1]),gy+4,f"{nm[i]} {xs[i+1]-xs[i]}″",up=False,cls="dim s")
    L=["નોંધ","• કાળી લીટી = હાલ નું કામ (તૂટેલા ભાગ સમારવા)","• લાલ લીટી = નવું બનાવવાનું","• અંડક : 1 + કર્ણ 8 + પઢરા 8 + ઉરુશૃંગ 8 = 25",f"• શિખર = પ્રાસાદ × 1¼ = {HS}″ (જ્યેષ્ઠ)","• સ્કંધ = પાયા ના 10 માંથી 6 ભાગ","• આમલસારો ઊંચાઈ = ½ પહોળાઈ","• કલશ પહોળાઈ = પ્રાસાદ ÷ 8, ઊંચાઈ 1½ ગણી","• આગળ ની બાજુ ભદ્રે ઉરુશૃંગ ને બદલે શુકનાસ"]
    for i,t in enumerate(L): o+=f'<text x="16" y="{32+i*5.2}" class="{"b" if i==0 else "t"}">{t}</text>'
    return o

def sheet_detail():
    s=1.55; gy=268; wx=120; X=lambda off:wx-off*s; Y=lambda h:gy-h*s
    o=frame("પીઠ અને મંડોવર ની વિગત (144 ભાગ)","3","માપ : ઇંચ")
    o+='<text x="16" y="20" class="h">પીઠ + મંડોવર — છેદ (સેક્શન) અને થર ના નામ</text>'
    rows=stack(); pts=[]
    for grp,n,b,i,pr,h in rows:
        for t,off in pr: pts.append((off,h+t*i))
    poly=[(X(o_),Y(h)) for o_,h in pts]+[(wx+34,Y(HP+HM)),(wx+34,gy)]
    o+=f'<polygon points="{" ".join(f"{a:.2f},{b:.2f}" for a,b in poly)}" class="kk" style="fill:url(#hat)"/>'
    o+=f'<line x1="{wx}" y1="{gy+3}" x2="{wx}" y2="{Y(HP+HM)-6}" class="dash"/><text x="{wx+1}" y="{Y(HP+HM)-7}" class="s">દીવાલ ની રેખા</text><line x1="40" y1="{gy}" x2="{wx+40}" y2="{gy}" class="kk"/>'
    # elevation strip of karna + padhro beside the section
    ex=wx+50; EX=lambda x:ex+ (x+54)*s
    sub=elevation(lambda x:ex+(x+54)*s, Y, s)
    o+=f'<clipPath id="cl"><rect x="{ex-20*s}" y="{Y(HP+HM)-1}" width="{(20+47)*s}" height="{(HP+HM)*s+1.2}"/></clipPath><g clip-path="url(#cl)">{sub}</g>'
    o+=f'<text x="{ex+6}" y="{gy+5}" class="s">કર્ણ</text><text x="{ex+33}" y="{gy+5}" class="s">પઢરો</text><text x="{wx-18}" y="{gy+5}" class="s">છેદ</text>'
    # table
    tx=262; ty=27; rh=9.6
    o+=f'<text x="{tx}" y="{ty-3}" class="b">થર ની યાદી — ઉપર થી નીચે</text>'
    hdr=[("નં",0),("થર નું નામ",9),("ભાગ",62),("ઊંચાઈ ″",80),("નીકાળો ″",104)]
    y=ty+2; o+=f'<rect x="{tx}" y="{y}" width="140" height="{rh}" fill="#eee" class="k"/>'
    for t,dxx in hdr: o+=f'<text x="{tx+dxx+2}" y="{y+6.3}" class="t" font-weight="700">{t}</text>'
    y+=rh; num=len(rows)
    for grp,n,b,i,pr,h in rows[::-1]:
        if n=="નરથર": 
            o+=f'<rect x="{tx}" y="{y}" width="140" height="{rh}" fill="#f4f4f4" class="k"/><text x="{tx+11}" y="{y+6.3}" class="t" font-weight="700">મંડોવર કુલ</text><text x="{tx+64}" y="{y+6.3}" class="t" font-weight="700">144</text><text x="{tx+82}" y="{y+6.3}" class="t" font-weight="700">{HM}″ · {fi(HM)}</text>'; y+=rh
        o+=f'<rect x="{tx}" y="{y}" width="140" height="{rh}" class="k"/><text x="{tx+2}" y="{y+6.3}" class="t">{num}</text><text x="{tx+11}" y="{y+6.3}" class="t">{n}</text><text x="{tx+64}" y="{y+6.3}" class="t">{b if b else "—"}</text><text x="{tx+82}" y="{y+6.3}" class="t" font-weight="700">{i}″</text><text x="{tx+106}" y="{y+6.3}" class="t">{math.ceil(max(q for _,q in pr))}″</text>'
        # leader from table number to band
        o+=f'<text x="{X(max(q for _,q in pr))-3:.2f}" y="{Y(h+i/2)+1:.2f}" text-anchor="end" class="s">{num} · {n.split(" (")[0]} {i}″</text>'
        y+=rh; num-=1
    o+=f'<rect x="{tx}" y="{y}" width="140" height="{rh}" fill="#f4f4f4" class="k"/><text x="{tx+11}" y="{y+6.3}" class="t" font-weight="700">પીઠ + ભીત કુલ</text><text x="{tx+64}" y="{y+6.3}" class="t" font-weight="700">46</text><text x="{tx+82}" y="{y+6.3}" class="t" font-weight="700">{HP}″ · {fi(HP)}</text>'
    for dxx in (9,62,80,104): o+=f'<line x1="{tx+dxx}" y1="{ty+2}" x2="{tx+dxx}" y2="{y+rh}" class="th"/>'
    o+=f'<text x="{tx}" y="{y+rh+6}" class="s">મંડોવર : 1 ભાગ = 99″ ÷ 144 = 0.69″ · દરેક થર આખા ઇંચ માં ઉપર ગોળ કરેલો.</text><text x="{tx}" y="{y+rh+10.5}" class="s">પીઠ : જાડ્યકુંભ 9, કર્ણિકા 7, ગ્રાસપટ્ટી 7, ગજથર 12, નરથર 8 ભાગ (1 ભાગ = ¾″).</text>'
    o+=dimv(Y(HP+HM),Y(HP),40,"")+f'<text x="33" y="{Y(HP+HM/2)}" class="dim" transform="rotate(-90 33 {Y(HP+HM/2)})" text-anchor="middle">મંડોવર {fi(HM)}</text>'
    o+=dimv(Y(HP),Y(0),40,"")+f'<text x="33" y="{Y(HP/2)}" class="dim" transform="rotate(-90 33 {Y(HP/2)})" text-anchor="middle">પીઠ {fi(HP)}</text>'
    return o

def sheet_notes():
    R=[("જગતી · મંડપ ની પીઠ","વિખેરાઈ ગઈ છે, પથ્થર છૂટા પડ્યા છે","પડેલા પથ્થર ને નંબર આપી ફરી ગોઠવવા; ખૂટતા નવા ઘડવા"),
       ("પ્રાસાદ ની પીઠ","મોટે ભાગે સલામત, ઘસારો છે","સાંધા ભરવા; તૂટેલા ખૂણા ના પથ્થર બદલવા"),
       ("મંડોવર (ખુરા થી છજ્જા)","ઊભો છે; ડાબા પ્રાસાદ માં પથ્થર ખસી ગયા છે, મૂર્તિઓ ઘસાઈ છે","ખસેલા પથ્થર સીધા કરવા; તૂટેલા થર શીટ 3 ના માપે નવા ઘડવા"),
       ("છજ્જું","ઘણી જગ્યા એ તૂટેલું","9″ ઊંચું, 13″ નીકળતું નવું છજ્જું ઘડવું"),
       ("શિખર અને શૃંગ","મૂળ શિખર ઊભું છે; કેટલાક શૃંગ પડી ગયા, ઝાડ ઊગ્યા છે","ઝાડ-મૂળ કાઢવા; ખૂટતા શૃંગ ગણી ને 25 અંડક પૂરા કરવા"),
       ("શુકનાસ (આગળ)","બંને શિખર માં બાકોરું — આગળ નો પથ્થર પડી ગયો","શુકનાસ નવો બનાવી બાકોરું બંધ કરવું"),
       ("આમલસારો","એક પર અડધો છે, બીજા પર નથી","બંને પર નવો — ગ્રીવા, આમલસારો, ચંદ્રિકા, આમલસારી (24″)"),
       ("કલશ · ધ્વજદંડ","નથી","નવો કલશ 14″ × 21″; ધ્વજદંડ પાછળ જમણા પઢરે"),
       ("ચોકી અને મંડપ","બે સ્તંભ અને પાટ ઊભા છે; છત નથી; વેદિકા થોડી બચી છે","સ્તંભ, પાટ, વેદિકા પૂરા કરી ઉપર સામરણ / ઘુમ્મટ"),
       ("દ્વાર શાખા","ઊભી છે, ઘસાયેલી","સાફ કરી સાચવવી; ઉંબર નવો")]
    S=["<b>પરવાનગી:</b> આ જૂનું (પુરાતન) મંદિર લાગે છે. કામ શરૂ કરતાં પહેલાં પુરાતત્વ ખાતા / ટ્રસ્ટ ની લેખિત મંજૂરી લેવી.",
       "<b>માપણી:</b> ગર્ભગૃહ, દીવાલ, દરેક થર ની ઊંચાઈ સાઇટ પર માપી આ અંદાજી માપ સુધારવા.",
       "<b>નોંધણી:</b> દરેક પથ્થર નો ફોટો અને નંબર; પડેલા પથ્થર કયા થર ના છે તે ઓળખવા.",
       "<b>સફાઈ:</b> ઝાડ, મૂળ, માટી કાઢવા. મૂળ ખેંચવા નહીં — કાપી ને દવા નાખવી.",
       "<b>પાયો અને પીઠ:</b> બેસી ગયેલો ભાગ તપાસવો, પીઠ સમતલ કરવી.",
       "<b>મંડોવર:</b> નીચે થી ઉપર, થર પ્રમાણે સમારકામ. નવો પથ્થર જૂના જેવો જ (એ જ ખાણ નો) લેવો.",
       "<b>શિખર:</b> શૃંગ, ઉરુશૃંગ, શુકનાસ પૂરા કરવા; પછી સ્કંધ ઉપર આમલસારો અને કલશ.",
       "<b>મંડપ:</b> સ્તંભ, પાટ, વેદિકા, છત.",
       "<b>પ્રતિષ્ઠા:</b> કલશ અને ધજા ચઢાવવા."]
    M=[("પ્રાસાદ (રેખા થી રેખા)",fi(P),"માણસ 6′ પરથી"),("ગર્ભગૃહ",fi(GARBH),"⚠ અંદર માપવું"),("દીવાલ",fi(WALL),"⚠"),("ભીત + પીઠ",fi(HP),"ફોટા પરથી 3′-9″ જેવી"),("મંડોવર",fi(HM),"ફોટા પરથી 8′-2″, થર ઉપર ગોળ કર્યા"),("શિખર",fi(HS),"ગ્રંથ : × 1¼"),("આમલસારો + કલશ",fi(HA+HK),"ગ્રંથ"),("કુલ ઊંચાઈ",fi(TOTAL),""),("દ્વાર",f"{fi(DOORW)} × {fi(DOORH)}","ફોટા પરથી; ગ્રંથ મુજબ ઊંચાઈ 4′-6″"),("મંડપ",fi(MAND),"⚠ અંદાજ")]
    h='<div class="txt"><div class="cols"><div><h2>કયો ભાગ કેવો છે અને શું કરવું</h2><table><tr><th>ભાગ</th><th>હાલ ની સ્થિતિ</th><th>પૂરું કરવા શું કરવું</th></tr>'
    h+="".join(f"<tr><td><b>{a}</b></td><td>{b}</td><td>{c}</td></tr>" for a,b,c in R)+"</table></div><div><h2>કામ નો ક્રમ</h2><ol>"
    h+="".join(f"<li>{x}</li>" for x in S)+"</ol><h2>અંદાજી માપ</h2><table><tr><th>ભાગ</th><th>માપ</th><th>ક્યાંથી</th></tr>"
    h+="".join(f"<tr><td>{a}</td><td><b>{b}</b></td><td>{c}</td></tr>" for a,b,c in M)+"</table><p style='font-size:10pt'>⚠ બધા માપ ફોટા પરથી અંદાજ છે (± 10% જેટલો ફેર પડી શકે). સાઇટ ના સાચા માપ આવે એટલે ડ્રોઇંગ સુધારવી.</p></div></div></div>"
    return '<svg viewBox="0 0 420 297">'+frame("પૂરું કરવાની રીત","4","")+'<text x="16" y="20" class="h">મંદિર પૂરું કરવાની રીત</text></svg>'+h
pages=[f'<div class="pg"><svg viewBox="0 0 420 297">{f()}</svg></div>' for f in (sheet_plan,sheet_elev,sheet_detail)]+[f'<div class="pg">{sheet_notes()}</div>']
open("temple-drawings.html","w").write('<!doctype html><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?family=Noto+Sans+Gujarati:wght@400;700&display=swap" rel="stylesheet"><style>'+CSS+'</style>'+"".join(pages))
print("ok",HP,HM,TOTAL)
