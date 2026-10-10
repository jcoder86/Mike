"""Zet alle ruwe generaties (raw/) om naar spelklare bestanden in assets/.

Gebruik: python tools/bouw_assets.py
"""
import os

from PIL import Image

from chromakey import chromakey

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
raw = lambda n: os.path.join(ROOT, "raw", n)
out = lambda n: os.path.join(ROOT, "assets", n)

# Hoofden niet bijsnijden: zo houden de drie varianten hetzelfde kader.
for naam in ("hoofd_neutraal", "hoofd_blij", "hoofd_vies"):
    chromakey(raw(naam + ".png"), out(naam + ".png"), 512, crop=False)
chromakey(raw("lijf.png"), out("lijf.png"), 640)
for naam in ("poepluier", "gouden_glitterluier", "bierblikje", "salmari"):
    chromakey(raw(naam + ".png"), out(naam + ".png"), 256)

# Achtergrond: midden uitsnijden naar 9:16 en als JPG opslaan.
bg = Image.open(raw("achtergrond_dag.png")).convert("RGB")
w, h = bg.size
if w / h > 9 / 16:
    nw = round(h * 9 / 16)
    bg = bg.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
else:
    nh = round(w * 16 / 9)
    bg = bg.crop((0, h - nh, w, h))
bg = bg.resize((720, 1280), Image.LANCZOS)
bg.save(out("achtergrond_dag.jpg"), quality=86, optimize=True, progressive=True)
print(f"{out('achtergrond_dag.jpg')}: {bg.size[0]}x{bg.size[1]} (bron {w}x{h})")
