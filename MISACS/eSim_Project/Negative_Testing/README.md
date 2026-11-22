# MISACS Phase 3 — Controlled Negative Testing Suite (Final Review Candidate)

**Project:** Modular Industrial Sensor Acquisition and Control System (MISACS)  
**Program:** FOSSEE eSim Winter Internship 2026 — Task 7  
**Module:** `Negative_Testing/test_negative_cases.py`  
**Status:** Verification Artifact & Quality Assurance Tool  

---

## 1. Overview and Objective
This directory contains the automated, self-contained negative testing suite designed to prove that `run_simulations.py` actively validates simulation outputs, enforces physical safety boundaries, and cleanly traps faults without crashing or silently passing corrupted data.

The suite executes each negative test case inside an isolated temporary directory created on demand. All modifications are confined to that temporary directory and completely deleted upon case completion, leaving the source project directory 100% clean and pristine.

---

## 2. Test Case Catalog

| Case # | Test Case Description | Injected Fault Condition | Expected Failure Signature | Expected Exit Code |
|:---:|---|---|---|:---:|
| **Case 1** | Insufficient TB4 Regression Samples | Sweep modified from `.dc Iloop 0m 25m 1m` to `.dc Iloop 0m 25m 2m`, generating 13 total rows with exactly 9 samples across the 4–20 mA operating interval (4, 6, 8, 10, 12, 14, 16, 18, 20 mA), tripping the minimum $\ge 10$ operating sample threshold | `Insufficient operating interval regression samples (got 9, minimum required >= 10)` | `1` |
| **Case 2** | Missing TB5 Mandatory 12V Point | Sweep truncated at 10.0V, omitting mandatory 12.0V over-range check | `Mandatory 12.0V over-range input fault point missing` | `1` |
| **Case 3** | Malformed Numerical Token | Injected corrupt non-numeric string token `MALFORMED_NON_NUMERIC_TOKEN` | `Non-numeric token in row` | `1` |
| **Case 4** | Non-Finite Token (NaN / Inf) | Injected IEEE non-finite token `NaN` into tabular simulator output | `Non-finite value (NaN/Inf) detected` | `1` |
| **Case 5** | Missing Simulator Output File | Deleted target raw data file immediately after simulation execution | `Missing raw output file` | `1` |
| **Case 6** | Missing Circuit SPICE Netlist | Deleted source circuit netlist `tb3_ams1117.cir` prior to execution | `Missing input netlist: tb3_ams1117.cir` | `1` |
| **Case 7** | Failed Simulator Executable Invocation | Configured non-existent executable path `C:\NonExistentPath\ngspice_invalid.exe` | `No functional Ngspice simulator found` / `Simulator launch failed` | `1` |
| **Case 8** | Crash-Proof Universal Report Generation | Deleted all 10 netlists to trigger total failure across all testbenches | Clean report generation with `0/10 PASSING` without `KeyError` or secondary crash | `1` |
| **Case 9** | Perturbed TB4 Ideal Agreement Dataset | Injected +0.015V (+15mV) offset into TB4 buffer stage, producing $SS_{ideal\_res} = 0.003825\,\text{V}^2$ and calculated $R^2_{ideal} = 0.999063 < 0.9999$ | `FAIL: Ideal agreement metric R^2(ideal)=0.999063 below specification (target >= 0.9999)` | `1` |

---

## 3. How to Execute
To run the automated negative testing suite from the project root:
```bash
python Negative_Testing/test_negative_cases.py
```
Or from within the `Negative_Testing/` directory:
```bash
python test_negative_cases.py
```

### Expected Execution Behavior:
- The script iterates through Cases 1 through 9.
- Each case reports `Result: [PASS]` when the runner successfully detects the error condition, records the failure, and returns exit code 1.
- Upon completion of all 9 cases, the master script generates `NEGATIVE_TEST_REPORT.json` and exits with code 0 (confirming that all 9 validation checks functioned as intended).
