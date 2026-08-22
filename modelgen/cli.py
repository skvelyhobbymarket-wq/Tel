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
from knob import knob
from mug import mug


def build(args) -> "primitives.Mesh":
    if args.shape == "knob":
        return knob(outer_d=args.outer_d, root_d=args.root_d, height=args.knob_height,
                    pockets=args.pockets, pocket_d=args.pocket_d,
                    pocket_circle_d=args.pocket_circle_d, pocket_depth=args.pocket_depth,
                    thread_d=args.thread_d, pitch=args.pitch, thread_depth=args.thread_depth,
                    recess_d=args.recess_d, recess_depth=args.recess_depth,
                    dot_d=args.dot_d, dot_depth=args.dot_depth,
                    boss_d=args.boss_d, boss_h=args.boss_h,
                    edge_r=args.edge_r, ring_w=args.ring_w, ring_depth=args.ring_depth)
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
    p.add_argument("shape", choices=["knob", "mug", "gear", "sphere", "box", "cylinder", "torus"])
    p.add_argument("--out", default=None, help="výstupní soubor (.stl nebo .obj)")
    p.add_argument("--radius", type=float, default=40.0)
    p.add_argument("--height", type=float, default=95.0)
    p.add_argument("--segments", type=int, default=64)
    p.add_argument("--teeth", type=int, default=20)
    p.add_argument("--module", type=float, default=3.0)
    p.add_argument("--thickness", type=float, default=8.0)
    p.add_argument("--bore", type=float, default=8.0)
    knob_group = p.add_argument_group("kolečko (knob), rozměry v mm")
    knob_group.add_argument("--outer-d", type=float, default=75.0, help="průměr přes laloky")
    knob_group.add_argument("--root-d", type=float, default=57.5, help="průměr v zářezech")
    knob_group.add_argument("--knob-height", type=float, default=26.0,
                            help="výška těla hvězdice, bez nálitku")
    knob_group.add_argument("--pockets", type=int, default=8)
    knob_group.add_argument("--pocket-d", type=float, default=9.4)
    knob_group.add_argument("--pocket-circle-d", type=float, default=52.0)
    knob_group.add_argument("--pocket-depth", type=float, default=22.0)
    knob_group.add_argument("--thread-d", type=float, default=24.0, help="velký průměr závitu")
    knob_group.add_argument("--pitch", type=float, default=3.0, help="stoupání závitu")
    knob_group.add_argument("--thread-depth", type=float, default=22.0, help="hloubka díry")
    knob_group.add_argument("--recess-d", type=float, default=52.5,
                            help="průměr zapuštěného kotouče na pohledové straně")
    knob_group.add_argument("--recess-depth", type=float, default=1.5,
                            help="hloubka vybrání; 0 = ploché čelo")
    knob_group.add_argument("--dot-d", type=float, default=2.4,
                            help="průměr tečky uprostřed vybrání")
    knob_group.add_argument("--dot-depth", type=float, default=0.8,
                            help="hloubka tečky; 0 = hladké dno")
    knob_group.add_argument("--boss-d", type=float, default=38.0,
                            help="průměr závitového nálitku pod tělem")
    knob_group.add_argument("--boss-h", type=float, default=4.0,
                            help="o kolik nálitek vystupuje pod tělo hvězdice")
    knob_group.add_argument("--edge-r", type=float, default=1.5,
                            help="poloměr zaoblení obvodových hran; 0 = ostrá hrana")
    knob_group.add_argument("--ring-w", type=float, default=1.0,
                            help="šířka prstence kolem kapes")
    knob_group.add_argument("--ring-depth", type=float, default=1.0,
                            help="hloubka prstence; 0 = bez prstence")
    p.add_argument("--preview", default=None, help="vykreslit náhled do PNG")
    args = p.parse_args(argv)

    out = args.out or f"{args.shape}.stl"
    directory = os.path.dirname(os.path.abspath(out))
    os.makedirs(directory, exist_ok=True)

    m = build(args)
    if out.lower().endswith(".obj"):
        m.write_obj(out, name=args.shape)
    else:
        m.write_stl(out, name=args.shape)

    if args.preview:
        from preview import render
        os.makedirs(os.path.dirname(os.path.abspath(args.preview)), exist_ok=True)
        render(m, args.preview)
        print(f"náhled: {args.preview}")

    lo, hi = m.bounds()
    size = tuple(round(hi[i] - lo[i], 2) for i in range(3))
    print(f"{out}: {len(m.vertices)} vrcholů, {len(m.faces)} trojúhelníků, rozměry {size} mm")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
