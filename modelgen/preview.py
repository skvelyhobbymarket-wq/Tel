"""Náhledový render sítě do PNG — z-buffer a difuzní stínování, jen stdlib."""

from __future__ import annotations

import math
import struct
import zlib

from mesh import Mesh


def render(m: Mesh, path: str, width: int = 640, height: int = 640,
           yaw: float = 0.6, pitch: float = -1.05,
           background: tuple[int, int, int] = (24, 26, 30)) -> str:
    lo, hi = m.bounds()
    cx = [(lo[i] + hi[i]) / 2.0 for i in range(3)]
    extent = max(hi[i] - lo[i] for i in range(3)) or 1.0

    cy_, sy = math.cos(yaw), math.sin(yaw)
    cp, sp = math.cos(pitch), math.sin(pitch)

    def project(v):
        x, y, z = v[0] - cx[0], v[1] - cx[1], v[2] - cx[2]
        x, y = x * cy_ - y * sy, x * sy + y * cy_
        y, z = y * cp - z * sp, y * sp + z * cp
        scale = width * 0.62 / extent
        return (width / 2.0 + x * scale, height / 2.0 - z * scale, y)

    zbuf = [float("inf")] * (width * height)
    pix = bytearray()
    for _ in range(width * height):
        pix.extend(background)

    # Projekce mapuje rotované osy na (x doprava, -z nahoru, y do hloubky),
    # takže světlo musí mít zápornou složku y, aby svítilo směrem od diváka.
    light = (-0.35, -0.83, 0.44)
    for face in m.faces:
        vs = [m.vertices[i] for i in face]
        p = [project(v) for v in vs]
        nx, ny, nz = m.face_normal(face)
        # světlo je dané v pohledových osách až po rotaci normály
        n = (nx * cy_ - ny * sy, nx * sy + ny * cy_, nz)
        n = (n[0], n[1] * cp - n[2] * sp, n[1] * sp + n[2] * cp)
        key = max(0.0, n[0] * light[0] + n[1] * light[1] + n[2] * light[2])
        fill = max(0.0, -n[1])          # přisvětlení od diváka, ať dutiny nezčernají
        shade = min(1.0, 0.16 + 0.62 * key + 0.30 * fill)
        color = (int(210 * shade), int(214 * shade), int(224 * shade))

        minx = max(0, int(min(q[0] for q in p)))
        maxx = min(width - 1, int(max(q[0] for q in p)) + 1)
        miny = max(0, int(min(q[1] for q in p)))
        maxy = min(height - 1, int(max(q[1] for q in p)) + 1)
        (x0, y0, z0), (x1, y1, z1), (x2, y2, z2) = p
        denom = (y1 - y2) * (x0 - x2) + (x2 - x1) * (y0 - y2)
        if abs(denom) < 1e-9:
            continue
        for py in range(miny, maxy + 1):
            for px in range(minx, maxx + 1):
                a = ((y1 - y2) * (px + 0.5 - x2) + (x2 - x1) * (py + 0.5 - y2)) / denom
                if a < 0.0:
                    continue
                b = ((y2 - y0) * (px + 0.5 - x2) + (x0 - x2) * (py + 0.5 - y2)) / denom
                if b < 0.0 or a + b > 1.0:
                    continue
                depth = a * z0 + b * z1 + (1.0 - a - b) * z2
                idx = py * width + px
                if depth < zbuf[idx]:
                    zbuf[idx] = depth
                    pix[idx * 3:idx * 3 + 3] = bytes(color)

    raw = b"".join(b"\x00" + bytes(pix[y * width * 3:(y + 1) * width * 3]) for y in range(height))

    def chunk(tag: bytes, data: bytes) -> bytes:
        return (struct.pack(">I", len(data)) + tag + data
                + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF))

    png = (b"\x89PNG\r\n\x1a\n"
           + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
           + chunk(b"IDAT", zlib.compress(raw, 6))
           + chunk(b"IEND", b""))
    with open(path, "wb") as fh:
        fh.write(png)
    return path
