# modelgen — generátor 3D modelů do STL / OBJ

Malá knihovna v čistém Pythonu (bez závislostí) pro tvorbu trojúhelníkových
sítí a jejich export do binárního STL nebo OBJ. Výstup je určený pro 3D tisk
i pro import do Blenderu.

## Rychlý start

```bash
python3 modelgen/cli.py knob --out out/kolecko.stl --preview out/kolecko.png
python3 modelgen/cli.py mug  --out out/hrnek.stl
python3 modelgen/cli.py gear --teeth 24 --module 2.5 --out out/kolo.stl
python3 modelgen/cli.py sphere --radius 20 --out out/koule.obj
```

Rozměry jsou v milimetrech.

## Použití jako knihovna

```python
import sys; sys.path.insert(0, "modelgen")
from mesh import Mesh
from primitives import box, cylinder, sphere, revolve

model = Mesh()
model.extend(box(40, 40, 10))
model.extend(cylinder(8, 30).translated(dx=20, dy=20, dz=10))
model.write_stl("out/podstavec.stl")
```

## Co je k dispozici

`modelgen/primitives.py`

| funkce | popis |
| --- | --- |
| `box(w, d, h, centered=False)` | kvádr |
| `cylinder(r, h, segments, radius_top=None)` | válec nebo komolý kužel |
| `cone(r, h, segments)` | kužel s hrotem |
| `sphere(r, segments, rings)` | UV koule |
| `torus(r, tube, ...)` | anuloid |
| `extrude(polygon, h)` | vytažení polygonu (v rovině xy) |
| `ring_extrude(outer, inner, h)` | vytažení mezikruží — průchozí otvor |
| `revolve(profile, segments)` | rotace profilu `[(r, z), ...]` kolem osy z |
| `prism(outer, holes, h)` | vytažení obecného (i konkávního) obrysu s otvory |

`modelgen/triangulate.py` — triangulace polygonu s otvory ořezáváním uší.

`modelgen/thread.py` — `threaded_hole()` generuje slepou díru se skutečným
vnitřním metrickým závitem jako helikální plochu, bez booleovských operací.

`modelgen/preview.py` — `render()` vykreslí síť do PNG (z-buffer, jen stdlib),
takže jde tvar zkontrolovat bez sliceru.

`modelgen/mesh.py` — třída `Mesh` s `translated`, `scaled`, `rotated_x/y/z`,
`extend`, `bounds`, `write_stl`, `write_obj`.

`modelgen/examples/`

- `knob.py` — ovládací hvězdicové kolečko k rozkládacímu lehátku: 8 laloků,
  uzavřené horní čelo se zapuštěným pohledovým kotoučem a tečkou uprostřed,
  prstenec odlehčovacích kapes ze spodní strany a vnitřní závit M24.
- `mug.py` — parametrický hrnek
- `gear.py` — čelní ozubené kolo s otvorem pro hřídel

### Kolečko k lehátku

```bash
python3 modelgen/cli.py knob \
  --outer-d 75 --root-d 57.5 --knob-height 26 \
  --pockets 7 --pocket-d 9.4 --pocket-circle-d 40 --pocket-depth 22 \
  --thread-d 24 --pitch 3.0 --thread-depth 22 \
  --recess-d 52.5 --recess-depth 1.5 --dot-d 2.4 --dot-depth 0.8 \
  --out out/kolecko.stl --preview out/kolecko.png
```

Změřené na dílu: průměr přes cípy hvězdy 75 mm, závit M24 (stoupání 3,0),
hloubka závitu i kapes 22 mm, průměr kapes 9,4 mm.

Odhadnuté a zatím neověřené: výška těla (26 mm — musí být větší než hloubka
závitu), průměr v zářezech, rozteč kapes, průměr a hloubka vybrání i tečky.

Zapuštěný kotouč na pohledové straně (`--recess-d`, `--recess-depth`) a tečka
uprostřed (`--dot-d`, `--dot-depth`) jsou čistě designové; nulová hloubka je
vypne. Celková výška dílu je `--knob-height`, vybrání ji nemění.

## Omezení

- `extrude` a `revolve` triangulují víka vějířem ze středu, takže polygon musí
  být vůči svému těžišti hvězdicovitý. Obecné konkávní tvary potřebují
  plnohodnotnou triangulaci.
- `extrude` zůstává pro rychlé konvexní tvary; obecné obrysy patří do `prism`.
- Závit má rovné boky přes celou rozteč, ne normovaný profil s vrcholovým
  úhlem 60° a zaoblením paty. Pro pohyblivý spoj je to dostatečné, ne však
  pro díl přenášející jmenovité zatížení podle normy.
- `extend` sítě jen spojí, neprovádí booleovské operace. Překrývající se tělesa
  (např. ucho hrnku) slicer sjednotí sám, ale odečítání není podporované —
  díry je potřeba modelovat rovnou, jako to dělá `ring_extrude`.
- Polygonové obrysy se očekávají proti směru hodinových ručiček; při opačném
  pořadí budou normály mířit dovnitř.

## Testy

```bash
python3 modelgen/test_mesh.py
```

Testy kontrolují to, na čem stojí použitelnost STL: že je každé těleso
vodotěsné (každá hrana sdílená přesně dvěma trojúhelníky v opačném směru),
že normály míří ven (kladný znaménkový objem) a že objemy sedí s analytickými
vzorci.
