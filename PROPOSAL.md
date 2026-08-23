# PCB Design Proposal — Battery Over/Under-Voltage Window Comparator

**Submitted by:** Krisanth M (Reg. No. 24VL0027)
**Program:** B.E. Electronics Engineering — VLSI Design \& Technology, Chennai Institute of Technology
**Internship:** FOSSEE eSim Semester Long Internship — IIT Bombay
**Task:** Task 7 — PCB Design using eSim

## Project Idea

This project implements the complete PCB design of a **Battery Over/Under-Voltage Window
Comparator** in eSim (KiCad-based), version 2.3/2.5. The circuit uses two LM741 operational
amplifiers as open-loop voltage comparators to continuously monitor a battery's terminal
voltage and flag both under-voltage (deep-discharge) and over-voltage (over-charge) conditions
in real time — a hardware-only building block relevant to battery management systems (BMS) in
electric vehicles, solar storage, and portable devices.

## Basic Functionality

* A three-resistor reference ladder (R1: 4.7k, R2: 3.3k, R3: 2.2k) divides the 12 V supply
rail to generate a fixed upper threshold (\~6.47 V) and lower threshold (\~2.59 V).
* A 1:1 precision divider (R4, R5: 10k each) scales the battery-under-test voltage down by
50%, so the safe operating window corresponds to roughly 5.18 V–12.94 V at the battery.
* Comparator U1 compares the scaled battery voltage against the lower threshold and drives
LED 1 (via current-limiting resistor R6) ON when the battery is under-voltage.
* Comparator U2 compares the scaled battery voltage against the upper threshold and drives
LED 2 (via current-limiting resistor R7) ON when the battery is over-voltage.
* Both LEDs stay OFF while the battery sits within its safe, nominal window.
* A 100 nF decoupling capacitor (C1) is placed across the supply rails to suppress transient
noise, and 2-pin headers (V1, V2) bring in the battery-under-test and +12 V supply inputs.

## Design Flow Followed

1. Schematic capture in Eeschema (LM741 comparators U1/U2, reference ladder R1–R3, sense
divider R4/R5, current-limiting resistors R6/R7, LEDs D1/D2, decoupling capacitor C1,
battery/supply input headers V1/V2), followed by an Electrical Rules Check (ERC).
2. Ngspice transient simulation of the netlist, using the LM741 SPICE subcircuit model
(lm741.sub), to verify comparator switching against the calculated threshold voltages.
3. Footprint assignment (through-hole packages: DIP-8 for both op-amps, axial resistors,
5 mm THT LEDs, disc-ceramic capacitor, 2.54 mm straight pin headers).
4. Sch-to-PCB update to generate the PCB layout.
5. Two-copper-layer (F.Cu/B.Cu) manual routing of all nets, with 45° mitred tracks at
0.250 mm width.
6. Design Rule Check — completed with 0 errors and 0 clearance violations, 20/20 connections.
7. 3D visualization of the fully populated board (top and bottom views).

Full details, screenshots, and design rationale are documented in
`Task7\_PCB\_Design\_eSim\_Report.docx` in this repository.

