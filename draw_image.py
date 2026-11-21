#!/usr/bin/env python3
"""Draw the entry image: the world news of Friday 20 November 2026 in one picture.

A newsprint-style infographic drawn with Pillow. Every word is real, spelled
text -- no generated imagery, no garbled lettering.

Run:   python3 draw_image.py
Writes entry.png (1024 x 1024) next to this file, deterministically.
"""
from PIL import Image, ImageDraw, ImageFont

CANVAS = (1024, 1024)
PAPER = (250, 247, 240)
CARD = (255, 255, 255)
INK = (22, 24, 30)
GREY = (96, 100, 112)
RED = (178, 34, 34)
NAVY = (24, 48, 88)
GOLD = (176, 124, 24)

FONTS = "/usr/share/fonts/truetype/dejavu"


def load(name, size):
    return ImageFont.truetype(f"{FONTS}/{name}", size)


TITLE = load("DejaVuSerif-Bold.ttf", 56)
DATE = load("DejaVuSans-Bold.ttf", 30)
KICKER = load("DejaVuSans-Bold.ttf", 19)
LEAD_HEAD = load("DejaVuSerif-Bold.ttf", 40)
LEAD_BODY = load("DejaVuSans.ttf", 22)
PANEL_KICK = load("DejaVuSans-Bold.ttf", 17)
PANEL_HEAD = load("DejaVuSans-Bold.ttf", 26)
PANEL_BODY = load("DejaVuSans.ttf", 20)
TICKER = load("DejaVuSans-Bold.ttf", 19)
FOOT = load("DejaVuSans.ttf", 16)


def flow(draw, text, font, width):
    """Split text into lines no wider than `width` pixels."""
    lines, current = [], ""
    for word in text.split():
        trial = (current + " " + word).strip()
        if draw.textlength(trial, font=font) <= width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


sheet = Image.new("RGB", CANVAS, PAPER)
pen = ImageDraw.Draw(sheet)

# ---------- masthead ----------
pen.text((48, 36), "THE WORLD TODAY", font=TITLE, fill=INK)
pen.text((48, 106), "FRIDAY 20 NOVEMBER 2026", font=DATE, fill=RED)
pen.line([(48, 154), (976, 154)], fill=INK, width=3)

# ---------- lead story ----------
pen.rounded_rectangle([48, 178, 976, 468], radius=12, fill=CARD)
pen.rectangle([48, 178, 60, 468], fill=RED)
pen.text((84, 198), "UKRAINE  ·  OVERNIGHT BARRAGE", font=KICKER, fill=RED)
pen.text((84, 226), "Kyiv\u2019s bridges hit in huge barrage",
         font=LEAD_HEAD, fill=INK)
lead = ("Russia fired 84 cruise missiles and 404 drones in one of the war\u2019s "
        "largest air attacks, striking three bridges over the Dnipro and knocking "
        "out power and heat. Missiles also fell inside Poland; Kyiv officials "
        "report at least eight dead and 28 injured.")
y = 292
for row in flow(pen, lead, LEAD_BODY, 856):
    pen.text((84, y), row, font=LEAD_BODY, fill=INK)
    y += 30
pen.text((84, 424), "THE DAY\u2019S BIGGEST STORY", font=KICKER, fill=GREY)

# ---------- four panels ----------
stories = [
    ("RIYADH", RED, "Missile hits PIF Tower",
     "A Houthi missile blew out windows across seven floors of Riyadh\u2019s tallest "
     "tower. No injuries; more attacks were intercepted Friday."),
    ("ODISHA, INDIA", NAVY, "Cyclone Akvan landfall",
     "Landfall near Gopalpur, winds gusting to 90 km/h, after 300,000+ evacuations. "
     "It weakened fast; no deaths in early assessments."),
    ("MARKETS", GOLD, "AI sell-off deepens",
     "Anthropic slid after its record debut: Taiwan\u2019s Taiex fell 6.2%, SoftBank "
     "over 14% and the Nikkei 4.8%."),
    ("COP31", NAVY, "Draft drops phase-out",
     "The summit draft no longer calls for phasing out fossil fuels, drawing fire "
     "from island states as the talks near their deadline."),
]
PX, PY = 48, 492
PW, PH, GAP = 452, 200, 24
for n, (kick, accent, head, body) in enumerate(stories):
    x = PX + (n % 2) * (PW + GAP)
    y0 = PY + (n // 2) * (PH + GAP)
    pen.rounded_rectangle([x, y0, x + PW, y0 + PH], radius=10, fill=CARD)
    pen.rectangle([x, y0, x + 6, y0 + PH], fill=accent)
    pen.text((x + 22, y0 + 14), kick, font=PANEL_KICK, fill=accent)
    pen.text((x + 22, y0 + 38), head, font=PANEL_HEAD, fill=INK)
    yy = y0 + 78
    for row in flow(pen, body, PANEL_BODY, PW - 44):
        pen.text((x + 22, yy), row, font=PANEL_BODY, fill=GREY)
        yy += 26

# ---------- ticker + footer ----------
pen.line([(0, 922), (1024, 922)], fill=INK, width=2)
pen.text((48, 934),
         "ALSO  ·  Kenya\u2019s last Ebola patient goes home  ·  Haiti police kill "
         "34 gang suspects",
         font=TICKER, fill=RED)
pen.text((48, 960),
         "Germany rejects \u201cnew Yalta\u201d  ·  EU\u2013UK summit in Brussels  ·  "
         "Israel crosses Gaza line",
         font=TICKER, fill=RED)
pen.text((48, 988), "Sources: Reuters · AP · BBC · Al Jazeera  —  20 November 2026",
         font=FOOT, fill=GREY)

sheet.save("entry.png", format="PNG", optimize=True)
print("wrote entry.png", sheet.size)
