"""Ovládací hvězdicové kolečko k rozkládacímu lehátku.

Osmilaločné kolečko s uzavřeným horním čelem, prstencem odlehčovacích kapes
ze spodní strany a vnitřním závitem uprostřed. Všechny rozměry v milimetrech.

POZOR: výchozí rozměry jsou odhad z fotografie, ne měření. Před tiskem je
potřeba zadat skutečné hodnoty — hlavně `thread_d`, `pitch` a `outer_d`.
"""

from __future__ import annotations

import math

from mesh import Mesh
from thread import mouth_polygon, threaded_hole
from triangulate import triangulate


def star_outline(outer_d: float, root_d: float, lobes: int = 8,
                 segments_per_lobe: int = 24) -> list[tuple[float, float]]:
    """Zaoblený hvězdicový obrys: poloměr kolísá kosinusově mezi patou a lalokem."""
    if root_d >= outer_d:
        raise ValueError("průměr paty musí být menší než průměr přes laloky")
    r_max, r_min = outer_d / 2.0, root_d / 2.0
    mid, amp = (r_max + r_min) / 2.0, (r_max - r_min) / 2.0
    n = lobes * segments_per_lobe
    return [((mid + amp * math.cos(lobes * 2 * math.pi * i / n)) * math.cos(2 * math.pi * i / n),
             (mid + amp * math.cos(lobes * 2 * math.pi * i / n)) * math.sin(2 * math.pi * i / n))
            for i in range(n)]


def _circle(r: float, n: int, cx: float = 0.0, cy: float = 0.0) -> list[tuple[float, float]]:
    return [(cx + r * math.cos(2 * math.pi * i / n), cy + r * math.sin(2 * math.pi * i / n))
            for i in range(n)]


def _cap(mesh: Mesh, outline, holes, z: float, up: bool) -> None:
    pts, tris = triangulate(outline, holes)
    idx = [mesh.add_vertex(x, y, z) for x, y in pts]
    for a, b, c in tris:
        mesh.add_face(idx[a], idx[b], idx[c]) if up else mesh.add_face(idx[c], idx[b], idx[a])


def _wall(mesh: Mesh, loop, z0: float, z1: float) -> None:
    """Smyčka proti směru hodinových ručiček dá normálu ven, po směru dovnitř."""
    b = [mesh.add_vertex(x, y, z0) for x, y in loop]
    t = [mesh.add_vertex(x, y, z1) for x, y in loop]
    for i in range(len(loop)):
        j = (i + 1) % len(loop)
        mesh.add_quad(b[i], b[j], t[j], t[i])


def knob(outer_d: float = 60.0, root_d: float = 46.0, height: float = 20.0,
         lobes: int = 8, pockets: int = 7, pocket_d: float = 9.0,
         pocket_circle_d: float = 34.0, pocket_depth: float = 13.0,
         thread_d: float = 12.0, pitch: float = 1.75, thread_depth: float = 14.0,
         segments: int = 64) -> Mesh:
    """Sestaví kolečko jako jedno vodotěsné těleso. Spodní čelo leží v z=0."""
    if pocket_depth >= height or thread_depth >= height:
        raise ValueError("kapsy ani závit nesmí prorazit horní čelo")
    if pocket_circle_d / 2.0 + pocket_d / 2.0 >= root_d / 2.0:
        raise ValueError("kapsy zasahují mimo patu laloků")
    if pocket_circle_d / 2.0 - pocket_d / 2.0 <= thread_d / 2.0:
        raise ValueError("kapsy zasahují do závitu")

    outline = star_outline(outer_d, root_d, lobes)
    mouth = mouth_polygon(thread_d, pitch, segments=segments)
    pocket_loops = [_circle(pocket_d / 2.0, segments // 2,
                            pocket_circle_d / 2.0 * math.cos(2 * math.pi * i / pockets),
                            pocket_circle_d / 2.0 * math.sin(2 * math.pi * i / pockets))
                    for i in range(pockets)]

    m = Mesh()
    _cap(m, outline, pocket_loops + [mouth], 0.0, up=False)   # spodní čelo s otvory
    _cap(m, outline, None, height, up=True)                   # uzavřené horní čelo
    _wall(m, outline, 0.0, height)                            # obvod hvězdice

    for loop in pocket_loops:                                 # slepé kapsy
        _wall(m, list(reversed(loop)), 0.0, pocket_depth)
        _cap(m, loop, None, pocket_depth, up=False)           # strop kapsy míří dolů

    hole, _ = threaded_hole(thread_d, pitch, thread_depth, segments=segments)
    m.extend(hole)
    return m


if __name__ == "__main__":
    knob().write_stl("kolecko.stl", name="kolecko_lehatko")
