"""Local graphical reports; no network calls or automatic uploads."""
from io import BytesIO
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from brand import PALETTE, TAGLINE

def font(path, size):
    if path:
        return ImageFont.truetype(str(Path(path)), size)
    return ImageFont.load_default(size=size)

def render_report(title, rows, fonts=None):
    """Return PNG bytes and accessible text. Rows are (label, value, state)."""
    fonts = fonts or {}
    rows = list(rows)[:20]
    heading = font(fonts.get('heading'), 38)
    body = font(fonts.get('body'), 26)
    mono = font(fonts.get('mono'), 23)
    im = Image.new('RGB', (1200, 230 + 90 * len(rows)), PALETTE['obsidian'])
    d = ImageDraw.Draw(im)
    def fit(value, face, width):
        value = ' '.join(str(value).split())[:1000]
        if d.textlength(value, font=face) <= width:
            return value
        while value and d.textlength(value + '…', font=face) > width:
            value = value[:-1]
        return value + '…'
    d.rectangle((0, 0, 1200, 8), fill=PALETTE['cyber_cyan'])
    d.text((40, 30), 'PHREX / CODEPHREX INTELLIGENCE', font=body, fill=PALETTE['cyber_cyan'])
    d.text((40, 85), fit(title, heading, 1120), font=heading, fill=PALETTE['platinum'])
    colors = {'success':'#43D997','failure':'#FF6B6B','pending':'#FFB547'}
    for i, (label, value, state) in enumerate(rows):
        y = 150 + 90*i
        d.rounded_rectangle((40,y,1160,y+76), radius=12, fill=PALETTE['midnight'])
        d.rectangle((40,y+12,46,y+64), fill=colors.get(state, PALETTE['electric_blue']))
        d.text((64,y+10), fit(label, body, 1060), font=body, fill=PALETTE['platinum'])
        d.text((64,y+42), fit(value, mono, 1060), font=mono, fill=PALETTE['cyber_cyan'])
    d.text((40, im.height-48), TAGLINE, font=body, fill=PALETTE['platinum'])
    out = BytesIO()
    im.save(out, format='PNG')
    alt = str(title) + '\n' + '\n'.join(f'{label}: {value} ({state})' for label,value,state in rows)
    return out.getvalue(), alt
