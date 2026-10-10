"""Controleer de assets (afmetingen, alfakanaal) en meet de maten die index.html nodig heeft.

Gebruik: python tools/meet.py
"""
import os

import numpy as np
from PIL import Image

A = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")


def alfa(naam):
    im = Image.open(os.path.join(A, naam))
    a = np.asarray(im.convert("RGBA").getchannel("A")) > 128
    kb = os.path.getsize(os.path.join(A, naam)) // 1024
    print(f"{naam}: {im.size[0]}x{im.size[1]} mode={im.mode} alfa={'ja' if im.mode == 'RGBA' else 'NEE'} "
          f"transparant={1 - a.mean():.0%} {kb} kB")
    return a


def runs(kolom):
    """Aaneengesloten dekkende stukken in een kolom, als (start, eind)-fracties."""
    uit, start = [], None
    for i, v in enumerate(list(kolom) + [False]):
        if v and start is None:
            start = i
        elif not v and start is not None:
            uit.append((round(start / len(kolom), 3), round(i / len(kolom), 3)))
            start = None
    return [r for r in uit if r[1] - r[0] > 0.01]


for naam in ("hoofd_neutraal.png", "hoofd_blij.png", "hoofd_vies.png"):
    a = alfa(naam)
    h, w = a.shape
    rijen = np.where(a.any(axis=1))[0]
    top, onder = rijen[0], rijen[-1]
    # breedste rij in de bovenste 60% van het hoofd = gezicht incl. oren (hand telt niet mee)
    stuk = a[top:top + int((onder - top) * 0.6)]
    breedtes = stuk.sum(axis=1)
    rij = stuk[breedtes.argmax()]
    xs = np.where(rij)[0]
    print(f"   b={(xs[-1] - xs[0]) / w:.3f} cx={(xs[0] + xs[-1]) / 2 / w:.3f} top={top / h:.3f} onder={onder / h:.3f}")

a = alfa("lijf.png")
h, w = a.shape
print(f"   aspect={w / h:.3f}")
for fx in (0.35, 0.5, 0.65):
    print(f"   kolom {fx}: dekkend {runs(a[:, int(w * fx)])}")
for fy in (0.03, 0.08, 0.13, 0.18, 0.25, 0.4, 0.55, 0.7, 0.85):
    print(f"   rij {fy}: dekkend {runs(a[int(h * fy), :])}")

for naam in ("poepluier.png", "gouden_glitterluier.png", "bierblikje.png", "salmari.png"):
    alfa(naam)

im = Image.open(os.path.join(A, "achtergrond_dag.jpg"))
print(f"achtergrond_dag.jpg: {im.size[0]}x{im.size[1]} mode={im.mode} verhouding={im.size[0] / im.size[1]:.3f} "
      f"{os.path.getsize(os.path.join(A, 'achtergrond_dag.jpg')) // 1024} kB")
