"""
NHP Simulation — Report Generator
Formats all scenario results into a professional text report.
"""
from typing import Dict, Any, List
from datetime import datetime
import os

import config


def _format_money(amount: float) -> str:
    """Format a dollar amount with appropriate suffix (B/M/K).

    Args:
        amount: Dollar amount to format.

    Returns:
        Formatted string like '$1.2B' or '$350M'.
    """
    if amount >= 1_000_000_000:
        return f"${amount / 1_000_000_000:.1f}B"
    elif amount >= 1_000_000:
        return f"${amount / 1_000_000:.0f}M"
    elif amount >= 1_000:
        return f"${amount / 1_000:.0f}K"
    else:
        return f"${amount:.2f}"


def generate_report(
    s1_results: List[Dict[str, Any]],
    s2_results: List[Dict[str, Any]],
    s3_results: List[Dict[str, Any]],
    s4_results: List[Dict[str, Any]],
    s5_results: List[Dict[str, Any]],
) -> str:
    """Generate the full simulation report text.

    Args:
        s1_results: Scenario 1 (Computing Power) results.
        s2_results: Scenario 2 (User Income) results.
        s3_results: Scenario 3 (Manufacturer Savings) results.
        s4_results: Scenario 4 (Network Growth) results.
        s5_results: Scenario 5 (Environmental Impact) results.

    Returns:
        The complete report as a string.
    """
    date_str: str = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines: List[str] = []

    lines.append("=" * 56)
    lines.append(f"NHP SIMULATION REPORT — {date_str}")
    lines.append("Neural Handset Protocol v1.0")
    lines.append("=" * 56)
    lines.append("")

    # ── Scenario 1 ───────────────────────────────────────────
    lines.append("SCENARIO 1: COMPUTING POWER")
    lines.append(f"  Fleet Size: {config.TOTAL_DEVICES:,} Galaxy S24 devices")
    lines.append(f"  Device GPU: {config.DEVICE_GPU_TOPS} TOPS | Reference: Nvidia H100 ({config.REFERENCE_SERVER_TOPS:.0f} TOPS)")
    lines.append("")
    for r in s1_results:
        lines.append(f"  {r['variant']:14s} {r['h100_equivalent']:>8,.0f} H100 equivalent  "
                      f"({r['active_devices']:>9,} active devices, {r['uptime_pct']:.0f}% uptime)")
    lines.append("")

    # ── Scenario 2 ───────────────────────────────────────────
    lines.append("SCENARIO 2: USER MONTHLY INCOME")
    lines.append(f"  Nightly Operation: {config.NIGHTLY_HOURS:.0f} hours | "
                  f"Extra Power: {config.DEVICE_EXTRA_WATT}W | "
                  f"Electricity: ${config.ELECTRICITY_COST_KWH}/kWh")
    lines.append("")
    for r in s2_results:
        lines.append(f"  {r['variant']:14s} ${r['monthly_net']:>7.2f}/month | "
                      f"${r['annual_net']:>8.2f}/year  "
                      f"(token: ${r['token_price']:.2f}/GPU-hr, "
                      f"electricity: ${r['monthly_electricity']:.2f}/mo)")
    lines.append("")

    # ── Scenario 3 ───────────────────────────────────────────
    lines.append("SCENARIO 3: MANUFACTURER SAVINGS (Samsung Galaxy AI)")
    lines.append(f"  Daily Requests: {config.DAILY_AI_REQUESTS:,} | "
                  f"GPU/request: {config.REQUEST_GPU_TIME_SEC}s | "
                  f"AWS cost: ${config.AWS_GPU_HOURLY_COST}/hr")
    lines.append("")
    for r in s3_results:
        annual_str = _format_money(r["annual_savings"])
        lines.append(f"  {r['variant']:14s} {annual_str:>8}/year saved  "
                      f"({r['coverage_pct']:.0f}% coverage)")
    lines.append("")

    # ── Scenario 4 ───────────────────────────────────────────
    lines.append("SCENARIO 4: NETWORK GROWTH (5 Years)")
    lines.append(f"  Starting Point: {config.BASE_DEVICES:,} devices")
    lines.append("")

    # Header
    year_headers = "  " + f"{'Variant':14s}" + "".join(f"{'Year ' + str(y):>14s}" for y in range(1, config.SIMULATION_YEARS + 1))
    lines.append(year_headers)
    lines.append("  " + "-" * (14 + 14 * config.SIMULATION_YEARS))

    for r in s4_results:
        row = f"  {r['variant']:14s}"
        for d in r["yearly_devices"]:
            row += f"{d:>14,}"
        row += f"  ({r['growth_pct']:.0f}%/yr)"
        lines.append(row)
    lines.append("")

    # ── Scenario 5 ───────────────────────────────────────────
    lines.append("SCENARIO 5: ENVIRONMENTAL IMPACT (CO₂ SAVINGS)")
    lines.append(f"  Data Center Emissions: {config.DATA_CENTER_CO2_TONS_YEAR:,.0f} tons CO₂/year each")
    lines.append("")
    for r in s5_results:
        lines.append(f"  {r['variant']:14s} {r['co2_saved_tons']:>12,.0f} tons CO₂/year  "
                      f"(≈ {r['cars_equivalent']:>10,} cars removed, "
                      f"{r['data_centers_replaced']:.1f} DCs replaced)")
    lines.append("")

    # ── Asset Summary ────────────────────────────────────────
    lines.append("=" * 56)
    lines.append("ASSETS GENERATED:")
    for i in range(1, 6):
        dir_path = os.path.join(config.ASSETS_DIR, f"scenario_0{i}")
        exists = os.path.isdir(dir_path)
        symbol = "✓" if exists else "✗"
        lines.append(f"  {symbol} {dir_path}/")
    lines.append("=" * 56)
    lines.append("")

    return "\n".join(lines)


def save_report(report_text: str) -> str:
    """Save the report text to the output directory.

    Args:
        report_text: The full report string.

    Returns:
        Path to the saved report file.
    """
    os.makedirs(config.OUTPUT_DIR, exist_ok=True)
    path: str = os.path.join(config.OUTPUT_DIR, "full_report.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(report_text)
    return path
