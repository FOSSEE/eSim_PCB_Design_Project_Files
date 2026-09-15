# Battery Low Voltage Cut-Off Circuit Using Transistor

## Project Overview

This project presents the design of a **Battery Low Voltage Cut-Off Circuit Using Transistor**. The circuit continuously monitors the battery voltage through a resistor-divider sensing network and automatically disconnects the load when the battery voltage falls below a preset threshold.

A transistor-based threshold sensing stage controls a MOSFET, which performs the actual load disconnection. An LED provides an indication of the load-connected condition.

## Key Features

* Battery low-voltage detection
* Automatic load disconnection
* Transistor-based threshold sensing
* MOSFET-based load switching
* LED status indication
* Hysteresis to reduce switching chatter near the threshold
* Manual ON/OFF control
* Two-layer THT PCB design

## Circuit Blocks

The circuit consists of the following major sections:

1. **Voltage Sensing** – R1 and R2 form a voltage divider to sense the battery voltage.
2. **Threshold Detection** – Q1 acts as the transistor-based voltage threshold element.
3. **Hysteresis** – R4 provides feedback to help prevent rapid switching near the threshold.
4. **Gate Driver** – Q2 drives the MOSFET gate.
5. **Load Disconnect** – Q3 is the power MOSFET used to disconnect the load.
6. **Status Indicator** – LED1 and R7 indicate the load-connected condition.
7. **Filtering** – C1 reduces noise at the sensing node.
8. **Manual Control** – SW1 provides manual battery input ON/OFF control.

## Main Components

| Reference | Component          | Value / Type             |
| --------- | ------------------ | ------------------------ |
| R1        | Resistor           | 10 kΩ                    |
| R2        | Resistor           | 10 kΩ                    |
| R3        | Resistor           | 10 kΩ                    |
| R4        | Resistor           | 100 kΩ                   |
| R5        | Resistor           | 4.7 kΩ                   |
| R6        | Resistor           | 10 kΩ                    |
| R7        | Resistor           | 1 kΩ                     |
| Q1        | NPN Transistor     | Small-signal             |
| Q2        | NPN Transistor     | Small-signal             |
| Q3        | N-MOSFET           | Logic-level              |
| D1        | LED                | Green                    |
| D2        | Protection Diode   | As selected in schematic |
| C1        | Capacitor          | 1 µF                     |
| SW1       | Switch             | SPST                     |
| J1        | Battery Connection | 2-pin                    |
| J2        | Load Connection    | 2-pin                    |

## PCB Design

The PCB is designed as a **two-layer board** using through-hole components. The sensing section is kept separate from the high-current battery/load path. Wider traces are used for the power path, while narrower traces are used for signal and control connections.

The PCB design includes:

* Front copper layer (F.Cu)
* Bottom copper layer (B.Cu)
* Through-hole components
* Ground return/ground zone
* Short MOSFET gate-drive connection
* Wider battery/load traces
* Board outline on the Edge.Cuts layer

## Project Files

This folder contains the eSim/KiCad project files required to open and continue the design:

* Schematic file (`.kicad_sch`)
* PCB layout file (`.kicad_pcb`)
* Project file (`.kicad_pro`)
* Supporting documentation
* PCB design screenshots and verification files

## Verification

The design is checked using:

* Electrical Rules Check (ERC)
* Design Rules Check (DRC)
* PCB layout inspection
* 3D PCB viewer

## Applications

A low-voltage cut-off stage is useful in battery-powered systems where excessive battery discharge needs to be prevented. Possible applications include:

* Portable electronic devices
* Battery-powered systems
* Solar power systems
* UPS/backup systems
* Battery management and protection stages

## Project Objective

The objective of this project is to design and document a simple, practical battery low-voltage protection circuit and implement it as a complete PCB using eSim/KiCad.

## Tools Used

* eSim
* eSchema
* KiCad PCB Editor / Pcbnew
* ngspice (for simulation, where applicable)

**eSim Semester Long Internship – Autumn 2026**
**Submission Task 7**
