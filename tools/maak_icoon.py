"""Maak het app-icoon (Mike's hoofd + titel) en de favicons in assets/.

Gebruik: python tools/maak_icoon.py
"""
import math
import os

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = os.path.join(ROOT, "assets")
REGENBOOG = ["#ff3b6b", "#ff9a3b", "#ffe14a", "#35d6c4", "#4a8dff", "#b765ff", "#ff6fd0"]
S = 1024  # werkformaat; daarna verkleinen


def zonnestralen(grootte, midden):
    """Regenboog-stralen vanuit het midden, als een discozon."""
    img = Image.new("RGB", (grootte, grootte), "#1b1035")
    d = ImageDraw.Draw(img)
    n, r = 14, grootte * 1.5
    for i in range(n):
        a0, a1 = (i / n) * 360 - 90, ((i + 1) / n) * 360 - 90
        d.pieslice([midden[0] - r, midden[1] - r, midden[0] + r, midden[1] + r], a0, a1, fill=REGENBOOG[i % 7])
    return img


def hoofd():
    h = Image.open(os.path.join(A, "hoofd_blij.png")).convert("RGBA")
    return h.crop(h.getbbox())


def titel(img, regels, y, px):
    """Regenboogletters met dikke zwarte rand, per regel gecentreerd."""
    font = ImageFont.truetype(r"C:\Windows\Fonts\ariblk.ttf", px)
    d = ImageDraw.Draw(img)
    k = 0
    for regel in regels:
        breedte = d.textlength(regel, font=font)
        x = (img.width - breedte) / 2
        for letter in regel:
            kleur = "#ffffff" if letter == " " else REGENBOOG[k % 7]
            d.text((x, y), letter, font=font, fill=kleur, stroke_width=px // 7, stroke_fill="#000000")
            x += d.textlength(letter, font=font)
            k += letter != " "
        y += px * 0.98


# --- groot icoon: beginscherm ---------------------------------------------
icoon = zonnestralen(S, (S // 2, int(S * 0.42)))
# donkere band onderin, zodat de titel leesbaar blijft
band = Image.new("RGBA", (S, S), (0, 0, 0, 0))
ImageDraw.Draw(band).rectangle([0, int(S * 0.70), S, S], fill=(27, 16, 53, 235))
icoon = Image.alpha_composite(icoon.convert("RGBA"), band)

h = hoofd()
hh = int(S * 0.70)
h = h.resize((int(h.width * hh / h.height), hh), Image.LANCZOS)
schaduw = Image.new("RGBA", icoon.size, (0, 0, 0, 0))
schaduw.paste((0, 0, 0, 150), ((S - h.width) // 2 + 14, int(S * 0.045) + 18), h.getchannel("A"))
icoon = Image.alpha_composite(icoon, schaduw.filter(ImageFilter.GaussianBlur(14)))
icoon.alpha_composite(h, ((S - h.width) // 2, int(S * 0.045)))
titel(icoon, ["DADDY MIKE"], int(S * 0.755), 120)

icoon = icoon.convert("RGB")
for maat, naam in ((512, "icon-512.png"), (192, "icon-192.png"), (180, "apple-touch-icon.png")):
    icoon.resize((maat, maat), Image.LANCZOS).save(os.path.join(A, naam), optimize=True)
    print(naam, maat)

# --- favicon: alleen het hoofd, de titel is op 32px toch niet te lezen ------
F = 256
fav = Image.new("RGBA", (F, F), (0, 0, 0, 0))
rond = zonnestralen(F, (F // 2, F // 2)).convert("RGBA")
masker = Image.new("L", (F, F), 0)
ImageDraw.Draw(masker).ellipse([2, 2, F - 3, F - 3], fill=255)
fav.paste(rond, (0, 0), masker)
h = hoofd()
hh = int(F * 0.94)
h = h.resize((int(h.width * hh / h.height), hh), Image.LANCZOS)
fav.alpha_composite(h, ((F - h.width) // 2, (F - hh) // 2))
fav.resize((64, 64), Image.LANCZOS).save(os.path.join(A, "favicon.png"), optimize=True)
fav.save(os.path.join(ROOT, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)])
print("favicon.png 64, favicon.ico 16/32/48")
