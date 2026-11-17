"""Basic representative elevation of a Shekhari shikhar in the manner of Mahakaleshwar, Ujjain (not measured)."""
import math
W=100.0                      # prasad width at rekha (units)
S=1.72                        # mm per unit on the sheet
CX=320; GY=600               # sheet coords (px in a 460x680 viewBox)
def X(x): return CX+x*S
def Y(y): return GY-y*S
out=[]
def poly(pts,cls='f',close=True):
    out.append(f'<path class="{cls}" d="M'+' L'.join(f'{X(x):.2f},{Y(y):.2f}' for x,y in pts)+('Z' if close else '')+'"/>')
def rekha(h,w0,H,top=.58,p=1.45): return w0*(1-(1-top)*(h/H)**p)
def shrung(xc,hb,w,H,tiers=None,cap=True,top=.58):
    w0=w/2; n=30
    L=[(xc-rekha(H*k/n,w0,H,top),hb+H*k/n) for k in range(n+1)]; R=[(xc+rekha(H*k/n,w0,H,top),hb+H*k/n) for k in range(n+1)]
    poly(L+R[::-1])
    for fr in (-.36,.36): poly([(xc+fr*2*rekha(H*k/n,w0,H,top),hb+H*k/n) for k in range(n+1)],'l',False)
    t=tiers or H/9; k=t
    while k<H-.5:
        ww=rekha(k,w0,H,top); poly([(xc-ww,hb+k),(xc+ww,hb+k)],'l',False); poly([(xc-ww,hb+k-.35*t*.25),(xc+ww,hb+k-.35*t*.25)],'l',False); k+=t
    if cap:
        tw=rekha(H,w0,H,top); hh=hb+H; g=tw*.62; a=tw*1.05; ar=max(.6,w*.05)
        poly([(xc-g,hh),(xc+g,hh),(xc+g,hh+w*.04),(xc-g,hh+w*.04)])
        e=[(xc+a*math.cos(2*math.pi*q/30),hh+w*.04+ar+ar*math.sin(2*math.pi*q/30)) for q in range(30)]; poly(e)
        for q in range(-4,5): poly([(xc+q*a/5,hh+w*.04+ar*.3),(xc+q*a/5,hh+w*.04+ar*1.7)],'l',False)
        b=hh+w*.04+2*ar; poly([(xc-g*.5,b),(xc-g*.7,b+w*.05),(xc-g*.35,b+w*.12),(xc,b+w*.2),(xc+g*.35,b+w*.12),(xc+g*.7,b+w*.05),(xc+g*.5,b)])
def band(x0,x1,y0,y1,cls='f'): poly([(x0,y0),(x1,y0),(x1,y1),(x0,y1)],cls)
# ---- base: jagati, peeth, mandovar (two jangha, like a large prasad) ----
band(-78,78,0,10); band(-74,74,10,13)
y=13
for w_,h_ in ((68,5),(66,4),(64,6),(61,3),(61,5),(60,4)): band(-w_,w_,y,y+h_); y+=h_        # peeth thars
PE=y
ang=[(-50,-36,0),(-36,-20,2),(-20,20,5),(20,36,2),(36,50,0)]           # karna, pratirath, bhadra
def mandovar_level(y0,jh):
    y=y0
    for h_,o in ((2.5,3),(6,2.5),(2.5,2),(2,3)):                       # khuro, kumbho, kalash, keval
        for a,b,d in ang: band(a-o,b+o,y,y+h_)
        y+=h_
    for a,b,d in ang:                                                  # jangha with figures/niches
        band(a-.4,b+.4,y,y+jh)
        if d==5:
            band(a+6,b-6,y+1,y+jh-2.5); band(a+9,b-9,y+2,y+jh-4,'d')
            poly([(a+5,y+jh-2.5),(0,y+jh+2),(b-5,y+jh-2.5)])
        else:
            band(a+1.5,b-1.5,y+1,y+jh-1)
            xm=(a+b)/2; poly([(xm-1.3,y+2),(xm+1.3,y+2),(xm+.9,y+jh*.55),(xm+1.6,y+jh*.6),(xm,y+jh*.85),(xm-1.6,y+jh*.6),(xm-.9,y+jh*.55)],'l')
    y+=jh
    for h_,o in ((3,1),(2,2.5),(2.5,3.5)):                             # udgam/bharni/shiravati
        for a,b,d in ang: band(a-o,b+o,y,y+h_)
        y+=h_
    poly([(-55,y),(55,y),(58,y+1.2),(58,y+2.4),(-58,y+2.4),(-58,y+1.2)])  # chhajja
    return y+2.4
y=mandovar_level(PE,15)
for a,b,d in ang: band(a,b,y,y+3)                                        # balcony band between levels
y=mandovar_level(y+3,12)
Y0=y
# ---- shikhar (Shekhari) ----
H=W*1.55
shrung(0,Y0,W*.9,H,tiers=H/14,cap=False,top=.5)                          # mool shikhar (latina)
t=Y0+H; poly([(-15,t),(15,t),(15,t+3),(-15,t+3)])                        # skandh
poly([(-11,t+3),(11,t+3),(11,t+5),(-11,t+5)])                            # griva
poly([(-24+24*(1-math.cos(math.pi*q/30)),t+5+5.5*math.sin(math.pi*q/30)) for q in range(31)])  # amalsaro
for q in range(-9,10): poly([(q*2.4,t+5.4),(q*2.4,t+10)],'l',False)
poly([(-12,t+10.5),(12,t+10.5),(10,t+13),(-10,t+13)])                    # chandrika
k=t+13; poly([(-4,k),(-8,k+3),(-8.5,k+7),(-4.5,k+9.5),(-2,k+11),(-1.2,k+15),(0,k+21),(1.2,k+15),(2,k+11),(4.5,k+9.5),(8.5,k+7),(8,k+3),(4,k)],'g')   # kalash
poly([(26,Y0+H-25),(27.4,Y0+H-25),(27.4,k+40),(26,k+40)]); poly([(27.4,k+40),(50,k+34),(27.4,k+27)],'r')  # dhwajdand, dhaja
# karna shrungs, 3 tiers (upper first so the lower ones sit in front)
for hb,w,h in ((Y0+52,13,24),(Y0+26,15,28),(Y0,17,32)):
    for s in (-1,1): shrung(s*(43-(hb-Y0)*.12),hb,w,h)
# pratirath shrungs, 2 tiers
for hb,w,h in ((Y0+30,13,26),(Y0,15,30)):
    for s in (-1,1): shrung(s*(28-(hb-Y0)*.1),hb,w,h)
# urushrungs on the bhadra, 3 stacked
for hb,w,h in ((Y0+68,26,62),(Y0+34,32,66),(Y0,38,68)): shrung(0,hb,w,h)
band(-7,7,Y0+6,Y0+22); band(-4.5,4.5,Y0+8,Y0+19,'d')                     # rathika (gavaksh) with deity
TOP=k+21
# ---- labels ----
lab=[]
def L(t,x,y,side=1,dy=0):
    tx=X(108*side); ty=Y(y)+dy
    lab.append(f'<polyline class="ld" points="{X(x):.1f},{Y(y):.1f} {X(96*side):.1f},{ty:.1f} {tx:.1f},{ty:.1f}"/><circle cx="{X(x):.1f}" cy="{Y(y):.1f}" r="1.2" class="dot"/><text x="{tx+(4 if side>0 else -4):.1f}" y="{ty+4:.1f}" text-anchor="{"start" if side>0 else "end"}">{t}</text>')
L('ધજા · ધ્વજદંડ',38,k+36,1); L('કળશ (સોનાનો)',0,k+12,1); L('આમલસારો',20,t+7.5,1); L('સ્કંધ · ગ્રીવા',14,t+2,1)
L('મૂળ શિખર (લતિન રેખા)',30,Y0+H-40,1); L('ઉરુશૃંગ 3',0,Y0+108,1); L('ઉરુશૃંગ 2',8,Y0+80,1); L('ઉરુશૃંગ 1 (ભદ્રે)',14,Y0+42,1)
L('રથિકા (ગવાક્ષ)',0,Y0+15,1)
L('કર્ણ શૃંગ — 3 થર',-40,Y0+62,-1); L('પ્રતિરથ શૃંગ — 2 થર',-26,Y0+40,-1); L('કર્ણ શૃંગ 1',-43,Y0+14,-1)
L('છજ્જું',-57,Y0-1,-1); L('ઉપર ની જંઘા',-43,Y0-12,-1); L('ઝરૂખા નો પટ્ટો',-40,PE+45,-1,0)
L('નીચે ની જંઘા (મૂર્તિઓ)',-43,PE+22,-1); L('કુંભો · કળશ · કેવાળ',-50,PE+7,-1); L('પીઠ',-64,20,-1); L('જગતી',-76,5,-1)
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 {GY+60}" width="640" height="{GY+60}">
<style>.f{{fill:#fff;stroke:#1b1b1b;stroke-width:.55;stroke-linejoin:round}}.l{{fill:none;stroke:#1b1b1b;stroke-width:.35}}.d{{fill:#2b2b2b;stroke:#1b1b1b;stroke-width:.4}}
.g{{fill:#f3d27a;stroke:#7a5a00;stroke-width:.6}}.r{{fill:#e8742a;stroke:#9a3a00;stroke-width:.5}}.ld{{fill:none;stroke:#0a3d91;stroke-width:.4}}.dot{{fill:#0a3d91}}
text{{font-family:'Noto Sans Gujarati',sans-serif;font-size:8.2px;fill:#111}}.h{{font-size:15px;font-weight:700}}.s{{font-size:7.2px;fill:#555}}</style>
<rect width="640" height="{GY+60}" fill="#fff"/>
<text x="20" y="28" class="h">મહાકાલેશ્વર, ઉજ્જૈન — શિખર (બેઝિક ડ્રોઇંગ)</text>
<text x="20" y="42" class="s">શેખરી (અનેકાંડક) નાગર શિખર · પ્રતિનિધિ ડ્રોઇંગ — માપેલું નથી, શૃંગ ની સંખ્યા અંદાજી</text>
{''.join(out)}
<line x1="{X(-95)}" y1="{GY}" x2="{X(95)}" y2="{GY}" stroke="#111" stroke-width="1.1"/>
{''.join(lab)}
<text x="20" y="{GY+28}" class="s">અંડક (અંદાજી): મૂળ શિખર 1 + ઉરુશૃંગ 3×4 + કર્ણ શૃંગ 3×8 + પ્રતિરથ શૃંગ 2×8 = 53 — સાચું નામ સાઇટ ના શૃંગ ગણી ને નક્કી થાય ⚠</text>
</svg>'''
open('mahakal.svg','w').write(svg)
open('mahakal.html','w').write('<!doctype html><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?family=Noto+Sans+Gujarati:wght@400;700&display=swap" rel="stylesheet"><style>body{margin:0}svg{display:block;width:1600px;height:auto}</style>'+svg)
print('top',round(TOP),'Y0',round(Y0))
