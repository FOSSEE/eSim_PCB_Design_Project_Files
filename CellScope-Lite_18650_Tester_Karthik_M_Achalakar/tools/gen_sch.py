"""Generate CellScope-Lite.kicad_sch from design/circuit.py.

Usage: python tools/gen_sch.py <kicad_symbol_dir> <out.kicad_sch> <sch_version>
Symbols are copied verbatim from the KiCad stock libraries shipped with eSim
(and from lib/CellScopeLite.kicad_sym), so the schematic is a normal eSchema file.
"""
import os
import sys
import uuid as uuidlib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "design"))
from sexpr import Sym as S, parse, dump, find, find_all  # noqa: E402
import circuit  # noqa: E402

PROJECT = "CellScope-Lite"
NS = uuidlib.UUID("6f1c2a52-3d8e-4b0a-9a51-cellscope00"[:36].replace("cellscope00", "0c0e11500000")) \
    if False else uuidlib.UUID("6f1c2a52-3d8e-4b0a-9a51-0c0e11500000")


def U(*key):
    """Deterministic UUIDs -> regenerating keeps PCB links stable."""
    return str(uuidlib.uuid5(NS, "/".join(str(k) for k in key)))


GRID = 1.27


def snap(v):
    return round(round(v / GRID) * GRID, 4)


POWER_NETS = {"GND": "power:GND", "+5V": "power:+5V", "+3V3": "power:+3V3"}
PWR_FLAG_NETS = ["GND", "+5V", "BAT_N", "DW_VCC"]

_libcache = {}


def load_lib(symdir, lib):
    if lib not in _libcache:
        path = os.path.join(ROOT, "CellScope-Lite", "libraries", lib + ".kicad_sym") if lib == "CellScopeLite" \
            else os.path.join(symdir, lib + ".kicad_sym")
        _libcache[lib] = parse(open(path, encoding="utf-8").read())
    return _libcache[lib]


def get_symbol(symdir, lib_id):
    lib, name = lib_id.split(":")
    t = load_lib(symdir, lib)
    syms = {s[1]: s for s in find_all(t, "symbol")}
    s = syms[name]
    ext = find(s, "extends")
    if ext:  # flatten 'extends' (derived symbol) onto its parent
        parent = [x for x in syms[ext[1]]]
        parent = parse(dump(parent))
        parent[1] = name
        own_props = {p[1]: p for p in find_all(s, "property")}
        for i, x in enumerate(parent):
            if isinstance(x, list) and x and x[0] == "property" and x[1] in own_props:
                parent[i] = own_props.pop(x[1])
            if isinstance(x, list) and x and x[0] == "symbol":
                x[1] = x[1].replace(ext[1] + "_", name + "_", 1)
        for p in own_props.values():
            parent.append(p)
        s = parent
    s = parse(dump(s))
    s[1] = lib_id
    return s


def sym_pins(sdef):
    """-> {unit: [(num, name, x, y, rot, length, etype)]} ; unit 0 = common."""
    out = {}
    base = sdef[1].split(":")[1]
    for sub in find_all(sdef, "symbol"):
        nm = sub[1]
        unit = int(nm[len(base) + 1:].split("_")[0])
        for p in find_all(sub, "pin"):
            at = find(p, "at")
            ln = find(p, "length")
            num = find(p, "number")[1]
            name = find(p, "name")[1]
            out.setdefault(unit, []).append((num, name, float(at[1]), float(at[2]), int(float(at[3]) if len(at) > 3 else 0),
                                             float(ln[1]), str(p[1])))
    return out


def sym_bbox(sdef, unit):
    xs, ys = [], []
    for u, pins in sym_pins(sdef).items():
        if u in (0, unit):
            for (_, _, x, y, *_r) in pins:
                xs.append(x)
                ys.append(y)
    base = sdef[1].split(":")[1]
    for sub in find_all(sdef, "symbol"):
        nm = sub[1]
        u = int(nm[len(base) + 1:].split("_")[0])
        if u not in (0, unit):
            continue
        for g in sub:
            if isinstance(g, list) and g and g[0] in ("rectangle",):
                for k in ("start", "end"):
                    v = find(g, k)
                    xs.append(float(v[1]))
                    ys.append(float(v[2]))
            if isinstance(g, list) and g and g[0] == "polyline":
                for pt in find_all(find(g, "pts"), "xy"):
                    xs.append(float(pt[1]))
                    ys.append(float(pt[2]))
    if not xs:
        return (-2.54, -2.54, 2.54, 2.54)
    return (min(xs), min(ys), max(xs), max(ys))


OUTWARD = {0: (-1, 0), 180: (1, 0), 90: (0, 1), 270: (0, -1)}  # schematic coords (y down)


def effects(size=1.27, hide=False, justify=None):
    e = [S("effects"), [S("font"), [S("size"), size, size]]]
    if justify:
        e.append([S("justify")] + [S(j) for j in justify])
    if hide:
        e.append([S("hide"), S("yes")])
    return e


class Sheet:
    def __init__(self, symdir, version):
        self.symdir = symdir
        self.version = version
        self.lib_symbols = {}
        self.items = []
        self.root = U("root")
        self.pwr_n = 0

    def libsym(self, lib_id):
        if lib_id not in self.lib_symbols:
            self.lib_symbols[lib_id] = get_symbol(self.symdir, lib_id)
        return self.lib_symbols[lib_id]

    def place(self, lib_id, ref, value, x, y, unit=1, fp="", fields=None, rot=0, power=False, key=None):
        sdef = self.libsym(lib_id)
        uid = U("sym", key or ref, unit)
        props = {p[1]: p for p in find_all(sdef, "property")}
        node = [S("symbol"), [S("lib_id"), lib_id], [S("at"), x, y, rot], [S("unit"), unit],
                [S("exclude_from_sim"), S("no")],
                [S("in_bom"), S("no") if power or ref.rstrip("0123456789") in ("H", "FID", "TP", "NT") else S("yes")],
                [S("on_board"), S("no") if power else S("yes")], [S("dnp"), S("no")],
                [S("uuid"), uid]]
        bb = sym_bbox(sdef, unit)
        vals = {"Reference": ref, "Value": value, "Footprint": fp,
                "Datasheet": find(props["Datasheet"], "at") and props["Datasheet"][2] if "Datasheet" in props else "~"}
        if "Description" in props:
            vals["Description"] = props["Description"][2]
        top = y - bb[3] - 1.6
        bot = y - bb[1] + 1.6
        right = x + bb[2] + 1.0
        place_side = (bb[2] - bb[0]) < 6  # narrow (passives): text to the right
        upins = [p for uu, pl in sym_pins(sdef).items() if uu in (0, unit) for p in pl]
        horiz_only = upins and all(OUTWARD[p[4]][1] == 0 for p in upins) and len(upins) <= 2
        right_pin = any(OUTWARD[p[4]] == (1, 0) for p in upins)
        has_bottom_pin = any(OUTWARD[p[4]] == (0, 1) for uu, pl in sym_pins(sdef).items() if uu in (0, unit) for p in pl)
        for name, val in vals.items():
            hide = name not in ("Reference", "Value") or power and name == "Reference"                 or (name == "Value" and lib_id in ("Connector:TestPoint", "Mechanical:Fiducial"))
            if horiz_only and not power:
                py = {"Reference": y - 3.2, "Value": y + 3.4}.get(name, y)
                at, just = [S("at"), x - 1.5 if name == "Value" else x, py, 0], (["left"] if name == "Value" else None)
            elif place_side and right_pin and not power:
                py = {"Reference": y - 1.27, "Value": y + 1.27}.get(name, y)
                at, just = [S("at"), x + bb[0] - 1.0, py, 0], ["right"]
            elif place_side:
                py = {"Reference": y - 1.27, "Value": y + 1.27}.get(name, y)
                at, just = [S("at"), right + 0.5, py, 0], ["left"]
            else:
                py = {"Reference": top, "Value": bot}.get(name, y)
                at, just = [S("at"), x, py, 0], None
                if name == "Value" and lib_id == "Switch:SW_SPDT":
                    at, just = [S("at"), x + bb[0] - 9.0, bot - 1.5, 0], ["left"]
                elif name == "Value" and has_bottom_pin:
                    at, just = [S("at"), x + bb[2] + 1.0, y - bb[1] - 1.0, 0], ["left"]
            if power and name == "Value":
                body = {0: (0, -1), 90: (-1, 0), 180: (0, 1), 270: (1, 0)}[rot]
                if lib_id == "power:GND":
                    body = (-body[0], -body[1])
                if lib_id == "power:PWR_FLAG":
                    body = (0, -1)
                at = [S("at"), x + body[0] * 4.5, y + body[1] * 4.2, 0]
                just = None
            node.append([S("property"), name, val, at, effects(hide=hide, justify=just)])
        for k, v in (fields or {}).items():
            node.append([S("property"), k, v, [S("at"), x, y, 0], effects(hide=True)])
        for u, pins in sym_pins(sdef).items():
            if u in (0, unit):
                for p in pins:
                    node.append([S("pin"), p[0], [S("uuid"), U("pin", key or ref, unit, p[0])]])
        node.append([S("instances"), [S("project"), PROJECT,
                                      [S("path"), "/" + self.root, [S("reference"), ref], [S("unit"), unit]]]])
        self.items.append(node)
        return sdef

    def wire(self, x1, y1, x2, y2):
        self.items.append([S("wire"), [S("pts"), [S("xy"), x1, y1], [S("xy"), x2, y2]],
                           [S("stroke"), [S("width"), 0], [S("type"), S("default")]], [S("uuid"), U("w", x1, y1, x2, y2)]])

    def label(self, net, x, y, ang):
        just = {0: ["left", "bottom"], 180: ["right", "bottom"], 90: ["left", "bottom"], 270: ["right", "bottom"]}[ang]
        self.items.append([S("label"), net, [S("at"), x, y, ang],
                           [S("fields_autoplaced"), S("yes")], effects(justify=just),
                           [S("uuid"), U("lbl", net, x, y)]])

    def junction(self, x, y):
        self.items.append([S("junction"), [S("at"), x, y], [S("diameter"), 0], [S("color"), 0, 0, 0, 0],
                           [S("uuid"), U("j", x, y)]])

    def noconnect(self, x, y):
        self.items.append([S("no_connect"), [S("at"), x, y], [S("uuid"), U("nc", x, y)]])

    def power(self, net, x, y, outward):
        lib_id = POWER_NETS[net]
        if net == "GND":
            rot = {(0, 1): 0, (1, 0): 90, (0, -1): 180, (-1, 0): 270}[outward]
        else:
            rot = {(0, -1): 0, (-1, 0): 90, (0, 1): 180, (1, 0): 270}[outward]
        self.pwr_n += 1
        ref = "#PWR%03d" % self.pwr_n
        self.place(lib_id, ref, net, x, y, rot=rot, power=True, key=ref)

    def pwr_flag(self, net, x, y):
        self.pwr_n += 1
        ref = "#FLG%03d" % self.pwr_n
        self.place("power:PWR_FLAG", ref, "PWR_FLAG", x, y, power=True, key=ref)
        if net in POWER_NETS:
            self.power(net, x, y + 2.54, (0, 1))
            self.wire(x, y, x, y + 2.54)
        else:
            self.wire(x, y, x, y + 2.54)
            self.label(net, x, y + 2.54, 0)

    def text(self, s, x, y, size=2.0, bold=False):
        e = [S("effects"), [S("font"), [S("size"), size, size]] + ([[S("bold"), S("yes")]] if bold else []),
             [S("justify"), S("left"), S("bottom")]]
        self.items.append([S("text"), s, [S("exclude_from_sim"), S("no")], [S("at"), x, y, 0], e,
                           [S("uuid"), U("txt", s, x, y)]])

    def rect(self, x1, y1, x2, y2):
        self.items.append([S("rectangle"), [S("start"), x1, y1], [S("end"), x2, y2],
                           [S("stroke"), [S("width"), 0.3], [S("type"), S("dash")]],
                           [S("fill"), [S("type"), S("none")]], [S("uuid"), U("rect", x1, y1)]])

    def connect_pins(self, sdef, x, y, unit, pinmap, rot=0):
        assert rot == 0
        allpins = []
        for u, pins in sym_pins(sdef).items():
            if u in (0, unit):
                allpins += [p for p in pins if p[0] in pinmap]
        # horizontal power pins: group per (side, net) -> one upright power symbol
        groups = {}
        for (num, name, px, py, prot, ln, et) in allpins:
            net = pinmap[num]
            ox, oy = OUTWARD[prot]
            if net in POWER_NETS and ox != 0:
                groups.setdefault((ox, net), []).append((snap(x + px), snap(y - py)))
        grouped = set()
        for (ox, net), pts in groups.items():
            ex = snap(pts[0][0] + ox * 2.54)
            ys = sorted(p[1] for p in pts)
            side_ys = [snap(y - p[3]) for p in allpins if OUTWARD[p[4]][0] == ox and pinmap[p[0]] is not None]
            below = any(v > ys[-1] for v in side_ys)
            above = any(v < ys[0] for v in side_ys)
            if net == "GND":
                d = 1 if not below else (-1 if not above else 0)
            else:
                d = -1 if not above else (1 if not below else 0)
            if d == 0:
                d = 1 if net == "GND" else -1
                ex = snap(pts[0][0] + ox * 7.62)
                ys = sorted(set(side_ys + ys))
            for (cx, cy) in pts:
                self.wire(cx, cy, ex, cy)
                grouped.add((cx, cy))
            end = snap((ys[-1] if d > 0 else ys[0]) + d * 2.54)
            own = sorted(p[1] for p in pts)
            start = own[0] if d > 0 else own[-1]
            stops = sorted(set(own + [end]), reverse=(d < 0))
            stops = [v for v in stops if (v >= start if d > 0 else v <= start)]
            for a, b in zip(stops, stops[1:]):
                self.wire(ex, a, ex, b)
            for mid in stops[1:-1]:
                self.junction(ex, mid)
            self.power(net, ex, end, (0, d))
        for (num, name, px, py, prot, ln, et) in allpins:
            net = pinmap[num]
            cx, cy = snap(x + px), snap(y - py)
            ox, oy = OUTWARD[prot]
            if net is None:
                self.noconnect(cx, cy)
                continue
            if (cx, cy) in grouped:
                continue
            ex, ey = snap(cx + ox * 2.54), snap(cy + oy * 2.54)
            self.wire(cx, cy, ex, ey)
            if net in POWER_NETS:
                self.power(net, ex, ey, (ox, oy))
            else:
                ang = {(-1, 0): 180, (1, 0): 0, (0, 1): 0, (0, -1): 0}[(ox, oy)]
                self.label(net, ex, ey, ang)

    def write(self, path, title_block):
        libs = [S("lib_symbols")] + [self.lib_symbols[k] for k in sorted(self.lib_symbols)]
        doc = [S("kicad_sch"), [S("version"), int(self.version)], [S("generator"), "eeschema"],
               [S("generator_version"), self.gen_ver], [S("uuid"), self.root], [S("paper"), "A2"],
               title_block, libs] + self.items + [
            [S("sheet_instances"), [S("path"), "/", [S("page"), "1"]]]]
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(dump(doc) + "\n")


# --------------- layout -----------------
CHW = 1.05  # approx width of one 1.27 mm stroke-font character


def tlen(t):
    return len(t) * CHW + 1.0


def part_extent(sdef, unit, pinmap, ref, value):
    """Bounding box (schematic coords, symbol at 0,0) incl. stubs, labels, power symbols, ref/value."""
    bb = sym_bbox(sdef, unit)
    xs = [bb[0], bb[2]]
    ys = [-bb[3], -bb[1]]
    for u, pins in sym_pins(sdef).items():
        if u not in (0, unit):
            continue
        for (num, name, px, py, prot, ln, et) in pins:
            if num not in pinmap:
                continue
            net = pinmap[num]
            cx, cy = px, -py
            ox, oy = OUTWARD[prot]
            ex, ey = cx + ox * 2.54, cy + oy * 2.54
            if net is None:
                xs += [cx - 1, cx + 1]; ys += [cy - 1, cy + 1]
            elif net in POWER_NETS:
                xs += [ex + ox * 4.5 - 2, ex + ox * 4.5 + 2]; ys += [ey + oy * 4.5 - 2, ey + oy * 4.5 + 2]
                if ox == 0:
                    xs += [ex + 2.5]
            elif ox != 0:
                L = tlen(net)
                xs += [ex, ex + ox * L]; ys += [ey - 1.6, ey + 0.4]
            else:
                L = tlen(net)
                xs += [ex, ex + L]; ys += [ey - 1.6, ey + 0.4]
    narrow = (bb[2] - bb[0]) < 6
    if narrow:
        xs.append(bb[2] + 1.5 + max(tlen(ref), tlen(value)))
    else:
        ys += [-bb[3] - 3.2, -bb[1] + 3.2]
        xs += [-max(tlen(ref), tlen(value)) / 2, max(tlen(ref), tlen(value)) / 2]
    return min(xs), min(ys), max(xs), max(ys)


COLS = [(12, 186), (204, 186), (396, 186)]
ROWS = [["USB", "CHG", "BMS"], ["PWR", "SET", "CCL"], ["MON", "UVL", "IO"]]


def flow(sh, parts, bw, dry, ox=0, oy=0):
    """Flow-layout parts inside a block. Returns used height."""
    gap_x, gap_y = 3.81, 3.81
    cx, cy, row_h = 0.0, 0.0, 0.0
    items = []
    big = [p for p in parts if len(p["pins"]) > 3 or p["lib"].startswith("Amplifier")]
    small = [p for p in parts if p not in big]
    for group in (big, small):
        for p in group:
            units = [1, 2, 3] if p["lib"].startswith("Amplifier") else [1]
            for un in units:
                sdef = sh.libsym(p["lib"])
                e = part_extent(sdef, un, p["pins"], p["ref"], p["value"])
                w, h = e[2] - e[0], e[3] - e[1]
                if cx > 0 and cx + w > bw:
                    cx, cy, row_h = 0.0, cy + row_h + gap_y, 0.0
                items.append((p, un, sdef, snap(ox + cx - e[0]), snap(oy + cy - e[1])))
                cx += w + gap_x
                row_h = max(row_h, h)
        if group is big and big and small:
            cx, cy, row_h = 0.0, cy + row_h + gap_y + 2, 0.0
    if not dry:
        for p, un, sdef, x, y in items:
            sh.place(p["lib"], p["ref"], p["value"], x, y, unit=un, fp=p["fp"], fields=p["fields"])
            sh.connect_pins(sdef, x, y, un, p["pins"])
    return cy + row_h


def build(symdir, out, version, gen_ver):
    sh = Sheet(symdir, version)
    sh.gen_ver = gen_ver
    titles = dict(circuit.BLOCKS)
    by_block = {}
    for p in circuit.PARTS:
        by_block.setdefault(p["block"], []).append(p)
    # IO block: mechanical parts are shown, PWR_FLAGs added separately
    y = 16.0
    for row in ROWS:
        hs = [flow(sh, by_block[b], COLS[i][1] - 10, True) for i, b in enumerate(row)]
        rh = max(hs) + 16 + (14 if "IO" in row else 0)
        for i, b in enumerate(row):
            bx, bw = COLS[i]
            sh.rect(bx, y, bx + bw, y + rh)
            sh.text(titles[b], bx + 2, y + 5, size=2.2, bold=True)
            flow(sh, by_block[b], bw - 10, False, bx + 5, y + 10)
            if b == "IO":
                fy = y + rh - 12
                for k, net in enumerate(PWR_FLAG_NETS):
                    sh.pwr_flag(net, snap(bx + 8 + k * 16), snap(fy))
        y += rh + 4
    sh.layout_bottom = y
    notes = [
        "DESIGN EQUATIONS & KEY NUMBERS",
        "Charge current (TP4056):  I_CHG = 1200 V / R3 = 1200 / 1.2k = 1.00 A  (CC/CV, 4.20 V +/-1 %)",
        "Cell protection (DW01A + FS8205A):  over-charge 4.30 V, over-discharge 2.40 V, over-current via R7 sensing V_DS of FS8205A",
        "Set-point:  V_SET = 2.048 V x RV1 / (R9 + RV1) = 0 ... 97.5 mV   |  external DAC: V_SET = V_DAC x R11 / (R10 + R11) = 0 ... 97 mV",
        "CC load:  I_LOAD = V_SET / R16 = V_SET / 0.1 ohm = 0 ... 0.975 A   (loop: U5A + Q3, C9/R13 compensation, R14 gate stopper)",
        "Thermal:  P_Q3 = (V_BAT - I x R16) x I = 4.1 W max at 4.2 V / 1 A  -> TO-220 on heatsink;  P_R16 = I^2 x R = 0.1 W (2512, 2 W rated)",
        "UVLO:  V_trip = V+ / k = 1.862 V / 0.6177 = 3.01 V (falling);  V_release = 2.162 V / 0.6177 = 3.50 V  (k = R21 / (R20 + R21))",
        "INA226 (addr 0x40):  shunt LSB 2.5 uV -> 25 uA;  bus LSB 1.25 mV;  CAL = 0.00512 / (I_LSB x R_SHUNT) = 2048 for I_LSB = 25 uA",
        "Kelvin sensing: NT1 ties SENSE_LO to GND only at R16 pad, so INA226 Vin-/Vin+ read the shunt without ground-plane IR drop",
    ]
    nx, ny = 12, snap(y + 4)
    sh.rect(nx, ny, nx + 378, ny + 8 + 4.6 * len(notes))
    for i, line in enumerate(notes):
        sh.text(line, nx + 3, ny + 7 + 4.6 * i, size=2.2 if i == 0 else 1.8, bold=(i == 0))
    print("layout bottom y = %.1f mm (A3 usable ~ 255 for right column above title block)" % y)
    tb = [S("title_block"), [S("title"), "CellScope-Lite: 18650 Li-ion Charger & Capacity Tester"],
          [S("date"), "2026-11-21"], [S("rev"), "1.0"], [S("company"), "FOSSEE eSim Semester Long Internship - Autumn 2026 - Task 7"],
          [S("comment"), 1, "4-layer PCB, eSim project in KiCad 6.0 format (opens in eSim 2.4 / 2.5 / 2.6)"],
          [S("comment"), 2, "Charge 1 A (TP4056) | Protect (DW01A+FS8205A) | CC discharge 0-1 A | INA226 I2C monitor"]]
    sh.write(out, tb)
    print("wrote", out, "symbols:", len(sh.lib_symbols))


if __name__ == "__main__":
    build(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4] if len(sys.argv) > 4 else "8.0")
