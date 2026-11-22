"""System block diagram for the report (matplotlib)."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

fig, ax = plt.subplots(figsize=(11, 5.6))
ax.set_xlim(0, 110)
ax.set_ylim(0, 56)
ax.axis("off")

PW, AN, DG, MC = "#fde7c8", "#d6e8fa", "#e2f2dc", "#eee"


def box(x, y, w, h, title, sub, fc):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.4,rounding_size=1.2", fc=fc, ec="#333", lw=1.2))
    ax.text(x + w / 2, y + h - 2.3, title, ha="center", va="top", fontsize=10.5, weight="bold")
    ax.text(x + w / 2, y + h - 6.2, sub, ha="center", va="top", fontsize=8.2, color="#333", linespacing=1.35)


def poly(pts, label="", color="#333", lw=1.6, ls="-", lpos=None):
    for (a, b) in zip(pts[:-2], pts[1:-1]):
        ax.plot([a[0], b[0]], [a[1], b[1]], color=color, lw=lw, ls=ls)
    (x1, y1), (x2, y2) = pts[-2], pts[-1]
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=13, color=color, lw=lw, ls=ls))
    if label:
        ax.text(lpos[0], lpos[1], label, ha="left", va="center", fontsize=7.8, color=color)


def arrow(x1, y1, x2, y2, label="", color="#333", lw=1.6, ls="-"):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=13, color=color, lw=lw, ls=ls))
    if label:
        ax.text((x1 + x2) / 2, (y1 + y2) / 2 + 0.9, label, ha="center", va="bottom", fontsize=7.8, color=color)


box(1, 38, 17, 14, "USB-C 5 V", "CC 5.1k sink\n1.5 A polyfuse\nSMAJ5.0A TVS", PW)
box(24, 38, 19, 14, "TP4056", "1 A CC/CV charger\nR_PROG 1.2k\nCHRG / FULL LEDs", PW)
box(49, 38, 20, 14, "18650 cell", "Keystone 1042\n+ DW01A / FS8205A\nOV 4.3 / UV 2.4 V / OC", PW)
box(24, 18, 19, 14, "3.3 V + 2.048 V", "AP2112K LDO\nLM4040 0.1 % ref", AN)
box(49, 18, 20, 14, "Set-point", "trimmer 0-97.5 mV\nor ext. DAC (JP1)\nsoft-start, LOAD sw", AN)
box(77, 33, 22, 19, "CC electronic load", "MCP6002 + IRLZ44N\nI = V_SET / 0.1 ohm\n0 - 0.975 A\nKelvin shunt (NT1)", AN)
box(77, 4, 22, 21, "UVLO cut-off", "MCP6002 comparator\ntrip 3.01 V\nrelease 3.50 V (latching)\nCUTOFF LED", AN)
box(49, 1, 20, 13, "INA226", "16-bit V / I / P, I2C 0x40\n25 uA / 1.25 mV LSB", DG)
box(24, 1, 19, 13, "Host / Qwiic", "J2 header, J3 JST-SH\nSDA SCL ALERT EXT_SET", DG)

arrow(18, 45, 24, 45, "5 V")
arrow(43, 45, 49, 45, "1 A")
arrow(69, 45, 77, 45, "VBAT")
arrow(33.5, 38, 33.5, 32, "5 V")
arrow(43, 25, 49, 25, "VREF")
poly([(66, 32), (66, 36), (77, 36)], "V_SET", lpos=(67, 37.2))
poly([(77, 34), (73.5, 34), (73.5, 7.5), (69, 7.5)], "Kelvin\nV+ / V-", color="#2e6fb0", ls="--", lpos=(69.6, 14))
arrow(82, 33, 82, 25, "", color="#c4452b")
ax.text(82.6, 29, "V_BAT sense", fontsize=7.8, color="#c4452b", va="center")
arrow(95, 25, 95, 33, "", color="#c4452b")
ax.text(88.3, 31.5, "disable", fontsize=7.8, color="#c4452b", va="center")
arrow(49, 7.5, 43, 7.5, "I2C")
ax.text(1, 54.5, "CellScope-Lite: system block diagram", fontsize=13, weight="bold")
ax.text(64, 54.5, "power path", fontsize=8.5, color="#a0601a")
ax.add_patch(FancyBboxPatch((60, 54.3), 3, 1.6, boxstyle="square,pad=0", fc=PW, ec="#333", lw=0.6))
ax.text(76, 54.5, "analog control", fontsize=8.5)
ax.add_patch(FancyBboxPatch((72, 54.3), 3, 1.6, boxstyle="square,pad=0", fc=AN, ec="#333", lw=0.6))
ax.text(92, 54.5, "measurement / I/O", fontsize=8.5)
ax.add_patch(FancyBboxPatch((88, 54.3), 3, 1.6, boxstyle="square,pad=0", fc=DG, ec="#333", lw=0.6))
fig.tight_layout()
fig.savefig("docs/img/block_diagram.png", dpi=170)
print("ok")
