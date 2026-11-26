"""Deterministic local PNG visualizations; no inferred measurements."""
from io import BytesIO
from itertools import islice
import math
from PIL import Image, ImageDraw
from graphics import font
from brand import PALETTE

def canvas(title, source, period, height):
    if not source or not period:
        raise ValueError("Source and reporting period required")
    im = Image.new("RGB", (1200, height), PALETTE["obsidian"])
    d = ImageDraw.Draw(im)
    d.rectangle((0,0,1200,8), fill=PALETTE["cyber_cyan"])
    d.text((40,25), "PHREX / CODEPHREX INTELLIGENCE", font=font(None,24), fill=PALETTE["cyber_cyan"])
    d.text((40,65), str(title)[:48], font=font(None,34), fill=PALETTE["platinum"])
    d.text((40,height-75), "Source: "+str(source)[:85], font=font(None,20), fill=PALETTE["platinum"])
    d.text((40,height-42), "Period: "+str(period)[:85], font=font(None,20), fill=PALETTE["platinum"])
    return im,d

def png(im):
    out = BytesIO()
    im.save(out, format="PNG")
    return out.getvalue()

def bar_chart(title, values, *, unit, source, period):
    if not unit:
        raise ValueError("Unit required")
    rows = list(islice(values, 13))
    if len(rows)>12:
        raise ValueError("Maximum 12 categories")
    for label,value in rows:
        if value is not None and (isinstance(value,bool) or not isinstance(value,(int,float)) or not math.isfinite(value) or value<0):
            raise ValueError("Expected finite nonnegative values or missing")
    im,d = canvas(title,source,period,240+60*max(1,len(rows)))
    maximum = max((v for _,v in rows if v is not None),default=0) or 1
    face = font(None,22)
    if not rows:
        d.text((40,130),"No observations available",font=face,fill=PALETTE["platinum"])
    for i,(label,value) in enumerate(rows):
        y=130+60*i
        d.text((40,y),str(label)[:22],font=face,fill=PALETTE["platinum"])
        d.rectangle((350,y,900,y+30),fill=PALETTE["midnight"])
        if value is not None and value>0:
            d.rectangle((350,y,350+550*(value/maximum),y+30),fill=PALETTE["electric_blue"])
        d.text((920,y),"Missing" if value is None else f"{value:g} {unit}"[:22],font=face,fill=PALETTE["platinum"])
    alt = f"{title}; {source}; {period}; unit: {unit}\n" + "\n".join(f"{k}: {'missing' if v is None else v}" for k,v in rows)
    return png(im),alt

def relationship_diagram(title, center, nodes, *, source, period, observed=False):
    nodes=list(islice(nodes,7))
    if len(nodes)>6:
        raise ValueError("Maximum six nodes")
    kind="Observed relationships" if observed else "Conceptual relationships"
    im,d=canvas(title,source,period,650)
    face=font(None,24)
    d.text((40,110),kind,font=face,fill=PALETTE["cyber_cyan"])
    for i,node in enumerate(nodes):
        x=70+(i%3)*370
        y=175+(i//3)*290
        d.line((600,340,x+160,y+35),fill=PALETTE["electric_blue"],width=3)
    for i,node in enumerate(nodes):
        x=70+(i%3)*370
        y=175+(i//3)*290
        d.rounded_rectangle((x,y,x+320,y+70),radius=12,fill=PALETTE["midnight"],outline=PALETTE["cyber_cyan"])
        d.text((x+160,y+35),str(node)[:20],anchor="mm",font=face,fill=PALETTE["platinum"])
    d.rounded_rectangle((440,305,760,375),radius=12,fill=PALETTE["midnight"],outline=PALETTE["cyber_cyan"])
    d.text((600,340),str(center)[:20],anchor="mm",font=face,fill=PALETTE["platinum"])
    return png(im),f"{title}; {kind}; {center} connected to {', '.join(map(str,nodes))}; Source: {source}; Period: {period}"
