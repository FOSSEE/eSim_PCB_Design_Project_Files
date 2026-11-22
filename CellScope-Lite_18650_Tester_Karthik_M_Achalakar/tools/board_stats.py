"""Collect board statistics for the report (KiCad python). Usage: board_stats.py board.kicad_pcb out.json"""
import json
import os
import sys

import pcbnew


def main(pcb, out):
    b = pcbnew.LoadBoard(pcb)
    tracks = [t for t in b.GetTracks() if t.GetClass() == "PCB_TRACK"]
    vias = [t for t in b.GetTracks() if t.GetClass() == "PCB_VIA"]
    length = sum(pcbnew.ToMM(t.GetLength()) for t in tracks)
    nets = len([n for n in b.GetNetsByName().keys() if str(n) and not str(n).startswith("unconnected")])
    lin = 0.0
    csv = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "sim", "out_dc.csv")
    if os.path.exists(csv):
        rows = [l.split() for l in open(csv).read().splitlines()[1:] if l.strip()]
        errs = [abs(float(r[1]) / 0.1 - float(r[0]) / 0.1) / (float(r[0]) / 0.1) * 100 for r in rows if float(r[0]) > 0.01]
        lin = max(errs) if errs else 0.0
    d = dict(tracks=len(tracks), vias=len(vias), track_length_mm=round(length, 1), nets=nets,
             footprints=len(b.GetFootprints()), layers=b.GetCopperLayerCount(), lin_err=lin)
    json.dump(d, open(out, "w"), indent=1)
    print(d)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
