# modelgen — generátor 3D modelů do STL / OBJ

Malá knihovna v čistém Pythonu (bez závislostí) pro tvorbu trojúhelníkových
sítí a jejich export do binárního STL nebo OBJ. Výstup je určený pro 3D tisk
i pro import do Blenderu.

## Rychlý start

```bash
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

`modelgen/mesh.py` — třída `Mesh` s `translated`, `scaled`, `rotated_x/y/z`,
`extend`, `bounds`, `write_stl`, `write_obj`.

`modelgen/examples/` — `mug.py` (parametrický hrnek) a `gear.py`
(čelní ozubené kolo s otvorem pro hřídel).

## Omezení

- `extrude` a `revolve` triangulují víka vějířem ze středu, takže polygon musí
  být vůči svému těžišti hvězdicovitý. Obecné konkávní tvary potřebují
  plnohodnotnou triangulaci.
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
