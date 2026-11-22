"""Dump pad / hole / outline geometry of a .kicad_pcb to JSON for the router (KiCad python)."""
import json
import sys

import pcbnew


def poly_pts(sps):
    out = []
    for i in range(sps.OutlineCount()):
        ol = sps.Outline(i)
        out.append([(pcbnew.ToMM(ol.CPoint(k).x), pcbnew.ToMM(ol.CPoint(k).y)) for k in range(ol.PointCount())])
    return out


def main(pcb, out):
    b = pcbnew.LoadBoard(pcb)
    pads = []
    for fp in b.GetFootprints():
        for p in fp.Pads():
            layers = []
            if p.IsOnLayer(pcbnew.F_Cu):
                layers.append("F")
            if p.IsOnLayer(pcbnew.B_Cu):
                layers.append("B")
            if not layers:
                continue
            poly = p.GetEffectivePolygon(pcbnew.F_Cu if "F" in layers else pcbnew.B_Cu, pcbnew.ERROR_INSIDE)
            drill = pcbnew.ToMM(p.GetDrillSize().x) if p.GetDrillSize().x > 0 else 0
            pads.append(dict(ref=fp.GetReference(), num=p.GetNumber(), net=p.GetNetname(),
                             x=pcbnew.ToMM(p.GetPosition().x), y=pcbnew.ToMM(p.GetPosition().y),
                             layers=layers, poly=poly_pts(poly), drill=drill,
                             tht=p.GetAttribute() in (pcbnew.PAD_ATTRIB_PTH, pcbnew.PAD_ATTRIB_NPTH)))
    bb = b.GetBoardEdgesBoundingBox()
    outline = dict(x0=pcbnew.ToMM(bb.GetX()), y0=pcbnew.ToMM(bb.GetY()),
                   x1=pcbnew.ToMM(bb.GetRight()), y1=pcbnew.ToMM(bb.GetBottom()))
    json.dump(dict(pads=pads, outline=outline), open(out, "w"))
    print("pads:", len(pads))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
