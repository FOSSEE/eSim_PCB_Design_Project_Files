"""Place every reference designator where it does not touch pads, other silk or the board edge (KiCad python).

Usage: python tidy_silk.py <board.kicad_pcb>
"""
import sys

import pcbnew

MM = pcbnew.FromMM


def rect(bb, grow=0.0):
    g = MM(grow)
    return (bb.GetLeft() - g, bb.GetTop() - g, bb.GetRight() + g, bb.GetBottom() + g)


def hit(a, b):
    return not (a[2] <= b[0] or b[2] <= a[0] or a[3] <= b[1] or b[3] <= a[1])


def main(path):
    board = pcbnew.LoadBoard(path)
    eb = board.GetBoardEdgesBoundingBox()
    inner = rect(eb, -0.6)
    obstacles = []
    for fp in board.GetFootprints():
        for p in fp.Pads():
            if p.IsOnLayer(pcbnew.F_Cu) or p.IsOnLayer(pcbnew.F_Mask):
                obstacles.append(rect(p.GetBoundingBox(), 0.15))
        for g in fp.GraphicalItems():
            if g.GetLayer() == pcbnew.F_SilkS and g.GetClass() != "PCB_TEXT":
                obstacles.append(rect(g.GetBoundingBox(), 0.1))
    for d in board.GetDrawings():
        if d.GetLayer() == pcbnew.F_SilkS:
            obstacles.append(rect(d.GetBoundingBox(), 0.1))
    for v in board.GetTracks():
        if v.GetClass() == "PCB_VIA":
            obstacles.append(rect(v.GetBoundingBox(), 0.1))   # via annular rings are mask-exposed
    placed, moved, failed = [], 0, []
    fps = sorted(board.GetFootprints(), key=lambda f: f.GetBoundingBox(False, False).GetArea())
    for fp in fps:
        ref = fp.Reference()
        if not ref.IsVisible() or ref.GetLayer() != pcbnew.F_SilkS:
            continue
        cy = fp.GetCourtyard(pcbnew.F_CrtYd)
        bb = cy.BBox() if cy.OutlineCount() else fp.GetBoundingBox(False, False)
        L, T, R, B = bb.GetLeft(), bb.GetTop(), bb.GetRight(), bb.GetBottom()
        cx, cyy = (L + R) // 2, (T + B) // 2
        best = None
        for size in (0.8,):
            ref.SetTextSize(pcbnew.VECTOR2I(MM(size), MM(size)))
            ref.SetTextThickness(MM(0.12))
            for ang in (0, 90):
                ref.SetTextAngleDegrees(ang)
                tb = ref.GetBoundingBox()
                hw, hh = tb.GetWidth() // 2, tb.GetHeight() // 2
                cands = []
                for g in (0.25, 0.7, 1.3):
                    gap = MM(g)
                    cands += [(cx, T - hh - gap), (cx, B + hh + gap), (R + hw + gap, cyy), (L - hw - gap, cyy),
                              (R + hw + gap, T - hh), (L - hw - gap, T - hh), (R + hw + gap, B + hh), (L - hw - gap, B + hh)]
                cands.append((cx, cyy))
                for (x, y) in cands:
                    ref.SetPosition(pcbnew.VECTOR2I(int(x), int(y)))
                    r = rect(ref.GetBoundingBox(), 0.05)
                    if not (r[0] >= inner[0] and r[1] >= inner[1] and r[2] <= inner[2] and r[3] <= inner[3]):
                        continue
                    if any(hit(r, o) for o in obstacles) or any(hit(r, o) for o in placed):
                        continue
                    best = (x, y, ang, size, r)
                    break
                if best:
                    break
            if best:
                break
        if best:
            x, y, ang, size, r = best
            ref.SetTextSize(pcbnew.VECTOR2I(MM(size), MM(size)))
            ref.SetTextAngleDegrees(ang)
            ref.SetPosition(pcbnew.VECTOR2I(int(x), int(y)))
            placed.append(r)
            moved += 1
        else:
            failed.append(ref.GetText())
            ref.SetVisible(False)     # documented on the assembly drawing / fab layer instead
    board.Save(path)
    print("refs placed %d, hidden (no room) %d %s" % (moved, len(failed), failed))


if __name__ == "__main__":
    main(sys.argv[1])
