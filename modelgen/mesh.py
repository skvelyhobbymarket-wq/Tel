"""Minimalistická trojúhelníková síť bez externích závislostí.

Mesh drží seznam vrcholů a trojúhelníků (indexy) a umí se zapsat
do binárního STL nebo do OBJ.
"""

from __future__ import annotations

import math
import struct
from dataclasses import dataclass, field

Vec3 = tuple[float, float, float]


def _sub(a: Vec3, b: Vec3) -> Vec3:
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def _cross(a: Vec3, b: Vec3) -> Vec3:
    return (
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    )


def _normalize(v: Vec3) -> Vec3:
    n = math.sqrt(v[0] * v[0] + v[1] * v[1] + v[2] * v[2])
    if n == 0.0:
        return (0.0, 0.0, 0.0)
    return (v[0] / n, v[1] / n, v[2] / n)


@dataclass
class Mesh:
    vertices: list[Vec3] = field(default_factory=list)
    faces: list[tuple[int, int, int]] = field(default_factory=list)

    def add_vertex(self, x: float, y: float, z: float) -> int:
        self.vertices.append((float(x), float(y), float(z)))
        return len(self.vertices) - 1

    def add_face(self, a: int, b: int, c: int) -> None:
        self.faces.append((a, b, c))

    def add_quad(self, a: int, b: int, c: int, d: int) -> None:
        """Čtyřúhelník rozdělený na dva trojúhelníky, orientace a->b->c->d."""
        self.add_face(a, b, c)
        self.add_face(a, c, d)

    def extend(self, other: "Mesh") -> "Mesh":
        """Spojí druhou síť do této (bez slučování shodných vrcholů)."""
        offset = len(self.vertices)
        self.vertices.extend(other.vertices)
        self.faces.extend((a + offset, b + offset, c + offset) for a, b, c in other.faces)
        return self

    def transform(self, fn) -> "Mesh":
        """Nová síť s vrcholy protaženými funkcí fn(x, y, z) -> Vec3."""
        out = Mesh(vertices=[tuple(map(float, fn(*v))) for v in self.vertices], faces=list(self.faces))
        return out

    def translated(self, dx: float = 0.0, dy: float = 0.0, dz: float = 0.0) -> "Mesh":
        return self.transform(lambda x, y, z: (x + dx, y + dy, z + dz))

    def scaled(self, sx: float, sy: float | None = None, sz: float | None = None) -> "Mesh":
        sy = sx if sy is None else sy
        sz = sx if sz is None else sz
        return self.transform(lambda x, y, z: (x * sx, y * sy, z * sz))

    def rotated_z(self, angle_rad: float) -> "Mesh":
        c, s = math.cos(angle_rad), math.sin(angle_rad)
        return self.transform(lambda x, y, z: (x * c - y * s, x * s + y * c, z))

    def rotated_x(self, angle_rad: float) -> "Mesh":
        c, s = math.cos(angle_rad), math.sin(angle_rad)
        return self.transform(lambda x, y, z: (x, y * c - z * s, y * s + z * c))

    def rotated_y(self, angle_rad: float) -> "Mesh":
        c, s = math.cos(angle_rad), math.sin(angle_rad)
        return self.transform(lambda x, y, z: (x * c + z * s, y, -x * s + z * c))

    def bounds(self) -> tuple[Vec3, Vec3]:
        xs = [v[0] for v in self.vertices]
        ys = [v[1] for v in self.vertices]
        zs = [v[2] for v in self.vertices]
        return (min(xs), min(ys), min(zs)), (max(xs), max(ys), max(zs))

    def face_normal(self, face: tuple[int, int, int]) -> Vec3:
        a, b, c = (self.vertices[i] for i in face)
        return _normalize(_cross(_sub(b, a), _sub(c, a)))

    # --- export ---------------------------------------------------------

    def write_stl(self, path: str, name: str = "mesh") -> str:
        with open(path, "wb") as fh:
            fh.write(name.encode("ascii", "replace")[:80].ljust(80, b"\0"))
            fh.write(struct.pack("<I", len(self.faces)))
            for face in self.faces:
                nx, ny, nz = self.face_normal(face)
                fh.write(struct.pack("<3f", nx, ny, nz))
                for i in face:
                    fh.write(struct.pack("<3f", *self.vertices[i]))
                fh.write(struct.pack("<H", 0))
        return path

    def write_obj(self, path: str, name: str = "mesh") -> str:
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(f"o {name}\n")
            for x, y, z in self.vertices:
                fh.write(f"v {x:.6f} {y:.6f} {z:.6f}\n")
            for a, b, c in self.faces:
                fh.write(f"f {a + 1} {b + 1} {c + 1}\n")
        return path
