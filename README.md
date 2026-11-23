# ESP32 Relay and Li-ion Charger Controller PCB

A compact PCB designed in **eSim 2.5** (KiCad 6.0.11) built around an ESP-WROOM-32. The board monitors Li-ion cell temperature and voltage, charges the cell with a TP4056, and uses a 5 V relay to switch the charger's supply path.

## Features

- ESP-WROOM-32 (U1) microcontroller module
- TP4056 (U3) single-cell Li-ion charger
- Keystone 1042 holder for one 18650 cell (BT1)
- 5 V relay (K1, G5V-1-DC5) driven by a transistor (Q1) from ESP32 pin D4, with a 1N4007 flyback diode (D1)
- NTC thermistor (RT1) with 10K resistor (R1), read on D36
- Battery voltage divider (R2, R3 = 10K each), read on D34
- LM1117-3.3 (U2) regulator for the 3.3 V rail
- 2-pin screw terminal (J1) for the +5 V input

## Design Results

| Item | Result |
|---|---|
| ERC | 0 errors, 0 warnings |
| DRC | 0 violations, 0 unconnected items |
| Pads / Vias / Track segments / Nets | 78 / 27 / 118 / 47 |
| Unrouted nets | 0 |
| Copper layers defined | Front, In1.Cu, In2.Cu, Back |

## Bill of Materials

| Ref | Part | Footprint |
|---|---|---|
| BT1 | 18650 holder | Battery:BatteryHolder_Keystone_1042_1x18650 |
| D1 | 1N4007 | Diode_SMD:D_SMA |
| J1 | Screw terminal 1x02 | TerminalBlock_Phoenix_MKDS-1,5-2-5.08_1x02_P5.08mm_Horizontal |
| K1 | G5V-1-DC5 | G5V-1:RELAY_G5V-1-DC5 |
| Q1 | BC857 | Package_TO_SOT_SMD:SOT-23 |
| R1, R2, R3 | 10K | Resistor_SMD:R_0805_2012Metric |
| RT1 | NCU15WF104D60RC | NCU15WF104D60RC:THRMC1005X55N |
| U1 | ESP-WROOM-32 | ESP-WROOM-32:MODULE_ESP-WROOM-32 |
| U2 | LM1117-3.3 | Package_TO_SOT_SMD:SOT-223-3_TabPin2 |
| U3 | TP4056 | TP4056:SOP127P600X175-9N |

## How to Open

1. Install eSim 2.5 (includes KiCad 6.0.11).
2. Open the project in KiCad from eSim.
3. Open the Schematic Editor for the circuit and the PCB Editor for the layout.
4. Use *Inspect > Electrical Rules Checker* (schematic) and *Inspect > Design Rules Checker* (PCB) to reproduce the results above. Use the 3D Viewer (*View > 3D Viewer*) to inspect the board.

## Known Notes / Possible Improvements

- Q1 is a BC857 (PNP) wired as a low-side switch with its emitter to GND. Verify the polarity; an NPN such as BC847 or an N-channel MOSFET is the usual choice here.
- Add a base resistor between D4 and Q1.
- The TP4056 PROG pin needs a resistor to set the charge current.
- Consider decoupling capacitors on the LM1117 and ESP32 supply, and an EN pull-up for the ESP32.
- Add input fuse and reverse-polarity protection.

## Documentation

See the accompanying design report for the schematic, footprint assignment, PCB layout, routing methodology, DRC results and 3D views.
