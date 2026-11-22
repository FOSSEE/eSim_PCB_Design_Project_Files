# Modular Industrial Sensor Acquisition and Control System (MISACS)
## Bill of Materials (BOM) — Screened and Verified Release

- **Project:** Modular Industrial Sensor Acquisition and Control System (MISACS)
- **Program:** FOSSEE eSim Winter Internship 2026 — Screening Task 7
- **Author / Lead Engineer:** Nikhil J
- **Hardware Status:** Frozen & Verified Bit-Identical
- **Total Electrical Components:** 70 (across 50 line items)
- **Mechanical Mounting Elements:** 4 (3.2 mm Plated M3 Mounting Holes)
- **Total Physical PCB Footprints:** 74 (70 Electrical + 4 Mechanical)

### Summary Breakdown by Reference Prefix
| Prefix | Category | Qty | Reference Designators |
| :---: | :--- | :---: | :--- |
| `C` | Capacitors | 15 | C1–C15 |
| `R` | Resistors | 19 | R1–R19 |
| `D` | Diodes & LEDs | 13 | D1–D12, D14 *(D13 skipped)* |
| `J` | Screw Terminals | 6 | J1–J6 |
| `JP` | Bus Termination Jumper | 1 | JP1 |
| `L` | Power Inductor | 1 | L1 |
| `Q` | Power MOSFETs | 2 | Q1, Q2 |
| `F` | Fuses (1 PTC + 2 Fast) | 3 | F1 (PTC), F2 (Fast), F3 (Fast) |
| `SW` | Tactile Switches | 2 | SW1 (RESET), SW2 (BOOT) |
| `U` | ICs & Active Modules | 8 | U1 (Buck), U2 (LDO), U3 (Op-Amp), U4 (ADC), U5 (ESP32), U6 (RS-485), U7 (Gate Driver), U8 (eFuse) |
| **Subtotal** | **Electrical Components** | **70** | **Exact sum: 15 + 19 + 13 + 6 + 1 + 1 + 2 + 3 + 2 + 8 = 70** |
| `H` | Mechanical Mounting Holes | 4 | H1–H4 (3.2 mm M3 drill features) |
| **Total** | **Physical PCB Footprints** | **74** | **70 Electrical + 4 Mechanical = 74 Physical Features** |

| Item | Qty | Reference | Value | Description | Footprint | Manufacturer | MPN |
| :---: | :---: | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | 1 | `J1` | `PWR_IN_24V` | Screw Terminal Block 2-Pin 5.08mm Pitch Horizontal 24V DC Main Power Input | `TerminalBlock_Phoenix:TerminalBlock_Phoenix_MKDS-1,5-2-5.08_1x02_P5.08mm_Horizontal` | Phoenix Contact | `1715721` |
| 2 | 1 | `F1` | `1.1A_PTC` | Resettable PTC Fuse 1.1A Hold / 2.2A Trip 24V SMD 1812 (Logic Rail Protection) | `Fuse:Fuse_1812_4532Metric` | Bourns | `MF-MSMF110/33X-2` |
| 3 | 1 | `D1` | `SMBJ30A` | TVS Diode Unidirectional 30V 600W SMB (Power Entry Transient Voltage Suppressor, Clamps @ 48.4V) | `Diode_SMD:D_SMB` | Littelfuse | `SMBJ30A` |
| 4 | 1 | `D2` | `SS36` | Schottky Barrier Diode 60V 3A SMC (Logic Rail Reverse Polarity Protection) | `Diode_SMD:D_SMC` | Vishay | `SS36-E3/57T` |
| 5 | 1 | `C1` | `100uF_50V` | Electrolytic Bulk Input Capacitor 100uF 50V Low-ESR SMD (8x10.5mm) | `Capacitor_SMD:CP_Elec_8x10.5` | Panasonic | `EEE-FK1H101P` |
| 6 | 1 | `C2` | `10uF_50V` | Ceramic High-Frequency Bypass Capacitor 10uF 50V X7R 1206 SMD | `Capacitor_SMD:C_1206_3216Metric` | KEMET | `C1206C106K5RAC7800` |
| 7 | 1 | `U1` | `LM2576HVS-5.0` | Step-Down Switching Voltage Regulator 5V 3A High-Voltage TO-263-5 (LM2576HVS) | `Package_TO_SOT_SMD:TO-263-5_TabPin3` | Texas Instruments | `LM2576HVS-5.0/NOPB` |
| 8 | 1 | `D8` | `SS56` | Schottky Barrier Diode 60V 5A SMC (Actuator Channel 1 Inductive Flyback Clamping Diode) | `Diode_SMD:D_SMC` | Vishay | `SS56-E3/57T` |
| 9 | 1 | `D10` | `SS56` | Schottky Barrier Diode 60V 5A SMC (Actuator Channel 2 Inductive Flyback Clamping Diode) | `Diode_SMD:D_SMC` | Vishay | `SS56-E3/57T` |
| 10 | 1 | `D12` | `SS56` | Schottky Barrier Diode 60V 5A SMC (24V-to-5V Buck Converter Fast Freewheeling Catch Diode) | `Diode_SMD:D_SMC` | Vishay | `SS56-E3/57T` |
| 11 | 1 | `D14` | `SS56` | Schottky Barrier Diode 60V 5A SMC (J1 Main 24V Power Input Reverse-Polarity Shunt Diode) | `Diode_SMD:D_SMC` | Vishay | `SS56-E3/57T` |
| 12 | 1 | `L1` | `100uH_1.7A` | Shielded Power Inductor 100uH 1.7A Saturation / RMS 180 mOhm Max DCR SMD (12.5x12.5mm, Limits 5V Rail to 1.15A Worst-Case / 1.32A Nom Continuous) | `Inductor_SMD:L_Bourns_SRR1260` | Bourns | `SRR1260-101M` |
| 13 | 1 | `C14` | `220uF_16V` | Low-ESR Bulk Output Electrolytic Capacitor 220uF 16V SMD (8x10.5mm) | `Capacitor_SMD:CP_Elec_8x10.5` | Panasonic | `EEE-FK1C221P` |
| 14 | 1 | `C3` | `10uF_16V` | High-Frequency Ceramic Output Filter Capacitor 10uF 16V X7R 0805 SMD | `Capacitor_SMD:C_0805_2012Metric` | Murata | `GRM21BR71C106KE15L` |
| 15 | 1 | `U2` | `AMS1117-3.3` | Low Dropout Linear Regulator 3.3V 1A SOT-223-3 (AMS1117-3.3) | `Package_TO_SOT_SMD:SOT-223-3_TabPin2` | Advanced Monolithic Systems | `AMS1117-3.3` |
| 16 | 1 | `C4` | `10uF_16V` | Ceramic Bulk Decoupling Capacitor 10uF 16V X7R 0805 SMD (AMS1117-3.3 Output Bulk Bypass) | `Capacitor_SMD:C_0805_2012Metric` | Murata | `GRM21BR71C106KE15L` |
| 17 | 1 | `C10` | `10uF` | Ceramic Bulk Decoupling Capacitor 10uF 16V X7R 1206 SMD (ESP32 3V3 Bulk Decoupling; Plausible static stability, dynamic Wi-Fi load stability pending prototype qualification; Case A tantalum hand-solderable for bench validation) | `Capacitor_SMD:C_1206_3216Metric` | KEMET | `C1206C106K4RACTU` |
| 18 | 8 | `C5, C6, C7, C8, C9, C11, C13, C15` | `100nF` | Ceramic Decoupling Capacitor 100nF 50V X7R 0805 SMD | `Capacitor_SMD:C_0805_2012Metric` | KEMET | `C0805C104K5RACTU` |
| 19 | 1 | `C12` | `100nF` | Ceramic Timing Capacitor 100nF 50V X7R 0805 SMD (ESP32 MCU_EN RC Reset Delay Network) | `Capacitor_SMD:C_0805_2012Metric` | KEMET | `C0805C104K5RACTU` |
| 20 | 2 | `R1, R3` | `1k` | Thick Film Resistor 1k 1% 0.125W 0805 SMD (Power LED & RC Filter) | `Resistor_SMD:R_0805_2012Metric` | Yageo | `RC0805FR-071KL` |
| 21 | 1 | `D3` | `GREEN` | SMD Indicator LED Green 0805 Clear (+3.3V Power Good Indicator) | `LED_SMD:LED_0805_2012Metric` | Lite-On | `LTST-C170KGKT` |
| 22 | 1 | `J2` | `4-20mA_IN` | Screw Terminal Block 2-Pin 5.08mm Pitch Horizontal 4-20mA Loop Input | `TerminalBlock_Phoenix:TerminalBlock_Phoenix_MKDS-1,5-2-5.08_1x02_P5.08mm_Horizontal` | Phoenix Contact | `1715721` |
| 23 | 1 | `U8` | `TPS26610DDF` | Active Current Limiter & Reverse Protection eFuse SOT-23-8 (TPS26610DDF) | `Package_TO_SOT_SMD:SOT-23-8` | Texas Instruments | `TPS26610DDFR` |
| 24 | 1 | `R2` | `100R_0.1%` | Metal Film Precision Current Shunt Resistor 100 Ohm 0.1% 0.25W 25ppm 1206 SMD | `Resistor_SMD:R_1206_3216Metric` | Susumu | `RR1220P-101-D` |
| 25 | 1 | `D4` | `SMAJ3.3A` | TVS Diode Unidirectional 3.3V 400W SMA (4-20mA Shunt Overvoltage Clamping) | `Diode_SMD:D_SMA` | Littelfuse | `SMAJ3.3A` |
| 26 | 1 | `J3` | `0-10V_IN` | Screw Terminal Block 2-Pin 5.08mm Pitch Horizontal 0-10V Sensor Input | `TerminalBlock_Phoenix:TerminalBlock_Phoenix_MKDS-1,5-2-5.08_1x02_P5.08mm_Horizontal` | Phoenix Contact | `1715721` |
| 27 | 1 | `R4` | `30k_0.1%` | Thin Film Precision Resistor 30k 0.1% 0.125W 25ppm 0805 SMD (4:1 Voltage Divider High Side) | `Resistor_SMD:R_0805_2012Metric` | Panasonic | `ERA-6AEB303V` |
| 28 | 1 | `R5` | `10k_0.1%` | Thin Film Precision Resistor 10k 0.1% 0.125W 25ppm 0805 SMD (4:1 Voltage Divider Low Side) | `Resistor_SMD:R_0805_2012Metric` | Panasonic | `ERA-6AEB103V` |
| 29 | 1 | `D5` | `BAT54S` | Dual Schottky Barrier Diode Series Pair SOT-23 (Analog Input Clamping to GND/+3.3V) | `Package_TO_SOT_SMD:SOT-23` | Diodes Inc. | `BAT54S-7-F` |
| 30 | 1 | `U3` | `LMV358` | Dual Rail-to-Rail Output Operational Amplifier SOIC-8 (LMV358) | `Package_SO:SOIC-8_3.9x4.9mm_P1.27mm` | Texas Instruments | `LMV358IDR` |
| 31 | 1 | `U4` | `ADS1115` | Ultra-Small 16-Bit Precision Delta-Sigma ADC with PGA and I2C MSOP-10 (ADS1115) | `Package_SO:MSOP-10_3x3mm_P0.5mm` | Texas Instruments | `ADS1115IDGSR` |
| 32 | 2 | `R6, R7` | `4.7k` | Thick Film Resistor 4.7k 1% 0.125W 0805 SMD (I2C Bus Pull-Ups) | `Resistor_SMD:R_0805_2012Metric` | Yageo | `RC0805FR-074K7L` |
| 33 | 1 | `U5` | `ESP32-WROOM-32` | Wi-Fi & Bluetooth MCU Module ESP32-WROOM-32 (16MB Flash, On-Board Antenna) | `RF_Module:ESP32-WROOM-32` | Espressif Systems | `ESP32-WROOM-32E-N16` |
| 34 | 2 | `SW1, SW2` | `PTS645` | Tactile Pushbutton Switch SPST-NO SMD 6x6mm (Reset and Boot Switches) | `Button_Switch_SMD:SW_SPST_PTS645` | C&K Components | `PTS645SM43SMTR92LFS` |
| 35 | 4 | `R8, R9, R15, R18` | `10k` | Thick Film Resistor 10k 1% 0.125W 0805 SMD (MCU Pull-Ups & Gate Pull-Downs) | `Resistor_SMD:R_0805_2012Metric` | Yageo | `RC0805FR-0710KL` |
| 36 | 1 | `D6` | `BLUE` | SMD Indicator LED Blue 0805 Clear (MCU Heartbeat / Status Indicator) | `LED_SMD:LED_0805_2012Metric` | Lite-On | `LTST-C170TBKT` |
| 37 | 1 | `R10` | `1k` | Thick Film Resistor 1k 1% 0.125W 0805 SMD (MCU Status LED Resistor) | `Resistor_SMD:R_0805_2012Metric` | Yageo | `RC0805FR-071KL` |
| 38 | 1 | `U6` | `MAX3485EESA` | 3.3V RS-485/RS-422 Transceiver Half-Duplex SOIC-8 Non-Isolated (MAX3485EESA+) | `Package_SO:SOIC-8_3.9x4.9mm_P1.27mm` | Analog Devices / Maxim | `MAX3485EESA+` |
| 39 | 1 | `R11` | `120R_1%` | Thick Film Resistor 120 Ohm 1% 0.125W 0805 SMD (RS-485 Differential Bus Termination) | `Resistor_SMD:R_0805_2012Metric` | Yageo | `RC0805FR-07120RL` |
| 40 | 1 | `JP1` | `TERM_ENABLE` | Pin Header 1x2 2.54mm Pitch Vertical with Jumper (RS-485 120 Ohm Bus Termination Enable) | `Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical` | Wurth Elektronik | `61300211121` |
| 41 | 2 | `R12, R13` | `390R_0.1%` | Thin Film Resistor 390 Ohm 0.1% 0.125W 25ppm 0805 SMD (RS-485 Dual-Termination Fail-Safe Biasing, Yields +235.7mV Differential Idle Across 60 Ohm Terminated Bus) | `Resistor_SMD:R_0805_2012Metric` | Yageo | `RC0805FR-07390RL` |
| 42 | 1 | `D7` | `SM712` | Asymmetrical Bidirectional TVS Diode for Extended RS-485 Common Mode (+12V/-7V) SOT-23 | `Package_TO_SOT_SMD:SOT-23` | Littelfuse | `SM712-02HTG` |
| 43 | 1 | `J4` | `RS485_BUS` | Screw Terminal Block 3-Pin 5.08mm Pitch Horizontal (RS-485 Differential Bus A, B, GND) | `TerminalBlock_Phoenix:TerminalBlock_Phoenix_MKDS-1,5-3-5.08_1x03_P5.08mm_Horizontal` | Phoenix Contact | `1715734` |
| 44 | 1 | `U7` | `UCC27524D` | Dual 5A High-Speed Low-Side Power MOSFET Gate Driver SOIC-8 (UCC27524D) | `Package_SO:SOIC-8_3.9x4.9mm_P1.27mm` | Texas Instruments | `UCC27524D` |
| 45 | 2 | `F2, F3` | `5A_FAST_FUSE` | Fast-Acting Surface Mount Fuse 5.0A 125V SMD 2410 (Actuator Rail Protection) | `Fuse:Fuse_2410_6125Metric` | Littelfuse | `0451005.MRL` |
| 46 | 2 | `R14, R17` | `10R` | Thick Film Resistor 10 Ohm 1% 0.125W 0805 SMD (MOSFET Gate Dampening Resistor) | `Resistor_SMD:R_0805_2012Metric` | Yageo | `RC0805FR-0710RL` |
| 47 | 2 | `Q1, Q2` | `IPD50N06S4L-08` | N-Channel Power MOSFET 60V 50A 8.4mOhm DPAK / TO-252 (IPD50N06S4L-08) | `Package_TO_SOT_SMD:TO-252-2` | Infineon Technologies | `IPD50N06S4L-08` |
| 48 | 2 | `D9, D11` | `YELLOW` | SMD Indicator LED Yellow 0805 Clear (Actuator Channel Output Active Indicator) | `LED_SMD:LED_0805_2012Metric` | Lite-On | `LTST-C170KSKT` |
| 49 | 2 | `R16, R19` | `2.2k` | Thick Film Resistor 2.2k 1% 0.125W 0805 (Actuator LED Current Limiter) | `Resistor_SMD:R_0805_2012Metric` | Yageo | `RC0805FR-072K2L` |
| 50 | 2 | `J5, J6` | `MKDS-1.5-2-5.08` | High-Current Screw Terminal Block 2-Pin 5.08mm Pitch Horizontal (Actuator Output Load) | `TerminalBlock_Phoenix:TerminalBlock_Phoenix_MKDS-1,5-2-5.08_1x02_P5.08mm_Horizontal` | Phoenix Contact | `1715721` |

---

### Notes & Verified Architectural Attributes
- **Q1, Q2 Power Switches:** Infineon OptiMOS-T2 `IPD50N06S4L-08` 60V 50A 8.4 mΩ in TO-252 (DPAK).
- **U7 Gate Driver:** Texas Instruments `UCC27524D` dual 5A high-speed low-side gate driver in SOIC-8. Driven directly by MCU PWM pins (non-isolated). There are no PC817 optocouplers in the design.
- **U3 Operational Amplifier:** Texas Instruments `LMV358` dual rail-to-rail op-amp in SOIC-8.
- **U4 Analog-to-Digital Converter:** Texas Instruments `ADS1115IDGS` 16-bit ΔΣ ADC in MSOP-10 (I2C address 0x48).
- **U5 Microcontroller:** Espressif Systems `ESP32-WROOM-32E-N16` 32-bit dual-core MCU module with 16MB SPI flash and on-board antenna.
- **U6 RS-485 Transceiver:** Analog Devices / Maxim `MAX3485EESA+` 3.3V half-duplex transceiver in SOIC-8. Non-isolated, protected by D7 (SM712 TVS array), with switchable 120Ω termination via JP1.
- **U8 Current-Loop Protector:** Texas Instruments `TPS26610DDF` in SOT-23-8, active current limiter and reverse-polarity protection.
- **F1 Logic Fuse:** Bourns `MF-MSMF110/33X-2` 1.1A hold / 2.2A trip resettable PTC fuse in 1812 SMD.
- **F2, F3 Actuator Fuses:** Littelfuse `0451005.MRL` 5.0A 125V fast-acting surface-mount fuses in 2410 SMD.
- **D14 Reverse Protection:** Vishay `SS56-E3/57T` 60V 5A SMC Schottky diode in reverse shunt configuration across J1 power entry.
- **Mechanical:** 4x 3.2 mm plated M3 mounting holes located at PCB corners with 4 mm setbacks.
