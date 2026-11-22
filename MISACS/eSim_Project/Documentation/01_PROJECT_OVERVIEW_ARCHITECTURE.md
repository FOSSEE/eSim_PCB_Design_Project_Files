# MISACS Phase 3 — Final Engineering and Submission Preparation — Project Overview and System Architecture
**Project:** Modular Industrial Sensor Acquisition and Control System (MISACS)  
**Program:** FOSSEE eSim Winter Internship 2026 — Task 7  
**EDA Environment:** eSim 2.5 + KiCad 6.0.11  
**Revision:** Phase 3 — Final Engineering and Submission Preparation  
**Status:** Engineering Release Candidate — Pending Physical Prototype Validation  

---

## 1. Executive Summary
The Modular Industrial Sensor Acquisition and Control System (MISACS) is a mixed-signal edge acquisition and control system designed for industrial telemetry, sensor conditioning, and actuator control. Running on an Espressif ESP32-WROOM-32E-N16 32-bit dual-core microcontroller (240 MHz, 16MB Flash), MISACS integrates dual analog front ends (4–20 mA current loop and 0–10 V voltage), a multi-drop RS-485 serial communication interface, and dual low-side power MOSFET actuator drivers onto a 2-layer FR-4 printed circuit board (nominal 100.00 mm x 80.00 mm routed centerline; 100.15 mm x 80.15 mm outer graphic stroke extents).

## 2. Subsystem Architecture & Parity Reconciliation
The physical board contains 70 electronic components plus 4 mechanical mounting holes (H1–H4), encompassing exactly **196 physical component pin endpoints**:
- **192 matched connected physical endpoints**
- **4 intentional no-connect physical endpoints** (U4.2 ALERT/RDY, U5.14 IO12/MTDI, U8.7 VSNS, U8.8 SGOOD)
- **0 electrical discrepancies**

### Subsystem Breakdown:

1. **Primary Power Entry & Reverse Protection:**
   - Connector `J1` ($+24\text{V DC}$ primary power) is fitted with `D14` (Vishay SS56 5A Schottky diode) configured in anti-parallel across J1 as a reverse-polarity shunt protection diode.
   - In simulation (TB1), under a static DC sweep with an assumed source resistance of $R_{src} = 0.5\,\Omega$, reversed input voltages are clamped to $-1.432\,\text{V}$ ($-0.75\,\text{V}$ static $V_F$ at 5A rated current).
   - **Diode Surge Capacity vs Continuous Destruction:** Vishay SS56 publishes a peak non-repetitive forward surge rating of $I_{FSM} = 150\,\text{A}$ ($8.3\,\text{ms}$ single half-sine wave, JEDEC method), corresponding to an energy integral of $I^2t = \frac{1}{2} (150)^2 (0.0083) \approx 93.38\,\text{A}^2\text{s}$. **Crucially, this is a non-repetitive surge rating and does NOT represent a guaranteed continuous destruction limit or continuous reverse-shunt rating.**
   - Under sustained reverse connection from an uncoordinated source (such as a 5A bench power supply in constant-current mode), D14 dissipates continuous power ($P_D = 5\text{A} \times 0.75\text{V} = 3.75\text{W}$). Given the SMC package thermal resistance of $R_{\theta JA} \approx 55-75\,\text{K/W}$, continuous dissipation causes internal junction temperature to rapidly exceed $250^\circ\text{C}$, resulting in catastrophic thermal destruction within seconds. Safe clearing strictly requires a coordinated upstream fast-clearing fuse.
   - **Retraction of Speculative Claims:** Previous claims asserting guaranteed clearing in "1–5 ms", guaranteed fault containment within "8.3 ms", generic arcing energy multipliers (1.5× to 2.5×), and guaranteed protection by uncoordinated power supply foldback (< 50 ms) are formally retracted as unverified engineering assumptions.
   - **Manufacturer Datasheet Evidence on Evaluated Fuses:**
     - **Littelfuse 0451005.MRL (451 Series NANO2® Very Fast-Acting 2410 SMT):**
       Rated Current: $5.0\,\text{A}$; Voltage Rating: $125\,\text{V AC/DC}$; Interrupting Rating: $50\,\text{A}$ @ $125\,\text{V AC/DC}$, $300\,\text{A}$ @ $32\,\text{V DC}$; Nominal Cold Resistance: $0.0125\,\Omega$; Nominal Melting $I^2t = \mathbf{5.566\,\text{A}^2\text{s}}$ (tested at $10\times$ rated current, $50\,\text{A}$); Total-Clearing $I^2t$: **NOT PUBLISHED** by Littelfuse in the datasheet.
     - **Littelfuse 0217005.MXP (217 Series $5\times 20\,\text{mm}$ Fast-Acting Glass Cartridge):**
       Rated Current: $5.0\,\text{A}$; Voltage Rating: $250\,\text{V AC}$; Interrupting Rating: $50\,\text{A}$ @ $250\,\text{V AC}$, **70A @ 60VDC**; Nominal Cold Resistance: $0.0137\,\Omega$; Nominal Melting $I^2t = \mathbf{42.795\,\text{A}^2\text{s}}$ (tested at $10\times$ rated current); Total-Clearing $I^2t$: **NOT PUBLISHED**. If prospective DC fault current exceeds 70A, this fuse cannot safely clear.
     - **Littelfuse 0216005.MXP (216 Series $5\times 20\,\text{mm}$ Fast-Acting Ceramic High-Breaking Cartridge):**
       Rated Current: $5.0\,\text{A}$; Voltage Rating: $250\,\text{V AC}$; Interrupting Rating: $1500\,\text{A}$ @ $250\,\text{V AC}$; Nominal Cold Resistance: $0.0183\,\Omega$; Nominal Melting $I^2t = \mathbf{27.46\,\text{A}^2\text{s}}$; Total-Clearing $I^2t$: **NOT PUBLISHED**; **NO DC INTERRUPTING RATING PUBLISHED** (AC interrupting ratings cannot be transferred to DC circuits).
   - **Critical Engineering Directives:**
     1. Never treat nominal melting $I^2t$ as maximum total-clearing $I^2t$. The nominal fuse melting $I^2t$ is lower than the calculated diode non-repetitive surge $I^2t$ equivalent, but this comparison does not establish protection coordination or prove diode survival. Maximum total-clearing $I^2t$ remains unpublished, and actual fault conditions are installation-dependent. Manufacturer time-current curves reflect pre-arcing opening time only, not guaranteed total-clearing time.
     2. Never transfer an $I^2t$ value between different fuse models. The 217 series ($42.8\,\text{A}^2\text{s}$) has an $I^2t$ nearly $8\times$ higher than the 451 series ($5.57\,\text{A}^2\text{s}$). If a 217 series fuse is used, total clearing energy could easily encroach upon or exceed the $93.38\,\text{A}^2\text{s}$ non-repetitive surge rating of D14.
     3. Prospective fault current is strongly source-dependent. Low-impedance sources (lead-acid batteries, industrial DIN-rail supplies) can deliver hundreds of amperes, requiring verified DC breaking ratings.
     4. Because total-clearing $I^2t$ is not published by the manufacturer and clearing time depends on external loop impedance, fuse coordination cannot be unconditionally guaranteed across arbitrary field installations.
   - **Physical Installation Requirements:** Because the Littelfuse 0451005.MRL is a surface-mount 2410 package, physical deployment strictly requires an external inline DIN-rail modular carrier PCB housing the 2410 SMT fuse upstream of J1. Standard uncoordinated constant-current bench supplies are strictly prohibited. - **Simulation Execution Status:** **PASS** (Static DC sweep verifies nominal $-1.432\,\text{V}$ reverse shunt diode clamp and $+44.02\,\text{V}$ TVS clamp).
   - **Engineering Qualification Status:** **CONDITIONAL / NOT VERIFIED** (TB1 verifies static protection behaviour under its stated model, but does not prove dynamic reverse-polarity fuse coordination. D14 survival under actual installation fault conditions remains unverified due to unpublished total-clearing $I^2t$ and source impedance dependencies).

2. **Logic Rail Protection:**
   - Downstream of connector J1, the logic power path is isolated by a 1.1A resettable PTC fuse (`F1`), Littelfuse SMBJ30A unidirectional TVS clamp (`D1`), and Vishay SS36 series Schottky blocking diode (`D2`).
   - The logic rail is 100% unconditionally protected against reverse supply voltages ($V_{prot} = -0.0000\,\text{V}$). Overvoltage clamping prevents transients up to $+50\,\text{V}$ from exceeding $43.56\,\text{V}$, maintaining a $15.98\,\text{V}$ safety margin below the $60\,\text{V}$ absolute maximum rating of the LM2576 buck converter. Status: **PASS**.

3. **Step-Down Buck Power Converter:**
   - Texas Instruments LM2576HVS-5.0 switching regulator with Vishay SS56 catch diode (`D12`) and Bourns SRR1260-101M $100\,\mu\text{H}$ shielded power inductor (`L1`, $I_{rms}=1.70\,\text{A}, I_{sat}=1.70\,\text{A}$, maximum DCR $R_{L1} = 0.18\,\Omega$ / $180\,\text{m}\Omega$).
   - Accounting for worst-case inductor current ripple ($\Delta I_L = 1.092\,\text{A}$ at $V_{in}=28\,\text{V}, V_{out}=5\,\text{V}, f_{sw}=47\,\text{kHz}, L=80\,\mu\text{H}$), the continuous output current rating is **1.15A continuous worst-case** ($1.32\,\text{A}$ nominal continuous), providing a $\mathbf{3.83\times}$ design margin over the actual $0.298\,\text{A} \approx 0.30\,\text{A}$ onboard system demand.
   - Simulation (TB2, open-loop macro with $0.18\,\Omega$ DCR) verifies a steady-state mean output of $\mathbf{4.993\,\text{V}}$ with $\mathbf{67.59\,\text{mV}_{p-p}}$ ripple ($1.5\,\text{ms} \le t \le 2.0\,\text{ms}$). Status: **PASS**.

4. **Secondary Linear LDO Regulator:**
   - Advanced Monolithic Systems AMS1117-3.3 linear regulator providing low-noise $+3.3\,\text{V}$ power to the ESP32, ADS1115, and MAX3485.
   - Full peak load is $285.3\,\text{mA}$ (Load $P_D = 0.4850\,\text{W}$, Quiescent $P_Q = 0.0250\,\text{W}$, Total $P_{tot} = 0.510\,\text{W}$), operating with an estimated junction temperature of $T_j = 83.15^\circ\text{C}$ at $50^\circ\text{C}$ ambient ($41.85^\circ\text{C}$ margin below $125^\circ\text{C}$ maximum rating at $R_{\theta JA} = 65\,\text{K/W}$).
   - TB3 models the physical series trace network ($R_{trace} = 18\,\text{m}\Omega$, $L_{trace} = 16\,\text{nH}$), producing an exact DC trace drop of $\mathbf{5.14\,\text{mV}}$ at $285.3\,\text{mA}$.
   - Stability status: Datasheet recommends $22\,\mu\text{F}$ solid tantalum for all operating conditions; MLCC derating under DC bias derates C4 to $\approx 7.5-8.0\,\mu\text{F}$ and C10 to $\approx 8.2-8.8\,\mu\text{F}$. Stability is formally classified as **plausible under static conditions, but unverified and potentially marginal under dynamic Wi-Fi pulsed loads — awaiting physical prototype testing; hardware correction option identified** (bench rework allows soldering a Case A tantalum onto C10). Status: **NOT VERIFIED**.

5. **4–20 mA Current Loop Receiver:**
   - Susumu $100.0\,\Omega$ ($0.1\%$, $25\,\text{ppm}$) precision shunt resistor, TI TPS26610DDFR active eFuse loop limiter (SOT-23-THIN DDF-8), and TI LMV358 rail-to-rail operational buffer ($0.400\,\text{V}$ to $2.000\,\text{V}$ output).
   - Qualified simulation (TB4) enforces minimum sample count ($\ge 10$ points in operating span), validates mandatory calibration points (4mA, 12mA, 20mA), and verifies conventional linear regression $R^2_{reg} = 1.000000$ (slope $100.000\,\text{V/A}$, intercept $0.0000\,\text{V}$) and ideal transfer agreement metric $R^2_{ideal} = 1.000000$. Status: **PASS**.

6. **0–10 V Industrial Voltage Receiver:**
   - Precision $4:1$ attenuation divider ($30.0\,\text{k}\Omega / 10.0\,\text{k}\Omega$, $0.1\%$) and TI LMV358 operational buffer ($0.000\,\text{V}$ to $2.500\,\text{V}$ output).
   - Qualified simulation (TB5) verifies exact $4.000:1$ division across the $0-10\,\text{V}$ range ($2.500\,\text{V}$ output at $10\,\text{V}$) and strictly enforces mandatory over-range protection verification at $12.0\,\text{V}$ input ($3.0000\,\text{V}$ output, safe within the $3.3\,\text{V}$ ADC supply rail). Status: **PASS**.

7. **16-Bit Analog-to-Digital Converter & Input Protection (TB6):**
   - Texas Instruments ADS1115 delta-sigma ADC with programmable gain amplifier, I2C interface, and Diodes Inc. BAT54S dual Schottky rail clamp diodes (`D3`, `D4`) with $R_7 = 1.0\,\text{k}\Omega$ series current-limiting resistor.
   - **Simulation Execution Status:** **PASS** (Nominal room-temperature clamp $-0.281\,\text{V}$ and $+3.591\,\text{V}$ satisfy nominal boundary limits of the generic parameterized macro).
   - **Engineering Qualification Status:** **CONDITIONAL / NOT VERIFIED**.
   - **Model Fidelity:** Evaluated with a generic parameterized Schottky diode macro (`tb6_adc_protection.cir`) under static DC sweep with a fixed 3.30V rail. It is not a vendor-qualified worst-case BAT54S model and does not simulate dynamic rail rising.
   - **Reassessment & Worst-Case Evidence:**
     - **Temperature Sensitivity:** BAT54S datasheet guaranteed maximum forward voltage: $V_F \le 0.32\,\text{V}$ at $1\,\text{mA}$, $V_F \le 0.40\,\text{V}$ at $10\,\text{mA}$ at $25^\circ\text{C}$. Schottky forward voltage has a negative temperature coefficient ($\approx +1.8\,\text{mV/}^\circ\text{C}$ increase at cold temperatures), reaching $V_F \approx 0.45 - 0.50\,\text{V}$ at $-40^\circ\text{C}$ (based on typical curves, as guaranteed sub-zero limits are unpublished).
     - **ADS1115 Absolute Limits:** Absolute maximum ratings are $-0.30\,\text{V} \le V_{AIN} \le V_{DD} + 0.30\,\text{V}$, continuous input current $\pm 10\,\text{mA}$. These are absolute stress ratings; staying within current limits does not ensure normal operation if voltage ratings are exceeded.
     - **Cold-Temperature Negative Margin:** Under guaranteed worst-case datasheet limits or at low industrial temperatures, the external Schottky forward drop exceeds $0.30\,\text{V}$, causing partial conduction of ADS1115 internal ESD diodes. Because $R_7 = 1.0\,\text{k}\Omega$ limits fault current to $< 10\,\text{mA}$ under $-5\,\text{V}$ to $+10\,\text{V}$ faults, physical destruction is prevented, but voltage margin to the absolute maximum rating is negative ($\le 0\,\text{V}$).
     - **Supply Rail Rise & Deep-Sleep Hazard:** Clamping a positive fault dumps current into the $+3.3\,\text{V}$ rail ($I_{inject} = 6.41\,\text{mA}$ at $+10\,\text{V}$). The AMS1117-3.3 regulator cannot sink current. Active MCU load ($> 80\,\text{mA}$) easily absorbs this current during run mode. However, if the ESP32 is in deep sleep ($< 100\,\mu\text{A}$), the injected current charges the $+3.3\,\text{V}$ rail capacitance ($C_{eff} \approx 15.8\,\mu\text{F}$) at $dV/dt = \frac{I}{C} \approx \frac{6.41\,\text{mA}}{15.8\,\mu\text{F}} \approx 405\,\text{V/s}$, charging the $+3.3\,\text{V}$ rail with a first-order initial slope estimate of $\approx 405\,\text{V/s}$ (analytical estimate, not a transient simulation or destruction guarantee; dynamic model and bench validation required).
     - **Supply Corner & Tolerance Analysis:** Evaluating 3.3V supply corners ($\pm 2\%$, $3.234\,\text{V} - 3.366\,\text{V}$) and $R_7$ tolerance ($\pm 1\%$) confirms the need for system-level clamping.
   - **Hardware Correction Evaluation & Unqualified Candidates:**
     1. *Clamp Component Limitations:* Generic clamps cannot be treated as qualified remedies. The MMSZ5227B Zener tolerance band (3.42–3.78 V at 20 mA) cannot guarantee clamping below the 3.60 V absolute maximum limit, while the SMAJ3.3A TVS has a breakdown voltage of 4.10–4.70 V and does not conduct at 3.60 V. No evaluated candidate has been qualified as a suitable solution.
     2. *Proposed Resistor Increase:* Increasing series resistor $R_7$ from $1.0\,\text{k}\Omega$ to $4.7\,\text{k}\Omega$ (reducing injected fault current from 6.41 mA to 1.36 mA) remains a proposed future hardware change for subsequent prototype spins, not an implemented PCB modification. Any revised protection network requires additional electrical analysis and physical testing.

8. **Processing Core:**
   - Espressif ESP32-WROOM-32E-N16 module with 16MB SPI flash, hardware UART, I2C, PWM, and strapping pins verified. Clean power distribution with localized decoupling. Status: **PASS**.

9. **RS-485 Serial Transceiver:**
   - Maxim Integrated / ADI MAX3485EESA half-duplex transceiver. **Non-isolated design referenced to system ground.**
   - Includes switchable $120\,\Omega$ bus termination, $390\,\Omega$ failsafe bias network, and Littelfuse SM712 asymmetrical TVS surge protection.
   - Qualified simulation (TB10) confirms differential mark ($+1.150\,\text{V}$), space ($-0.951\,\text{V}$), and dynamic differential eye swing of $2.10\,\text{V}_{pp}$ ($> 1.5\,\text{V}$ standard). Status: **PASS**.

10. **Dual Low-Side Actuator Drivers:**
    - TI UCC27524 high-speed dual gate driver driving two Infineon IPD50N06S4L-08 $60\,\text{V}, 50\,\text{A}$ power MOSFETs in PG-TO252-3 package (KiCad footprint `TO-252-2`) with Vishay SS56 flyback clamp diodes (`D8`, `D10`).
    - **Thermal Specifications & Evidence:**
      - Infineon IPD50N06S4L-08 datasheet Table 3: $R_{thJC} = 2.1\,\text{K/W}$ (guaranteed maximum), $R_{thJA} = 62\,\text{K/W}$ on minimal footprint ($0.43\,\text{cm}^2$), and $R_{thJA} = 40\,\text{K/W}$ on $6.0\,\text{cm}^2$ cooling area ($70\,\mu\text{m}$ copper on $40\times 40\times 1.5\,\text{mm}$ epoxy PCB).
      - Board layout mapping: MISACS provides $139.13\,\text{mm}^2$ ($1.39\,\text{cm}^2$) of 2-layer $35\,\mu\text{m}$ ($1\,\text{oz}$) copper per channel with 4 thermal vias ($0.40\,\text{mm}$ drill, $0.80\,\text{mm}$ annular ring, via conductive resistance $33.1\,\text{K/W}$).
      - Logarithmic area interpolation yields self-thermal resistance $\theta_{11} = \theta_{22} \approx 52.2\,\text{K/W}$ (modeled as $\theta_{11} = 52.0\,\text{K/W}$, bounded by $50 - 55\,\text{K/W}$).
      - Mutual thermal resistance $\theta_{12} = \theta_{21} \approx 6.5\,\text{K/W}$ across $d \approx 50\,\text{mm}$ center-to-center spacing is an unvalidated engineering assumption ($\approx 12.5\%$ cross-coupling heuristic).
      - Forced-air convection ($>1.0\,\text{m/s}$): analytically estimated at $\theta_{11,forced} \approx 25\,\text{K/W}, \theta_{12,forced} \approx 2.5\,\text{K/W}$ based on convective coefficient doubling, yielding $T_j \approx 67.4^\circ\text{C}$ for dual 5A continuous, with a conservative analytical upper bound of $78.0^\circ\text{C}$ (analytical approximation, pending physical wind-tunnel validation).
      - Continuous operating envelopes:
        - Natural convection ($T_{amb} \le 50^\circ\text{C}$, $R_{DS(on),hot} = 22.3\,\text{m}\Omega$): **4.0A single channel continuous** ($T_j \approx 71.7^\circ\text{C}$) / **3.0A dual channel continuous** ($T_j \approx 64.4^\circ\text{C}$).
        - PWM duty cycle: **5.0A at up to 50% duty cycle** ($T_j \approx 68.5^\circ\text{C}$).
      - All thermal envelopes are formally designated **Estimated Design Envelopes — Pending Physical Thermal Qualification**. Status: **CONDITIONAL / NOT VERIFIED**.

---

## 3. Simulation Fidelity & Validation Classification

| Testbench | Circuit Subsystem | Model Fidelity Classification | Simulation Scope & Verification Limits | Verdict |
|:---:|:---|:---|:---|:---:|
| **TB1** | 24V Input Protection | Parametric Diode & TVS Static DC-Sweep Macro | Static DC sweep ($R_{src} = 0.5\,\Omega$). Verifies D2 reverse blocking, D14 static forward clamp ($-1.432\,\text{V}$ at 5A), and SMBJ30A breakdown. Does not model dynamic lightning/surge transients. | **PASS** |
| **TB2** | LM2576 Buck Converter | Open-Loop Buck Switching Macro | Behavioral pulse generator + physical LC filter ($100\,\mu\text{H}, 0.18\,\Omega$ DCR, $680\,\mu\text{F}$ ESR). Mean $4.993\,\text{V}$, ripple $67.59\,\text{mV}_{pp}$. Does not model LM2576 internal error amplifier compensation loop. | **PASS** |
| **TB3** | AMS1117-3.3 Linear LDO | Behavioural LDO Macro with Series Trace Parasitics | Behavioral regulation with distributed physical trace network ($18\,\text{m}\Omega, 16\,\text{nH}$). Verifies $5.14\,\text{mV}$ DC drop at $285.3\,\text{mA}$. Does not evaluate AC loop stability under dynamic pulsed RF load. | **PASS** |
| **TB4** | 4–20 mA Current Loop | Shunt Resistor & VCVS Ideal Op-Amp Macro | Ideal VCVS op-amp model. Confirms linear regression $R^2_{reg} = 1.000000$ (slope $100.000\,\text{V/A}$, intercept $0.0000\,\text{V}$) and ideal agreement $R^2_{ideal} = 1.000000$ from 4 to 20 mA ($0.400\,\text{V}$ to $2.000\,\text{V}$). Enforces minimum 10 sample count. Does not model op-amp offset drift or eFuse series drop. | **PASS** |
| **TB5** | 0–10 V Voltage Receiver | Divider & VCVS Ideal Op-Amp Macro | Ideal VCVS op-amp model. Confirms exact $4.000:1$ division across $0-10\,\text{V}$ range ($2.500\,\text{V}$) and mandatory $12\,\text{V}$ over-range check ($3.000\,\text{V} \le 3.3\,\text{V}$). Does not simulate op-amp common-mode input limits. | **PASS** |
| **TB6** | ADS1115 Rail Clamping | Parametric BAT54S Diode Macro | Parametric Schottky diode macro under nominal room-temperature conditions. Verifies clamping between $-0.281\,\text{V}$ and $+3.591\,\text{V}$ under $-5\,\text{V}$ and $+10\,\text{V}$ faults. Simulation execution PASS; engineering qualification CONDITIONAL / NOT VERIFIED due to cold-temperature negative margin and deep-sleep rail rising hazard. | **PASS (Sim) / CONDITIONAL (Qual)** |
| **TB7** | MOSFET Dynamic Switching | Generic Level 1 NMOS Switching Macro | Generic Level 1 NMOS model. Verifies gate drive transition ($4.99\,\text{V}$) and switching dynamics ($t_f = 12.5\,\text{ns}, t_r = 9.9\,\text{ns}$). Informational switching speed; does not reflect vendor-specific sub-threshold or gate charge curves. | **PASS** |
| **TB8** | Dual Actuator Driver | Simplified Dual Resistive-Load Switching Macro | Simplified dual resistive switching (CH1 4.0A / $6\,\Omega$, CH2 2.5A / $9.6\,\Omega$). Verifies on-state conduction ($V_{DS} \le 0.11\,\text{V}$). Does not claim crosstalk, shoot-through, or thermal coupling validation. | **PASS** |
| **TB9** | Inductive Turn-off Clamp | Simplified RL Inductive Turn-off Macro | Turn-off transient with $10\,\text{mH}$ inductor and SS56 flyback diode. Clamps drain voltage to $24.629\,\text{V}$ ($35.37\,\text{V}$ margin below $60\,\text{V}$ rating). Does not model parasitic trace inductance or diode reverse recovery. | **PASS** |
| **TB10** | RS-485 Transceiver | Behavioural Driver & Transmission Line Macro | Behavioral pulse transmitter across $120\,\Omega$ termination. Differential swing $2.10\,\text{V}_{pp}$ (mark $+1.150\,\text{V}$, space $-0.951\,\text{V}$). Does not model common-mode ground potential differences or transceiver driver impedance tolerances. | **PASS** |
