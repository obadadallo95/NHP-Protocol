#!/usr/bin/env python3
"""
NHP Mega Simulation — Entry Point
Run with: python mega_simulation/run.py

Generates 580+ scenarios across 13 categories, produces charts,
and saves a comprehensive bilingual report + CSV data export.
"""
import sys
import os
import time

# Ensure project root is in path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mega_simulation.scenarios import run_all_categories
from mega_simulation.charts import generate_all_charts
from mega_simulation.report import generate_mega_report, save_mega_report, save_csv_export


def main() -> None:
    """Run the complete mega simulation pipeline."""
    print("=" * 60)
    print("  NHP MEGA SIMULATION — v2.0")
    print("  Neural Handset Protocol — محاكاة شاملة")
    print("=" * 60)
    print()

    start_time = time.time()

    # ── Step 1: Run all scenario categories ──────────────────
    print("▶ Running all 13 scenario categories...")
    all_results = run_all_categories()

    total_scenarios = sum(len(v) for v in all_results.values())
    print(f"  ✅ Total scenarios computed: {total_scenarios}")
    print()

    for cat, results in sorted(all_results.items()):
        print(f"  Category {cat}: {len(results):>4} scenarios")

    print()

    # ── Step 2: Generate charts ──────────────────────────────
    print("▶ Generating charts...")
    chart_paths = generate_all_charts(all_results)
    for p in chart_paths:
        print(f"  ✅ {p}")
    print()

    # ── Step 3: Generate and save report ─────────────────────
    print("▶ Generating bilingual report...")
    report_text = generate_mega_report(all_results, total_scenarios, chart_paths)
    report_path = save_mega_report(report_text)
    print(f"  ✅ Report saved: {report_path}")

    # ── Step 4: CSV export ───────────────────────────────────
    print("▶ Exporting CSV data...")
    csv_path = save_csv_export(all_results)
    print(f"  ✅ CSV saved: {csv_path}")

    elapsed = time.time() - start_time
    print()
    print("=" * 60)
    print(f"  MEGA SIMULATION COMPLETE")
    print(f"  {total_scenarios} scenarios | {len(chart_paths)} charts | {elapsed:.1f}s")
    print("=" * 60)

    # ── Print summary stats ──────────────────────────────────
    print()
    print("📊 QUICK SUMMARY / ملخص سريع:")
    print()

    # Best moderate results
    a_mod = [r for r in all_results["A"] if r["variant"] == "Moderate"]
    top_mfg = max(a_mod, key=lambda r: r["h100_equivalent"])
    print(f"  💪 Top fleet (moderate): {top_mfg['manufacturer']} = "
          f"{top_mfg['h100_equivalent']:,.0f} H100 equiv")

    f_mod = [r for r in all_results["F"] if r["variant"] == "Moderate"]
    top_alliance = max(f_mod, key=lambda r: r["h100_equivalent"])
    print(f"  🤝 Top alliance (moderate): {top_alliance['alliance']} = "
          f"{top_alliance['h100_equivalent']:,.0f} H100 equiv")

    d_mod = [r for r in all_results["D"] if r["variant"] == "Moderate"]
    top_saver = max(d_mod, key=lambda r: r["annual_savings"])
    print(f"  💰 Top savings (moderate): {top_saver['manufacturer']} = "
          f"${top_saver['annual_savings']/1e6:.1f}M/year")

    j_mod = [r for r in all_results["J"] if r["variant"] == "Moderate"]
    top_token = max(j_mod, key=lambda r: r["platform_revenue_monthly"])
    print(f"  🪙 Max platform revenue (moderate): "
          f"${top_token['platform_revenue_monthly']/1e6:.1f}M/month @ {top_token['scale_label']}")

    print()


if __name__ == "__main__":
    main()
