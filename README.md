# ?? Battery Over/Under-Voltage Window Comparator PCB Design

[![eSim Version](https://img.shields.io/badge/eSim-v2.3%20%7C%20v2.5-blue.svg)](https://esim.fossee.in/)
[![KiCad Version](https://img.shields.io/badge/KiCad-v4.0.7-orange.svg)](https://www.kicad.org/)
[![Ngspice](https://img.shields.io/badge/Ngspice-v35-red.svg)](http://ngspice.sourceforge.net/)
[![ERC Status](https://img.shields.io/badge/ERC-0%20Errors-brightgreen.svg)]()
[![DRC Status](https://img.shields.io/badge/DRC-0%20Violations-brightgreen.svg)]()
[![PCB Layers](https://img.shields.io/badge/Layers-2%20Copper-green.svg)]()
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE)

---

## ?? Project Overview
In modern Battery Management Systems (BMS), maintaining battery cell voltages within a safe operational window is vital to prevent deep-discharge degradation or overcharge thermal runaway.

This project implements an **autonomous hardware-level Window Comparator** using dual precision **LM741 Operational Amplifiers**. It continuously senses the battery terminal voltage in real-time and provides immediate visual alerts through dedicated fault LEDs without requiring a microcontroller.

### ?? Key Features:
- **Under-Voltage Indicator (Low Battery):** Red **LED 1** turns **ON** when battery voltage falls below **5.18 V**.
- **Normal Operating Window (Safe Zone):** Both LEDs remain **OFF** while the battery voltage stays between **5.18 V and 12.94 V**.
- **Over-Voltage Indicator (Over-Charge):** Red **LED 2** turns **ON** when battery voltage exceeds **12.94 V**.
- **Decoupling Protection:** Integrated 100 nF high-frequency ceramic capacitor to suppress power rail switching transients.

---

## ?? Circuit Schematic

The schematic was designed and captured in **eSim Eeschema** with complete Electrical Rules Check validation (**0 Errors**).

![Circuit Schematic](./battery_comparator.png)

---

## ?? Mathematical Formulations & Working

### 1. Reference Voltage Ladder ({CC} = 12\text{ V}$):
R_{total} = R_1 (4.7\text{k}\Omega) + R_2 (3.3\text{k}\Omega) + R_3 (2.2\text{k}\Omega) = 10.2\text{k}\Omega

- **High Reference Voltage ({high\_ref}$):**
  V_{high\_ref} = 12\text{V} \times \frac{R_2 + R_3}{R_{total}} = 12\text{V} \times \frac{5.5\text{k}}{10.2\text{k}} \approx \mathbf{6.47\text{ V}}

- **Low Reference Voltage ({low\_ref}$):**
  V_{low\_ref} = 12\text{V} \times \frac{R_3}{R_{total}} = 12\text{V} \times \frac{2.2\text{k}}{10.2\text{k}} \approx \mathbf{2.59\text{ V}}

### 2. Battery Voltage Sense Divider ( = R_5 = 10\text{k}\Omega$):
V_{sense} = V_{battery} \times \frac{R_5}{R_4 + R_5} = \mathbf{0.50 \times V_{battery}}

### 3. Threshold Mapping:
- **Low-Battery Cutoff:** {batt\_low} = \frac{V_{low\_ref}}{0.50} = \frac{2.59\text{V}}{0.50} = \mathbf{5.18\text{ V}}$
- **Over-Voltage Cutoff:** {batt\_high} = \frac{V_{high\_ref}}{0.50} = \frac{6.47\text{V}}{0.50} = \mathbf{12.94\text{ V}}$

---

## ?? Operational Truth Table

| Battery Voltage ({batt}$) | Scaled Sense ({sense}$) | Comparator U1 (Low-Batt) | Comparator U2 (Over-Volt) | LED 1 (Low-Batt) | LED 2 (Over-Volt) | Operating Status |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **$< 5.18\text{ V}$** | $< 2.59\text{ V}$ | **HIGH ($\approx 11.5\text{V}$)** | LOW (\text{V}$) | ?? **ON** | ? OFF | **Under-Voltage Fault** |
| **.18\text{ V} - 12.94\text{ V}$** | .59\text{ V} - 6.47\text{ V}$ | LOW (\text{V}$) | LOW (\text{V}$) | ? OFF | ? OFF | ?? **Normal (Safe Window)** |
| **$> 12.94\text{ V}$** | $> 6.47\text{ V}$ | LOW (\text{V}$) | **HIGH ($\approx 11.5\text{V}$)** | ? OFF | ?? **ON** | ?? **Over-Voltage Fault** |

---

## ??? Bill of Materials (BOM) & Footprint Assignment

| RefDes | Qty | Value / Component | Function | KiCad Footprint (CvPcb) |
| :--- | :---: | :--- | :--- | :--- |
| **X1, X2** | 2 | LM741 | Operational Amplifier ICs | Housings_DIP:DIP-8_W7.62mm |
| **R1** | 1 | .7\text{ k}\Omega$, .25\text{W}$ | Ref Ladder (Top) | Resistors_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal |
| **R2** | 1 | .3\text{ k}\Omega$, .25\text{W}$ | Ref Ladder (Middle) | Resistors_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal |
| **R3** | 1 | .2\text{ k}\Omega$, .25\text{W}$ | Ref Ladder (Bottom) | Resistors_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal |
| **R4, R5** | 2 | \text{ k}\Omega$, .25\text{W}$ | Battery Sense Divider | Resistors_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal |
| **R6, R7** | 2 | \ \Omega$, .25\text{W}$ | LED Current Limiters | Resistors_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal |
| **D1, D2** | 2 | 5mm Standard LED | Status Indicator LEDs | LEDs:LED_D5.0mm |
| **C1** | 1 | \text{ nF}$ (.1\mu\text{F}$) | HF Decoupling Capacitor | Capacitors_THT:C_Disc_D3.0mm_W1.6mm_P2.50mm |
| **v1, v2** | 2 | 2-Pin Screw Terminal | Power & Sense Ports | Pin_Headers:Pin_Header_Straight_1x02_Pitch2.54mm |

---

## ??? 2-Layer PCB Layout & 3D Visualization

The PCB was laid out and routed in **Pcbnew** adhering to IPC standards with **0 DRC Violations** and **0 Unconnected Pads (20/20 Connections Complete)**.

![3D PCB Layout](./battery_comparator_3d.png)

### Design Specifications:
- **Stackup:** 2 Copper Layers (Top Layer F.Cu in Red, Bottom Layer B.Cu in Green).
- **Track Geometry:** 0.250 mm (9.84 mils) signal traces with ^\circ$ mitered bends.
- **Routing Strategy:** Orthogonal trace routing to eliminate track collisions without external jumpers.
- **Manufacturing Outputs:** Industrial standard RS-274X Gerber and Excellon drill files generated in ./Gerber/.

---

## ?? How to Run the Project in eSim

1. **Clone the repository:**
   `ash
   git clone https://github.com/krisanthM/eSim_PCB_Design_Project_Files.git
   `
2. **Open in eSim:**
   - Launch **eSim v2.3 / v2.5**.
   - Click **Open Project** $\rightarrow$ Select the attery_comparator directory.
3. **Verify Schematic:**
   - Open **Eeschema** $\rightarrow$ Click **Tools > Perform Electrical Rules Check (ERC)** $\rightarrow$ Verify **0 Errors**.
4. **Run Simulation:**
   - In eSim, click **Convert KiCad to Ngspice** $\rightarrow$ Click **Simulation**.
5. **Inspect PCB Layout & 3D View:**
   - Click **PCB Layout** to launch Pcbnew $\rightarrow$ Click **Tools > Perform Design Rules Check (DRC)**.
   - Press **Alt + 3** to view the 3D board render.

---

## ?? Repository Structure

`
+-- battery_comparator.sch              # Schematic file (Eeschema)
+-- battery_comparator.kicad_pcb         # 2-Layer PCB Layout (Pcbnew)
+-- battery_comparator.net              # PCB Netlist
+-- battery_comparator.cir              # Ngspice Netlist
+-- battery_comparator.pro              # Project Configuration
+-- Gerber/                             # Gerber & Drill Manufacturing Files
+-- report_esim.pdf                     # Detailed Project Report
+-- battery_comparator.png              # Circuit Schematic
+-- battery_comparator_3d.png           # 3D PCB View
+-- README.md                           # Project Documentation
`

---

## ?? Author & Acknowledgements

- **Author:** Krisanth M ([@krisanthM](https://github.com/krisanthM))  
- **Email:** krisanth2006@gmail.com  
- **Organization:** FOSSEE, Indian Institute of Technology Bombay (IIT Bombay)  
- **Program:** eSim Semester-Long Internship — Autumn 2026 (Task 7 Submission)
