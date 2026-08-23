# Battery Over/Under-Voltage Window Comparator PCB Design

[![eSim Version](https://img.shields.io/badge/eSim-v2.3%20%7C%20v2.5-blue.svg)](https://esim.fossee.in/)
[![KiCad Version](https://img.shields.io/badge/KiCad-v4.0.7-orange.svg)](https://www.kicad.org/)
[![Ngspice](https://img.shields.io/badge/Ngspice-v35-red.svg)](http://ngspice.sourceforge.net/)
[![ERC Status](https://img.shields.io/badge/ERC-0%20Errors-brightgreen.svg)]()
[![DRC Status](https://img.shields.io/badge/DRC-0%20Violations-brightgreen.svg)]()
[![PCB Layers](https://img.shields.io/badge/Layers-2%20Copper-green.svg)]()
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE)

---

## 1. Project Overview

In modern Battery Management Systems (BMS), maintaining battery cell voltages within a safe operational window is vital to prevent deep-discharge degradation or overcharge thermal runaway.

This project implements an **autonomous hardware-level Window Comparator** using dual precision **LM741 Operational Amplifiers**. It continuously senses the battery terminal voltage in real-time and provides immediate visual alerts through dedicated fault LEDs without requiring a microcontroller.

### Key Features:
- **Under-Voltage Indicator (Low Battery):** Red **LED 1** turns **ON** when battery voltage falls below **5.18 V**.
- **Normal Operating Window (Safe Zone):** Both LEDs remain **OFF** while the battery voltage stays between **5.18 V** and **12.94 V**.
- **Over-Voltage Indicator (Over-Charge):** Red **LED 2** turns **ON** when battery voltage exceeds **12.94 V**.
- **Decoupling Protection:** Integrated 100 nF high-frequency ceramic capacitor to suppress power rail switching transients.

---

## 2. Circuit Schematic

The schematic was designed and captured in **eSim Eeschema** with complete Electrical Rules Check validation (**0 Errors**).

![Circuit Schematic](./battery_comparator.png)

---

## 3. Mathematical Calculations & Working Principle

### A. Reference Voltage Ladder (Supply V_CC = 12 V):
- **Total Resistance:**  
  R_total = R1 (4.7 k) + R2 (3.3 k) + R3 (2.2 k) = 10.2 k Ohm

- **Upper Threshold Reference (V_high_ref):**  
  V_high_ref = 12 V * (R2 + R3) / R_total = 12 V * (5.5 k / 10.2 k) = 6.47 V

- **Lower Threshold Reference (V_low_ref):**  
  V_low_ref = 12 V * R3 / R_total = 12 V * (2.2 k / 10.2 k) = 2.59 V

### B. Battery Voltage Sensing Divider (R4 = R5 = 10 k Ohm):
- **Scaled Sense Voltage (V_sense):**  
  V_sense = V_battery * R5 / (R4 + R5) = V_battery * (10 k / 20 k) = 0.50 * V_battery

### C. Threshold Mapping to Actual Battery Voltages:
- **Low-Battery Fault Cutoff:**  
  V_batt_low = V_low_ref / 0.50 = 2.59 V / 0.50 = 5.18 V

- **Over-Voltage Fault Cutoff:**  
  V_batt_high = V_high_ref / 0.50 = 6.47 V / 0.50 = 12.94 V

---

## 4. Operational Truth Table

| Battery Voltage (V_batt) | Scaled Sense (V_sense) | Comparator U1 (Low-Batt) | Comparator U2 (Over-Volt) | LED 1 (Low-Batt) | LED 2 (Over-Volt) | Operating Status |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **< 5.18 V** | < 2.59 V | **HIGH (~11.5 V)** | LOW (0 V) | **ON (Red)** | OFF | **Under-Voltage Fault** |
| **5.18 V - 12.94 V** | 2.59 V - 6.47 V | LOW (0 V) | LOW (0 V) | OFF | OFF | **Normal (Safe Window)** |
| **> 12.94 V** | > 6.47 V | LOW (0 V) | **HIGH (~11.5 V)** | OFF | **ON (Red)** | **Over-Voltage Fault** |

---

## 5. Bill of Materials (BOM) & Footprint Assignment

| RefDes | Qty | Value / Component | Function | KiCad Footprint (CvPcb) |
| :--- | :---: | :--- | :--- | :--- |
| **X1, X2** | 2 | LM741 | Operational Amplifier ICs | Housings_DIP:DIP-8_W7.62mm |
| **R1** | 1 | 4.7 k Ohm, 0.25 W | Reference Ladder (Top) | Resistors_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal |
| **R2** | 1 | 3.3 k Ohm, 0.25 W | Reference Ladder (Middle) | Resistors_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal |
| **R3** | 1 | 2.2 k Ohm, 0.25 W | Reference Ladder (Bottom) | Resistors_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal |
| **R4, R5** | 2 | 10 k Ohm, 0.25 W | Battery Sense Divider | Resistors_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal |
| **R6, R7** | 2 | 330 Ohm, 0.25 W | LED Current Limiters | Resistors_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal |
| **D1, D2** | 2 | 5mm Standard LED | Status Indicator LEDs | LEDs:LED_D5.0mm |
| **C1** | 1 | 100 nF (0.1 uF) | HF Decoupling Capacitor | Capacitors_THT:C_Disc_D3.0mm_W1.6mm_P2.50mm |
| **v1, v2** | 2 | 2-Pin Screw Terminal | Power & Sense Ports | Pin_Headers:Pin_Header_Straight_1x02_Pitch2.54mm |

---

## 6. 2-Layer PCB Design Specifications

The PCB was laid out and routed in **Pcbnew** adhering to IPC standards:
- **Copper Layers:** 2 Layers (Top Layer F.Cu in Red, Bottom Layer B.Cu in Green).
- **Track Width:** 0.250 mm (9.84 mils) signal traces with 45 degree mitered bends.
- **Routing Strategy:** Orthogonal trace routing to eliminate track collisions without external jumpers.
- **DRC Verification:** **0 Errors**, **0 Unconnected Pads (20/20 Connections Complete)**.
- **Manufacturing Outputs:** Industrial standard RS-274X Gerber and Excellon drill files generated in ./Gerber/.

---

## 7. How to Run the Project in eSim

1. **Clone the repository:**
   ```bash
   git clone https://github.com/krisanthM/eSim_PCB_Design_Project_Files.git
   ```

2. **Open in eSim:**
   - Launch **eSim v2.3 / v2.5**.
   - Click **Open Project** -> Select the `battery_comparator` directory.

3. **Verify Schematic:**
   - Open **Eeschema** -> Click **Tools > Perform Electrical Rules Check (ERC)** -> Verify **0 Errors**.

4. **Run Simulation:**
   - In eSim, click **Convert KiCad to Ngspice** -> Click **Simulation**.

5. **Inspect PCB Layout:**
   - Click **PCB Layout** to launch Pcbnew -> Click **Tools > Perform Design Rules Check (DRC)**.
   - Press **Alt + 3** to view the 3D board render.

---

## 8. Repository File Structure

```text
├── battery_comparator.sch              # Schematic file (Eeschema)
├── battery_comparator.kicad_pcb         # 2-Layer PCB Layout (Pcbnew)
├── battery_comparator.net              # PCB Netlist
├── battery_comparator.cir              # Ngspice Netlist
├── battery_comparator.pro              # Project Configuration
├── Gerber/                             # Gerber & Drill Manufacturing Files
├── report_esim.pdf                     # Detailed Project Report
├── battery_comparator.png              # Circuit Schematic Image
└── README.md                           # Project Documentation
```

---

## 9. Author & Acknowledgements

- **Author:** Krisanth M ([@krisanthM](https://github.com/krisanthM))
- **Email:** krisanth2006@gmail.com
- **Organization:** FOSSEE, Indian Institute of Technology Bombay (IIT Bombay)
- **Program:** eSim Semester-Long Internship -- Autumn 2026 (Task 7 Submission)
