# PCB Design Proposal — 555 Timer Based Servo Motor PWM Controller

**Submitted by:** Sridhar (Reg. No. 24VL0054)
**Program:** B.E. Electronics Engineering — VLSI Design & Technology, Chennai Institute of Technology
**Internship:** FOSSEE eSim Semester Long Internship — IIT Bombay
**Task:** Task 7 — PCB Design using eSim

## Project Idea

This project implements the complete PCB design of a **555 Timer based Servo Motor PWM
Controller** in eSim (KiCad-based), version 2.3/2.5. The circuit uses the NE555/LM555 timer IC
as an astable multivibrator with an adjustable duty cycle, generating a pulse-width-modulated
output that can drive a servo motor, small motor driver, or similar load — without needing a
microcontroller.

## Basic Functionality

- The 555 timer (X1) is configured as an astable multivibrator: resistor R1 (10k) charges
  timing capacitor C1 (0.1uF) from VCC through the DISCHARGE pin, while resistor R2 (220k),
  potentiometer R3 (47k) and steering diode D1 form an independently adjustable discharge path.
- Turning potentiometer R3 changes the relative charge/discharge time constants, letting the
  output duty cycle (pulse width) be tuned by hand — effectively a manual PWM generator.
- The OUT pin (pin 3) drives a 3-pin header (J1: VCC, OUT, GND) intended for connection to a
  servo motor or motor driver.
- A 2-pin terminal block (J2, +Bat−) accepts the DC battery/supply input for the board.

## Design Flow Followed

1. Schematic capture in eSchema (LM555N timer, R1/R2 resistors, R3 potentiometer, D1 diode,
   C1 timing capacitor, output header J1, battery terminal block J2).
2. Footprint assignment (through-hole packages: DIP-8, axial resistors, Bourns 3296W
   potentiometer, DO-41 diode, 2.54 mm pin header, Phoenix terminal block).
3. Sch-to-PCB update to generate the PCB layout.
4. Two-copper-layer (F.Cu/B.Cu) manual routing of all 8 nets.
5. Design Rule Check — completed with 0 errors and 0 warnings.
6. 3D visualization of the fully populated board.

Full details, screenshots, and design rationale are documented in
`Task7_PCB_Design_eSim_Report.pdf` in this repository.
