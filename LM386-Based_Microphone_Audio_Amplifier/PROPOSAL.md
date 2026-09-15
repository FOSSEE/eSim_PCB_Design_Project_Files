# PCB Design Proposal — LM386-Based Microphone Audio Amplifier

**Submitted by:** Santhosh C (Reg. No. 24VL0052)
**Program:** B.E. Electronics Engineering — VLSI Design & Technology, Chennai Institute of Technology
**Internship:** FOSSEE eSim Semester Long Internship — IIT Bombay
**Task:** Task 7 — PCB Design using eSim

## Project Idea

This project implements the complete PCB design of an **LM386-based microphone audio amplifier**
in eSim (KiCad-based), version 2.3/2.5. The circuit amplifies the weak signal from a condenser
microphone and drives a small loudspeaker, and is based on the classic LM386 mic-amplifier
reference design (CircuitDigest).

## Basic Functionality

- A condenser microphone feeds its AC audio signal, through a DC-blocking capacitor and a 100k
  volume-control potentiometer, into the LM386's non-inverting input.
- The LM386 (U1) amplifies the signal with a gain of up to 200 (set via a 10µF capacitor across
  pins 1–8).
- The amplified output is AC-coupled through a 220µF capacitor and passed through a Zobel
  network (10k resistor + 0.05µF capacitor) for stability, before driving the loudspeaker.
- Supply and bypass decoupling capacitors (10µF each) keep the power rail clean.

## Design Flow Followed

1. Schematic capture in eSchema (LM386 IC, capacitors, resistors, potentiometer, mic/speaker/
   battery terminal blocks).
2. Footprint assignment (through-hole packages: DIP-8, radial/disc capacitors, axial resistors,
   Bourns 3296W potentiometer, Phoenix terminal blocks).
3. Sch-to-PCB update to generate the PCB layout.
4. Two-copper-layer (F.Cu/B.Cu) manual routing of all 11 nets.
5. Design Rule Check — completed with 0 errors and 0 warnings.
6. 3D visualization of the fully populated board.

Full details, screenshots, and design rationale are documented in
`Task7_PCB_Design_eSim_Report.pdf` in this repository.
