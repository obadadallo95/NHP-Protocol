"""
NHP Mega Simulation — Bilingual Report Generator
Produces a comprehensive Arabic/English report from all scenario results.
"""
from typing import Dict, Any, List
import os
from datetime import datetime

from mega_simulation.data import VARIANT_NAMES, VARIANT_NAMES_AR, VARIANT_EMOJIS


def _fmt(val: float) -> str:
    """Format large numbers."""
    if val >= 1e9: return f"${val/1e9:.1f}B"
    if val >= 1e6: return f"${val/1e6:.1f}M"
    if val >= 1e3: return f"${val/1e3:.0f}K"
    return f"${val:.2f}"


def _num(val: float) -> str:
    """Format number with commas."""
    return f"{val:,.0f}"


def generate_mega_report(
    all_results: Dict[str, List[Dict[str, Any]]],
    total_scenarios: int,
    chart_paths: List[str],
) -> str:
    """Build the full bilingual mega report.

    Args:
        all_results: Dict of category letter -> results list.
        total_scenarios: Total number of scenarios computed.
        chart_paths: Paths to generated charts.

    Returns:
        Complete report as markdown string.
    """
    now = datetime.now().strftime("%d.%m.%Y — %H:%M")
    lines: List[str] = []

    # ── Header ───────────────────────────────────────────────
    lines.append("# NHP Mega Simulation Report — تقرير المحاكاة الشاملة")
    lines.append("### Neural Handset Protocol — بروتوكول الشبكة العصبية المحمولة")
    lines.append("")
    lines.append(f"**📅 Date / التاريخ: {now}**")
    lines.append(f"**📊 Total Scenarios / عدد السيناريوهات: {total_scenarios}**")
    lines.append(f"**📌 Version / الإصدار: 2.0 (Mega)**")
    lines.append("")
    lines.append("---")
    lines.append("")

    # ── Category A ───────────────────────────────────────────
    lines.append("## A — Computing Power per Manufacturer / القوة الحسابية لكل مصنّع")
    lines.append("")
    lines.append("| Manufacturer / المصنّع | Variant | Active Devices | H100 Equiv | Total TOPS |")
    lines.append("|---|---|---|---|---|")
    for r in all_results["A"]:
        vi = VARIANT_NAMES.index(r["variant"])
        lines.append(f"| {r['manufacturer']} | {VARIANT_EMOJIS[vi]} {r['variant']} | "
                     f"{_num(r['active_devices'])} | **{_num(r['h100_equivalent'])}** | {_num(r['total_tops'])} |")
    lines.append("")

    # ── Category B — Summary (moderate only) ─────────────────
    lines.append("## B — NHP vs Cloud Providers / مقارنة مع مزودي السحابة")
    lines.append("*(Moderate variant — 40% coverage)*")
    lines.append("")
    lines.append("| Manufacturer | Cloud Provider | Annual Savings | Savings % |")
    lines.append("|---|---|---|---|")
    for r in all_results["B"]:
        if r["variant"] == "Moderate":
            lines.append(f"| {r['manufacturer']} | {r['cloud_short']} | "
                         f"**{_fmt(r['annual_savings'])}** | {r['savings_pct']:.0f}% |")
    lines.append("")

    # ── Category C ───────────────────────────────────────────
    lines.append("## C — User Income by Region / دخل المستخدم حسب المنطقة")
    lines.append("")
    lines.append("| Region / المنطقة | Variant | Monthly Net | Annual Net | % of Avg Income |")
    lines.append("|---|---|---|---|---|")
    for r in all_results["C"]:
        vi = VARIANT_NAMES.index(r["variant"])
        lines.append(f"| {r['region']} ({r['region_ar']}) | {VARIANT_EMOJIS[vi]} {r['variant']} | "
                     f"${r['monthly_net']:.2f} | ${r['annual_net']:.2f} | {r['income_pct_of_avg']:.2f}% |")
    lines.append("")

    # ── Category D ───────────────────────────────────────────
    lines.append("## D — Manufacturer AI Savings vs AWS / توفير المصنّع مقارنة بـ AWS")
    lines.append("")
    lines.append("| Manufacturer / المصنّع | Variant | Annual Savings | Coverage |")
    lines.append("|---|---|---|---|")
    for r in all_results["D"]:
        vi = VARIANT_NAMES.index(r["variant"])
        lines.append(f"| {r['manufacturer']} | {VARIANT_EMOJIS[vi]} {r['variant']} | "
                     f"**{_fmt(r['annual_savings'])}** | {r['coverage_pct']:.0f}% |")
    lines.append("")

    # ── Category E ───────────────────────────────────────────
    lines.append("## E — Environmental Impact / الأثر البيئي")
    lines.append("")
    lines.append("| Manufacturer | Variant | CO₂ Saved (net) | Cars Removed | Phone CO₂ Added |")
    lines.append("|---|---|---|---|---|")
    for r in all_results["E"]:
        vi = VARIANT_NAMES.index(r["variant"])
        lines.append(f"| {r['manufacturer']} | {VARIANT_EMOJIS[vi]} {r['variant']} | "
                     f"**{_num(r['co2_saved_net'])} tons** | {_num(r['cars_equivalent'])} | {_num(r['co2_added_phones'])} tons |")
    lines.append("")

    # ── Category F ───────────────────────────────────────────
    lines.append("## F — Network Alliance Power / قوة التحالفات")
    lines.append("")
    lines.append("| Alliance / التحالف | Variant | Active Devices | H100 Equiv |")
    lines.append("|---|---|---|---|")
    for r in all_results["F"]:
        vi = VARIANT_NAMES.index(r["variant"])
        lines.append(f"| {r['alliance']} | {VARIANT_EMOJIS[vi]} {r['variant']} | "
                     f"{_num(r['total_active_devices'])} | **{_num(r['h100_equivalent'])}** |")
    lines.append("")

    # ── Category G ───────────────────────────────────────────
    lines.append("## G — AI Task Feasibility / جدوى المهام الحسابية")
    lines.append("")
    lines.append("| Task / المهمة | Variant | Score | Capable? | Latency-Sensitive? | Tasks/Day |")
    lines.append("|---|---|---|---|---|---|")
    for r in all_results["G"]:
        vi = VARIANT_NAMES.index(r["variant"])
        capable = "✅" if r["device_capable"] else "❌"
        latency = "⚡ Yes" if r["latency_sensitive"] else "No"
        lines.append(f"| {r['task_name']} ({r['task_name_ar']}) | {VARIANT_EMOJIS[vi]} {r['variant']} | "
                     f"**{r['feasibility_score']:.0f}/100** | {capable} | {latency} | {_num(r['tasks_per_day'])} |")
    lines.append("")

    # ── Category H ───────────────────────────────────────────
    lines.append("## H — Battery Impact / تأثير البطارية")
    lines.append("")
    lines.append("| Device Tier | Variant | Life w/ NHP (yrs) | Life w/o NHP (yrs) | Reduction (months) |")
    lines.append("|---|---|---|---|---|")
    for r in all_results["H"]:
        vi = VARIANT_NAMES.index(r["variant"])
        lines.append(f"| {r['tier']} | {VARIANT_EMOJIS[vi]} {r['variant']} | "
                     f"{r['battery_life_with_nhp_years']:.1f} | {r['battery_life_without_nhp_years']:.1f} | "
                     f"{r['life_reduction_months']:.1f} |")
    lines.append("")

    # ── Category I ───────────────────────────────────────────
    lines.append("## I — Market Size / حجم السوق")
    lines.append("")
    lines.append("| Region / المنطقة | Variant | Total Smartphones | NHP Devices | Annual Revenue |")
    lines.append("|---|---|---|---|---|")
    for r in all_results["I"]:
        vi = VARIANT_NAMES.index(r["variant"])
        lines.append(f"| {r['region']} ({r['region_ar']}) | {VARIANT_EMOJIS[vi]} {r['variant']} | "
                     f"{_num(r['total_smartphones'])} | {_num(r['nhp_devices'])} | {_fmt(r['annual_platform_revenue'])} |")
    lines.append("")

    # ── Category J ───────────────────────────────────────────
    lines.append("## J — Token Economics / اقتصاد التوكن")
    lines.append("")
    lines.append("| Scale | Variant | Monthly GPU Hours | Monthly Flow | Platform Rev/mo | Market Cap (est) |")
    lines.append("|---|---|---|---|---|---|")
    for r in all_results["J"]:
        vi = VARIANT_NAMES.index(r["variant"])
        lines.append(f"| {r['scale_label']} | {VARIANT_EMOJIS[vi]} {r['variant']} | "
                     f"{_num(r['monthly_gpu_hours'])} | {_fmt(r['total_monthly_flow'])} | "
                     f"{_fmt(r['platform_revenue_monthly'])} | {_fmt(r['market_cap_conservative'])}–{_fmt(r['market_cap_aggressive'])} |")
    lines.append("")

    # ── Category K ───────────────────────────────────────────
    lines.append("## K — Competitive Positioning / الموقع التنافسي")
    lines.append("")
    lines.append("| Competitor | Variant | NHP TOPS | Comp TOPS | Power Ratio | NHP Advantages |")
    lines.append("|---|---|---|---|---|---|")
    for r in all_results["K"]:
        vi = VARIANT_NAMES.index(r["variant"])
        ratio_str = f"{r['power_ratio']:.1f}×" if r['power_ratio'] < 1000 else "1000×+"
        advs = ", ".join(r["nhp_advantages"]) if r["nhp_advantages"] else "—"
        lines.append(f"| {r['competitor']} | {VARIANT_EMOJIS[vi]} {r['variant']} | "
                     f"{_num(r['nhp_total_tops'])} | {_num(r['comp_total_tops'])} | **{ratio_str}** | {advs} |")
    lines.append("")

    # ── Category L ───────────────────────────────────────────
    lines.append("## L — Breakeven Analysis / تحليل نقطة التعادل")
    lines.append("")
    lines.append("| Manufacturer | Variant | Dev Cost | Monthly Savings | Breakeven (mo) | 5yr ROI |")
    lines.append("|---|---|---|---|---|---|")
    for r in all_results["L"]:
        vi = VARIANT_NAMES.index(r["variant"])
        be = f"{r['breakeven_months']:.0f}" if r['breakeven_months'] < 999 else "∞"
        lines.append(f"| {r['manufacturer']} | {VARIANT_EMOJIS[vi]} {r['variant']} | "
                     f"{_fmt(r['development_cost'])} | {_fmt(r['monthly_savings'])} | "
                     f"**{be}** | {r['roi_5yr_pct']:.0f}% |")
    lines.append("")

    # ── Category M ───────────────────────────────────────────
    lines.append("## M — Risk Analysis / تحليل المخاطر")
    lines.append("")
    lines.append("| Risk / المخاطرة | Variant | Impact | Probability | Expected Loss | Severity |")
    lines.append("|---|---|---|---|---|---|")
    for r in all_results["M"]:
        vi = VARIANT_NAMES.index(r["variant"])
        lines.append(f"| {r['risk_name']} ({r['risk_name_ar']}) | {VARIANT_EMOJIS[vi]} {r['variant']} | "
                     f"{r['impact_pct']:.0f}% | {r['probability_pct']:.0f}% | "
                     f"{_fmt(r['expected_loss'])} | {r['severity']} |")
    lines.append("")

    # ── Charts ───────────────────────────────────────────────
    lines.append("---")
    lines.append("")
    lines.append("## 📊 Generated Charts / الرسوم البيانية")
    lines.append("")
    for p in chart_paths:
        lines.append(f"- ✅ `{p}`")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(f"*NHP Mega Simulation v2.0 — {now}*")
    lines.append("*الحوسبة في يد الجميع — Computing in Everyone's Hands*")

    return "\n".join(lines)


def save_mega_report(report_text: str, output_dir: str = "output") -> str:
    """Save the mega report.

    Args:
        report_text: The complete report string.
        output_dir: Output directory.

    Returns:
        Path to saved report.
    """
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "mega_report.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write(report_text)
    return path


def save_csv_export(
    all_results: Dict[str, List[Dict[str, Any]]],
    output_dir: str = "output",
) -> str:
    """Export all results as CSV for further analysis.

    Args:
        all_results: Dict of category -> results.
        output_dir: Output directory.

    Returns:
        Path to saved CSV.
    """
    import csv

    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "mega_scenarios_all.csv")

    # Collect all unique keys
    all_keys: set = set()
    for cat_results in all_results.values():
        for r in cat_results:
            all_keys.update(r.keys())

    all_keys_sorted = sorted(all_keys)

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=all_keys_sorted, extrasaction="ignore")
        writer.writeheader()
        for cat_results in all_results.values():
            for r in cat_results:
                # Convert lists to strings for CSV
                row = {}
                for k, v in r.items():
                    row[k] = str(v) if isinstance(v, list) else v
                writer.writerow(row)

    return path
