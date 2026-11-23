# STM32F407-MVCU

**A 4-layer STM32F407-based Master Control Unit board**, designed in KiCad as part of the FOSSEE Internship.



## Overview

The STM32F407-MVCU is the master board of a distributed control system. Built around the **STM32F407 (ARM Cortex-M4F)** microcontroller, it talks to five slave control boards over **CAN bus** (DB9 connectors), connects to an inertial navigation system (INS) over **RS-232**, and provides wireless, storage, user-interface and debug interfaces on one PCB.



## Key Features

| Feature | Description |
|---|---|
| Microcontroller | STM32F407 (Cortex-M4F with FPU, LQFP) |
| Stack-up | 4 layers: Top (signal) / Inner 1 (GND) / Inner 2 (power) / Bottom (signal) |
| Input supply | 9–36 V DC via DC-DC module, split into 5 V and 3.3 V rails |
| CAN | 5 × DB9 ports to slave boards, with reserved GPIOs |
| RS-232 | DB9 port with level converter (INS link) |
| Wireless | XBee-format RF module socket with ASSO and RSSI LEDs |
| Storage | SD card slot |
| User interface | 7-segment display, 10 user LEDs (A–J), 5 V / 3.3 V power LEDs |
| Debug / programming | 5-pin SWD header, BOOT0 jumper, reset switch |
| Breakouts | UART, SPI, I2C, ADC, DAC |

## Main Headers and Jumpers

| Ref. | Label | Function |
|---|---|---|
| J1 | BOOT0 | Boot from user flash (0) or system bootloader (1) |
| J5 | – | Main power input screw terminal |
| J10 | UART_2 | Second UART breakout |
| J13 | SWDIO / SWO / GND / SWCLK / 3V3 | SWD programming and debug |
| J14 | SPI_2 | Second SPI breakout |
| J15 | SDA1 / SCL1 | I2C breakout |
| J17 | i/p, 5V, 3V3 | Supply source selection |
| J18 | Main_PWR | Connect / isolate main power |

## Design Summary

- **Tool:** KiCad (schematic editor, footprint assignment, PCB editor, 3D viewer)
- **Power:** screw terminal (J5) → DC-DC module (U7) → 5 V regulator (U6) and 3.3 V regulator (U4)
- **Routing order:** power → clock → CAN differential pairs → SDIO/SPI/UART buses → general signals → copper pours and via stitching
- **Design rules:** min track 0.2 mm, min clearance 0.2 mm, via 0.6 / 0.3 mm, annular ring 0.15 mm, hole-to-hole 0.25 mm, edge clearance 0.3 mm
- **DRC result:** 0 errors, 0 unconnected items

## Bring-Up Plan

1. Visual inspection and continuity check (supply rails vs. GND).
2. Power up with a current-limited supply; verify 5 V and 3.3 V rails and power LEDs.
3. Connect an ST-Link to J13 and confirm the MCU is detected.
4. Flash a test program (blink LEDs, drive the 7-segment display).
5. Test UART, SPI, I2C, SD card and RF module one at a time.
6. Test CAN with a second node over a DB9 cable.
7. Test RS-232 with a serial terminal or the INS.

## Future Improvements

- ESD and surge protection on DB9 connectors and the power input
- Reverse-polarity protection and an input fuse
- Jumper- or switch-selectable CAN termination
- Signal-integrity and thermal analysis of the power stage
- Extra test points (CAN lines, clock)

## Repository Contents

```
.
├── README.md
├── images/                 # Renders and diagrams used in this README
├── <KiCad project files>   # .kicad_pro, .kicad_sch, .kicad_pcb
└── STM32F407-MVCU_PCB_Design_Report.docx
```

> Adjust the file list above to match the actual files in your repository.

## Opening the Project

1. Install [KiCad](https://www.kicad.org/).
2. Clone this repository.
3. Open the `.kicad_pro` file in KiCad.

## References

1. STMicroelectronics, *STM32F405xx / STM32F407xx Datasheet*
2. STMicroelectronics, *RM0090 Reference Manual*
3. ISO 11898-2, *Road vehicles – Controller area network (CAN) – High-speed physical layer*
4. KiCad Documentation, kicad.org

## Author

**Jasmine Kaur**
B.Tech, Electronics and Communication Engineering
SRM Institute of Science and Technology, Chennai
FOSSEE Internship

