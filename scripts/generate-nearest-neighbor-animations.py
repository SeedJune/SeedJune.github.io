#!/usr/bin/env python3
"""Generate the two nearest-neighbor teaching GIFs (Python 3 + Pillow).

Run from any directory. The geometry and algorithm trace are computed from the
same fixed samples. No plotting, triangulation, or image-generation API is used.
Voronoi cells are exact half-plane intersections; global adjacency is tested
along pairwise bisectors, including unbounded ridges.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
POINTS = [
    (-0.443, 1.333), (-2.069, 1.916), (-0.683, -1.500),
    (-1.687, 0.557), (-0.720, 2.022), (-2.292, 1.020),
    (2.054, 1.330), (2.709, 0.101), (0.709, -0.672),
    (2.657, -1.389), (0.664, -1.667), (1.090, 1.577),
]
LABELS = [0] * 6 + [1] * 6
ALL = list(range(len(POINTS)))
W, H, SCALE = 1280, 850, 2
BOX = (58, 168, 746, 723)
BOUNDS = (-3.5, 3.7, -2.5, -2.5 + (BOX[3] - BOX[1]) * 7.2 / (BOX[2] - BOX[0]))
INK, MUTED = "#193750", "#526471"
TEAL, CORAL = "#227E82", "#C6553B"
GOLD, LINE, BG = "#AD750B", "#CBD4D5", "#FAF8F2"
CLASS = [TEAL, CORAL]
FILL = ["#E7F2EF", "#F9EAE1"]
FONT_FILES = [
    "/System/Library/Fonts/Hiragino Sans GB.ttc",
    "/System/Library/Fonts/STHeiti Medium.ttc",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
]
FONTS = {}
CELLS = {}


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1]


def sub(a, b):
    return a[0] - b[0], a[1] - b[1]


def nearest(q, active):
    return min(active, key=lambda i: (dot(sub(POINTS[q], POINTS[i]), sub(POINTS[q], POINTS[i])), i))


def clip(poly, normal, bound):
    """Clip a convex polygon against normal dot x <= bound."""
    result = []
    for a, b in zip(poly, poly[1:] + poly[:1]):
        da, db = dot(normal, a) - bound, dot(normal, b) - bound
        inside_a, inside_b = da <= 1e-9, db <= 1e-9
        if inside_a:
            result.append(a)
        if inside_a != inside_b:
            t = da / (da - db)
            result.append((a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1])))
    return result


def cells(active):
    key = tuple(active)
    if key not in CELLS:
        xmin, xmax, ymin, ymax = BOUNDS
        result = {}
        for i in active:
            polygon = [(xmin, ymin), (xmax, ymin), (xmax, ymax), (xmin, ymax)]
            for j in active:
                if i == j:
                    continue
                normal = tuple(2 * v for v in sub(POINTS[j], POINTS[i]))
                bound = dot(POINTS[j], POINTS[j]) - dot(POINTS[i], POINTS[i])
                polygon = clip(polygon, normal, bound)
            result[i] = polygon
        CELLS[key] = result
    return CELLS[key]


def ridge(i, j, active, viewport=False):
    """Return bisector interval; positive-length intervals mean adjacency."""
    a, b = POINTS[i], POINTS[j]
    middle = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
    delta = sub(b, a)
    direction = (-delta[1], delta[0])
    lo, hi = -math.inf, math.inf
    constraints = [
        (tuple(2 * v for v in sub(POINTS[q], a)), dot(POINTS[q], POINTS[q]) - dot(a, a))
        for q in active if q not in (i, j)
    ]
    if viewport:
        xmin, xmax, ymin, ymax = BOUNDS
        constraints += [((1, 0), xmax), ((-1, 0), -xmin), ((0, 1), ymax), ((0, -1), -ymin)]
    for normal, bound in constraints:
        coefficient = dot(normal, direction)
        remainder = bound - dot(normal, middle)
        if abs(coefficient) < 1e-12:
            if remainder < -1e-9:
                return None
        elif coefficient > 0:
            hi = min(hi, remainder / coefficient)
        else:
            lo = max(lo, remainder / coefficient)
    if hi - lo <= 1e-8:
        return None
    if not viewport:
        return lo, hi
    return [
        (middle[0] + t * direction[0], middle[1] + t * direction[1])
        for t in (lo, hi)
    ]


NEIGHBORS = {i: [j for j in ALL if j != i and ridge(i, j, ALL) is not None] for i in ALL}
KEEP = [i for i in ALL if any(LABELS[j] != LABELS[i] for j in NEIGHBORS[i])]


def font(size):
    if size not in FONTS:
        path = next((p for p in FONT_FILES if Path(p).is_file()), None)
        if not path:
            raise RuntimeError("A CJK font is required; add its path to FONT_FILES.")
        FONTS[size] = ImageFont.truetype(path, size * SCALE)
    return FONTS[size]


def xy(p):
    xmin, xmax, ymin, ymax = BOUNDS
    return (BOX[0] + (p[0] - xmin) / (xmax - xmin) * (BOX[2] - BOX[0]),
            BOX[3] - (p[1] - ymin) / (ymax - ymin) * (BOX[3] - BOX[1]))


class Canvas:
    def __init__(self):
        self.image = Image.new("RGB", (W * SCALE, H * SCALE), BG)
        self.d = ImageDraw.Draw(self.image)

    def text(self, x, y, value, size=23, color=INK, anchor=None):
        self.d.text((x * SCALE, y * SCALE), value, font=font(size), fill=color, anchor=anchor)

    def line(self, points, fill=LINE, width=1):
        self.d.line([(x * SCALE, y * SCALE) for x, y in points], fill=fill, width=round(width * SCALE))

    def polygon(self, points, fill, outline=None, width=1):
        self.d.polygon([(x * SCALE, y * SCALE) for x, y in points], fill=fill)
        if outline:
            self.line(points + points[:1], outline, width)

    def rect(self, box, fill, outline=None, radius=0, width=1):
        self.d.rounded_rectangle(tuple(v * SCALE for v in box), radius=radius * SCALE,
                                 fill=fill, outline=outline, width=round(width * SCALE))

    def circle(self, x, y, radius, fill=None, outline=None, width=1):
        self.d.ellipse(((x-radius)*SCALE, (y-radius)*SCALE, (x+radius)*SCALE, (y+radius)*SCALE),
                       fill=fill, outline=outline, width=round(width*SCALE))

    def dashed(self, a, b, color=GOLD, width=2):
        dx, dy = b[0]-a[0], b[1]-a[1]
        length = math.hypot(dx, dy)
        for start in range(0, int(length), 13):
            t, u = start/length, min(start+7, length)/length
            self.line([(a[0]+t*dx,a[1]+t*dy),(a[0]+u*dx,a[1]+u*dy)],color,width)

    def finish(self):
        return self.image.resize((W, H), Image.Resampling.LANCZOS)


def marker(c, i, filled=True, ring=False, current=False, removed=False, opacity=1):
    if opacity <= 0:
        return
    x, y = xy(POINTS[i])
    if removed:
        color = "#AAB4B6"
    else:
        color = CLASS[LABELS[i]]
    if opacity < 1:
        rgb = Image.new("RGB",(1,1),color).getpixel((0,0))
        base = Image.new("RGB",(1,1),FILL[LABELS[i]]).getpixel((0,0))
        color = tuple(round(opacity*a+(1-opacity)*b) for a,b in zip(rgb,base))
    if ring:
        c.circle(x, y, 23, outline=INK, width=2.8)
    if current:
        c.circle(x, y, 29, outline=GOLD, width=3.4)
    if LABELS[i] == 0:
        c.circle(x,y,17,fill=color if filled else BG,outline=color,width=2.4)
    else:
        c.rect((x-16,y-16,x+16,y+16),fill=color if filled else BG,outline=color,radius=4,width=2.4)
    if opacity > .2:
        c.text(x,y+.5,f"{i+1:02d}",17,"#FFFFFF" if filled else color,anchor="mm")


def diagram(c, active, *, show_cells=True, focus=None, neighbors=()):
    c.rect(BOX,"#FFFFFF",LINE,radius=0)
    if show_cells:
        for i, poly in cells(active).items():
            pts = [xy(p) for p in poly]
            if pts:
                c.polygon(pts,FILL[LABELS[i]],LINE,1.1)
        if focus is not None and focus in cells(active):
            for i in neighbors:
                if i in cells(active):
                    pts=[xy(p) for p in cells(active)[i]]
                    if pts:c.line(pts+pts[:1],CLASS[LABELS[i]],2)
            pts = [xy(p) for p in cells(active)[focus]]
            if pts:c.polygon(pts,"#FFF2CE",GOLD,2.8)
        for p,i in enumerate(active):
            for j in active[p+1:]:
                if LABELS[i] != LABELS[j]:
                    edge=ridge(i,j,active,viewport=True)
                    if edge:c.line([xy(v) for v in edge],INK,3.2)
    else:
        for x in range(-3,4):
            c.line([xy((x,BOUNDS[2])),xy((x,BOUNDS[3]))],"#E4E9E6")
        for y in range(-2,4):
            if y<BOUNDS[3]:c.line([xy((BOUNDS[0],y)),xy((BOUNDS[1],y))],"#E4E9E6")
    c.line([(BOX[0],BOX[1]),(BOX[2],BOX[1]),(BOX[2],BOX[3]),(BOX[0],BOX[3]),(BOX[0],BOX[1])],LINE,1.2)
    c.text(BOX[2]-8,BOX[3]+17,"特征 1",18,MUTED,anchor="ra")
    c.text(BOX[0],BOX[1]-31,"特征 2",18,MUTED)


def scaffold(title, subtitle, stage, step, steps, footer):
    c=Canvas()
    c.text(48,28,title,35)
    c.text(50,85,subtitle,22,MUTED)
    c.rect((779,148,1233,747),"#FFFFFF","#DCE1DD",14)
    c.text(805,171,stage,27)
    c.circle(805,780,10,TEAL);c.text(825,766,"类别 I",20)
    c.rect((939,770,959,790),CORAL,radius=3);c.text(970,766,"类别 II",20)
    c.text(58,774,footer,19,MUTED)
    c.rect((48,820,1232,825),"#E2E6DF",radius=2)
    c.rect((48,820,48+1184*(step+1)/steps,825),TEAL,radius=2)
    c.text(1227,779,f"{step+1:02d} / {steps:02d}",17,MUTED,anchor="rm")
    return c


def ids(items):
    return "、".join(f"{i+1:02d}" for i in items) if items else "无"


def wrapped(c,x,y,value,size=22,color=INK,width=386,lineheight=36):
    line="";lines=[]
    for char in value:
        candidate=line+char
        if font(size).getlength(candidate)/SCALE>width:
            if char in "，。；：！？、":
                lines.append(line[:-1]);line=line[-1:]+char
            else:
                lines.append(line);line=char
        else:line=candidate
    if line:lines.append(line)
    if len(lines)>1 and len(lines[-1])<5:
        count=5-len(lines[-1])
        lines[-1]=lines[-2][-count:]+lines[-1]
        lines[-2]=lines[-2][:-count]
    for line in lines:
        c.text(x,y,line,size,color);y+=lineheight
    return y


def chips(c,items,y,caption):
    c.text(805,y,caption,20,MUTED)
    for n,i in enumerate(items):
        x=809+(n%6)*62
        yy=y+43+(n//6)*48
        c.rect((x-3,yy-3,x+46,yy+32),FILL[LABELS[i]],radius=6)
        c.text(x+21,yy+14,f"{i+1:02d}",19,CLASS[LABELS[i]],anchor="mm")


def editing_frames():
    states=[dict(kind="raw",duration=2200),dict(kind="voronoi",duration=2400)]
    marked=[]
    for i in ALL:
        if i in KEEP:marked.append(i)
        states.append(dict(kind="scan",focus=i,marked=marked[:],duration=1800))
    states.append(dict(kind="marked",marked=KEEP,duration=2600))
    for alpha in [.8,.6,.4,.2,0]:
        states.append(dict(kind="remove",marked=KEEP,alpha=alpha,duration=180))
    states.append(dict(kind="rebuild",marked=KEEP,duration=5200))
    frames=[]
    for step,s in enumerate(states):
        kind=s["kind"];i=s.get("focus");marked=s.get("marked",[])
        stage={"raw":"原始训练样本","voronoi":"构造 Voronoi 图","scan":f"检查样本 {i+1:02d}" if i is not None else "",
               "marked":"完成邻接检查","remove":"统一删除未标记点","rebuild":"重建原型与分类区域"}[kind]
        c=scaffold("剪辑最近邻：保留与异类相邻的原型",
                   "邻接指两个 Voronoi 单元共享边界；先完成标记，再统一删除。",
                   stage,step,len(states),"细线：单元边界   深色线：分类边界")
        active=KEEP if kind=="rebuild" else ALL
        ns=NEIGHBORS[i] if i is not None else []
        diagram(c,active,show_cells=kind!="raw",focus=i,neighbors=ns)
        if i is not None:
            for j in ns:c.dashed(xy(POINTS[i]),xy(POINTS[j]),CLASS[LABELS[j]],1.7)
        for q in ALL:
            if kind=="rebuild" and q not in KEEP:continue
            removed=(kind in ("marked","remove") and q not in KEEP) or (kind=="scan" and q<=i and q not in KEEP)
            marker(c,q,ring=q in marked,current=q==i,removed=removed,
                   opacity=s.get("alpha",1) if kind=="remove" and q not in KEEP else 1)
        if kind=="raw":
            wrapped(c,805,233,"固定同一组 12 个带标签样本。每个样本最初都是最近邻分类的原型。")
            chips(c,ALL,386,"初始原型")
        elif kind=="voronoi":
            wrapped(c,805,233,"每个单元归属于距离最近的样本。异类单元之间的公共边界形成分类边界。")
            wrapped(c,805,390,"随后按编号逐点检查邻接关系。",color=MUTED)
        elif kind=="scan":
            c.text(805,232,"邻接样本",21,MUTED)
            y=wrapped(c,805,269,ids(ns),24)
            different=[j for j in ns if LABELS[j]!=LABELS[i]]
            c.text(805,y+16,"异类邻接",21,MUTED)
            y=wrapped(c,805,y+52,ids(different),24,color=CORAL if different else MUTED)
            c.text(805,y+25,"标记保留" if different else "不标记，待统一删除",26,TEAL if different else MUTED)
            chips(c,marked,541,"已标记原型（深色外圈）")
        else:
            delete=[q for q in ALL if q not in KEEP]
            wrapped(c,805,234,f"保留 {len(KEEP)} 个边界相关原型，删除 {len(delete)} 个未标记原型。",26)
            c.text(805,348,"删除编号",21,MUTED)
            wrapped(c,805,388,ids(delete),23,MUTED)
            chips(c,KEEP,489,"保留的原型")
            if kind=="rebuild":
                wrapped(c,805,664,"重建后单元改变，分类边界保持。",19,MUTED,lineheight=29)
        frames.append((c.finish(),s["duration"],s))
    return frames


def condensation_states():
    active=[0]
    states=[dict(kind="init",active=active[:],duration=2400)]
    passes=[]
    for passno in range(1,len(ALL)+1):
        states.append(dict(kind="pass",active=active[:],passno=passno,duration=1600))
        added=[]
        # An item added to A is removed from B immediately.
        for q in ALL:
            if q in active:continue
            nn=nearest(q,active)
            wrong=LABELS[q]!=LABELS[nn]
            states.append(dict(kind="check",active=active[:],query=q,nn=nn,wrong=wrong,
                               passno=passno,duration=1800 if wrong else 1100))
            if wrong:
                active.append(q);added.append(q)
                states.append(dict(kind="add",active=active[:],query=q,nn=nn,passno=passno,duration=1500))
        passes.append(added)
        states.append(dict(kind="endpass",active=active[:],added=added[:],passno=passno,duration=2400))
        if not added:break
    states.append(dict(kind="done",active=active[:],passno=passno,duration=5400))
    assert all(LABELS[nearest(q,active)]==LABELS[q] for q in ALL)
    return states,passes


def compression_frames():
    states,passes=condensation_states()
    frames=[]
    for step,s in enumerate(states):
        kind=s["kind"];active=s["active"];q=s.get("query");nn=s.get("nn")
        passno=s.get("passno",1)
        stage={"init":"初始化原型集合 A","pass":f"第 {passno} 轮 · 重新遍历 B",
               "check":f"第 {passno} 轮 · 检查 {q+1:02d}" if q is not None else "",
               "add":f"将样本 {q+1:02d} 加入 A" if q is not None else "",
               "endpass":f"第 {passno} 轮结束","done":"收敛：一整轮无新增原型"}[kind]
        c=scaffold("压缩最近邻：将误分类样本加入原型集",
                   "实心为原型 A，空心为待检查样本 B；背景随当前 A 的分类结果更新。",
                   stage,step,len(states),"金色圈：当前样本   虚线：最近原型")
        diagram(c,active)
        if kind=="check":c.dashed(xy(POINTS[q]),xy(POINTS[nn]),GOLD,3)
        for i in ALL:
            marker(c,i,filled=i in active,ring=i in active,current=i==q)
        if kind=="init":
            wrapped(c,805,235,"先选择样本 01 作为唯一原型，其余样本暂存于集合 B。",25)
            wrapped(c,805,370,"按 02 → 12 的顺序检查 B，之后从剩余编号重新遍历。",22,MUTED)
        elif kind=="pass":
            wrapped(c,805,235,"本轮使用当前 A 分类剩余样本。之前分类正确的样本也必须重新检查。",25)
            wrapped(c,805,405,"原型增加后，最近邻关系可能发生改变。",22,MUTED)
        elif kind=="check":
            c.text(805,232,f"当前样本：{q+1:02d}  /  类别 {'I' if LABELS[q]==0 else 'II'}",24)
            c.text(805,281,f"最近原型：{nn+1:02d}  /  类别 {'I' if LABELS[nn]==0 else 'II'}",24)
            c.text(805,359,"分类错误 → 移入 A" if s["wrong"] else "分类正确 → 留在 B",27,CORAL if s["wrong"] else TEAL)
            if q==2 and passno==2:
                wrapped(c,805,418,f"样本 03 在首轮分类正确；新增原型 {nn+1:02d} 后，它的预测类别发生改变。",21,MUTED)
        elif kind=="add":
            wrapped(c,805,236,f"样本 {q+1:02d} 从 B 移入 A，并立即参与后续分类。",26)
            wrapped(c,805,378,"背景已经按新的原型集合重算。",23,MUTED)
        elif kind=="endpass":
            added=s["added"]
            wrapped(c,805,237,("本轮新增原型："+ids(added)) if added else "本轮所有剩余样本均分类正确，没有新增原型。",25)
            wrapped(c,805,375,"继续遍历 B，检查原型更新后的影响。" if added else "满足停止条件。",23,TEAL if not added else MUTED)
        else:
            wrapped(c,805,238,f"12 个训练样本由 {len(active)} 个原型正确分类。",27)
            wrapped(c,805,365,"保留训练集上的分类一致性，并不要求保持原始分类边界。",22,MUTED)
        chips(c,active,551,f"原型集合 A：{len(active)} 个")
        c.text(805,699,f"待检查集合 B：{12-len(active)} 个",21,MUTED)
        frames.append((c.finish(),s["duration"],s))
    return frames,passes


def validate_geometry():
    # Check that clipping and adjacency agree and that the selected samples
    # preserve the visible classification regions after Voronoi editing.
    for i in ALL:
        for j in NEIGHBORS[i]:
            assert i in NEIGHBORS[j]
            if LABELS[i] != LABELS[j]:
                # Every class-border adjacency used to justify retention is
                # visible in the displayed viewport, not only outside it.
                assert ridge(i,j,ALL,viewport=True) is not None
    xmin,xmax,ymin,ymax=BOUNDS
    checked=0
    for ix in range(151):
        for iy in range(121):
            point=(xmin+(xmax-xmin)*ix/150,ymin+(ymax-ymin)*iy/120)
            def closest(active):
                return min(active,key=lambda q:(dot(sub(point,POINTS[q]),sub(point,POINTS[q])),q))
            assert LABELS[closest(ALL)]==LABELS[closest(KEEP)]
            checked+=1
    return checked


def save_animation(name,frames,out,preview):
    # One shared palette avoids palette flicker between successive states.
    samples=Image.new("RGB",(256*8,170*math.ceil(len(frames)/8)),BG)
    for i,(frame,_,_) in enumerate(frames):
        samples.paste(frame.resize((256,170)),((i%8)*256,(i//8)*170))
    palette=samples.quantize(colors=256,method=Image.Quantize.MEDIANCUT)
    images=[im.quantize(palette=palette,dither=Image.Dither.NONE) for im,_,_ in frames]
    path=out/f"{name}.gif"
    images[0].save(path,save_all=True,append_images=images[1:],
                   duration=[ms for _,ms,_ in frames],loop=0,disposal=1,optimize=False)
    picked=list(dict.fromkeys([0,1,len(frames)//3,len(frames)//2,len(frames)-2,len(frames)-1]))
    contact=Image.new("RGB",(W*2,H*3),"#FFFFFF")
    for j,i in enumerate(picked):
        contact.paste(frames[i][0],((j%2)*W,(j//2)*H))
    contact.resize((1536,1530),Image.Resampling.LANCZOS).save(preview/f"{name}-contact.jpg")
    frames[-1][0].save(preview/f"{name}-final.png")
    for i in picked:
        frames[i][0].save(preview/f"{name}-{i:03d}.png")
    with Image.open(path) as image:
        durations=[]
        for i in range(image.n_frames):
            image.seek(i);durations.append(image.info.get("duration",0))
        assert image.n_frames>1
        assert image.size==(W,H)
        assert sum(durations)==sum(ms for _,ms,_ in frames)
        assert image.info.get("loop")==0
        return {"path":str(path),"frames":image.n_frames,"duration_seconds":sum(durations)/1000,"bytes":path.stat().st_size}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir",type=Path,default=ROOT/"src/assets/blogs")
    parser.add_argument("--preview-dir",type=Path,default=Path("/private/tmp/nearest-neighbor-previews"))
    args=parser.parse_args()
    args.out_dir.mkdir(parents=True,exist_ok=True);args.preview_dir.mkdir(parents=True,exist_ok=True)
    checked=validate_geometry()
    editing=editing_frames();compression,passes=compression_frames()
    result={
        "kept_after_editing":[i+1 for i in KEEP],
        "compression_additions_by_pass":[[i+1 for i in p] for p in passes],
        "editing_grid_points_verified":checked,
        "animations":[
            save_animation("pattern-recognition-voronoi-editing",editing,args.out_dir,args.preview_dir),
            save_animation("pattern-recognition-condensed-neighbor",compression,args.out_dir,args.preview_dir),
        ],
    }
    (args.preview_dir/"verification.json").write_text(json.dumps(result,ensure_ascii=False,indent=2))
    print(json.dumps(result,ensure_ascii=False,indent=2))


if __name__=="__main__":
    main()
