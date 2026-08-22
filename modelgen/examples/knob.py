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


def outline_radius(angle: float, outer_d: float, root_d: float, lobes: int = 8) -> float:
    """Poloměr hvězdicového obrysu v daném úhlu — stejný předpis jako `star_outline`."""
    mid = (outer_d + root_d) / 4.0
    amp = (outer_d - root_d) / 4.0
    return mid + amp * math.cos(lobes * angle)


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


def knob(outer_d: float = 75.0, root_d: float = 57.5, height: float = 26.0,
         lobes: int = 8, pockets: int = 8, pocket_d: float = 9.4,
         pocket_circle_d: float = 55.0, pocket_depth: float = 22.0,
         thread_d: float = 24.0, pitch: float = 3.0, thread_depth: float = 22.0,
         recess_d: float = 52.5, recess_depth: float = 1.5,
         dot_d: float = 2.4, dot_depth: float = 0.8,
         boss_d: float = 42.0, boss_h: float = 4.0, min_wall: float = 0.8,
         segments: int = 64) -> Mesh:
    """Sestaví kolečko jako jedno vodotěsné těleso. Nejnižší bod leží v z=0.

    Pohledová strana není plochá: je v ní kruhové vybrání (`recess_d`,
    `recess_depth`) a uprostřed jeho dna malý důlek (`dot_d`, `dot_depth`).
    Obojí je čistě pohledové — nulová hloubka příslušný prvek vypne.
    Závitový nálitek (`boss_d`, `boss_h`) vystupuje pod tělo hvězdice, takže
    celková výška dílu je `height + boss_h`. Závit začíná na čele nálitku.
    """
    if boss_h < 0:
        raise ValueError("výška nálitku nesmí být záporná")
    if boss_h > 0 and boss_d <= thread_d:
        raise ValueError("nálitek musí být širší než závit")
    if boss_h > 0 and boss_d / 2.0 > pocket_circle_d / 2.0 - pocket_d / 2.0 - min_wall:
        raise ValueError(
            f"mezi nálitkem a kapsami by zbylo méně než {min_wall} mm materiálu")
    if pocket_depth >= height:
        raise ValueError("kapsy nesmí prorazit horní čelo")
    if thread_depth >= height + boss_h:
        raise ValueError("závit nesmí prorazit horní čelo")
    # Kapsy smí zasahovat za patu zářezů, pokud leží v cípu. Rozhoduje tedy
    # skutečný poloměr obrysu v místě kapsy, ne poloměr paty.
    for i in range(pockets):
        a = 2 * math.pi * i / pockets
        cx = pocket_circle_d / 2.0 * math.cos(a)
        cy = pocket_circle_d / 2.0 * math.sin(a)
        # nejtěsnější místo hledej po obvodu kapsy, ne jen v jejím středu
        for k in range(72):
            b = 2 * math.pi * k / 72
            px = cx + pocket_d / 2.0 * math.cos(b)
            py = cy + pocket_d / 2.0 * math.sin(b)
            r = math.hypot(px, py)
            if r + min_wall >= outline_radius(math.atan2(py, px), outer_d, root_d, lobes):
                raise ValueError(
                    f"kapsa {i + 1} se přibližuje k obvodu na méně než {min_wall} mm")
    if pocket_circle_d / 2.0 - pocket_d / 2.0 - min_wall <= thread_d / 2.0:
        raise ValueError(
            f"mezi kapsami a závitem by zbylo méně než {min_wall} mm materiálu")
    if recess_depth < 0 or dot_depth < 0:
        raise ValueError("hloubka vybrání ani důlku nesmí být záporná")
    if recess_depth > 0 and recess_d >= root_d:
        raise ValueError("vybrání musí být menší než průměr v zářezech")
    if dot_depth > 0 and recess_depth > 0 and dot_d >= recess_d:
        raise ValueError("důlek musí být menší než vybrání")
    # Vybrání shora a kapsy zdola si nesmí prorazit navzájem.
    if height - recess_depth - dot_depth <= max(pocket_depth, thread_depth - boss_h):
        raise ValueError("vybrání a kapsy se protínají — chybí materiál mezi nimi")

    outline = star_outline(outer_d, root_d, lobes)
    mouth = mouth_polygon(thread_d, pitch, segments=segments)
    pocket_loops = [_circle(pocket_d / 2.0, segments // 2,
                            pocket_circle_d / 2.0 * math.cos(2 * math.pi * i / pockets),
                            pocket_circle_d / 2.0 * math.sin(2 * math.pi * i / pockets))
                    for i in range(pockets)]

    m = Mesh()
    _wall(m, outline, 0.0, height)                            # obvod hvězdice

    if boss_h > 0:
        # Závitový nálitek vystupuje pod tělo; závit ústí až na jeho čele.
        boss_loop = _circle(boss_d / 2.0, segments)
        _cap(m, outline, pocket_loops + [boss_loop], 0.0, up=False)
        _wall(m, boss_loop, -boss_h, 0.0)
        _cap(m, boss_loop, [mouth], -boss_h, up=False)
        thread_z0 = -boss_h
    else:
        _cap(m, outline, pocket_loops + [mouth], 0.0, up=False)
        thread_z0 = 0.0

    if recess_depth > 0:
        # Pohledové vybrání: čelo hvězdice je mezikruží, kotouč je zapuštěný.
        recess_loop = _circle(recess_d / 2.0, segments)
        floor_z = height - recess_depth
        _cap(m, outline, [recess_loop], height, up=True)      # obruba kolem vybrání
        _wall(m, list(reversed(recess_loop)), floor_z, height)  # stěna vybrání, normála dovnitř

        if dot_depth > 0:
            # Důlek uprostřed dna vybrání.
            dot_loop = _circle(dot_d / 2.0, max(12, segments // 4))
            _cap(m, recess_loop, [dot_loop], floor_z, up=True)
            _wall(m, list(reversed(dot_loop)), floor_z - dot_depth, floor_z)
            _cap(m, dot_loop, None, floor_z - dot_depth, up=True)
        else:
            _cap(m, recess_loop, None, floor_z, up=True)      # hladké dno vybrání
    else:
        _cap(m, outline, None, height, up=True)               # ploché horní čelo

    for loop in pocket_loops:                                 # slepé kapsy
        _wall(m, list(reversed(loop)), 0.0, pocket_depth)
        _cap(m, loop, None, pocket_depth, up=False)           # strop kapsy míří dolů

    hole, _ = threaded_hole(thread_d, pitch, thread_depth, segments=segments)
    m.extend(hole.translated(dz=thread_z0))
    return m.translated(dz=-thread_z0)   # nejnižší bod dílu na z=0


if __name__ == "__main__":
    knob().write_stl("kolecko.stl", name="kolecko_lehatko")
