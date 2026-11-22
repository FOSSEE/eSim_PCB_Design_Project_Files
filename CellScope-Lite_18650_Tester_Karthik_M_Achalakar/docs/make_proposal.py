"""Build docs/CellScope-Lite_Proposal.pdf: the Task 7 PCB design proposal (reportlab)."""
import os

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "docs", "CellScope-Lite_Proposal.pdf")
AUTHOR = os.environ.get("REPORT_AUTHOR", "Karthik M Achalakar, Ramaiah Institute of Technology, Bengaluru "
                                          "(B.E. Electrical and Electronics Engineering, 3rd year)")

ss = getSampleStyleSheet()
H1 = ParagraphStyle("H1", parent=ss["Heading1"], fontSize=13.5, spaceBefore=6, spaceAfter=4, textColor=colors.HexColor("#123b6b"))
B = ParagraphStyle("B", parent=ss["BodyText"], fontSize=9.6, leading=13, spaceAfter=3)
T = ParagraphStyle("T", parent=H1, fontSize=19, leading=23, alignment=TA_CENTER, spaceAfter=2)
SUB = ParagraphStyle("S", parent=B, fontSize=10.5, alignment=TA_CENTER, textColor=colors.HexColor("#333"))
CAP = ParagraphStyle("C", parent=B, fontSize=8.2, alignment=TA_CENTER, textColor=colors.HexColor("#555"))
W = A4[0] - 36 * mm


def table(rows, widths, fs=8.6):
    t = Table([[Paragraph(str(c), ParagraphStyle("c", parent=B, fontSize=fs, leading=fs + 2.4)) for c in r] for r in rows],
              colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#dfe8f3")),
                           ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9aa9bb")),
                           ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    return t


def main():
    s = [Paragraph("PCB Design Proposal: CellScope-Lite", T),
         Paragraph("18650 Li-ion Charger &amp; Constant-Current Capacity Tester (4-layer PCB)", SUB),
         Paragraph("FOSSEE eSim Semester Long Internship - Autumn 2026, Task 7: PCB Design using eSim", SUB),
         Paragraph(AUTHOR, SUB), Spacer(1, 4 * mm),
         Paragraph("1. Idea and motivation", H1),
         Paragraph("18650 Li-ion cells are everywhere (power banks, laptops, e-bikes), but their printed capacity is often wrong, "
                   "and second-hand cells lose capacity with age. CellScope-Lite is a small board that <b>charges</b> a cell, then "
                   "<b>discharges</b> it at a precise constant current and <b>measures</b> the energy delivered, so the real "
                   "capacity (mAh / mWh) can be known before the cell is reused.", B),
         Paragraph("2. Basic functionality", H1),
         table([["Function", "How"],
                ["USB-C 5 V input", "Sink identification (5.1 k on CC1/CC2), 1.5 A polyfuse and TVS protection"],
                ["Charging", "TP4056 linear CC/CV charger, 1.0 A to 4.20 V, with CHRG / FULL LEDs"],
                ["Cell protection", "DW01A + FS8205A: over-charge 4.3 V, over-discharge 2.4 V, over-current and short"],
                ["Constant-current load", "Op-amp + logic-level MOSFET + 0.1 ohm shunt: I = V_SET / 0.1 ohm, 0 to 0.975 A, "
                                          "set by a 25-turn trimmer or an external DAC"],
                ["Automatic cut-off", "Comparator with hysteresis stops the load at 3.0 V (release 3.5 V); precision 2.048 V reference"],
                ["Measurement", "INA226 16-bit monitor (voltage, current, power) over I2C, Kelvin-connected to the shunt"],
                ["Interfaces", "6-pin HOST header + Qwiic connector, 7 test points, status LEDs, LOAD on/off switch"]],
               [36 * mm, W - 36 * mm]),
         Spacer(1, 3 * mm)]
    bd = os.path.join(ROOT, "docs", "img", "block_diagram.png")
    if os.path.exists(bd):
        from PIL import Image as PI
        w, h = PI.open(bd).size
        s += [Image(bd, width=W * 0.9, height=W * 0.9 * h / w), Paragraph("Block diagram", CAP)]
    s += [Paragraph("3. PCB plan", H1),
          table([["Item", "Plan"],
                 ["Layers", "4 copper layers: F.Cu signals / In1.Cu GND plane / In2.Cu +3V3 plane / B.Cu signals"],
                 ["Size", "About 104 x 72 mm with the 18650 holder on the board, 4 x M3 mounting holes"],
                 ["Parts", "About 76 components, mostly SMD (0603/0805, SOIC, SOT-23, MSOP), TO-220 MOSFET at the edge for a heatsink"],
                 ["Key layout points", "Short 1 A current loops with wide power tracks, Kelvin sensing at the shunt, thermal vias "
                                       "under the charger, analog parts away from the power path"],
                 ["Verification", "ERC, footprint check, Sch-to-PCB update, DRC with schematic parity, 3D viewer; Ngspice "
                                  "simulation of the constant-current loop and the cut-off comparator"]],
                [36 * mm, W - 36 * mm]),
          Paragraph("4. Design flow in eSim", H1),
          Paragraph("Schematic in eSchema, footprint assignment, Update PCB from Schematic, placement and routing on 4 layers, "
                    "DRC, and 3D viewer, all inside eSim (KiCad). The project is kept in the KiCad 6.0 file format so that it "
                    "opens in eSim 2.5 as well as in newer eSim versions.", B),
          Paragraph("5. Deliverables", H1),
          Paragraph("Complete eSim project folder (schematic, PCB, libraries, 3D models), a detailed PDF report, ERC/DRC reports, "
                    "Ngspice simulation files and manufacturing outputs (Gerber, drill, BOM, pick-and-place, STEP).", B)]
    SimpleDocTemplate(OUT, pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=14 * mm, bottomMargin=14 * mm,
                      title="CellScope-Lite - PCB design proposal", author=AUTHOR).build(s)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
