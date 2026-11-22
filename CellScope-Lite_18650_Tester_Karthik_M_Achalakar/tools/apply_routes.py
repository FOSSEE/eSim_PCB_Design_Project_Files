"""Apply build/routes.json to the board, add planes / pours, fill zones (KiCad python).

Usage: python apply_routes.py <skeleton.kicad_pcb> <routes.json> <out.kicad_pcb>
"""
import json
import sys

import pcbnew

MM = pcbnew.FromMM
LAYER = {"F": pcbnew.F_Cu, "B": pcbnew.B_Cu}


def add_zone(board, netname, layer, prio, outline_pts, clearance=0.25, minw=0.25, name=""):
    z = pcbnew.ZONE(board)
    z.SetLayer(layer)
    z.SetNet(board.FindNet(netname))
    z.SetAssignedPriority(prio)
    z.SetLocalClearance(MM(clearance))
    z.SetMinThickness(MM(minw))
    z.SetPadConnection(pcbnew.ZONE_CONNECTION_THT_THERMAL)  # SMD pads solid, THT thermal relief
    z.SetThermalReliefGap(MM(0.3))
    z.SetThermalReliefSpokeWidth(MM(0.4))
    z.SetIslandRemovalMode(pcbnew.ISLAND_REMOVAL_MODE_ALWAYS)
    if name:
        z.SetZoneName(name)
    ol = z.Outline()
    ol.NewOutline()
    for x, y in outline_pts:
        ol.Append(MM(x), MM(y))
    board.Add(z)
    return z


def main(skeleton, routes, pcb):
    """skeleton = placed but unrouted board (from build_pcb.py); result is written to pcb."""
    board = pcbnew.LoadBoard(skeleton)
    assert len(board.GetTracks()) == 0 and len(list(board.Zones())) == 0, "skeleton must be unrouted"
    r = json.load(open(routes))
    for t in r["tracks"]:
        tr = pcbnew.PCB_TRACK(board)
        tr.SetStart(pcbnew.VECTOR2I(MM(t["x1"]), MM(t["y1"])))
        tr.SetEnd(pcbnew.VECTOR2I(MM(t["x2"]), MM(t["y2"])))
        tr.SetWidth(MM(t["w"]))
        tr.SetLayer(LAYER[t["layer"]])
        tr.SetNet(board.FindNet(t["net"]))
        board.Add(tr)
    for v in r["vias"]:
        via = pcbnew.PCB_VIA(board)
        via.SetPosition(pcbnew.VECTOR2I(MM(v["x"]), MM(v["y"])))
        via.SetWidth(pcbnew.F_Cu, MM(v["d"]))
        via.SetDrill(MM(v["drill"]))
        via.SetViaType(pcbnew.VIATYPE_THROUGH)
        via.SetLayerPair(pcbnew.F_Cu, pcbnew.B_Cu)
        via.SetNet(board.FindNet(v["net"]))
        board.Add(via)

    bb = board.GetBoardEdgesBoundingBox()
    x0, y0 = pcbnew.ToMM(bb.GetX()) + 0.05, pcbnew.ToMM(bb.GetY()) + 0.05
    x1, y1 = pcbnew.ToMM(bb.GetRight()) - 0.05, pcbnew.ToMM(bb.GetBottom()) - 0.05
    rect = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
    add_zone(board, "GND", pcbnew.In1_Cu, 0, rect, name="GND plane")
    add_zone(board, "+3V3", pcbnew.In2_Cu, 0, rect, name="3V3 plane")
    add_zone(board, "GND", pcbnew.F_Cu, 0, rect, clearance=0.3, name="GND pour top")
    add_zone(board, "GND", pcbnew.B_Cu, 0, rect, clearance=0.3, name="GND pour bottom")
    filler = pcbnew.ZONE_FILLER(board)
    filler.Fill(board.Zones())
    board.Save(pcb)
    print("applied tracks=%d vias=%d zones=%d" % (len(r["tracks"]), len(r["vias"]), len(list(board.Zones()))))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
