# RP2040 Custom Development Board – PCB Design using eSim 2.6

**Author:** Divyansh Pandey
**Task:** eSim Winter Internship 2026 – Screening Task 7 (PCB Design using eSim)

## Project overview
A four-layer custom development board built around the Raspberry Pi RP2040 microcontroller, designed with eSim 2.6 (schematic capture, footprint assignment, Sch-to-PCB update, routing, DRC and 3D viewer).

Main features:
- USB Type-C input with CC resistors, input fuse and ESD protection (USBLC6-2SC6)
- Single-cell Li-ion charger and power path (BQ24075) with battery protection (BQ29700 + CSD17308Q3 MOSFETs)
- 3.3 V buck-boost regulator (TPS63070)
- Battery fuel gauge (MAX17048) with NTC thermistor connector (J3)
- 16 MB QSPI flash (W25Q128JVS) and 12 MHz crystal
- SWD debug header (J4), reset header (J7), BOOTSEL and RESET buttons, status LEDs (power-good, charging, RGB)
- 34-pin GPIO/power breakout: J5 (1x20) and J6 (1x14) = 30 GPIOs + 2 x 3V3 + 2 x GND

## Repository structure
```
RP2040_Dev_Board/
├── README.md        This file (instructions for execution)
├── Proposal/
│   └── Proposal.pdf     PCB design proposal
├── Report/
│   └── RP2040_Custom_Dev_Board_PCB_Design_Report_Divyansh_Pandey.pdf
└── Project/         Complete eSim project
    ├── RP2040_4Layer.kicad_pro
    ├── RP2040_4Layer.kicad_prl
    ├── RP2040_4Layer.kicad_pcb
    ├── RP2040_4Layer.kicad_sch          (root schematic)
    ├── 01_Power_Input.kicad_sch
    ├── 02_Battery_Charger.kicad_sch
    ├── 03_Power_Regulator.kicad_sch
    ├── 04_Battery_Monitor.kicad_sch
    ├── 05_RP2040_Core.kicad_sch
    ├── 06_QSPI_Flash.kicad_sch
    ├── 07_USB_Interface.kicad_sch
    ├── 08_Debug_Interface.kicad_sch
    ├── 09_GPIO_Headers.kicad_sch
    ├── 10_Status_LEDs.kicad_sch
    ├── 11_Battery_Protection.kicad_sch
    └── project-specific libraries (symbols, footprints, 3D models)
```

## Instructions for execution (open, verify and test)
1. Install **eSim 2.6** from https://esim.fossee.in/downloads.
2. Download this repository (green **Code** button -> **Download ZIP**) and extract it, or clone it with Git.
3. Open eSim and open the project: select `RP2040_Dev_Board/Project/RP2040_4Layer.kicad_pro`.
4. **Schematic:** open `RP2040_4Layer.kicad_sch`. The root sheet contains 11 hierarchical sheets (01 to 11).
5. **ERC:** run the Electrical Rules Checker. Expected result: 0 errors (3 warnings caused by the downloaded SnapEDA libraries).
6. **Footprints:** open the Assign Footprints tool. Every symbol is mapped to a footprint.
7. **PCB:** open the PCB editor (`RP2040_4Layer.kicad_pcb`). The board has four copper layers: F.Cu, In1.Cu, In2.Cu and B.Cu (ground).
8. **DRC:** run the Design Rules Checker. Expected result: 0 violations, 0 errors and 0 unconnected items (78 warnings caused by the SnapEDA libraries).
9. **3D view:** open the 3D Viewer from the PCB editor to inspect the assembled board.

## Project-specific libraries
Symbols/footprints for U2 (BQ24075RGT), U3 (TPS63070RNMR), U4 (MAX17048G) and Q1/Q2 (CSD17308Q3), together with 3D models for the inductor, MOSFETs and fuse, were downloaded from SnapEDA.com and added as project-specific libraries. All ERC and DRC warnings come from these libraries, not from the board connectivity.

## Verification results
| Check | Result |
|---|---|
| ERC | 0 errors, 3 warnings (library related) |
| DRC | 0 violations, 0 errors, 0 unconnected items, 78 warnings (library related) |
| Unrouted nets | 0 |
| Pads / Vias / Track segments / Nets | 341 / 169 / 1091 / 91 |

Documentation
Full design report: Report/RP2040_Custom_Dev_Board_PCB_Design_Report_Divyansh_Pandey.pdf
Design proposal: Proposal/Proposal.pdf
## Documentation
- Full design report: `Report/RP2040_Custom_Dev_Board_PCB_Design_Report_Divyansh_Pandey.pdf`
- Design proposal: `Proposal/Proposal.pdf`
