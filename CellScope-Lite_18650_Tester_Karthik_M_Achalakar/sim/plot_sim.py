"""Plot Ngspice (eSim 2.6, ngspice-45.2) results for the report."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams.update({"font.size": 10, "axes.grid": True, "grid.alpha": 0.3, "axes.spines.top": False, "axes.spines.right": False})
C1, C2, C3 = "#1f5fa8", "#c4452b", "#2e8b57"

d = np.genfromtxt("sim/out_tran.csv", names=True)
t = d["time"] * 1e3
fig, ax = plt.subplots(3, 1, figsize=(8.5, 7.2), sharex=True)
ax[0].plot(t, d["I_LOAD"], color=C1, lw=1.6); ax[0].set_ylabel("I_LOAD (A)")
ax[0].set_title("CC load + UVLO cut-off: transient (time-compressed discharge)", fontsize=11, loc="left")
ax[0].annotate("0.247 A @ 25 mV", (40, 0.26), color=C1); ax[0].annotate("0.968 A @ 97.5 mV", (130, 0.9), color=C1)
ax[1].plot(t, d["vVBAT"], color=C2, lw=1.6); ax[1].set_ylabel("V_BAT (V)")
ax[1].axhline(3.0, color="0.5", ls="--", lw=0.8)
ax[2].plot(t, d["vUVLO"], color=C3, lw=1.6, label="UVLO (comparator out)")
ax[2].plot(t, d["vGATE"], color=C1, lw=1.2, ls="--", label="MOSFET gate")
ax[2].set_ylabel("V"); ax[2].set_xlabel("time (ms)"); ax[2].legend(loc="center left", frameon=False)
fig.tight_layout(); fig.savefig("sim/fig_transient.png", dpi=160)

dc = np.genfromtxt("sim/out_dc.csv", names=True)
vs = dc[dc.dtype.names[0]] * 1e3
i = dc["vSENSE_HI"] / 0.1
fig, ax = plt.subplots(figsize=(6.2, 4.2))
ax.plot(vs, vs / 100.0, color="0.6", ls="--", lw=1, label="ideal  I = V_SET / 0.1 ohm")
ax.plot(vs, i, color=C1, lw=1.8, label="simulated (ngspice)")
ax.set_xlabel("V_SET (mV)"); ax.set_ylabel("I_LOAD (A)"); ax.legend(frameon=False)
err = np.max(np.abs(i[vs > 10] - vs[vs > 10] / 100) / (vs[vs > 10] / 100)) * 100
ax.set_title("Set-point linearity (max error %.1f %% above 10 mV)" % err, fontsize=11, loc="left")
fig.tight_layout(); fig.savefig("sim/fig_linearity.png", dpi=160)

dn = np.genfromtxt("sim/out_uvlo_down.csv", names=True)
up = np.genfromtxt("sim/out_uvlo_up.csv", names=True)
fig, ax = plt.subplots(figsize=(6.2, 4.2))
ax.plot(dn["vVBAT"], dn["vUVLO"], color=C2, lw=1.8, label="cell falling")
ax.plot(up["vVBAT"], up["vUVLO"], color=C1, lw=1.8, ls="--", label="cell rising")
ax.axvline(3.0175, color=C2, lw=0.8, ls=":"); ax.axvline(3.4905, color=C1, lw=0.8, ls=":")
ax.text(3.03, 1.5, "trip 3.017 V", color=C2); ax.text(3.50, 1.0, "release 3.490 V", color=C1)
ax.set_xlabel("V_BAT (V)"); ax.set_ylabel("UVLO output (V)"); ax.legend(frameon=False, loc="upper right")
ax.set_title("UVLO comparator hysteresis (DC sweep)", fontsize=11, loc="left")
fig.tight_layout(); fig.savefig("sim/fig_uvlo_hysteresis.png", dpi=160)
print("linearity max err %.2f %%" % err)
