"""Parametrický hrnek: rotační skořepina + ucho z výseče anuloidu."""

from __future__ import annotations

import math

from mesh import Mesh
from primitives import revolve


def mug(height: float = 95.0, radius: float = 40.0, wall: float = 3.0,
        floor: float = 4.0, handle_tube: float = 6.0, segments: int = 96) -> Mesh:
    """Rozměry v milimetrech. Profil jde vnější stěnou nahoru, přes okraj a vnitřkem dolů."""
    if wall <= 0 or floor <= 0 or wall >= radius:
        raise ValueError("neplatná tloušťka stěny nebo dna")
    profile = [
        (0.0, 0.0),                      # střed dna
        (radius, 0.0),                   # dno ven
        (radius, height),                # vnější stěna nahoru
        (radius - wall, height),         # okraj dovnitř
        (radius - wall, floor),          # vnitřní stěna dolů
        (0.0, floor),                    # vnitřní dno
    ]
    body = revolve(profile, segments=segments)
    return body.extend(_handle(height, radius, handle_tube, segments))


def _handle(height: float, radius: float, tube: float, segments: int) -> Mesh:
    """Otevřený oblouk anuloidu, oba konce zapuštěné do stěny hrnku."""
    arc_r = height * 0.30
    center_z = height * 0.55
    arc_segments = max(24, segments // 2)
    tube_segments = 24
    # Oblouk vede od stěny ven a zpět; přesah dovnitř stěny zajistí splynutí objemů.
    start, end = -math.pi / 2.2, math.pi / 2.2
    m = Mesh()
    grid = []
    for i in range(arc_segments + 1):
        t = start + (end - start) * i / arc_segments
        cx = radius - tube * 0.5 + arc_r * math.cos(t)
        cz = center_z + arc_r * math.sin(t)
        # tečna oblouku v rovině xz; kružnice trubky leží v rovině kolmé na ni
        tx, tz = -math.sin(t), math.cos(t)
        row = []
        for k in range(tube_segments):
            v = 2 * math.pi * k / tube_segments
            # normála v rovině xz + osa y dávají lokální bázi trubky
            nx, nz = tz, -tx
            row.append(m.add_vertex(cx + tube * math.cos(v) * nx,
                                    tube * math.sin(v),
                                    cz + tube * math.cos(v) * nz))
        grid.append(row)
    for i in range(arc_segments):
        for k in range(tube_segments):
            k2 = (k + 1) % tube_segments
            m.add_quad(grid[i][k], grid[i][k2], grid[i + 1][k2], grid[i + 1][k])
    # víčka na koncích, aby byl oblouk sám o sobě uzavřený
    for row, flip in ((grid[0], True), (grid[-1], False)):
        cx = sum(m.vertices[i][0] for i in row) / len(row)
        cy = sum(m.vertices[i][1] for i in row) / len(row)
        cz = sum(m.vertices[i][2] for i in row) / len(row)
        c = m.add_vertex(cx, cy, cz)
        for k in range(tube_segments):
            k2 = (k + 1) % tube_segments
            m.add_face(c, row[k2], row[k]) if flip else m.add_face(c, row[k], row[k2])
    return m


if __name__ == "__main__":
    mug().write_stl("hrnek.stl", name="hrnek")
