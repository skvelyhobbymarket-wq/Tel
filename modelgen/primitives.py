"""Základní tělesa a rotační/vytahovací operace nad Mesh."""

from __future__ import annotations

import math

from mesh import Mesh


def box(width: float, depth: float, height: float, centered: bool = False) -> Mesh:
    """Kvádr. Bez centered leží rohem v počátku a roste do +x/+y/+z."""
    m = Mesh()
    x0, y0, z0 = (-width / 2, -depth / 2, -height / 2) if centered else (0.0, 0.0, 0.0)
    x1, y1, z1 = x0 + width, y0 + depth, z0 + height
    for z in (z0, z1):
        for y in (y0, y1):
            for x in (x0, x1):
                m.add_vertex(x, y, z)
    # indexy: bit0 = x1, bit1 = y1, bit2 = z1
    m.add_quad(0, 2, 3, 1)  # spodek (normála -z)
    m.add_quad(4, 5, 7, 6)  # vršek
    m.add_quad(0, 1, 5, 4)  # y0
    m.add_quad(2, 6, 7, 3)  # y1
    m.add_quad(0, 4, 6, 2)  # x0
    m.add_quad(1, 3, 7, 5)  # x1
    return m


def cylinder(radius: float, height: float, segments: int = 48, radius_top: float | None = None) -> Mesh:
    """Válec (nebo komolý kužel při radius_top) podél osy z, podstavou v z=0."""
    radius_top = radius if radius_top is None else radius_top
    m = Mesh()
    bottom = [m.add_vertex(radius * math.cos(2 * math.pi * i / segments),
                           radius * math.sin(2 * math.pi * i / segments), 0.0)
              for i in range(segments)]
    top = [m.add_vertex(radius_top * math.cos(2 * math.pi * i / segments),
                        radius_top * math.sin(2 * math.pi * i / segments), height)
           for i in range(segments)]
    cb = m.add_vertex(0.0, 0.0, 0.0)
    ct = m.add_vertex(0.0, 0.0, height)
    for i in range(segments):
        j = (i + 1) % segments
        m.add_quad(bottom[i], bottom[j], top[j], top[i])
        m.add_face(cb, bottom[j], bottom[i])
        m.add_face(ct, top[i], top[j])
    return m


def cone(radius: float, height: float, segments: int = 48) -> Mesh:
    """Kužel s hrotem — komolý kužel s nulovým horním poloměrem by dal degenerované trojúhelníky."""
    m = Mesh()
    ring = [m.add_vertex(radius * math.cos(2 * math.pi * i / segments),
                         radius * math.sin(2 * math.pi * i / segments), 0.0)
            for i in range(segments)]
    apex = m.add_vertex(0.0, 0.0, height)
    center = m.add_vertex(0.0, 0.0, 0.0)
    for i in range(segments):
        j = (i + 1) % segments
        m.add_face(ring[i], ring[j], apex)
        m.add_face(center, ring[j], ring[i])
    return m


def sphere(radius: float, segments: int = 48, rings: int = 24) -> Mesh:
    """UV koule se středem v počátku; póly jsou samostatné vrcholy."""
    m = Mesh()
    grid = []
    for r in range(1, rings):
        phi = math.pi * r / rings
        row = [m.add_vertex(radius * math.sin(phi) * math.cos(2 * math.pi * i / segments),
                            radius * math.sin(phi) * math.sin(2 * math.pi * i / segments),
                            radius * math.cos(phi))
               for i in range(segments)]
        grid.append(row)
    north = m.add_vertex(0.0, 0.0, radius)
    south = m.add_vertex(0.0, 0.0, -radius)
    for i in range(segments):
        j = (i + 1) % segments
        m.add_face(north, grid[0][i], grid[0][j])
        m.add_face(south, grid[-1][j], grid[-1][i])
        for r in range(len(grid) - 1):
            m.add_quad(grid[r][i], grid[r + 1][i], grid[r + 1][j], grid[r][j])
    return m


def torus(radius: float, tube: float, segments: int = 64, tube_segments: int = 32) -> Mesh:
    m = Mesh()
    grid = []
    for i in range(segments):
        u = 2 * math.pi * i / segments
        row = []
        for k in range(tube_segments):
            v = 2 * math.pi * k / tube_segments
            r = radius + tube * math.cos(v)
            row.append(m.add_vertex(r * math.cos(u), r * math.sin(u), tube * math.sin(v)))
        grid.append(row)
    for i in range(segments):
        i2 = (i + 1) % segments
        for k in range(tube_segments):
            k2 = (k + 1) % tube_segments
            m.add_quad(grid[i][k], grid[i2][k], grid[i2][k2], grid[i][k2])
    return m


def extrude(polygon: list[tuple[float, float]], height: float) -> Mesh:
    """Vytažení konvexního nebo hvězdicovitého polygonu (v rovině xy) do výšky.

    Víko a dno se triangulují vějířem ze středu, takže polygon musí být
    vůči svému těžišti hvězdicovitý; pro obecné konkávní tvary je potřeba
    plnohodnotná triangulace.
    """
    if len(polygon) < 3:
        raise ValueError("polygon potřebuje alespoň 3 body")
    m = Mesh()
    n = len(polygon)
    bottom = [m.add_vertex(x, y, 0.0) for x, y in polygon]
    top = [m.add_vertex(x, y, height) for x, y in polygon]
    cx = sum(p[0] for p in polygon) / n
    cy = sum(p[1] for p in polygon) / n
    cb = m.add_vertex(cx, cy, 0.0)
    ct = m.add_vertex(cx, cy, height)
    for i in range(n):
        j = (i + 1) % n
        m.add_quad(bottom[i], bottom[j], top[j], top[i])
        m.add_face(cb, bottom[j], bottom[i])
        m.add_face(ct, top[i], top[j])
    return m


def revolve(profile: list[tuple[float, float]], segments: int = 64) -> Mesh:
    """Rotace profilu [(r, z), ...] kolem osy z.

    Body s r == 0 se sloučí do jediného vrcholu na ose, aby na hrotech
    nevznikly degenerované trojúhelníky. Profil se neuzavírá — konce
    s r > 0 nechají model otevřený, což je záměr pro skořepiny.
    """
    m = Mesh()
    rows: list[list[int]] = []
    for r, z in profile:
        if abs(r) < 1e-12:
            axis = m.add_vertex(0.0, 0.0, z)
            rows.append([axis] * segments)
        else:
            rows.append([m.add_vertex(r * math.cos(2 * math.pi * i / segments),
                                      r * math.sin(2 * math.pi * i / segments), z)
                         for i in range(segments)])
    for a in range(len(rows) - 1):
        for i in range(segments):
            j = (i + 1) % segments
            va, vb = rows[a][i], rows[a][j]
            wa, wb = rows[a + 1][i], rows[a + 1][j]
            if va == vb:            # spodní řada je na ose -> trojúhelník
                m.add_face(va, wb, wa)
            elif wa == wb:          # horní řada je na ose
                m.add_face(va, vb, wa)
            else:
                m.add_quad(va, vb, wb, wa)
    return m


def ring_extrude(outer: list[tuple[float, float]], inner: list[tuple[float, float]],
                 height: float) -> Mesh:
    """Vytažení mezikruží: skutečný průchozí otvor, ne jen obrácené normály.

    Oba obrysy musí být proti směru hodinových ručiček a mít stejný počet bodů,
    aby si víko a dno odpovídaly bod po bodu. Vnitřní obrys musí ležet celý
    uvnitř vnějšího.
    """
    if len(outer) != len(inner):
        raise ValueError("obrysy musí mít stejný počet bodů")
    if len(outer) < 3:
        raise ValueError("obrys potřebuje alespoň 3 body")
    m = Mesh()
    n = len(outer)
    ob = [m.add_vertex(x, y, 0.0) for x, y in outer]
    ot = [m.add_vertex(x, y, height) for x, y in outer]
    ib = [m.add_vertex(x, y, 0.0) for x, y in inner]
    it = [m.add_vertex(x, y, height) for x, y in inner]
    for i in range(n):
        j = (i + 1) % n
        m.add_quad(ob[i], ob[j], ot[j], ot[i])   # vnější plášť, normála ven
        m.add_quad(ib[j], ib[i], it[i], it[j])   # stěna otvoru, normála do otvoru
        m.add_quad(ot[i], ot[j], it[j], it[i])   # víko (mezikruží)
        m.add_quad(ib[i], ib[j], ob[j], ob[i])   # dno
    return m


def prism(outer: list[tuple[float, float]], holes: list[list[tuple[float, float]]] | None = None,
          height: float = 1.0, z0: float = 0.0) -> Mesh:
    """Vytažení obecného obrysu s libovolným počtem průchozích otvorů.

    Na rozdíl od `extrude` triangulují víka ořezáváním uší, takže obrys smí
    být konkávní. Otvory musí ležet uvnitř obrysu a navzájem se neprotínat.
    """
    from triangulate import signed_area, triangulate

    pts, tris = triangulate(outer, holes)
    m = Mesh()
    bottom = [m.add_vertex(x, y, z0) for x, y in pts]
    top = [m.add_vertex(x, y, z0 + height) for x, y in pts]
    for a, b, c in tris:
        m.add_face(top[a], top[b], top[c])       # víko, normála +z
        m.add_face(bottom[c], bottom[b], bottom[a])  # dno, normála -z

    def wall(loop: list[tuple[float, float]]) -> None:
        # Stěna se staví ze samostatných vrcholů, aby na můstcích z triangulace
        # nezůstaly viset zdvojené indexy. Směr normály nese pořadí bodů:
        # obrys proti směru hodinových ručiček dá normálu ven, otvor po směru
        # dá normálu do otvoru — jeden vzorec stačí na oboje.
        n = len(loop)
        ring_b = [m.add_vertex(x, y, z0) for x, y in loop]
        ring_t = [m.add_vertex(x, y, z0 + height) for x, y in loop]
        for i in range(n):
            j = (i + 1) % n
            m.add_quad(ring_b[i], ring_b[j], ring_t[j], ring_t[i])

    wall(list(outer) if signed_area(outer) > 0 else list(reversed(outer)))
    for hole in holes or []:
        wall(list(reversed(hole)) if signed_area(hole) > 0 else list(hole))
    return m
