# ESP32-CAM Based TinyML Hand Classifier Carrier Board

> **Task 7 Submission** — eSim Semester Long Internship, Autumn 2026  
> **Intern:** Arya Sharan | **EDA Tool:** eSim 2.5

---

## 📋 Project Overview

A custom dual-layer PCB designed using eSim 2.5 to serve as a production-grade hardware carrier for an ESP32-CAM module running TinyML hand-sign classification at the edge. This board replaces fragile breadboard prototypes with a stable, high-current power supply, robust peripheral interfaces, and RF-aware layout for reliable Wi-Fi/Bluetooth connectivity.

## 🔧 Key Features

- **AMS1117-3.3V Power Regulation** — 5V input filtered by 10µF + 1000µF capacitors, stepped down to clean 3.3V
- **High-Current Power Traces** — 0.8mm wide traces for 5V/3.3V rails to minimize voltage drop
- **RF Antenna Keepout Zone** — Component-free exclusion area beneath ESP32-CAM's onboard PCB antenna
- **Hardware RESET & FLASH Buttons** — Tactile switches with 10kΩ pull-ups for streamlined firmware programming
- **Status LED** — Power indicator with 330Ω current-limiting resistor
- **I²C Expansion Header** — External peripheral connectivity via header connectors
- **Custom Footprint Library** — Dedicated `esp32cam.pretty` library with custom ESP32-CAM footprint

## 📐 Board Specifications

| Parameter | Value |
|---|---|
| Board Layers | 2 (F.Cu + B.Cu) |
| Power Trace Width | 0.8 mm |
| Signal Trace Width | 0.4 mm |
| Power Input | 5V DC (Terminal Block) |
| Regulated Output | 3.3V (AMS1117-3.3) |
| EDA Software | eSim 2.5 |
| DRC Result | **0 Errors** ✅ |

## 📂 Repository Structure

```
ESP32_TinyML_Hand_Classifier/
├── ESP32_TinyML_Classifier.kicad_sch    # Schematic
├── ESP32_TinyML_Classifier.kicad_pcb    # PCB Layout
├── ESP32_TinyML_Classifier.kicad_pro    # Project file
├── ESP32_TinyML_Classifier.kicad_prl    # Project local settings
├── ESP32_TinyML_Classifier.net          # Netlist
├── esp32camheader.kicad_sym             # Custom symbol library
├── fp-lib-table                         # Footprint library table
├── sym-lib-table                        # Symbol library table
├── esp32cam.pretty/                     # Custom footprint library
│   ├── ESP32CAM_2x08_18mm.kicad_mod     # Custom ESP32-CAM footprint
│   ├── esp32.kicad_mod                  # ESP32 footprint
│   └── esp32_cam.kicad_mod              # ESP32-CAM alternate footprint
└── Gerbers/                             # Production-ready Gerber files
    ├── Tiny_ml_hand_classifier-F_Cu.gbr
    ├── Tiny_ml_hand_classifier-B_Cu.gbr
    ├── Tiny_ml_hand_classifier-F_Mask.gbr
    ├── Tiny_ml_hand_classifier-B_Mask.gbr
    ├── Tiny_ml_hand_classifier-F_Paste.gbr
    ├── Tiny_ml_hand_classifier-B_Paste.gbr
    ├── Tiny_ml_hand_classifier-F_Silkscreen.gbr
    ├── Tiny_ml_hand_classifier-B_Silkscreen.gbr
    ├── Tiny_ml_hand_classifier-Edge_Cuts.gbr
    ├── Tiny_ml_hand_classifier-PTH.drl
    ├── Tiny_ml_hand_classifier-NPTH.drl
    └── Tiny_ml_hand_classifier-job.gbrjob
```

## 🔌 Circuit Description

- **Power Stage:** AMS1117-3.3V LDO with 10µF + 1000µF input filtering and clean 3.3V output for ESP32-CAM
- **Control Logic:** Hardware RESET (SW1) and FLASH/GPIO0 (SW2) pushbuttons with 10kΩ pull-up resistors
- **Status Indicator:** Green LED with 330Ω series resistor on 3.3V rail
- **Expansion:** I²C and serial headers (J1–J3) for external peripherals

## 🛠 Routing Methodology

- **Dual-width routing:** 0.8mm for power, 0.4mm for signals
- **Orthogonal layer transitions** to avoid signal trapping
- **Trace necking** at tight pad clearances to prevent DRC violations
- **RF keepout rule area** isolated to antenna footprint layers (F.Cu/B.Cu)

## ✅ DRC Verification

The board passes DRC with **0 Errors**. 15 non-blocking cosmetic warnings were reviewed and intentionally accepted (single-layer via tie points and silkscreen/margin overlaps from custom footprint creation).

## 📝 License

This project is submitted as part of the FOSSEE eSim Semester Long Internship — Autumn 2026.

---

**Author:** Arya Sharan  
**GitHub:** [@Aryakuna14](https://github.com/Aryakuna14)
