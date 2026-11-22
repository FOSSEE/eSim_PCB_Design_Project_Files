import sys, os, pcbnew
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "design"))
import circuit
F = sys.argv[1]
seen = {}
for p in circuit.PARTS:
    l, n = p["fp"].split(":")
    if p["fp"] not in seen:
        fp = pcbnew.FootprintLoad(os.path.join(F, l + ".pretty"), n)
        cy = fp.GetCourtyard(pcbnew.F_CrtYd)
        bb = cy.BBox() if cy.OutlineCount() else fp.GetBoundingBox(False, False)
        pads = " ".join("%s@(%.2f,%.2f)" % (pd.GetNumber(), pcbnew.ToMM(pd.GetPosition().x), pcbnew.ToMM(pd.GetPosition().y)) for pd in fp.Pads())[:140]
        seen[p["fp"]] = (pcbnew.ToMM(bb.GetX()), pcbnew.ToMM(bb.GetY()), pcbnew.ToMM(bb.GetWidth()), pcbnew.ToMM(bb.GetHeight()), pads)
    x, y, w, h, pads = seen[p["fp"]]
    print("%-5s %-42s crt x%.2f..%.2f y%.2f..%.2f (%.1fx%.1f)  %s" % (p["ref"], n[:42], x, x + w, y, y + h, w, h, pads if p["ref"] in ("BT1", "Q3", "J1", "RV1", "SW1", "J3", "JP1", "J2", "U1") else ""))
