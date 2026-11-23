# ATmega328P Environment Monitor (eSim 2.5 PCB Project)

A 2-layer PCB design for a small environment-monitoring board built around an **ATmega328P (ATMEGA328P-AU, TQFP-32)**. The board reads temperature/humidity (DHT11) and ambient light (LDR), shows data on an I2C OLED, gives feedback through three status LEDs and a buzzer, and can be programmed over ICSP or a UART header.

- **Author:** Mohnish Sathiamurthy, Dept. of ECE, Chennai Institute of Technology
- **Tool:** eSim 2.5 (Eeschema / Pcbnew, KiCad 6.0 file format)
- **Board:** 2 layers, [100 x 80] mm, GND copper pour on the bottom layer
- **Status:** schematic complete, layout complete, DRC: [fill in result, e.g. 0 errors / 0 unconnected]

> Items in `[square brackets]` are values to confirm or fill in from your final design before submission.

---

## 1. Features

| Function | Implementation |
|---|---|
| Processing | ATmega328P-AU, 16 MHz crystal, 5 V |
| Power input | DC barrel jack, reverse-polarity diode, L7805 (5 V), AMS1117-3.3 (3.3 V) |
| Programming | 6-pin ICSP header, 4-pin UART header |
| Sensing | DHT11 (temperature/humidity) header, LDR light divider on ADC0 |
| Display | 4-pin I2C OLED header (3.3 V, with 4.7 kOhm pull-ups) |
| Indicators | 3 status LEDs (330 Ohm), buzzer driven by BC547 with flyback diode |
| Mechanical | 4 x M3 mounting holes, connectors placed on the board edges |

## 2. Circuit description

**Power.** The jack (J1) feeds D1 (1N4007, reverse-polarity protection) to the `VIN` rail. U1 (L7805) generates the 5 V `VCC` rail (C1 0.33 uF in, C2 0.1 uF out). U2 (AMS1117-3.3) takes `VCC` and generates `+3V3` for the OLED (C3 10 uF in, C4 22 uF out).

**Microcontroller.** U3 is powered from `VCC` on VCC and AVCC pins, each decoupled with 100 nF (C5, C6, C7). AREF is decoupled with C8 (100 nF). All GND pins connect to the ground plane.

**Clock and reset.** Y1 (16 MHz) with C9/C10 (22 pF) sits on XTAL1/XTAL2. RESET is pulled up by R1 (10 kOhm) with SW1 to ground, and is also brought to the ICSP header.

**Sensors.** The DHT11 data line (PD2) has a 10 kOhm pull-up (R2). The LDR (J6) forms a divider with R3 (10 kOhm); the midpoint `LDR_OUT` goes to PC0 (ADC0).

**Display.** The OLED header (J5) uses PC4 (SDA) and PC5 (SCL) with 4.7 kOhm pull-ups (R4, R5) to 3.3 V.

**Outputs.** PD4/PD5/PD6 drive LEDs D2-D4 through 330 Ohm resistors (R6-R8). PD7 drives Q1 (BC547) through R9 (1 kOhm); BZ1 sits between `VCC` and the collector with D5 (1N4148) as a flyback diode.

## 3. MCU pin assignment

| Pin | Name | Net | Use |
|---|---|---|---|
| 2 | PD4 | LED1 | Status LED 1 |
| 9 | PD5 | LED2 | Status LED 2 |
| 10 | PD6 | LED3 | Status LED 3 |
| 11 | PD7 | BUZ | Buzzer driver |
| 15 | PB3 | MOSI | ICSP |
| 16 | PB4 | MISO | ICSP |
| 17 | PB5 | SCK | ICSP |
| 7 / 8 | PB6 / PB7 | XTAL1 / XTAL2 | 16 MHz crystal |
| 23 | PC0 | LDR_OUT | Light sensor (ADC0) |
| 27 | PC4 | SDA | OLED (I2C) |
| 28 | PC5 | SCL | OLED (I2C) |
| 29 | PC6 | RESET | Reset / ICSP |
| 30 | PD0 | UART_RX | UART header |
| 31 | PD1 | UART_TX | UART header |
| 32 | PD2 | DHT_DATA | DHT11 data |
| 4, 6, 18 | VCC, VCC, AVCC | VCC | 5 V supply |
| 3, 5, 21 | GND | GND | Ground |
| 20 | AREF | AREF | Decoupled with C8 |
| 1, 12, 13, 14, 19, 22, 24, 25, 26 | - | - | Unused (no-connect) |

## 4. Connectors (board edge)

| Ref | Function | Pins |
|---|---|---|
| J1 | DC power jack | 1 = tip (+), 2 = sleeve (GND), MP = shield |
| J2 | ICSP (2x3) | 1 MISO, 2 VCC, 3 SCK, 4 MOSI, 5 RESET, 6 GND |
| J3 | UART (1x4) | 1 GND, 2 VCC, 3 UART_TX, 4 UART_RX |
| J4 | DHT11 (1x3) | 1 VCC, 2 DATA, 3 GND |
| J5 | OLED I2C (1x4) | 1 GND, 2 +3V3, 3 SCL, 4 SDA |
| J6 | LDR (1x2) | 1 VCC, 2 LDR_OUT |

Connect the UART header to a USB-serial adapter as: adapter RX to J3 pin 3, adapter TX to J3 pin 4, GND to GND. Use 5 V logic levels.

## 5. Bill of materials

| Ref | Value | Footprint |
|---|---|---|
| U3 | ATMEGA328P-AU | TQFP-32_7x7mm_P0.8mm |
| U1 | L7805 | TO-220-3_Vertical |
| U2 | AMS1117-3.3 | SOT-223-3_TabPin2 |
| Q1 | BC547 | TO-92_Inline |
| D1 | 1N4007 | D_DO-41_SOD81_P10.16mm_Horizontal |
| D5 | 1N4148 | D_DO-35_SOD27_P7.62mm_Horizontal |
| D2-D4 | LED | LED_0805_2012Metric |
| Y1 | 16 MHz | Crystal_HC49-4H_Vertical |
| SW1 | Reset switch | SW_PUSH_6mm |
| BZ1 | Buzzer | Buzzer_12x9.5RM7.6 |
| R1-R3 | 10 kOhm | R_0805_2012Metric |
| R4, R5 | 4.7 kOhm | R_0805_2012Metric |
| R6-R8 | 330 Ohm | R_0805_2012Metric |
| R9 | 1 kOhm | R_0805_2012Metric |
| C1 | 0.33 uF | C_0805_2012Metric |
| C2 | 0.1 uF | C_0805_2012Metric |
| C3 | 10 uF | C_0805_2012Metric |
| C4 | 22 uF | C_0805_2012Metric |
| C5-C8 | 100 nF | C_0805_2012Metric |
| C9, C10 | 22 pF | C_0805_2012Metric |
| J1 | DC jack | BarrelJack_CUI_PJ-063AH_Horizontal |
| J2 | ICSP | PinHeader_2x03_P2.54mm_Vertical |
| J3, J5 | 1x4 header | PinHeader_1x04_P2.54mm_Vertical |
| J4 | 1x3 header | PinHeader_1x03_P2.54mm_Vertical |
| J6 | 1x2 header | PinHeader_1x02_P2.54mm_Vertical |
| H1-H4 | M3 hole | MountingHole_3.2mm_M3 |

[Update this table if you changed any value or footprint during layout.]

## 6. PCB design notes

- **Stack-up:** 2 layers (F.Cu, B.Cu). Bottom layer is a filled GND zone; refill with `B` after any change.
- **Track widths:** [signal 0.25 mm / power 0.5-1.0 mm. Replace with the values you used.]
- **Placement:** the crystal and its load capacitors are next to pins 7 and 8; decoupling capacitors sit next to the VCC, AVCC and AREF pins; the regulators are near the DC jack.
- **Edge connectors:** J1 to J6 and the mounting holes are at the board edges. J1's plug opening faces outward.
- **Routing:** power first with wider tracks, then signals, avoiding 90 degree corners; crystal traces kept short.
- **Silkscreen:** reference designators, connector pin 1 markers and a board title.

## 7. Verification

| Check | Result |
|---|---|
| ERC (schematic) | [fill in, e.g. 0 errors] |
| DRC (layout) | [fill in, e.g. 0 errors, 0 unconnected items] |
| All symbols have footprints | [yes / no] |
| 3D viewer reviewed (top, bottom, isometric) | [yes / no] |
| Reopened in a fresh eSim 2.5 install | [yes / no] |

## 7a. Known limitations

- The AMS1117-3.3 regulator can be unstable with low-ESR ceramic output capacitors; a tantalum or electrolytic 22 uF is recommended on a built board.
- The 5 V MCU reads the OLED bus through 3.3 V pull-ups; this works with the AVR input thresholds, but keep the AVR internal pull-ups on SDA/SCL disabled.
- The DHT11 is slow and low-accuracy; it is used here as a simple sensor example.
- [Add anything else you noticed: clearances, parts you would change, etc.]

## 8. Project structure

```
environment/
├── environment.kicad_pro      project settings
├── environment.kicad_sch      schematic
├── environment.kicad_pcb      PCB layout
├── environment.kicad_prl      local project state
├── sym-lib-table              project symbol libraries
├── fp-lib-table               project footprint library (esim_fp)
├── README.md                  this file
├── report/                    PDF report and screenshots
└── lib/
    ├── symbols/               project symbol libraries
    ├── footprints.pretty/     footprints used on the board
    └── 3d/                    3D models (.wrl)
```

All libraries are inside the project folder and referenced with relative paths (`${KIPRJMOD}`), so the project opens in eSim 2.3 / 2.5 without importing anything.

## 9. How to open the project

1. Copy the whole `environment` folder to your eSim workspace.
2. Open eSim, then open the project, then open **Eeschema** and **Pcbnew** from the toolbar.
3. If a library is reported missing: **Preferences, Manage Symbol Libraries / Manage Footprint Libraries, Project Specific Libraries**, and confirm the paths start with `${KIPRJMOD}/lib/`.
4. In Eeschema run **Inspect, Electrical Rules Checker**. In Pcbnew run **Inspect, Design Rules Checker**.

