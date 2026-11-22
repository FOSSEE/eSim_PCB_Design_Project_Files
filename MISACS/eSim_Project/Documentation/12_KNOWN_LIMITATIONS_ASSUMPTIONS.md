# MISACS Phase 3 — Final Engineering and Submission Preparation — Known Engineering Limitations and Assumptions
**Project:** Modular Industrial Sensor Acquisition and Control System (MISACS)  
**Program:** FOSSEE eSim Winter Internship 2026 — Task 7  
**Revision:** Phase 3 — Final Engineering and Submission Preparation Final Qualified Release Candidate  
**Status:** Engineering Release Candidate — Pending Physical Prototype Validation  

---

## 1. Technical Boundary Clarifications

### A. Non-Isolated RS-485 Interface
- **Architecture:** The onboard MAX3485EESA transceiver is a **non-isolated** $+3.3\text{V}$ transceiver sharing common system ground. Pin 3 of terminal block `J4` is connected directly to system GND.
- **Limitation:** For field installations subject to ground loops, differential earth potentials ($> \pm 7\text{V}$), or high-voltage transient coupling, an external isolated repeater or an isolated transceiver module (e.g., ADM2587E or ISO1410) must be utilized.

### B. Power Entry Reverse-Polarity Clearing & Coordination
- **Architecture:** Shunt reverse-polarity diode `D14` (Vishay SS56) clamps reversed supply voltages to $-1.432\text{V}$ under a static DC sweep with $0.5\,\Omega$ source resistance ($-0.75\text{V}$ static $V_F$ at 5A rated current). Series Schottky diode `D2` (SS36) completely isolates the logic rail ($V_{prot} = -0.0000\text{V}$).
- **Coordination Limits & Non-Repetitive Surge:** Diode D14 non-repetitive surge rating is $I_{FSM} = 150\,\text{A}$ ($8.3\,\text{ms}$ single half-sine wave), corresponding to an energy integral of $I^2t \approx 93.38\,\text{A}^2\text{s}$.
- **Distinction Between Transient Surge and Continuous Conduction:** The $150\,\text{A}$ rating ($93.38\,\text{A}^2\text{s}$) is a non-repetitive test rating. Under sustained reverse connection from an uncoordinated source, D14 experiences catastrophic thermal runaway and destruction within seconds ($P_D = 5\text{A} \times 0.75\text{V} = 3.75\text{W}$, exceeding package dissipation by $> 2.5\times$).
- **Retraction of Speculative Claims:** Previous claims asserting guaranteed clearing in "1–5 ms", guaranteed fault containment within "8.3 ms", generic arcing energy multipliers (1.5× to 2.5×), and guaranteed protection by uncoordinated power supply foldback (< 50 ms) are formally retracted as unverified engineering assumptions.
- **Mandatory Installation Requirements:**
  - Because `D14` is connected directly across connector `J1` upstream of internal board fuses F1, F2, and F3, an external clearing device is mandatory.
  - **Datasheet Truth Across Three Evaluated Littelfuse 5A Fast-Acting Fuses:**
    1. **Littelfuse 0451005.MRL (NANO2 2410 SMT):** Interrupting rating **300A @ 32VDC**; nominal cold resistance $0.0125\,\Omega$; nominal melting $I^2t = \mathbf{5.566\,\text{A}^2\text{s}}$ at $10\times$ rated current ($50\text{A}$). Total clearing $I^2t$ is **NOT PUBLISHED** by Littelfuse.
    2. **Littelfuse 0217005.MXP ($5\times 20\,\text{mm}$ Glass Cartridge):** AC interrupting rating 50A @ 250VAC, but DC interrupting rating is limited to **70A @ 60VDC**; nominal melting $I^2t = \mathbf{42.795\,\text{A}^2\text{s}}$ at $10\times$ rated current ($50\text{A}$). Total clearing $I^2t$ is **NOT PUBLISHED** by Littelfuse. *Critical Limitation:* If prospective DC fault current exceeds 70A, this fuse cannot safely extinguish the DC arc.
    3. **Littelfuse 0216005.MXP ($5\times 20\,\text{mm}$ Ceramic Cartridge):** Interrupting rating 1500A @ 250VAC; nominal melting $I^2t = \mathbf{27.46\,\text{A}^2\text{s}}$ at $10\times$ rated current ($50\text{A}$). Total clearing $I^2t$ is **NOT PUBLISHED** by Littelfuse; **NO DC INTERRUPTING RATING PUBLISHED**. An AC breaking rating cannot be applied to DC systems.
  - **Fuse Coordination Assessment:** The nominal fuse melting $I^2t$ is lower than the calculated diode non-repetitive surge $I^2t$ equivalent ($5.566\,\text{A}^2\text{s} < 93.38\,\text{A}^2\text{s}$ for the 0451005.MRL), but this comparison does not establish protection coordination or prove diode survival. Maximum total-clearing $I^2t$ remains unpublished, and actual fault conditions are installation-dependent. Published time-current curves reflect pre-arcing opening time only, not guaranteed total-clearing time.
- **Fuse Coordination Assessment:** The nominal fuse melting $I^2t$ is lower than the calculated diode non-repetitive surge $I^2t$ equivalent ($5.566\,\text{A}^2\text{s} < 93.38\,\text{A}^2\text{s}$ for the 0451005.MRL), but this comparison does not establish protection coordination or prove diode survival. Maximum total-clearing $I^2t$ remains unpublished, and actual fault conditions are installation-dependent. Published time-current curves reflect pre-arcing opening time only, not guaranteed total-clearing time.
- **Prohibition of Cross-Model $I^2t$ Transfer:** Total clearing $I^2t$ or melting $I^2t$ cannot be transferred or assumed across different fuse constructions. Cartridge fuses have significantly higher melting $I^2t$ ($27.46\,\text{A}^2\text{s}$ and $42.795\,\text{A}^2\text{s}$) than the SMT NANO2 fuse ($5.566\,\text{A}^2\text{s}$), and their total let-through energy under DC fault conditions may approach or exceed D14's $93.38\,\text{A}^2\text{s}$ non-repetitive rating.
  - **Prospective Fault Current Reality:** Prospective short-circuit current is entirely dependent on the specific source impedance and installation wiring. A stiff 24V source or battery bank can deliver hundreds of amperes, requiring verified DC breaking ratings.
  - **Physical Mounting Options:** Because the Littelfuse 0451005.MRL is a surface-mount 2410 package, physical deployment requires:
    1. A DIN-rail or inline PCB modular carrier housing the Littelfuse 0451005.MRL 2410 SMT fuse, OR
    2. A standardized inline cable fuseholder housing a fast-acting cartridge fuse (**Littelfuse 0216005.MXP** ceramic or **Littelfuse 0217005.MXP** glass), which must be empirically qualified on the prototype bench due to higher $I^2t$ and DC breaking limitations.
  - **Prohibited Configurations:** Connecting MISACS to an uncoordinated bench power supply in constant-current mode (e.g. 5A CC limit) during reverse connection is strictly prohibited, as sustained conduction will destroy D14.
  - **Verification Matrix Classification:** Formally classified: **CONDITIONAL / NOT VERIFIED** (never unconditionally PASS).

### C. Actuator Current Operational Envelope
- **Infineon IPD50N06S4L-08 Datasheet Evidence (Table 3):**
  - $R_{thJC} = 2.1\,\text{K/W}$ (guaranteed maximum).
  - Minimal footprint $R_{thJA} = 62\,\text{K/W}$ ($0.43\,\text{cm}^2$ pad).
  - $6.0\,\text{cm}^2$ copper ($70\,\mu\text{m}$ on FR-4) $R_{thJA} = 40\,\text{K/W}$.
- **PCB Geometry & Thermal Via Extraction:**
  - MISACS provides $139.13\,\text{mm}^2$ ($1.39\,\text{cm}^2$) of 2-layer $35\,\mu\text{m}$ ($1\,\text{oz}$) copper per channel.
  - 4 thermal vias ($0.40\,\text{mm}$ drill, $0.80\,\text{mm}$ annular ring, via conductive resistance $33.1\,\text{K/W}$) per drain tab.
  - Logarithmic area interpolation: self-thermal resistance $\theta_{11} \approx 52.2\,\text{K/W}$ (modeled as $\theta_{11} = 52.0\,\text{K/W}$, bounded by $50.0 - 55.0\,\text{K/W}$).
- **Mutual Thermal Coupling Resistance ($\theta_{12}$):**
  - $\theta_{12} = \theta_{21} \approx 6.5\,\text{K/W}$ (bounds $5.0 - 7.5\,\text{K/W}$) across $50\,\text{mm}$ spacing.
  - **Classified as an Unvalidated Engineering Assumption** ($\approx 12.5\%$ cross-coupling heuristic).
- **Forced-Air Cooling Derivation ($> 1.0\,\text{m/s}$):**
  - Analytically estimated thermal resistances: $\theta_{11,forced} \approx 25.0\,\text{K/W}, \theta_{12,forced} \approx 2.5\,\text{K/W}$.
  - At dual 5.0A continuous ($P_1 = P_2 = 0.632\,\text{W}$): $T_j \approx 67.4^\circ\text{C}$ (analytical upper bound $78.0^\circ\text{C}$).
  - Analytical approximation based on convective theory; pending wind-tunnel / prototype testing.
- **Authoritative Thermal Envelopes ($T_{amb} \le 50.0^\circ\text{C}$, $R_{DS(on),hot} = 22.3\,\text{m}\Omega$):**
  - **Single Channel Continuous:** Up to **4.0A continuous** ($T_j \approx 71.7^\circ\text{C}$ nominal, $\le 72.9^\circ\text{C}$ upper bound; margin $102.1^\circ\text{C}$ below $175^\circ\text{C}$).
  - **Dual Channels Simultaneously Active:** **3.0A continuous per channel** ($6.0\text{A}$ total combined, $T_j \approx 64.4^\circ\text{C}$ nominal, $\le 65.4^\circ\text{C}$ upper bound; margin $109.6^\circ\text{C}$).
  - **Dual Asymmetrical Continuous:** **4.0A on CH1 and 2.0A on CH2** ($T_{j1} \approx 72.4^\circ\text{C}, T_{j2} \approx 58.9^\circ\text{C}$).
  - **Pulsed PWM Operation:** **5.0A per channel at up to 50% PWM duty cycle** (or pulse duration $< 10\text{s}$, $T_j \approx 68.5^\circ\text{C}$).
  - **Rating Designation:** Formally classified: **Estimated Design Envelopes — Pending Physical Thermal Qualification**.

### D. 5V Power Supply Continuous Output Limit
- **Architecture:** Although the LM2576HVS-5.0 IC features an internal 3.0A switch limit, the selected power inductor `L1` (Bourns SRR1260-101M) has rated saturation and RMS limits of $I_{rms} = 1.70\,\text{A}, I_{sat} = 1.70\,\text{A}$ ($25\%$ inductance roll-off, worst-case DCR $R_{L1} = 0.18\,\Omega$ / $180\,\text{m}\Omega$).
- **Inductor Ripple Derivation:** Under worst-case operating conditions ($V_{in,max} = 28\,\text{V}, V_{out} = 5.0\,\text{V}, f_{sw,min} = 47\,\text{kHz}, L_{min} = 80\,\mu\text{H}$), peak-to-peak inductor ripple is $\Delta I_L = 1.092\,\text{A}$.
- **Continuous Rating:** Sized for **1.15A continuous worst-case** ($1.32\text{A}$ nominal continuous) to prevent peak core saturation ($I_{sat} - \Delta I_L/2 = 1.70 - 0.546 = 1.154\,\text{A}$). This provides a **$3.83\times$ design margin** over onboard system demand ($0.298\,\text{A} \approx 0.30\,\text{A}$). Qualified simulation (TB2) with worst-case $0.18\,\Omega$ DCR yields steady-state mean of $4.993\,\text{V}$ and ripple of $67.59\,\text{mV}_{pp}$. External $+5\text{V}$ tapping must not exceed $0.85\,\text{A}$.

### E. AMS1117-3.3 Linear Regulator Stability Qualification
- **Datasheet Baseline:** AMS1117 datasheet states: $22\,\mu\text{F}$ solid tantalum recommended for all operating conditions; smaller capacitors may work under fixed-output conditions without adjust-pin bypass. Does not strictly mandate 10µF or 0.1–1.0Ω ESR tunnel.
- **Physical Implementation:** MISACS fits C4 ($10\,\mu\text{F}$ 0805 MLCC, 6.0mm from U2) and C10 ($10\,\mu\text{F}$ 1206 MLCC, 18.8mm from U2 across $18\,\text{m}\Omega, 16\,\text{nH}$ trace). Full peak load is $285.3\,\text{mA}$ ($0.485\,\text{W}$ load, $0.025\,\text{W}$ quiescent, $0.510\,\text{W}$ total), yielding $T_j \approx 83.15^\circ\text{C}$ at $50^\circ\text{C}$ ambient ($41.85^\circ\text{C}$ safety margin below $125^\circ\text{C}$).
- **DC-Bias Derating:** Murata MLCCs derate under 3.3V DC bias: C4 derates to $\approx 7.5-8.0\,\mu\text{F}$, C10 derates to $\approx 8.2-8.8\,\mu\text{F}$ (combined bulk capacitance $\approx 16.0\,\mu\text{F}$).
- **TB3 Series Trace Simulation:** Models physical series connection of $R_{trace}$ ($18\,\text{m}\Omega$) and $L_{trace}$ ($16\,\text{nH}$), yielding an exact DC trace drop of $\mathbf{5.14\,\text{mV}}$ ($5.135\,\text{mV}$) at $285.3\,\text{mA}$.
- **Stability Status:** MLCC ESR is $< 15\,\text{m}\Omega$, below the recommended tantalum window. Formally classified: **Plausible under static conditions, but unverified and potentially marginal under dynamic Wi-Fi pulsed loads — awaiting physical prototype testing; hardware correction option identified.**
- **Hardware Mitigation:** If prototype testing reveals transient ringing under Wi-Fi bursts, an EIA 3216-18 (Case A) solid tantalum capacitor ($10\,\mu\text{F}, 16\text{V}, ESR \approx 0.5\,\Omega$) can be hand-soldered onto C10 (`C_1206_3216Metric`) pads.

### F. Intentional No-Connect Pins
- **Physical Endpoint Accounting:**
  - `U4.2` (ADS1115 Pin 2 ALERT/RDY): Open-drain alert flag, intentionally NC when using standard I2C polling.
  - `U5.14` (ESP32 Pin 14 IO12 / MTDI): Strapping pin, intentionally NC to prevent pull-up and ensure standard 3.3V flash boot.
  - `U8.7` (TPS26610 Pin 7 VSNS): Voltage sense cutoff input, intentionally NC per TI datasheet for standard current-limit mode.
  - `U8.8` (TPS26610 Pin 8 SGOOD): Power-good flag, intentionally NC; loop health acquired via 16-bit ADC.
  - Total: 192 connected endpoints + 4 intentional no-connect endpoints = 196 physical pin endpoints ($0$ discrepancies).

### G. ADS1115 Analog Input Rail Clamping Protection Limitations (TB6)
- **Circuit Configuration:** Dual Schottky diode rail clamps (`D3`, `D4`, Diodes Inc. BAT54S) with upstream $R_7 = 1.0\,\text{k}\Omega \pm 1\%$ series resistor.
- **Datasheet Tolerances vs Absolute Maximum Stress Limits:**
  - ADS1115 absolute maximum limits are $-0.30\,\text{V} \le V_{AIN} \le V_{DD} + 0.30\,\text{V}$ (with $V_{DD} = 3.30\,\text{V}$, maximum allowable pin voltage is $-0.30\,\text{V}$ to $+3.60\,\text{V}$). Absolute maximum ratings are stress ratings; operating beyond them causes junction stress and can corrupt conversions even when continuous current is limited below $\pm 10\,\text{mA}$.
  - BAT54S guaranteed maximum forward voltage is specified **only at $25^\circ\text{C}$**: $V_F \le 0.32\,\text{V}$ at $1\,\text{mA}$ and $0.40\,\text{V}$ at $10\,\text{mA}$. Guaranteed sub-zero ratings are unpublished; typical curve extrapolations show $V_F \approx 0.45 - 0.50\,\text{V}$ at $-40^\circ\text{C}$.
  - Under cold temperature operation, the external Schottky forward drop exceeds $0.30\,\text{V}$, yielding a negative voltage margin ($\le 0\,\text{V}$) relative to ADS1115 absolute maximum limits and forcing internal ESD structures to share current.
  - Silicon survival is assured because $R_7 = 1.0\,\text{k}\Omega$ restricts fault current to $< 6.5\,\text{mA}$ under $-5\,\text{V}$ to $+10\,\text{V}$ fault conditions (below the continuous $\pm 10\,\text{mA}$ limit).
- **Rail Sinking Dynamics & Deep-Sleep Overvoltage Hazard:**
  - Clamping positive overvoltages dumps fault current ($I_{inject} = 6.41\,\text{mA}$ at $+10\,\text{V}$) into the $+3.3\,\text{V}$ rail.
  - The AMS1117-3.3 linear regulator is a source-only device and cannot sink current from its output.
  - While active MCU load ($80-240\,\text{mA}$) easily absorbs this current during run mode, an MCU in deep sleep ($< 100\,\mu\text{A}$) leaves the injected current unabsorbed, charging rail capacitance ($15.8\,\mu\text{F}$) with a first-order initial slope estimate of $dV/dt \approx 405\,\text{V/s}$ (analytical estimate, not a transient simulation or destruction guarantee; dynamic model and bench validation required).
- **Hardware Correction Evaluation & Unqualified Candidates:**
  - Generic clamp diodes are unviable: MMSZ5227B is not guaranteed to remain below the 3.60 V maximum at its upper tolerance limit (3.78 V), SMAJ3.3A does not conduct at 3.60 V (breakdown begins at 4.10–4.70 V), and no evaluated candidate has been qualified as a suitable solution.
  - The proposed 4.7 kΩ $R_7$ option (which reduces fault current from 6.41 mA to 1.36 mA) remains a proposed future hardware change, not an implemented PCB modification. Any revised protection network requires additional electrical analysis and physical testing.
- **Verification Matrix Classification:**
  - **Simulation Execution Status:** **PASS** (Nominal room-temperature simulation satisfies defined numerical limits).
  - **Engineering Qualification Status:** **CONDITIONAL / NOT VERIFIED** (Cold temperature negative margin, deep-sleep rail rising hazard, and absence of a qualified rail clamp require physical prototype bench testing; proposed circuit modifications reserved for future hardware revision).
