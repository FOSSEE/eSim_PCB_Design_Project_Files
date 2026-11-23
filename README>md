# Industrial Sensor Monitor PCB

A two-channel industrial sensor monitoring system designed using **eSim and KiCad** as part of the FOSSEE eSim Semester Long Internship, Autumn 2026, Task 7.

The PCB is designed to interface with two independent analogue sensors, compare their input voltages against predefined reference levels and provide visual and external alarm indications.

## Project Overview

The Industrial Sensor Monitor is designed to monitor two analogue sensor inputs in the range of 0–5 V.

The circuit uses an LM393 dual comparator to monitor the sensor signals. A regulated 5 V supply is generated from a 12 V DC input using an LM7805 voltage regulator.

Each channel has its own reference voltage network and indicator output. The PCB also provides an external connector for an alarm interface.

## Key Features

- Two independent 0–5 V analogue sensor inputs
- LM393 dual comparator for threshold detection
- LM7805-based 12 V to 5 V voltage regulation
- Individual LED status indicators
- Reference voltage generation using resistor dividers
- External alarm output connector
- Two-layer PCB design
- Manually routed copper tracks
- GND copper zone on the bottom layer

## Circuit Architecture

The circuit is divided into four main sections.

### 1. Power Supply

A 12 V DC input is provided through connector J1. The LM7805 voltage regulator converts this input into a nominal 5 V supply for the comparator and other circuit sections.

The capacitors C1, C2 and C3 are included in the power supply section for filtering and decoupling.

### 2. Sensor Input Section

Two independent analogue sensor signals are connected through J2 and J3.

Each input is connected to the comparator circuit for threshold monitoring.

### 3. Comparator and Reference Section

An LM393 dual comparator is used to process both sensor channels.

Two resistor divider networks generate the reference voltages:

- R1 = 10 kΩ and R2 = 15 kΩ
- R3 = 10 kΩ and R4 = 15 kΩ

With a 5 V supply, each divider provides a nominal reference voltage of approximately 3 V.

### 4. Indicator and Alarm Section

D1 and D2 provide visual status indication for the two channels. R7 and R8 are used as LED current-limiting resistors.

The output section also includes signal diodes and connector J4 for an external alarm interface.

## Main Components

| Component | Description |
|---|---|
| LM7805 | 5 V voltage regulator |
| LM393 | Dual comparator |
| R1, R3 | 10 kΩ resistors |
| R2, R4 | 15 kΩ resistors |
| R5, R6 | 10 kΩ resistors |
| R7, R8 | 1 kΩ resistors |
| R9 | 10 kΩ resistor |
| D1, D2 | Indicator LEDs |
| D3, D4 | Signal diodes |
| C1 | 330 nF capacitor |
| C2 | 100 nF capacitor |
| C3 | 10 µF capacitor |

## PCB Design

The PCB was developed as a two-layer board using KiCad through the eSim design workflow.

The component placement is organised around the power supply, sensor input, comparator and output sections.

The connectors are positioned around the board edges to provide convenient access for external connections.

The routing was completed manually using both copper layers. A GND copper zone was added on the bottom copper layer to provide a common ground return.

The board outline is defined using the Edge.Cuts layer.

## Design Verification

The following design checks were completed:

- Electrical Rule Check (ERC): Zero errors and zero warnings reported.
- Design Rule Check (DRC): Zero violations reported.
- Schematic-to-PCB parity check: Zero violations reported.
- Unconnected items: Zero reported.

## Project Screenshots

### Circuit Schematic

The complete circuit schematic showing the power supply, sensor inputs, comparator, reference networks and output connections.

### PCB Layout

The two-layer PCB layout showing component placement, copper routing and the ground zone.

### 3D Board View

The PCB viewed through the KiCad 3D Viewer.

## Software and Tools

- eSim 2.5
- KiCad
- GitHub

## Repository Contents

This repository contains the PCB design proposal, final project report, circuit schematic, PCB layout and supporting project files.

The complete project workspace is included to make the design easier to review and open in the supported eSim/KiCad environment.

## Project Information

**Project:** Industrial Sensor Monitor PCB

**Program:** FOSSEE eSim Semester Long Internship

**Season:** Autumn 2026

**Task:** Task 7

**Design Software:** eSim 2.5 / KiCad

---

Developed as part of the FOSSEE eSim Semester Long Internship, Autumn 2026.
