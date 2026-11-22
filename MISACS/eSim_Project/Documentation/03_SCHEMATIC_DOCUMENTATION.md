# MISACS Phase 3 — Complete Schematic Documentation
**File:** `MISACS.kicad_sch`  
**SHA-256:** `6DE222A83B9F2B13141575CEB4C2BE5E1923FCCB374766BCFE82D35701CE10B8`  
**Size:** 134,618 bytes  

## 1. Schematic Design Rules and Verification
- **Native KiCad 6.0.11 ERC Status:** **0 Errors, 74 Warnings** (all warnings verified as standalone embedded library metadata).
- **Physical Pin Coverage:** 196 / 196 pin endpoints reconciled against PCB pads with 100.0% net parity.
- **Embedded Symbols:** Self-contained within `(lib_symbols ...)` block, guaranteeing complete project portability across eSim 2.5 and KiCad installations without external library path dependencies.

## 2. Integrated Power Routing & Subsystem Net Mapping
- `+24V`: Main incoming industrial DC rail from terminal block `J1`.
- `+24V_LOGIC_FUSED`: Protected by resettable PTC fuse `F1` (1.1A hold, 2.2A trip).
- `+24V_LOGIC_PROT`: Reverse-polarity blocked rail downstream of Schottky diode `D2` (SS36).
- `+5V`: Regulated switching supply rail from buck converter `U1` (LM2576HVS-5.0).
- `+3V3`: Regulated linear supply rail from LDO regulator `U2` (AMS1117-3.3).
- `GND`: Unified low-impedance system ground referenced to continuous bottom-layer copper plane.
- `+24V_ACT1_FUSED` / `+24V_ACT2_FUSED`: Dedicated 5A fused actuator power rails.
- `MOSFET1_DRAIN` / `MOSFET2_DRAIN`: Low-side switched load terminals with SS56 flyback clamp protection.
