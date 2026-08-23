# 📡 RF-LNA

**A 2.4 GHz low-noise amplifier front-end board — designed schematic-to-Gerber in eSim + KiCad, for the FOSSEE Autumn Internship 2026 Screening Task 7.**

![eSim](https://img.shields.io/badge/eSim-2.3%20%2F%202.5-orange?style=flat-square)
![KiCad](https://img.shields.io/badge/KiCad-6.0.11-2E8B57?style=flat-square)
![Layers](https://img.shields.io/badge/copper%20layers-4-1E90FF?style=flat-square)

> Boosts a whisper of a signal into something worth listening to

<p align="center">
  <img src="https://github.com/SarHglitch/eSim_PCB_Design_Project_Files/blob/main/files/3d-render-top.png" alt="3D rendered top view of the RF LNA PCB" width="620">
</p>

<p align="center"><i>Yes, it really is that small. Two SMA jacks, one barrel jack, and thirteen tiny parts doing all the work.</i></p>

---

## What is this?

A single-stage **Low-Noise Amplifier (LNA)** front-end for 2.4 GHz RF signals, with its own onboard clean power regulation and a power-status LED, because a board that just quietly works is less satisfying than one that glows a little.

Signal comes in one SMA jack, gets amplified with minimal added noise, and leaves through the other. Feed it 9–12V DC and it handles the rest.

```
   RF IN                                            RF OUT
 (J1, SMA)  ──▶ C1 ──▶ [ U1: SPF5189Z LNA ] ──▶ C2 ──▶ (J2, SMA)
                              ▲
                              │  bias tee (L1, 47nH)
                              │
                    ┌─────────┴─────────┐
        9–12V ──▶ D1 ──▶ [ U2: AMS1117-5.0 ] ──▶ +5V rail ──▶ R2 ──▶ LED1 (💡)
       (J3, jack)              (LDO regulator)
```

---

## ✅ Verification status

| Check | Result |
|---|---|
| Electrical Rules Check (ERC) | 🟢 **0 errors, 0 warnings** |
| Design Rule Check (DRC) | 🟢 **0 errors, 0 warnings, 0 unconnected items** |
| Copper layers | 4 / 4 configured |
| Manufacturability | Gerber-export ready |

<details>
<summary>🔍 Click to see the actual ERC & DRC screenshots</summary>
<br>

| ERC | DRC |
|---|---|
| ![ERC clean](https://github.com/SarHglitch/eSim_PCB_Design_Project_Files/blob/main/files/erc-result.png) | ![DRC clean](https://github.com/SarHglitch/eSim_PCB_Design_Project_Files/blob/main/files/drc-result.png) |

</details>

---

## Full specification

### Core specs

| Spec | Value |
|---|---|
| Frequency band | 2.4 GHz (ISM band) |
| RF impedance | 50 Ω, both ports |
| Amplifier IC | Skyworks **SPF5189Z** (SOT-89) |
| Input power | 9–12 V DC, barrel jack |
| Regulated rail | +5 V (AMS1117-5.0 LDO) |
| Board size | Compact 2-SMA + 1-jack layout (see render above) |
| Copper layers | 4 (F.Cu / In1.Cu / In2.Cu / B.Cu) |
| Design tools | eSim 2.3/2.5 (schematic) + KiCad 6.0.11 (layout, via eSim integration) |

> 📎 Gain and noise-figure values quoted anywhere for the SPF5189Z are **datasheet typicals**, not bench-measured on this specific board.

### 📦 Bill of Materials

| Ref Des | Part | Value | Footprint | Role |
|---|---|---|---|---|
| U1 | SPF5189Z | — | `SOT-89-3` | RF LNA |
| J1, J2 | SMA edge-launch | 50 Ω | `SMA_Amphenol_132134_EdgeMount` | RF in / out |
| C1, C2 | Ceramic cap | 100 pF | `C_0603_1608Metric` | RF DC-block |
| C3 | Ceramic cap | 100 pF | `C_0603_1608Metric` | Local decoupling |
| C4 | Ceramic cap | 100 pF | `C_0805_2012Metric` | Bulk decoupling |
| L1 | RF choke | 47 nH | `L_0603_1608Metric` | Bias tee |
| J3 | Barrel jack | 9–12 V in | `BarrelJack_Horizontal` | DC power in |
| D1 | Schottky diode | 1N5819 | `D_SOD-123` | Reverse-polarity guard |
| U2 | LDO regulator | AMS1117-5.0 | `SOT-223-3_TabPin2` | +5V regulation |
| C5, C6 | Electrolytic/ceramic cap | 100 µF | `C_0805_2012Metric` | LDO in/out decoupling |
| R2 | Resistor | 330 Ω | `R_0603_1608Metric` | LED current limit |
| LED1 | LED | Green, 0805 | `LED_0805_2012Metric` | Power-on indicator |

**13 components. Zero mystery parts. Every footprint pulled straight from eSim/KiCad's default libraries** — nothing custom, nothing that'll break on someone else's machine.

### 🧱 Layer stackup

| Layer | Name | Carries | Why it's there |
|---|---|---|---|
| 1 | **F.Cu** (top) | RF signal + top ground fill | The actual 50Ω microstrip between J1 → U1 → J2 |
| 2 | **In1.Cu** | Ground plane | Sits *right under* the RF trace — this is what makes the impedance calculation real, not a guess |
| 3 | **In2.Cu** | +5V power plane | Clean, isolated power distribution, sandwiched between two grounded layers |
| 4 | **B.Cu** (bottom) | Ground plane | Stitched back to In1.Cu with vias — shields the whole board from both sides |

---

## Repo structure

```
RF-LNA
├── README.md                  ← you are here
├── pcbdesign.kicad_sch         schematic (also openable in eSim eSchema)
├── pcbdesign.kicad_pcb         PCB layout, 4-layer
├── pcbdesign.kicad_pro         project file
├── Task7_RF_LNA_Report.pdf   full write-up: circuit, footprints, routing, DRC, 3D views
└── Files                   images used in this README
```

---

## Opening it

1. Install **eSim 2.3 or 2.5** ([official download](https://esim.fossee.in/downloads)).
2. `File → Open Project`, point it at this folder.
3. Open the schematic in **eSchema** — run **ERC** if you don't believe the badge above. 😄
4. Jump into the **PCB Editor** (via eSim's KiCad integration) to see the 4-layer layout.
5. `View → 3D Viewer` for the render you saw at the top of this page.

Full step-by-step verification instructions (including how to check individual nets) are in [`docs/Task7_RF_LNA_Report.docx`](docs/Task7_RF_LNA_Report.pdf).

---

## Gallery

<table>
<tr>
<td width="50%"><b>Schematic</b><br><img src="https://github.com/SarHglitch/eSim_PCB_Design_Project_Files/blob/main/files/schematic.png"></td>
<td width="50%"><b>PCB routing (top view)</b><br><img src="https://github.com/SarHglitch/eSim_PCB_Design_Project_Files/blob/main/files/pcb-layout.png"></td>
</tr>
</table>

---


Designed by **Sarah Ezaz Shaikh**
Electrical and Electronics Engineering, University of Visvesvaraya College of Engineering
Submitted for the **FOSSEE Autumn Internship 2026 — Task 7 (PCB Design using eSim)**, IIT Bombay.
