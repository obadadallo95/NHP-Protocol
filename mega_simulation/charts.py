"""
NHP Mega Simulation — Chart Generator
Produces summary charts for key categories of the mega simulation.
"""
from typing import Dict, Any, List
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

from mega_simulation.data import VARIANT_COLORS, VARIANT_NAMES


CHART_DPI: int = 300
WATERMARK: str = "NHP Mega Simulation v2.0"


def _ensure_dir(path: str) -> None:
    """Create directory if needed."""
    os.makedirs(path, exist_ok=True)


def _watermark(ax: plt.Axes) -> None:
    """Add watermark."""
    ax.text(0.99, 0.01, WATERMARK, transform=ax.transAxes,
            fontsize=7, color="gray", alpha=0.4, ha="right", va="bottom")


def _fmt_money(val: float) -> str:
    """Format dollar amounts."""
    if val >= 1e9: return f"${val/1e9:.1f}B"
    if val >= 1e6: return f"${val/1e6:.0f}M"
    if val >= 1e3: return f"${val/1e3:.0f}K"
    return f"${val:.2f}"


def generate_all_charts(
    all_results: Dict[str, List[Dict[str, Any]]],
    output_dir: str = "assets/mega",
) -> List[str]:
    """Generate summary charts for all major categories.

    Args:
        all_results: Dict of category -> list of results.
        output_dir: Where to save charts.

    Returns:
        List of saved file paths.
    """
    _ensure_dir(output_dir)
    plt.style.use("seaborn-v0_8-darkgrid")
    plt.rcParams["font.family"] = "DejaVu Sans"
    plt.rcParams["font.size"] = 10

    saved: List[str] = []

    # ── Chart A: Computing Power per Manufacturer ────────────
    saved.append(_chart_a(all_results["A"], output_dir))
    # ── Chart B: Cloud Cost Comparison ───────────────────────
    saved.append(_chart_b_summary(all_results["B"], output_dir))
    # ── Chart C: User Income by Region ───────────────────────
    saved.append(_chart_c(all_results["C"], output_dir))
    # ── Chart D: Manufacturer Savings ────────────────────────
    saved.append(_chart_d(all_results["D"], output_dir))
    # ── Chart E: Environmental ───────────────────────────────
    saved.append(_chart_e(all_results["E"], output_dir))
    # ── Chart F: Network Alliances ───────────────────────────
    saved.append(_chart_f(all_results["F"], output_dir))
    # ── Chart G: Task Feasibility ────────────────────────────
    saved.append(_chart_g(all_results["G"], output_dir))
    # ── Chart I: Market Size ─────────────────────────────────
    saved.append(_chart_i(all_results["I"], output_dir))
    # ── Chart J: Token Economics ─────────────────────────────
    saved.append(_chart_j(all_results["J"], output_dir))
    # ── Chart K: Competitive ─────────────────────────────────
    saved.append(_chart_k(all_results["K"], output_dir))

    return saved


def _chart_a(results: List[Dict[str, Any]], out: str) -> str:
    """Computing power — grouped bars per manufacturer."""
    fig, ax = plt.subplots(figsize=(14, 7))
    mfgs = sorted(set(r["manufacturer"] for r in results),
                  key=lambda m: -max(r["h100_equivalent"] for r in results if r["manufacturer"] == m))
    x = np.arange(len(mfgs))
    width = 0.2

    for i, variant in enumerate(VARIANT_NAMES):
        vals = []
        for m in mfgs:
            v = next((r["h100_equivalent"] for r in results
                      if r["manufacturer"] == m and r["variant"] == variant), 0)
            vals.append(v)
        bars = ax.bar(x + i * width, vals, width, label=variant, color=VARIANT_COLORS[i], edgecolor="white")

    ax.set_xticks(x + width * 1.5)
    ax.set_xticklabels(mfgs, rotation=15, ha="right")
    ax.set_title("Computing Power: H100 Equivalents per Manufacturer", fontsize=14, fontweight="bold")
    ax.set_ylabel("H100 Equivalents")
    ax.legend()
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda v, _: f"{v:,.0f}"))
    _watermark(ax)
    plt.tight_layout()
    path = os.path.join(out, "A_computing_power.png")
    fig.savefig(path, dpi=CHART_DPI)
    plt.close(fig)
    return path


def _chart_b_summary(results: List[Dict[str, Any]], out: str) -> str:
    """Cloud cost comparison — moderate variant, all mfg × cloud."""
    mod = [r for r in results if r["variant"] == "Moderate"]
    fig, ax = plt.subplots(figsize=(14, 7))

    mfgs = sorted(set(r["manufacturer"] for r in mod))
    clouds = sorted(set(r["cloud_short"] for r in mod))
    x = np.arange(len(mfgs))
    width = 0.12

    for j, cloud in enumerate(clouds):
        vals = []
        for m in mfgs:
            v = next((r["annual_savings"] for r in mod
                      if r["manufacturer"] == m and r["cloud_short"] == cloud), 0)
            vals.append(v)
        ax.bar(x + j * width, vals, width, label=cloud, edgecolor="white")

    ax.set_xticks(x + width * len(clouds) / 2)
    ax.set_xticklabels(mfgs, rotation=15, ha="right")
    ax.set_title("Annual Savings: NHP vs Cloud (Moderate, 40% Coverage)", fontsize=14, fontweight="bold")
    ax.set_ylabel("Annual Savings (USD)")
    ax.legend(fontsize=8, ncol=2)
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda v, _: _fmt_money(v)))
    _watermark(ax)
    plt.tight_layout()
    path = os.path.join(out, "B_cloud_comparison.png")
    fig.savefig(path, dpi=CHART_DPI)
    plt.close(fig)
    return path


def _chart_c(results: List[Dict[str, Any]], out: str) -> str:
    """User income by region — moderate variant bar chart."""
    mod = [r for r in results if r["variant"] == "Moderate"]
    fig, ax = plt.subplots(figsize=(12, 6))

    regions = [r["region"] for r in mod]
    incomes = [r["monthly_net"] for r in mod]
    pcts = [r["income_pct_of_avg"] for r in mod]

    bars = ax.bar(regions, incomes, color="#3498DB", edgecolor="white")
    for bar, pct in zip(bars, pcts):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
                f"{pct:.1f}%\nof avg", ha="center", fontsize=8, fontweight="bold")

    ax.set_title("Monthly User Income by Region (Moderate: $0.20/GPU-hr)", fontsize=14, fontweight="bold")
    ax.set_ylabel("Monthly Net Income (USD)")
    ax.set_xticklabels(regions, rotation=20, ha="right")
    _watermark(ax)
    plt.tight_layout()
    path = os.path.join(out, "C_user_income_regions.png")
    fig.savefig(path, dpi=CHART_DPI)
    plt.close(fig)
    return path


def _chart_d(results: List[Dict[str, Any]], out: str) -> str:
    """Manufacturer savings (AWS) — grouped bars."""
    fig, ax = plt.subplots(figsize=(14, 7))
    mfgs = sorted(set(r["manufacturer"] for r in results),
                  key=lambda m: -max(r["annual_savings"] for r in results if r["manufacturer"] == m))
    x = np.arange(len(mfgs))
    width = 0.2

    for i, variant in enumerate(VARIANT_NAMES):
        vals = [next((r["annual_savings"] for r in results
                      if r["manufacturer"] == m and r["variant"] == variant), 0) for m in mfgs]
        ax.bar(x + i*width, vals, width, label=variant, color=VARIANT_COLORS[i], edgecolor="white")

    ax.set_xticks(x + width*1.5)
    ax.set_xticklabels(mfgs, rotation=15, ha="right")
    ax.set_title("Annual Savings: Manufacturer AI via NHP vs AWS", fontsize=14, fontweight="bold")
    ax.set_ylabel("Annual Savings (USD)")
    ax.legend()
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda v, _: _fmt_money(v)))
    _watermark(ax)
    plt.tight_layout()
    path = os.path.join(out, "D_manufacturer_savings.png")
    fig.savefig(path, dpi=CHART_DPI)
    plt.close(fig)
    return path


def _chart_e(results: List[Dict[str, Any]], out: str) -> str:
    """Environmental impact — net CO2 per manufacturer."""
    fig, ax = plt.subplots(figsize=(14, 7))
    mfgs = sorted(set(r["manufacturer"] for r in results),
                  key=lambda m: -max(r["co2_saved_net"] for r in results if r["manufacturer"] == m))
    x = np.arange(len(mfgs))
    width = 0.2

    for i, variant in enumerate(VARIANT_NAMES):
        vals = [next((r["co2_saved_net"] for r in results
                      if r["manufacturer"] == m and r["variant"] == variant), 0) for m in mfgs]
        ax.bar(x + i*width, vals, width, label=variant, color=VARIANT_COLORS[i], edgecolor="white")

    ax.set_xticks(x + width*1.5)
    ax.set_xticklabels(mfgs, rotation=15, ha="right")
    ax.set_title("Net CO₂ Saved per Year by Manufacturer Fleet", fontsize=14, fontweight="bold")
    ax.set_ylabel("Tons CO₂ / Year")
    ax.legend()
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda v, _: f"{v:,.0f}"))
    _watermark(ax)
    plt.tight_layout()
    path = os.path.join(out, "E_environmental.png")
    fig.savefig(path, dpi=CHART_DPI)
    plt.close(fig)
    return path


def _chart_f(results: List[Dict[str, Any]], out: str) -> str:
    """Network alliances — moderate variant comparison."""
    mod = [r for r in results if r["variant"] == "Moderate"]
    fig, ax = plt.subplots(figsize=(12, 6))
    alliances = [r["alliance"] for r in mod]
    vals = [r["h100_equivalent"] for r in mod]

    bars = ax.barh(alliances, vals, color="#3498DB", edgecolor="white")
    for bar, val in zip(bars, vals):
        ax.text(bar.get_width() + max(vals)*0.01, bar.get_y() + bar.get_height()/2,
                f"{val:,.0f}", va="center", fontweight="bold", fontsize=9)

    ax.set_title("Network Alliance Power (Moderate, 25% Uptime)", fontsize=14, fontweight="bold")
    ax.set_xlabel("H100 Equivalents")
    _watermark(ax)
    plt.tight_layout()
    path = os.path.join(out, "F_network_alliances.png")
    fig.savefig(path, dpi=CHART_DPI)
    plt.close(fig)
    return path


def _chart_g(results: List[Dict[str, Any]], out: str) -> str:
    """Task feasibility — heatmap-style."""
    mod = [r for r in results if r["variant"] == "Moderate"]
    fig, ax = plt.subplots(figsize=(10, 5))
    tasks = [r["task_name"] for r in mod]
    scores = [r["feasibility_score"] for r in mod]

    colors_list = ["#E74C3C" if s < 40 else "#E67E22" if s < 60 else "#2ECC71" for s in scores]
    bars = ax.barh(tasks, scores, color=colors_list, edgecolor="white")
    for bar, val in zip(bars, scores):
        ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2,
                f"{val:.0f}/100", va="center", fontweight="bold", fontsize=10)

    ax.set_xlim(0, 110)
    ax.set_title("AI Task Feasibility for NHP (20% Overhead)", fontsize=14, fontweight="bold")
    ax.set_xlabel("Feasibility Score")
    _watermark(ax)
    plt.tight_layout()
    path = os.path.join(out, "G_task_feasibility.png")
    fig.savefig(path, dpi=CHART_DPI)
    plt.close(fig)
    return path


def _chart_i(results: List[Dict[str, Any]], out: str) -> str:
    """Market size — moderate variant."""
    mod = [r for r in results if r["variant"] == "Moderate"]
    fig, ax = plt.subplots(figsize=(12, 6))
    regions = [r["region"] for r in mod]
    devices = [r["nhp_devices"] for r in mod]

    bars = ax.bar(regions, devices, color="#2ECC71", edgecolor="white")
    for bar, val in zip(bars, devices):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(devices)*0.02,
                f"{val:,.0f}", ha="center", fontsize=8, fontweight="bold", rotation=45)

    ax.set_title("Potential NHP Devices by Region (5% Penetration)", fontsize=14, fontweight="bold")
    ax.set_ylabel("Devices")
    ax.set_xticklabels(regions, rotation=20, ha="right")
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda v, _: f"{v/1e6:.1f}M"))
    _watermark(ax)
    plt.tight_layout()
    path = os.path.join(out, "I_market_size.png")
    fig.savefig(path, dpi=CHART_DPI)
    plt.close(fig)
    return path


def _chart_j(results: List[Dict[str, Any]], out: str) -> str:
    """Token economics — moderate variant across scales."""
    mod = [r for r in results if r["variant"] == "Moderate"]
    fig, ax = plt.subplots(figsize=(12, 6))
    labels = [r["scale_label"] for r in mod]
    revenues = [r["platform_revenue_monthly"] for r in mod]

    bars = ax.bar(labels, revenues, color="#3498DB", edgecolor="white")
    for bar, val in zip(bars, revenues):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(revenues)*0.02,
                _fmt_money(val), ha="center", fontsize=9, fontweight="bold")

    ax.set_title("Monthly Platform Revenue by Network Scale (Moderate)", fontsize=14, fontweight="bold")
    ax.set_ylabel("Monthly Revenue (USD)")
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda v, _: _fmt_money(v)))
    _watermark(ax)
    plt.tight_layout()
    path = os.path.join(out, "J_token_economics.png")
    fig.savefig(path, dpi=CHART_DPI)
    plt.close(fig)
    return path


def _chart_k(results: List[Dict[str, Any]], out: str) -> str:
    """Competitive — moderate variant power ratio."""
    mod = [r for r in results if r["variant"] == "Moderate"]
    fig, ax = plt.subplots(figsize=(10, 5))
    comps = [r["competitor"] for r in mod]
    ratios = [min(r["power_ratio"], 100) for r in mod]

    bars = ax.barh(comps, ratios, color="#2ECC71", edgecolor="white")
    for bar, val in zip(bars, ratios):
        label = f"{val:.0f}×" if val < 100 else "100×+"
        ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2,
                label, va="center", fontweight="bold", fontsize=11)

    ax.set_title("NHP Power Advantage vs Competitors (Moderate)", fontsize=14, fontweight="bold")
    ax.set_xlabel("Power Ratio (NHP / Competitor)")
    ax.axvline(x=1, color="red", linewidth=1, linestyle="--", alpha=0.5)
    _watermark(ax)
    plt.tight_layout()
    path = os.path.join(out, "K_competitive.png")
    fig.savefig(path, dpi=CHART_DPI)
    plt.close(fig)
    return path
