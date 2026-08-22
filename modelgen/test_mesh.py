"""Kontroly, na kterých stojí použitelnost STL: uzavřenost a orientace normál."""

import math
import os
import struct
import sys
import tempfile
import unittest
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "examples"))

import primitives as p
import triangulate as tri
from knob import knob, star_outline
from mesh import Mesh
from thread import mouth_polygon, thread_radius


def signed_volume(m: Mesh) -> float:
    """Objem přes divergenční větu; kladný = normály ven."""
    total = 0.0
    for a, b, c in m.faces:
        (ax, ay, az), (bx, by, bz), (cx, cy, cz) = m.vertices[a], m.vertices[b], m.vertices[c]
        total += (ax * (by * cz - bz * cy)
                  - ay * (bx * cz - bz * cx)
                  + az * (bx * cy - by * cx)) / 6.0
    return total


def edge_counts(m: Mesh) -> Counter:
    """Počítá hrany podle pozice vrcholů, aby nevadily duplicitní indexy."""
    def key(i):
        return tuple(round(c, 9) for c in m.vertices[i])

    edges = Counter()
    for a, b, c in m.faces:
        for u, v in ((a, b), (b, c), (c, a)):
            ku, kv = key(u), key(v)
            if ku == kv:
                continue  # degenerovaná hrana na ose
            edges[(ku, kv)] += 1
    return edges


CLOSED_SOLIDS = {
    "box": p.box(2, 3, 4),
    "box_centered": p.box(2, 2, 2, centered=True),
    "cylinder": p.cylinder(1.5, 4, segments=16),
    "truncated_cone": p.cylinder(2.0, 3, segments=16, radius_top=0.5),
    "cone": p.cone(1.0, 2.0, segments=16),
    "sphere": p.sphere(1.0, segments=16, rings=8),
    "torus": p.torus(2.0, 0.5, segments=16, tube_segments=8),
    "extrude": p.extrude([(0, 0), (2, 0), (2, 2), (0, 2)], 1.5),
    "revolve_closed": p.revolve([(0, 0), (1, 0), (1, 2), (0, 2)], segments=16),
    "ring_extrude": p.ring_extrude(
        [(2, 0), (0, 2), (-2, 0), (0, -2)], [(1, 0), (0, 1), (-1, 0), (0, -1)], 3),
    "gear": __import__("gear").gear(teeth=12),
    "prism_two_holes": p.prism(
        [(-5, -5), (5, -5), (5, 5), (-5, 5)],
        [[(1 * math.cos(a) - 2.5, 1 * math.sin(a) - 2.5) for a in
          [2 * math.pi * i / 16 for i in range(16)]],
         [(1 * math.cos(a) + 2.5, 1 * math.sin(a) + 2.5) for a in
          [2 * math.pi * i / 16 for i in range(16)]]], height=3),
    "knob": knob(segments=32),
    "mug": __import__("mug").mug(),
}


class TestSolids(unittest.TestCase):
    def test_watertight(self):
        """Každá hrana musí být sdílena právě dvěma trojúhelníky v opačném směru."""
        for name, m in CLOSED_SOLIDS.items():
            with self.subTest(solid=name):
                edges = edge_counts(m)
                for (u, v), n in edges.items():
                    self.assertEqual(n, 1, f"{name}: hrana {u}->{v} použita {n}x ve stejném směru")
                    self.assertEqual(edges[(v, u)], 1, f"{name}: hrana {u}->{v} nemá protějšek")

    def test_normals_point_outward(self):
        for name, m in CLOSED_SOLIDS.items():
            with self.subTest(solid=name):
                self.assertGreater(signed_volume(m), 0.0, f"{name}: normály míří dovnitř")

    def test_no_degenerate_faces(self):
        for name, m in CLOSED_SOLIDS.items():
            with self.subTest(solid=name):
                for face in m.faces:
                    n = m.face_normal(face)
                    self.assertGreater(math.sqrt(sum(c * c for c in n)), 0.5,
                                       f"{name}: nulová normála u {face}")

    def test_volumes_match_analytic(self):
        cases = [
            (p.box(2, 3, 4), 24.0, 0.0),
            (p.cylinder(1.0, 5.0, segments=512), math.pi * 5.0, 0.01),
            (p.cone(1.0, 3.0, segments=512), math.pi * 3.0 / 3.0, 0.01),
            (p.sphere(1.0, segments=256, rings=128), 4.0 / 3.0 * math.pi, 0.01),
            (p.torus(3.0, 1.0, segments=256, tube_segments=128), 2 * math.pi**2 * 3.0 * 1.0, 0.01),
            # mezikruží: (8 - 2) * výška 3, čtverce mají přesnou plochu
            (p.ring_extrude([(2, 0), (0, 2), (-2, 0), (0, -2)],
                            [(1, 0), (0, 1), (-1, 0), (0, -1)], 3.0), 18.0, 0.0),
        ]
        for m, expected, tol in cases:
            with self.subTest(expected=expected):
                self.assertAlmostEqual(signed_volume(m), expected, delta=max(tol * expected, 1e-9))


class TestTransforms(unittest.TestCase):
    def test_translate_and_scale(self):
        m = p.box(1, 1, 1).translated(dz=5).scaled(2)
        lo, hi = m.bounds()
        self.assertEqual(lo, (0.0, 0.0, 10.0))
        self.assertEqual(hi, (2.0, 2.0, 12.0))

    def test_rotation_preserves_volume(self):
        m = p.box(1, 2, 3, centered=True).rotated_z(0.7).rotated_x(0.3).rotated_y(1.1)
        self.assertAlmostEqual(signed_volume(m), 6.0, places=9)

    def test_extend_merges(self):
        a, b = p.box(1, 1, 1), p.box(1, 1, 1).translated(dx=5)
        merged = Mesh().extend(a).extend(b)
        self.assertEqual(len(merged.faces), len(a.faces) + len(b.faces))
        self.assertAlmostEqual(signed_volume(merged), 2.0, places=9)


class TestTriangulate(unittest.TestCase):
    """Triangulace musí zachovat plochu — to odhalí vynechaná i zdvojená ucha."""

    @staticmethod
    def _area(pts, tris):
        return sum(tri._cross(pts[a], pts[b], pts[c]) / 2.0 for a, b, c in tris)

    @staticmethod
    def _circle(r, n, cx=0.0, cy=0.0):
        return [(cx + r * math.cos(2 * math.pi * i / n),
                 cy + r * math.sin(2 * math.pi * i / n)) for i in range(n)]

    def test_square_without_holes(self):
        pts, tris = tri.triangulate([(-5, -5), (5, -5), (5, 5), (-5, 5)])
        self.assertEqual(len(tris), 2)
        self.assertAlmostEqual(self._area(pts, tris), 100.0, places=9)

    def test_area_with_holes(self):
        outer = [(-5, -5), (5, -5), (5, 5), (-5, 5)]
        holes = [self._circle(1, 24, -2.5, -2.5), self._circle(1, 24, 2.5, 2.5)]
        pts, tris = tri.triangulate(outer, holes)
        hole_area = 2 * tri.signed_area(holes[0])
        self.assertAlmostEqual(self._area(pts, tris), 100.0 - hole_area, places=9)

    def test_clockwise_input_is_normalised(self):
        pts, tris = tri.triangulate([(-5, 5), (5, 5), (5, -5), (-5, -5)])
        self.assertGreater(self._area(pts, tris), 0.0)

    def test_concave_polygon(self):
        # tvar písmene L, na který vějířová triangulace nestačí
        poly = [(0, 0), (6, 0), (6, 2), (2, 2), (2, 6), (0, 6)]
        pts, tris = tri.triangulate(poly)
        self.assertAlmostEqual(self._area(pts, tris), 20.0, places=9)

    def test_many_holes_at_several_densities(self):
        """Regrese: sedm kapes plus nálitek se dřív při hustším dělení nedaly
        otriangulovat — můstky k otvorům se zamotávaly do sebe."""
        for n in (16, 24, 32, 48, 64):
            with self.subTest(segments=n):
                outer = self._circle(37.5, 8 * 24)
                holes = [self._circle(4.7, n // 2, 20 * math.cos(2 * math.pi * i / 7),
                                      20 * math.sin(2 * math.pi * i / 7)) for i in range(7)]
                holes.append(self._circle(14.0, n))
                pts, tris = tri.triangulate(outer, holes)
                expected = tri.signed_area(outer) - sum(abs(tri.signed_area(h)) for h in holes)
                self.assertAlmostEqual(self._area(pts, tris), expected, places=6)

    def test_hole_order_does_not_matter(self):
        """Výsledná plocha nesmí záviset na pořadí, v jakém otvory přijdou."""
        outer = [(-10, -10), (10, -10), (10, 10), (-10, 10)]
        holes = [self._circle(1.5, 20, 5, 5), self._circle(1.5, 20, -5, 5),
                 self._circle(1.5, 20, -5, -5), self._circle(1.5, 20, 5, -5)]
        areas = []
        for order in (holes, list(reversed(holes)), [holes[2], holes[0], holes[3], holes[1]]):
            pts, tris = tri.triangulate(outer, order)
            areas.append(self._area(pts, tris))
        for a in areas[1:]:
            self.assertAlmostEqual(a, areas[0], places=9)

    def test_rejects_hole_outside_contour(self):
        with self.assertRaises(ValueError):
            tri.triangulate([(0, 0), (4, 0), (4, 4), (0, 4)], [self._circle(1, 12, 50, 50)])

    def test_rejects_degenerate_input(self):
        with self.assertRaises(ValueError):
            tri.triangulate([(0, 0), (1, 1)])


class TestThread(unittest.TestCase):
    def test_profile_is_periodic_along_helix(self):
        """Posun o jednu rozteč ve výšce musí dát stejný poloměr."""
        for theta in (0.0, 1.0, 2.5):
            for z in (0.0, 0.4, 3.1):
                a = thread_radius(theta, z, 6.0, 1.75, 1.07)
                b = thread_radius(theta, z + 1.75, 6.0, 1.75, 1.07)
                self.assertAlmostEqual(a, b, places=9)

    def test_profile_stays_within_bounds(self):
        for i in range(200):
            r = thread_radius(i * 0.31, i * 0.17, 6.0, 1.75, 1.07)
            self.assertGreaterEqual(r, 6.0 - 1.07 - 1e-9)
            self.assertLessEqual(r, 6.0 + 1e-9)

    def test_mouth_matches_thread_at_z0(self):
        poly = mouth_polygon(12.0, 1.75, segments=32)
        for s, (x, y) in enumerate(poly):
            theta = 2 * math.pi * s / 32
            expected = thread_radius(theta, 0.0, 6.0, 1.75, 0.613 * 1.75)
            self.assertAlmostEqual(math.hypot(x, y), expected, places=9)

    def test_rejects_bad_parameters(self):
        import thread as th
        with self.assertRaises(ValueError):
            th.threaded_hole(12.0, 0.0, 10.0)
        with self.assertRaises(ValueError):
            th.threaded_hole(2.0, 8.0, 10.0)


class TestKnob(unittest.TestCase):
    def test_outline_lobe_count(self):
        """Počet lokálních maxim poloměru musí odpovídat počtu laloků."""
        pts = star_outline(75.0, 57.5, lobes=8)
        radii = [math.hypot(x, y) for x, y in pts]
        peaks = sum(1 for i in range(len(radii))
                    if radii[i] > radii[i - 1] and radii[i] >= radii[(i + 1) % len(radii)])
        self.assertEqual(peaks, 8)
        self.assertAlmostEqual(max(radii), 37.5, places=6)
        self.assertAlmostEqual(min(radii), 28.75, places=6)

    def test_pockets_do_not_break_through(self):
        """Kapsy ani závit nesmí prorazit horní čelo — tělo si drží svou výšku."""
        m = knob(segments=32, height=26.0, boss_h=0.0, pocket_depth=22.0,
                 thread_depth=22.0, recess_depth=0.0)
        lo, hi = m.bounds()
        self.assertAlmostEqual(hi[2] - lo[2], 26.0, places=6)
        # žádný vrchol nesmí ležet nad horním čelem
        self.assertLessEqual(max(v[2] for v in m.vertices), 26.0 + 1e-9)

    def test_rejects_pockets_deeper_than_body(self):
        with self.assertRaises(ValueError):
            knob(height=10.0, boss_h=0.0, pocket_depth=12.0, thread_depth=5.0)
        with self.assertRaises(ValueError):
            knob(height=10.0, boss_h=0.0, pocket_depth=5.0, thread_depth=11.0)

    def test_rejects_pockets_colliding_with_thread(self):
        with self.assertRaises(ValueError):
            knob(pocket_circle_d=14.0, pocket_d=9.0, thread_d=12.0)

    def test_recess_removes_its_own_volume(self):
        """Vybrání na pohledové straně musí ubrat právě objem svého válce."""
        flat = knob(segments=64, recess_depth=0.0)
        dished = knob(segments=64, recess_d=52.5, recess_depth=1.5, dot_depth=0.0)
        expected = math.pi * 26.25 ** 2 * 1.5
        self.assertAlmostEqual(signed_volume(flat) - signed_volume(dished),
                               expected, delta=0.01 * expected)

    def test_dot_removes_its_own_volume(self):
        plain = knob(segments=64, dot_depth=0.0)
        dotted = knob(segments=64, dot_d=2.4, dot_depth=0.8)
        expected = math.pi * 1.2 ** 2 * 0.8
        self.assertAlmostEqual(signed_volume(plain) - signed_volume(dotted),
                               expected, delta=0.05 * expected)

    def test_recess_does_not_change_total_height(self):
        """Vybrání je zapuštěné, takže obrys dílu musí zůstat stejně vysoký."""
        for kw in ({}, {"recess_depth": 0.0}, {"dot_depth": 0.0}):
            with self.subTest(**kw):
                lo, hi = knob(segments=32, height=26.0, boss_h=4.0, **kw).bounds()
                self.assertAlmostEqual(hi[2] - lo[2], 30.0, places=6)

    def test_boss_adds_its_height_below_the_body(self):
        """Nálitek vystupuje pod tělo, takže celková výška je height + boss_h."""
        without = knob(segments=32, height=26.0, boss_h=0.0)
        with_boss = knob(segments=32, height=26.0, boss_h=4.0)
        lo_a, hi_a = without.bounds()
        lo_b, hi_b = with_boss.bounds()
        self.assertAlmostEqual(hi_a[2] - lo_a[2], 26.0, places=6)
        self.assertAlmostEqual(hi_b[2] - lo_b[2], 30.0, places=6)
        # díl stojí na nule v obou případech
        self.assertAlmostEqual(lo_a[2], 0.0, places=6)
        self.assertAlmostEqual(lo_b[2], 0.0, places=6)

    def test_boss_only_widens_the_part_near_its_own_base(self):
        """Ve výšce nálitku smí být materiál jen do jeho průměru."""
        m = knob(segments=32, boss_d=28.0, boss_h=4.0)
        near_base = [math.hypot(v[0], v[1]) for v in m.vertices if v[2] < 3.0]
        self.assertLessEqual(max(near_base), 14.0 + 1e-6)

    def test_fillet_keeps_the_outer_dimension(self):
        """Zaoblení zatahuje čela dovnitř, ale největší průměr drží uprostřed."""
        for edge_r in (0.0, 1.0, 1.5):
            with self.subTest(edge_r=edge_r):
                m = knob(segments=48, edge_r=edge_r)
                span = max(math.hypot(v[0], v[1]) for v in m.vertices)
                self.assertAlmostEqual(span, 37.5, delta=0.05)

    def test_fillet_pulls_the_faces_in(self):
        """Na čele je obrys zatažený o poloměr zaoblení proti rovné části boku."""
        edge_r = 1.5
        m = knob(segments=48, edge_r=edge_r, boss_h=4.0, height=26.0)
        # rovná část boku začíná ve výšce edge_r nad spodkem těla (to je v z=4)
        at_straight = max(math.hypot(v[0], v[1])
                          for v in m.vertices if abs(v[2] - (4.0 + edge_r)) < 1e-6)
        at_face = max(math.hypot(v[0], v[1]) for v in m.vertices if abs(v[2] - 30.0) < 1e-6)
        self.assertAlmostEqual(at_straight, 37.5, delta=0.05)
        self.assertAlmostEqual(at_face, 37.5 - edge_r, delta=0.15)

    def test_fillet_removes_material(self):
        sharp = knob(segments=48, edge_r=0.0)
        rounded = knob(segments=48, edge_r=1.5)
        self.assertLess(signed_volume(rounded), signed_volume(sharp))

    def test_rejects_fillet_larger_than_body(self):
        with self.assertRaises(ValueError):
            knob(height=4.0, edge_r=3.0)
        with self.assertRaises(ValueError):
            knob(edge_r=-1.0)

    def test_rings_remove_their_own_annulus(self):
        """Prstence musí ubrat právě objem svých mezikruží."""
        pocket_r, ring_w, ring_depth, pockets = 9.4 / 2.0, 1.0, 1.0, 8
        plain = knob(segments=64, ring_depth=0.0)
        ringed = knob(segments=64, ring_w=ring_w, ring_depth=ring_depth)
        expected = pockets * math.pi * ((pocket_r + ring_w) ** 2 - pocket_r ** 2) * ring_depth
        self.assertAlmostEqual(signed_volume(plain) - signed_volume(ringed),
                               expected, delta=0.02 * expected)

    def test_rejects_ring_deeper_than_pocket(self):
        with self.assertRaises(ValueError):
            knob(pocket_depth=22.0, ring_depth=25.0)

    def test_rejects_boss_colliding_with_pockets(self):
        with self.assertRaises(ValueError):
            knob(boss_d=34.0, boss_h=4.0, pocket_circle_d=40.0, pocket_d=9.4)
        with self.assertRaises(ValueError):
            knob(boss_d=20.0, boss_h=4.0, thread_d=24.0)
        with self.assertRaises(ValueError):
            knob(boss_h=-1.0)

    def test_rejects_bad_recess(self):
        with self.assertRaises(ValueError):
            knob(root_d=46.0, recess_d=50.0, recess_depth=1.5)
        with self.assertRaises(ValueError):
            knob(recess_depth=-1.0)
        with self.assertRaises(ValueError):
            knob(recess_d=40.0, dot_d=42.0, dot_depth=0.5)

    def test_rejects_recess_meeting_the_pockets(self):
        """Mezi dnem vybrání a stropem kapes musí zůstat materiál."""
        with self.assertRaises(ValueError):
            knob(height=20.0, boss_h=0.0, pocket_depth=19.0, thread_depth=19.0,
                 recess_depth=1.5)

    def test_thread_defaults_to_m24(self):
        """Největší poloměr závitové plochy odpovídá velkému průměru M24."""
        m = knob(segments=32)
        radii = [math.hypot(v[0], v[1]) for v in m.vertices
                 if 0.0 < v[2] < 20.0 and math.hypot(v[0], v[1]) < 13.0]
        self.assertAlmostEqual(max(radii), 12.0, places=6)

    def test_pockets_and_thread_remove_material(self):
        solid = knob(segments=32, pocket_d=0.6, thread_d=1.2, pitch=0.25,
                     pocket_circle_d=34.0, boss_d=2.0)
        drilled = knob(segments=32)
        self.assertLess(signed_volume(drilled), signed_volume(solid))


class TestExamples(unittest.TestCase):
    """Příklady musí zůstat tisknutelné, ne jen spustitelné."""

    def test_gear_bore_is_a_real_hole(self):
        g = __import__("gear").gear(teeth=16, module=2.0, thickness=5.0, bore=6.0)
        lo, hi = g.bounds()
        self.assertAlmostEqual(hi[2] - lo[2], 5.0, places=6)
        # Rozdíl proti stejnému kolu s minimálním otvorem musí odpovídat objemu válce,
        # který díra odebrala — to ověří, že jde o skutečnou dutinu, ne jen obrácené normály.
        tiny = __import__("gear").gear(teeth=16, module=2.0, thickness=5.0, bore=0.5)
        removed = signed_volume(tiny) - signed_volume(g)
        expected = math.pi * (3.0**2 - 0.25**2) * 5.0
        self.assertAlmostEqual(removed, expected, delta=0.02 * expected)

    def test_gear_rejects_bad_parameters(self):
        with self.assertRaises(ValueError):
            __import__("gear").gear(teeth=4)
        with self.assertRaises(ValueError):
            __import__("gear").gear(teeth=10, module=2.0, bore=100.0)

    def test_mug_rejects_bad_wall(self):
        with self.assertRaises(ValueError):
            __import__("mug").mug(wall=0.0)
        with self.assertRaises(ValueError):
            __import__("mug").mug(radius=10.0, wall=20.0)

    def test_mug_is_hollow(self):
        m = __import__("mug").mug(height=90.0, radius=40.0, wall=3.0, floor=4.0)
        self.assertLess(signed_volume(m), math.pi * 40.0**2 * 90.0)


class TestExport(unittest.TestCase):
    def test_stl_binary_roundtrip(self):
        m = p.sphere(1.0, segments=16, rings=8)
        with tempfile.TemporaryDirectory() as d:
            path = m.write_stl(os.path.join(d, "s.stl"), name="koule")
            with open(path, "rb") as fh:
                data = fh.read()
            count = struct.unpack("<I", data[80:84])[0]
            self.assertEqual(count, len(m.faces))
            self.assertEqual(len(data), 84 + 50 * count)

    def test_obj_indices_are_one_based(self):
        m = p.box(1, 1, 1)
        with tempfile.TemporaryDirectory() as d:
            path = m.write_obj(os.path.join(d, "b.obj"))
            with open(path, encoding="utf-8") as fh:
                lines = fh.read().splitlines()
            verts = [l for l in lines if l.startswith("v ")]
            faces = [l for l in lines if l.startswith("f ")]
            self.assertEqual(len(verts), len(m.vertices))
            self.assertEqual(len(faces), len(m.faces))
            idx = [int(t) for l in faces for t in l.split()[1:]]
            self.assertEqual(min(idx), 1)
            self.assertEqual(max(idx), len(m.vertices))


if __name__ == "__main__":
    unittest.main(verbosity=2)
