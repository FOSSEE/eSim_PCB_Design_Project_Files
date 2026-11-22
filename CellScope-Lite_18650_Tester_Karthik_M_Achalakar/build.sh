#!/bin/sh
# Full regeneration: schematic -> ERC -> netlist check -> PCB skeleton -> project rules
set -e
cd "$(dirname "$0")"
ESIM=${ESIM:-/d/eSim}
K="$ESIM/tools/kicad/bin/kicad-cli.exe"; KPY="$ESIM/tools/kicad/bin/python.exe"
SYM="$ESIM/tools/kicad/share/kicad/symbols"; FP="$ESIM/tools/kicad/share/kicad/footprints"
mkdir -p build
echo "schematicFile CellScope-Lite.kicad_sch" > CellScope-Lite/CellScope-Lite.proj
python tools/make_symlib.py CellScope-Lite/libraries/CellScopeLite.kicad_sym
python tools/gen_sch.py "$SYM" CellScope-Lite/CellScope-Lite.kicad_sch 20250114 9.0
"$K" sch erc --severity-all --format report -o build/erc.rpt CellScope-Lite/CellScope-Lite.kicad_sch | tail -1
"$K" sch export netlist --format kicadsexpr -o build/CellScope-Lite.net CellScope-Lite/CellScope-Lite.kicad_sch >/dev/null
python tools/check_netlist.py build/CellScope-Lite.net | tail -1
if [ "$1" = "pcb" ]; then
  "$KPY" tools/build_pcb.py build/CellScope-Lite.net "$FP" CellScope-Lite/CellScope-Lite.kicad_pcb
  python tools/make_pro.py CellScope-Lite/CellScope-Lite.kicad_pro
  cp CellScope-Lite/CellScope-Lite.kicad_pcb build/skeleton.kicad_pcb
fi
if [ "$1" = "pcb" ] || [ "$1" = "route" ]; then
  "$KPY" tools/export_geom.py build/skeleton.kicad_pcb build/geom.json
  python tools/router.py build/geom.json build/routes.json | tail -2
  "$KPY" tools/apply_routes.py build/skeleton.kicad_pcb build/routes.json CellScope-Lite/CellScope-Lite.kicad_pcb
  python tools/make_pro.py CellScope-Lite/CellScope-Lite.kicad_pro
fi
