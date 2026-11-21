#!/usr/bin/env python3
"""Draw the entry image: the world news of Friday 20 November 2026 in one picture.

A dark broadsheet-style infographic composed with Pillow: every word is real,
spelled text — no generated imagery, no garbled lettering.
Run:  python3 draw_image.py
Writes entry.png (1024 x 1024) next to this file, deterministically.
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
INK_BG = (13, 17, 28)
CARD = (24, 31, 48)
CARD_ALT = (19, 25, 40)
CREAM = (243, 236, 222)
WHITE = (255, 255, 255)
PALE = (169, 179, 199)
AMBER = (233, 178, 76)
CRIMSON = (224, 92, 70)
TEAL = (84, 186, 178)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def F(name, size):
    return ImageFont.truetype(f"{FONT_DIR}/{name}", size)


F_MAST = F("DejaVuSerif-Bold.ttf", 58)
F_DATE = F("DejaVuSans-Bold.ttf", 30)
F_LK = F("DejaVuSans-Bold.ttf", 20)
F_LH = F("DejaVuSerif-Bold.ttf", 42)
F_LB = F("DejaVuSans.ttf", 24)
F_KICK = F("DejaVuSans-Bold.ttf", 18)
F_HEAD = F("DejaVuSans-Bold.ttf", 27)
F_BODY = F("DejaVuSans.ttf", 21)
F_TICK = F("DejaVuSans-Bold.ttf", 20)
F_FOOT = F("DejaVuSans.ttf", 16)


def wrapped(draw, text, fnt, width):
    out, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                out.append(cur)
            cur = word
    if cur:
        out.append(cur)
    return out


img = Image.new("RGB", (W, H), INK_BG)
d = ImageDraw.Draw(img)

# ---- masthead ----
d.text((48, 34), "THE WORLD TODAY", font=F_MAST, fill=CREAM)
d.text((48, 104), "FRIDAY 20 NOVEMBER 2026", font=F_DATE, fill=AMBER)
d.line([(48, 152), (976, 152)], fill=AMBER, width=3)

# ---- lead story ----
d.rounded_rectangle([48, 176, 976, 470], radius=14, fill=CARD)
d.rectangle([48, 176, 62, 470], fill=CRIMSON)
d.text((84, 196), "UKRAINE  ·  OVERNIGHT BARRAGE", font=F_LK, fill=CRIMSON)
d.text((84, 226), "Kyiv\u2019s bridges hit in huge barrage", font=F_LH, fill=WHITE)
lead_body = ("Russia fired 84 cruise missiles and 404 drones in one of the war\u2019s "
             "largest air attacks, striking three bridges over the Dnipro and knocking "
             "out power and heat. Missiles also fell inside Poland; Kyiv officials "
             "report at least eight dead and 28 injured.")
y = 292
for line in wrapped(d, lead_body, F_LB, 976 - 84 - 36):
    d.text((84, y), line, font=F_LB, fill=CREAM)
    y += 32
d.text((84, 420), "THE DAY\u2019S BIGGEST STORY", font=F_KICK, fill=PALE)

# ---- 2 x 2 grid ----
panels = [
    ("RIYADH", "Missile hits PIF Tower",
     "A Houthi missile blew out windows across seven floors of Riyadh\u2019s tallest "
     "tower. No injuries reported; more attacks were intercepted on Friday.",
     AMBER),
    ("ODISHA, INDIA", "Cyclone Akvan landfall",
     "Landfall near Gopalpur, winds gusting to 90 km/h, after more than 300,000 "
     "people were evacuated. It weakened fast; no deaths in early assessments.",
     TEAL),
    ("MARKETS", "AI sell-off deepens",
     "Anthropic slid after its record debut as the AI trade unwound: Taiwan\u2019s "
     "Taiex fell 6.2%, SoftBank dropped over 14% and the Nikkei lost 4.8%.",
     AMBER),
    ("COP31", "Draft drops phase-out",
     "The summit draft no longer calls for phasing out fossil fuels, drawing fire "
     "from island states as the talks near their deadline.",
     TEAL),
]
gx, gy, cw, ch, gap = 48, 494, 452, 196, 24
for i, (kick, head, text, accent) in enumerate(panels):
    x = gx + (i % 2) * (cw + gap)
    y0 = gy + (i // 2) * (ch + gap)
    d.rounded_rectangle([x, y0, x + cw, y0 + ch], radius=12, fill=CARD_ALT)
    d.rectangle([x, y0, x + 6, y0 + ch], fill=accent)
    d.text((x + 24, y0 + 14), kick, font=F_KICK, fill=accent)
    d.text((x + 24, y0 + 40), head, font=F_HEAD, fill=WHITE)
    yy = y0 + 82
    for line in wrapped(d, text, F_BODY, cw - 48):
        d.text((x + 24, yy), line, font=F_BODY, fill=PALE)
        yy += 27

# ---- ticker (two lines, so nothing is cut off) ----
d.rectangle([0, 918, W, 920], fill=AMBER)
tick1 = ("ALSO  ·  Kenya\u2019s last Ebola patient goes home  ·  Haiti police kill "
         "34 gang suspects")
tick2 = ("Germany rejects \u201cnew Yalta\u201d  ·  EU\u2013UK summit in Brussels  ·  "
         "Israel crosses Gaza line")
d.text((48, 926), tick1, font=F_TICK, fill=AMBER)
d.text((48, 954), tick2, font=F_TICK, fill=AMBER)
d.text((48, 986), "Sources: Reuters · AP · BBC · Al Jazeera  —  20 November 2026",
       font=F_FOOT, fill=PALE)

img.save("entry.png", format="PNG", optimize=True)
print("wrote entry.png", img.size)
