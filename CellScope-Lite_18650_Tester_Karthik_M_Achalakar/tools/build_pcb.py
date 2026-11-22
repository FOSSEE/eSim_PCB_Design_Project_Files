"""Build CellScope-Lite.kicad_pcb from the eSchema netlist (run with KiCad's bundled python).

Usage: python build_pcb.py <netlist.net> <footprint_dir> <out.kicad_pcb>

* 4-layer stack: F.Cu signal / In1.Cu GND plane / In2.Cu +3V3 plane / B.Cu signal
* Every footprint gets the schematic symbol path (KIID) so eSim's
  "Update PCB from Schematic" sees a 1:1 match (no adds/deletes).
"""
import os
import sys

import pcbnew

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from sexpr import parse, find, find_all  # noqa: E402
from placement import PLACE, BOARD_W, BOARD_H, ORIGIN  # noqa: E402

MM = pcbnew.FromMM


def P(x, y):
    return pcbnew.VECTOR2I(MM(ORIGIN[0] + x), MM(ORIGIN[1] + y))


def read_netlist(path):
    t = parse(open(path, encoding="utf-8").read())
    comps = {}
    for c in find_all(find(t, "components"), "comp"):
        ref = find(c, "ref")[1]
        comps[ref] = dict(value=find(c, "value")[1], fp=find(c, "footprint")[1] if find(c, "footprint") else "",
                          tstamps=find(c, "tstamps")[1:] if find(c, "tstamps") else [find(c, "tstamp")[1]],
                          sheet=find(c, "sheetpath"))
    nets = []
    for n in find_all(find(t, "nets"), "net"):
        name = find(n, "name")[1]
        nodes = [(find(x, "ref")[1], find(x, "pin")[1]) for x in find_all(n, "node")]
        nets.append((name, nodes))
    return comps, nets


def relink_models(path):
    """Point 3D models at the project-bundled copies (eSim 2.6 ships no KiCad 3D library)."""
    import re
    txt = open(path, encoding="utf-8").read()

    def rep(m):
        base = m.group(1).replace("\\", "/").split("/")[-1]
        if base.startswith("USB_C_Receptacle_HRO_TYPE-C-31-M-12"):
            base = base.rsplit(".", 1)[0] + ".wrl"
        return '(model "${KIPRJMOD}/3dmodels/%s"' % base
    txt = re.sub(r'\(model "([^"]+)"', rep, txt)
    open(path, "w", encoding="utf-8", newline="\n").write(txt)


def main(netfile, fpdir, out):
    comps, nets = read_netlist(netfile)
    board = pcbnew.BOARD()
    board.SetCopperLayerCount(4)
    ds = board.GetDesignSettings()
    ds.SetCopperLayerCount(4)
    ds.m_TrackMinWidth = MM(0.15)
    ds.m_MinClearance = MM(0.15)
    ds.m_ViasMinSize = MM(0.5)
    ds.m_MinThroughDrill = MM(0.25)
    ds.m_CopperEdgeClearance = MM(0.3)
    ds.m_HoleClearance = MM(0.25)

    # board outline: rounded rectangle on Edge.Cuts
    r = 3.0
    w, h = BOARD_W, BOARD_H
    segs = [((r, 0), (w - r, 0)), ((w, r), (w, h - r)), ((w - r, h), (r, h)), ((0, h - r), (0, r))]
    for a, b in segs:
        s = pcbnew.PCB_SHAPE(board)
        s.SetShape(pcbnew.SHAPE_T_SEGMENT)
        s.SetStart(P(*a))
        s.SetEnd(P(*b))
        s.SetLayer(pcbnew.Edge_Cuts)
        s.SetWidth(MM(0.1))
        board.Add(s)
    import math
    k = r * (1 - math.sqrt(0.5))
    for (sx, sy), (mx, my), (ex, ey) in [((0, r), (k, k), (r, 0)), ((w - r, 0), (w - k, k), (w, r)),
                                         ((w, h - r), (w - k, h - k), (w - r, h)), ((r, h), (k, h - k), (0, h - r))]:
        a = pcbnew.PCB_SHAPE(board)
        a.SetShape(pcbnew.SHAPE_T_ARC)
        a.SetArcGeometry(P(sx, sy), P(mx, my), P(ex, ey))
        a.SetLayer(pcbnew.Edge_Cuts)
        a.SetWidth(MM(0.1))
        board.Add(a)

    netinfo = {}
    for name, _ in nets:
        ni = pcbnew.NETINFO_ITEM(board, name)
        board.Add(ni)
        netinfo[name] = ni
    padnet = {}
    for name, nodes in nets:
        for ref, pin in nodes:
            padnet[(ref, pin)] = name

    missing = []
    for ref, c in sorted(comps.items()):
        lib, name = c["fp"].split(":")
        fp = pcbnew.FootprintLoad(os.path.join(fpdir, lib + ".pretty"), name)
        if fp is None:
            missing.append(c["fp"])
            continue
        fp.SetReference(ref)
        fp.SetValue(c["value"])
        fp.SetFPID(pcbnew.LIB_ID(lib, name))
        fp.SetPath(pcbnew.KIID_PATH("/" + c["tstamps"][0]))
        fp.SetSheetname("Root")
        fp.SetSheetfile("CellScope-Lite.kicad_sch")
        if ref in PLACE:
            x, y, rot, side = PLACE[ref]
            fp.SetPosition(P(x, y))
            if side == "B":
                fp.Flip(fp.GetPosition(), False)
            fp.SetOrientationDegrees(rot)
        else:
            print("WARNING: no placement for", ref)
        board.Add(fp)
        for pad in fp.Pads():
            n = padnet.get((ref, pad.GetNumber()))
            if n:
                pad.SetNet(netinfo[n])
    if missing:
        raise SystemExit("missing footprints: %s" % missing)

    # bottom silkscreen: branding + pinout + key specs (mirrored, read from the back)
    # (text, size, thickness, y) -- y chosen so lines clear the holder's NPTH locating holes at y = 51 and 67 mm
    lines = [("FOSSEE eSim Internship Autumn 2026 - Task 7", 1.2, 0.18, 47.6),
             ("CellScope-Lite", 3.0, 0.45, 51.2),
             ("18650 Li-ion charger & capacity tester  rev 1.0", 1.5, 0.22, 54.9),
             ("HOST J2: 1 3V3  2 SDA  3 SCL  4 ALERT  5 EXT_SET  6 GND", 1.2, 0.18, 57.4),
             ("QWIIC J3: GND 3V3 SDA SCL   |   INA226 I2C addr 0x40", 1.2, 0.18, 59.4),
             ("Charge 1.0 A CC/CV 4.2 V  |  Load 0-0.975 A (V_SET / 0.1 ohm)", 1.2, 0.18, 61.4),
             ("Cut-off 3.01 V / release 3.50 V  |  JP1: 1-2 trimmer, 2-3 DAC", 1.2, 0.18, 63.4)]
    for txt, size, th, y in lines:
        t = pcbnew.PCB_TEXT(board)
        t.SetText(txt)
        t.SetLayer(pcbnew.B_SilkS)
        t.SetTextSize(pcbnew.VECTOR2I(MM(size), MM(size)))
        t.SetTextThickness(MM(th))
        t.SetMirrored(True)
        t.SetHorizJustify(pcbnew.GR_TEXT_H_ALIGN_CENTER)
        t.SetPosition(P(BOARD_W / 2, y))
        board.Add(t)
    # top silkscreen function labels at the edge controls
    for txt, x, yy in [("USB-C 5V", 6.0, 24.6), ("PWR", 15.0, 5.4), ("CHRG", 24.0, 5.4), ("FULL", 31.0, 5.4),
                       ("CUTOFF", 38.0, 5.4), ("I SET", 45.0, 9.3), ("LOAD", 56.5, 7.8), ("HOST", 71.4, 6.6),
                       ("QWIIC", 87.0, 9.0), ("+", 12.3, 50.5), ("-", 91.7, 50.5), ("HEATSINK", 96.5, 29.5)]:
        t = pcbnew.PCB_TEXT(board)
        t.SetText(txt)
        t.SetLayer(pcbnew.F_SilkS)
        t.SetTextSize(pcbnew.VECTOR2I(MM(0.9), MM(0.9)))
        t.SetTextThickness(MM(0.15))
        t.SetPosition(P(x, yy))
        if txt == "HEATSINK":
            t.SetTextAngleDegrees(90)
        board.Add(t)

    board.Save(out)
    relink_models(out)
    print("saved", out, "footprints:", len(board.GetFootprints()), "nets:", len(nets))


if __name__ == "__main__":
    main(*sys.argv[1:4])
