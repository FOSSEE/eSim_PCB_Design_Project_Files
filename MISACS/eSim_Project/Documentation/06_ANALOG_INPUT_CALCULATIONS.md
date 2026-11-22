# MISACS Phase 3 — Analog Input Conditioning & Protection Calculations
**Project:** Modular Industrial Sensor Acquisition and Control System (MISACS)  
**Program:** FOSSEE eSim Winter Internship 2026 — Task 7  
**Revision:** Phase 3 Final Review Release Candidate  
**Status:** Engineering Release Candidate — Pending Physical Prototype Validation  

---

## 1. 4–20 mA Current Loop Input Conditioning
- **Precision Shunt Resistor:** $R_{shunt} = 100.0\,\Omega$ ($0.1\%$ tolerance, $25\,\text{ppm/}^\circ\text{C}$, Susumu RR1220P-101-D).
- **Active Current Limiter:** TI TPS26610DDFR 50V active industrial eFuse loop limiter (SOT-23-THIN DDF-8) providing active reverse input protection and clamping.
- **Voltage Transfer Function:**
  $$V_{shunt} = I_{loop} \times 100.0\,\Omega$$
  - At $I_{loop} = 4.0\,\text{mA}$: $V_{shunt} = 0.004 \times 100 = 0.400\,\text{V}$
  - At $I_{loop} = 12.0\,\text{mA}$: $V_{shunt} = 0.012 \times 100 = 1.200\,\text{V}$
  - At $I_{loop} = 20.0\,\text{mA}$: $V_{shunt} = 0.020 \times 100 = 2.000\,\text{V}$
  - Overrange at $24.0\,\text{mA}$: $V_{shunt} = 0.024 \times 100 = 2.400\,\text{V}$
- **Shunt Power Dissipation at $20\,\text{mA}$:**
  $$P_{shunt} = I^2 R = (0.020)^2 \times 100 = 40.0\,\text{mW}$$
  Using a $250\,\text{mW}$ rated 0805 precision resistor yields a derating factor of $16.0\%$, ensuring negligible thermal drift.
- **Anti-Aliasing Filter:** $R_{filt} = 1.0\,\text{k}\Omega, C_{filt} = 100\,\text{nF}$. Cutoff frequency $f_c = \frac{1}{2\pi R C} = 1.59\,\text{kHz}$, eliminating industrial 50/60 Hz noise and high-frequency switching EMI.
- **Simulation Validation (TB4):**
  - Linear regression fit across 17 operating-range sample points (1 mA sweep step from 4.0 mA to 20.0 mA): $R^2_{reg} = 1.000000$ (slope $100.000\,\text{V/A}$, intercept $0.0000\,\text{V}$), well exceeding the mandatory minimum acceptance requirement of $\ge 10$ points.
  - Ideal transfer agreement metric: $R^2_{ideal} = 1.000000 \ge 0.999900$. Status: **PASS**.

---

## 2. 0–10 V Industrial Voltage Input Scaling
- **Resistive Divider Network:** $R_{top} = 30.0\,\text{k}\Omega, R_{bot} = 10.0\,\text{k}\Omega$ ($0.1\%$ precision, Ratio $K = 0.250$).
- **Buffer Amplifier:** TI LMV358IDR rail-to-rail operational amplifier configured as a unity-gain buffer.
- **Output Voltage:**
  $$V_{div} = V_{in} \times \frac{10.0\,\text{k}\Omega}{30.0\,\text{k}\Omega + 10.0\,\text{k}\Omega} = 0.250 \times V_{in}$$
  - $V_{in} = 0.0\,\text{V} \implies V_{div} = 0.000\,\text{V}$
  - $V_{in} = 5.0\,\text{V} \implies V_{div} = 1.250\,\text{V}$
  - $V_{in} = 10.0\,\text{V} \implies V_{div} = 2.500\,\text{V}$
  - Mandatory over-range check at $V_{in} = 12.0\,\text{V} \implies V_{div} = 3.000\,\text{V}$ (safe within the $3.3\,\text{V}$ ADC supply rail).
- **Divider Power Consumption at $10.0\,\text{V}$:**
  $$P_{div} = \frac{V^2}{R_{eq}} = \frac{100}{40,000} = 2.50\,\text{mW}$$
  Total input impedance is $40.0\,\text{k}\Omega$, presenting negligible loading to external process transmitters.
- **Simulation Validation (TB5):**
  - Confirms exact $4.000:1$ division across $0-10\,\text{V}$ and enforces mandatory $12\,\text{V}$ over-range check ($3.0000\,\text{V} \le 3.3\,\text{V}$). Status: **PASS**.

---

## 3. ADS1115 ADC Resolution and Dynamic Range
- **ADC Architecture:** 16-bit Delta-Sigma with internal PGA and precision voltage reference ($2.048\text{V} / 4.096\text{V}$).
- **Configured PGA Range:** $\pm 4.096\,\text{V}$ ($1\,\text{LSB} = 125\,\mu\text{V}$).
- **Single-Ended Resolution:**
  - 4–20 mA input ($0.400\text{V}$ to $2.000\text{V}$): $\Delta V = 1.600\text{V} \implies 12,800\text{ counts}$ ($\approx 13.6\text{ bits}$ effective resolution).
  - 0–10 V input ($0.000\text{V}$ to $2.500\text{V}$): $\Delta V = 2.500\text{V} \implies 20,000\text{ counts}$ ($\approx 14.3\text{ bits}$ effective resolution).

---

## 4. Analog Input Clamping Protection Analysis (TB6 / ADS1115)
- **Protection Network Components:**
  - Dual Schottky rail-clamp diodes: Diodes Inc. BAT54S (`D3`, `D4`, SOT-23) connected between analog input lines, $GND$, and $+3.3\,\text{V}$ rail.
  - Series input resistor: $R_7 = 1.0\,\text{k}\Omega$ ($0805, 0.125\,\text{W}, \pm 1\%$) placed upstream of the clamping node and ADC input pin.
- **Simulation Model Fidelity & Scope (TB6):**
  - **Model Architecture:** The SPICE netlist `tb6_adc_protection.cir` implements a **generic parameterized Schottky diode macro** (`.model D_BAT54S D(...)`) evaluated under a static DC voltage sweep with an ideal, fixed $+3.30\,\text{V}$ DC voltage rail.
  - **Limitations of Model:** This netlist is an illustrative DC macro under nominal $+25^\circ\text{C}$ room-temperature conditions. It is **not** a manufacturer-qualified worst-case BAT54S model, does not simulate sub-zero temperature curves, does not model ADS1115 internal ESD diode conduction structures, and does not simulate dynamic $+3.3\,\text{V}$ rail rising under low-power sleep modes.
- **Datasheet Specifications and Limitations:**
  - **Diodes Inc. BAT54S:**
    - Guaranteed maximum forward voltage is specified **only at $25^\circ\text{C}$**: $V_F \le 0.32\,\text{V}$ at $1\,\text{mA}$, $V_F \le 0.40\,\text{V}$ at $10\,\text{mA}$.
    - Guaranteed sub-zero forward voltage limits are **not published**. Typical manufacturer curves indicate a negative temperature coefficient of $\approx +1.8\,\text{mV/}^\circ\text{C}$, reaching typical $V_F \approx 0.45 - 0.50\,\text{V}$ at $-40^\circ\text{C}$.
  - **Texas Instruments ADS1115:**
    - Absolute Maximum Ratings: $-0.30\,\text{V} \le V_{AIN} \le V_{DD} + 0.30\,\text{V}$ (with $V_{DD} = 3.30\,\text{V}$, maximum allowable pin voltage is $-0.30\,\text{V}$ to $+3.60\,\text{V}$).
    - Maximum Continuous Input Current: $\pm 10.0\,\text{mA}$ through internal ESD diode structures.
    - *Critical Reliability Principle:* Absolute maximum ratings are stress limits. Exceeding $-0.30\,\text{V}$ or $V_{DD} + 0.30\,\text{V}$ stresses internal silicon junctions and can cause substrate injection, latch-up, or conversion corruption, even if current remains below $\pm 10\,\text{mA}$.
- **Fault Condition Evaluation:**
  1. **Nominal Room-Temperature Simulation (TB6):**
     - Negative fault ($-5.0\,\text{V}$ applied): Lower Schottky conducts with $I_{clamp,lower} = 4.72\,\text{mA}$, clamping $V_{AIN}$ to $\mathbf{-0.281\,\text{V}}$ (compliant with nominal $-0.30\,\text{V}$ limit; margin $+0.019\,\text{V}$).
     - Positive fault ($+10.0\,\text{V}$ applied): Upper Schottky conducts into $+3.3\,\text{V}$ rail with $I_{inject} = 6.41\,\text{mA}$, clamping $V_{AIN}$ to $\mathbf{+3.591\,\text{V}}$ (compliant with nominal $+3.60\,\text{V}$ limit; margin $+0.009\,\text{V}$).
  2. **Worst-Case Tolerance and Low-Temperature Assessment:**
     - Under manufacturing maximum $V_F$ limits or cold temperatures (down to $-40^\circ\text{C}$ where typical $V_F \approx 0.45\,\text{V}$), the external Schottky forward drop exceeds $0.30\,\text{V}$.
     - As a result, the internal ESD protection diodes of the ADS1115 share current with the external BAT54S.
     - **Voltage Margin:** Negative ($\le 0\,\text{V}$) relative to ADS1115 absolute maximum ratings under corner conditions.
     - **Current Limitation:** Series resistor $R_7 = 1.0\,\text{k}\Omega \pm 1\%$ limits maximum fault current:
       $$I_{fault,max} = \frac{|V_{fault} - V_{clamp}|}{R_{7,min}} = \frac{10.0\,\text{V} - 3.6\,\text{V}}{990\,\Omega} = \mathbf{6.47\,\text{mA}} < 10.0\,\text{mA}$$
       This current limit protects internal ESD structures from immediate fusing, but does not prevent out-of-spec voltage stress.
  3. **Supply Corner and Rail Current Injection Hazard:**
     - Evaluating 3.3V supply corners ($\pm 2\%$, $3.234\,\text{V} - 3.366\,\text{V}$) shows that at minimum supply ($3.234\,\text{V}$), the upper limit is $3.534\,\text{V}$, further eroding margin.
     - Clamping a positive fault injects $6.41\,\text{mA}$ directly into the $+3.3\,\text{V}$ rail.
     - The AMS1117-3.3 linear regulator is a source-only device and cannot sink reverse current from its output pin.
     - **Active Mode:** When the ESP32 is running actively ($80-240\,\text{mA}$), this $6.41\,\text{mA}$ is absorbed by active circuit demand without pulling up the supply rail.
     - **Deep Sleep Mode & First-Order Initial Slope Estimate:** When the ESP32 enters deep sleep ($< 100\,\mu\text{A}$ quiescent), total board load drops below $0.2\,\text{mA}$. The unabsorbed injected current ($I_{net} \approx 6.4\,\text{mA}$) flows directly into the rail decoupling capacitance ($C_{eff} \approx 15.8\,\mu\text{F}$ derated):
       $$\left.\frac{dV_{DD}}{dt}\right|_{t=0} = \frac{I_{net}}{C_{eff}} = \frac{6.4\times 10^{-3}\,\text{A}}{15.8\times 10^{-6}\,\text{F}} \approx \mathbf{405\,\text{V/s}}$$
       *Important Engineering Qualification:* This $405\,\text{V/s}$ figure is a **first-order initial-slope estimate** assuming constant current injection into pure lumped capacitance under deep-sleep load conditions. It is **not** a transient simulation output or a guaranteed destruction time. Actual rail voltage dynamics depend on non-linear diode characteristics, regulator behavior, board parasitics, and ESD structures, and strictly require dynamic modeling and physical laboratory bench validation.
- **Evaluation of Proposed Hardware Corrections & Candidate Clamps (Future Revision Proposal):**
  *(Note: The physical hardware is 100% frozen for this release candidate; the following analyses evaluate proposed modifications for subsequent revisions. No evaluated candidate has been qualified as a suitable solution, and the 4.7 kΩ R7 option remains a proposed future hardware change, not an implemented PCB modification. Any revised protection network requires additional electrical analysis and physical testing.)*

  1. **Evaluation of Candidate Clamping Components for $+3.3\,\text{V}$ Rail:**
     - **Candidate A: Diodes Inc. MMSZ5227B Zener Diode (Unqualified Candidate):**
       - Datasheet Rating: Nominal $V_Z = 3.6\,\text{V}$ at test current $I_{ZT} = 20\,\text{mA}$.
       - Published Manufacturing Tolerance: At $20\,\text{mA}$, $V_Z$ ranges from **$3.42\,\text{V}$ minimum to $3.78\,\text{V}$ maximum** ($\pm 5\%$).
       - *Protection Evaluation:* Because the upper tolerance boundary ($3.78\,\text{V}$) exceeds the ADS1115 and ESP32 absolute maximum supply limit of **$3.60\,\text{V}$**, the MMSZ5227B **cannot guarantee clamping below $3.60\,\text{V}$**. At its upper tolerance limit, the rail is permitted to rise to $3.78\,\text{V}$, violating the ADC absolute maximum stress limit.
       - *Knee Impedance & Current Sinking:* At fault current levels ($I_{inject} \approx 2-6\,\text{mA}$), dynamic impedance rises significantly ($Z_{ZT} \approx 24\,\Omega$ at 20 mA, but $Z_{ZK} \approx 1700\,\Omega$ near 0.25 mA knee), further softening clamping.
       - *Normal Rail Leakage:* At nominal $3.3\,\text{V}$, reverse leakage can reach hundreds of microamperes, adding undesirable battery/quiescent drain.
       - *Power Dissipation:* $P_D = 3.6\,\text{V} \times 6.41\,\text{mA} \approx 23.1\,\text{mW}$ (well within SOD-123 $500\,\text{mW}$ rating).
       - *Conclusion:* MMSZ5227B is an **unqualified candidate** and cannot be used as a guaranteed $3.6\,\text{V}$ clamp.
     - **Candidate B: Littelfuse SMAJ3.3A Unidirectional TVS Diode (Unsuitable Candidate):**
       - Datasheet Ratings: Reverse standoff voltage $V_{RWM} = 3.3\,\text{V}$; breakdown voltage $V_{BR} = \mathbf{4.10\,\text{V} - 4.70\,\text{V}}$ at $I_T = 10\,\text{mA}$; maximum clamping voltage $V_C = 7.3\,\text{V}$ at $54.8\,\text{A}$.
       - *Protection Evaluation:* Because conduction does not begin until $V_{BR} \ge 4.10\,\text{V}$, the SMAJ3.3A provides **zero protection at $3.60\,\text{V}$** (it does not conduct at all at 3.60 V). It is designed for high-energy transient suppression (ESD/surge), not precise DC rail overvoltage regulation.
       - *Conclusion:* SMAJ3.3A is **completely unsuitable** for clamping a 3.3V rail below 3.6V.
     - **Candidate C: Precision Active Shunt Clamp (Future Architectural Investigation):**
       - A precision active shunt architecture (e.g. TI TLV431 with $V_{ref} = 1.24\,\text{V} \pm 0.5\%$ driving an external PNP or PMOS shunt) configured to turn on sharply at $3.50\,\text{V} \pm 1.5\%$ ($3.45\,\text{V} - 3.55\,\text{V}$), sinking fault currents up to $50\,\text{mA}$ with $< 1\,\mu\text{A}$ normal leakage.
     - **Summary on Rail Clamping:** **No evaluated candidate component has been qualified as a suitable solution.** Simple passive Zeners or TVS diodes cannot bridge the tight $3.30\,\text{V}$ to $3.60\,\text{V}$ window.

  2. **Analysis of Proposed $R_7$ Increase ($1.0\,\text{k}\Omega \to 2.2\,\text{k}\Omega - 4.7\,\text{k}\Omega$):**
     Increasing $R_7$ directly reduces injected fault current, but impacts ADC input dynamics:
     - **Fault Current Reduction:**
       - At $R_7 = 1.0\,\text{k}\Omega$: $I_{fault} = \frac{10\,\text{V} - 3.6\,\text{V}}{1.0\,\text{k}\Omega} = \mathbf{6.40\,\text{mA}}$ (initial rail rise $\approx 405\,\text{V/s}$).
       - At $R_7 = 2.2\,\text{k}\Omega$: $I_{fault} = \frac{10\,\text{V} - 3.6\,\text{V}}{2.2\,\text{k}\Omega} = \mathbf{2.91\,\text{mA}}$ ($54.5\%$ reduction; initial rail rise $\approx 184\,\text{V/s}$).
       - At $R_7 = 4.7\,\text{k}\Omega$: $I_{fault} = \frac{10\,\text{V} - 3.6\,\text{V}}{4.7\,\text{k}\Omega} = \mathbf{1.36\,\text{mA}}$ ($78.8\%$ reduction; initial rail rise $\approx 86\,\text{V/s}$).
     - **ADS1115 Input Impedance and DC Gain Error:**
       - The ADS1115 features a switched-capacitor differential input stage with differential input impedance $R_{diff} = 6.0\,\text{M}\Omega$ (PGA = 1, $\pm 4.096\,\text{V}$) and common-mode impedance $R_{CM} = 100\,\text{M}\Omega$.
       - The series resistor forms a voltage divider with $R_{diff}$, introducing a systematic gain attenuation error:
         $$\text{Gain Error} = \frac{R_7}{R_{diff} + R_7}$$
         * At $R_7 = 1.0\,\text{k}\Omega$: $\text{Gain Error} = \frac{1.0\,\text{k}\Omega}{6001\,\text{k}\Omega} \approx 0.0167\% = 167\,\text{ppm}$ ($10.9\,\text{LSBs}$ at 16-bit resolution).
         * At $R_7 = 2.2\,\text{k}\Omega$: $\text{Gain Error} = \frac{2.2\,\text{k}\Omega}{6002.2\,\text{k}\Omega} \approx 0.0367\% = 367\,\text{ppm}$ ($24.0\,\text{LSBs}$).
         * At $R_7 = 4.7\,\text{k}\Omega$: $\text{Gain Error} = \frac{4.7\,\text{k}\Omega}{6004.7\,\text{k}\Omega} \approx 0.0783\% = 783\,\text{ppm}$ ($51.3\,\text{LSBs}$).
       - *Conclusion on DC Error:* The gain error increases from $11\,\text{LSB}$ to $51\,\text{LSB}$ at $4.7\,\text{k}\Omega$. While this is not negligible, it is linear and fully correctable in software firmware calibration.
     - **Input Filter Settling Time and Conversion Rate:**
       - Input RC low-pass filter with capacitor $C_{filt} = 10\,\text{nF}$:
         * At $R_7 = 1.0\,\text{k}\Omega$: $\tau = R_7 C_{filt} = 10\,\mu\text{s}$; cutoff frequency $f_c = \frac{1}{2\pi \tau} \approx 15.9\,\text{kHz}$.
         * At $R_7 = 2.2\,\text{k}\Omega$: $\tau = 22\,\mu\text{s}$; $f_c \approx 7.2\,\text{kHz}$.
         * At $R_7 = 4.7\,\text{k}\Omega$: $\tau = 47\,\mu\text{s}$; $f_c \approx 3.39\,\text{kHz}$.
       - At maximum ADS1115 sampling rate ($860\,\text{SPS}$, conversion time $T_{conv} = 1.163\,\text{ms}$):
         $$\frac{T_{conv}}{\tau_{4.7k}} = \frac{1163\,\mu\text{s}}{47\,\mu\text{s}} \approx \mathbf{24.7\text{ time constants}}$$
         Because settling to $0.5\,\text{LSB}$ at 16 bits requires $N = \ln(2^{16}) \approx 11.1$ time constants, $24.7\,\tau$ provides more than $2\times$ required settling margin, ensuring zero dynamic settling truncation error even at the maximum conversion speed of $860\,\text{SPS}$.
- **Formal Status Classification:**
  - **Simulation Execution Status:** **PASS** (Nominal room-temperature simulation satisfies defined numerical limits).
  - **Engineering Qualification Status:** **CONDITIONAL / NOT VERIFIED** (Negative voltage margin at low industrial temperatures and unverified deep-sleep rail-rising behavior require physical prototype testing; proposed circuit modifications reserved for future hardware revision).
