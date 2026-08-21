"""Triangulace jednoduchého polygonu s otvory metodou ořezávání uší.

Otvory se nejdřív spojí můstky s vnějším obrysem do jednoho jednoduchého
polygonu, ten se pak ořezává. Díky tomu zvládne knihovna i konkávní tvary,
na které vějířová triangulace v `extrude` nestačí.
"""

from __future__ import annotations

Point = tuple[float, float]
EPS = 1e-12


def signed_area(poly: list[Point]) -> float:
    total = 0.0
    for i in range(len(poly)):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % len(poly)]
        total += x1 * y2 - x2 * y1
    return total / 2.0


def _is_ccw(poly: list[Point]) -> bool:
    return signed_area(poly) > 0.0


def _cross(o: Point, a: Point, b: Point) -> float:
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def _point_in_triangle(p: Point, a: Point, b: Point, c: Point) -> bool:
    d1, d2, d3 = _cross(a, b, p), _cross(b, c, p), _cross(c, a, p)
    has_neg = d1 < -EPS or d2 < -EPS or d3 < -EPS
    has_pos = d1 > EPS or d2 > EPS or d3 > EPS
    return not (has_neg and has_pos)


def _segments_properly_intersect(p1: Point, p2: Point, p3: Point, p4: Point) -> bool:
    d1, d2 = _cross(p3, p4, p1), _cross(p3, p4, p2)
    d3, d4 = _cross(p1, p2, p3), _cross(p1, p2, p4)
    return ((d1 > EPS and d2 < -EPS) or (d1 < -EPS and d2 > EPS)) and \
           ((d3 > EPS and d4 < -EPS) or (d3 < -EPS and d4 > EPS))


def _bridge_hole(outer: list[Point], hole: list[Point]) -> list[Point]:
    """Spojí otvor s vnějším obrysem dvojicí shodných hran (můstkem)."""
    # Nejpravější bod otvoru je zaručeně "vidět" ven ve směru +x.
    hi = max(range(len(hole)), key=lambda i: (hole[i][0], hole[i][1]))
    m = hole[hi]

    # Z kandidátů na vnějším obrysu vyber ten, ke kterému můstek nic neprotíná.
    candidates = sorted(range(len(outer)), key=lambda i: (outer[i][0] - m[0]) ** 2
                        + (outer[i][1] - m[1]) ** 2)
    for oi in candidates:
        p = outer[oi]
        blocked = False
        for loop in (outer, hole):
            for i in range(len(loop)):
                a, b = loop[i], loop[(i + 1) % len(loop)]
                if _segments_properly_intersect(m, p, a, b):
                    blocked = True
                    break
            if blocked:
                break
        if not blocked:
            return (outer[:oi + 1] + hole[hi:] + hole[:hi + 1] + outer[oi:])
    raise ValueError("nepodařilo se propojit otvor s obrysem")


def _same(p: Point, q: Point) -> bool:
    return abs(p[0] - q[0]) <= EPS and abs(p[1] - q[1]) <= EPS


def _is_reflex(poly: list[Point], indices: list[int], k: int) -> bool:
    n = len(indices)
    prev, cur, nxt = poly[indices[(k - 1) % n]], poly[indices[k]], poly[indices[(k + 1) % n]]
    return _cross(prev, cur, nxt) <= EPS


def _triangle_blocked(poly, indices, corner, a: Point, b: Point, c: Point) -> bool:
    """Ucho je blokované, jen když do něj zasahuje nekonvexní vrchol.

    Můstky k otvorům zdvojují vrcholy, takže se porovnává i poloha — bod
    ležící přesně v rohu ucha není překážka, je to tentýž vrchol.
    """
    for k, j in enumerate(indices):
        if j in corner:
            continue
        p = poly[j]
        if _same(p, a) or _same(p, b) or _same(p, c):
            continue
        if not _is_reflex(poly, indices, k):
            continue
        if _point_in_triangle(p, a, b, c):
            return True
    return False


def triangulate(outer: list[Point], holes: list[list[Point]] | None = None
                ) -> tuple[list[Point], list[tuple[int, int, int]]]:
    """Vrátí (body, trojúhelníky) pro obrys proti směru hodinových ručiček.

    Otvory se dovnitř otočí po směru hodinových ručiček automaticky.
    Výsledné trojúhelníky jsou proti směru hodinových ručiček, tedy s
    normálou v +z.
    """
    if len(outer) < 3:
        raise ValueError("obrys potřebuje alespoň 3 body")
    poly = list(outer) if _is_ccw(outer) else list(reversed(outer))

    for hole in holes or []:
        if len(hole) < 3:
            raise ValueError("otvor potřebuje alespoň 3 body")
        h = list(reversed(hole)) if _is_ccw(hole) else list(hole)
        poly = _bridge_hole(poly, h)

    indices = list(range(len(poly)))
    triangles: list[tuple[int, int, int]] = []
    guard = 0
    limit = len(indices) * len(indices) + 16
    while len(indices) > 3:
        guard += 1
        if guard > limit:
            raise ValueError("triangulace nekonverguje — obrys se patrně protíná")
        clipped = False
        for k in range(len(indices)):
            i0 = indices[(k - 1) % len(indices)]
            i1 = indices[k]
            i2 = indices[(k + 1) % len(indices)]
            a, b, c = poly[i0], poly[i1], poly[i2]
            if _cross(a, b, c) <= EPS:
                continue  # nekonvexní vrchol nebo kolineární trojice
            if _triangle_blocked(poly, indices, (i0, i1, i2), a, b, c):
                continue
            triangles.append((i0, i1, i2))
            indices.pop(k)
            clipped = True
            break
        if not clipped:
            raise ValueError("nelze najít ucho — obrys je neplatný")
    triangles.append((indices[0], indices[1], indices[2]))
    return poly, triangles
