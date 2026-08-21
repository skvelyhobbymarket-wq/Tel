"""Parametrické čelní ozubené kolo s lichoběžníkovými zuby a otvorem pro hřídel."""

from __future__ import annotations

import math

from mesh import Mesh
from primitives import ring_extrude


def gear(teeth: int = 20, module: float = 3.0, thickness: float = 8.0,
         bore: float = 8.0, tooth_ratio: float = 0.45) -> Mesh:
    """module = roztečný průměr / počet zubů. Rozměry v milimetrech."""
    if teeth < 6:
        raise ValueError("kolo potřebuje alespoň 6 zubů")
    pitch_r = module * teeth / 2.0
    outer_r = pitch_r + module
    root_r = pitch_r - 1.25 * module
    if bore >= 2 * root_r:
        raise ValueError("otvor pro hřídel je větší než pata zubů")

    polygon: list[tuple[float, float]] = []
    step = 2 * math.pi / teeth
    for t in range(teeth):
        base = t * step
        # čtyři body na zub: pata, náběh, hlava, výběh
        for frac, r in ((0.0, root_r), (tooth_ratio * 0.5, outer_r),
                        (tooth_ratio, outer_r), (0.5, root_r)):
            a = base + step * frac
            polygon.append((r * math.cos(a), r * math.sin(a)))

    # Otvor jako druhý obrys se stejným počtem bodů -> skutečně průchozí díra.
    n = len(polygon)
    hole = [(bore / 2.0 * math.cos(2 * math.pi * i / n),
             bore / 2.0 * math.sin(2 * math.pi * i / n)) for i in range(n)]
    return ring_extrude(polygon, hole, thickness)


if __name__ == "__main__":
    gear().write_stl("kolo.stl", name="ozubene_kolo")
