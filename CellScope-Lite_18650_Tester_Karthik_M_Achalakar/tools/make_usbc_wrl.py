"""Simplified VRML body for HRO TYPE-C-31-M-12 (datasheet: 8.94 W x 7.35 L x 3.16 H mm).
KiCad VRML unit = 0.1 inch (2.54 mm). Footprint origin: pads at y=-4.04 (rear), mating face at +y."""
import sys
U = 1 / 2.54
def box(x0, x1, y0, y1, z0, z1, rgb, shin=0.6):
    # VRML: x right, y up, z out of board. KiCad footprint y is down -> VRML y = -y
    X = [x0 * U, x1 * U]; Y = [-y1 * U, -y0 * U]; Z = [z0 * U, z1 * U]
    pts = [(X[i], Y[j], Z[k]) for k in (0, 1) for j in (0, 1) for i in (0, 1)]
    faces = [(0, 2, 3, 1), (4, 5, 7, 6), (0, 1, 5, 4), (2, 6, 7, 3), (0, 4, 6, 2), (1, 3, 7, 5)]
    p = ", ".join("%.4f %.4f %.4f" % q for q in pts)
    f = ", ".join("%d, %d, %d, %d, -1" % q for q in faces)
    return ("Shape { appearance Appearance { material Material { diffuseColor %s specularColor 0.9 0.9 0.9 shininess %s } }\n"
            " geometry IndexedFaceSet { coord Coordinate { point [ %s ] } coordIndex [ %s ] } }\n") % (rgb, shin, p, f)
shell = "0.78 0.78 0.80"
out = "#VRML V2.0 utf8\n# Simplified HRO TYPE-C-31-M-12 body (dimensions per datasheet), CellScope-Lite project\n"
out += box(-4.47, 4.47, -3.25, 4.10, 0.0, 3.16, shell)          # metal shell
out += box(-3.35, 3.35, 3.20, 4.12, 0.55, 2.61, "0.05 0.05 0.05", 0.1)  # mating opening (dark)
out += box(-2.20, 2.20, 3.30, 4.13, 1.30, 1.86, "0.15 0.15 0.15", 0.1)  # tongue
for x in (-3.25, -2.45, -1.75, -1.25, -0.75, -0.25, 0.25, 0.75, 1.25, 1.75, 2.45, 3.25):
    out += box(x - 0.12, x + 0.12, -4.60, -3.25, 0.0, 0.15, "0.85 0.7 0.3")  # rear SMD leads
open(sys.argv[1], "w").write(out)
print("wrote", sys.argv[1])
