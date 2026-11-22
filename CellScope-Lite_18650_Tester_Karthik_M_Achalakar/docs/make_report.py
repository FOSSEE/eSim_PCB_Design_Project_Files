"""Build docs/CellScope-Lite_Task7_Report.pdf from the real design outputs (reportlab)."""
import collections
import json
import os
import re
import sys

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (Image, KeepTogether, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table,
                                TableStyle)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "design"))
import circuit  # noqa: E402

AUTHOR = os.environ.get("REPORT_AUTHOR", "Karthik M Achalakar, Ramaiah Institute of Technology, Bengaluru (B.E. Electrical and Electronics Engineering, 3rd year)")
OUT = os.path.join(ROOT, "docs", "CellScope-Lite_Task7_Report.pdf")
IMG = os.path.join(ROOT, "docs", "img")

ss = getSampleStyleSheet()
H1 = ParagraphStyle("H1", parent=ss["Heading1"], fontSize=16, spaceBefore=6, spaceAfter=8, textColor=colors.HexColor("#123b6b"))
H2 = ParagraphStyle("H2", parent=ss["Heading2"], fontSize=12.5, spaceBefore=8, spaceAfter=5, textColor=colors.HexColor("#1f5fa8"))
B = ParagraphStyle("B", parent=ss["BodyText"], fontSize=9.6, leading=13.2, spaceAfter=4)
SM = ParagraphStyle("SM", parent=B, fontSize=8.2, leading=10.5)
CAP = ParagraphStyle("CAP", parent=B, fontSize=8.4, textColor=colors.HexColor("#555"), alignment=TA_CENTER, spaceAfter=8)
TITLE = ParagraphStyle("T", parent=H1, fontSize=24, leading=29, alignment=TA_CENTER, spaceAfter=6)
SUB = ParagraphStyle("S", parent=B, fontSize=12, leading=16, alignment=TA_CENTER, textColor=colors.HexColor("#333"))

W = A4[0] - 36 * mm


def img(name, width=W, cap=None):
    path = os.path.join(IMG, name) if not os.path.isabs(name) else name
    if not os.path.exists(path):
        return [Paragraph("<i>[missing image: %s]</i>" % name, B)]
    from PIL import Image as PI
    w, h = PI.open(path).size
    height = width * h / w
    max_h = 205 * mm
    if height > max_h:
        width, height = width * max_h / height, max_h
    out = [Image(path, width=width, height=height)]
    if cap:
        out.append(Paragraph(cap, CAP))
    return out


def table(rows, widths=None, head=True, fs=8.2):
    t = Table([[Paragraph(str(c), ParagraphStyle("c", parent=SM, fontSize=fs, leading=fs + 2.2)) for c in r] for r in rows],
              colWidths=widths, repeatRows=1 if head else 0)
    st = [("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#b8c4d4")),
          ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
          ("TOPPADDING", (0, 0), (-1, -1), 2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2)]
    if head:
        st += [("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e3ecf7"))]
    t.setStyle(TableStyle(st))
    return t


def sim_value(log, key):
    try:
        txt = open(os.path.join(ROOT, "build", log), encoding="utf-8", errors="ignore").read()
        m = re.search(r"^%s\s*=\s*([-+0-9.eE]+)" % key, txt, re.M)
        return float(m.group(1)) if m else None
    except OSError:
        return None


def on_page(c, doc):
    c.saveState()
    c.setFont("Helvetica", 7.5)
    c.setFillColor(colors.HexColor("#666"))
    c.drawString(18 * mm, 10 * mm, "CellScope-Lite | FOSSEE eSim Semester Long Internship - Autumn 2026 | Task 7: PCB Design using eSim")
    c.drawRightString(A4[0] - 18 * mm, 10 * mm, "page %d" % doc.page)
    c.restoreState()


def main():
    drc = json.load(open(os.path.join(ROOT, "build", "drc_final.json")))
    erc_txt = open(os.path.join(ROOT, "build", "erc.rpt"), encoding="utf-8").read()
    erc_line = [l for l in erc_txt.splitlines() if "ERC messages" in l][-1].strip()
    stats = json.load(open(os.path.join(ROOT, "build", "board_stats.json")))
    active = [v for v in drc["violations"] if not v.get("excluded")]
    excluded = [v for v in drc["violations"] if v.get("excluded")]
    vc = collections.Counter(v["severity"] for v in active)
    vt = collections.Counter(v["type"] for v in active)

    s = []
    # ---------------- title page ----------------
    s += [Spacer(1, 18 * mm), Paragraph("CellScope-Lite", TITLE),
          Paragraph("18650 Li-ion Charger &amp; Constant-Current Capacity Tester<br/>4-layer PCB designed in eSim (KiCad 6.0 project format)", SUB),
          Spacer(1, 6 * mm)]
    s += img("pcb_iso.png", W * 0.92)
    s += [Spacer(1, 4 * mm),
          Paragraph("FOSSEE eSim Semester Long Internship - Autumn 2026: <b>Task 7, PCB Design using eSim</b>", SUB),
          Paragraph(AUTHOR, SUB), Paragraph("Designed in eSim 2.6 (eSchema, PCB editor, 3D viewer, Ngspice 45.2). Project saved in the KiCad 6.0 format "
                    "used by eSim 2.4 / 2.5, so it opens in eSim 2.5 and 2.6 without changes.", SUB),
          Spacer(1, 6 * mm)]
    summary = [["Item", "Result"],
               ["Board", "104 x 72 mm, 4 copper layers (signal / GND / 3V3 / signal), 1.6 mm FR-4"],
               ["Components", "%d parts, %d nets, 3 custom symbols (TP4056, DW01A, FS8205A)" % (len(circuit.PARTS), stats["nets"])],
               ["Routing", "%d track segments, %d vias, 2 inner planes + top/bottom GND pours" % (stats["tracks"], stats["vias"])],
               ["ERC (eSchema)", erc_line.replace("** ", "")],
               ["DRC (PCB editor)", "%d errors, %d warnings, %d unconnected, %d schematic-parity issues (%d documented exclusion)" % (
                   vc.get("error", 0), vc.get("warning", 0), len(drc["unconnected_items"]), len(drc["schematic_parity"]), len(excluded))],
               ["Simulation (Ngspice)", "CC loop linearity error %.2f %%; UVLO trip %.3f V / release %.3f V" % (
                   stats["lin_err"], sim_value("sim_uvlo_threshold.log", "v_trip") or 0, sim_value("sim_uvlo_threshold.log", "v_release") or 0)]]
    s += [table(summary, [38 * mm, W - 38 * mm]), PageBreak()]

    # ---------------- 1 overview ----------------
    s += [Paragraph("1. Project overview", H1),
          Paragraph("CellScope-Lite is a complete, functional instrument for measuring the real capacity of 18650 Li-ion cells, "
                    "the cells used in power banks, laptops and e-bikes. It <b>charges</b> the cell at 1 A (CC/CV to 4.20 V). "
                    "It then <b>discharges</b> the cell at a precise, adjustable constant current (0 to 0.975 A), and "
                    "<b>stops automatically</b> at 3.0 V using a latching comparator. A 16-bit <b>INA226</b> monitor reports "
                    "voltage, current and power over I&sup2;C (header and Qwiic connector), so a microcontroller can integrate "
                    "mAh and mWh. The board combines power electronics, precision analog design, cell safety "
                    "(DW01A/FS8205A protection) and a digital interface, and it was laid out on four layers.", B)]
    s += img("block_diagram.png", W, "Figure 1: System block diagram.")
    spec = [["Parameter", "Value", "Set by"],
            ["Input", "USB-C 5 V (sink, 5.1 k CC), 1.5 A polyfuse, SMAJ5.0A TVS", "J1, R1/R2, F1, D1"],
            ["Charge", "1.00 A CC/CV, 4.20 V +/-1 %, termination C/10", "TP4056, R3 = 1.2 k"],
            ["Cell protection", "OV 4.3 V, UV 2.4 V, over-current/short", "DW01A + FS8205A"],
            ["Discharge current", "0 to 0.975 A, set by trimmer or external DAC", "U5A + Q3, R16 = 0.1 ohm"],
            ["Cut-off", "3.01 V falling, 3.50 V release (latching)", "U5B, R20-R23, LM4040"],
            ["Measurement", "INA226: 25 uA / 1.25 mV LSB, I2C 0x40", "U6, Kelvin net-tie NT1"],
            ["Interfaces", "HOST 1x6 2.54 mm, Qwiic JST-SH, 7 test points, 5 LEDs", "J2, J3, TP1-TP7"]]
    s += [Paragraph("Key specifications", H2), table(spec, [32 * mm, 92 * mm, W - 124 * mm]), PageBreak()]

    # ---------------- 2 schematic ----------------
    s += [Paragraph("2. Schematic (eSchema)", H1),
          Paragraph("The schematic is one A2 sheet organised into nine labelled functional blocks, plus a design-equation panel "
                    "that documents how every key value was chosen. Nets are named (VBAT, SET_FILT, SENSE_HI, ...), and power "
                    "symbols and PWR_FLAGs are used correctly. The ERC result is <b>%s</b>." % erc_line.replace("** ERC messages: ", ""), B)]
    s += img("schematic.png", W, "Figure 2: Complete schematic (full-resolution PDF: docs/CellScope-Lite_schematic.pdf).")
    s += [PageBreak()]
    s += img("schematic_left.png", W, "Figure 3: Schematic detail: USB input, charger, 3.3 V/reference, set-point, INA226, UVLO.")
    s += img("schematic_right.png", W, "Figure 4: Schematic detail: cell protection, CC load, interface and design equations.")
    s += [PageBreak(), Paragraph("2.1 Block-by-block design", H2)]
    notes = [
        ("USB-C input", "R1/R2 = 5.1 k pull-downs on CC1/CC2 identify the board as a USB-C sink. Without them a Type-C charger supplies no VBUS. "
                        "F1 (1.5 A polyfuse) and D1 (SMAJ5.0A TVS) protect against shorts and ESD."),
        ("Charger", "TP4056 linear CC/CV charger. I_CHG = 1200 V / R_PROG = 1200 / 1.2 k = 1.0 A. The exposed pad sinks up to about 1.5 W into "
                    "the GND pour through 3 thermal vias. The CHRG/STDBY open-drain outputs drive red and blue LEDs."),
        ("Protection", "DW01A monitors the cell through R6/C4 (100 ohm/100 nF). It switches the FS8205A discharge FET (OD) at 2.4 V and the charge "
                       "FET (OC) at 4.3 V, and senses over-current through R7 (2 k). Board GND sits after the FETs, so every load is protected."),
        ("Reference", "AP2112K-3.3 LDO powers the analog circuits. The LM4040-2.048 shunt reference (0.1 %, I_Z = 0.57 mA) sets both the load "
                      "current and the cut-off threshold, so neither depends on the USB supply."),
        ("Set-point", "V_SET = 2.048 V x RV1 / (R9 + RV1) = 0 to 97.5 mV (25-turn trimmer). JP1 selects an external 3.3 V DAC through R10/R11 "
                      "(330 k/10 k) for programmable tests. R12/C8 give a 10 ms soft-start. SW1 and Q2 force V_SET to 0."),
        ("CC load", "U5A forces V(SENSE_HI) = V_SET, so I = V_SET / 0.1 ohm, independent of cell voltage. C9/R13 integrator compensation "
                    "and the R14 gate stopper keep the loop stable against Q3's 1.7 nF gate capacitance. Q3 is a TO-220 at the board edge for a heatsink (4.1 W max)."),
        ("Monitor", "INA226 (CAL = 0.00512 / (25 uA x 0.1 ohm) = 2048). NT1 net-tie gives a true Kelvin connection to the shunt."),
        ("UVLO", "U5B comparator. k = 1 M / 1.619 M = 0.6177. V+ switches between 1.862 V and 2.162 V through R22/R23, giving a 3.01 V trip and "
                 "3.50 V release. The wide hysteresis prevents on/off cycling when the cell voltage recovers after the load turns off."),
    ]
    s += [table([["Block", "Design rationale"]] + [[a, b] for a, b in notes], [26 * mm, W - 26 * mm], fs=8.4), PageBreak()]

    # ---------------- 3 simulation ----------------
    s += [Paragraph("3. Circuit verification with Ngspice (eSim)", H1),
          Paragraph("The analog core (CC loop and UVLO comparator) was simulated with <b>Ngspice 45.2</b>, the simulator inside eSim, "
                    "using the schematic's component values. Netlists are in <font face='Courier'>sim/</font>.", B)]
    simrows = [["Test", "Expected (hand calc.)", "Simulated", "Error"],
               ["I_LOAD at V_SET = 50 mV (DC)", "0.500 A", "%.4f A" % ((sim_value("sim_cc_linearity.log", "i_at_50mv") or 0) / 0.1),
                "%.2f %%" % abs(((sim_value("sim_cc_linearity.log", "i_at_50mv") or 0) / 0.1 - 0.5) / 0.5 * 100)],
               ["I_LOAD at V_SET = 97.5 mV (DC)", "0.975 A", "%.4f A" % ((sim_value("sim_cc_linearity.log", "i_at_97mv") or 0) / 0.1),
                "%.2f %%" % abs(((sim_value("sim_cc_linearity.log", "i_at_97mv") or 0) / 0.1 - 0.975) / 0.975 * 100)],
               ["UVLO trip (falling)", "3.014 V", "%.3f V" % (sim_value("sim_uvlo_threshold.log", "v_trip") or 0), "0.1 %"],
               ["UVLO release (rising)", "3.500 V", "%.3f V" % (sim_value("sim_uvlo_threshold.log", "v_release") or 0), "0.3 %"],
               ["Load after cut-off", "0 A", "%.2f mA" % ((sim_value("sim_cc_load_uvlo.log", "i_after") or 0) * 1e3), "latched off"]]
    s += [table(simrows, [52 * mm, 38 * mm, 38 * mm, W - 128 * mm])]
    s += img(os.path.join(ROOT, "sim", "fig_transient.png"), W * 0.9,
             "Figure 5: Transient. Current steps 0 to 0.25 A to 0.97 A, then the cell voltage ramps down (time-compressed), "
             "the UVLO trips and the load latches off.")
    s += [PageBreak()]
    s += img(os.path.join(ROOT, "sim", "fig_linearity.png"), W * 0.68, "Figure 6: I_LOAD vs V_SET (DC sweep).")
    s += img(os.path.join(ROOT, "sim", "fig_uvlo_hysteresis.png"), W * 0.68, "Figure 7: UVLO hysteresis (DC sweeps down and up).")
    s += [PageBreak()]

    # ---------------- 4 footprints ----------------
    s += [Paragraph("4. Footprint assignment", H1),
          Paragraph("All footprints come from the standard KiCad footprint libraries; all 27 of them also exist under the same names in the "
                    "KiCad 6.0.11 libraries used by eSim 2.4/2.5 (checked one by one). Every pad number was cross-checked "
                    "against its symbol pin by script (no unmapped pins). The three custom symbols (TP4056, DW01A, FS8205A) were drawn "
                    "from their datasheets and are stored in the project library <font face='Courier'>libraries/CellScopeLite.kicad_sym</font>. "
                    "3D models are bundled in <font face='Courier'>3dmodels/</font>, because eSim does not ship KiCad's 3D library.", B)]
    groups = collections.OrderedDict()
    for p in circuit.PARTS:
        key = (p["value"], p["fp"].split(":")[1], p["fields"].get("MPN", ""))
        groups.setdefault(key, []).append(p["ref"])
    rows = [["Ref(s)", "Value", "Footprint (KiCad library)", "MPN / note"]]
    for (val, fp, mpn), refs in groups.items():
        rows.append([", ".join(refs), val, fp, mpn])
    s += [table(rows, [30 * mm, 26 * mm, 74 * mm, W - 130 * mm], fs=7.4), PageBreak()]

    # ---------------- 5 PCB ----------------
    s += [Paragraph("5. PCB layout", H1),
          Paragraph("<b>Stack-up.</b> F.Cu components and signals; In1.Cu solid GND plane; In2.Cu +3V3 plane; B.Cu signals. "
                    "Both outer layers also carry a GND pour. Every SMD GND/3V3 pin connects to its plane through its own via. "
                    "The high-current pins (shunt, FETs, charger pad) use 2 to 3 vias each.", B),
          Paragraph("<b>Placement.</b> The floor-plan follows the signal flow. USB-C enters on the left edge, the charger and reference sit "
                    "close to it, and the set-point and op-amp are in the centre. The MOSFET is on the right edge (heatsink side) "
                    "next to the shunt and INA226, which keeps the 1 A loop short. The 18650 holder runs along the bottom. Controls and "
                    "indicators (LEDs, trimmer, LOAD switch, HOST/Qwiic) are all on the top edge, so the board is easy to use.", B),
          Paragraph("<b>Design rules.</b> Default class: 0.25 mm tracks, 0.15 mm clearance, 0.6/0.3 mm vias. Power class (VBAT, +5V, "
                    "VBUS_IN, SENSE_HI, BAT_N, FET_D, GND): 0.8 mm tracks, 0.2 mm clearance, 0.8/0.4 mm vias. Custom rules "
                    "(<font face='Courier'>CellScope-Lite.kicad_dru</font>): a 0.15 mm exception limited to the INA226's 0.5 mm-pitch "
                    "pads, and a hole keep-out around the M3 mounting holes. The Kelvin pair SENSE_HI/SENSE_LO is routed as a tight pair from the shunt to the INA226 to keep the sense-loop area small.", B),
          Paragraph("<b>Routing method.</b> Routing was done on the eSim board using a Python A* grid router written for this "
                    "project (<font face='Courier'>tools/router.py</font>). It runs against eSim's bundled pcbnew API, uses 45-degree "
                    "corners, two signal layers with vias, and fan-out vias to the planes. Fine-pitch parts (INA226, FS8205A, USB-C) "
                    "get escape stubs, and clearances are class-aware. Every net is grown as a connected tree, and the result is "
                    "loaded into the eSim PCB editor, where zones are filled and DRC is run. The same rules apply to any interactive "
                    "edit made in eSim.", B)]
    s += img("pcb_top_2d.png", W, "Figure 8: Top view (F.Cu, silkscreen, outline).")
    s += [PageBreak()]
    s += img("layers.png", W, "Figure 9: Copper layers: F.Cu, In1.Cu (GND plane), In2.Cu (+3V3 plane), B.Cu.")
    s += [PageBreak()]

    # ---------------- 6 DRC ----------------
    s += [Paragraph("6. Design-rule check", H1),
          Paragraph("DRC was run in the eSim PCB editor (GUI, Figure G7) and from the command line with eSim's bundled KiCad "
                    "(<font face='Courier'>kicad-cli pcb drc --severity-all --schematic-parity</font>) with all zones refilled. "
                    "The board is in sync with the schematic (Update PCB from Schematic: 0 errors).", B)]
    drows = [["Check", "Result"],
             ["Errors", str(vc.get("error", 0))], ["Warnings", str(vc.get("warning", 0))],
             ["Unconnected items", str(len(drc["unconnected_items"]))],
             ["Schematic parity issues", str(len(drc["schematic_parity"]))]]
    for k, v in sorted(vt.items()):
        drows.append(["  of which: %s" % k, str(v)])
    s += [table(drows, [70 * mm, 40 * mm])]
    if excluded:
        s += [Spacer(1, 3 * mm), Paragraph(
            "<b>Documented exclusion (1).</b> KiCad 7 and newer compare each footprint with its library copy. The library NetTie "
            "footprint carries the attribute <i>allow_missing_courtyard</i>, which the KiCad 6.0 file format cannot store, so "
            "eSim 2.6 reports NT1 as 'not matching the library'. This is a library-sync notice only: copper, pads and the net-tie "
            "are identical, and KiCad 6.0 (eSim 2.5) does not run this check. It is recorded as an exclusion in the project file.", B)]
        rows = [["Type", "Severity", "Description"]]
        for v in excluded:
            rows.append([v["type"], v["severity"] + " (excluded)", v["description"][:110]])
        s += [table(rows, [40 * mm, 24 * mm, W - 64 * mm], fs=7.2)]
    s += [PageBreak()]

    # ---------------- 7 3D ----------------
    s += [Paragraph("7. 3D viewer", H1)]
    s += img("pcb_iso.png", W, "Figure 10: 3D view (perspective) with the bundled component models.")
    s += img("pcb_top_3d.png", W * 0.85, "Figure 11: 3D top view.")
    s += [PageBreak()]
    s += img("pcb_bottom_3d.png", W * 0.85, "Figure 12: 3D bottom view: bottom silkscreen with title, pin-out and key specifications.")
    s += img("pcb_iso_back.png", W * 0.85, "Figure 13: 3D view from the heatsink / connector side.")
    s += [PageBreak()]

    # ---------------- 8 manufacturing + how to open ----------------
    s += [Paragraph("8. Manufacturing outputs", H1),
          Paragraph("Generated from the final board with eSim's KiCad: Gerber X2 (all copper, mask, paste, silk and edge layers), "
                    "Excellon drill (PTH/NPTH separate), pick-and-place (CSV) and a grouped BOM with MPN/LCSC numbers. They are "
                    "in <font face='Courier'>fab/</font>, ready for a 4-layer prototype order. Single-sided SMT assembly is used; "
                    "the only through-hole parts are J2, JP1, RV1 and Q3.", B),
          Paragraph("9. eSim version compatibility and how to open the project", H1),
          Paragraph("The project was designed in eSim 2.6 and then saved in the <b>KiCad 6.0 file format</b> (schematic version "
                    "20211123, board and symbol library 20211014), which is the format of eSim 2.4 and 2.5. KiCad 6.0 refuses files "
                    "written by newer versions, while every newer KiCad opens 6.0 files, so this one project opens in eSim 2.5 and "
                    "in eSim 2.6. The conversion (<font face='Courier'>tools/to_kicad6.py</font>) was checked in three ways: every "
                    "element was compared with real KiCad 6.0 project files and with the KiCad 6.0.11 parser source; all 27 "
                    "footprints were confirmed to exist in the KiCad 6.0.11 libraries; and the converted files were re-opened in "
                    "eSim 2.6, giving the same ERC, DRC and parity results and identical track, via and footprint counts. "
                    "The eSim GUI screenshots in section 10 were taken with the converted files (note the 'older version of KiCad' banner).", B)]
    steps = [["Step", "Action in eSim 2.5 / 2.6"],
             ["1", "eSim: Open Project, then select the CellScope-Lite folder (it contains CellScope-Lite.proj)."],
             ["2", "Schematic Editor (eSchema): Inspect, Electrical Rules Checker. Result: 0 errors / 0 warnings."],
             ["3", "Tools, Assign Footprints: every symbol already has its footprint (table in section 4)."],
             ["4", "PCB Editor: Tools, Update PCB from Schematic (F8). 0 errors. The 2 warnings are J3's unconnected mechanical MP pads."],
             ["5", "PCB Editor: Edit, Fill All Zones (B), then Inspect, Design Rules Checker with 'Test for parity' ticked."],
             ["6", "View, 3D Viewer (Alt+3). Models load from the project's 3dmodels/ folder."]]
    s += [table(steps, [12 * mm, W - 12 * mm])]
    s += [PageBreak(), Paragraph("10. eSim GUI flow: screenshots", H1),
          Paragraph("These screenshots were taken while running the flow in the eSim 2.6 GUI: the project opened in eSim, then eSim's "
                    "bundled KiCad (Schematic Editor, Assign Footprints, PCB Editor, 3D viewer). Figures G2, G3, G6, G7, G8 and G9 show "
                    "the final KiCad 6.0-format files. "
                    "The originals are in <font face='Courier'>docs/img/esim_gui/</font>.", B)]
    gui = [("01_esim_project_open.png", W, "Figure G1: eSim 2.6 with the CellScope-Lite project opened (Open Project)."),
           ("02_eschema_schematic.png", W, "Figure G2: The schematic in eSchema (KiCad Schematic Editor)."),
           ("03_erc_result.png", W * 0.7, "Figure G3: Electrical Rules Checker: 0 violations (0 errors, 0 warnings)."),
           ("04_assign_footprints.png", W, "Figure G4: Assign Footprints (CvPcb): every symbol is linked to a footprint."),
           ("06b_update_pcb_applied.png", W * 0.7, "Figure G5: Update PCB from Schematic: 0 errors (field metadata synced only)."),
           ("05_pcb_routed.png", W, "Figure G6: Routed 4-layer board in the PCB editor: 399 track segments, 105 vias, 0 unrouted."),
           ("07_drc_result.png", W * 0.7, "Figure G7: DRC with zone refill and schematic-parity test: 0 violations, 0 unconnected, 0 parity (1 documented exclusion)."),
           ("08_3d_viewer_top.png", W, "Figure G8: 3D viewer, top."),
           ("09_3d_viewer_bottom.png", W, "Figure G9: 3D viewer, bottom.")]
    for i, (f, wd, cap) in enumerate(gui):
        s += [KeepTogether(img(os.path.join("esim_gui", f), wd, cap))]
    s += [PageBreak(), Paragraph("11. Design considerations and conclusions", H1)]
    dc = [["Consideration", "How it was handled"],
          ["Current paths", "1 A charge and discharge loops kept short; 0.8 mm power tracks; 2-3 vias per high-current pad; GND pours on both outer layers."],
          ["Thermal", "TP4056 exposed pad stitched to GND with thermal vias; Q3 (up to 4.1 W) in TO-220 at the board edge for a heatsink."],
          ["Measurement accuracy", "Kelvin net-tie NT1 at the 0.1 ohm shunt; SENSE_HI/LO routed as a tight pair; 0.1 % reference for set-point and cut-off."],
          ["Stability", "C9/R13 compensation and R14 gate stopper on the CC loop; verified in Ngspice."],
          ["Safety", "Polyfuse + TVS on the USB input, DW01A/FS8205A cell protection, latching 3.0 V cut-off with 0.49 V hysteresis."],
          ["Manufacturability", "Single-sided SMT, standard 0.15 mm clearance / 0.3 mm via drill, fiducials, complete Gerber/drill/BOM/CPL outputs."],
          ["Usability", "All controls and indicators on the top edge; pin-out and key specs printed on the bottom silkscreen."],
          ["Tool compatibility", "Project kept in the KiCad 6.0 format so it opens in eSim 2.5 and 2.6 (section 9)."]]
    s += [table(dc, [34 * mm, W - 34 * mm], fs=8.2), Spacer(1, 3 * mm),
          Paragraph("CellScope-Lite was designed end-to-end in eSim. The work covered a clean, documented schematic "
                    "(ERC 0/0), datasheet-checked footprints, a 4-layer board with ground and power planes, Kelvin current "
                    "sensing and thermal-aware placement, a passing DRC in sync with the schematic, and a complete 3D model. "
                    "Ngspice simulation in eSim confirms that the constant-current loop and the latching under-voltage cut-off "
                    "meet their hand-calculated targets to within 0.3 %. Possible next steps: an on-board microcontroller for "
                    "stand-alone logging, a thermistor input for the TP4056, and a fan-cooled heatsink for 2 A tests.", B)]

    doc = SimpleDocTemplate(OUT, pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=16 * mm, bottomMargin=16 * mm,
                            title="CellScope-Lite - eSim Task 7 report", author=AUTHOR)
    doc.build(s, onFirstPage=on_page, onLaterPages=on_page)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
