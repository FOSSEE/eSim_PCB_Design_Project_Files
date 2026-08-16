<div align="center">
Flight Controller PCB

**A 4-layer STM32F446-based flight controller board for UAV / drone applications**

</div>

---

## Overview

This repository contains the full hardware design for a custom **4-layer flight controller PCB** built around the **STM32F446RE** (ARM Cortex-M4) microcontroller. It integrates a 9-axis IMU, barometer, six PWM servo/ESC outputs, CAN, dual SPI, triple UART, USB, and a filtered analog input — everything needed for a self-contained drone / RC flight control board.

Designed in **eSim 2.5**, all schematic, PCB layout, and manufacturing source files are included.

---

## Features

-  **STM32F446RETx** — ARM Cortex-M4 with FPU, LQFP64 package
-  **ICM-20948** 9-axis IMU (accelerometer + gyroscope + magnetometer)
-  **BMP280** barometric pressure sensor
-  **6× PWM outputs** for ESCs / servos (TIM1 & TIM2 channels)
-  **2× ESC signal inputs** on the raw power rail
-  **3× UART**, **2× SPI**, **CAN bus**, and **I²C** breakouts
-  Onboard **3.3 V regulation** with reverse-polarity & overcurrent protection
-  **USB** interface for configuration / firmware updates
-  Filtered **ADC input** (RC low-pass, 15.9 kHz cutoff)
-  **SWD** debug/programming header
-  Boot-select and reset push-buttons

---


##  Hardware Summary

| Subsystem | Details |
|---|---|
| **MCU** | STM32F446RETx, Cortex-M4, LQFP64, external 8 MHz HSE crystal |
| **Power** | Schottky-protected input → 3.3 V LDO/switcher regulator, in-line fuse, power-good LED |
| **IMU** | ICM-20948 over I²C1 (addr `0x68`/`0x69`) |
| **Barometer** | BMP280 over I²C3 (addr `0x76`/`0x77`) |
| **PWM Outputs** | SERVO_1 – SERVO_6 (TIM1_CH1-4, TIM2_CH2-4) |
| **ESC Inputs** | J1, J2 — 3-pin headers on raw battery rail |
| **Comms** | USART1/2/3, SPI1/2, CAN1, I²C1/3/4 breakouts |
| **USB** | USB-C style connector, native USB_D+/D− to MCU |
| **Debug** | SWD header (SWDIO, SWDCLK, NRST, 3V3, GND) |
| **Analog** | ADC1_IN0/IN1 with RC low-pass filtering |

---

