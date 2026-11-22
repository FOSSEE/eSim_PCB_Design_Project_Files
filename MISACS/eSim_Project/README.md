# Modular Industrial Sensor Acquisition and Control System (MISACS)
## FOSSEE eSim Winter Internship 2026 — Task 7 Master Release Candidate (Phase 3 Final Review Candidate)

**Project Title:** Modular Industrial Sensor Acquisition and Control System (MISACS)  
**EDA Suite:** eSim 2.5 (FOSSEE, IIT Bombay) + KiCad 6.0.11  
**Target Hardware:** Industrial Mixed-Signal Edge Controller  
**Release Date:** November 2026  
**Revision:** Phase 3 Final Review Candidate  
**Status:** Engineering Release Candidate — Pending Physical Prototype Validation  

---

## 1. Project Directory Structure

```text
eSim_Project/
├── MISACS.proj                 # Canonical eSim 2.5 Project Anchor (schematicFile MISACS.kicad_sch)
├── MISACS.kicad_sch            # Canonical Schematic (0 Native ERC Errors, 74 lib_symbol_issues warnings)
├── MISACS.kicad_pcb            # Canonical 2-Layer PCB (0 DRC Violations, 0 Unconnected Pads)
├── MISACS.kicad_pro            # KiCad 6 Project Settings & Design Rules
├── sym-lib-table               # Local Symbol Library Table
├── fp-lib-table                # Local Footprint Library Table
├── README.md                   # Master project README and instruction guide
├── run_simulations.py          # Portable, Non-Destructive 10-Testbench Hardened Simulation Runner
├── MISACS_PHASE3_RELEASE_MANIFEST_SHA256.txt # Cryptographic SHA-256 release manifest
├── BOM/                        # Bill of Materials
│   ├── MISACS_BOM.csv          # Structured CSV BOM (70 Circuit Components + 4 Mounting Holes)
│   └── MISACS_BOM.md           # Formatted Markdown BOM with MPNs, Footprints, and Sourcing
├── Gerber/                     # Manufacturing RS-274X Gerbers and Excellon Drill Files
│   ├── MISACS-F_Cu.gbr         # Top Copper Layer
│   ├── MISACS-B_Cu.gbr         # Bottom Copper Layer & Solid GND Plane
│   ├── MISACS-F_Mask.gbr       # Top Solder Mask
│   ├── MISACS-B_Mask.gbr       # Bottom Solder Mask
│   ├── MISACS-F_SilkS.gbr      # Top Silkscreen Legend
│   ├── MISACS-B_SilkS.gbr      # Bottom Silkscreen
│   ├── MISACS-F_Paste.gbr      # Top Solder Paste (Stencil)
│   ├── MISACS-B_Paste.gbr      # Bottom Solder Paste
│   ├── MISACS-Edge_Cuts.gbr    # Board Outline (100.00 mm x 80.00 mm nom. centerline, 100.15 x 80.15 mm stroke)
│   ├── MISACS-PTH.drl          # Plated Through-Hole Drill File
│   └── MISACS-NPTH.drl         # Non-Plated Through-Hole Drill File (M3 Mounting Holes)
├── Reports/                    # Official Engineering Audit Reports
│   ├── PHASE3_6_BASELINE_MANIFEST.txt
│   ├── MISACS_PHASE3_6_ERC.rpt # Native KiCad 6.0.11 ERC Report (0 Errors, 74 Warnings)
│   ├── MISACS_PHASE3_6_DRC.rpt # Native KiCad 6.0.11 DRC Report (0 Violations, 0 Unconnected)
│   ├── SCHEMATIC_PCB_NETLIST_PARITY_REPORT.txt # 192 Connected + 4 NC Endpoints = 196 Total
│   ├── MECHANICAL_MANUFACTURING_REPORT.txt
│   ├── GERBER_DRILL_MANIFEST.txt
│   ├── FINAL_AUDIT_VERIFICATION_TABLE.md
│   └── MISACS_PHASE3_RELEASE_MANIFEST_SHA256.txt
├── Simulation/                 # 10 Functional Ngspice Testbenches & Netlists
│   ├── SIMULATION_REPORT.md    # Complete Simulation Verification Document
│   ├── SIMULATION_RUN_MANIFEST.json # Automated execution tracking and cryptographic manifest
│   ├── run_simulations.py      # Hardened simulation runner (synchronized copy)
│   ├── tb1_input_protection.cir & tb1_plot.svg (24V TVS Clamp & D14 Reverse Shunt Diode)
│   ├── tb2_lm2576_buck.cir & tb2_plot.svg (24V -> 5V Buck Regulator 52kHz)
│   ├── tb3_ams1117.cir & tb3_plot.svg (5V -> 3.3V LDO Series Distributed Ceramic Network)
│   ├── tb4_current_loop.cir & tb4_plot.svg (4-20mA 100R Shunt & Buffer)
│   ├── tb5_voltage_input.cir & tb5_plot.svg (0-10V 4:1 Divider & Buffer)
│   ├── tb6_adc_protection.cir & tb6_plot.svg (ADS1115 BAT54S Rail Clamp)
│   ├── tb7_gate_drive.cir & tb7_plot.svg (UCC27524 Gate Driver & NMOS)
│   ├── tb8_dual_actuators.cir & tb8_plot.svg (Dual Actuators 4A / 2.5A)
│   ├── tb9_flyback_clamp.cir & tb9_plot.svg (10mH Inductive Flyback Clamp)
│   └── tb10_rs485_bus.cir & tb10_plot.svg (RS-485 Differential Bus Signaling)
├── Negative_Testing/           # Automated Verification of Runner Error Traps
│   ├── README.md               # Negative testing documentation and execution guide
│   ├── test_negative_cases.py  # Standalone suite verifying 9 error trapping cases
│   └── NEGATIVE_TEST_REPORT.json # Sanitized machine-readable negative test report
├── Documentation/              # 13 Exhaustive Technical Engineering Documents
│   ├── 01_PROJECT_OVERVIEW_ARCHITECTURE.md
│   ├── 02_FUNCTIONAL_BLOCK_DIAGRAM.md
│   ├── 03_SCHEMATIC_DOCUMENTATION.md
│   ├── 04_PCB_LAYER_ROUTING_EXPLANATION.md
│   ├── 05_POWER_PROTECTION_CALCULATIONS.md
│   ├── 06_ANALOG_INPUT_CALCULATIONS.md
│   ├── 07_THERMAL_CURRENT_CARRYING_ANALYSIS.md
│   ├── 08_SIMULATION_METHODOLOGY_RESULTS.md
│   ├── 09_ERC_REPORT.md
│   ├── 10_DRC_REPORT.md
│   ├── 11_GERBER_EXCELLON_VALIDATION.md
│   ├── 12_KNOWN_LIMITATIONS_ASSUMPTIONS.md
│   ├── 13_ASSEMBLY_CONNECTOR_PINOUT.md
│   └── FINAL_AUDIT_VERIFICATION_TABLE.md
└── Evidence/                   # Visual Verification Artifacts, Logs & Vector Renders
    ├── Simulation_Logs/        # Persistent Execution Logs for TB1-TB10
    │   ├── TB1_execution.log through TB10_execution.log
    ├── MISACS-MISACS_PCB_Board_Outline_Edge_Cuts.svg
    ├── MISACS-MISACS_PCB_Bottom_Layer_B_Cu.svg
    ├── MISACS-MISACS_PCB_Bottom_Silkscreen_B_SilkS.svg
    ├── MISACS-MISACS_PCB_Top_Layer_F_Cu.svg
    ├── MISACS-MISACS_PCB_Top_Silkscreen_F_SilkS.svg
    ├── MISACS-MISACS_PCB_Top_Solder_Mask_F_Mask.svg
    ├── MISACS_NATIVE_ERC_RESULTS.txt
    ├── MISACS_NATIVE_DRC_RESULTS.txt
    ├── SCHEMATIC_PCB_PARITY_RESULTS.txt
    ├── MECHANICAL_MANUFACTURING_RESULTS.txt
    ├── GERBER_DRILL_MANIFEST.txt
    ├── FINAL_PROJECT_DIRECTORY_LISTING.txt
    └── tb1_plot.svg through tb10_plot.svg
```

---

## 2. Key Engineering Specifications & Reconciled Boundaries

1. **Power Supply & Protection:**
   - **Main 24V Input (J1):** Protected by Littelfuse SMBJ30A unidirectional TVS ($V_{RWM} = 30.0\,\text{V}, V_{BR} = 34.5\,\text{V}$, simulated clamp $44.020\,\text{V} < 60.0\,\text{V}$), series Schottky diode D2 (SS36) on logic rail ($V_{prot} = -0.0000\,\text{V}$), and shunt Schottky diode D14 (SS56) across J1 entry terminals as a reverse-polarity shunt diode (clamped to $-1.432\,\text{V}$ under a static DC sweep with $0.5\,\Omega$ source resistance; $-0.75\,\text{V}$ static $V_F$ at 5A).
   - **Mandatory Installation & Fuse Coordination Notice:**
     - D14 non-repetitive surge rating is $I_{FSM} = 150\,\text{A}$ ($8.3\,\text{ms}$ single half-sine wave, energy integral $I^2t \approx 93.38\,\text{A}^2\text{s}$). Under sustained reverse connection from an uncoordinated source (such as a 5A current-limited bench supply), D14 dissipates $>3.75\,\text{W}$ continuously and will suffer thermal destruction within seconds.
     - Upstream protection requires careful fuse selection. Manufacturer datasheet ratings for candidate 5A Littelfuse parts show significant differences:
       * **0451005.MRL (SMT 2410 fast-acting):** DC interrupting rating of **300A @ 32VDC**; nominal melting $I^2t = 5.566\,\text{A}^2\text{s}$; total clearing $I^2t$ unpublished.
       * **0217005.MXP ($5\times 20\,\text{mm}$ glass):** AC rating 50A @ 250VAC, but DC interrupting rating is limited to **70A @ 60VDC**; melting $I^2t = 42.795\,\text{A}^2\text{s}$; total clearing $I^2t$ unpublished. If prospective DC fault current exceeds 70A, this fuse cannot safely extinguish the arc.
       * **0216005.MXP ($5\times 20\,\text{mm}$ ceramic):** AC rating 1500A @ 250VAC; **NO DC interrupting rating published** (an AC breaking rating cannot be applied to DC circuits).
     - The nominal fuse melting $I^2t$ is lower than the calculated diode non-repetitive surge $I^2t$ equivalent ($5.566\,\text{A}^2\text{s} < 93.38\,\text{A}^2\text{s}$), but this comparison does not establish protection coordination or prove diode survival. Maximum total-clearing $I^2t$ remains unpublished, and actual fault conditions are installation-dependent. Manufacturer time-current curves reflect pre-arcing opening time only, not guaranteed total-clearing time. Prospective clearing current cannot be claimed as "1–5 ms" without a verified source model. Generic arcing multipliers and foldback assumptions are formally retracted.
     - D14 Reverse Shunt Diode Status: **CONDITIONAL / NOT VERIFIED** (requires physical prototype qualification and strict source coordination).
   - **5V Buck Converter:** LM2576HVS-5.0 with Bourns SRR1260-101M ($100\,\mu\text{H}$, $1.70\,\text{A} I_{rms} / 1.70\,\text{A} I_{sat}$, worst-case DCR $R_{L1} = 0.18\,\Omega$, $\Delta I_L = 1.092\,\text{A}$). Sized for **1.15A continuous worst-case (1.32A nominal continuous)**, providing a $3.83\times$ safety margin over actual onboard system demand ($0.298\,\text{A} \approx 0.30\,\text{A}$). Qualified simulation (TB2) with worst-case $0.18\,\Omega$ DCR yields steady-state mean of $4.993\,\text{V}$ and ripple of $67.59\,\text{mV}_{p-p}$ ($1.5-2.0\,\text{ms}$).
   - **3.3V Linear Regulator:** AMS1117-3.3 delivering $285.3\,\text{mA}$ peak ($0.485\,\text{W}$ load, $0.025\,\text{W}$ quiescent, $0.510\,\text{W}$ total), operating with an estimated $T_j = 83.15^\circ\text{C}$ at $50^\circ\text{C}$ ambient ($41.85^\circ\text{C}$ margin below $125^\circ\text{C}$). TB3 verifies physical series trace parasitics ($18\,\text{m}\Omega, 16\,\text{nH}$), producing an exact DC trace drop of $\mathbf{5.14\,\text{mV}}$ ($5.135\,\text{mV}$). Stability status: **Plausible under static conditions, but unverified and potentially marginal under dynamic Wi-Fi pulsed loads — awaiting physical prototype testing; hardware correction option identified** (C10 pads accommodate hand-soldering of EIA Case A tantalum capacitor for bench validation).

2. **Analog Front Ends:**
   - **4–20 mA Current Loop:** Susumu $100.0\,\Omega$ ($0.1\%$, $25\,\text{ppm}$) precision shunt, TI TPS26610DDFR active eFuse loop limiter (SOT-23-THIN / DDF-8, footprint SOT-23-8), and TI LMV358 buffer ($0.400\,\text{V}$ to $2.000\,\text{V}$). Pin 7 (VSNS) and Pin 8 (SGOOD) intentionally unconnected (NC). TB4 confirms linear regression $R^2_{reg} = 1.000000$ (slope $100.000\,\text{V/A}$, intercept $0.0000\,\text{V}$) and ideal transfer agreement $R^2_{ideal} = 1.000000$ (with $SS_{ideal\_tot} = \sum (V_{ideal,i} - \bar{V}_{ideal})^2$).
   - **0–10 V Voltage Input:** Precision $4:1$ divider ($30.0\,\text{k}\Omega / 10.0\,\text{k}\Omega$, $0.1\%$) and TI LMV358 buffer ($0.000\,\text{V}$ to $2.500\,\text{V}$). TB5 verifies exact 4.000:1 division across $0-10\,\text{V}$ and over-range safety at $12.0\,\text{V}$ ($3.0000\,\text{V} \le 3.3\,\text{V}$).
   - **ADC Protection (TB6):** Diodes Inc. BAT54S dual Schottky rail clamps and TI ADS1115 16-bit delta-sigma ADC. Pin 2 (ALERT/RDY) intentionally NC.
     * **Simulation Execution Status:** **PASS** (Nominal room-temperature clamp $-0.281\,\text{V}$ and $+3.591\,\text{V}$ satisfy nominal boundary limits).
     * **Engineering Qualification Status:** **CONDITIONAL / NOT VERIFIED**.
     * **Engineering Rationale:**
       1. At cold ambient temperatures (e.g. $-40^\circ\text{C}$), BAT54S forward voltage rises to $\approx 0.45\,\text{V}$ (typical curve reading, as guaranteed limits are specified only at $25^\circ\text{C}$). This exceeds the ADS1115 absolute maximum rating ($\text{GND}-0.30\,\text{V}$ / $V_{DD}+0.30\,\text{V}$), resulting in negative voltage margin and forcing internal ESD protection diodes to conduct.
       2. During a $+10\,\text{V}$ overvoltage fault, $6.41\,\text{mA}$ is injected into the $+3.3\,\text{V}$ rail through the upper clamp. The AMS1117 linear regulator cannot sink current. When the MCU is operating in active mode ($80-240\,\text{mA}$), this current is safely absorbed. However, if the MCU enters deep sleep ($<100\,\mu\text{A}$), the injected current charges the rail capacitance ($16\,\mu\text{F}$) with a first-order initial slope estimate of $dV/dt \approx 405\,\text{V/s}$ (analytical estimate, not a transient simulation or destruction guarantee; dynamic model and bench validation required).
     * **Hardware Correction Evaluation:** Generic clamp diodes are unviable: MMSZ5227B is not guaranteed to remain below the 3.60 V maximum at its upper tolerance limit (3.78 V), SMAJ3.3A does not conduct at 3.60 V (breakdown 4.10–4.70 V), and no evaluated candidate has been qualified as a suitable solution. The proposed 4.7 kΩ R7 option remains a proposed future hardware change (not an implemented PCB modification), and any revised protection network requires additional electrical analysis and physical testing.

3. **Digital Core & Industrial Communication:**
   - **MCU:** Espressif ESP32-WROOM-32E-N16 (240 MHz dual-core, 16MB SPI Flash). Pin 14 (IO12 / MTDI) intentionally NC to ensure standard 3.3V flash boot.
   - **RS-485 Transceiver:** Maxim / ADI MAX3485EESA half-duplex transceiver. **Non-isolated design referenced to system ground.** Includes switchable $120\,\Omega$ bus termination, $390\,\Omega$ failsafe bias network, and Littelfuse SM712 asymmetrical TVS diode. TB10 confirms $2.10\,\text{V}_{pp}$ differential swing (mark $+1.150\,\text{V}$, space $-0.951\,\text{V}$).

4. **Dual Power Actuator Drivers:**
   - **Driver & Switches:** TI UCC27524 high-speed dual gate driver driving two Infineon IPD50N06S4L-08 $60\,\text{V}, 50\,\text{A}$ power MOSFETs in PG-TO252-3 package (KiCad footprint `TO-252-2`) with Vishay SS56 flyback clamp diodes (D8, D10). PCB features $42.90\,\text{mm}^2$ drain pads with **4 dedicated thermal stitching vias** ($0.40\,\text{mm}$ drill, $0.80\,\text{mm}$ annular ring) and $139.13\,\text{mm}^2$ total connected copper per channel.
   - **Thermal Matrix Formulation ($\theta_{11} = 52.0\,\text{K/W}, \theta_{12} = 6.5\,\text{K/W}$, $T_{amb} \le 50^\circ\text{C}$):**
     - Single Channel Continuous: Up to **4.0A continuous** ($T_j \approx 71.7^\circ\text{C}$ nominal, $\le 72.9^\circ\text{C}$ upper bound).
     - Dual Channels Simultaneously Active: **3.0A continuous per channel** ($6.0\,\text{A}$ combined, $T_j \approx 64.4^\circ\text{C}$ nominal, $\le 65.4^\circ\text{C}$ upper bound), or asymmetrical (e.g. 4.0A CH1 / 2.0A CH2, $T_{j1} \approx 72.4^\circ\text{C}$).
     - Pulsed Operation: **5.0A per channel at up to 50% PWM duty cycle** ($< 10\,\text{s}$ duration, $T_j \approx 68.5^\circ\text{C}$).
     - Forced-Air Cooling ($> 1\,\text{m/s}$): Up to **5.0A continuous per channel** ($T_j \approx 67.4^\circ\text{C}$, analytical upper bound $78.0^\circ\text{C}$).
     - Classification: **Estimated Design Envelopes — Pending Physical Thermal Qualification**.

5. **Physical Pin Endpoint Accounting:**
   - **192 Matched Connected Endpoints**
   - **4 Intentional No-Connect Endpoints** (U4.2 ALERT, U5.14 IO12, U8.7 VSNS, U8.8 SGOOD)
   - **196 Total Physical Component Pads / Nodes** across all 70 components
   - **0 Electrical Discrepancies**

---

## 3. How to Run Simulations
The simulation suite can be executed from the project root or the `Simulation/` directory:
```bash
python run_simulations.py
```
This performs:
- Automatic Ngspice binary location and environment hardening (Windows 8.3 short-path resolution, HOME trailing slash handling).
- Non-destructive execution in an isolated scratch directory without touching source `.cir` netlists.
- Strict tabular parsing rejecting malformed tokens, wrong column counts, and non-finite values (`NaN`, `Inf`).
- Mandatory measurement point validation across all 10 testbenches.
- Distinction between Simulation Execution Status (**PASS**) and Engineering Qualification Status (**CONDITIONAL / NOT VERIFIED** for TB6).
- Generation of standalone SVG plots, structured execution logs in `Evidence/Simulation_Logs/`, and cryptographic tracking in `Simulation/SIMULATION_RUN_MANIFEST.json`.

---

## 4. How to Run Automated Negative Testing
The automated error-trapping and boundary-enforcement negative testing suite can be executed from the project root or `Negative_Testing/`:
```bash
python Negative_Testing/test_negative_cases.py
```
This non-destructively verifies 9 controlled failure scenarios:
1. Insufficient TB4 regression sample count (2mA step generating exactly 9 operating interval samples, < 10 threshold).
2. Missing TB5 mandatory 12.0V over-range input check.
3. Malformed non-numeric token injection.
4. Non-finite token injection (`NaN` / `Inf`).
5. Missing simulator output data file.
6. Missing circuit SPICE netlist file.
7. Failed simulator executable invocation.
8. Universal report generation robustness without secondary crashes.
9. Deliberately perturbed TB4 ideal agreement dataset (+15mV offset producing $R^2_{ideal} = 0.999063 < 0.9999$ specific failure and helper unit testing).
Results are recorded in `Negative_Testing/NEGATIVE_TEST_REPORT.json`.

---

## 5. How to Open and Verify in eSim 2.5
1. Launch **eSim 2.5** graphical user interface.
2. Select **Project -> Open Project**.
3. In the directory browser dialog, navigate to the extracted release directory.
4. Select `MISACS.proj` (or select the project folder).
5. The eSim console and activity explorer will display:
   `Project MISACS opened successfully.`
6. Click the **Schematic Editor** (Eeschema) icon to open `MISACS.kicad_sch`. Confirm 0 errors on load.
7. Click the **PCB Editor** (Pcbnew) icon to open `MISACS.kicad_pcb`. Confirm board renders with complete routing and solid ground plane.

---

## 6. How to Open and Verify in KiCad 6.0.11
1. Open KiCad 6.0.11.
2. Select **File -> Open Project...** and choose `MISACS.kicad_pro`.
3. Open Schematic: Run **Inspect -> Electrical Rules Checker (ERC)** -> Confirm **0 Errors**, 74 documented `lib_symbol_issues` warnings (`Reports/MISACS_PHASE3_6_ERC.rpt`).
4. Open PCB Layout: Run **Inspect -> Design Rules Checker (DRC)** -> Confirm **0 Violations, 0 Unconnected Pads** (`Reports/MISACS_PHASE3_6_DRC.rpt`).
