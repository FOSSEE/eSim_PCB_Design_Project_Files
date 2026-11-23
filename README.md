# Industrial 4–20 mA Current Loop Receiver & Fault Detection System

**FOSSEE / IIT Bombay eSim Semester Long Internship (Autumn 2026)**  
**Submission:** Task 7 — PCB Design using eSim  
**Toolchain:** eSim 2.5 (KiCad 6.0.11 native design engine)  
**Author:** Eshaan Abrol  

---

## 1. Project Overview & Motivation

The 4–20 mA current loop is the global standard in industrial instrumentation and SCADA process control due to its unmatched noise immunity and zero signal attenuation over long cable distances.

This project delivers a **hardware-autonomous, highly reliable 2-layer PCB receiver board** that:
1. Converts industrial **4–20 mA** sensor current into a calibrated **1.000 V to 5.000 V DC** analog voltage.
2. Provides active hardware window comparison to immediately detect and flag critical line faults:
   - **Wire-Break Fault** (< 3.2 mA, Yellow LED2) — open circuit, severed field cable, or disconnected transmitter.
   - **Normal Loop Operation** (4.0 mA – 20.0 mA, Green LED4) — healthy process loop.
   - **Over-Current Fault** (> 20.8 mA, Red LED3) — short circuit, sensor failure, or current runaway.
3. Incorporates heavy-duty input surge protection (5.6 V Zener clamp), EMI/RFI filtering ( \approx 1.59\text{ kHz}$), reverse-polarity protection, and an onboard +12 V regulated rail.

---

## 2. Key Technical Specifications

| Parameter | Implemented Specification | Notes |
|:---|:---|:---|
| **Power Supply Input** | +24.0 V DC nominal (18–30 V DC range) | Reverse-polarity diode protected (1N4007) |
| **Regulated Rail** | +12.0 V DC ± 4% | LM7812 TO-220 linear regulator with heat relief |
| **Input Signal** | 4–20 mA industrial current loop | From pressure, temperature, or flow transmitters |
| **Current Shunt** | 250.0 Ω, 0.1% tolerance, 1/4 W | Yields exactly 1.000 V at 4 mA, 5.000 V at 20 mA |
| **Input Surge Clamp** | 5.6 V Zener diode (D4) | Protects LM358 input from inductive line surges |
| **Analog Filter** | 1.0 kΩ + 100 nF RC low-pass ( \approx 1.59\text{ kHz}$) | Suppresses 50 Hz hum, relay chatter & EMI |
| **Buffer Amplifier** | LM358 unity-gain voltage follower | High input impedance, eliminates shunt loading |
| **Precision Reference** | TL431 programmable bandgap (2.500 V) | High thermal stability (50 ppm/°C) |
| **Low Fault Trip Point** | 0.800 V DC (corresponds to 3.20 mA) | Wire-break / open-loop fault detection |
| **High Fault Trip Point**| 5.200 V DC (corresponds to 20.80 mA) | Over-current / sensor short fault detection |
| **Window Comparator** | LM393 dual open-collector comparator | Drives diagnostic LED indicators directly |
| **Output Field Port** | 4-pin 5.08 mm screw terminal (J3) | V_BUFFERED, FAULT_LOW, FAULT_HIGH, GND |
| **PCB Dimensions** | 78.74 mm × 48.26 mm (3.10 in × 1.90 in) | 2-layer FR-4, 1.6 mm thickness, 1 oz copper |
| **DRC Compliance** | 0 DRC errors, 0 unconnected nets | Verified in native eSim 2.5 / KiCad 6.0 engine |

---

## 3. Repository Contents

- Industrial_4_20mA_Receiver.kicad_pcb: Fully routed 2-layer PCB file (native KiCad 6.0 / eSim 2.5 format).
- Industrial_4_20mA_Receiver.kicad_sch: Complete schematic captured in eSim Eeschema.
- Industrial_4_20mA_Receiver.net: Electrical netlist.
- Industrial_4_20mA_Receiver.proj: eSim project configuration file.
- Report_Industrial_4_20mA_Receiver.pdf: Comprehensive 16-page technical report covering project overview, circuit analysis, schematic details, footprint selection, PCB placement, routing methodology, DRC audit, 3D renderings, and bill of materials.
- PCB_Design_Proposal.pdf: Formal PCB design proposal for FOSSEE submission.
- system_block_diagram.png / .svg: High-resolution functional system block diagram.
- pcb_3d_top.png, pcb_3d_iso.png, pcb_3d_bottom.png: 3D photorealistic renderings of the PCB.
- pcb_layout_2d.png / .svg: 2D copper layer layout diagram.
- schematic_overview.png: High-resolution full schematic overview.

---

## 4. Software Compatibility

This project is 100% compatible with **eSim 2.5** and KiCad 6.0.11:
- Uses standard KiCad THT footprint libraries (Resistor_THT, Capacitor_THT, Package_DIP, TerminalBlock_Phoenix).
- Free of any external proprietary libraries or higher-version KiCad syntax conflicts.
