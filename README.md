# DIY SpO₂ Monitoring PCB

A compact, educational pulse oximeter PCB based on the **Arduino Nano (ATmega328P)**. The board integrates an I²C pulse oximeter sensor module (MAX30100/MAX30102), an SSD1306 OLED display, 3-button navigation, power regulation, and an LED alarm indicator onto a single prototyping PCB designed in KiCad.


---

## Key Features
* **Controller:** Arduino Nano
* **Display:** 0.96" I²C SSD1306 OLED (128×64)
* **Sensor Interface:**  MAX30102 via I²C with interrupt support (`D2`)
* **User Input:** 3 tactile push buttons (`MODE`, `UP`, `DOWN`)
* **Alert System:** Visual LED threshold alarm (`D6`)
* **Design Tool:** KiCad EDA

---

## Repository Structure

```text
My_project/
└── SPo2/
    ├── hardware/
    │   ├── footprints/           # Custom footprint libraries (.pretty / .kicad_mod)
    │   ├── gerbers/              # Fabrication output files
    │   ├── spo2.kicad_pro        # KiCad project file
    │   ├── spo2.kicad_sch        # Schematic file
    │   └── spo2.kicad_pcb        # PCB layout file
    ├── docs/
    │   ├── schematic.pdf         # Schematic reference
    │   └── bom.csv               # Bill of materials
    └── README.md                 # Project documentation
