# Hardware Implementation and 2-Layer PCB Design of an Asynchronous UART to Synchronous SPI Protocol Bridge Interface Board

**Author:** R. Selvakumaran  
**Affiliation:** Department of Electronics and Communication Engineering, National Institute of Technology Tiruchirappalli (NIT Trichy), Tamil Nadu, India — 620015  
**Host Organization:** Free and Open Source Software for Education (FOSSEE), Indian Institute of Technology Bombay (IIT Bombay)  
**Submission Category:** FOSSEE Semester Long Internship — Autumn 2026 | **Task 7: PCB Design using eSim**  
**EDA Software:** eSim v2.5 / v2.6 (KiCad 6.0.11 Schematic Capture + PCB Editor + 3D Viewer)  
**Date of Completion:** November 23, 2026  

---

## 1. Project Abstract & Overview

This project presents the complete hardware implementation and 2-layer printed circuit board (PCB) design of an autonomous **Universal Asynchronous Receiver-Transmitter (UART) to Serial Peripheral Interface (SPI) Protocol Bridge Interface Board** created strictly using the open-source **eSim EDA** (KiCad backend) suite.

Modern heterogeneous embedded platforms frequently encounter protocol incompatibility when low-speed asynchronous peripherals (UART sensors, GPS units, telemetry links) must interface with high-throughput synchronous bus devices (SPI flash, graphical LCDs, digital signal processors). Conventional solutions rely on software bit-banging on a host microcontroller, introducing severe interrupt latencies, jitter, and excessive CPU utilization. 

This design implements a **hardware-level protocol converter** using discrete 74xx-series high-speed CMOS logic:
1. **Asynchronous Deserializer & Output Latch (U3 - 74HC595):** Captures the incoming asynchronous serial bitstream on `RX` at baud clock edges, shifts bits into an 8-bit SIPO register, and latches the completed byte.
2. **Clock Divider & SPI Frame Controller (U1 - 74HC74):** A dual positive-edge D-flip-flop that prescales the input master clock and generates the autonomous active-low Chip Select (`/CS`) framing signal.
3. **Glitch-Free Gated SPI Clock Generator (U2 - 74LS08):** High-speed 2-input positive AND logic gating the synthesized serial clock with the `/CS` transmission window, guaranteeing compliance with **SPI Mode 0 (`CPOL=0, CPHA=0`)**.
4. **Power Conditioning & Decoupling:** 10 µF electrolytic bulk capacitor (`C1`) and three 100 nF ceramic bypass capacitors (`C2, C3, C4`) placed directly adjacent to IC `VCC`/`GND` pins to suppress high-frequency switching transients and ground bounce.
5. **Diagnostics & Standard Interfacing:** Visual Power LED (`D1`) and SPI Activity LED (`D2`), with standard 2.54 mm pitch vertical headers for 5V DC power (`J1`), UART host (`J2`), and SPI bus (`J3`).

The physical board is realized on a **2-layer rigid FR4 PCB (88.0 mm × 52.0 mm)** with low-impedance ground track chaining and ground plane fill. KiCad's integrated Design Rules Checker (DRC) validates the layout with **0 Violations, 0 Unconnected Items, 0 Errors, and 0 Warnings**.

---

## 2. Hardware Architecture & System Interconnect

```
         +-------------------------------------------------------------+
         |                 5V DC Power Input (J1)                      |
         |                 [+5V, GND] + C1 (10uF) Bulk                 |
         +-------------------------------------------------------------+
                                      |
                                      v
  +--------------------+    +--------------------+    +--------------------+
  |  UART Input (J2)   |    |    74HC595 (U3)    |    |   SPI Output (J3)  |
  |  [VCC, GND, RX,    |--->|  8-Bit SIPO Shift  |--->|  [VCC, GND,        |
  |   Ext CLK]         |    |   Register & Latch |    |   /CS, SCK,        |
  +--------------------+    +--------------------+    |   MOSI, MISO]      |
            |                         ^               +--------------------+
            v                         |                          ^
  +--------------------+              |                          |
  |    74HC74 (U1)     |--------------+                          |
  | Dual D-FF Divider  |-----------------------------------------+
  |  & /CS Controller  |               Gated Burst SCK
  +--------------------+                      ^
            |                                 |
            +------------------------>+----------------+
                                      |  74LS08 (U2)   |
                                      | AND Clock Gate |
                                      +----------------+
```

---

## 3. Bill of Materials (BOM)

| Item | RefDes | Value / Component | Package / Footprint | Qty | Description & Purpose |
|:---:|:---:|:---:|:---:|:---:|:---|
| 1 | U1 | 74HC74 | `Package_DIP:DIP-14_W7.62mm` | 1 | Dual D-type positive-edge flip-flop (clock divider & /CS frame controller) |
| 2 | U2 | 74LS08 | `Package_DIP:DIP-14_W7.62mm` | 1 | Quad 2-input positive-AND gate (SPI Mode 0 gated SCK burst generator) |
| 3 | U3 | 74HC595 | `Package_DIP:DIP-16_W7.62mm` | 1 | 8-bit SIPO shift register with 3-state output storage latch |
| 4 | C1 | 10 µF, 25V | `Capacitor_THT:CP_Radial_D5.0mm_P2.50mm` | 1 | Bulk polarized electrolytic capacitor for input supply ripple smoothing |
| 5 | C2, C3, C4 | 100 nF, 50V | `Capacitor_THT:C_Disc_D3.0mm_W1.6mm_P2.50mm` | 3 | Ceramic disc bypass decoupling capacitors adjacent to IC power pins |
| 6 | R1, R3 | 330 Ω, 0.25W | `Resistor_THT:R_Axial_DIN0207_P7.62mm` | 2 | Current-limiting series resistors for Power LED (D1) and Activity LED (D2) |
| 7 | R2 | 10 kΩ, 0.25W | `Resistor_THT:R_Axial_DIN0207_P7.62mm` | 1 | Pull-up resistor on UART RX line ensuring stable high idle state |
| 8 | D1 | LED Red (PWR) | `LED_THT:LED_D3.0mm` | 1 | 5V DC primary power health indicator |
| 9 | D2 | LED Red (ACT) | `LED_THT:LED_D3.0mm` | 1 | Active SPI transmission burst telemetry indicator |
| 10 | J1 | Conn_01x02 | `Connector_PinHeader_2.54mm:PinHeader_1x02_Vertical` | 1 | Main 5V DC input header (Pin 1: +5V, Pin 2: GND) |
| 11 | J2 | Conn_01x04 | `Connector_PinHeader_2.54mm:PinHeader_1x04_Vertical` | 1 | UART host interface (Pin 1: VCC, Pin 2: GND, Pin 3: RX, Pin 4: CLK) |
| 12 | J3 | Conn_01x06 | `Connector_PinHeader_2.54mm:PinHeader_1x06_Vertical` | 1 | SPI Master header (1: VCC, 2: GND, 3: /CS, 4: SCK, 5: MOSI, 6: MISO) |
| 13 | H1-H4 | MountingHole | `MountingHole:MountingHole_3.2mm_M3` | 4 | M3 mechanical chassis mounting holes at the four board corners |

---

## 4. PCB Specifications & Physical Stackup

- **Board Dimensions:** 88.0 mm × 52.0 mm
- **Board Thickness:** 1.6 mm standard rigid FR4 substrate ($\epsilon_r = 4.5$)
- **Copper Layers:** 2 Copper Layers (1.0 oz / 35 µm copper foil per layer)
  - **Top Copper (`F.Cu` - Red):** Horizontal signal tracks, IC local interconnects, VCC distribution
  - **Bottom Copper (`B.Cu` - Blue):** Vertical orthogonal tracks, low-impedance ground return chaining
- **Track Widths:**
  - Power / Ground Rails (`VCC`, `GND`): **0.50 mm (20 mils)**
  - Digital Logic Signals: **0.25 mm (10 mils)**
- **Clearance Constraints:** 0.25 mm (10 mils) track-to-track; 0.50 mm (20 mils) copper zone clearance
- **Mechanical Mounting:** Four M3 (3.2 mm diameter) unplated holes positioned symmetrically at `(X, Y) = (4.0 mm, 4.0 mm)` from board corners
- **Silkscreen & Solder Mask:** High-contrast white silkscreen over industrial green liquid photo-imageable (LPI) solder mask

---

## 5. Design Rule Check (DRC) Verification

The board was validated using KiCad's integrated **Design Rules Checker (DRC)** with full schematic netlist parity:
- **Violations:** **0**
- **Unconnected Items:** **0**
- **Errors:** **0**
- **Warnings:** **0**

The design has zero unrouted nets, zero clearance violations, and 100% connectivity across all power and signal domains.

---

## 6. How to Open and Inspect the Project in eSim

### Option A: Using eSim GUI
1. Launch **eSim v2.5** (or v2.6).
2. Click **Open Project** and navigate to this directory (`uart_spi_pcb`).
3. Select `uart_spi_pcb.proj` and click **Open**.
4. To view the schematic, click the **Open Schematic** icon (launches eSchema).
5. To view the PCB layout, click the **Open PCB** icon (launches KiCad PCB Editor).
6. In PCB Editor, press **Alt + 3** or navigate to `View -> 3D Viewer` to examine the 3D rendered board.

### Option B: Using Standalone KiCad 6
1. Launch KiCad 6.
2. Open `uart_spi_pcb.kicad_pro`.
3. Open `uart_spi_pcb.kicad_sch` to view and edit the schematic.
4. Open `uart_spi_pcb.kicad_pcb` to view and edit the routed 2-layer layout.
5. In the PCB Editor, navigate to `Inspect -> Design Rules Checker` and click **Run DRC** to confirm **0 Errors, 0 Warnings, 0 Unconnected Items**.

---

## 7. Deliverable File Structure

```
uart_spi_pcb/
│
├── uart_spi_pcb.kicad_sch           # Complete eSchema circuit schematic
├── uart_spi_pcb.kicad_pcb           # 2-layer routed PCB layout file
├── uart_spi_pcb.kicad_pro           # KiCad 6 master project definition file
├── uart_spi_pcb.kicad_prl           # KiCad project local settings file
├── uart_spi_pcb.proj                # eSim project descriptor
├── fp-info-cache                    # Footprint library cache
│
├── UART_to_SPI_Hardware_PCB_Report.pdf  # Comprehensive 11-page technical report
├── README.md                        # Complete project documentation & guide
│
└── Images/                          # High-resolution publication figures
    ├── fig1_circuit_schematic.png           # Schematic capture in eSchema
    ├── fig2_footprint_assignment.jpg        # Footprint assignment dialog
    ├── fig3_pcb_floorplan_silkscreen.png    # Floorplan, Edge.Cuts & silkscreen
    ├── fig4_pcb_routed_2layer_layout.png    # 2-layer routed copper layout
    ├── fig5_drc_validation_zero_errors.png  # DRC report (0 errors, 0 unconnected)
    ├── fig6_3d_viewer_isometric_render.png  # Photorealistic 3D isometric view
    └── fig7_3d_viewer_routed_traces.png     # 3D view of copper traces & annular rings
```

---

## 8. Author Declaration & Compliance

I, **R. Selvakumaran**, hereby declare that this project, submitted for **Task 7: PCB Design using eSim** of the FOSSEE Winter Internship 2026 at the Indian Institute of Technology Bombay (IIT Bombay), is an authentic, original work executed independently by me using eSim and KiCad. All schematics, footprint selections, routing strategies, DRC verifications, and technical documentations were produced directly from my engineering design efforts.

**Contact Details:**
- **Name:** R. Selvakumaran
- **Department:** Electronics and Communication Engineering (2nd Year B.Tech)
- **Institution:** National Institute of Technology Tiruchirappalli (NIT Trichy), Tamil Nadu, India — 620015
- **Submission Destination:** `contact-esim@fossee.in`
