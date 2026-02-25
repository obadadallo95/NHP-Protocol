#!/usr/bin/env python3
"""
NHP Simulation — Main Entry Point
Neural Handset Protocol: Distributed GPU Computing Feasibility Study

Run with: python main.py

This script:
  1. Runs all 5 scenarios (20 variant simulations)
  2. Generates charts and saves them to assets/
  3. Prints a summary to the terminal
  4. Saves a full report to output/full_report.txt
"""
import sys
import os

# Ensure project root is in path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from typing import Dict, Any, List

from scenarios.scenario_01_computing_power.simulation import run_all as run_s1
from scenarios.scenario_02_user_income.simulation import run_all as run_s2
from scenarios.scenario_03_manufacturer_savings.simulation import run_all as run_s3
from scenarios.scenario_04_network_growth.simulation import run_all as run_s4
from scenarios.scenario_05_environmental_impact.simulation import run_all as run_s5

from visualizations.chart_generator import (
    generate_scenario_01,
    generate_scenario_02,
    generate_scenario_03,
    generate_scenario_04,
    generate_scenario_05,
)
from visualizations.report_generator import generate_report, save_report


def main() -> None:
    """Run the complete NHP simulation pipeline."""
    print("=" * 56)
    print("  NHP SIMULATION — Neural Handset Protocol v1.0")
    print("=" * 56)
    print()

    # ── Step 1: Run all scenarios ────────────────────────────
    print("▶ Running Scenario 1: Computing Power...")
    s1_results: List[Dict[str, Any]] = run_s1()
    print(f"  ✓ {len(s1_results)} variants completed")

    print("▶ Running Scenario 2: User Income...")
    s2_results: List[Dict[str, Any]] = run_s2()
    print(f"  ✓ {len(s2_results)} variants completed")

    print("▶ Running Scenario 3: Manufacturer Savings...")
    s3_results: List[Dict[str, Any]] = run_s3()
    print(f"  ✓ {len(s3_results)} variants completed")

    print("▶ Running Scenario 4: Network Growth...")
    s4_results: List[Dict[str, Any]] = run_s4()
    print(f"  ✓ {len(s4_results)} variants completed")

    print("▶ Running Scenario 5: Environmental Impact...")
    s5_results: List[Dict[str, Any]] = run_s5()
    print(f"  ✓ {len(s5_results)} variants completed")

    print()

    # ── Step 2: Generate charts ──────────────────────────────
    print("▶ Generating charts...")
    chart1: str = generate_scenario_01(s1_results)
    print(f"  ✓ {chart1}")
    chart2: str = generate_scenario_02(s2_results)
    print(f"  ✓ {chart2}")
    chart3: str = generate_scenario_03(s3_results)
    print(f"  ✓ {chart3}")
    chart4: str = generate_scenario_04(s4_results)
    print(f"  ✓ {chart4}")
    chart5: str = generate_scenario_05(s5_results)
    print(f"  ✓ {chart5}")

    print()

    # ── Step 3: Generate and save report ─────────────────────
    print("▶ Generating report...")
    report_text: str = generate_report(
        s1_results, s2_results, s3_results, s4_results, s5_results,
    )
    report_path: str = save_report(report_text)
    print(f"  ✓ Full report saved to: {report_path}")

    print()

    # ── Step 4: Print summary to terminal ────────────────────
    print(report_text)

    print()
    print("=" * 56)
    print("  SIMULATION COMPLETE — All assets generated")
    print("=" * 56)


if __name__ == "__main__":
    main()
