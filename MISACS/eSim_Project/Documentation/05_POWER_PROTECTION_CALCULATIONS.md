# MISACS Phase 3 — Power and Protection Engineering Calculations
**Phase 3 — Final Engineering and Submission Preparation**
**Project:** Modular Industrial Sensor Acquisition and Control System (MISACS)  
**Program:** FOSSEE eSim Winter Internship 2026 — Task 7  
**Revision:** Phase 3 Final Review Release Candidate  
**Status:** Engineering Release Candidate — Pending Physical Prototype Validation  

---

## 1. Primary TVS Clamping Analysis (Littelfuse SMBJ30A)
- **Device:** Littelfuse SMBJ30A (Unidirectional, 600W peak pulse power rating at $10/1000\,\mu\text{s}$).
- **Reverse Stand-off Voltage ($V_{RWM}$):** $30.0\,\text{V}$. (Maximum reverse leakage current $I_R \le 5\,\mu\text{A}$ at $25^\circ\text{C}$).
- **Breakdown Voltage ($V_{BR}$):** $33.3\,\text{V}$ min, $34.5\,\text{V}$ typ, $36.8\,\text{V}$ max at $I_T = 1.0\,\text{mA}$ test current.
- **Dynamic Resistance ($R_{dyn}$):**
  $$R_{dyn} \approx \frac{V_C - V_{BR}}{I_{PP}} = \frac{48.4\,\text{V} - 34.5\,\text{V}}{12.4\,\text{A}} \approx 1.12\,\Omega$$
- **Circuit Surge Response at $+50.0\,\text{V}$ Input:**
  In the MISACS power entry network, the source impedance ($R_{src} = 0.5\,\Omega$) and PTC fuse cold resistance ($R_{fuse} = 0.15\,\Omega$) form a voltage divider with the conducting TVS ($R_{dyn} = 1.12\,\Omega$):
  $$I_{surge} = \frac{V_{in} - V_{BR}}{R_{src} + R_{fuse} + R_{dyn}} = \frac{50.0\,\text{V} - 34.5\,\text{V}}{0.5 + 0.15 + 1.12} = \frac{15.5\,\text{V}}{1.77\,\Omega} \approx 8.76\,\text{A}$$
  $$V_{TVS,clamped} = 34.5\,\text{V} + (8.76\,\text{A} \times 1.12\,\Omega) = \mathbf{44.31\,\text{V}} \quad (\text{Simulated in TB1: } \mathbf{44.020\,\text{V}})$$
- **Margin to Downstream Components:**
  The downstream switching regulator is the high-voltage series **LM2576HVS-5.0**, which has an absolute maximum input rating of **$60.0\,\text{V}$**.
  $$\text{Safety Margin} = 60.0\,\text{V} - 44.02\,\text{V} = \mathbf{15.98\,\text{V}}$$
  Even under the manufacturer absolute worst-case datasheet limit ($48.4\,\text{V}$ at $12.4\,\text{A}$), the margin is $11.6\,\text{V}$ below the component breakdown limit.

---

## 2. Reverse-Polarity Fault Path and Fuse Coordination Analysis

### 2.1 Logic Rail Reverse Protection (Unconditional)
Protected by Vishay SS36 series Schottky barrier diode `D2` ($V_R = 60\,\text{V}, I_F = 3\,\text{A}$, SMC package). Under $-24\,\text{V}$ reverse input, D2 is reverse-biased with $< 20\,\mu\text{A}$ leakage, maintaining the logic rail at $V_{prot} = -0.0000\,\text{V}$. The logic circuit is 100% unconditionally protected against reverse supply connection.

### 2.2 Connector J1 Reverse Shunt Diode `D14` Architecture & Coordination Truth
- **Device Placement & Topology:** Diode `D14` (Vishay SS56-E3/57T, 60V 5A SMC Schottky) is placed directly across incoming power terminals at J1 with Cathode at `+24V` and Anode at `GND`.
- **Branch Topology Truth:** Onboard fuses `F1` (logic branch PTC) and `F2, F3` (actuator branch fuses) are located downstream on branched circuits. **Neither F1, F2, nor F3 is in series with J1 or the D14 shunt loop.** Under a reverse-voltage event at J1, reverse current flows directly through D14 without passing through F1, F2, or F3. Consequently, internal board fuses will not trip or clear to protect D14.
- **Internal Coordination Non-Applicability:** Internal fuse-diode coordination is **NOT APPLICABLE** to D14. Protection of D14 against thermal burnout is strictly conditional upon upstream external current limiting or fusing provided by the external power source.
- **Static DC Sweep Performance:** Under a static DC sweep with an assumed source resistance of $R_{src} = 0.5\,\Omega$, D14 conducts in forward bias, clamping connector J1 entry to $\mathbf{-1.432\,\text{V}}$ at 5A ($V_F \approx 0.75\,\text{V}$ static).
- **Non-Repetitive Peak Surge Rating ($I_{FSM}$):**
  - Vishay SS56 datasheet publishes $I_{FSM} = 150\,\text{A}$ for an $8.3\,\text{ms}$ single half-sine wave (JEDEC method).
  - Energy integral equivalent:
    $$I^2t = \frac{1}{2} I_{peak}^2 \times t_w = \frac{1}{2} (150\,\text{A})^2 \times 0.0083\,\text{s} \approx \mathbf{93.38\,\text{A}^2\text{s}}$$
- **Critical Distinction: Non-Repetitive Surge vs Continuous Destruction:**
  - The $150\,\text{A}$ ($93.38\,\text{A}^2\text{s}$) rating is a **non-repetitive test rating** for an isolated half-sine pulse. It is **NOT** a continuous destruction threshold or a continuous shunt conduction rating.
  - Under sustained reverse voltage from an uncoordinated source (such as a 5A bench power supply in constant-current mode), D14 dissipates continuous power:
    $$P_D = I_{rev} \times V_F = 5.0\,\text{A} \times 0.75\,\text{V} = \mathbf{3.75\,\text{W}}$$
    Given the SMC package thermal resistance of $R_{\theta JA} \approx 55-75\,\text{K/W}$, continuous dissipation causes internal junction temperature to rapidly exceed $250^\circ\text{C}$, resulting in catastrophic thermal destruction (open-circuit or package rupture) within seconds.
  - Therefore, reverse-polarity survival of D14 is **strictly conditional** upon an external upstream fast-clearing fuse or fast electronic foldback current limiting on the 24V supply.

### 2.3 Official Manufacturer Datasheet Data Across Evaluated 5A Fuses

| Parameter | Littelfuse 0451005.MRL | Littelfuse 0217005.MXP | Littelfuse 0216005.MXP |
| :--- | :--- | :--- | :--- |
| **Series / Construction** | 451 Series NANO2® SMT Wire-in-Air | 217 Series $5\times 20\,\text{mm}$ Glass Cartridge | 216 Series $5\times 20\,\text{mm}$ Ceramic Cartridge |
| **Package** | 2410 Surface Mount (Ceramic/Silver) | $5\times 20\,\text{mm}$ Glass, Brass Endcaps | $5\times 20\,\text{mm}$ Ceramic, Sand Filler |
| **Current Rating** | 5.0 A | 5.0 A | 5.0 A |
| **Voltage Ratings** | $125\,\text{V AC/DC}$, $32\,\text{V DC}$ | $250\,\text{V AC}$, **$60\,\text{V DC}$** | $250\,\text{V AC}$ |
| **Interrupting Ratings** | $50\,\text{A}$ @ $125\,\text{V AC/DC}$, **$300\,\text{A}$ @ $32\,\text{V DC}$** | $50\,\text{A}$ @ $250\,\text{V AC}$, **$70\,\text{A}$ @ $60\,\text{V DC}$** | **$1500\,\text{A}$ @ $250\,\text{V AC}$** (No DC Rating) |
| **DC Breaking Limits** | Rated up to 300 A at 32 VDC | **Limited to 70 A at 60 VDC** | **NO DC RATING PUBLISHED** |
| **Nominal Cold Resistance** | $0.0125\,\Omega$ | $0.0137\,\Omega$ | $0.0183\,\Omega$ |
| **Nominal Melting $I^2t$** | **$5.566\,\text{A}^2\text{s}$** (at $10\times$, $50\,\text{A}$) | **$42.795\,\text{A}^2\text{s}$** (at $10\times$, $50\,\text{A}$) | **$27.46\,\text{A}^2\text{s}$** (at $10\times$, $50\,\text{A}$) |
| **Total Clearing $I^2t$** | **NOT PUBLISHED** by Littelfuse | **NOT PUBLISHED** by Littelfuse | **NOT PUBLISHED** by Littelfuse |
| **Time-Current Opening Time**<br>*(Pre-arcing/melting only; not total-clearing)* | $10\times$: 1 ms to 10 ms typical band | $10\times$: $\le 20\,\text{ms}$ maximum | $10\times$: $\le 20\,\text{ms}$ maximum |

> [!IMPORTANT]
> **Coordination Assessment:** The nominal fuse melting $I^2t$ is lower than the calculated diode non-repetitive surge $I^2t$ equivalent ($5.566\,\text{A}^2\text{s} < 93.38\,\text{A}^2\text{s}$ for the 0451005.MRL), but **this comparison does not establish protection coordination or prove diode survival**. Maximum total-clearing $I^2t$ remains unpublished by the manufacturer, and actual fault conditions are installation-dependent. Published time-current curves indicate manufacturer opening time (pre-arcing/melting only), not guaranteed total-clearing time.

### 2.4 Critical Post-Audit Corrections and Retractions of Unsupported Claims
To establish complete technical veracity, the following corrections and retractions are formally recorded:
1. **Retraction of 1–5 ms Clearing Claim:** Previous documentation claimed that fuses clear in 1–5 ms under the stated reverse fault. This claim is **retracted**. Total clearing time consists of melting time plus arcing time ($t_{clear} = t_{melt} + t_{arc}$); without exact prospective fault current, source inductance, and empirical oscillograms, a 1–5 ms clearing time cannot be guaranteed.
2. **Retraction of 8.3 ms Surge Interval Containment:** Previous documentation claimed that the fuse necessarily clears within D14's $8.3\,\text{ms}$ surge window. This claim is **retracted**. D14's $8.3\,\text{ms}$ rating corresponds to a single $60\,\text{Hz}$ half-sine pulse; DC arc extinction depends on circuit loop inductance and voltage, and cannot be assumed to clear within 8.3 ms.
3. **Melting $I^2t$ vs Total Clearing $I^2t$ Distinction:** Nominal melting $I^2t$ represents only the energy required to melt the fuse element, not the total energy let-through during arcing. A low nominal melting $I^2t$ does **not** prove total clearing $I^2t$ coordination.
4. **Retraction of Generic Arcing Multipliers:** The previously cited $1.5\times$ to $2.5\times$ arcing multipliers are empirical industry rules of thumb, **not** manufacturer-guaranteed figures. Total clearing $I^2t$ is unpublished by Littelfuse for all three devices.
5. **Retraction of 50 ms Foldback Safety Claim:** Claiming that an electronic power supply with a 50 ms foldback cutoff is inherently safe without a demonstrated diode thermal calculation is **retracted**. A 30 A peak foldback current sustained for 50 ms dissipates $E \approx 0.9\,\text{V} \times 30\,\text{A} \times 0.050\,\text{s} = 1.35\,\text{J}$ in the diode, which could exceed the transient thermal capacity of the SMC package.
6. **Part-Specific Application Limitations:**
   - **0217005.MXP ($5\times 20\,\text{mm}$ glass):** The DC interrupting rating is strictly **70 A at 60 VDC**. It must **not** be implied that this fuse can interrupt prospective DC fault currents above 70 A.
   - **0216005.MXP ($5\times 20\,\text{mm}$ ceramic):** The 1500 A rating applies **strictly to 250 VAC**. Littelfuse publishes **no DC interrupting rating**. It is prohibited to infer a DC rating from AC interrupting capacity, and 0216005.MXP cannot be designated as a qualified 24 VDC alternative without official manufacturer DC qualification data.

### 2.5 Maximum Available Fault Current & Source Model Limitations
The actual maximum available fault current during a reverse connection cannot be universally established from datasheet figures alone because it depends entirely on external installation parameters:
- **Loop Resistance:** $R_{loop} = R_{source} + R_{cable} + R_{fuse} + R_{D14(dyn)}$
- **Unknown Source Impedance:** If powered by an uncoordinated 5A bench supply in constant-current mode, fault current is restricted to 5A, preventing fuse opening and causing continuous $3.75\,\text{W}$ dissipation in D14, resulting in catastrophic diode destruction within seconds.
- **Bulk Bus Installations:** If powered by an industrial 24V central bus or battery bank with low impedance ($R_{loop} < 0.2\,\Omega$), prospective fault current can exceed $120\,\text{A}$, exceeding the 70 A DC interrupting rating of the 0217005 glass fuse.
- **Conclusion:** Without a standardized, site-specific power source specification and empirical testing, the maximum available fault current cannot be established, and D14 reverse shunt diode protection is formally designated:
  $$\mathbf{CONDITIONAL\ /\ NOT\ VERIFIED}$$

### 2.6 Actuator Branch Fuses (F2, F3)
- Fuses `F2` and `F3` protect the two actuator output channels against external wiring shorts and motor stalls.
- Component: Littelfuse 0451005.MRL (5A Fast-Acting NANO2, 2410 SMT).
- Nominal Melting $I^2t$: $5.566\,\text{A}^2\text{s}$.
- Interrupting rating: $300\,\text{A}$ at $32\,\text{VDC}$.

---


### 2.7 Logic Rail Resettable PTC Fuse (F1)
- **Component:** Bourns MF-MSMF110/33X-2 (Resettable PTC, SMD 1812 / 4532 Metric).
- **Hold Current ($I_{hold}$):** $1.10\,\text{A}$ at $23^\circ\text{C}$.
- **Trip Current ($I_{trip}$):** $2.20\,\text{A}$ at $23^\circ\text{C}$.
- **Maximum Voltage ($V_{max}$):** $24.0\,\text{V DC}$ (operating up to $33\,\text{V}$ maximum fault condition).
- **Resistance Range:** Initial minimum $R_{min} = 0.06\,\Omega$, post-trip maximum $R_{1max} = 0.21\,\Omega$ (nominal operating resistance $R_{fuse} \approx 0.15\,\Omega$).
- **Function:** Provides overcurrent protection and fault isolation specifically for the logic power rail (+24V_LOGIC_FUSED), feeding LM2576HVS-5.0 and AMS1117-3.3 regulators. F1 does not protect the high-current actuator channels (which are protected by F2 and F3) nor does it clear on reverse connection at J1.

---

## 3. Buck Converter Inductor Sizing and Continuous Capacity (LM2576HVS)
- **Fitted Inductor:** Bourns SRR1260-101M ($100\,\mu\text{H} \pm 20\%$, $DCR_{max} = 0.18\,\Omega$ / $180\,\text{m}\Omega$).
- **Manufacturer Ratings:** $I_{rms} = 1.70\,\text{A}$ ($\Delta T = 40^\circ\text{C}$), $I_{sat} = 1.70\,\text{A}$ ($25\%$ inductance roll-off).
- **Worst-Case Inductor Current Ripple ($\Delta I_L$):**
  $$\Delta I_L = \frac{(V_{in,max} - V_{out}) \times V_{out}}{V_{in,max} \times f_{sw,min} \times L_{min}}$$
  Evaluating at $V_{in,max} = 28\,\text{V}, V_{out} = 5.0\,\text{V}, f_{sw,min} = 47\,\text{kHz}, L_{min} = 80\,\mu\text{H}$:
  $$\Delta I_L = \frac{(28 - 5.0) \times 5.0}{28 \times 47\times 10^3 \times 80\times 10^{-6}} = \frac{115}{105.28} = \mathbf{1.092\,\text{A}}$$
  (Nominal operating conditions $24\text{V}_{in}, 52\,\text{kHz}, 100\,\mu\text{H}$: $\Delta I_L = 0.761\,\text{A}$).
- **Continuous Current Carrying Derivation:**
  1. *Peak Saturation Current Criterion:*
     $$I_{out,max(sat)} = I_{sat} - \frac{\Delta I_L}{2} = 1.70\,\text{A} - \frac{1.092\,\text{A}}{2} = \mathbf{1.154\,\text{A}} \approx \mathbf{1.15\,\text{A continuous worst-case}}$$
     (Nominal continuous capacity: $1.70 - 0.761/2 = \mathbf{1.32\,\text{A}}$).
  2. *RMS Thermal Heating Criterion:*
     $$I_{rms}^2 = I_{out}^2 + \frac{\Delta I_L^2}{12} \le 1.70^2 \implies I_{out,rms} \le \sqrt{1.70^2 - \frac{1.092^2}{12}} = \mathbf{1.67\,\text{A}}$$
- **System Operating Margin:** Actual onboard 5V system peak demand is $0.298\,\text{A} \approx 0.30\,\text{A}$.
  $$\text{Design Margin} = \frac{1.154\,\text{A}}{0.298\,\text{A}} = \mathbf{3.87\times} \quad (287\% \text{ continuous current headroom})$$
- **Output Steady-State Performance ($1.5\,\text{ms} \le t \le 2.0\,\text{ms}$):**
  - Evaluated with Bourns worst-case DCR ($R_{L1} = 0.18\,\Omega$ / $180\,\text{m}\Omega$):
  - Mean Output Voltage: **$4.993\,\text{V}$** (specification window: $4.90\,\text{V}$ to $5.10\,\text{V}$)
  - Peak-to-Peak Output Ripple: **$67.59\,\text{mV}_{pp}$** (specification limit: $\le 100\,\text{mV}_{pp}$).
