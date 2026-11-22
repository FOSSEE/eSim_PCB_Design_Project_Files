# MISACS — FOSSEE eSim Winter Internship 2026 Task 7 Project Execution & Verification Guide

**Project:** Modular Industrial Sensor Acquisition and Control System (MISACS)  
**Program:** FOSSEE eSim Winter Internship 2026 — Screening Task 7: PCB Design using eSim  
**Author / Intern:** Nikhil J (Lead Engineer)
  
**EDA Software:** eSim 2.5 (FOSSEE, IIT Bombay) + KiCad 6.0.11 + Ngspice (nghdl-simulator)  
**OS Platform:** Microsoft Windows 10 / 11 (64-bit)  
**Submission Package:** `MISACS_FOSSEE_Winter_2026_Task7_Submission_Package_VisualEvidence_Revision2.zip`  
**Status:** Approved Engineering Release Candidate — Submission Preparation Ready  

---

## 1. System Requirements & EDA Environment

To open, inspect, simulate, and verify the MISACS project, ensure your workstation meets the following configuration:

| Component | Minimum Version | Recommended / Tested Version | Sourcing / Install Path |
| :--- | :--- | :--- | :--- |
| **Operating System** | Windows 10 x64 | Windows 11 x64 (22H2+) | Standard OS |
| **eSim Suite** | eSim 2.4 | eSim 2.5 (IIT Bombay) | `C:\FOSSEE\eSim\eSim.exe` |
| **KiCad EDA** | KiCad 6.0.0 | KiCad 6.0.11 (64-bit) | `C:\Program Files\KiCad\6.0\bin\kicad.exe` |
| **Ngspice Engine** | Ngspice 32 | Ngspice 35 (FOSSEE NGHDL build) | `C:\FOSSEE\nghdl-simulator\bin\ngspice.exe` |
| **Python Runtime** | Python 3.8 x64 | Python 3.9+ x64 | Standard System Python or KiCad Python |
| **Dependencies** | Standard Library | `math`, `subprocess`, `hashlib`, `json`, `os`, `re` | No external pip packages needed for sim runner |

---

## 2. Archive Extraction & Provenance Verification

### 2.1 Archive Extraction
Extract the submission package `MISACS_FOSSEE_Winter_2026_Task7_Submission_Package_VisualEvidence_Revision2.zip` into your working directory (e.g. `C:\FOSSEE_Review\`):
```powershell
Expand-Archive -Path 'MISACS_FOSSEE_Winter_2026_Task7_Submission_Package_VisualEvidence_Revision2.zip' -DestinationPath 'C:\FOSSEE_Review\'
```

### 2.2 Cryptographic Baseline Verification
The hardware design files are frozen and cryptographically immutable. You can verify the integrity of the core schematic and PCB layout files:

```powershell
Get-FileHash 'eSim_Project\MISACS.kicad_sch' -Algorithm SHA256
Get-FileHash 'eSim_Project\MISACS.kicad_pcb' -Algorithm SHA256
```
**Expected Canonical Digest Values:**
- **Schematic (`MISACS.kicad_sch`):** `6DE222A83B9F2B13141575CEB4C2BE5E1923FCCB374766BCFE82D35701CE10B8`
- **PCB Layout (`MISACS.kicad_pcb`):** `136E71039AF185293E34E51087B60F242863BE97F9A93EC3C97C44F1EA3E88A4`

---

## 3. Opening the Project in eSim 2.5 / KiCad 6.0.11

### 3.1 Method A: Native eSim 2.5 Front-End
1. Launch **eSim 2.5** from the Start Menu or run `C:\FOSSEE\eSim\eSim.exe`.
2. Click **Open Project** (or `File -> Open Project`).
3. Navigate to the extracted `eSim_Project/` folder and select `MISACS.proj`.
4. eSim 2.5 Execution & Host Verification:
   `C:\FOSSEE\eSim\eSim.exe` executes natively on Windows 11 Enterprise (64-bit), unpacks its PyInstaller bundled dependencies into `%TEMP%\_MEI*` in ~13 seconds, and renders its PyQt5 graphical interface. The previous claim of WinError 4551 / Smart App Control interception was investigated and disproved (it was caused by automated non-interactive process timeout during initial unpack; zero Code Integrity blocks occurred).
5. Standard Evaluator Execution:
   Evaluators on Windows or Linux can open `MISACS.proj` directly in eSim 2.5 or open `MISACS.kicad_pro` via **Method B (KiCad 6.0.11 Project Manager)** to inspect all design files with 100% bit-level fidelity.

### 3.2 Method B: KiCad 6.0.11 Project Manager
1. Launch **KiCad 6.0** (`C:\Program Files\KiCad\6.0\bin\kicad.exe`).
2. Click `File -> Open Project...` and select `eSim_Project\MISACS.kicad_pro`.
3. The project tree will display all associated project files:
   - `MISACS.kicad_sch` (Hierarchical / Flat Schematic)
   - `MISACS.kicad_pcb` (Board Layout)
   - Project library tables (`sym-lib-table`, `fp-lib-table`)

---

## 4. Inspecting Schematic & Subsystems in KiCad Eeschema

1. From the KiCad Project Manager, double-click `MISACS.kicad_sch` (or click the Schematic Editor icon).
2. The schematic will open in **Eeschema 6.0.11**.
3. Use the mouse wheel to zoom and drag to pan across the 10 functional subsystems:
   - **Subsystem 1:** Main 24V Input Protection (D14 SS56 5A reverse shunt diode, F1 Bourns 1.1A hold / 2.2A trip resettable PTC, D2 SS36 series reverse blocking diode, D1 SMBJ30A 30V TVS surge clamp).
   - **Subsystem 2:** 24V-to-5V Step-Down Buck Converter (TI LM2576HVS-5.0, 100uH inductor, 1N5822 catch diode, 1000uF low-ESR bulk output capacitor).
   - **Subsystem 3:** 5V-to-3.3V Low-Dropout Linear Regulator (AMS1117-3.3 with distributed ceramic decoupling).
   - **Subsystem 4:** 4–20 mA Current-Loop Receiver (Susumu 100.0 Ohm 0.1% precision shunt, TI TPS26610 active eFuse current limiter, TI LMV358 buffer).
   - **Subsystem 5:** 0–10 V Industrial Voltage Input (Susumu 30.0k / 10.0k 0.1% precision 4:1 divider, TI LMV358 buffer).
   - **Subsystem 6:** ADS1115 16-Bit Precision ADC (TI ADS1115IDGSR, I2C pullups, BAT54S dual Schottky rail clamp diodes).
   - **Subsystem 7:** Processing Core (Espressif ESP32-WROOM-32E-N16, EN reset RC network, IO0 boot switch).
   - **Subsystem 8:** RS-485 Differential Interface (Maxim MAX3485EESA half-duplex transceiver, 120 Ohm termination DIP switch, pull-up/pull-down failsafe bias network).
   - **Subsystem 9:** High-Current Actuator Gate Drivers (TI UCC27524 high-speed dual low-side driver with independent gate resistors).
   - **Subsystem 10:** Dual Low-Side Actuator MOSFETs (Infineon IPD50N06S4L-08 60V 50A 8.4mΩ N-channel MOSFETs, SS36 inductive flyback clamp diodes).
4. **Intentional No-Connect (NC) Verification:**  
   Confirm that all 4 intentional NC endpoints carry KiCad No-Connect flags:
   - ESP32 Pin 14 (`IO12 / MTDI`): Left unconnected to guarantee standard 3.3V flash boot voltage.
   - ADS1115 Pin 2 (`ALERT/RDY`): Left unconnected (polling mode operation).
   - TPS26610 Pin 7 (`VSNS`) & Pin 8 (`SGOOD`): Dedicated current limiter mode with internal sensing.

---

## 5. Inspecting PCB Layout in KiCad Pcbnew

1. Double-click `MISACS.kicad_pcb` to launch **Pcbnew 6.0.11**.
2. **Physical Dimensions:** Verify the board outline on `Edge.Cuts` measures exactly 100.0 mm x 80.0 mm with 3.0 mm corner radii.
3. **Mounting Holes:** Confirm 4x M3 mounting holes (`MountingHole_3.2mm_M3`) located symmetrically at (5.0 mm, 5.0 mm) inset from board edges.
4. **Layer Stackup:**
   - **F.Cu (Top Layer):** Carries component pads, signal traces, gate drive tracks (1.0 mm), 24V actuator bus polygons (2.0 mm), and thermal copper pours.
   - **B.Cu (Bottom Layer):** Solid, unbroken low-impedance ground plane (`GND`) with thermal via stitching under regulators and MOSFET tabs.
5. **Layer Navigation Hotkeys:**
   - Press `Page Up` to switch to `F.Cu`.
   - Press `Page Down` to switch to `B.Cu`.
   - Press `B` to recalculate and refresh all copper zone fills.

---

## 6. Running ERC and Native DRC

### 6.1 Electrical Rules Check (ERC)
1. In Eeschema, click `Inspect -> Electrical Rules Checker`.
2. Click **Run ERC**.
3. **Result:**
   - **0 Errors.**
   - **74 Warnings:** All 74 warnings represent benign symbol library pin-type mismatches documented in `Documentation/09_ERC_REPORT.md` (e.g. passive pins on ground networks).

### 6.2 Design Rules Check (DRC)
1. In Pcbnew, click `Inspect -> Design Rules Checker` (or click the ladybug DRC icon).
2. Ensure the following test constraints are active:
   - Minimum track clearance: 0.20 mm
   - Minimum track width: 0.25 mm
   - Minimum annular ring: 0.15 mm
   - Minimum copper-to-edge clearance: 0.50 mm
3. Click **Run DRC**.
4. **Verification Result:**
   ```
   ** Found 0 DRC violations **
   ** Found 0 unconnected pads **
   ** Found 0 Footprint errors **
   ```
   A fresh native DRC report is preserved at `Verification/MISACS_FRESH_NATIVE_DRC_REPORT.rpt`.

---

## 7. Launching and Navigating KiCad 3D Viewer

1. In Pcbnew, press `Alt+3` (or click `View -> 3D Viewer`).
2. The interactive 3D Viewer canvas will open, rendering the fully populated MISACS PCB assembly.
3. **Navigation Controls:**
   - **Rotate:** Left-click and drag across the canvas.
   - **Pan:** Middle-click and drag (or right-click and drag).
   - **Zoom:** Mouse wheel scroll.
   - **Top View:** Press `Z` (or `View -> Top View`).
   - **Bottom View:** Press `Shift+Z` (or `View -> Bottom View`).
   - **Fit Board to Window:** Press `Home`.
4. **3D Model Audit:**
   - 70 functional circuit components have 3D models assigned and render accurately.
   - 4 mechanical mounting holes (`MountingHole_3.2mm_M3`) are non-component plated drill holes and do not require 3D models.

---

## 8. Executing Qualified Ngspice Simulation Suite (10 Testbenches)

Both the root project directory and the `Simulation/` subdirectory contain the hardened automated simulation runner `run_simulations.py`.

### 8.1 Running the Suite
Open a terminal in `eSim_Project/` (or the project root) and execute:
```bash
python run_simulations.py
```
*(Alternatively, point to system python: `python Simulation/run_simulations.py`)*

### 8.2 Execution Results & Status Matrix
The suite executes all 10 Ngspice netlists in approximately 4.9 s, producing vector SVG plots in `Evidence/` and execution logs in `Evidence/Simulation_Logs/`:

| Testbench | Description | Simulation Status | Engineering Qualification | Key Verified Metric |
| :--- | :--- | :---: | :---: | :--- |
| **TB1** | 24V Input Protection & Shunt Clamping | **PASS** | **CONDITIONAL / NOT VERIFIED** | TVS clamp 44.02 V <= 60.0 V; reverse logic 0.00 V; D14 reverse shunt conditional on external fusing |
| **TB2** | LM2576 Buck Regulator (52 kHz) | **PASS** | **PASS** | V_out = 5.019 V, ripple 24.7 mV <= 50.0 mV, switch freq 52.4 kHz |
| **TB3** | AMS1117-3.3 LDO Regulator | **PASS** | **NOT VERIFIED** | Static V_out = 3.308 V, ripple 3.12 mV; RF load dynamic stability unverified |
| **TB4** | 4–20 mA Current Loop Receiver | **PASS** | **PASS** | R^2_reg = 1.000000, slope 100.00 V/A, ideal fit R^2_ideal = 1.000000 |
| **TB5** | 0–10 V Voltage Input Divider | **PASS** | **PASS** | Division ratio 4.000:1, max output 2.5000 V, over-range 12V -> 3.000 V <= 3.3 V |
| **TB6** | ADS1115 ADC Input Protection | **PASS** | **CONDITIONAL / NOT VERIFIED** | Room temp clamp -0.281 V / +3.591 V; cold clamp and deep-sleep rail rise unverified |
| **TB7** | UCC27524 Gate Driver Dynamics | **PASS** | **PASS** | Rise time t_r = 18.2 ns <= 50.0 ns, fall time t_f = 14.6 ns <= 50.0 ns |
| **TB8** | Dual Low-Side Actuator Loads | **PASS** | **PASS** | Channel 1: 3.996 A >= 3.8 A; Channel 2: 2.498 A >= 2.3 A |
| **TB9** | Inductive Flyback Clamp (10 mH) | **PASS** | **PASS** | Drain clamp 24.846 V <= 35.0 V, safe margin below 30 V V_DSS rating |
| **TB10** | RS-485 Differential Bus (1 Mbps)| **PASS** | **PASS** | Differential swing V_diff = 2.144 V >= 1.5 V, t_r = 14.1 ns, t_f = 14.3 ns |

---

## 9. Executing the Automated Negative Testing Suite

To independently verify the robustness of the simulation runner against malformed netlists, non-convergent sweeps, non-finite tokens, and corrupted tables, run the negative testing suite:

```bash
python Negative_Testing/test_negative_cases.py
```

### Verified Error Trapping Cases:
- **Case 1:** Swept table too short / missing operating points -> Trapped.
- **Case 2:** Missing required measurement signal header -> Trapped.
- **Case 3:** Non-finite numeric token (`NaN`) -> Trapped.
- **Case 4:** Non-finite numeric token (`Inf`) -> Trapped.
- **Case 5:** Malformed non-numeric token in data line -> Trapped.
- **Case 6:** Mismatched token count per row -> Trapped.
- **Case 7:** Non-monotonic sweep values -> Trapped.
- **Case 8:** Missing DC bias point table -> Trapped.
- **Case 9:** Out-of-range operating DC voltage -> Trapped.

**Result: 9 / 9 Test Cases PASSED.** (Machine-readable report preserved in `Negative_Testing/NEGATIVE_TEST_REPORT.json`).

---

## 10. Manufacturing Gerbers & Drill Files Inspection

The `Gerber/` folder contains production-ready manufacturing files formatted to RS-274X (Gerber) and Excellon (Drill) standards:
- `MISACS-F_Cu.gbr` (Top Copper)
- `MISACS-B_Cu.gbr` (Bottom Copper & Solid GND)
- `MISACS-F_Mask.gbr` & `MISACS-B_Mask.gbr` (Solder Masks)
- `MISACS-F_SilkS.gbr` & `MISACS-B_SilkS.gbr` (Silkscreen Legends)
- `MISACS-F_Paste.gbr` & `MISACS-B_Paste.gbr` (Solder Paste Stencils)
- `MISACS-Edge_Cuts.gbr` (Board Outline: 100.00 mm x 80.00 mm nominal centerline; 100.15 mm x 80.15 mm outer line extents)
- `MISACS-PTH.drl` (Plated Through Holes)
- `MISACS-NPTH.drl` (Non-Plated Holes for M3 Mounting Screws)

These can be inspected using KiCad GerbView (`C:\Program Files\KiCad\6.0\bin\gerbview.exe`) or any standard CAM tool.

---

## 11. Support & Contact

For questions regarding this screening task submission:
- **Project Repository / Submission:** FOSSEE eSim Winter Internship 2026 Screening Task 7
- **FOSSEE eSim Team:** contact-esim@fossee.in | https://esim.fossee.in
