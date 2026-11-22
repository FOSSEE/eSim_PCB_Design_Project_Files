# Custom 2.4 GHz Ergonomic Drone RC Transmitter (2-Layer PCB)

**Submitted by:** MD Hazijul Haque  
**Internship:** FOSSEE eSim Winter Internship 2026 (Task 7)  
**Tool:** eSim (KiCad-based PCB Design Workflow)

## Overview
This project implements a handheld 2.4 GHz radio-control (RC) transmitter for quadcopters and custom UAVs using a custom gamepad-shaped 2-layer FR4 PCB (1.6 mm thick, 1 oz copper on `F.Cu` and `B.Cu`, 47 components total).

## Key Circuit & Layout Highlights
- **Power Stage:** Powered by a 2S LiPo battery (`J4`, 7.4 V nominal / 8.4 V peak) via power switch `SW5`, Schottky reverse-polarity protection `D6`, an `LM2596S-5` buck converter (`U4`) generating `+5V`, and an `AMS1117-3.3` LDO (`U5`) supplying a clean `+3V3` rail.
- **MCU & Peripherals:** `ESP32-WROOM-32E` (`U2`) paired with an `nRF24L01+PA+LNA` radio (`U1` over SPI), a `0.91"` I2C OLED telemetry display (`U3`), dual analog joysticks (`J3`, `J9`), `SW1` (Reset), `SW2` (Boot), `SW3` (3-way Flight Mode SPDT), `SW4` (Arm SPST), status LEDs (`D1`, `D2`, `D4`, `D5`), buzzer header (`J2`), and UART header (`J1`).
- **Battery Sensing & Layout:** Voltage divider `R2` (20k) / `R3` (10k) with filter capacitor `C2` scales battery voltage safely to `SENSOR_VP` (`Pin 4`) within the 3.3 V ADC limit. Buck switching components are grouped in the lower-right grip away from RF and analog lines, with antenna keep-out respected and ERC/DRC verified.
