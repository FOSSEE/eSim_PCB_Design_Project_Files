#!/usr/bin/env python3
"""
MISACS Phase 3 — Controlled Negative Testing Suite (Final Review Candidate)
Program: FOSSEE eSim Winter Internship 2026 — Task 7

Automated verification of the simulation runner error-trapping and boundary enforcement logic.
Tests 9 controlled failure and edge-case conditions in an isolated temporary workspace.
Restores all files cleanly upon completion.
"""

import os
import sys
import shutil
import subprocess
import json
import tempfile

def run_test_case(case_num, case_name, setup_fn, verify_fn, extra_env=None):
    print(f"\n[Case {case_num}] {case_name}...")
    temp_dir = tempfile.mkdtemp(prefix=f"misacs_neg_test_{case_num}_")
    try:
        rc_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        for item in os.listdir(rc_dir):
            if item in [".git", "_temp_run_output", "Negative_Testing"]:
                continue
            s = os.path.join(rc_dir, item)
            d = os.path.join(temp_dir, item)
            if os.path.isdir(s):
                shutil.copytree(s, d)
            else:
                shutil.copy2(s, d)
                
        # Run case-specific setup
        setup_fn(temp_dir)
        
        # Configure environment
        env = os.environ.copy()
        if extra_env:
            env.update(extra_env)
            
        cmd = [sys.executable, "run_simulations.py"]
        res = subprocess.run(cmd, cwd=temp_dir, capture_output=True, text=True, env=env)
        
        passed, details = verify_fn(res, temp_dir)
        if passed:
            print(f"  Result: [PASS] {details}")
            return {"case": case_num, "name": case_name, "status": "PASS", "details": details, "returncode": res.returncode}
        else:
            print(f"  Result: [FAIL] {details}")
            return {"case": case_num, "name": case_name, "status": "FAIL", "details": details, "returncode": res.returncode}
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)

# Case 1: Insufficient TB4 regression samples (< 10 points)
def setup_case_1(td):
    cir_path = os.path.join(td, "Simulation", "tb4_current_loop.cir")
    with open(cir_path, "r", encoding="utf-8") as f:
        content = f.read()
    # Sweep from 0mA to 25mA with 2mA step: 13 total rows, but exactly 9 samples in 4-20mA interval (4, 6, 8, 10, 12, 14, 16, 18, 20 mA), < 10 threshold
    content = content.replace(".dc Iloop 0m 25m 1m", ".dc Iloop 0m 25m 2m")
    with open(cir_path, "w", encoding="utf-8") as f:
        f.write(content)

def verify_case_1(res, td):
    if res.returncode != 0 and ("Insufficient operating interval regression samples" in res.stdout or "Insufficient regression samples" in res.stdout):
        return True, "Runner caught sample count (< 10; exactly 9 samples generated at 2mA step in 4-20mA interval) and failed with exit code 1"
    return False, f"Expected returncode != 0 and sample count error, got code {res.returncode}"

# Case 2: Missing TB5 mandatory 12V point
def setup_case_2(td):
    cir_path = os.path.join(td, "Simulation", "tb5_voltage_input.cir")
    with open(cir_path, "r", encoding="utf-8") as f:
        content = f.read()
    content = content.replace(".dc Vin 0 12 0.5", ".dc Vin 0 10 0.5")
    with open(cir_path, "w", encoding="utf-8") as f:
        f.write(content)

def verify_case_2(res, td):
    if res.returncode != 0 and "Mandatory 12.0V over-range input fault point missing" in res.stdout:
        return True, "Runner caught missing 12V over-range check and exited with code 1"
    return False, f"Expected missing 12V point error, got code {res.returncode}"

# Case 3: Malformed numerical output (non-numeric token)
def setup_case_3(td): pass
def verify_case_3(res, td):
    if res.returncode != 0 and "has non-numeric token: 'MALFORMED_TOKEN'" in res.stdout:
        return True, "Runner caught non-numeric token and rejected row cleanly"
    return False, f"Expected non-numeric token rejection, got code {res.returncode}"

# Case 4: Non-Finite Token Injection (NaN / Inf)
def setup_case_4(td): pass
def verify_case_4(res, td):
    if res.returncode != 0 and "contains non-finite value: nan" in res.stdout:
        return True, "Runner caught NaN token and rejected non-finite value cleanly"
    return False, f"Expected NaN rejection, got code {res.returncode}"

# Case 5: Missing Simulator Output Data File
def setup_case_5(td): pass
def verify_case_5(res, td):
    if res.returncode != 0 and "Expected output file not created or empty:" in res.stdout:
        return True, "Runner detected missing output file and recorded test failure"
    return False, f"Expected missing output file detection, got code {res.returncode}"

# Case 6: Missing Circuit SPICE Netlist File
def setup_case_6(td):
    cir_path = os.path.join(td, "Simulation", "tb3_ams1117.cir")
    if os.path.exists(cir_path):
        os.remove(cir_path)

def verify_case_6(res, td):
    if res.returncode != 0 and "Missing input netlist:" in res.stdout:
        return True, "Runner trapped missing input netlist before execution"
    return False, f"Expected missing netlist trap, got code {res.returncode}"

# Case 7: Failed Simulator Executable Invocation
def setup_case_7(td): pass
def verify_case_7(res, td):
    if res.returncode != 0 and ("No functional Ngspice simulator found" in res.stdout or "The system cannot find the file specified" in res.stderr or "FileNotFoundError" in res.stdout):
        return True, "Runner cleanly aborted on invalid simulator executable path"
    return False, f"Expected simulator invocation failure, got code {res.returncode}"

# Case 8: Failure-Report Generation Without Secondary KeyError
def setup_case_8(td):
    sim_dir = os.path.join(td, "Simulation")
    for f in os.listdir(sim_dir):
        if f.endswith(".cir"):
            os.remove(os.path.join(sim_dir, f))

def verify_case_8(res, td):
    report_path = os.path.join(td, "Simulation", "SIMULATION_REPORT.md")
    manifest_path = os.path.join(td, "Simulation", "SIMULATION_RUN_MANIFEST.json")
    if res.returncode != 0 and os.path.exists(report_path) and os.path.exists(manifest_path):
        with open(report_path, "r", encoding="utf-8") as f:
            rep_text = f.read()
        if "0/10 PASSING" in rep_text:
            return True, "Report and manifest generated cleanly without KeyError or secondary crash during universal failure"
    return False, f"Expected crash-proof report generation under total failure, got code {res.returncode}"

# Case 9: Deliberately Perturbed TB4 Ideal Agreement Dataset
def setup_case_9(td):
    cir_path = os.path.join(td, "Simulation", "tb4_current_loop.cir")
    with open(cir_path, "r", encoding="utf-8") as f:
        content = f.read()
    # Injects +0.015V (+15mV) offset into TB4 buffer stage:
    # Operating points across 4mA-20mA span (17 points) will measure V = 100*I + 0.015V.
    # Residual SS_ideal_res = 17 * (0.015)^2 = 0.003825 V^2.
    # Total SS_ideal_tot = 4.08 V^2.
    # Expected R^2(ideal) = 1.0 - (0.003825 / 4.08) = 0.9990625 (~0.999063), strictly below 0.9999 threshold.
    content = content.replace(
        "Ebuf buf_out 0 VALUE = { min(5.0, max(0.0, v(filt_node))) }",
        "Ebuf buf_out 0 VALUE = { min(5.0, max(0.0, v(filt_node) + 0.015)) }"
    )
    with open(cir_path, "w", encoding="utf-8") as f:
        f.write(content)

def verify_case_9(res, td):
    # Requirement:
    # 1. Verify returncode != 0
    # 2. Verify that calculated R^2(ideal) is below 0.9999 (~0.999063)
    # 3. Specifically verify that the ideal-agreement acceptance check itself failed
    # 4. Reject if ONLY generic calibration-point deviation is present without R^2(ideal) check failure
    if res.returncode == 0:
        return False, f"Expected non-zero returncode on perturbed dataset, got {res.returncode}"
        
    has_r2_val = ("R^2(ideal)=0.99906" in res.stdout or "0.999063" in res.stdout or "0.999062" in res.stdout)
    has_ideal_fail_msg = ("FAIL: Ideal agreement metric R^2(ideal)=" in res.stdout and "below specification (target >= 0.9999)" in res.stdout)
    
    if not has_r2_val:
        return False, f"Runner did not calculate expected R^2(ideal) (~0.999063). Output:\n{res.stdout}"
    if not has_ideal_fail_msg:
        return False, f"Runner did not trigger specific ideal agreement acceptance check failure. Output:\n{res.stdout}"
        
    # Also verify synthetic calculation helper directly
    sys.path.insert(0, td)
    try:
        from run_simulations import compute_ideal_agreement
        xs = [i * 1e-3 for i in range(4, 21)]
        # Synthetic pure ideal
        ys_ideal = [100.0 * x for x in xs]
        r_ideal = compute_ideal_agreement(xs, ys_ideal, 100.0, 0.9999)
        assert r_ideal["passes"] is True, "Helper failed on pure ideal data"
        assert abs(r_ideal["r2_ideal"] - 1.000000) < 1e-6, "Helper R^2 != 1.0"
        
        # Synthetic +15mV perturbation
        ys_pert = [100.0 * x + 0.015 for x in xs]
        r_pert = compute_ideal_agreement(xs, ys_pert, 100.0, 0.9999)
        assert r_pert["passes"] is False, "Helper passed on perturbed data"
        assert abs(r_pert["r2_ideal"] - 0.9990625) < 1e-6, "Helper R^2 calculation mismatch"
        
        # Synthetic sub-5mV perturbation (+4.95mV, pointwise tests pass <= 5mV, but R^2 fails)
        ys_sub5 = [100.0 * x + 0.00495 for x in xs]
        r_sub5 = compute_ideal_agreement(xs, ys_sub5, 100.0, 0.9999)
        assert r_sub5["passes"] is False, "Helper passed on sub-5mV cumulative perturbation"
        assert r_sub5["r2_ideal"] < 0.9999, "Helper R^2 unexpectedly >= 0.9999"
    except Exception as e:
        return False, f"Synthetic ideal agreement helper verification failed: {e}"
        
    return True, "Runner computed R^2(ideal)=0.999063 (< 0.9999) and specifically trapped ideal agreement failure; verified compute_ideal_agreement helper across 3 synthetic datasets"

def main():
    print("================================================================================")
    print("  MISACS PHASE 3 — CONTROLLED NEGATIVE TESTING SUITE")
    print("================================================================================")
    
    cases = [
        (1, "Insufficient TB4 Regression Samples (< 10 samples)", setup_case_1, verify_case_1, None),
        (2, "Missing TB5 Mandatory 12V Over-Range Point", setup_case_2, verify_case_2, None),
        (3, "Malformed Non-Numeric Token Injection", setup_case_3, verify_case_3, {"MISACS_TEST_INJECT_MALFORMED": "1"}),
        (4, "Non-Finite Token Injection (NaN / Inf)", setup_case_4, verify_case_4, {"MISACS_TEST_INJECT_NAN": "1"}),
        (5, "Missing Simulator Output Data File", setup_case_5, verify_case_5, {"MISACS_TEST_DELETE_OUTPUT": "1"}),
        (6, "Missing Circuit SPICE Netlist File", setup_case_6, verify_case_6, None),
        (7, "Failed Simulator Executable Invocation", setup_case_7, verify_case_7, {"MISACS_TEST_BAD_SIMULATOR": "1"}),
        (8, "Universal Report Generation Without Secondary KeyError", setup_case_8, verify_case_8, None),
        (9, "Deliberately Perturbed TB4 Ideal Agreement Dataset", setup_case_9, verify_case_9, None),
    ]
    
    results = []
    all_passed = True
    for c_num, c_name, setup_f, verify_f, env_extra in cases:
        r = run_test_case(c_num, c_name, setup_f, verify_f, env_extra)
        results.append(r)
        if r["status"] != "PASS":
            all_passed = False
            
    # Save test report
    report_file = os.path.join(os.path.dirname(__file__), "NEGATIVE_TEST_REPORT.json")
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump({
            "suite": "MISACS Phase 3 Controlled Negative Testing Suite (Final Review Candidate)",
            "total_cases": len(cases),
            "passed_cases": sum(1 for r in results if r["status"] == "PASS"),
            "all_passed": all_passed,
            "results": results
        }, f, indent=2)
        
    print("\n================================================================================")
    print(f"  NEGATIVE TESTING SUMMARY: {sum(1 for r in results if r['status'] == 'PASS')}/{len(cases)} TEST CASES PASSED")
    print(f"  Report written to: {report_file}")
    print("================================================================================\n")
    
    if not all_passed:
        sys.exit(1)
    sys.exit(0)

if __name__ == "__main__":
    main()
