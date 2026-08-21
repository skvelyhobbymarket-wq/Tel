"""CLI: vygeneruje model do STL nebo OBJ.

Použití:
    python3 cli.py mug --out out/hrnek.stl
    python3 cli.py gear --teeth 24 --out out/kolo.stl
    python3 cli.py sphere --radius 20 --out out/koule.obj
"""

from __future__ import annotations

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "examples"))

import primitives
from gear import gear
from mug import mug


def build(args) -> "primitives.Mesh":
    if args.shape == "mug":
        return mug(height=args.height, radius=args.radius)
    if args.shape == "gear":
        return gear(teeth=args.teeth, module=args.module, thickness=args.thickness, bore=args.bore)
    if args.shape == "sphere":
        return primitives.sphere(args.radius, segments=args.segments)
    if args.shape == "box":
        return primitives.box(args.radius * 2, args.radius * 2, args.height)
    if args.shape == "cylinder":
        return primitives.cylinder(args.radius, args.height, segments=args.segments)
    if args.shape == "torus":
        return primitives.torus(args.radius, args.radius / 3.0, segments=args.segments)
    raise ValueError(f"neznámý tvar: {args.shape}")


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Generátor 3D modelů do STL/OBJ.")
    p.add_argument("shape", choices=["mug", "gear", "sphere", "box", "cylinder", "torus"])
    p.add_argument("--out", default=None, help="výstupní soubor (.stl nebo .obj)")
    p.add_argument("--radius", type=float, default=40.0)
    p.add_argument("--height", type=float, default=95.0)
    p.add_argument("--segments", type=int, default=64)
    p.add_argument("--teeth", type=int, default=20)
    p.add_argument("--module", type=float, default=3.0)
    p.add_argument("--thickness", type=float, default=8.0)
    p.add_argument("--bore", type=float, default=8.0)
    args = p.parse_args(argv)

    out = args.out or f"{args.shape}.stl"
    directory = os.path.dirname(os.path.abspath(out))
    os.makedirs(directory, exist_ok=True)

    m = build(args)
    if out.lower().endswith(".obj"):
        m.write_obj(out, name=args.shape)
    else:
        m.write_stl(out, name=args.shape)

    lo, hi = m.bounds()
    size = tuple(round(hi[i] - lo[i], 2) for i in range(3))
    print(f"{out}: {len(m.vertices)} vrcholů, {len(m.faces)} trojúhelníků, rozměry {size} mm")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
