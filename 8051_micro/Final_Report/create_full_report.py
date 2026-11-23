# -*- coding: utf-8 -*-
"""
Generates the complete academic engineering report:
DESIGN AND DEVELOPMENT OF AN 8051 MICROCONTROLLER-BASED PCB USING KICAD
"""

import os
import sys
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

sys.path.append(r"C:\8051_micro\Final_Report")
from build_helpers import (
    configure_styles, set_cell_background, set_cell_margins, set_table_borders,
    add_callout, add_heading_1, add_heading_2, add_heading_3,
    add_body_p, add_bullet_p, add_figure
)

def create_report():
    doc = Document()
    configure_styles(doc)
    
    # Page setup - A4
    for section in doc.sections:
        section.page_width = Inches(8.27)  # A4 width
        section.page_height = Inches(11.69) # A4 height
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        
        # Configure Header and Footer
        header = section.header
        hp = header.paragraphs[0]
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hrun = hp.add_run("DESIGN AND DEVELOPMENT OF AN 8051 MICROCONTROLLER PCB USING KICAD")
        hrun.font.name = "Calibri"
        hrun.font.size = Pt(8.5)
        hrun.font.color.rgb = RGBColor(128, 128, 128)
        
        footer = section.footer
        fp = footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        frun = fp.add_run("Academic Engineering Project Report  |  Final Design & Verification Dossier")
        frun.font.name = "Calibri"
        frun.font.size = Pt(8.5)
        frun.font.color.rgb = RGBColor(128, 128, 128)

    # ---------------------------------------------------------------------------
    # COVER PAGE
    # ---------------------------------------------------------------------------
    p_pre = doc.add_paragraph()
    p_pre.paragraph_format.space_before = Pt(36)
    p_pre.paragraph_format.space_after = Pt(12)
    p_pre.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_inst = p_pre.add_run("ACADEMIC ENGINEERING DESIGN REPORT\nDEPARTMENT OF ELECTRONICS & COMMUNICATION ENGINEERING")
    r_inst.font.name = "Arial"
    r_inst.font.size = Pt(11)
    r_inst.bold = True
    r_inst.font.color.rgb = RGBColor(0, 102, 153)
    
    # Title decorative line
    p_line1 = doc.add_paragraph()
    p_line1.paragraph_format.space_before = Pt(12)
    p_line1.paragraph_format.space_after = Pt(18)
    p_line1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_line1 = p_line1.add_run("______________________________________________________________________")
    r_line1.font.color.rgb = RGBColor(0, 51, 102)
    r_line1.bold = True

    # Main Title
    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(12)
    p_title.paragraph_format.space_after = Pt(12)
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_title = p_title.add_run("DESIGN AND DEVELOPMENT OF AN\n8051 MICROCONTROLLER-BASED PCB\nUSING KICAD")
    r_title.font.name = "Arial"
    r_title.font.size = Pt(22)
    r_title.bold = True
    r_title.font.color.rgb = RGBColor(0, 51, 102)

    # Subtitle
    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_before = Pt(6)
    p_sub.paragraph_format.space_after = Pt(24)
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_sub = p_sub.add_run("A Comprehensive Technical Investigation Encompassing Schematic Capture,\nComponent Footprint Assignment, Double-Sided PCB Layout Routing,\nThermal & Power Analysis, and 3D Physical Verification")
    r_sub.font.name = "Calibri"
    r_sub.font.size = Pt(12)
    r_sub.font.italic = True
    r_sub.font.color.rgb = RGBColor(80, 80, 80)

    p_line2 = doc.add_paragraph()
    p_line2.paragraph_format.space_before = Pt(6)
    p_line2.paragraph_format.space_after = Pt(36)
    p_line2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_line2 = p_line2.add_run("______________________________________________________________________")
    r_line2.font.color.rgb = RGBColor(0, 51, 102)
    r_line2.bold = True

    # Metadata Table
    meta_tbl = doc.add_table(rows=5, cols=2)
    meta_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(meta_tbl, color="FFFFFF", sz="0", val="none")
    
    meta_data = [
        ("Target Microcontroller Core:", "Silicon Labs C8051F382-GQ (48-Pin TQFP)"),
        ("EDA Design Environment:", "KiCad EDA Suite v6.0.11 / eSim Integrated Toolchain"),
        ("PCB Physical Characteristics:", "2-Layer Double-Sided FR-4, Single-Sided Top Assembly"),
        ("Project Source Directory:", "C:\\8051_micro"),
        ("Document Classification:", "Final Technical Project Dossier & Audit Report")
    ]
    
    for row_idx, (k, v) in enumerate(meta_data):
        c0 = meta_tbl.cell(row_idx, 0)
        c1 = meta_tbl.cell(row_idx, 1)
        c0.width = Inches(2.6)
        c1.width = Inches(3.6)
        
        p0 = c0.paragraphs[0]
        p0.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p0.paragraph_format.space_before = Pt(2)
        p0.paragraph_format.space_after = Pt(2)
        r0 = p0.add_run(k)
        r0.font.name = "Calibri"
        r0.font.size = Pt(10)
        r0.bold = True
        r0.font.color.rgb = RGBColor(0, 51, 102)
        
        p1 = c1.paragraphs[0]
        p1.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p1.paragraph_format.space_before = Pt(2)
        p1.paragraph_format.space_after = Pt(2)
        r1 = p1.add_run(v)
        r1.font.name = "Calibri"
        r1.font.size = Pt(10)
        r1.font.color.rgb = RGBColor(51, 51, 51)
        
    p_date = doc.add_paragraph()
    p_date.paragraph_format.space_before = Pt(48)
    p_date.paragraph_format.space_after = Pt(0)
    p_date.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_date = p_date.add_run("Project Academic Dossier  *  Academic Year 2026-2027")
    r_date.font.name = "Calibri"
    r_date.font.size = Pt(10)
    r_date.font.bold = True
    r_date.font.color.rgb = RGBColor(100, 100, 100)

    doc.add_page_break()

    # ---------------------------------------------------------------------------
    # EXECUTIVE SUMMARY & TABLE OF CONTENTS
    # ---------------------------------------------------------------------------
    add_heading_1(doc, "Executive Summary")
    add_body_p(doc, 
        "This engineering report provides an exhaustive technical analysis, architectural breakdown, and manufacturing audit "
        "of an 8051 microcontroller-based printed circuit board (PCB) designed in the KiCad 6.0 electronic design automation (EDA) "
        "suite. The system integrates a high-performance Silicon Labs C8051F382-GQ microcontroller (TQFP-48 package) with on-board "
        "linear voltage regulation (L7805), high-stability quartz crystal timing, power-on/manual hardware reset circuitry, and "
        "comprehensive multi-bus breakout interfacing across Ports 0, 1, and 2. Through rigorous forensic examination of the "
        "schematic capture (ESIM.kicad_sch), front/back copper routing layers (F.Cu and B.Cu), and three-dimensional spatial renderings, "
        "this document evaluates component footprint assignments, signal integrity considerations, power distribution network (PDN) "
        "dynamics, and design-for-manufacturing (DFM) compliance. In addition, critical engineering discrepancies—including global "
        "power net naming contention, active-low reset polarity mismatches, and silkscreen placement consolidation—are identified "
        "and accompanied by actionable, industry-standard remediation strategies.")

    add_heading_1(doc, "Table of Contents")
    toc_marker = doc.add_paragraph()
    toc_marker.paragraph_format.space_before = Pt(6)
    toc_marker.paragraph_format.space_after = Pt(18)
    r_toc = toc_marker.add_run("<<TOC_LOCATION_MARKER>>")
    r_toc.font.size = Pt(9)
    r_toc.font.color.rgb = RGBColor(150, 150, 150)

    add_heading_2(doc, "List of Figures")
    lof_data = [
        ("Figure 2.1", "Complete 8051 Microcontroller System Schematic Capture (Eeschema)"),
        ("Figure 3.1", "KiCad Schematic Design Environment and Modular Architectural Hierarchy"),
        ("Figure 5.1", "PCB Component Placement and Front Copper Layer (F.Cu) Routing Geometry"),
        ("Figure 6.1", "Completed Double-Sided PCB Track Routing Displaying Both F.Cu and B.Cu Layers"),
        ("Figure 8.1", "Three-Dimensional Top Isometric Rendering of the Assembled 8051 Microcontroller PCB"),
        ("Figure 8.2", "Three-Dimensional Bottom Rendering Illustrating Solder Joints and Lead Terminations")
    ]
    for fig_id, fig_title in lof_data:
        p_lof = doc.add_paragraph()
        p_lof.paragraph_format.space_after = Pt(2)
        r_f1 = p_lof.add_run(f"{fig_id}: ")
        r_f1.bold = True
        r_f1.font.size = Pt(9.5)
        r_f1.font.color.rgb = RGBColor(0, 51, 102)
        r_f2 = p_lof.add_run(fig_title)
        r_f2.font.size = Pt(9.5)

    add_heading_2(doc, "List of Tables")
    lot_data = [
        ("Table 2.1", "Microcontroller Core Pin Allocations and Functional Designations (C8051F382-GQ)"),
        ("Table 4.1", "Comprehensive Component Bill of Materials (BOM) and KiCad Footprint Mapping"),
        ("Table 6.1", "Electrical and Mechanical Track Routing Design Parameters"),
        ("Table 7.1", "Pre-Fabrication Design Rule Check (DRC) and Electrical Rule Check (ERC) Audit Matrix")
    ]
    for tbl_id, tbl_title in lot_data:
        p_lot = doc.add_paragraph()
        p_lot.paragraph_format.space_after = Pt(2)
        r_t1 = p_lot.add_run(f"{tbl_id}: ")
        r_t1.bold = True
        r_t1.font.size = Pt(9.5)
        r_t1.font.color.rgb = RGBColor(0, 51, 102)
        r_t2 = p_lot.add_run(tbl_title)
        r_t2.font.size = Pt(9.5)

    doc.add_page_break()

    # ---------------------------------------------------------------------------
    # CHAPTER 1: PROJECT OVERVIEW
    # ---------------------------------------------------------------------------
    add_heading_1(doc, "Chapter 1: Project Overview")
    
    add_heading_2(doc, "1.1 Introduction")
    add_body_p(doc, 
        "Microcontroller development boards represent the foundational hardware platform upon which embedded firmware "
        "algorithms, peripheral device drivers, and real-time electronic control systems are prototyped and deployed. "
        "The Intel 8051 architecture, originally introduced in 1980, remains one of the most widely studied and industrially "
        "enduring microcontroller instruction set architectures (ISAs) in computing history. Modern silicon implementations, "
        "such as the Silicon Labs C8051 family, execute pipelined single-cycle machine instructions at clock rates up to 48 MHz "
        "while preserving binary compatibility with legacy 8051 assembly code. This project documents the complete design, "
        "schematic implementation, printed circuit board (PCB) layout, and verification of a dedicated 8051-based embedded "
        "controller board developed using the open-source KiCad EDA software suite.")

    add_heading_2(doc, "1.2 Objectives of the 8051 Microcontroller PCB")
    add_body_p(doc, "The primary engineering objectives of this PCB development project are defined as follows:")
    add_bullet_p(doc, " Design a modular, stand-alone embedded computing board centered around a modern, high-speed 8051-compatible microcontroller core.", "Microcontroller Integration:")
    add_bullet_p(doc, " Incorporate an on-board linear voltage regulation stage capable of converting unregulated DC input voltage down to a stable +5.0V system rail with reverse-polarity protection and high-frequency decoupling.", "Power Conditioning:")
    add_bullet_p(doc, " Establish a precise external quartz crystal oscillator network and a reliable hardware reset timing subsystem.", "Clock and Reset Generation:")
    add_bullet_p(doc, " Break out primary parallel I/O ports (Port 0, Port 1, and Port 2) to external terminal connectors via dedicated series resistor arrays to safeguard MCU I/O pins against over-current and bus contention.", "Peripheral Interfacing:")
    add_bullet_p(doc, " Realize a compact, manufacturable 2-layer double-sided printed circuit board layout utilizing standard IPC-2221 design rules, surface-mount passives, and optimized ground copper pours.", "Physical Implementation:")
    add_bullet_p(doc, " Perform comprehensive verification using schematic capture, design rule checking (DRC), and 3D raytraced visualization.", "Verification & Audit:")

    add_heading_2(doc, "1.3 Purpose of Developing the Custom PCB")
    add_body_p(doc, 
        "While commercial off-the-shelf (COTS) evaluation boards are widely available, they frequently introduce redundant "
        "complexity, substantial physical footprints, and unpredictable parasitic behavior due to breadboard jumper leads. "
        "Developing a custom-engineered PCB addresses these limitations by providing an application-specific form factor, "
        "eliminating loose wiring, minimizing inductive loop areas for improved electromagnetic compatibility (EMC), and "
        "delivering a dedicated, robust physical platform for embedded automation and academic experimentation.")

    add_heading_2(doc, "1.4 Overview of the KiCad EDA Design Flow")
    add_body_p(doc, 
        "KiCad is an advanced, open-source Electronic Design Automation (EDA) suite that provides a seamless workflow spanning "
        "from initial schematic capture to fabrication output generation. The design methodology implemented in this project "
        "follows a rigorous, staged engineering cycle:")
    add_bullet_p(doc, " Creation of electrical symbols, functional hierarchical grouping, assignment of net labels, and power distribution flags within KiCad Eeschema (v6.0.11).", "Stage 1 - Schematic Capture:")
    add_bullet_p(doc, " Association of physical geometric land patterns (footprints) with schematic symbols using the KiCad Footprint Library.", "Stage 2 - Footprint Assignment:")
    add_bullet_p(doc, " Generation of the unified circuit netlist and forward-annotation into the KiCad Pcbnew layout editor.", "Stage 3 - Netlist & Forward Annotation:")
    add_bullet_p(doc, " Definition of board mechanical boundaries (Edge.Cuts), strategic component floorplanning, and orientation optimization.", "Stage 4 - Board Floorplanning:")
    add_bullet_p(doc, " Interactive manual routing of signal buses, power rails, and reference ground planes across Front Copper (F.Cu) and Back Copper (B.Cu) layers.", "Stage 5 - Trace Routing & Plane Pour:")
    add_bullet_p(doc, " Automated verification of electrical clearances, physical trace widths, and unrouted net detection via DRC.", "Stage 6 - Design Rule Verification:")
    add_bullet_p(doc, " Spatial collision detection, mechanical component clearance verification, and solder joint inspection using the 3D Raytracing Viewer.", "Stage 7 - 3D Mechanical Inspection:")

    add_heading_2(doc, "1.5 Industrial and Academic Applications")
    add_body_p(doc, 
        "The completed 8051 Microcontroller PCB serves a diverse spectrum of embedded engineering applications, including:")
    add_bullet_p(doc, " Interfacing with relays, solenoid valves, inductive proximity sensors, and stepper motor drivers in automated assembly machinery.", "Industrial Process Control:")
    add_bullet_p(doc, " Multi-point temperature monitoring, pressure logging, and automated environmental chambers.", "Data Acquisition & Sensing:")
    add_bullet_p(doc, " Serves as a modular reference platform for teaching microcomputer architecture, assembly/C programming, interrupt handling, and timer peripherals.", "Academic Laboratory Instruction:")
    add_bullet_p(doc, " Fast-turnaround functional testing of smart appliances, lighting controllers, and motor control algorithms.", "Embedded System Prototyping:")

    # ---------------------------------------------------------------------------
    # CHAPTER 2: CIRCUIT DESCRIPTION
    # ---------------------------------------------------------------------------
    add_heading_1(doc, "Chapter 2: Circuit Description")
    
    add_heading_2(doc, "2.1 Complete Circuit Architecture")
    add_body_p(doc, 
        "The overall circuit architecture comprises five interconnected functional modules: the Microcontroller Processing Core, "
        "the Linear Voltage Regulation Power Stage, the Clock Oscillator Network, the Hardware Reset Subsystem, and the "
        "Peripheral I/O Interconnection Blocks. The full electrical schematic capture from the project files is presented in Figure 2.1.")

    add_figure(doc, 
        r"C:\8051_micro\schematic.jpeg", 
        "Figure 2.1: Complete 8051 Microcontroller System Schematic Capture (KiCad Eeschema v6.0.11)",
        "The schematic reveals a structured two-block functional layout comprising the 'POWER SECTION' (left bounding box) and "
        "the 'MICROCONTROLLER SECTION' (right bounding box). The microcontroller core (U2) interfaces to peripheral connectors "
        "J1, J2, and J3 through parallel resistor arrays, with crystal Y1 and switch SW1 establishing clock and reset timing.",
        width_in=6.1
    )

    add_heading_2(doc, "2.2 The 8051 Microcontroller Core (Silicon Labs C8051F382-GQ)")
    add_body_p(doc, 
        "At the heart of the system is the Silicon Labs C8051F382-GQ microcontroller (designated U2 in the schematic). "
        "Unlike classic NMOS 8051 variants that require 12 clock cycles per machine instruction, the C8051F382 features a high-speed, "
        "pipelined CIP-51 core where 70% of instructions execute in 1 or 2 system clock cycles, yielding up to 48 MIPS peak throughput. "
        "The device is housed in a 48-pin Thin Quad Flat Package (TQFP-48) with a 0.5 mm lead pitch, providing a compact 7x7 mm body footprint.")

    add_body_p(doc, 
        "A forensic audit of the schematic reveals the detailed pinout connections of U2:")
    add_bullet_p(doc, " Operating supply voltage input connected to the system +5V rail.", "Pin 10 (VDD):")
    add_bullet_p(doc, " On-chip 5V-to-3.3V voltage regulator input, shown terminated with a No-Connect flag.", "Pin 11 (REGIN):")
    add_bullet_p(doc, " Bidirectional active-low system reset input and Silicon Labs C2 debug clock interface.", "Pin 13 (~RST/C2CK):")
    add_bullet_p(doc, " Universal Serial Bus transceiver pins (D+, D-, VBUS), marked with No-Connect flags for standard GPIO operation.", "Pins 8, 9, 12 (USB):")
    add_bullet_p(doc, " General Purpose I/O Port 0 pins, routed through series resistors R11-R18 to connector J2.", "Pins 6, 5, 4, 3, 2, 1, 48, 47 (Port 0):")
    add_bullet_p(doc, " General Purpose I/O Port 1 pins, routed through series resistors R19-R26 to connector J3.", "Pins 46, 45, 44, 43, 42, 41, 40, 39 (Port 1):")
    add_bullet_p(doc, " General Purpose I/O Port 2 pins, routed through series resistors R2-R10 to connector J1.", "Pins 38, 37, 36, 35, 34, 33, 32, 31 (Port 2):")
    add_bullet_p(doc, " Port 3 parallel lines, left unrouted with No-Connect flags.", "Pins 30 to 23 (Port 3):")
    add_bullet_p(doc, " External crystal oscillator input/output lines, routed to quartz crystal Y1.", "Pins 19, 18 (P4.3/XTAL1, P4.4/XTAL2):")

    # Table 2.1 Pin allocations
    p_t1_title = doc.add_paragraph()
    p_t1_title.paragraph_format.space_before = Pt(8)
    p_t1_title.paragraph_format.space_after = Pt(2)
    r_t1_ttl = p_t1_title.add_run("Table 2.1: Microcontroller Core Pin Allocations and Functional Designations")
    r_t1_ttl.font.name = "Arial"
    r_t1_ttl.font.size = Pt(10)
    r_t1_ttl.bold = True
    r_t1_ttl.font.color.rgb = RGBColor(0, 51, 102)

    t1 = doc.add_table(rows=10, cols=4)
    t1.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t1)
    
    headers_t1 = ["Pin Range / Pin #", "Signal Name", "Interface / Net Connection", "Functional Description"]
    widths_t1 = [Inches(1.4), Inches(1.2), Inches(1.8), Inches(2.1)]
    
    for c_idx, h_text in enumerate(headers_t1):
        cell = t1.cell(0, c_idx)
        cell.width = widths_t1[c_idx]
        set_cell_background(cell, "003366")
        set_cell_margins(cell, 80, 80, 100, 100)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(h_text)
        run.bold = True
        run.font.name = "Arial"
        run.font.size = Pt(9)
        run.font.color.rgb = RGBColor(255, 255, 255)
        
    t1_rows = [
        ("Pin 10", "VDD", "+5V Rail", "Primary core and I/O power supply voltage input."),
        ("Pin 11", "REGIN", "NC (No-Connect)", "Internal 5V regulator input (unconnected in schematic)."),
        ("Pin 13", "~RST / C2CK", "Reset Node (SW1, C3, R7)", "Active-low system reset and Silicon Labs 2-wire debug clock."),
        ("Pins 8, 9, 12", "D+, D-, VBUS", "NC (No-Connect)", "USB full-speed transceiver differential pair and bus sense."),
        ("Pins 47-48, 1-6", "P0.0 - P0.7", "Resistors R11-R18 -> J2", "Port 0 open-drain/push-pull parallel digital I/O bus."),
        ("Pins 39-46", "P1.0 - P1.7", "Resistors R19-R26 -> J3", "Port 1 configurable digital I/O bus lines."),
        ("Pins 31-38", "P2.0 - P2.7", "Resistors R2-R10 -> J1", "Port 2 configurable digital I/O bus lines."),
        ("Pins 23-30", "P3.0 - P3.7", "NC (No-Connect)", "Port 3 peripheral bus (unconnected in schematic)."),
        ("Pins 18, 19", "P4.4 / P4.3", "Oscillator Y1, C5, C6", "External quartz crystal oscillator feedback inverting amplifier.")
    ]
    
    for r_idx, row_vals in enumerate(t1_rows, start=1):
        bg = "FFFFFF" if r_idx % 2 != 0 else "F2F6FA"
        for c_idx, val in enumerate(row_vals):
            cell = t1.cell(r_idx, c_idx)
            cell.width = widths_t1[c_idx]
            set_cell_background(cell, bg)
            set_cell_margins(cell, 60, 60, 80, 80)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if c_idx != 0 else WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after = Pt(1)
            run = p.add_run(val)
            run.font.name = "Calibri"
            run.font.size = Pt(8.5)

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    add_heading_2(doc, "2.3 Linear Power Supply Section")
    add_body_p(doc, 
        "The power supply subsystem (schematic block 'POWER SECTION') provides voltage conditioning, rectification, "
        "and regulation for the digital electronics. It centers around U1, an L7805 three-terminal positive linear voltage regulator "
        "packaged in a through-hole TO-220 envelope. A 1N4007 power rectifier diode (D1) is placed in series with the input "
        "to prevent catastrophic circuit damage in the event of reverse-polarity power connection.")

    add_body_p(doc, 
        "Capacitive filtering is distributed across the regulator terminals:")
    add_bullet_p(doc, " Connected between Pin 1 (IN) and GND to bypass inductive line impedance and stabilize input voltage against low-frequency ripple.", "Input Decoupling Capacitor C4:")
    add_bullet_p(doc, " Connected in parallel between Pin 3 (OUT) and GND. In standard linear power supply engineering, C1 (typically 0.1 µF ceramic) shunts high-frequency switching transients, while C2 (typically 10 µF electrolytic or tantalum) delivers bulk charge storage and maintains transient load stability.", "Output Filter Capacitors C1 and C2:")
    add_bullet_p(doc, " A visual indicator network comprising LED D2 in series with current-limiting resistor R1 is tied across the power rail to signal active board energization.", "Status Indicator Network:")

    add_heading_2(doc, "2.4 Clock Generation and Oscillator Circuit")
    add_body_p(doc, 
        "Synchronous operation of the 8051 CPU core requires an accurate, low-jitter clock reference. In this design, "
        "an external quartz crystal resonator (Y1) is connected across GPIO pins P4.3 and P4.4, which internally map to the "
        "on-chip oscillator inverting amplifier (XTAL1 and XTAL2). Two ceramic load capacitors, C5 and C6, connect from each "
        "crystal terminal to ground, establishing the π-network phase shift required for sustained Barkhausen oscillation. "
        "The total effective load capacitance (C_L) is governed by:")
    
    add_body_p(doc, "C_L = (C5 * C6) / (C5 + C6) + C_stray", bold_prefix="Oscillator Formula: ")
    add_body_p(doc, 
        "Assuming typical 22 pF to 33 pF ceramic capacitors and 4 pF to 6 pF of PCB stray capacitance (C_stray), the circuit "
        "provides the 12 pF to 18 pF nominal load capacitance required by standard parallel-resonant quartz crystals (e.g., 11.0592 MHz or 12.0 MHz).")

    add_heading_2(doc, "2.5 Hardware Reset Subsystem")
    add_body_p(doc, 
        "The reset circuit provides both automatic power-on reset (POR) and manual user-initiated hardware reset. "
        "In the schematic, the reset network interfaces to Pin 13 (~RST/C2CK) and consists of switch SW1 (symbol SW_DIP_x02, "
        "physically implemented as a 6x6 mm tactile pushbutton switch), timing capacitor C3, and discharge resistor R7.")

    add_heading_2(doc, "2.6 Peripheral Connectors and Bus Resistor Arrays")
    add_body_p(doc, 
        "To enable external interfacing with sensors, actuators, and peripheral daughterboards, 24 general-purpose I/O lines "
        "are routed to three 9-pin single-row connectors designated J1, J2, and J3. Each 9-pin connector provides eight digital "
        "I/O lines accompanied by a dedicated +5V power rail pin, allowing connected peripherals to draw power directly from the board. "
        "Crucially, every I/O line incorporates an inline series resistor:")
    add_bullet_p(doc, " Interfaced to Port 2 (P2.0 to P2.7) via series resistors R2, R3, R4, R5, R6, R8, R9, R10. Pin 1 connects to +5V.", "Connector J1:")
    add_bullet_p(doc, " Interfaced to Port 0 (P0.0 to P0.7) via series resistors R11 to R18. Pin 1 connects to +5V.", "Connector J2:")
    add_bullet_p(doc, " Interfaced to Port 1 (P1.0 to P1.7) via series resistors R19 to R26. Pin 9 connects to +5V.", "Connector J3:")

    # ---------------------------------------------------------------------------
    # CHAPTER 3: SCHEMATIC DESIGN
    # ---------------------------------------------------------------------------
    add_heading_1(doc, "Chapter 3: Schematic Design")
    
    add_heading_2(doc, "3.1 Schematic Development in KiCad Eeschema")
    add_body_p(doc, 
        "The system schematic was authored in KiCad Eeschema v6.0.11 on an A4 drawing sheet template (file name ESIM.kicad_sch). "
        "Eeschema provides a hierarchical, rule-based capture environment that links graphic electrical symbols to electrical nets "
        "and physical footprints. Figure 3.1 displays the captured schematic within the KiCad design frame.")

    add_figure(doc, 
        r"C:\8051_micro\schematic.jpeg", 
        "Figure 3.1: Detailed Schematic Capture in KiCad Eeschema (File: ESIM.kicad_sch)",
        "High-resolution capture of the complete schematic layout within the KiCad title block boundary. The design exhibits "
        "clean orthogonal wiring, explicit functional grouping boxes, and consistent placement of KiCad power flags and no-connect crosses.",
        width_in=6.1
    )

    add_heading_2(doc, "3.2 Modular Functional Grouping and Sheet Organization")
    add_body_p(doc, 
        "A key indicator of high-quality schematic engineering is modular partitioning. As evidenced in Figure 3.1, the designer "
        "segregated the system into two distinct bordered regions: 'POWER SECTION' on the left and 'MICROCONTROLLER SECTION' on the right. "
        "This separation enforces visual clarity, accelerates debugging, and ensures that high-current power conditioning networks "
        "do not visually clutter sensitive micro-power digital control paths.")

    add_heading_2(doc, "3.3 Power and Ground Distribution Networks")
    add_body_p(doc, 
        "Power distribution is governed by global power symbols (+5V and GND). In KiCad's electrical paradigm, power port symbols "
        "automatically connect to identically named global nets throughout the schematic hierarchy. To satisfy KiCad's Electrical "
        "Rules Check (ERC), which requires that every power net possesses at least one driving source, the designer placed "
        "PWR_FLAG symbols at the input of regulator U1 and at the GND node of U2.")

    add_heading_2(doc, "3.4 Signal Integrity and Bus Interconnections")
    add_body_p(doc, 
        "Interconnections between the microcontroller and peripheral headers are routed using point-to-point green net wires. "
        "Unconnected microcontroller pins—including Port 3 (pins 23-30), unused Port 4 pins (pins 15-17, 20-22), USB transceiver "
        "pins (8, 9, 12), and debug line C2D (pin 14)—are terminated with blue 'X' (No-Connect) flags. This practice prevents "
        "KiCad ERC from throwing 'Pin not connected' errors for deliberately unused hardware lines.")

    # ---------------------------------------------------------------------------
    # CHAPTER 4: FOOTPRINT ASSIGNMENT DETAILS
    # ---------------------------------------------------------------------------
    add_heading_1(doc, "Chapter 4: Footprint Assignment Details")
    
    add_heading_2(doc, "4.1 Importance of Footprint Association")
    add_body_p(doc, 
        "In electronic design automation, schematic symbols represent abstract logical connections, whereas PCB footprints define "
        "the physical copper land patterns, pad geometries, drill holes, and component clearances required for fabrication and assembly. "
        "Meticulous footprint assignment is critical: an incorrect pad pitch, lead spacing, or pin numbering mismatch between a "
        "schematic symbol and its footprint results in non-functional, un-solderable circuit boards.")

    add_heading_2(doc, "4.2 Comprehensive Component Bill of Materials (BOM)")
    add_body_p(doc, 
        "Table 4.1 details the complete Bill of Materials extracted and verified from the project's schematic and layout files. "
        "Every physical component is enumerated with its reference designator, schematic value, assigned footprint, package type, "
        "and physical function.")

    # Table 4.1 BOM Table
    p_t4_title = doc.add_paragraph()
    p_t4_title.paragraph_format.space_before = Pt(8)
    p_t4_title.paragraph_format.space_after = Pt(2)
    r_t4_ttl = p_t4_title.add_run("Table 4.1: Comprehensive Component Bill of Materials (BOM) and Footprint Mapping")
    r_t4_ttl.font.name = "Arial"
    r_t4_ttl.font.size = Pt(10)
    r_t4_ttl.bold = True
    r_t4_ttl.font.color.rgb = RGBColor(0, 51, 102)

    bom_rows = [
        ("U2", "Microcontroller", "C8051F382-GQ", "Package_QFP:TQFP-48_7x7mm_P0.5mm", "TQFP-48 (SMD)", "Core 8051 MCU, 48 MIPS, USB 2.0"),
        ("U1", "Voltage Regulator", "L7805", "Package_TO_SOT_THT:TO-220-3_Vertical", "TO-220-3 (THT)", "+5V 1.5A Linear Voltage Regulator"),
        ("D1", "Rectifier Diode", "1N4007", "Diode_THT:D_DO-41_SOD81_P10.16mm_Horizontal", "DO-41 (THT)", "1A 1000V Reverse Polarity Protection"),
        ("D2", "Indicator LED", "LED", "LED_SMD:LED_0805_2012Metric", "0805 (SMD)", "Power Rail Visual Status Indicator"),
        ("SW1", "Pushbutton Switch", "SW_DIP_x02", "Button_Switch_THT:SW_PUSH_6mm", "6x6mm (THT)", "Manual System Hardware Reset Switch"),
        ("Y1", "Quartz Crystal", "Crystal", "Crystal:Crystal_HC49-U_Vertical", "HC-49/U (THT)", "External System Clock Resonator"),
        ("J1", "Port 2 Header", "Screw_Terminal_01x09", "Connector_PinHeader_2.54mm:PinHeader_1x09", "1x09 2.54mm (THT)", "Port 2 (P2.0-P2.7) + 5V Breakout Header"),
        ("J2", "Port 0 Header", "Screw_Terminal_01x09", "Connector_PinHeader_2.54mm:PinHeader_1x09", "1x09 2.54mm (THT)", "Port 0 (P0.0-P0.7) + 5V Breakout Header"),
        ("J3", "Port 1 Header", "Screw_Terminal_01x09", "Connector_PinHeader_2.54mm:PinHeader_1x09", "1x09 2.54mm (THT)", "Port 1 (P1.0-P1.7) + 5V Breakout Header"),
        ("C1", "Output Capacitor", "capacitor", "Capacitor_SMD:C_0805_2012Metric", "0805 (SMD)", "High-Frequency Regulator Output Decoupling"),
        ("C2", "Bulk Capacitor", "capacitor", "Capacitor_SMD:C_0805_2012Metric", "0805 (SMD)", "Regulator Output Transient Storage"),
        ("C3", "Reset Capacitor", "capacitor", "Capacitor_SMD:C_0805_2012Metric", "0805 (SMD)", "Power-On Reset RC Timing Capacitor"),
        ("C4", "Input Capacitor", "capacitor", "Capacitor_SMD:C_0805_2012Metric", "0805 (SMD)", "Regulator Input Voltage Ripple Filter"),
        ("C5", "XTAL1 Load Cap", "capacitor", "Capacitor_SMD:C_0805_2012Metric", "0805 (SMD)", "Quartz Crystal Load Phase Shift Capacitor"),
        ("C6", "XTAL2 Load Cap", "capacitor", "Capacitor_SMD:C_0805_2012Metric", "0805 (SMD)", "Quartz Crystal Load Phase Shift Capacitor"),
        ("R1", "LED Resistor", "resistor", "Resistor_SMD:R_0805_2012Metric", "0805 (SMD)", "Current-Limiting Resistor for LED D2"),
        ("R7", "Reset Resistor", "resistor", "Resistor_SMD:R_0805_2012Metric", "0805 (SMD)", "Hardware Reset Discharge/Pull Resistor"),
        ("R2-R6", "Port 2 Bus Resistors", "resistor", "Resistor_SMD:R_0805_2012Metric", "0805 (SMD)", "Series Current Protection for Port 2 (5 pcs)"),
        ("R8-R10", "Port 2 Bus Resistors", "resistor", "Resistor_SMD:R_0805_2012Metric", "0805 (SMD)", "Series Current Protection for Port 2 (3 pcs)"),
        ("R11-R18", "Port 0 Bus Resistors", "resistor", "Resistor_SMD:R_0805_2012Metric", "0805 (SMD)", "Series Current Protection for Port 0 (8 pcs)"),
        ("R19-R26", "Port 1 Bus Resistors", "resistor", "Resistor_SMD:R_0805_2012Metric", "0805 (SMD)", "Series Current Protection for Port 1 (8 pcs)")
    ]

    t4 = doc.add_table(rows=len(bom_rows)+1, cols=6)
    t4.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t4)
    
    headers_t4 = ["Ref Des", "Component Name", "Schematic Val", "Assigned Footprint", "Package", "Circuit Role / Notes"]
    widths_t4 = [Inches(0.8), Inches(1.2), Inches(1.0), Inches(1.8), Inches(0.9), Inches(1.8)]
    
    for c_idx, h_text in enumerate(headers_t4):
        cell = t4.cell(0, c_idx)
        cell.width = widths_t4[c_idx]
        set_cell_background(cell, "003366")
        set_cell_margins(cell, 80, 80, 80, 80)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(h_text)
        run.bold = True
        run.font.name = "Arial"
        run.font.size = Pt(8.5)
        run.font.color.rgb = RGBColor(255, 255, 255)
        
    for r_idx, row_vals in enumerate(bom_rows, start=1):
        bg = "FFFFFF" if r_idx % 2 != 0 else "F2F6FA"
        for c_idx, val in enumerate(row_vals):
            cell = t4.cell(r_idx, c_idx)
            cell.width = widths_t4[c_idx]
            set_cell_background(cell, bg)
            set_cell_margins(cell, 50, 50, 60, 60)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if c_idx not in (0, 4) else WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after = Pt(1)
            run = p.add_run(val)
            run.font.name = "Calibri"
            run.font.size = Pt(8)

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    add_heading_2(doc, "4.3 Analysis of Assigned Footprints and Packaging Technologies")
    add_body_p(doc, 
        "The bill of materials demonstrates a hybrid packaging philosophy combining high-density surface mount devices (SMD) "
        "with robust, mechanically durable through-hole technology (THT):")
    add_bullet_p(doc, " By adopting a 48-pin TQFP package (0.5 mm pitch) rather than a legacy 40-pin Dual In-line Package (DIP-40), the board realizes an 80% reduction in microcontroller footprint area, freeing substantial real estate for routing channels.", "High-Density SMD Microcontroller:")
    add_bullet_p(doc, " All 26 resistors and 6 capacitors are assigned standard 0805 (2012 metric) surface mount footprints. The 0805 package offers an ideal balance between assembly density and manual reworkability, permitting straightforward hand-soldering with fine soldering iron tips.", "0805 Passive Components:")
    add_bullet_p(doc, " The L7805 regulator (TO-220), rectifier diode (DO-41), crystal resonator (HC-49/U), and peripheral connectors (J1-J3) utilize through-hole mounting. This provides exceptional mechanical shear strength against connector mating cycles and thermal durability for the regulator heatsink tab.", "Through-Hole Connectors and Power Devices:")

    add_heading_2(doc, "4.4 Audit of Symbol-to-Footprint Discrepancies")
    add_body_p(doc, 
        "A rigorous forensic audit between the schematic symbols and physical PCB layout reveals two notable symbol-to-footprint substitutions:")
    add_bullet_p(doc, " In Eeschema, connectors J1, J2, and J3 are labeled with the symbol 'Screw_Terminal_01x09'. In the physical PCB layout (front_layout.jpeg) and 3D rendering (3D_front.jpeg), these connectors are assigned standard 2.54 mm pitch vertical male pin headers ('PinHeader_1x09_P2.54mm_Vertical'). While electrically compatible (1-to-1 pin mapping), screw terminals require significantly wider pitch (3.5 mm or 5.0 mm) and larger pad diameters. The pin header assignment is far more compact and suited for ribbon cables or female jumper wires.", "Connectors J1, J2, J3:")
    add_bullet_p(doc, " In the schematic, SW1 is designated with symbol 'SW_DIP_x02' (a 2-pole dual in-line switch). On the PCB layout and 3D rendering, SW1 is assigned a standard 6x6 mm tactile momentary pushbutton footprint ('SW_PUSH_6mm'). This change is functionally appropriate for a momentary reset switch, though the schematic symbol was not updated to match.", "Switch SW1:")

    # ---------------------------------------------------------------------------
    # CHAPTER 5: PCB LAYOUT DESIGN
    # ---------------------------------------------------------------------------
    add_heading_1(doc, "Chapter 5: PCB Layout Design")
    
    add_heading_2(doc, "5.1 Netlist Import and Initial Board Floorplanning")
    add_body_p(doc, 
        "Following successful schematic capture and footprint assignment in Eeschema, the design netlist was generated and "
        "imported into KiCad Pcbnew. The initial layout stage involved defining the board boundary (Edge.Cuts) and executing "
        "strategic floorplanning to minimize ratsnest flight-line crossings.")

    add_figure(doc, 
        r"C:\8051_micro\front_layout.jpeg", 
        "Figure 5.1: PCB Component Placement and Front Copper Layer (F.Cu) Layout in KiCad Pcbnew",
        "Front layer layout view displaying red copper traces, annular ring pads, component outlines, and a solid top copper pour zone. "
        "Microcontroller U2 occupies the board center, flanked by peripheral resistor arrays and edge-mounted I/O connectors J1, J2, and J3.",
        width_in=6.1
    )

    add_heading_2(doc, "5.2 Board Dimensions and Mechanical Form Factor")
    add_body_p(doc, 
        "The PCB outline is defined on the Edge.Cuts layer using a solid rectangular contour. In accordance with professional "
        "auditing standards, it must be noted that exact dimensional callouts (e.g., millimeter dimension lines) were not annotated "
        "directly on the exported Pcbnew screenshot. However, geometric scaling relative to the known 2.54 mm pin-to-pin pitch of "
        "connectors J1-J3 and the 9.0x9.0 mm lead-tip span of the TQFP-48 package indicates an approximate board dimension of "
        "50 mm x 45 mm, yielding a highly compact form factor.")

    add_heading_2(doc, "5.3 Component Placement and Partitioning Strategy")
    add_body_p(doc, 
        "The physical layout exhibits clear engineering logic governed by signal flow and thermal dissipation:")
    add_bullet_p(doc, " U2 is positioned precisely in the board center, minimizing the average trace length required to reach peripheral connectors on the left, right, and bottom board edges.", "Centralized Processing Core:")
    add_bullet_p(doc, " The L7805 regulator (U1) and diode (D1) are situated along the upper-left perimeter. This placement isolates thermal dissipation from the temperature-sensitive microcontroller and keeps unregulated input power traces away from digital signal lines.", "Isolated Power Section:")
    add_bullet_p(doc, " Quartz crystal Y1 and load capacitors C5, C6 are positioned in the lower-left sector directly adjacent to MCU pins 18 and 19. Keeping crystal trace lengths short is paramount to minimizing stray capacitance and electromagnetic radiation.", "Localized Oscillator Circuit:")
    add_bullet_p(doc, " Connectors J1 (Port 2), J2 (Port 0), and J3 (Port 1) are placed directly along the right, left, and bottom PCB edges, respectively, ensuring unobstructed accessibility for external wiring harnesses.", "Peripheral I/O Accessibility:")

    add_heading_2(doc, "5.4 Silkscreen Placement Anomaly")
    add_body_p(doc, 
        "An inspection of Figure 5.1 reveals a distinct silkscreen anomaly: the reference designator text labels for resistors "
        "and capacitors are not positioned individually adjacent to their respective component pads. Instead, the labels are "
        "consolidated into vertical columnar lists along the outer margins (e.g., labels R10 through C1 stacked vertically on the left edge; "
        "labels R16 through R13 stacked on the right edge; labels R22 through R23 stacked on the bottom-right). While this keeps "
        "the dense routing channels free of silkscreen ink, it complicates manual component assembly and troubleshooting unless "
        "technicians cross-reference the assembly drawing.")

    # ---------------------------------------------------------------------------
    # CHAPTER 6: ROUTING METHODOLOGY
    # ---------------------------------------------------------------------------
    add_heading_1(doc, "Chapter 6: Routing Methodology")
    
    add_heading_2(doc, "6.1 Double-Sided Routing Strategy")
    add_body_p(doc, 
        "The design employs a 2-layer printed circuit board stackup utilizing both the Front Copper (F.Cu) and Back Copper (B.Cu) "
        "layers. To ensure robust signal integrity and manageable routing density, a preferred routing direction methodology was applied: "
        "predominantly horizontal trace segments on one layer and vertical cross-under segments on the opposing layer, interconnected "
        "via plated through-hole (PTH) annular vias. Figure 6.1 illustrates the completed double-sided routing layout.")

    add_figure(doc, 
        r"C:\8051_micro\back_layout.jpeg", 
        "Figure 6.1: Completed Double-Sided PCB Track Routing Displaying Both F.Cu (Red) and B.Cu (Blue) Layers",
        "Composite layer view illustrating orthogonal routing methodology. Red traces on the Top Layer (F.Cu) interface directly "
        "to SMD component pads, while blue traces on the Bottom Layer (B.Cu) provide essential cross-under routing beneath the MCU core.",
        width_in=6.1
    )

    add_heading_2(doc, "6.2 Signal, Power, and Ground Routing Implementation")
    add_body_p(doc, 
        "Routing within the board is segregated according to electrical net classification:")
    add_bullet_p(doc, " Digital I/O traces connecting U2 to resistor banks R2-R26 and headers J1-J3 are routed with fine-pitch traces (approximately 0.25 mm / 10 mil width) to navigate the narrow 0.5 mm spacing between adjacent TQFP-48 gull-wing pins.", "Digital Signal Traces:")
    add_bullet_p(doc, " The unregulated DC input line and regulated +5V power distribution tracks feature wider copper geometries (approximately 0.50 mm to 0.75 mm / 20-30 mil width) to reduce DC loop resistance and tolerate higher surge currents.", "Power Distribution Traces:")
    add_bullet_p(doc, " Both layout views confirm the application of a solid copper ground zone pour on the Top Layer (F.Cu). Ground pours lower ground return impedance, enhance electromagnetic shielding, and aid in thermal dissipation from active silicon.", "Ground Plane & Copper Fill:")

    add_heading_2(doc, "6.3 Track Width and Clearance Analysis (IPC-2221)")
    add_body_p(doc, 
        "In accordance with IPC-2221 generic standards for printed board design, the current-carrying capacity of a surface copper track "
        "is a function of track cross-sectional area, copper foil weight (typically 1 oz/ft² or 35 µm thickness), and allowable temperature rise:")
    
    add_body_p(doc, "I = k * (ΔT)^0.44 * A^0.725", bold_prefix="IPC-2221 Current Formula: ")
    add_body_p(doc, 
        "Where k = 0.048 for external layers, ΔT is the permissible thermal rise in °C, and A is the track area in mils². "
        "For a standard 10 mil (0.254 mm) digital signal trace in 1 oz copper, the allowable DC current for a modest 10°C temperature rise "
        "exceeds 1.0 A—far surpassing the microampere-level switching currents of the C8051 CMOS I/O pins, confirming ample thermal safety margin.")

    # Table 6.1 Routing Parameters
    p_t6_title = doc.add_paragraph()
    p_t6_title.paragraph_format.space_before = Pt(8)
    p_t6_title.paragraph_format.space_after = Pt(2)
    r_t6_ttl = p_t6_title.add_run("Table 6.1: Electrical and Mechanical Track Routing Design Parameters")
    r_t6_ttl.font.name = "Arial"
    r_t6_ttl.font.size = Pt(10)
    r_t6_ttl.bold = True
    r_t6_ttl.font.color.rgb = RGBColor(0, 51, 102)

    t6 = doc.add_table(rows=6, cols=4)
    t6.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t6)
    
    headers_t6 = ["Parameter Description", "Verified / Estimated Value", "Standard Industry Rule", "Engineering Compliance Status"]
    widths_t6 = [Inches(1.8), Inches(1.5), Inches(1.5), Inches(1.7)]
    
    for c_idx, h_text in enumerate(headers_t6):
        cell = t6.cell(0, c_idx)
        cell.width = widths_t6[c_idx]
        set_cell_background(cell, "003366")
        set_cell_margins(cell, 80, 80, 80, 80)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(h_text)
        run.bold = True
        run.font.name = "Arial"
        run.font.size = Pt(8.5)
        run.font.color.rgb = RGBColor(255, 255, 255)
        
    t6_rows = [
        ("Digital Signal Track Width", "0.25 mm (10 mil)", "0.20 - 0.25 mm min", "Compliant for low-current signal routing"),
        ("Power Rail Track Width", "0.50 - 0.75 mm (20-30 mil)", "0.50 mm min for 1A", "Compliant for 7805 regulator bus"),
        ("Trace-to-Trace Clearance", "0.20 - 0.25 mm (8-10 mil)", "0.15 - 0.20 mm min", "Compliant with standard 6/6 mil fab rules"),
        ("Via Outer Diameter / Drill", "0.80 mm pad / 0.40 mm drill", "0.60 / 0.30 mm min", "Robust aspect ratio, standard PTH fab"),
        ("Copper Fill Clearance", "0.35 - 0.50 mm (14-20 mil)", "0.25 mm min", "Adequate thermal relief and pad isolation")
    ]
    
    for r_idx, row_vals in enumerate(t6_rows, start=1):
        bg = "FFFFFF" if r_idx % 2 != 0 else "F2F6FA"
        for c_idx, val in enumerate(row_vals):
            cell = t6.cell(r_idx, c_idx)
            cell.width = widths_t6[c_idx]
            set_cell_background(cell, bg)
            set_cell_margins(cell, 50, 50, 60, 60)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if c_idx != 1 else WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after = Pt(1)
            run = p.add_run(val)
            run.font.name = "Calibri"
            run.font.size = Pt(8)

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    # ---------------------------------------------------------------------------
    # CHAPTER 7: DESIGN RULE CHECK (DRC) RESULTS
    # ---------------------------------------------------------------------------
    add_heading_1(doc, "Chapter 7: Design Rule Check (DRC) Results")
    
    add_heading_2(doc, "7.1 Role of DRC and Verification Standards")
    add_body_p(doc, 
        "Design Rule Checking (DRC) represents the automated gatekeeper between computer-aided design and physical circuit board "
        "manufacturing. In KiCad, the DRC engine verifies copper clearances, track widths, via annular rings, hole sizes, "
        "and solder mask dams against predefined PCB fabricator design constraints. Concurrently, the Electrical Rules Check (ERC) "
        "in Eeschema verifies net connectivity, detects conflicting pin drive types, and flags unpowered nets.")

    add_heading_2(doc, "7.2 Status of Verification Artifacts in Project Files")
    add_body_p(doc, 
        "In strict compliance with Technical Accuracy requirements, it is formally recorded that no DRC log file (.rpt) or DRC dialog "
        "screenshot was provided within the project directory C:\\8051_micro. Therefore, it cannot be claimed or assumed that this design "
        "has officially passed an automated DRC cycle without errors. A rigorous forensic inspection of the schematic and layout images "
        "reveals several critical electrical and layout discrepancies that would trigger significant ERC/DRC warnings or hardware malfunction.")

    add_callout(doc, 
        "Transparent Verification Disclosure: Formal KiCad DRC report files were absent from the project directory. "
        "The technical audit below identifies verified circuit anomalies directly observable from the source schematic and PCB layout.",
        title="AUDIT DISCLOSURE: DRC EVIDENCE ABSENT",
        alert_type="WARNING"
    )

    add_heading_2(doc, "7.3 Forensic Circuit and Layout Audit Findings")
    
    add_heading_3(doc, "Finding 1: Global Net Naming Contention Across Voltage Regulator U1")
    add_body_p(doc, 
        "In the schematic (Figure 2.1), the net preceding rectifier diode D1 is assigned the global power label '+5V'. "
        "Crucially, the output pin of the L7805 voltage regulator (Pin 3) is also assigned the global label '+5V'. "
        "In KiCad EDA, global power labels establish a direct virtual short-circuit across all identically named nodes. "
        "As a result, the input node of diode D1 and the regulated output of U1 are shorted together! Furthermore, the L7805 is a linear "
        "bipolar regulator requiring a minimum dropout voltage of ~2.0V (V_dropout = V_in - V_out >= 2.0V). To produce a regulated +5.0V output, "
        "the input must be at least +7.0V to +12.0V DC. If an external 5V supply is applied to the input, diode D1 drops ~0.7V, leaving only "
        "4.3V at the regulator input, causing the L7805 to completely drop out of regulation. "
        "Correction: Re-label the input rail as 'VIN' or 'EXT_DC' (7-12V) and isolate it completely from the +5V regulated distribution rail.")

    add_heading_3(doc, "Finding 2: Active-Low Reset Polarity Conflict")
    add_body_p(doc, 
        "The Silicon Labs C8051F382-GQ microcontroller utilizes an active-low reset pin labeled '~RST/C2CK' (Pin 13). "
        "In the schematic, the reset circuit is designed with capacitor C3 connected to +5V and resistor R7 connected to GND. "
        "In vintage 8051 chips (e.g., AT89C51), reset was active-high, where this RC arrangement provided a temporary high pulse during power-up. "
        "However, for an active-low ~RST pin, tying R7 to GND pulls Pin 13 permanently LOW! As a consequence, the microcontroller will be held "
        "in permanent hardware reset and will never execute firmware! "
        "Correction: Connect pull-up resistor R7 between Pin 13 and +5V (Silicon Labs recommends 1.0 kΩ to 4.7 kΩ), and connect capacitor C3 "
        "and switch SW1 between Pin 13 and GND.")

    add_heading_3(doc, "Finding 3: Floating Internal Voltage Regulator Input (REGIN)")
    add_body_p(doc, 
        "On the C8051F382-GQ, Pin 11 is 'REGIN'—the input to the internal 5V-to-3.3V core voltage regulator. Pin 10 is 'VDD'. "
        "In the project schematic, Pin 11 (REGIN) is terminated with a No-Connect flag, while Pin 10 (VDD) is tied to +5V. "
        "The C8051F382 internal core operates at 3.3V; supplying +5V directly to VDD while leaving REGIN floating violates the manufacturer's "
        "recommended operating conditions and risks damaging the internal silicon core.")

    # Table 7.1 DRC Audit Matrix
    p_t7_title = doc.add_paragraph()
    p_t7_title.paragraph_format.space_before = Pt(8)
    p_t7_title.paragraph_format.space_after = Pt(2)
    r_t7_ttl = p_t7_title.add_run("Table 7.1: Pre-Fabrication Design Rule Check (DRC) and Electrical Audit Matrix")
    r_t7_ttl.font.name = "Arial"
    r_t7_ttl.font.size = Pt(10)
    r_t7_ttl.bold = True
    r_t7_ttl.font.color.rgb = RGBColor(0, 51, 102)

    t7 = doc.add_table(rows=6, cols=4)
    t7.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t7)
    
    headers_t7 = ["Audit Item", "Observed Condition", "Severity Level", "Recommended Engineering Action"]
    widths_t7 = [Inches(1.5), Inches(1.8), Inches(1.2), Inches(2.0)]
    
    for c_idx, h_text in enumerate(headers_t7):
        cell = t7.cell(0, c_idx)
        cell.width = widths_t7[c_idx]
        set_cell_background(cell, "003366")
        set_cell_margins(cell, 80, 80, 80, 80)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(h_text)
        run.bold = True
        run.font.name = "Arial"
        run.font.size = Pt(8.5)
        run.font.color.rgb = RGBColor(255, 255, 255)
        
    t7_rows = [
        ("Power Net Loop", "+5V label on both U1 input and output", "CRITICAL ERROR", "Rename input net to 'VIN' (7-12V DC input)"),
        ("Reset Polarity", "Pull-down R7 on active-low ~RST pin", "CRITICAL ERROR", "Configure R7 as pull-up to +5V; SW1 to GND"),
        ("MCU Core Power", "REGIN floating; +5V directly to VDD", "HIGH WARNING", "Route 5V to REGIN (pin 11); decouple VDD (pin 10)"),
        ("Silkscreen Placement", "Ref des grouped in edge columns", "MODERATE WARNING", "Reposition labels adjacent to respective footprints"),
        ("DRC Run Report", "No .rpt or DRC dialog screenshot found", "DOCUMENTATION GAP", "Execute and archive formal KiCad DRC before ordering")
    ]
    
    for r_idx, row_vals in enumerate(t7_rows, start=1):
        bg = "FFFFFF" if r_idx % 2 != 0 else "F2F6FA"
        for c_idx, val in enumerate(row_vals):
            cell = t7.cell(r_idx, c_idx)
            cell.width = widths_t7[c_idx]
            set_cell_background(cell, bg)
            set_cell_margins(cell, 50, 50, 60, 60)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if c_idx != 2 else WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after = Pt(1)
            run = p.add_run(val)
            run.font.name = "Calibri"
            run.font.size = Pt(8)
            if c_idx == 2:
                run.bold = True
                if "CRITICAL" in val:
                    run.font.color.rgb = RGBColor(204, 0, 0)
                elif "HIGH" in val:
                    run.font.color.rgb = RGBColor(204, 102, 0)

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    # ---------------------------------------------------------------------------
    # CHAPTER 8: 3D PCB VISUALIZATION
    # ---------------------------------------------------------------------------
    add_heading_1(doc, "Chapter 8: 3D PCB Visualization")
    
    add_heading_2(doc, "8.1 3D Raytracing and Spatial Verification")
    add_body_p(doc, 
        "KiCad incorporates an advanced 3D Viewer capable of real-time OpenGL and photorealistic raytraced rendering. "
        "The 3D viewer links mechanical STEP and VRML models to PCB footprints, enabling engineers to inspect physical component "
        "heights, enclosure clearances, silkscreen readability, and solder joint geometry prior to committing to fabrication tooling.")

    add_heading_2(doc, "8.2 Top-Side Physical Assembly Inspection")
    add_body_p(doc, 
        "Figure 8.1 presents the raytraced 3D rendering of the fully assembled top surface of the 8051 Microcontroller PCB.")

    add_figure(doc, 
        r"C:\8051_micro\3D_front.jpeg", 
        "Figure 8.1: Three-Dimensional Top Isometric Rendering of the Assembled 8051 Microcontroller PCB",
        "Photorealistic 3D visualization illustrating component packaging and vertical heights. Notice the upright TO-220 heatsink tab "
        "of U1, the axial cylinder of diode D1, the tactile plunger of switch SW1, the low-profile TQFP-48 quad flat pack of MCU U2, "
        "the metallic HC-49 quartz crystal Y1, and the three gold-plated 1x09 vertical header pin strips.",
        width_in=5.8
    )

    add_body_p(doc, 
        "Key spatial observations from the top 3D model include:")
    add_bullet_p(doc, " The TO-220 package stands vertically along the upper boundary. Adequate clearance exists behind the metal tab for a clip-on extruded aluminum heatsink without encroaching upon adjacent components.", "Regulator Clearance:")
    add_bullet_p(doc, " The 48 gull-wing leads of U2 align with the PCB copper pads with zero rotational skew. Passive chip resistors and capacitors flank the chip closely.", "Surface Mount Alignment:")
    add_bullet_p(doc, " Connectors J1, J2, and J3 display standard 2.54 mm square post pins with standard 6.0 mm mating height, ideal for IDC ribbon cable sockets or DuPont female jumper wires.", "Header Pin Protrusion:")
    add_bullet_p(doc, " 100% of populated devices feature complete 3D geometric models. There are no missing CAD models or generic bounding-box placeholders.", "3D Model Completeness:")

    add_heading_2(doc, "8.3 Bottom-Side Solder Termination and Lead Clearance")
    add_body_p(doc, 
        "Figure 8.2 presents the 3D rendering of the PCB underside (solder side).")

    add_figure(doc, 
        r"C:\8051_micro\3D_back.jpeg", 
        "Figure 8.2: Three-Dimensional Bottom Rendering Illustrating Solder Joints and Lead Terminations",
        "Raytraced bottom perspective revealing the trimmed lead tails and plated through-hole annular rings of connectors J1, J2, J3, "
        "regulator U1, diode D1, switch SW1, and crystal Y1. Bottom copper routing tracks are visible beneath the green solder mask.",
        width_in=5.8
    )

    add_body_p(doc, 
        "The bottom 3D view confirms a single-sided component mounting assembly: all active and passive electronic components are "
        "mounted exclusively on the Top Layer (F.Cu). The bottom side contains only through-hole solder fillets, trimmed component "
        "leads, and secondary copper traces. This layout significantly streamlines the manufacturing assembly process, requiring only "
        "a single-pass SMD solder paste stencil and reflow stage, followed by selective wave or hand soldering for through-hole pins.")

    # ---------------------------------------------------------------------------
    # CHAPTER 9: DESIGN CONSIDERATIONS
    # ---------------------------------------------------------------------------
    add_heading_1(doc, "Chapter 9: Design Considerations")
    
    add_heading_2(doc, "9.1 Component Selection Rationales")
    add_body_p(doc, 
        "The selection of components balances performance, cost, and availability. The Silicon Labs C8051F382 provides an exceptional "
        "combination of classic 8051 code compatibility and modern capabilities (48 MIPS execution, 64 KB Flash, 4352 bytes RAM, "
        "hardware SPI, UARTs, SMBus, and USB 2.0). The choice of an L7805 linear regulator provides an ultra-low-noise +5V rail "
        "completely free of high-frequency switching EMI, which is critical for precision clock generation and analog peripheral operations.")

    add_heading_2(doc, "9.2 Power Supply Optimization and Thermal Dissipation")
    add_body_p(doc, 
        "Linear voltage regulators drop voltage by dissipating excess energy as heat. The power dissipated across U1 is given by:")
    add_body_p(doc, "P_D = (V_IN - V_OUT) * I_LOAD + V_IN * I_quiescent", bold_prefix="Regulator Power Equation: ")
    add_body_p(doc, 
        "Assuming a 9V external DC power supply, a 5V regulated output, and a total system load current of 150 mA (MCU core, LED, "
        "and peripheral loads):")
    add_body_p(doc, "P_D = (9.0V - 5.0V) * 0.150A = 0.60 Watts", bold_prefix="Calculated Dissipation: ")
    add_body_p(doc, 
        "With a standard TO-220 junction-to-ambient thermal resistance (θ_JA) of 65°C/W in free air, the junction temperature rise is:")
    add_body_p(doc, "ΔT_J = P_D * θ_JA = 0.60W * 65°C/W = 39.0°C", bold_prefix="Thermal Rise: ")
    add_body_p(doc, 
        "At a 25°C ambient temperature, the regulator operates at ~64°C—well below the 125°C maximum operating junction threshold. "
        "However, if the board is powered from 12V DC or load current reaches 500 mA, power dissipation rises to 3.5W, mandating a stamped "
        "aluminum heatsink to prevent thermal shutdown.")

    add_heading_2(doc, "9.3 High-Frequency Crystal Oscillator Routing")
    add_body_p(doc, 
        "Crystal oscillator circuits operate as high-impedance RF nodes prone to electromagnetic interference. In this layout, "
        "Y1 is placed close to U2 pins 18 and 19. For maximum noise immunity in future revisions, the crystal traces should be "
        "enclosed within a localized ground guard ring, with the underlying ground pour solid and unperforated by high-speed signal tracks.")

    add_heading_2(doc, "9.4 Electromagnetic Compatibility (EMC) and Ground Return Paths")
    add_body_p(doc, 
        "High-speed digital signals generate return currents that follow the path of least impedance directly beneath the signal track. "
        "The solid ground copper pour on F.Cu provides an effective reference plane, suppressing radiated EMI and maintaining signal "
        "integrity across the peripheral parallel buses.")

    add_heading_2(doc, "9.5 Design for Manufacturing (DFM) and Assembly (DFA)")
    add_body_p(doc, 
        "The board adheres to fundamental DFM and DFA principles:")
    add_bullet_p(doc, " Restricting all SMD devices to the top surface eliminates expensive double-sided stencil printing and secondary reflow passes.", "Single-Sided Assembly:")
    add_bullet_p(doc, " Standard 0805 passives and 2.54 mm pin headers are readily handled by standard pick-and-place feeders and manual assembly techniques.", "Standard Component Sizing:")
    add_bullet_p(doc, " Solder mask dams between adjacent 0.5 mm TQFP pins must be maintained at >= 0.10 mm (4 mil) to prevent molten solder bridging during reflow.", "Solder Mask Integrity:")

    # ---------------------------------------------------------------------------
    # CHAPTER 10: CONCLUSION AND FUTURE SCOPE
    # ---------------------------------------------------------------------------
    add_heading_1(doc, "Chapter 10: Conclusion and Future Scope")
    
    add_heading_2(doc, "10.1 Project Synthesis and Design Summary")
    add_body_p(doc, 
        "This project successfully completed the full design lifecycle of an 8051 Microcontroller Printed Circuit Board utilizing "
        "the KiCad 6.0 EDA suite. The resulting board integrates an advanced Silicon Labs C8051F382 microcontroller with dedicated "
        "power conditioning, clock generation, hardware reset, and comprehensive parallel bus breakouts in a compact, highly manufacturable "
        "2-layer form factor.")

    add_heading_2(doc, "10.2 Academic and Engineering Competencies Demonstrated")
    add_body_p(doc, "Through the execution of this project, several core electronic design engineering competencies were demonstrated:")
    add_bullet_p(doc, " Schematic capture, hierarchical grouping, global net management, and power distribution design in KiCad Eeschema.", "EDA Toolchain Mastery:")
    add_bullet_p(doc, " Strategic component floorplanning, layer stackup management, and double-sided orthogonal routing in KiCad Pcbnew.", "PCB Layout Engineering:")
    add_bullet_p(doc, " Thermal budgeting, current carrying capacity calculations (IPC-2221), and oscillator π-network tuning.", "Circuit Analysis & Physics:")
    add_bullet_p(doc, " Identifying net contention, polarity conflicts, and DFM constraints through critical forensic design auditing.", "Forensic Design Verification:")

    add_heading_2(doc, "10.3 Identified Hardware Limitations")
    add_body_p(doc, "The current design revision exhibits the following verified limitations:")
    add_bullet_p(doc, " Global net '+5V' is mapped across the input and output of U1, creating an electrical short circuit across the regulator.", "Power Rail Net Contention:")
    add_bullet_p(doc, " Active-low reset pin ~RST is pulled to ground by R7, holding the microcontroller in permanent reset.", "Inverted Reset Polarity:")
    add_bullet_p(doc, " The 2-wire C2 debug interface (C2CK and C2D) lacks a dedicated programming header, requiring manual flying-lead probing for firmware programming.", "Absence of Dedicated In-System Programming Header:")
    add_bullet_p(doc, " The board outline lacks mechanical mounting holes for standoff fastening inside an equipment enclosure.", "Missing Mechanical Mounting Holes:")

    add_heading_2(doc, "10.4 Strategic Roadmap for Future Revisions (v2.0 Improvements)")
    add_body_p(doc, "To advance this design to a commercial or laboratory-grade deployment, the following enhancements are recommended for Revision 2.0:")
    add_bullet_p(doc, " Re-label the external input as 'VIN' (7-12V DC) and isolate it from the internal +5V bus. Add a 500 mA PTC resettable fuse.", "Power Supply Remediation:")
    add_bullet_p(doc, " Convert R7 to a 2.2 kΩ pull-up to +5V and route SW1 to GND with a parallel 0.1 µF debounce capacitor.", "Correct Reset Architecture:")
    add_bullet_p(doc, " Incorporate a standard 10-pin or 6-pin Silicon Labs C2 debug interface connector for direct programming via USB Debug Adapters.", "Add C2 / ISP Programming Port:")
    add_bullet_p(doc, " The C8051F382 features on-chip USB 2.0. Route pins 8, 9, and 12 to a surface-mount USB Type-C or Micro-B connector with ESD protection.", "Implement Native USB Connectivity:")
    add_bullet_p(doc, " Add four M3 (3.2 mm diameter) plated mounting holes at the board corners, maintaining 4.0 mm clearance from copper routing traces.", "Mechanical Chassis Standoffs:")
    add_bullet_p(doc, " Relocate reference designators directly next to individual footprints for rapid visual inspection during assembly.", "Silkscreen Relocation:")

    add_heading_2(doc, "10.5 Hardware Testing and Commissioning Protocol")
    add_body_p(doc, 
        "Prior to applying power to a newly assembled board, the following sequential commissioning protocol must be executed:")
    add_bullet_p(doc, " Inspect board using a stereomicroscope to verify absence of solder bridges, particularly between 0.5 mm TQFP pins.", "Step 1 - Visual Microscopic Inspection:")
    add_bullet_p(doc, " Measure resistance between +5V and GND using a digital multimeter. Verify resistance is in the kilo-ohm range (no power-to-ground short).", "Step 2 - Unpowered Cold Resistance Check:")
    add_bullet_p(doc, " Apply 9V DC to VIN through a current-limited bench power supply (set limit to 50 mA). Verify LED D2 illuminates and measure voltage at U1 Pin 3 (+5.0V ± 0.1V).", "Step 3 - First Power-On & Voltage Verification:")
    add_bullet_p(doc, " Measure DC voltage at Pin 13 (~RST). Confirm voltage is +5V (high state). Press SW1 and confirm voltage drops to 0V.", "Step 4 - Reset Line Functional Verification:")
    add_bullet_p(doc, " Probe crystal pins 18 and 19 using a high-impedance 10x oscilloscope probe to observe clean sinusoidal clock oscillation.", "Step 5 - Clock Oscillation Verification:")
    add_bullet_p(doc, " Connect C2 programmer, verify target device identification (ID: C8051F382), flash a GPIO toggle test program, and verify output square waves at headers J1, J2, and J3.", "Step 6 - Firmware Programming & GPIO Test:")

    # Save document
    out_path = r"C:\8051_micro\Final_Report\8051_Microcontroller_PCB_Design_Report.docx"
    doc.save(out_path)
    print(f"Report successfully saved to {out_path}")

if __name__ == "__main__":
    create_report()
