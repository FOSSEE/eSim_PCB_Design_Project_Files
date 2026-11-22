# MISACS Phase 3 — Assembly Instructions and Connector Pinout Reference
**Revision:** Phase 3 Master Release Candidate  

## 1. Connector Pinout Reference

### J1: Main DC Power Input (Phoenix MKDS 1,5/2-5.08)
- **Pin 1:** `+24V` Main DC Power Input ($+18\text{V}$ to $+30\text{V DC}$)
- **Pin 2:** `GND` System Power Ground Return

### J2: 4–20 mA Current Loop Input (Phoenix MKDS 1,5/2-5.08)
- **Pin 1:** `LOOP_POS` Loop Current Signal (+)
- **Pin 2:** `GND` Loop Current Return (-)

### J3: 0–10 V Industrial Voltage Input (Phoenix MKDS 1,5/2-5.08)
- **Pin 1:** `0-10V_IN` Process Voltage Input ($0\text{V}$ to $10\text{V DC}$)
- **Pin 2:** `GND` Analog Signal Ground Reference

### J4: RS-485 Industrial Serial Bus (Phoenix MKDS 1,5/3-5.08)
- **Pin 1:** `RS485_A` Non-Inverting Differential Line (Data +)
- **Pin 2:** `RS485_B` Inverting Differential Line (Data -)
- **Pin 3:** `GND` Common Bus Reference Shield / Ground

### J5: Actuator Channel 1 Low-Side Switched Output (Phoenix MKDS 1,5/2-5.08)
- **Pin 1:** `+24V_ACT1_FUSED` Dedicated Fused Supply (+)
- **Pin 2:** `MOSFET1_DRAIN` Switched Low-Side Return (-)

### J6: Actuator Channel 2 Low-Side Switched Output (Phoenix MKDS 1,5/2-5.08)
- **Pin 1:** `+24V_ACT2_FUSED` Dedicated Fused Supply (+)
- **Pin 2:** `MOSFET2_DRAIN` Switched Low-Side Return (-)

---

## 2. Hardware Controls and Status Indicators
- **SW1 (RESET):** Hardware reset button (pulls ESP32 `EN` pin to GND).
- **SW2 (BOOT):** Bootloader download mode button (pulls ESP32 `IO0` to GND).
- **D3 (Green LED):** $+24\text{V}$ Main Power Entry Indicator.
- **D6 (Blue LED):** $+3.3\text{V}$ Logic Power Rail Indicator.
- **D9 (Amber LED):** Actuator Channel 1 Output Active Indicator.
- **D11 (Amber LED):** Actuator Channel 2 Output Active Indicator.
