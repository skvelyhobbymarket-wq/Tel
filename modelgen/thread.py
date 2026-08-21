"""Vnitřní metrický závit modelovaný jako helikální plocha.

Poloměr vnitřní stěny je funkcí úhlu i výšky, r(θ, z), kde profil závitu
závisí na fázi (z - p·θ/2π)/p. Tím vznikne skutečná šroubovice bez nutnosti
booleovských operací — plocha se vygeneruje rovnou ve výsledné podobě.
"""

from __future__ import annotations

import math

from mesh import Mesh


def thread_radius(theta: float, z: float, major_r: float, pitch: float,
                  depth: float) -> float:
    """Poloměr vnitřní stěny závitu v daném úhlu a výšce.

    Profil je symetrický trojúhelník (metrický závit má vrcholový úhel 60°,
    ten je zde aproximovaný lineárními boky přes celou rozteč).
    """
    phase = ((z - pitch * theta / (2.0 * math.pi)) % pitch) / pitch
    # 0 -> dno drážky (velký poloměr), 0.5 -> vrchol zubu (malý poloměr)
    return major_r - depth * (1.0 - abs(2.0 * phase - 1.0))


def threaded_hole(major_d: float, pitch: float, depth_z: float,
                  segments: int = 96, steps_per_turn: int = 24,
                  thread_depth: float | None = None) -> tuple[Mesh, float]:
    """Slepá díra s vnitřním závitem, ústí v z=0, dno v z=depth_z.

    Vrací (síť, jmenovitý_poloměr). Síť obsahuje jen plášť závitu a dno —
    ústí zůstane otevřené, aby se dalo napojit na okolní těleso.
    """
    if pitch <= 0 or depth_z <= 0 or major_d <= 0:
        raise ValueError("neplatné parametry závitu")
    major_r = major_d / 2.0
    td = 0.613 * pitch if thread_depth is None else thread_depth
    if td >= major_r:
        raise ValueError("hloubka profilu je větší než poloměr závitu")

    rows = max(2, int(round(steps_per_turn * depth_z / pitch)) + 1)
    m = Mesh()
    grid: list[list[int]] = []
    for r_i in range(rows):
        z = depth_z * r_i / (rows - 1)
        row = []
        for s in range(segments):
            theta = 2.0 * math.pi * s / segments
            r = thread_radius(theta, z, major_r, pitch, td)
            row.append(m.add_vertex(r * math.cos(theta), r * math.sin(theta), z))
        grid.append(row)

    # Plášť: normála musí mířit do díry, tedy k ose.
    for a in range(rows - 1):
        for s in range(segments):
            s2 = (s + 1) % segments
            m.add_quad(grid[a][s2], grid[a][s], grid[a + 1][s], grid[a + 1][s2])

    # Dno díry: normála dolů, směrem z díry ven do materiálu.
    center = m.add_vertex(0.0, 0.0, depth_z)
    for s in range(segments):
        s2 = (s + 1) % segments
        m.add_face(center, grid[-1][s2], grid[-1][s])
    return m, major_r


def mouth_polygon(major_d: float, pitch: float, segments: int = 96,
                  thread_depth: float | None = None) -> list[tuple[float, float]]:
    """Obrys ústí závitu v z=0 — přesně sedí na horní řadu z `threaded_hole`."""
    major_r = major_d / 2.0
    td = 0.613 * pitch if thread_depth is None else thread_depth
    out = []
    for s in range(segments):
        theta = 2.0 * math.pi * s / segments
        r = thread_radius(theta, 0.0, major_r, pitch, td)
        out.append((r * math.cos(theta), r * math.sin(theta)))
    return out
