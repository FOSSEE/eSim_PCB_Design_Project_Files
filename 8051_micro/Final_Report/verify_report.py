# -*- coding: utf-8 -*-
"""
Verification script for 8051 Microcontroller PCB Design Report PDF.
"""

from pypdf import PdfReader
import re

pdf_path = r"C:\8051_micro\Final_Report\8051_Microcontroller_PCB_Design_Report.pdf"
reader = PdfReader(pdf_path)

num_pages = len(reader.pages)
print(f"Total PDF Pages: {num_pages}")

# Verify all required chapters
required_chapters = [
    "Chapter 1: Project Overview",
    "Chapter 2: Circuit Description",
    "Chapter 3: Schematic Design",
    "Chapter 4: Footprint Assignment Details",
    "Chapter 5: PCB Layout Design",
    "Chapter 6: Routing Methodology",
    "Chapter 7: Design Rule Check (DRC) Results",
    "Chapter 8: 3D PCB Visualization",
    "Chapter 9: Design Considerations",
    "Chapter 10: Conclusion and Future Scope"
]

full_text = ""
for idx, page in enumerate(reader.pages):
    txt = page.extract_text() or ""
    full_text += f"\n--- PAGE {idx+1} ---\n" + txt

print("\n--- CHAPTER DETECTION AUDIT ---")
for ch in required_chapters:
    if ch in full_text:
        print(f"[PASSED] Found: {ch}")
    else:
        print(f"[FAILED] Missing: {ch}")

# Check figures
figures = [
    "Figure 2.1",
    "Figure 3.1",
    "Figure 5.1",
    "Figure 6.1",
    "Figure 8.1",
    "Figure 8.2"
]
print("\n--- FIGURE DETECTION AUDIT ---")
for fig in figures:
    if fig in full_text:
        print(f"[PASSED] Found: {fig}")
    else:
        print(f"[FAILED] Missing: {fig}")

# Check tables
tables = [
    "Table 2.1",
    "Table 4.1",
    "Table 6.1",
    "Table 7.1"
]
print("\n--- TABLE DETECTION AUDIT ---")
for tbl in tables:
    if tbl in full_text:
        print(f"[PASSED] Found: {tbl}")
    else:
        print(f"[FAILED] Missing: {tbl}")

# Check for forbidden placeholder patterns
forbidden = ["TODO", "FIXME", "XXX", "LOREM IPSUM", "PLACEHOLDER", "<<TOC_LOCATION_MARKER>>"]
print("\n--- PLACEHOLDER AUDIT ---")
found_forbidden = False
for fb in forbidden:
    matches = re.findall(rf"\b{fb}\b", full_text, re.IGNORECASE)
    if matches:
        print(f"[WARNING] Found placeholder token: {fb} ({len(matches)} occurrences)")
        found_forbidden = True
if not found_forbidden:
    print("[PASSED] Zero placeholder or dummy tokens found across all 22 pages.")

print("\nVerification script finished.")
