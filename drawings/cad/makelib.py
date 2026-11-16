"""Build murti_lib.dxf: the owner's figures as named blocks (base point = bottom centre)."""
import ezdxf
from ezdxf import recover, bbox
from ezdxf.addons import Importer
from extract import comps
U='/root/.claude/uploads/b113044e-3600-59b5-a6ad-4d97fce82858/'
PICK={'d466ed1d-Dxf_Samples006.dxf':{0:'DIK_KUBER',1:'DIK_ISHAN',2:'DIK_INDRA',3:'DIK_AGNI',4:'DIK_YAM',5:'DIK_NIRUTI',6:'DIK_VARUN',7:'DIK_VAYU'},
      '0ede287d-004.dxf':{0:'APSARA',1:'VISHNU'},
      '67ed3f6f-005.dxf':{1:'SINH',2:'HATHI_BETHO',3:'HATHI_JODU'}}
t=ezdxf.new('R2018',setup=True); t.units=1
t.layers.add('MURTI',color=7)
info={}
for f,pk in PICK.items():
    s,cs=comps(U+f); imp=Importer(s,t)
    for i,name in pk.items():
        c=cs[i]; x0,y0,x1,y1=c['box']
        b=t.blocks.new(name,base_point=((x0+x1)/2,y0,0))
        imp.import_entities(c['ents'],b); info[name]=(x1-x0,y1-y0)
    imp.finalize()
s,_=recover.readfile(U+'d017817a-new_block.dxf'); imp=Importer(s,t)
sb=s.blocks.get('A$C233E209E'); ex=bbox.extents(sb)
b=t.blocks.new('HATHI_SAVAR',base_point=((ex.extmin.x+ex.extmax.x)/2,ex.extmin.y,0))
imp.import_entities(list(sb),b); imp.finalize(); info['HATHI_SAVAR']=(ex.size.x,ex.size.y)
for blk in t.blocks:
    if blk.name in info:
        for e in blk: e.dxf.layer='MURTI'
t.saveas('murti_lib.dxf')
for k,v in info.items(): print(k,round(v[0],1),round(v[1],1))
