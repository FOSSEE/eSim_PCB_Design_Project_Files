# 4-Layer Avionics Flight Computer & Telemetry Node
[![YouTube Watch Demo](https://img.shields.io/badge/YouTube-Watch%20Video%20Demo-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](https://youtu.be/cIcnoNsfvB8)

**Screening Task 7 Submission | FOSSEE eSim Semester Long Internship (Autumn 2026)**

- **Author:** Aayushman Das
- **Department:** Electronics and Telecommunication Engineering (ETCE)
- **Institution:** Jadavpur University, Kolkata
- **Target Platform:** eSim v2.5

---

## Project Overview
A production-grade, 4-layer mixed-signal avionics flight computer and environmental telemetry node designed in eSim v2.5. The board incorporates an ESP32-WROOM-32U microcontroller with U.FL external RF breakout, Quectel L86 GNSS receiver with integrated patch antenna, Bosch BMP390L barometric altimeter, STMicroelectronics LSM6DSOX 6-axis IMU, 128 Mbit SPI NOR Flash, and an AP63203 synchronous buck regulator (7.4V–25.2V input down to 3.3V @ 2A).

## Video Demonstration
- **YouTube Walkthrough:** [Watch Task 7 Video Demonstration](https://youtu.be/cIcnoNsfvB8)

## Key Technical Specifications
- **Stackup:** 4 Layers (F.Cu Top Signal, In1.Cu Solid Ground Plane, In2.Cu Dedicated 3.3V Power Plane, B.Cu Bottom Signal)
- **DRC Validation:** 0 Errors, 0 Unconnected Nets (24 intentional thermal ground via exclusions for MCU1)
- **Portability:** All 3D STEP assets are locally referenced using `${KIPRJMOD}` for clean out-of-the-box loading.

## Deliverables
- Project Report: `eSim_Task7_Flight_Computer_Report_Aayushman_Das.pdf`
- Design Files: Native eSim schematic and PCB layout located in the root directory.
