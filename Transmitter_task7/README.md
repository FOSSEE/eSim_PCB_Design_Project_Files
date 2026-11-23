# Custom 2.4 GHz Ergonomic Drone RC Transmitter (2-Layer PCB)

A custom handheld 2.4 GHz radio-control (RC) transmitter PCB designed for quadcopters and UAVs using **eSim (KiCad-based PCB workflow)**. The board integrates an **ESP32-WROOM-32E** microcontroller, an **nRF24L01+PA+LNA** long-range transceiver, dual analog joysticks, flight-mode switches, and an OLED telemetry display on a compact, gamepad-shaped 2-layer FR4 board.

**Author:** MD Hazijul Haque  
**Program:** FOSSEE eSim Winter Internship 2026 (Task 7)  
**Project Folder:** `Transmitter_task7/`

---

## Hardware Specifications

| Parameter | Specification |
| :--- | :--- |
| **Microcontroller** | ESP32-WROOM-32E (`U2`) |
| **RF Module** | nRF24L01+PA+LNA 2.4 GHz Transceiver (`U1`, SPI) |
| **Display** | 0.91" I2C OLED Telemetry Screen (`U3`) |
| **Power Input** | 2S LiPo Battery (`J4`, 7.4 V nominal / 8.4 V max) |
| **Voltage Rails** | `+5V` via LM2596S-5 Buck (`U4`), `+3V3` via AMS1117-3.3 LDO (`U5`) |
| **Controls** | 2x Dual-Axis Analog Joysticks (`J3`, `J9`), Arm & Mode Switches (`SW3`, `SW4`) |
| **PCB Stackup** | 2-Layer FR4, 1.6 mm thickness, 1 oz copper (`F.Cu` & `B.Cu`) |
| **Component Count** | 47 components (including 4 mounting holes `H1`–`H4`) |

---

## Schematic Explanation

The schematic (`Transmitter_task7.kicad_sch`) is organized into four functional blocks so that power, control, communication, and user feedback stay clean and easy to debug.

### 1. Power Supply & Protection Stage
* **Battery Input & Safety:** A 2S LiPo battery connects through header `J4` and main power switch `SW5`. A Schottky diode (`D6`) provides reverse-polarity protection so an accidentally reversed battery will not damage the board.
* **Two-Stage Regulation:** The battery voltage first steps down to a stable **`+5V`** rail through the `LM2596S-5` switching buck converter (`U4`). From `+5V`, an `AMS1117-3.3` linear regulator (`U5`) generates a low-noise **`+3V3`** rail to safely power the ESP32, RF transceiver, and OLED display.

### 2. Battery Voltage Sensing
* To monitor battery health without exceeding the ESP32's 3.3 V ADC limit, a resistor voltage divider made of **`R2` (20 kΩ)** and **`R3` (10 kΩ)** scales the 2S LiPo voltage down by one-third (8.4 V max becomes **2.8 V**).
* A filter capacitor (`C2`) smooths out voltage spikes before feeding the signal into **`SENSOR_VP` (Pin 4)** of the ESP32.

### 3. Microcontroller & Wireless Communication
* The **ESP32-WROOM-32E (`U2`)** acts as the central controller, reading all pilot inputs and driving the radio and display.
* The **nRF24L01+PA+LNA (`U1`)** connects to the ESP32 over the **SPI** bus for fast, low-latency 2.4 GHz packet transmission.
* A dedicated **UART header (`J1`)** along with tactile **Reset (`SW1`)** and **Boot (`SW2`)** buttons allow easy firmware flashing and serial debugging.

### 4. Pilot Controls & Telemetry Feedback
* **Joysticks (`J3`, `J9`):** Two 5-pin socket headers connect the left and right analog joysticks (Throttle, Yaw, Pitch, Roll) to the ESP32 ADC pins.
* **Switches (`SW3`, `SW4`):** A 3-way SPDT toggle switch (`SW3`) selects flight modes, while an SPST toggle switch (`SW4`) handles arming and disarming.
* **Display & Alerts:** A **0.91" I2C OLED (`U3`)** displays live battery voltage, arming status, and flight mode. Four status LEDs (`D1`, `D2`, `D4`, `D5`) and a **buzzer header (`J2`)** provide instant visual and audible alerts.

---

## PCB Design & Layout Explanation

The 2-layer PCB (`Transmitter_task7.kicad_pcb`) is designed for both comfortable handheld ergonomics and reliable RF/analog signal integrity:

* **Gamepad Ergonomics:** The board outline is shaped like a handheld game controller, placing the dual joysticks (`J3`, `J9`) naturally under the thumbs, the OLED screen (`U3`) in the upper center for clear visibility, and the switches (`SW3`, `SW4`) within easy finger reach. Four mounting holes (`H1`–`H4`) allow secure attachment inside a 3D-printed enclosure.
* **Noise Isolation:** The switching buck converter (`LM2596S-5`, `U4`) and its associated power components are grouped tightly in the **lower-right grip**. Keeping high-frequency switching currents away from the RF transceiver and analog joystick traces reduces electromagnetic noise and joystick jitter.
* **RF Antenna Keep-Out:** Copper pours and signal traces are kept clear around the antenna area so the 2.4 GHz signal radiates cleanly without detuning or range loss.
* **2-Layer Routing Strategy:** Top (`F.Cu`) and bottom (`B.Cu`) layers carry signal and power traces with short, direct paths for SPI, I2C, and decoupling capacitors, supported by a clean ground reference across the board.
* **Design Verification:** Both **Electrical Rules Check (`ERC.rpt`)** and **Design Rules Check (`DRC.rpt`)** were executed to verify connectivity, clearances, and manufacturability.

---

## System Working Flow

```text
  [ 2S LiPo Battery (7.4V - 8.4V) ]
                  │
                  ▼
     [ Switch SW5 + Diode D6 ] ──────► [ Voltage Divider R2/R3 + C2 ] ──► Battery Level
                  │                                                            │
                  ▼                                                            ▼
    [ LM2596S-5 Buck (+5V) ]                                         (ESP32 ADC Pin 4)
                  │
                  ▼
   [ AMS1117-3.3 LDO (+3V3) ]
                  │
                  ▼
  ┌────────────────────────────────────────────────────────────────────────────┐
  │                         ESP32-WROOM-32E (U2)                               │
  │   • Reads Joysticks (J3, J9) & Switches (SW3 Mode, SW4 Arm)                │
  │   • Reads Battery Voltage via SENSOR_VP                                    │
  │   • Packs control channels into 2.4 GHz data packets                       │
  └───────────────────┬────────────────────────────────────┬───────────────────┘
                      │ (SPI)                              │ (I2C / GPIO)
                      ▼                                    ▼
         [ nRF24L01+PA+LNA (U1) ]            [ 0.91" OLED (U3), LEDs, Buzzer ]
                      │                                    │
                      ▼                                    ▼
        Transmits RC Control Packets         Displays Telemetry & Status Alerts
             to Drone Receiver                       to the Pilot