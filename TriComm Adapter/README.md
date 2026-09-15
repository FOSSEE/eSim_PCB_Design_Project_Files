# TriComm Adapter

## Project Overview

The **TriComm Adapter** is a multi-protocol communication interface PCB designed to provide USB connectivity for UART, I²C, and SPI communication through an RJ45 interface. The design integrates multiple dedicated interface controllers with a USB hub to provide a compact and flexible communication adapter for embedded systems and hardware development.

## Features

* USB connectivity through an integrated USB hub.
* USB-to-UART communication using the **CP2102**.
* USB-to-I²C communication using the **CP2112**.
* USB-to-SPI communication using the **CP2130**.
* RJ45 interface for external communication and connectivity.
* On-board 3.3 V power regulation and power selection.
* ESD and power protection provisions.
* Four-layer PCB design with dedicated routing and power/ground planes.
* PCB layout designed and validated using eSim/KiCad.

## Project Files

This directory contains the complete eSim project files, including:

* Schematic files for the main design and hierarchical child sheets.
* PCB layout file.
* eSim project files.
* Netlist and associated project files.
* Supporting files required to open and review the design.

## Validation

The design was subjected to electrical and PCB design validation, including:

* Electrical Rules Check (ERC)
* Design Rules Check (DRC)

The corresponding validation reports are included in the `Documentation` directory.

## Documentation

The project report and ERC/DRC validation reports are provided separately in the `Documentation` directory.

## Tools Used

* **FOSSEE eSim**
* **KiCad**

## Project Type

PCB Design and Hardware Development Project

---

**TriComm Adapter**
Designed as part of the eSim PCB Design Project.
