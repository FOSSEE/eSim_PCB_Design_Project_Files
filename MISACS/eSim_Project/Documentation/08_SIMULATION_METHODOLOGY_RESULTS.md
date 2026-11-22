# MISACS Phase 3 (Final Review Candidate) — Simulation Methodology and Complete Results
**Project:** Modular Industrial Sensor Acquisition and Control System (MISACS)  
**Program:** FOSSEE eSim Winter Internship 2026 — Task 7  
**Simulation Engine:** Ngspice 35 (FOSSEE eSim integrated simulation suite)  
**Execution Date:** November 2026  
**Revision:** Phase 3 Final Review Candidate  
**Suite Status:** 10/10 Testbenches Qualified & Passing (Execution: 10 PASS; Qualification: 8 PASS, 2 CONDITIONAL / NOT VERIFIED)  

---

## 1. Simulation Methodology & Verification Standard
To rigorously validate circuit dynamics without modifying the production hardware design, 10 separate standalone SPICE netlists were authored under `Simulation/`. Each testbench models realistic circuit elements, parasitic components, and operational boundaries.

All 10 testbenches execute non-destructively via `run_simulations.py`, generating both raw output tabular data and standalone vector SVG plots in `Simulation/` and `Evidence/`. All test runs are tracked with persistent logs in `Evidence/Simulation_Logs/` and cataloged in `Simulation/SIMULATION_RUN_MANIFEST.json`.

The simulation runner implements strict tabular data parsing and mathematical boundary validation:
- Rejects malformed rows, missing or extra columns, non-numeric strings, and non-finite values (`NaN`, `Inf`).
- Enforces mandatory measurement points for all testbenches.
- Calculates both conventional linear regression metrics ($R^2_{reg}$, slope, intercept) and ideal agreement metrics ($R^2_{ideal}$) for TB4.
- Validates over-range fault protection for TB5 ($12.0\,\text{V}$ input yielding $3.0000\,\text{V}$, safe below $3.3\,\text{V}$ ADC rail).
- Evaluates nodal clamp and rail-injected currents in TB6 ($I_{clamp,lower} = 4.72\,\text{mA}, I_{inject} = 6.41\,\text{mA}$) and distinguishes simulation execution status (**PASS**) from engineering qualification status (**CONDITIONAL / NOT VERIFIED**).
- Generates structured two-part logs distinguishing the raw Ngspice simulator transcript from the wrapper audit validation summary.
- Records SHA-256 cryptographic hashes of every input netlist, raw output, plot vector, and log file in `SIMULATION_RUN_MANIFEST.json`.

---

## 2. Testbench Summary Matrix & Model Fidelity

| ID | Testbench | Circuit Architecture & Model Fidelity | Quantitative Simulation Result | Simulation Status | Qualification Status |
|---|---|---|---|:---:|:---:|
| **TB1** | 24V Input & Protection | **Parametric Diode & TVS Static DC-Sweep Macro**<br>*Static DC sweep ($R_{src} = 0.5\,\Omega$); models reverse blocking of D2, forward clamp of D14 reverse-polarity shunt diode, and breakdown of SMBJ30A. Does not simulate dynamic high-energy lightning/surge transients.* | Blocked: $V_{prot} = -0.0000\,\text{V}$ ($V_{in}=-24\text{V}, V_{entry}=-1.432\text{V}$)<br>Nominal: $V_{prot} = 23.253\,\text{V}$ ($V_{in}=+24\text{V}, V_{entry}=23.758\text{V}$)<br>Clamped: $V_{fused} = 44.020\,\text{V}, V_{prot} = 43.558\,\text{V}$ ($V_{in}=+50\text{V}$, Margin to 60V LM2576: $15.98\,\text{V}$) | **PASS** | **CONDITIONAL / NOT VERIFIED** (D14 continuous survival dependent on upstream fuse) |
| **TB2** | LM2576 Buck Step-Down | **Open-Loop Switched Inductor Power Stage**<br>*Open-loop 52kHz pulse switch with Bourns SRR1260-101M ($100\,\mu\text{H}, 1.70\text{A}$ sat, $180\,\text{m}\Omega$ worst-case DCR) and SS56 catch diode macro. Does not model closed-loop LM2576 error amplifier dynamics, loop compensation, or line/load step transient response.* | Steady-state window $1.5\,\text{ms} \le t \le 2.0\,\text{ms}$:<br>Mean: **$4.993\,\text{V}$** (specification window: $4.90 - 5.10\,\text{V}$)<br>Peak-to-Peak Ripple: **$67.59\,\text{mV}_{pp}$** (specification limit: $\le 100\,\text{mV}_{pp}$) | **PASS** | **PASS** |
| **TB3** | AMS1117-3.3 Distributed Network | **Behavioural LDO Macro with Series Distributed PCB Trace Network**<br>*Behavioural dropout voltage macro with physical series $R_{trace}$ ($18\,\text{m}\Omega$) and $L_{trace}$ ($16\,\text{nH}$), C4 local MLCC ($8.0\,\mu\text{F}$ derated), and C10 bulk MLCC ($8.5\,\mu\text{F}$ derated) at $285.3\,\text{mA}$ peak load. Evaluates DC dropout transfer and DC trace drop ($5.14\,\text{mV}$); does not establish AC loop stability, phase margin, or dynamic Wi-Fi pulsed load stability.* | Dropout corner: $V_{in} = 3.5\,\text{V} \implies V_{out} = 2.386\,\text{V}$<br>Nominal operation: $V_{in} = 5.0\,\text{V} \implies V_{out(local)} = 3.2857\,\text{V}, V_{out(mcu)} = 3.2806\,\text{V}$<br>Series Trace Drop: **$5.14\,\text{mV}$** ($5.135\,\text{mV}$, limit $4.5 - 5.8\,\text{mV}$) | **PASS** | **NOT VERIFIED** (Dynamic RF load loop stability requires bench testing) |
| **TB4** | 4–20 mA Signal Conditioning | **Ideal Resistive Shunt with Behavioural VCVS Buffer**<br>*Precision $100.0\,\Omega$ ($0.1\%$) shunt resistor with behavioural voltage-controlled voltage source (VCVS) clipping buffer ($0-5\text{V}$). Models DC transfer linearity; does not simulate physical LMV358 op-amp silicon parasitics, input offset voltage, bias currents, or slew-rate limitations.* | $I_{in} = 4\,\text{mA} \implies 0.4000\,\text{V}$<br>$I_{in} = 12\,\text{mA} \implies 1.2000\,\text{V}$<br>$I_{in} = 20\,\text{mA} \implies 2.0000\,\text{V}$<br>Linear Regression: **$R^2_{reg} = 1.000000$**, Slope = **$100.000\,\text{V/A}$**, Intercept = **$0.00000\,\text{V}$**<br>Ideal Agreement Metric: **$R^2_{ideal} = 1.000000$** (spec $\ge 0.9999$) | **PASS** | **PASS** |
| **TB5** | 0–10 V Signal Conditioning | **Precision Resistive Divider (4:1) with Behavioural VCVS Buffer**<br>*Precision 4:1 attenuation divider ($30.0\,\text{k}\Omega / 10.0\,\text{k}\Omega$, $0.1\%$) with behavioural VCVS clipping buffer. Models nominal DC division and extended fault range; does not simulate physical LMV358 op-amp silicon parasitics.* | Normal $0-10\,\text{V}$ Span: $0\text{V} \to 0.0000\,\text{V}$, $5\text{V} \to 1.2500\,\text{V}$, $10\text{V} \to 2.5000\,\text{V}$ (exact 4.000:1 division)<br>Extended Over-Range Fault: $V_{in} = 12.0\,\text{V} \implies V_{out} = 3.0000\,\text{V}$ ($\le 3.3\,\text{V}$ ADC absolute rail) | **PASS** | **PASS** |
| **TB6** | ADS1115 Input Clamping | **Dual Schottky Rail Clamp Network**<br>*Diodes Inc. BAT54S dual Schottky series pair and $1.0\,\text{k}\Omega$ series current-limiting resistor to ADS1115 analog input. Models static DC overvoltage/undervoltage fault clamping under nominal room-temperature conditions. Simulation status PASS; engineering qualification CONDITIONAL / NOT VERIFIED due to cold-temperature negative margin and deep-sleep rail rising hazard.* | Negative Fault: $-5.0\,\text{V} \implies$ Clamped to **$-0.281\,\text{V}$** ($I_{clamp,lower} = 4.72\,\text{mA}$)<br>Positive Fault: $+10.0\,\text{V} \implies$ Clamped to **$+3.591\,\text{V}$** ($I_{inject} = 6.41\,\text{mA}$)<br>Full sweep range bounds: $-0.30\,\text{V} \le V_{pin} \le +3.60\,\text{V}$ (Nominal 25°C)<br>Injected rail current requires active MCU sinking or external clamp | **PASS** | **CONDITIONAL / NOT VERIFIED** (Cold temp $V_F \approx 0.45\text{V} > 0.30\text{V}$; deep-sleep rail rise $405\text{V/s}$) |
| **TB7** | UCC27524 Gate Driver | **Generic Level 1 NMOS Model Dynamic Switching**<br>*Ideal pulse source driving Level 1 NMOS model ($V_{TO}=2.0\text{V}, K_P=20.0, C_{iss}=3.68\text{nF}$) through $10\,\Omega$ gate resistor at 20kHz. Models qualitative switching transitions and gate voltage plateau; does not substitute for manufacturer subcircuit model of Infineon IPD50N06S4L-08.* | Gate Drive: $V_{gate,max} = 4.99\,\text{V}$ ($\ge 4.80\,\text{V}$)<br>Drain Switching: $V_{drain,on} = 0.136\,\text{V}$, $V_{drain,off} = 24.09\,\text{V}$<br>Switching Dynamics: $t_f = 12.5\,\text{ns}$ (acceptance $5-30\,\text{ns}$), $t_r = 9.9\,\text{ns}$ (acceptance $5-30\,\text{ns}$)<br>*(Informational switching speed metric based on generic Level 1 NMOS)* | **PASS** | **PASS** |
| **TB8** | Dual Actuator Switching | **Simplified Dual Resistive-Load Switching Simulation**<br>*Simultaneous asynchronous switching of CH1 ($4.0\,\text{A}$ resistive load) and CH2 ($2.5\,\text{A}$ resistive load) with Level 1 NMOS models. Models independent static load switching; does not simulate physical inter-channel crosstalk, ground bounce, or shoot-through.* | CH1 (4.0A load): On = $0.110\,\text{V}$, Off = $24.00\,\text{V}$<br>CH2 (2.5A load): On = $0.069\,\text{V}$, Off = $24.00\,\text{V}$<br>Scope: Simplified dual resistive-load test; does not claim crosstalk, shoot-through, or thermal coupling validation | **PASS** | **PASS** |
| **TB9** | Inductive Flyback Clamping | **Inductive Energy Dump with SS56 Schottky Clamp**<br>*$10\,\text{mH}$ inductive load carrying 5.0A interrupted abruptly; models SS56 diode forward conduction and magnetic energy recirculation. Does not simulate cable transmission-line reflections or high-frequency diode reverse-recovery ringing.* | Clamped Peak Drain Voltage: **$24.629\,\text{V}$** (acceptance limit: $24.50 - 25.00\,\text{V}$)<br>Safety Margin: **$35.37\,\text{V}$** below $60\,\text{V}$ MOSFET breakdown rating | **PASS** | **PASS** |
| **TB10**| RS-485 Bus Signaling | **RS-485 Differential Bus Signaling with Ideal Pulse Stimulus, 390R Bias, and 60R Termination**<br>*Ideal pulse source stimulus into dual $120\,\Omega$ termination ($60\,\Omega$ equivalent load) with $390\,\Omega$ fail-safe pull-up and pull-down bias network. Models differential bus voltage swing and passive bias levels; does not model physical MAX3485E transceiver driver output impedance, slew-rate control, or common-mode rejection.* | Mark Level ($V_A - V_B$): **$+1.150\,\text{V}$** ($\ge +0.80\,\text{V}$)<br>Space Level ($V_A - V_B$): **$-0.951\,\text{V}$** ($\le -0.80\,\text{V}$)<br>Dynamic Differential Eye Swing: **$2.10\,\text{V}_{pp}$** ($\ge 1.80\,\text{V}_{pp}$ acceptance, $> 1.5\,\text{V}$ standard) | **PASS** | **PASS** |

---

## 3. Mathematical Formulation of Linearity and Agreement Metrics (TB4)
To avoid ambiguity between conventional empirical regression and ideal model conformity, TB4 computes two mathematically distinct metrics across the 4–20 mA operating span ($N = 17$ samples at $1\,\text{mA}$ steps):

1. **Conventional Least-Squares Linear Regression ($R^2_{reg}$):**
   Evaluates the degree to which measured voltage points follow an empirical best-fit straight line:
   $$\hat{V}_i = \text{slope} \cdot I_{in,i} + \text{intercept}$$
   $$SS_{reg\_res} = \sum_{i=1}^N \left(V_{meas,i} - \hat{V}_i\right)^2, \quad SS_{reg\_tot} = \sum_{i=1}^N \left(V_{meas,i} - \bar{V}_{meas}\right)^2$$
   $$R^2_{reg} = 1 - \frac{SS_{reg\_res}}{SS_{reg\_tot}}$$
   *Simulated Result:* $\text{Slope} = 100.000\,\text{V/A}$, $\text{Intercept} = 0.00000\,\text{V}$, $R^2_{reg} = \mathbf{1.000000}$.

2. **Ideal Transfer Agreement Metric ($R^2_{ideal}$):**
   Evaluates the direct point-by-point adherence to the theoretically ideal transfer function ($V_{ideal,i} = 100.0 \cdot I_{in,i}$):
   $$SS_{ideal\_res} = \sum_{i=1}^N \left(V_{meas,i} - V_{ideal,i}\right)^2, \quad SS_{ideal\_tot} = \sum_{i=1}^N \left(V_{ideal,i} - \bar{V}_{ideal}\right)^2$$
   $$R^2_{ideal} = 1 - \frac{SS_{ideal\_res}}{SS_{ideal\_tot}}$$
   where $\bar{V}_{ideal} = 1.2000\,\text{V}$ and $SS_{ideal\_tot} = 4.080000\,\text{V}^2$.
   *Simulated Result:* $SS_{ideal\_res} = 0.000000\,\text{V}^2$, $R^2_{ideal} = \mathbf{1.000000}$ (acceptance specification: $\ge 0.9999$).
   *Negative Testing Verification (Cases 1 & 9):*
   - **Case 1:** Step size changed to 2mA (`.dc Iloop 0m 25m 2m`), generating 13 total rows, but exactly 9 operating interval samples in [4mA, 20mA] (4, 6, 8, 10, 12, 14, 16, 18, 20 mA), strictly failing the sample count criterion (>= 10).
   - **Case 9:** An offset of $+0.015\,\text{V}$ (+15mV) is injected into the TB4 buffer output ($V = 100\cdot I + 0.015\,\text{V}$ across 17 samples). Residual sum of squares evaluates to $SS_{ideal\_res} = 17\times (0.015)^2 = 0.003825\,\text{V}^2$, with $SS_{ideal\_tot} = 4.080000\,\text{V}^2$, yielding $R^2_{ideal} = 1 - (0.003825/4.08) = \mathbf{0.999063} < 0.999900$. The testbench specifically verifies that the ideal agreement acceptance check triggers `FAIL: Ideal agreement metric R^2(ideal)=0.999063 below specification (target >= 0.9999)` rather than accepting generic calibration deviation alone. In addition, the standalone `compute_ideal_agreement` helper function was verified against 3 controlled synthetic datasets (pure ideal $R^2 = 1.000000$, +15mV perturbed $R^2 = 0.999063$, and +4.95mV sub-5mV offset $R^2 = 0.999898$).

---

## 4. Engineering Qualification Analysis of TB6 (ADS1115 & BAT54S)
TB6 demonstrates a critical distinction between simulation execution compliance and hardware engineering qualification:

- **Model Fidelity:** The SPICE netlist `tb6_adc_protection.cir` is a **generic parameterized Schottky diode macro** evaluated under static DC sweep with an ideal, fixed 3.30V rail. It is not a manufacturer-qualified worst-case BAT54S model and does not simulate dynamic rail rising.

- **Simulation Execution: PASS.** In the SPICE environment under nominal room temperature ($25^\circ\text{C}$), the BAT54S model clamps a $-5.0\,\text{V}$ fault to $-0.281\,\text{V}$ and a $+10.0\,\text{V}$ fault to $+3.591\,\text{V}$, both within the nominal absolute maximum window ($-0.30\,\text{V}$ to $+3.60\,\text{V}$).
- **Engineering Qualification: CONDITIONAL / NOT VERIFIED.**
  1. *Sub-Zero Temperature Operation:* At low ambient temperatures (e.g. $-40^\circ\text{C}$), Schottky forward voltage rises to $\approx 0.45 - 0.50\,\text{V}$ (typical curve behavior). This exceeds the ADS1115 limit of $0.30\,\text{V}$, forcing internal ESD diodes to conduct. While $R_7 = 1.0\,\text{k}\Omega$ limits fault current to $< 10\,\text{mA}$, voltage margin is negative ($\le 0\,\text{V}$).
  2. *Deep-Sleep Supply Rail Rising:* Clamping a $+10.0\,\text{V}$ fault injects $I_{inject} = 6.41\,\text{mA}$ into the $+3.3\,\text{V}$ rail. The AMS1117 linear regulator cannot sink current. When the ESP32 is running actively ($80-240\,\text{mA}$), this current is safely absorbed. However, if the MCU enters deep sleep ($< 100\,\mu\text{A}$), unabsorbed injected current charges the rail decoupling capacitance ($15.8\,\mu\text{F}$) with a first-order initial slope estimate of $\left.\frac{dV_{DD}}{dt}\right|_{t=0} = \frac{6.41\,\text{mA}}{15.8\,\mu\text{F}} \approx 405\,\text{V/s}$ (analytical estimate, not a transient simulation or destruction guarantee; dynamic model and bench validation required).
  3. *Hardware Protection Evaluation:* Generic clamps are unviable: MMSZ5227B cannot guarantee clamping below 3.60 V at its 3.78 V upper limit, and SMAJ3.3A (breakdown 4.10–4.70 V) does not conduct at 3.60 V. No evaluated candidate has been qualified as a suitable solution. Increasing $R_7$ to $4.7\,\text{k}\Omega$ remains a proposed future hardware change (not an implemented PCB modification), and any revised network requires additional electrical analysis and physical testing.

---

## 5. Persistent Artifacts & Cryptographic Tracking
- **Simulation Execution Logs:** Stored in `Evidence/Simulation_Logs/{tb_id}_execution.log`. Each log clearly delineates:
  1. `RAW NGSPICE SIMULATOR TRANSCRIPT` (direct simulator execution output)
  2. `WRAPPER AUDIT VALIDATION SUMMARY` (testbench metrics, quantitative checks, and cryptographic file hashes)
- **Run Manifest:** JSON manifest with timestamps, input files, checksums, and execution times stored in `Simulation/SIMULATION_RUN_MANIFEST.json`. Tracks SHA-256 digests of:
  - Source `.cir` netlists
  - Raw tabular output `.txt` files
  - Rendered vector `.svg` plots
  - Execution log `.log` files
- **Vector Plots:** Visual plots for all 10 testbenches generated as clean SVGs in `Simulation/` and `Evidence/`.
- **Simulation Execution Logs:** Stored in `Evidence/Simulation_Logs/{tb_id}_execution.log`. Each log clearly delineates:
  1. `RAW NGSPICE SIMULATOR TRANSCRIPT` (direct simulator execution output)
  2. `WRAPPER AUDIT VALIDATION SUMMARY` (testbench metrics, quantitative checks, and cryptographic file hashes)
- **Run Manifest:** JSON manifest with timestamps, input files, checksums, and execution times stored in `Simulation/SIMULATION_RUN_MANIFEST.json`. Tracks SHA-256 digests of:
  - Source `.cir` netlists
  - Raw tabular output `.txt` files
  - Rendered vector `.svg` plots
  - Execution log `.log` files
- **Vector Plots:** Visual plots for all 10 testbenches generated as clean SVGs in `Simulation/` and `Evidence/`.
