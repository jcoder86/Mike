"""Verwijder een egale #00FF00 (of #FF00FF) achtergrond en schrijf een transparante PNG.

Gebruik: python tools/chromakey.py raw/naam.png assets/naam.png [max_zijde]
"""
import sys

import numpy as np
from PIL import Image, ImageFilter


def chromakey(src, dst, max_side=None, crop=True, key="groen"):
    rgb = np.asarray(Image.open(src).convert("RGB")).astype(np.float32)
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]

    if key == "magenta":
        # Voor groene onderwerpen (het bierblikje): magenta achtergrond wegsleutelen.
        spil = np.minimum(np.minimum(r, b) - g, np.minimum(r, b) - 100.0)
        alpha = 1.0 - np.clip((spil - 25.0) / 85.0, 0.0, 1.0)
        rand = (alpha < 1.0) | (spil > 8.0)
        r = np.where(rand, np.minimum(r, g + 20.0), r)
        b = np.where(rand, np.minimum(b, g + 20.0), b)
    else:
        # Alleen fel groen telt, zodat donkergroen dekkend blijft.
        green = np.minimum(g - np.maximum(r, b), g - 100.0)
        lo, hi = 25.0, 110.0  # soft edge tussen deze drempels
        alpha = 1.0 - np.clip((green - lo) / (hi - lo), 0.0, 1.0)

        # Rand ontsmetten: groen nooit hoger dan het gemiddelde van rood en blauw
        # op (half)transparante en felgroenige pixels.
        spill = (alpha < 1.0) | (green > 8.0)
        g = np.where(spill, np.minimum(g, (r + b) / 2.0), g)

    out = np.dstack([r, g, b, alpha * 255.0]).clip(0, 255).astype(np.uint8)
    img = Image.fromarray(out, "RGBA")

    # Alfa een fractie krimpen en verzachten tegen een groen randje.
    a = img.getchannel("A").filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.8))
    img.putalpha(a)

    bbox = img.getbbox()
    if bbox and crop:
        img = img.crop(bbox)
    if max_side and max(img.size) > max_side:
        img.thumbnail((max_side, max_side), Image.LANCZOS)
    img.save(dst, optimize=True)

    a = np.asarray(img.getchannel("A"))
    print(f"{dst}: {img.size[0]}x{img.size[1]} mode={img.mode} "
          f"transparant={(a == 0).mean():.0%} dekkend={(a == 255).mean():.0%}")


if __name__ == "__main__":
    chromakey(sys.argv[1], sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else None)
