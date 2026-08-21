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
from mesh import Mesh


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
