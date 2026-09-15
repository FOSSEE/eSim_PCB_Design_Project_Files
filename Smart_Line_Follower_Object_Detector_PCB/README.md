# Smart Line-Following and Object-Detection Robot Controller PCB

## eSim Semester Long Internship - Autumn 2026

### Screening Task 7: PCB Design Using eSim

## Project Overview

This project is a two-layer robot-controller PCB designed using eSim 2.5
and its integrated KiCad tools.

The PCB supports:

- Arduino Nano controller
- Six IR line-sensor interfaces
- HC-SR04 ultrasonic sensor
- Servo motor for directional object detection
- Two external L298N motor-driver modules
- Four DC motors
- Protected battery input
- External regulated 5 V buck-converter interface
- Power, status and object-detection LEDs
- Five electrical test points
- Four mounting holes

## Main Functions

The six IR sensors provide independent line-position inputs to the
Arduino Nano. The controller processes the sensor signals and controls
the left and right motor groups through two external L298N modules.

The HC-SR04 sensor measures object distance. The servo interface allows
the ultrasonic sensor to scan different directions.

## Final Design Results

- Copper layers: 2
- Pads: 124
- Vias: 30
- Track segments: 320
- Electrical nets: 37
- Unrouted connections: 0
- ERC errors: 0
- ERC warnings: 0
- DRC violations: 0
- DRC unconnected items: 0
- Mounting holes: 4

## Project Structure

- `01_Report`: Final PDF and editable report
- `02_KiCad_Project`: Complete KiCad project files
- `03_BOM`: Bill of Materials in Excel and CSV formats
- `04_Proposal`: Task 7 project proposal
- `05_Screenshots`: Schematic, routing, DRC and 3D evidence

## Software

- eSim Version 2.5
- Integrated KiCad tools
- KiCad 6.0.11

## Important Hardware Note

The battery input is intended for a properly assembled and protected
battery pack. Individual 18650 cells must not be connected without a
suitable BMS, balancing, short-circuit protection and compatible charger.

The external buck-converter output must be adjusted to 5.0 V before
connecting the Arduino Nano, sensors or servo branch.

## Design Validation

The design was validated digitally using:

- KiCad Electrical Rules Checker
- Complete two-layer routing
- KiCad Design Rules Checker
- Edge.Cuts inspection
- KiCad 3D Viewer

Physical fabrication and hardware testing were outside the scope of the
screening submission.

## Author

Name: BrajBhushan Sah

College: Techno Main Salt Lake, Kolkata

Department: Electronics and Communication Engineering
