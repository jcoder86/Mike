# Daddy Mike

Gimmick-spel in één `index.html` (canvas, geen framework). Mike vangt overdag
poepluiers en 's nachts bier; elke 20 seconden wisselt dag/nacht.

## Lokaal draaien

```bash
python -m http.server 8765
```

Daarna staat het spel op `http://localhost:8765`. Met `#test` achter de URL ben
je onsterfelijk, handig om de nachtfase te bekijken.

## Deployen (Dokploy)

Draait op **mike.genapps.nl**. Dokploy bouwt rechtstreeks uit deze repo.

| Veld | Waarde |
|---|---|
| Source | GitHub, branch `main` |
| Build type | Dockerfile |
| Dockerfile path | `./Dockerfile` |
| Domain | `mike.genapps.nl` |
| Container port | `3013` |

Het image is `nginx:alpine` met alleen `index.html` en `assets/`. Nieuwe versie
uitrollen is een `git push` naar `main`.

Vervang je een beeld in `assets/`, hoog dan `VERSIE` op in `index.html`; de
assets worden een dag gecachet.

## Beelden opnieuw maken

`tools/gen.ps1` genereert de ruwe beelden (naar `raw/`, niet in git),
`tools/bouw_assets.py` haalt de groene achtergrond weg en schrijft naar
`assets/`, `tools/meet.py` controleert afmetingen en alfakanaal.
