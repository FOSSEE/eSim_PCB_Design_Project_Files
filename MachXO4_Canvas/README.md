# MachX04_Canvas — Custom FPGA Development Board

> **FOSSEE eSim Winter Internship 2026 — Task 7: PCB Design using eSim**  
> **Designed by:** Saurabh Sinha (Third-Year B.Tech ECE, IIIT Naya Raipur)  
> **Date:** 23 November 2026  

---

## 🎥 Demonstration Video

A comprehensive 5-minute technical walkthrough and hardware demonstration of the MachXO4 Canvas development board:  
- **Video Link:** [https://drive.google.com/file/d/1bA2fzb_Q_-FsYkzUnRTprIzDjuLGJhoq/view?usp=sharing](https://drive.google.com/file/d/1bA2fzb_Q_-FsYkzUnRTprIzDjuLGJhoq/view?usp=sharing)

---

## 📋 Project Overview

**MachX04_Canvas** is a custom 2-layer FPGA development board built around the **Lattice MachXO4-4300HC (TQFP-144)** FPGA. The board is designed to serve as a versatile, low-cost development and prototyping platform for digital logic design, featuring USB-based JTAG programming and UART communication via an **FTDI FT2232HL** dual-channel USB bridge.

### Key Features
- **FPGA:** Lattice MachXO4-4300HC in TQFP-144 package (U4)
- **USB-JTAG/UART Bridge:** FTDI FT2232HL (U3) with 93LC56C-I/SN SPI configuration EEPROM (U2)
- **Power Supply:** NCP1117ST33T3G 3.3V LDO (U1) with +5V (USB VBUS), +3.3V, and +1.8V rails
- **Clock Sources:** Two crystal/oscillator footprints (Y1, Y2)
- **User I/O:** 11 user LEDs (D1–D11), 4 user switches + 1 reset switch (SW1–SW5)
- **Expansion Headers:** 4× I/O expansion headers (J2–J5) exposing FPGA bank pins
- **USB Interface:** USB-A connector (J6) for power and FTDI communication
- **PCB:** 2-layer design with top/bottom ground pours

---

## 📁 Folder Structure

```
MachX04_Canvas/
├── MachX04_Canvas.kicad_pro          # KiCad 9 project file
├── MachX04_Canvas.kicad_prl          # Project local settings
├── MachX04_Canvas.kicad_sch          # Root schematic (hierarchical)
├── MachX04_Canvas.kicad_pcb          # PCB layout
├── MachX04_Canvas.proj               # eSim project file
├── sym-lib-table                     # Project symbol library table
├── fp-lib-table                      # Project footprint library table
│
├── power_supply.kicad_sch            # Sub-sheet: LDO power supply (+5V/+3.3V/+1.8V)
├── ftdi_bridge.kicad_sch             # Sub-sheet: FTDI FT2232HL USB-JTAG/UART bridge + EEPROM
├── fpga_power.kicad_sch              # Sub-sheet: FPGA power distribution & decoupling
├── bank0.kicad_sch                   # Sub-sheet: FPGA Bank 0 I/O, LEDs, switches
├── bank1.kicad_sch                   # Sub-sheet: FPGA Bank 1 I/O, LEDs, header
├── bank2.kicad_sch                   # Sub-sheet: FPGA Bank 2 I/O, LEDs, header
├── bank345.kicad_sch                 # Sub-sheet: FPGA Banks 3/4/5 I/O, LEDs, headers
│
├── local_symbols/                    # Project-local symbol libraries (11 .kicad_sym files)
│   ├── 93LC56C-I_SN.kicad_sym
│   ├── Connector.kicad_sym
│   ├── Connector_Generic.kicad_sym
│   ├── Device.kicad_sym
│   ├── Interface_USB.kicad_sym
│   ├── Jumper.kicad_sym
│   ├── MachXO4.kicad_sym
│   ├── NCP1117ST33T3G.kicad_sym
│   ├── Oscillator.kicad_sym
│   ├── power.kicad_sym
│   └── Switch.kicad_sym
│
├── SnapEDA.pretty/                   # Project-local footprint library
│   ├── 61400416021.kicad_mod         # USB connector footprint
│   ├── SOT230P700X180-4N.kicad_mod   # NCP1117 LDO footprint
│   ├── SOIC127P600X175-8N.kicad_mod  # 93LC56C EEPROM footprint
│   ├── GCT_USB4085-GF-A_REVA4.kicad_mod  # Alternate USB footprint
│   ├── MULTICOMP_MC000991.kicad_mod  # Alternate switch footprint
│   └── USB4085-GF-A_REVA4.step      # 3D model for USB connector
│
├── local_3dmodels/                   # Custom 3D STEP models
│   ├── 61400416021.step              # USB connector 3D model
│   ├── NCP1117ST33T3G.step           # LDO regulator 3D model
│   └── 831019987.STEP               # FT2232HL 3D model
│
└── ERC/                              # ERC & DRC reports
    ├── ERC.rpt                       # Electrical Rules Check (0 errors)
    └── DRC.rpt                       # Design Rules Check (0 errors)
```

---

## 🚀 How to Open in eSim / KiCad

1. **Clone or download** this repository.
2. Open **eSim** (which bundles KiCad 9.0).
3. In KiCad, go to **File → Open Project** and navigate to `MachX04_Canvas/MachX04_Canvas.kicad_pro`.
4. The project will open with all symbol libraries, footprint libraries, and 3D models resolved automatically via `${KIPRJMOD}` paths — **no manual library configuration required**.

> **Note:** All custom libraries are included in the project folder. Standard KiCad libraries (resistors, capacitors, LEDs, etc.) use `${KICAD9_3DMODEL_DIR}` and ship with eSim/KiCad.

---

## 🔧 Design Summary

| Parameter | Value |
|-----------|-------|
| PCB Layers | 2 (F.Cu + B.Cu) |
| Board Size | Custom outline |
| Min Track Width | 0.2 mm |
| Min Clearance | 0.2 mm |
| Via Size | 0.9 mm dia / 0.5 mm drill |
| Power Track Width | 0.6 mm |
| Ground Strategy | Top & bottom ground pours |

---

## 📄 License

This project is submitted as part of the FOSSEE eSim Internship program at IIT Bombay.

---

## 🔗 Links

- [FOSSEE eSim](https://esim.fossee.in/)
- [Lattice MachXO4 Family](https://www.latticesemi.com/Products/FPGAandCPLD/MachXO4)
- [FTDI FT2232HL](https://ftdichip.com/products/ft2232hl/)
