"""Split the owner's ornament DXF sheets into single figures (connected groups of entities)."""
import sys, json, ezdxf
from ezdxf import recover, bbox
def comps(path, tol=0.4, minsize=6):
    d,_=recover.readfile(path); m=d.modelspace(); ents=[]
    ext=bbox.extents(m); W=ext.size.x
    for e in m:
        if e.dxftype() in ('TEXT','MTEXT','DIMENSION'): continue
        try: b=bbox.extents([e])
        except Exception: continue
        if not b.has_data: continue
        if b.size.x>W*0.5: continue                      # page frame
        ents.append((b.extmin.x-tol,b.extmin.y-tol,b.extmax.x+tol,b.extmax.y+tol,e))
    n=len(ents); par=list(range(n))
    def f(i):
        while par[i]!=i: par[i]=par[par[i]]; i=par[i]
        return i
    order=sorted(range(n),key=lambda i:ents[i][0]); active=[]
    for i in order:
        x0,y0,x1,y1,_=ents[i]; active=[j for j in active if ents[j][2]>=x0]
        for j in active:
            a=ents[j]
            if a[1]<=y1 and a[3]>=y0: par[f(i)]=f(j)
        active.append(i)
    g={}
    for i in range(n): g.setdefault(f(i),[]).append(i)
    out=[]
    for k,ix in g.items():
        x0=min(ents[i][0] for i in ix);y0=min(ents[i][1] for i in ix);x1=max(ents[i][2] for i in ix);y1=max(ents[i][3] for i in ix)
        if max(x1-x0,y1-y0)<minsize: continue
        out.append(dict(box=[x0+tol,y0+tol,x1-tol,y1-tol],ents=[ents[i][4] for i in ix]))
    out.sort(key=lambda c:(-round(c['box'][3]/20),c['box'][0]))
    return d,out
if __name__=='__main__':
    d,cs=comps(sys.argv[1])
    for i,c in enumerate(cs): print(i,[round(v,1) for v in c['box']],len(c['ents']))
