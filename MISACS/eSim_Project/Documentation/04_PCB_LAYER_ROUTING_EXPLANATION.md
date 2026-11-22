# MISACS Phase 3 — PCB Layer Stackup and Routing Architecture
**File:** `MISACS.kicad_pcb`  
**SHA-256:** `136E71039AF185293E34E51087B60F242863BE97F9A93EC3C97C44F1EA3E88A4`  
**Dimensions:** $100.00\,\text{mm} \times 80.00\,\text{mm}$ nominal routed centerline ($100.15\,\text{mm} \times 80.15\,\text{mm}$ outer graphic stroke extents)  

## 1. Layer Stackup Specification
- **Layer 1 (F.Cu - Top Copper):** 1 oz ($35\,\mu\text{m}$) copper thickness. Carries point-to-point analog sensor traces, digital high-speed signals (UART, I2C, PWM), gate drive tracks, and wide power tracks (1.0 mm to 2.5 mm). Total segment count: 292 tracks.
- **Dielectric (FR-4):** $1.6\,\text{mm}$ core thickness, relative dielectric permittivity $\epsilon_r \approx 4.5$.
- **Layer 2 (B.Cu - Bottom Copper):** 1 oz ($35\,\mu\text{m}$) copper thickness. Dominated by a solid, unbroken system ground plane polygon ($6,661.3\,\text{mm}^2$ filled area) providing low-inductance return paths for analog, digital, and switching currents. Total segment count: 59 tracks.
- **Via Count:** 91 through-hole plated vias (0.30 mm drill / 0.65 mm pad for signal transitions; 0.60 mm drill / 1.20 mm pad for thermal ground stitching).

## 2. Noise Mitigation and Grounding Strategy
- **Ground Plane Integrity:** The continuous bottom-layer ground plane ensures minimal ground loop areas and negligible common-impedance coupling.
- **High-Current Path Separation:** High-current actuator return loops are kept localized near the power entry connector `J1` and output blocks `J5`/`J6`, preventing high-current ground bounce from perturbing sensitive ADS1115 analog measurements.
- **Analog Partitioning:** The AFE operational amplifier `U3` and ADC `U4` are grouped in a dedicated analog cluster with direct short decoupling loops to GND.
