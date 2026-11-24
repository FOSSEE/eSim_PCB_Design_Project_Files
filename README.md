# ESP32-Based Silent SOS and Emergency Alert System

## 1. Project Overview

The Silent SOS is an ESP32-based emergency alert system designed to help users send emergency notifications when they are in a potentially dangerous situation.

The system uses an MPU6050 motion sensor to detect abnormal movement. When a possible emergency is detected, the system provides a 5-second cancellation period. If the user does not cancel the alert, an emergency notification is triggered.

The project uses Wi-Fi connectivity to send alerts through Firebase and Telegram.

## 2. Project Objectives

- Design a compact PCB for the Silent SOS system.
- Interface the MPU6050 motion sensor with the ESP32.
- Detect potential emergency situations using motion data.
- Provide a 5-second cancellation period before sending an alert.
- Send emergency notifications using Wi-Fi connectivity.

## 3. Hardware Components

| Component | Purpose |
|---|---|
| ESP32 DevKit V1 | Main microcontroller |
| MPU6050 | Motion and orientation detection |
| BC547 transistor | Switching circuit |
| Supporting components | Circuit interfacing and protection |

## 4. System Working

The system operates in three different states:

1. **SAFE:** Normal operating condition.
2. **ARMED:** Emergency detection is enabled.
3. **DANGER:** A potential emergency is detected.

### Emergency Alert Process

1. The MPU6050 continuously provides motion data.
2. The ESP32 processes the sensor readings.
3. When a potential emergency is detected, the system enters the DANGER state.
4. A 5-second cancellation period is provided.
5. If the alert is not cancelled, an emergency notification is sent through Firebase and Telegram.
6. The user's location is obtained through the connected smartphone's GPS.

## 5. PCB Design

The PCB is designed using **KiCad**.

The design integrates the ESP32 interface, motion sensor connections, and supporting electronic circuitry into a compact board.

### PCB Design Files

| File | Description |
|---|---|
| `SOS.kicad_pro` | KiCad project file |
| `SOS.kicad_sch` | Circuit schematic |
| `SOS.kicad_pcb` | PCB layout |
| `SOS.proj` | Supporting project file |

## 6. Software and Tools

- KiCad – Schematic and PCB design
- Arduino IDE – ESP32 programming
- Firebase – Emergency alert integration
- Telegram Bot API – Emergency notifications

## 7. Applications

- Personal emergency assistance
- Women's safety applications
- Emergency notification systems
- Personal safety monitoring

## 8. Project Repository

This repository contains the PCB design files and supporting documentation developed for the eSim Semester Long Internship – Autumn 2026, Submission Task 7.

## 9. Author

**Kaushik N.**  
Department of Electronics and Communication Engineering  
Chennai Institute of Technology

---

**Project:** ESP32-Based Silent SOS and Emergency Alert System  
**Internship:** eSim Semester Long Internship – Autumn 2026
