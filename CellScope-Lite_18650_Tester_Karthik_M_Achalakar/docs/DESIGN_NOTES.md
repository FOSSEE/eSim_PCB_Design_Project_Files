# CellScope-Lite: design notes (block by block)

CellScope-Lite is a single-cell **18650 Li-ion charger and capacity tester**. It charges a cell at 1 A
(CC/CV to 4.20 V). It then discharges the cell at a precise constant current between 0 and 0.975 A,
and stops automatically at 3.0 V. An INA226 monitor reports cell voltage, current and power over I²C,
so any microcontroller can integrate mAh and mWh and report the cell's real capacity.

All values below are on the schematic (sheet A2, nine blocks) and were checked with Ngspice 45.2,
which ships with eSim 2.6.

---

## 1. USB-C 5 V input and protection (J1, R1, R2, F1, D1, C1, R25, D2)
| Part | Why |
|---|---|
| J1 USB-C (HRO TYPE-C-31-M-12) | Modern connector; any USB-C charger works. |
| R1, R2 = 5.1 kΩ on CC1/CC2 | Tells the USB-C source "I am a sink". Without these resistors a USB-C charger supplies **no** 5 V. |
| F1 polyfuse, 1.5 A hold | Resettable protection against shorts on the board. |
| D1 SMAJ5.0A TVS | Clamps ESD and hot-plug spikes above about 6.4 V. |
| C1 10 µF | Bulk input capacitor. |
| D2 + R25 (2 kΩ) | Green power LED, about 1.5 mA. |

## 2. TP4056 charger (U1, R3, C2, C3, R4/D3, R5/D4)
* Linear CC/CV charger: constant current until 4.2 V, then constant voltage until the current drops to 1/10.
* **Charge current = 1200 V / R_PROG = 1200 / 1.2 kΩ = 1.0 A** (from the datasheet).
* CHRG (red) and STDBY (blue, "FULL") are open-drain outputs that drive LEDs from 5 V.
* TEMP is tied to GND, which disables the NTC function because the holder has no thermistor.
* The exposed pad (pin 9) is soldered to a GND copper area with 3 vias. A linear charger dissipates
  (5 − V_bat) × I, up to about 1.5 W, and this pad is its heatsink.

## 3. Cell protection: DW01A + FS8205A (U2, Q1, R6, C4, R7)
* Industry-standard 1-cell protection (the same IC pair used in every power bank).
* The DW01A watches the cell voltage through the R6/C4 filter (100 Ω / 100 nF) and drives two MOSFETs in the FS8205A:
  * **OD** turns off the *discharge* FET when V_cell < 2.4 V (over-discharge).
  * **OC** turns off the *charge* FET when V_cell > 4.3 V (over-charge).
  * **CS** senses the voltage across the MOSFETs through R7 (2 kΩ) for over-current and short-circuit trips.
* The cell negative is **BAT_N**. The board ground (GND) sits *after* the protection FETs, so everything is protected.

## 4. 3.3 V rail and precision reference (U3, C5, C6, U4, R8, C7)
* AP2112K-3.3: 600 mA LDO with low noise. It powers the op-amp, the INA226 and the host connector.
* LM4040-2.048: 0.1 % shunt reference. R8 = 2.2 kΩ gives I_Z = (3.3 − 2.048) / 2.2 kΩ = 0.57 mA,
  which is above the 60 µA minimum.
* The set-point comes from a **precision reference, not the 3.3 V rail**, so the load current does not
  drift with supply ripple or temperature.

## 5. Set-point (R9, RV1, R10, R11, JP1, R12, C8, SW1, Q2)
* **V_SET = 2.048 V × RV1 / (R9 + RV1) = 2.048 × 10k / 210k = 0 to 97.5 mV**, which is 0 to 0.975 A.
* A multi-turn trimmer (Bourns 3296W, 25 turns) gives fine resolution of about 1 mA per 1/4 turn.
* **JP1** selects the set-point source: 1-2 = trimmer, 2-3 = external DAC on the HOST header (J2 pin 5).
  A 3.3 V DAC output is divided by R10/R11 (330k/10k), which gives the same 0–97 mV range. A
  microcontroller can then run *programmable* discharge profiles (pulse tests, internal-resistance tests).
* **R12 + C8 (10 kΩ, 1 µF, τ = 10 ms)** form a soft-start and noise filter, so the current ramps up smoothly.
* **SW1 (LOAD ON/OFF)** shorts the set-point to GND, so the load is off without touching the trimmer.
* **Q2 (2N7002)** is driven by the UVLO comparator. It also clamps the set-point to 0, which turns the load off.

## 6. Constant-current electronic load (U5A, Q3, R16, R13, C9, R14, R15, NT1)
* Classic op-amp + MOSFET current sink. The op-amp forces V(SENSE_HI) = V_SET, so
  **I_LOAD = V_SET / R16 = V_SET / 0.1 Ω**, independent of the cell voltage.
* MCP6002: rail-to-rail input and output, which matters because the set-point is only a few mV above 0 V.
* Q3 IRLZ44N: *logic-level* MOSFET. It is rated R_DS(on) ≤ 35 mΩ at V_GS = 4 V and ≤ 25 mΩ at 5 V. At 1 A it needs only about 1.9 V of gate
  drive (simulated), so a 3.3 V op-amp controls it easily.
* **Stability:** C9 (10 nF) from the output to the −input, with R13 (1 kΩ), forms an integrator that rolls off the
  loop gain before the MOSFET's gate capacitance (about 1.7 nF) adds phase lag. R14 (100 Ω) is a gate stopper
  that isolates the op-amp output from that capacitance. R15 (100 kΩ) holds the gate off at power-up.
* **Thermal:** P_Q3 = (V_BAT − I·R16) × I, which is 4.1 W at 4.2 V and 1 A. Q3 is a TO-220 at the board edge
  ("HEATSINK" on the silkscreen) so a clip-on heatsink fits. R16 dissipates only I²R = 0.1 W in a 2 W 2512 package.
* **Kelvin sensing:** NT1 (net-tie) joins SENSE_LO to GND *only at R16's ground pad*. The INA226 therefore measures
  the true shunt voltage, not the shunt plus ground-plane IR drop.

## 7. INA226 power monitor (U6, C12, R17–R19)
* 16-bit current, voltage and power monitor, I²C address **0x40** (A0 = A1 = GND).
* Shunt LSB = 2.5 µV, so 25 µA resolution with 0.1 Ω. Bus (cell voltage) LSB = 1.25 mV.
* Calibration register: **CAL = 0.00512 / (I_LSB × R_SHUNT) = 0.00512 / (25 µA × 0.1 Ω) = 2048.**
* R17/R18 (4.7 kΩ) are the I²C pull-ups and R19 is the ALERT pull-up. ALERT can be programmed as a second,
  software-defined cut-off.
* The same I²C bus goes to the **Qwiic/STEMMA-QT** connector (J3), so it plugs straight into
  Arduino, ESP32 or Raspberry Pi boards without soldering.

## 8. UVLO discharge cut-off (U5B, R20–R24, R26, C13, D5)
* The second half of the MCP6002 is used as a comparator with hysteresis.
* Divider k = R21 / (R20 + R21) = 1 M / 1.619 M = 0.6177 (1 % resistors). C13 filters noise (τ = 38 ms).
* V+ = 2.048 V × 100k/110k = 1.862 V (output low) or 2.162 V (output high).
* **Trip (falling) = 1.862 / 0.6177 = 3.01 V; release (rising) = 2.162 / 0.6177 = 3.50 V.**
  Simulated: 3.017 V and 3.490 V.
* Why so much hysteresis? When the load turns off, a real cell "bounces back" by 100–300 mV. A small
  hysteresis would make the load switch on and off repeatedly near the end of discharge. The 0.49 V window
  makes the cut-off **latch**, so the test ends cleanly. The amber CUTOFF LED (D5) shows that the test has finished.
* With no cell inserted, V_BAT = 0 V, so UVLO is active and the load is safely disabled.

## 9. Interface, test points, mechanical
* J2 HOST (2.54 mm): 3V3, SDA, SCL, ALERT, EXT_SET, GND.
* J3 Qwiic (JST-SH 4-pin): GND, 3V3, SDA, SCL (standard SparkFun/Adafruit pin-out).
* TP1–TP7: VBAT, SENSE_HI (true load current), SET_FILT (set-point), GATE, 3V3, 5V, GND, for bring-up with a DMM or scope.
* 4 × M3 mounting holes and 3 fiducials for pick-and-place assembly.

---

## PCB (4 layers, 104 × 72 mm)
| Layer | Use |
|---|---|
| F.Cu | Components, signal routing, GND pour |
| In1.Cu | **Solid GND plane** (return path, shielding) |
| In2.Cu | **+3V3 plane** (low-impedance supply for the analog parts) |
| B.Cu | Signal routing, GND pour |

Design rules: 0.15 mm minimum clearance and track width, 0.6/0.3 mm signal vias, 0.8/0.4 mm power vias.
The Power net class (VBAT, +5V, VBUS_IN, SENSE_HI, BAT_N, FET_D, GND) uses 0.8 mm tracks.
Custom DRC rules (`CellScope-Lite.kicad_dru`):
1. a 0.15 mm fine-pitch exception that applies only inside the INA226 courtyard;
2. a hole-clearance keep-out around the M3 mounting holes.

INA226 GND pin 7 goes straight to the ground pad of its decoupling capacitor C12 (which has its own plane via).

## How a capacity test runs
1. Insert the cell and plug in USB-C. The red CHRG LED lights, and the cell charges at 1 A until the blue FULL LED lights.
2. Set the discharge current with RV1 while measuring TP3 (V_SET; 1 mV = 10 mA), or drive EXT_SET from a DAC.
3. Turn SW1 to LOAD ON. The cell discharges at constant current, and the INA226 logs V, I and P over I²C.
4. At 3.0 V the comparator latches the load off and the amber CUTOFF LED lights.
   Capacity = ∫ I dt (with a constant current, simply I × t).
