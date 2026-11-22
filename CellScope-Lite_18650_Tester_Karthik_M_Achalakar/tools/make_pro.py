"""Write design rules + net classes into CellScope-Lite.kicad_pro (merging with what KiCad wrote)."""
import json, os, sys
path = sys.argv[1]
d = json.load(open(path)) if os.path.exists(path) else {}
def nc(name, clr, tw, vd, vdrill, prio):
    return {"name": name, "clearance": clr, "track_width": tw, "via_diameter": vd, "via_drill": vdrill,
            "microvia_diameter": 0.3, "microvia_drill": 0.1, "diff_pair_gap": 0.25, "diff_pair_width": 0.2,
            "diff_pair_via_gap": 0.25, "wire_width": 6, "bus_width": 12, "line_style": 0,
            "pcb_color": "rgba(0, 0, 0, 0.000)", "schematic_color": "rgba(0, 0, 0, 0.000)", "priority": prio}
POWER = ["/VBAT", "+5V", "/VBUS_IN", "/SENSE_HI", "/FET_D", "/BAT_N", "GND"]
ns = d.setdefault("net_settings", {})
ns["classes"] = [nc("Default", 0.15, 0.25, 0.6, 0.3, 2147483647), nc("Power", 0.2, 0.8, 0.8, 0.4, 0)]
ns["meta"] = {"version": 4}
ns["netclass_patterns"] = [{"netclass": "Power", "pattern": n} for n in POWER]
ns.setdefault("net_colors", None); ns.setdefault("netclass_assignments", None)
ds = d.setdefault("board", {}).setdefault("design_settings", {})
rules = ds.setdefault("rules", {})
rules.update({"min_clearance": 0.15, "min_track_width": 0.15, "min_via_diameter": 0.5, "min_via_annular_width": 0.1,
              "min_through_hole_diameter": 0.25, "min_copper_edge_clearance": 0.3, "min_hole_clearance": 0.25,
              "min_hole_to_hole": 0.25, "min_silk_clearance": 0.0, "min_text_height": 0.8, "min_text_thickness": 0.12,
              "solder_mask_to_copper_clearance": 0.0, "min_microvia_diameter": 0.2, "min_microvia_drill": 0.1})
ds["track_widths"] = [0.0, 0.25, 0.4, 0.8, 1.2]
ds["via_dimensions"] = [{"diameter": 0.0, "drill": 0.0}, {"diameter": 0.6, "drill": 0.3}, {"diameter": 0.8, "drill": 0.4}]
d.setdefault("meta", {"filename": os.path.basename(path), "version": 3})
json.dump(d, open(path, "w"), indent=2)
print("project rules + net classes written")
