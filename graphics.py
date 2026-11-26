"""Local graphical reports; no network calls or automatic uploads."""
from io import BytesIO
from pathlib import Path
from itertools import islice
import os
from PIL import Image, ImageDraw, ImageFont
from brand import PALETTE, TAGLINE

def font(path, size):
    if path:
        try:
            return ImageFont.truetype(str(Path(path)), size)
        except (OSError, ValueError):
            pass
    return ImageFont.load_default(size=size)

def render_report(title, rows, fonts=None, *, source=None, period=None):
    """Return PNG bytes and accessible text. Rows are (label, value, state)."""
    fonts = fonts if fonts is not None else {role: os.getenv('PHREX_FONT_' + role.upper()) for role in ('heading', 'body', 'mono')}
    rows = list(islice(rows, 20))
    metadata = source is not None or period is not None
    heading = font(fonts.get('heading'), 38)
    body = font(fonts.get('body'), 26)
    mono = font(fonts.get('mono'), 23)
    im = Image.new('RGB', (1200, 230 + 90 * len(rows) + (70 if metadata else 0)), PALETTE['obsidian'])
    d = ImageDraw.Draw(im)
    def fit(value, face, width):
        value = ' '.join(str(value).split())[:1000]
        if d.textlength(value, font=face) <= width:
            return value
        while value and d.textlength(value + '…', font=face) > width:
            value = value[:-1]
        return value + '…'
    d.rectangle((0, 0, 1200, 8), fill=PALETTE['cyber_cyan'])
    d.polygon([(65,22),(89,36),(89,64),(65,78),(41,64),(41,36)], outline=PALETTE['cyber_cyan'], width=3)
    d.text((54,33), 'P', font=body, fill=PALETTE['platinum'])
    d.text((110, 35), 'PHREX / CODEPHREX INTELLIGENCE', font=body, fill=PALETTE['cyber_cyan'])
    d.text((40, 85), fit(title, heading, 1120), font=heading, fill=PALETTE['platinum'])
    colors = {'success':'#43D997','failure':'#FF6B6B','pending':'#FFB547'}
    for i, (label, value, state) in enumerate(rows):
        y = 150 + 90*i
        d.rounded_rectangle((40,y,1160,y+76), radius=12, fill=PALETTE['midnight'])
        d.rectangle((40,y+12,46,y+64), fill=colors.get(state, PALETTE['electric_blue']))
        d.text((64,y+10), fit(label, body, 1060), font=body, fill=PALETTE['platinum'])
        d.text((64,y+42), fit(value, mono, 1060), font=mono, fill=PALETTE['cyber_cyan'])
    if metadata:
        d.text((40, im.height-112), fit("Source: " + str(source or "Not supplied"), mono, 1120), font=mono, fill=PALETTE['platinum'])
        d.text((40, im.height-82), fit("Period: " + str(period or "Not supplied"), mono, 1120), font=mono, fill=PALETTE['platinum'])
    d.text((40, im.height-48), TAGLINE, font=body, fill=PALETTE['platinum'])
    out = BytesIO()
    im.save(out, format='PNG')
    alt = str(title) + '\n' + '\n'.join(f'{label}: {value} ({state})' for label,value,state in rows)
    if metadata:
        alt += '\nSource: ' + str(source or 'Not supplied') + '\nPeriod: ' + str(period or 'Not supplied')
    return out.getvalue(), alt
