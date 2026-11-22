"""Down-convert the CellScope-Lite KiCad 9 files to the KiCad 6.0 file format.

eSim 2.4 / 2.5 ship KiCad 6.0, which refuses files written by newer KiCad
versions.  KiCad 6.0 files open unchanged in KiCad 7/8/9/10 (eSim 2.6), so the
submitted project is kept in the 6.0 format.

Usage: python tools/to_kicad6.py <project_dir>
Converts in place:  <name>.kicad_sch, <name>.kicad_pcb, libraries/*.kicad_sym,
<name>.kicad_pro, <name>.kicad_prl
"""
import glob
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sexpr import Sym, parse  # noqa: E402

PCB_VERSION = 20211014      # KiCad 6.0 SEXPR_BOARD_FILE_VERSION
SCH_VERSION = 20211123      # KiCad 6.0 SEXPR_SCHEMATIC_FILE_VERSION
SYM_VERSION = 20211014      # KiCad 6.0 SEXPR_SYMBOL_LIB_FILE_VERSION

LAYER_ID6 = {"F.Cu": 0, "B.Cu": 31, "B.Adhes": 32, "F.Adhes": 33, "B.Paste": 34, "F.Paste": 35,
             "B.SilkS": 36, "F.SilkS": 37, "B.Mask": 38, "F.Mask": 39, "Dwgs.User": 40, "Cmts.User": 41,
             "Eco1.User": 42, "Eco2.User": 43, "Edge.Cuts": 44, "Margin": 45, "B.CrtYd": 46, "F.CrtYd": 47,
             "B.Fab": 48, "F.Fab": 49}
LAYER_ID6.update({"In%d.Cu" % i: i for i in range(1, 31)})
LAYER_ID6.update({"User.%d" % i: 49 + i for i in range(1, 10)})


# --------------------------------------------------------------------------- helpers
def head(n):
    return n[0] if isinstance(n, list) and n else None


def kids(n, key):
    return [x for x in n if isinstance(x, list) and x and x[0] == key]


def kid(n, key):
    k = kids(n, key)
    return k[0] if k else None


def drop(n, *keys):
    n[:] = [x for x in n if not (isinstance(x, list) and x and x[0] in keys)]


def yesno(n, key):
    """Return True/False/None for a (key yes|no) child, and remove it."""
    k = kid(n, key)
    if k is None:
        return None
    drop(n, key)
    return len(k) > 1 and k[1] == "yes"


def rename_uuid(n):
    """(uuid x) -> (tstamp x), recursively (board files only)."""
    if isinstance(n, list):
        if n and n[0] == "uuid":
            n[0] = Sym("tstamp")
        for x in n:
            rename_uuid(x)


def write6(path, tree):
    """KiCad-6 style writer: short leaf lists stay on one line."""
    def q(s):
        return '"%s"' % str(s).replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")

    def atom(x):
        if isinstance(x, Sym):
            return str(x)
        if isinstance(x, bool):
            return "yes" if x else "no"
        if isinstance(x, (int, float)):
            s = repr(x) if isinstance(x, int) else ("%.6f" % x).rstrip("0").rstrip(".")
            return s
        return q(x)

    def simple(n):
        return all(not isinstance(x, list) for x in n)

    def flat(n):
        return "(" + " ".join(flat(x) if isinstance(x, list) else atom(x) for x in n) + ")"

    def emit(n, ind):
        if not isinstance(n, list):
            return atom(n)
        if simple(n) or (len(flat(n)) < 110 and n[0] not in ("footprint", "symbol", "zone", "kicad_pcb", "kicad_sch",
                                                                 "lib_symbols", "kicad_symbol_lib", "setup", "layers",
                                                                 "net", "filled_polygon", "polygon")):
            return flat(n)
        pad = "  " * (ind + 1)
        hd = []
        for x in n:
            if isinstance(x, list):
                break
            hd.append(atom(x))
        out = "(" + " ".join(hd)
        for x in n[len(hd):]:
            out += "\n" + pad + emit(x, ind + 1)
        return out + "\n" + "  " * ind + ")"

    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(emit(tree, 0) + "\n")


# --------------------------------------------------------------------------- text effects
def fix_effects(eff, hide=False):
    """KiCad 9 effects -> KiCad 6 effects.  'hide' becomes a bare atom."""
    if eff is None:
        return
    h = yesno(eff, "hide")
    font = kid(eff, "font")
    if font is not None:
        for b in ("bold", "italic"):
            v = yesno(font, b)
            if v:
                font.append(Sym(b))
        drop(font, "face", "color", "line_spacing")
    j = kid(eff, "justify")
    if (hide or h) and Sym("hide") not in eff:
        eff.append(Sym("hide"))
    drop(eff, "href")
    return j


# --------------------------------------------------------------------------- PCB
PLOTPARAMS6 = parse("""(pcbplotparams
      (layerselection 0x00010fc_ffffffff)
      (disableapertmacros false) (usegerberextensions false) (usegerberattributes true)
      (usegerberadvancedattributes true) (creategerberjobfile true) (svguseinch false) (svgprecision 6)
      (excludeedgelayer true) (plotframeref false) (viasonmask false) (mode 1) (useauxorigin false)
      (hpglpennumber 1) (hpglpenspeed 20) (hpglpendiameter 15.000000) (dxfpolygonmode true)
      (dxfimperialunits true) (dxfusepcbnewfont true) (psnegative false) (psa4output false)
      (plotreference true) (plotvalue true) (plotinvisibletext false) (sketchpadsonfab false)
      (subtractmaskfromsilk false) (outputformat 1) (mirror false) (drillshape 1) (scaleselection 1)
      (outputdirectory ""))""")

LOST_ATTR = []   # footprints whose KiCad 9 'allow_missing_courtyard' flag has no KiCad 6 equivalent

GRAPHIC = ("gr_line", "gr_arc", "gr_circle", "gr_rect", "gr_poly", "gr_curve",
           "fp_line", "fp_arc", "fp_circle", "fp_rect", "fp_poly", "fp_curve")


def stroke_to_width(n):
    st = kid(n, "stroke")
    if st is not None:
        w = kid(st, "width")
        drop(n, "stroke")
        lay = [i for i, x in enumerate(n) if head(x) == "layer"]
        pos = lay[0] + 1 if lay else len(n)
        n.insert(pos, [Sym("width"), w[1] if w else 0.1])
    f = kid(n, "fill")
    if f is not None and len(f) > 1 and f[1] in ("yes", "no"):
        f[1] = Sym("solid" if f[1] == "yes" else "none")


def conv_pcb_text(n, kind=None):
    """gr_text / fp_text: hide -> bare atom after layer, drop unlocked/knockout bits."""
    hide = yesno(n, "hide")
    yesno(n, "unlocked")
    lay = kid(n, "layer")
    if lay is not None and len(lay) > 2:      # (layer "F.SilkS" knockout)
        del lay[2:]
    if hide:
        i = n.index(lay) + 1 if lay is not None else len(n)
        n.insert(i, Sym("hide"))
    fix_effects(kid(n, "effects"))
    drop(n, "render_cache")


def conv_footprint(fp):
    drop(fp, "embedded_fonts", "embedded_files", "net_tie_pad_groups", "component_classes", "duplicate_pad_numbers_are_jumpers")
    yesno(fp, "locked")
    out = []
    for x in fp:
        h = head(x)
        if h == "property":
            name, val = x[1], x[2]
            if name in ("Reference", "Value"):
                t = [Sym("fp_text"), Sym("reference" if name == "Reference" else "value"), val]
                t += [y for y in x[3:]]
                conv_pcb_text(t)
                out.append(t)
            elif name in ("Datasheet", "Description", "Footprint", "ki_fp_filters"):
                continue        # KiCad 6 footprints keep only user properties
            else:
                out.append([Sym("property"), name, val])
        elif h == "sheetname":
            out.append([Sym("property"), "Sheetname", "" if x[1] == "/" else x[1]])
        elif h == "sheetfile":
            out.append([Sym("property"), "Sheetfile", x[1]])
        elif h == "attr":
            keep = [a for a in x[1:] if a in ("smd", "through_hole", "board_only", "exclude_from_pos_files",
                                               "exclude_from_bom")]
            if "allow_missing_courtyard" in x[1:]:
                at = kid(fp, "at")
                LOST_ATTR.append((kid(fp, "tstamp")[1], at[1], at[2]))
            out.append([Sym("attr")] + keep)
        elif h == "fp_text":
            conv_pcb_text(x)
            out.append(x)
        elif h in GRAPHIC:
            stroke_to_width(x)
            drop(x, "locked")
            out.append(x)
        elif h == "pad":
            conv_pad(x)
            out.append(x)
        elif h == "model":
            drop(x, "hide", "opacity")
            out.append(x)
        elif h == "zone":
            conv_zone(x)
            out.append(x)
        else:
            out.append(x)
    fp[:] = out


def conv_pad(p):
    for k in ("remove_unused_layers", "keep_end_layers"):
        v = yesno(p, k)
        if v:
            p.append([Sym(k)])
    drop(p, "teardrops", "zone_layer_connections", "tenting", "padstack", "thermal_bridge_angle_",
         "clearance_override", "backdrill")
    prim = kid(p, "primitives")
    if prim is not None:
        for g in prim[1:]:
            if isinstance(g, list):
                st = kid(g, "stroke")
                if st is not None:
                    w = kid(st, "width")
                    drop(g, "stroke")
                    g.append([Sym("width"), w[1] if w else 0])


def conv_zone(z):
    drop(z, "placement", "attr")
    f = kid(z, "fill")
    if f is not None:
        drop(f, "island_removal_mode_")
    for poly in kids(z, "filled_polygon"):
        drop(poly, "island")


def convert_pcb(path):
    t = parse(open(path, encoding="utf-8").read())
    assert t[0] == "kicad_pcb"
    rename_uuid(t)
    out = []
    for x in t:
        h = head(x)
        if h == "version":
            x[1] = PCB_VERSION
        elif h == "generator":
            x[1] = Sym("pcbnew")
        elif h in ("generator_version", "embedded_fonts", "embedded_files"):
            continue
        elif h == "general":
            x[:] = [Sym("general")] + kids(x, "thickness")
        elif h == "layers":
            rows = []
            for L in x[1:]:
                name = L[1]
                typ = L[2]
                if name.startswith("In") and name.endswith(".Cu") or name in ("F.Cu", "B.Cu"):
                    typ = Sym("signal") if typ not in ("signal", "power", "mixed", "jumper") else typ
                row = [LAYER_ID6[name], name, typ] + list(L[3:])
                rows.append(row)
            rows.sort(key=lambda r: r[0])
            x[:] = [Sym("layers")] + rows
        elif h == "setup":
            drop(x, "allow_soldermask_bridges_in_footprints", "tenting", "covering", "plugging", "capping",
                 "filling", "zone_defaults", "pcbplotparams")
            x.append(PLOTPARAMS6)
        elif h == "footprint":
            conv_footprint(x)
        elif h in GRAPHIC:
            stroke_to_width(x)
            drop(x, "locked")
        elif h in ("gr_text",):
            conv_pcb_text(x)
        elif h == "zone":
            conv_zone(x)
        elif h in ("segment", "arc", "via"):
            drop(x, "teardrops", "tenting", "capping", "covering", "plugging", "filling", "padstack")
            for k in ("free", "remove_unused_layers", "keep_end_layers"):
                v = yesno(x, k)
                if v:
                    x.append([Sym(k)])
            yesno(x, "locked")
        elif h in ("property", "generated", "group"):
            continue
        out.append(x)
    write6(path, out)


# --------------------------------------------------------------------------- symbols (lib + schematic lib_symbols)
FIELD_ID = {"Reference": 0, "Value": 1, "Footprint": 2, "Datasheet": 3}


def conv_property(p, next_id):
    """KiCad 9 sch property -> KiCad 6: add (id n), hide into effects, drop newer flags."""
    name = p[1]
    hide = yesno(p, "hide")
    drop(p, "uuid", "show_name", "do_not_autoplace", "private")
    if name in FIELD_ID:
        pid = FIELD_ID[name]
    else:
        pid = next_id[0]
        next_id[0] += 1
    i = 3 if len(p) > 3 and not isinstance(p[2], list) else 2
    p.insert(3, [Sym("id"), pid])
    eff = kid(p, "effects")
    if eff is None and hide:
        eff = [Sym("effects"), [Sym("font"), [Sym("size"), 1.27, 1.27]]]
        p.append(eff)
    fix_effects(eff, hide=bool(hide))


def conv_lib_symbol(s):
    drop(s, "exclude_from_sim", "embedded_fonts", "embedded_files", "duplicate_pin_numbers_are_jumpers",
         "jumper_pin_groups")
    for k in ("pin_names", "pin_numbers"):
        pn = kid(s, k)
        if pn is not None and yesno(pn, "hide"):
            pn.append(Sym("hide"))
    nid = [4]
    for p in kids(s, "property"):
        conv_property(p, nid)
    for u in kids(s, "symbol"):
        drop(u, "unit_name")
        for g in u[2:]:
            if not isinstance(g, list):
                continue
            if g[0] == "pin":
                if yesno(g, "hide"):
                    g.insert(3, Sym("hide"))
                for nn in kids(g, "name") + kids(g, "number"):
                    fix_effects(kid(nn, "effects"))
                for alt in kids(g, "alternate"):
                    pass
            elif g[0] == "text":
                fix_effects(kid(g, "effects"))
                drop(g, "exclude_from_sim")


def convert_symlib(path):
    t = parse(open(path, encoding="utf-8").read())
    out = [Sym("kicad_symbol_lib"), [Sym("version"), SYM_VERSION], [Sym("generator"), Sym("kicad_symbol_editor")]]
    for s in kids(t, "symbol"):
        conv_lib_symbol(s)
        out.append(s)
    write6(path, out)


# --------------------------------------------------------------------------- schematic
def rect_to_polylines(r):
    """KiCad 6 schematic graphic lines have exactly two points: one rectangle -> four lines."""
    import uuid as _uuid
    st, en = kid(r, "start"), kid(r, "end")
    x0, y0, x1, y1 = st[1], st[2], en[1], en[2]
    stroke = kid(r, "stroke") or [Sym("stroke"), [Sym("width"), 0], [Sym("type"), Sym("default")]]
    if kid(stroke, "color") is None:
        stroke.append([Sym("color"), 0, 0, 0, 0])
    base = _uuid.UUID(kid(r, "uuid")[1])
    corners = ((x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0))
    out = []
    for i in range(4):
        (a, b), (c, d) = corners[i], corners[i + 1]
        u = str(_uuid.uuid5(base, "edge%d" % i))
        out.append([Sym("polyline"), [Sym("pts"), [Sym("xy"), a, b], [Sym("xy"), c, d]],
                    [list(y) if isinstance(y, list) else y for y in stroke], [Sym("uuid"), u]])
    return out


def convert_sch(path):
    t = parse(open(path, encoding="utf-8").read())
    assert t[0] == "kicad_sch"
    root_uuid = kid(t, "uuid")[1]
    sym_inst = []
    out = []
    for x in t:
        h = head(x)
        if h == "version":
            x[1] = SCH_VERSION
        elif h == "generator":
            x[1] = Sym("eeschema")
        elif h in ("generator_version", "embedded_fonts", "embedded_files"):
            continue
        elif h == "lib_symbols":
            for s in kids(x, "symbol"):
                conv_lib_symbol(s)
        elif h == "symbol":
            drop(x, "exclude_from_sim", "dnp")
            if yesno(x, "fields_autoplaced"):
                x.insert(x.index(kid(x, "uuid")), [Sym("fields_autoplaced")])
            nid = [4]
            for p in kids(x, "property"):
                conv_property(p, nid)
            inst = kid(x, "instances")
            drop(x, "instances")
            ref = next(p[2] for p in kids(x, "property") if p[1] == "Reference")
            val = next(p[2] for p in kids(x, "property") if p[1] == "Value")
            fpn = next((p[2] for p in kids(x, "property") if p[1] == "Footprint"), "")
            unit = kid(x, "unit")[1]
            if inst is not None:
                pth = kid(kid(inst, "project"), "path")
                ref = kid(pth, "reference")[1]
                unit = kid(pth, "unit")[1]
            sym_inst.append([Sym("path"), "/" + kid(x, "uuid")[1], [Sym("reference"), ref], [Sym("unit"), unit],
                             [Sym("value"), val], [Sym("footprint"), fpn]])
        elif h in ("label", "global_label", "hierarchical_label", "text"):
            if yesno(x, "fields_autoplaced"):
                x.insert(x.index(kid(x, "uuid")) if kid(x, "uuid") else len(x), [Sym("fields_autoplaced")])
            drop(x, "exclude_from_sim")
            fix_effects(kid(x, "effects"))
            for p in kids(x, "property"):
                conv_property(p, [0])
        elif h == "rectangle":
            out.extend(rect_to_polylines(x))
            continue
        elif h in ("wire", "bus", "polyline"):
            st = kid(x, "stroke")
            if st is not None and kid(st, "color") is None:
                st.append([Sym("color"), 0, 0, 0, 0])
        elif h == "sheet_instances":
            continue
        out.append(x)
    out.append([Sym("sheet_instances"), [Sym("path"), "/", [Sym("page"), "1"]]])
    sym_inst.sort(key=lambda r: r[2][1])
    out.append([Sym("symbol_instances")] + sym_inst)
    write6(path, out)


# --------------------------------------------------------------------------- project / local settings
def convert_pro(path):
    d = json.load(open(path))
    ns = d.get("net_settings", {})
    pats = ns.pop("netclass_patterns", None) or []
    ns.pop("netclass_assignments", None)
    for c in ns.get("classes", []):
        c.pop("priority", None)
        c.pop("tuning_profile", None)
        c["nets"] = [p["pattern"] for p in pats if p["netclass"] == c["name"]]
    ns["meta"] = {"version": 2}
    ds = d.setdefault("board", {}).setdefault("design_settings", {})
    ex = [e for e in ds.get("drc_exclusions", []) if not e.startswith("lib_footprint_mismatch|")]
    for u, x, y in LOST_ATTR:
        ex.append("lib_footprint_mismatch|%d|%d|%s|00000000-0000-0000-0000-000000000000"
                  % (round(float(x) * 1e6), round(float(y) * 1e6), u))
    ds["drc_exclusions"] = ex
    d["meta"] = {"filename": os.path.basename(path), "version": 1}
    json.dump(d, open(path, "w"), indent=2)


def convert_prl(path):
    d = {"board": {"active_layer": 0, "active_layer_preset": "", "auto_track_width": True, "hidden_nets": [],
                   "high_contrast_mode": 0, "net_color_mode": 1,
                   "opacity": {"pads": 1.0, "tracks": 1.0, "vias": 1.0, "zones": 0.6},
                   "ratsnest_display_mode": 0, "visible_items": [], "visible_layers": "fffffff_ffffffff"},
         "meta": {"filename": os.path.basename(path), "version": 3},
         "project": {"files": []}}
    json.dump(d, open(path, "w"), indent=2)


def convert_dru(path):
    """KiCad 6 knows insideCourtyard(); KiCad 7+ renamed it intersectsCourtyard() but keeps the old name."""
    if os.path.exists(path):
        t = open(path, encoding="utf-8").read().replace("intersectsCourtyard(", "insideCourtyard(")
        open(path, "w", encoding="utf-8", newline="\n").write(t)


def main(proj):
    name = os.path.basename(os.path.normpath(proj))
    base = os.path.join(proj, name)
    convert_sch(base + ".kicad_sch")
    convert_pcb(base + ".kicad_pcb")
    for lib in glob.glob(os.path.join(proj, "libraries", "*.kicad_sym")):
        convert_symlib(lib)
    convert_pro(base + ".kicad_pro")
    convert_dru(base + ".kicad_dru")
    convert_prl(base + ".kicad_prl")
    print("converted to KiCad 6.0 format:", proj)


if __name__ == "__main__":
    main(sys.argv[1])
