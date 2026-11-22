#!/bin/sh
# Final checks + all deliverable outputs from the finished board (uses only eSim's bundled KiCad).
set -e
cd "$(dirname "$0")/.."
ESIM=${ESIM:-/d/eSim}
K="$ESIM/tools/kicad/bin/kicad-cli.exe"; KPY="$ESIM/tools/kicad/bin/python.exe"
P=CellScope-Lite/CellScope-Lite
EDGE="/c/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"
mkdir -p build docs/img fab/gerbers

# ---- checks ----
"$K" sch erc --severity-all --format report -o build/erc.rpt $P.kicad_sch | tail -1
"$K" pcb drc --severity-all --schematic-parity --format json -o build/drc_final.json $P.kicad_pcb | grep Found
"$K" pcb drc --severity-all --schematic-parity --format report -o docs/DRC_report.rpt $P.kicad_pcb >/dev/null
cp build/erc.rpt docs/ERC_report.rpt
"$KPY" tools/board_stats.py $P.kicad_pcb build/board_stats.json

# ---- schematic PDF + images ----
"$K" sch export pdf -o docs/CellScope-Lite_schematic.pdf $P.kicad_sch >/dev/null
"$K" sch export svg -o build/ $P.kicad_sch >/dev/null
python tools/svg2png.py build/CellScope-Lite.svg docs/img/schematic.png 4200
python -c "from PIL import Image; im=Image.open('docs/img/schematic.png'); w,h=im.size; im.crop((0,0,int(w*0.67),int(h*0.80))).save('docs/img/schematic_left.png'); im.crop((int(w*0.33),0,w,h)).save('docs/img/schematic_right.png')"

# ---- 2D board plots (layers) ----
for L in F.Cu In1.Cu In2.Cu B.Cu; do
  "$K" pcb export svg --mode-single --layers "$L,Edge.Cuts" --exclude-drawing-sheet --page-size-mode 2 \
      -o build/layer_$L.svg $P.kicad_pcb >/dev/null
done
"$K" pcb export svg --mode-single --layers "F.Cu,F.SilkS,F.Mask,Edge.Cuts" --exclude-drawing-sheet --page-size-mode 2 \
    -o build/top2d.svg $P.kicad_pcb >/dev/null
python tools/svg2png.py build/top2d.svg docs/img/pcb_top_2d.png 2400
for L in F.Cu In1.Cu In2.Cu B.Cu; do python tools/svg2png.py build/layer_$L.svg build/layer_$L.png 1400; done
python tools/layers_sheet.py build docs/img/layers.png

# ---- 3D renders ----
R="$K pcb render --quality high --background opaque --width 2000 --height 1400"
$R --side top -o docs/img/pcb_top_3d.png $P.kicad_pcb >/dev/null
$R --side bottom -o docs/img/pcb_bottom_3d.png $P.kicad_pcb >/dev/null
$R --side top --perspective --rotate "320,0,25" --zoom 1.05 -o docs/img/pcb_iso.png $P.kicad_pcb >/dev/null
$R --side top --perspective --rotate "305,0,205" --zoom 1.05 -o docs/img/pcb_iso_back.png $P.kicad_pcb >/dev/null

# ---- manufacturing ----
"$K" pcb export gerbers --layers "F.Cu,In1.Cu,In2.Cu,B.Cu,F.Paste,B.Paste,F.SilkS,B.SilkS,F.Mask,B.Mask,Edge.Cuts" \
    --subtract-soldermask -o fab/gerbers/ $P.kicad_pcb >/dev/null
"$K" pcb export drill --excellon-separate-th --generate-map --map-format gerberx2 -o fab/gerbers/ $P.kicad_pcb >/dev/null
"$K" pcb export pos --format csv --units mm --side front --use-drill-file-origin -o fab/CellScope-Lite_cpl.csv $P.kicad_pcb >/dev/null || \
"$K" pcb export pos --format csv --units mm --side front -o fab/CellScope-Lite_cpl.csv $P.kicad_pcb >/dev/null
"$K" sch export bom --fields "Reference,Value,Footprint,MPN,LCSC,\${QUANTITY}" --labels "Designator,Value,Footprint,MPN,LCSC,Qty" \
    --group-by "Value,Footprint,MPN" --exclude-dnp -o fab/CellScope-Lite_bom.csv $P.kicad_sch >/dev/null
"$K" pcb export step --subst-models --include-tracks --force -o fab/CellScope-Lite.step $P.kicad_pcb >/dev/null 2>&1 || echo "step export skipped"
(cd fab && python -c "import shutil; shutil.make_archive('CellScope-Lite_gerbers', 'zip', 'gerbers')")
echo "outputs done"
