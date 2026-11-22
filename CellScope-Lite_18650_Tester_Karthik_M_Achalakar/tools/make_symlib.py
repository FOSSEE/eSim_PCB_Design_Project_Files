"""Generate the project symbol library CellScopeLite.kicad_sym (TP4056, DW01A, FS8205A).

Pin numbers/names follow the manufacturer datasheets:
  TP4056 (NanJing Top Power, ESOP-8): 1 TEMP 2 PROG 3 GND 4 VCC 5 BAT 6 STDBY 7 CHRG 8 CE, EP = GND
  DW01A (Fortune Semi, SOT-23-6):      1 OD 2 CS 3 OC 4 TD 5 VCC 6 GND
  FS8205A (Fortune Semi, TSSOP-8):     1 D12 2 S1 3 S1 4 G1 5 G2 6 S2 7 S2 8 D12
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from sexpr import Sym as S, dump  # noqa: E402


def prop(name, val, x, y, hide=False):
    eff = [S("effects"), [S("font"), [S("size"), 1.27, 1.27]]]
    if hide:
        eff.append([S("hide"), S("yes")])
    return [S("property"), name, val, [S("at"), x, y, 0], eff]


def pin(num, name, etype, x, y, rot, length=2.54, hidden=False):
    p = [S("pin"), S(etype), S("line"), [S("at"), x, y, rot], [S("length"), length]]
    if hidden:
        p.append([S("hide"), S("yes")])
    p += [[S("name"), name, [S("effects"), [S("font"), [S("size"), 1.27, 1.27]]]],
          [S("number"), str(num), [S("effects"), [S("font"), [S("size"), 1.27, 1.27]]]]]
    return p


def box_symbol(name, ref, fp, desc, ds, left, right, w=15.24, extra_graphics=None):
    """left/right: list of (num, name, type) top->bottom; pins on 2.54 grid."""
    rows = max(len(left), len(right))
    h = (rows + 1) * 2.54
    top = h / 2
    top = round(top / 1.27) * 1.27
    x0 = -w / 2
    g = [S("rectangle"), [S("start"), x0, top], [S("end"), -x0, -top],
         [S("stroke"), [S("width"), 0.254], [S("type"), S("default")]], [S("fill"), [S("type"), S("background")]]]
    pins = []
    y = top - 2.54
    for item in left:
        if item:
            pins.append(pin(item[0], item[1], item[2], x0 - 2.54, y, 0, hidden=(len(item) > 3)))
        y -= 2.54
    y = top - 2.54
    for item in right:
        if item:
            pins.append(pin(item[0], item[1], item[2], -x0 + 2.54, y, 180, hidden=(len(item) > 3)))
        y -= 2.54
    body = [S("symbol"), name + "_0_1", g] + (extra_graphics or [])
    pinsu = [S("symbol"), name + "_1_1"] + pins
    return [S("symbol"), name,
            [S("pin_names"), [S("offset"), 1.016]],
            [S("exclude_from_sim"), S("no")], [S("in_bom"), S("yes")], [S("on_board"), S("yes")],
            prop("Reference", ref, 0, top + 1.905),
            prop("Value", name, 0, -top - 1.905),
            prop("Footprint", fp, 0, -top - 4.445, True),
            prop("Datasheet", ds, 0, -top - 6.985, True),
            prop("Description", desc, 0, 0, True),
            body, pinsu]


def main(out):
    syms = []
    syms.append(box_symbol(
        "TP4056", "U", "Package_SO:SOIC-8-1EP_3.9x4.9mm_P1.27mm_EP2.29x3mm",
        "1 A standalone linear Li-ion charger, CC/CV 4.2 V, ESOP-8",
        "https://dlnmh9ip6v2uc.cloudfront.net/datasheets/Prototyping/TP4056.pdf",
        left=[("4", "VCC", "power_in"), ("8", "CE", "input"), ("2", "PROG", "passive"), ("1", "TEMP", "input")],
        right=[("5", "BAT", "power_out"), ("7", "~{CHRG}", "open_collector"), ("6", "~{STDBY}", "open_collector"),
               ("3", "GND", "power_in"), ("9", "EP", "passive")],
        w=12.7))
    syms.append(box_symbol(
        "DW01A", "U", "Package_TO_SOT_SMD:SOT-23-6",
        "One-cell Li-ion protection IC (OV 4.3 V / UV 2.4 V / OC / short), SOT-23-6",
        "https://www.lcsc.com/datasheet/lcsc_datasheet_1810101713_Fortune-Semicon-DW01A_C351410.pdf",
        left=[("5", "VCC", "power_in"), ("2", "CS", "input"), ("4", "TD", "input")],
        right=[("1", "OD", "output"), ("3", "OC", "output"), ("6", "GND", "power_in")],
        w=10.16))
    syms.append(box_symbol(
        "FS8205A", "Q", "Package_SO:TSSOP-8_4.4x3mm_P0.65mm",
        "Dual N-channel 20 V 6 A MOSFET, common drain, for 1-cell protection, TSSOP-8",
        "https://www.lcsc.com/datasheet/lcsc_datasheet_1811101213_Fortune-Semicon-FS8205A_C32254.pdf",
        left=[("4", "G1", "input"), ("1", "D12", "passive"), ("2", "S1", "passive"), ("3", "S1", "passive")],
        right=[("5", "G2", "input"), ("8", "D12", "passive"), ("6", "S2", "passive"), ("7", "S2", "passive")],
        w=10.16))
    lib = [S("kicad_symbol_lib"), [S("version"), 20231120], [S("generator"), "cellscope_lite_gen"],
           [S("generator_version"), "1.0"]] + syms
    with open(out, "w", newline="\n") as f:
        f.write(dump(lib) + "\n")
    print("wrote", out)


if __name__ == "__main__":
    main(sys.argv[1])
