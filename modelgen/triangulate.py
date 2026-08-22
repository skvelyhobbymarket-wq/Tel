"""Triangulace jednoduchého polygonu s otvory metodou ořezávání uší.

Otvory se nejdřív spojí můstky s vnějším obrysem do jednoho jednoduchého
polygonu, ten se pak ořezává. Díky tomu zvládne knihovna i konkávní tvary,
na které vějířová triangulace v `extrude` nestačí.
"""

from __future__ import annotations

import math

Point = tuple[float, float]
EPS = 1e-9


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


def _point_on_segment(p: Point, a: Point, b: Point) -> bool:
    """Leží p na úsečce ab? Test protnutí úseček tenhle případ míjí."""
    if abs(_cross(a, b, p)) > EPS:
        return False
    return (min(a[0], b[0]) - EPS <= p[0] <= max(a[0], b[0]) + EPS
            and min(a[1], b[1]) - EPS <= p[1] <= max(a[1], b[1]) + EPS)


def _bridge_hole(outer: list[Point], hole: list[Point]) -> list[Point]:
    """Spojí otvor s vnějším obrysem dvojicí shodných hran (můstkem).

    Postup podle Eberlyho: z nejpravějšího bodu otvoru se vyšle paprsek ve
    směru +x, najde se nejbližší protnutá hrana obrysu a jako cíl můstku se
    vezme její pravější konec. Pokud výhled zaclání nekonvexní vrchol, použije
    se ten s nejmenším odklonem od paprsku. Naivní "nejbližší viditelný vrchol"
    zde selhává, protože můstek umí projít přesně přes jiný vrchol.
    """
    hi = max(range(len(hole)), key=lambda i: (hole[i][0], hole[i][1]))
    m = hole[hi]

    # 1) Nejbližší protnutí paprsku z m ve směru +x s hranou obrysu.
    best_x, best_edge = None, None
    for i in range(len(outer)):
        a, b = outer[i], outer[(i + 1) % len(outer)]
        if (a[1] > m[1] and b[1] > m[1]) or (a[1] < m[1] and b[1] < m[1]):
            continue
        if abs(a[1] - b[1]) <= EPS:
            continue
        t = (m[1] - a[1]) / (b[1] - a[1])
        if t < -EPS or t > 1 + EPS:
            continue
        x = a[0] + t * (b[0] - a[0])
        if x < m[0] - EPS:
            continue
        if best_x is None or x < best_x:
            best_x, best_edge = x, (i, (i + 1) % len(outer))
    if best_edge is None:
        raise ValueError("otvor leží mimo obrys")

    intersection = (best_x, m[1])
    # 2) Cíl je pravější konec protnuté hrany.
    p_idx = max(best_edge, key=lambda i: (outer[i][0], outer[i][1]))

    # 3) Zaclání-li výhled nekonvexní vrchol, stane se cílem on.
    def reflex(i: int) -> bool:
        prev, cur, nxt = outer[i - 1], outer[i], outer[(i + 1) % len(outer)]
        return _cross(prev, cur, nxt) <= EPS

    tri = (m, intersection, outer[p_idx])
    best_angle, best_dist = None, None
    for i in range(len(outer)):
        if i == p_idx or not reflex(i):
            continue
        q = outer[i]
        if not _point_in_triangle(q, *tri):
            continue
        dx, dy = q[0] - m[0], q[1] - m[1]
        dist = dx * dx + dy * dy
        if dist <= EPS:
            continue
        angle = abs(dy) / math.sqrt(dist)      # odklon od vodorovného paprsku
        if best_angle is None or angle < best_angle - EPS or \
                (abs(angle - best_angle) <= EPS and dist < best_dist):
            best_angle, best_dist, p_idx = angle, dist, i

    return outer[:p_idx + 1] + hole[hi:] + hole[:hi + 1] + outer[p_idx:]


def _same(p: Point, q: Point) -> bool:
    return abs(p[0] - q[0]) <= EPS and abs(p[1] - q[1]) <= EPS


def _strictly_inside(p: Point, a: Point, b: Point, c: Point) -> bool:
    """Leží p uvnitř trojúhelníku abc (proti směru hod. ručiček), mimo jeho hrany?

    Můstky k otvorům kladou vrcholy přesně na hrany sousedních uší. Takový bod
    ucho nekazí, takže test musí být striktní — jinak se ořezávání zablokuje.
    """
    return (_cross(a, b, p) > EPS and _cross(b, c, p) > EPS and _cross(c, a, p) > EPS)


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

    prepared = []
    for hole in holes or []:
        if len(hole) < 3:
            raise ValueError("otvor potřebuje alespoň 3 body")
        prepared.append(list(reversed(hole)) if _is_ccw(hole) else list(hole))
    # Eberlyho postup vyžaduje otvory seřazené podle nejpravějšího bodu
    # sestupně — jinak vede můstek do oblasti, kterou teprve rozdělí další
    # můstek, a obrys se zamotá.
    prepared.sort(key=lambda h: max(p[0] for p in h), reverse=True)
    for h in prepared:
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
            # Můstky k otvorům zdvojují vrcholy a tvoří nulové výběžky. Takový
            # vrchol nenese plochu, takže ho lze zahodit bez trojúhelníku —
            # a ořezávání se tím zase rozjede.
            dropped = False
            for k in range(len(indices)):
                a = poly[indices[(k - 1) % len(indices)]]
                b = poly[indices[k]]
                c = poly[indices[(k + 1) % len(indices)]]
                if abs(_cross(a, b, c)) <= EPS or _same(a, b) or _same(b, c):
                    indices.pop(k)
                    dropped = True
                    break
            if not dropped:
                raise ValueError("nelze najít ucho — obrys je neplatný")
    triangles.append((indices[0], indices[1], indices[2]))
    return poly, triangles
