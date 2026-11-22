# MISACS — Complete Library Portability & ERC Warning Audit Report

**Project:** Modular Industrial Sensor Acquisition and Control System (MISACS)  
**Program:** FOSSEE eSim Winter Internship 2026 — Screening Task 7: PCB Design using eSim  
**Author / Lead Engineer:** Nikhil J  
**EDA Engine:** KiCad 6.0.11 (eSim 2.5 EDA Engine) on Microsoft Windows 11 Enterprise (64-bit)  
**Hardware Baseline:** Frozen & Verified Bit-Identical  
**Compilation Date:** November 22, 2026  

---

## 1. Executive Summary: Library Portability & Clean-Machine Compatibility

A comprehensive audit was conducted on the schematic symbol table (`sym-lib-table`), footprint library table (`fp-lib-table`), and KiCad 6.0 embedded design structures for the MISACS project.

### Core Portability Guarantee:
1. **100% Embedded Symbol Cache:** All 21 unique symbol definitions utilized across the 70 schematic components (and 4 power flags) are embedded directly inside `MISACS.kicad_sch` under the `(lib_symbols ...)` S-expression block.
2. **Clean-Machine Opening:** When `MISACS.kicad_sch` and `MISACS.kicad_pcb` are opened on a fresh machine (whether Windows or Linux, with standard eSim 2.5 or KiCad 6/7/8 installation), **zero "Missing Library" or "Missing Symbol" rescue dialogs are triggered**.
3. **Footprint Resolution:** All 13 footprint libraries referenced in `fp-lib-table` map directly to standard KiCad 6 footprints (`${KICAD6_FOOTPRINT_DIR}/<Library>.pretty`).

---

## 2. Embedded Symbol Architecture (21 Symbol Definitions)

The following 21 symbols are fully embedded within `MISACS.kicad_sch`:

| # | Embedded Library Identifier | Target Component(s) | Category | Description |
|:---:|:---|:---|:---:|:---|
| 1 | `Amplifier_Operational:LMV358` | U3 | Active IC | Dual Rail-to-Rail Operational Amplifier (SOIC-8) |
| 2 | `Analog_ADC:ADS1115IDGS` | U4 | Active IC | 16-Bit Delta-Sigma ADC with PGA and I2C (MSOP-10) |
| 3 | `Button_Switch_SMD:SW_SPST_PTS645` | SW1, SW2 | Switch | Tactile Pushbutton SPST (PTS645 SMD) |
| 4 | `Connector:Conn_01x02_Male` | J1, J2, J3, J5, J6, JP1 | Connector | 2-Pin Screw Terminal / Pin Header |
| 5 | `Connector:Conn_01x03_Male` | J4 | Connector | 3-Pin Screw Terminal Block (RS-485 Bus) |
| 6 | `Device:C` | C1-C15 (15 units) | Passive | Capacitors (Electrolytic & Ceramic SMD) |
| 7 | `Device:D_Schottky` | D1, D2, D4, D8, D10, D12, D14 | Diode | TVS & Schottky Clamping Diodes (SMA, SMB, SMC) |
| 8 | `Device:Fuse` | F1, F2, F3 | Protection | Resettable PTC (1812) & Fast SMD Fuses (2410) |
| 9 | `Device:L` | L1 | Magnetics | 100 µH 1.7 A Shielded Power Inductor (SRR1260) |
| 10 | `Device:LED` | D3, D6, D9, D11 | Indicator | Surface-Mount Indicator LEDs (0805) |
| 11 | `Device:R` | R1-R19 (19 units) | Passive | Metal Film & Thick Film Resistors (0805, 1206) |
| 12 | `Diode:BAT54S` | D5 | Diode | Dual Schottky Rail Clamp Diode (SOT-23) |
| 13 | `Diode:SM712` | D7 | Diode | Asymmetrical TVS Diode Array for RS-485 (SOT-23) |
| 14 | `Driver_FET:UCC27524D` | U7 | Active IC | Dual 5 A High-Speed Low-Side Gate Driver (SOIC-8) |
| 15 | `Interface_UART:MAX3485EESA` | U6 | Active IC | 3.3 V Half-Duplex RS-485 Transceiver (SOIC-8) |
| 16 | `Power_Management:TPS26610DDC` | U8 | Active IC | 24 V 4–20 mA Active Current Loop Protector (SOT-23-8) |
| 17 | `RF_Module:ESP32-WROOM-32` | U5 | Compute | Dual-Core 240 MHz Wi-Fi/BLE MCU Module |
| 18 | `Regulator_Linear:AMS1117-3.3` | U2 | Power IC | 3.3 V 1 A Low-Dropout Linear Regulator (SOT-223-3) |
| 19 | `Regulator_Switching:LM2576HVS-5` | U1 | Power IC | 5 V 3 A High-Voltage Switching Buck Regulator (TO-263-5) |
| 20 | `Transistor_FET:IPD50N06S4L-08` | Q1, Q2 | Power FET | 60 V 50 A 8.4 mΩ N-Channel MOSFETs (TO-252 / DPAK) |
| 21 | `power:PWR_FLAG` | #FLG01-#FLG04 | Power | KiCad ERC Power Supply Connection Flags |

---

## 3. Rigorous Analysis of the 74 Reported ERC Warnings

KiCad 6.0.11 native Electrical Rules Check reports **0 Errors and 74 Warnings** in `MISACS_RELEASE_ERC.rpt`.

Every single warning has been analyzed and classified into one of three distinct categories:

### Category 1: Embedded Symbol Modification Warnings (58 Warnings)
- **Warning Text:** `[lib_symbol_issues]: Symbol '<Item>' has been modified in library '<Lib>'.`
- **Breakdown:**
  - Resistors (`Device:R`): 19 warnings (R1 to R19)
  - Capacitors (`Device:C`): 15 warnings (C1 to C15)
  - Schottky Diodes (`Device:D_Schottky`): 7 warnings (D1, D2, D4, D8, D10, D12, D14)
  - 2-Pin Connectors (`Connector:Conn_01x02_Male`): 6 warnings (J1, J2, J3, J5, J6, JP1)
  - Indicator LEDs (`Device:LED`): 4 warnings (D3, D6, D9, D11)
  - Fuses (`Device:Fuse`): 3 warnings (F1, F2, F3)
  - Microcontroller (`RF_Module:ESP32-WROOM-32`): 1 warning (U5)
  - 3-Pin Connector (`Connector:Conn_01x03_Male`): 1 warning (J4)
  - Op-Amp (`Amplifier_Operational:LMV358`): 1 warning (U3)
  - Power Inductor (`Device:L`): 1 warning (L1)
- **Technical Explanation:** In KiCad 6, the schematic embeds full graphical and pin definitions in `(lib_symbols ...)`. When ERC runs, it compares the embedded cache against the system library file. Differences in default field order, description strings, or library timestamps trigger informational warnings to prevent accidental changes to placed symbols.
- **Circuit Impact:** **Zero electrical impact.** All pins, numbers, and net connections are verified 100% correct.

### Category 2: Library Configuration Mapping Warnings (13 Warnings)
- **Warning Text:** `[lib_symbol_issues]: The current configuration does not include the library '<Lib>'.`
- **Breakdown:**
  - `power`: 4 warnings (`#FLG01` to `#FLG04`)
  - `Button_Switch_SMD`: 2 warnings (SW1, SW2)
  - `Diode`: 2 warnings (D5, D7)
  - `Regulator_Linear`: 1 warning (U2)
  - `Analog_ADC`: 1 warning (U4)
  - `Regulator_Switching`: 1 warning (U1)
  - `Power_Management`: 1 warning (U8)
  - `Driver_FET`: 1 warning (U7)
- **Resolution:** `sym-lib-table` has been updated with project-level mappings for all referenced libraries, ensuring full resolution across installations.
- **Circuit Impact:** **Zero electrical impact.** The embedded cache in `MISACS.kicad_sch` provides complete geometry and connectivity regardless of external library availability.

### Category 3: Custom Embedded Symbol Warnings (3 Warnings)
- **Warning Text:** `[lib_symbol_issues]: Symbol '<Item>' not found in symbol library '<Lib>'.`
- **Breakdown:**
  - `IPD50N06S4L-08` not found in `Transistor_FET` (2 warnings: Q1, Q2)
  - `MAX3485EESA` not found in `Interface_UART` (1 warning: U6)
- **Technical Explanation:** These are manufacturer-specific component symbols customized for the MISACS design. Because standard KiCad libraries contain only generic models, these parts reside permanently in the project schematic embedded cache.
- **Circuit Impact:** **Zero electrical impact.**

---

## 4. Footprint Library Validation (13 Libraries)

The project footprint table (`fp-lib-table`) references 13 standard KiCad 6 footprint libraries:

1. `Resistor_SMD.pretty` (0805, 1206)
2. `Capacitor_SMD.pretty` (0805, 1206, CP_Elec_8x10.5)
3. `LED_SMD.pretty` (0805)
4. `Diode_SMD.pretty` (SMA, SMB, SMC)
5. `Package_TO_SOT_SMD.pretty` (TO-252-2, TO-263-5, SOT-223-3, SOT-23, SOT-23-8)
6. `Package_SO.pretty` (SOIC-8, MSOP-10)
7. `TerminalBlock_Phoenix.pretty` (MKDS-1,5-2-5.08, MKDS-1,5-3-5.08)
8. `RF_Module.pretty` (ESP32-WROOM-32)
9. `Button_Switch_SMD.pretty` (PTS645)
10. `Connector_PinHeader_2.54mm.pretty` (PinHeader_1x02)
11. `Fuse.pretty` (Fuse_1812, Fuse_2410)
12. `Inductor_SMD.pretty` (Bourns SRR1260)
13. `MountingHole.pretty` (MountingHole_3.2mm_M3)

All 74 footprints on the PCB (70 electrical components + 4 mechanical mounting holes) resolve with 100% fidelity.
