"""
NHP Simulation — Chart Generator
Produces high-quality charts for all 5 scenarios.
"""
from typing import Dict, Any, List
import os

import matplotlib
matplotlib.use("Agg")  # Non-interactive backend
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

import config


# ── Color map ────────────────────────────────────────────────────────────────
COLORS: Dict[str, str] = {
    "Optimistic": config.COLOR_OPTIMISTIC,
    "Moderate": config.COLOR_MODERATE,
    "Pessimistic": config.COLOR_PESSIMISTIC,
    "Catastrophic": config.COLOR_CATASTROPHIC,
}


def _ensure_dir(path: str) -> None:
    """Create directory if it doesn't exist."""
    os.makedirs(path, exist_ok=True)


def _apply_style() -> None:
    """Apply the project-wide chart style."""
    plt.style.use(config.CHART_STYLE)
    plt.rcParams["font.family"] = config.CHART_FONT
    plt.rcParams["font.size"] = 12


def _add_watermark(ax: plt.Axes) -> None:
    """Add watermark text to the bottom-right of the axes."""
    ax.text(
        0.99, 0.01, config.CHART_WATERMARK,
        transform=ax.transAxes,
        fontsize=8, color="gray", alpha=0.5,
        ha="right", va="bottom",
    )


# ── Scenario 1: Computing Power (Bar Chart) ─────────────────────────────────
def generate_scenario_01(results: List[Dict[str, Any]]) -> str:
    """Generate a bar chart comparing H100 equivalents across variants.

    Args:
        results: List of result dicts from scenario 01 variants.

    Returns:
        Path to the saved combined chart PNG.
    """
    _apply_style()
    fig, ax = plt.subplots(figsize=(10, 6))

    variants = [r["variant"] for r in results]
    h100_vals = [r["h100_equivalent"] for r in results]
    colors = [COLORS[v] for v in variants]

    bars = ax.bar(variants, h100_vals, color=colors, edgecolor="white", linewidth=1.2)

    # Add value labels on bars
    for bar, val in zip(bars, h100_vals):
        ax.text(
            bar.get_x() + bar.get_width() / 2, bar.get_height() + max(h100_vals) * 0.02,
            f"{val:,.0f}", ha="center", va="bottom", fontweight="bold", fontsize=11,
        )

    ax.set_title("Computing Power: H100 Equivalents\n(1M Galaxy S24 Network)", fontsize=config.CHART_TITLE_SIZE, fontweight="bold")
    ax.set_ylabel("Nvidia H100 Equivalents")
    ax.set_xlabel("Scenario Variant")
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))

    _add_watermark(ax)
    plt.tight_layout()

    out_dir = os.path.join(config.ASSETS_DIR, "scenario_01")
    _ensure_dir(out_dir)
    path = os.path.join(out_dir, "scenario_01_combined_chart.png")
    fig.savefig(path, dpi=config.CHART_DPI, format=config.CHART_FORMAT)
    plt.close(fig)
    return path


# ── Scenario 2: User Income (Grouped Bar Chart) ─────────────────────────────
def generate_scenario_02(results: List[Dict[str, Any]]) -> str:
    """Generate a grouped bar chart showing monthly & annual income.

    Args:
        results: List of result dicts from scenario 02 variants.

    Returns:
        Path to the saved combined chart PNG.
    """
    _apply_style()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    variants = [r["variant"] for r in results]
    monthly = [r["monthly_net"] for r in results]
    annual = [r["annual_net"] for r in results]
    colors = [COLORS[v] for v in variants]

    # Monthly income
    bars1 = ax1.bar(variants, monthly, color=colors, edgecolor="white", linewidth=1.2)
    for bar, val in zip(bars1, monthly):
        ax1.text(
            bar.get_x() + bar.get_width() / 2, bar.get_height() + max(max(monthly), 0.01) * 0.03,
            f"${val:.2f}", ha="center", va="bottom", fontweight="bold", fontsize=10,
        )
    ax1.set_title("Monthly Net Income per User", fontsize=13, fontweight="bold")
    ax1.set_ylabel("USD / Month")
    ax1.axhline(y=0, color="gray", linewidth=0.8, linestyle="--")
    _add_watermark(ax1)

    # Annual income
    bars2 = ax2.bar(variants, annual, color=colors, edgecolor="white", linewidth=1.2)
    for bar, val in zip(bars2, annual):
        ax2.text(
            bar.get_x() + bar.get_width() / 2, bar.get_height() + max(max(annual), 0.01) * 0.03,
            f"${val:.2f}", ha="center", va="bottom", fontweight="bold", fontsize=10,
        )
    ax2.set_title("Annual Net Income per User", fontsize=13, fontweight="bold")
    ax2.set_ylabel("USD / Year")
    ax2.axhline(y=0, color="gray", linewidth=0.8, linestyle="--")
    _add_watermark(ax2)

    fig.suptitle("User Income Analysis — NHP", fontsize=config.CHART_TITLE_SIZE, fontweight="bold")
    plt.tight_layout()

    out_dir = os.path.join(config.ASSETS_DIR, "scenario_02")
    _ensure_dir(out_dir)
    path = os.path.join(out_dir, "scenario_02_combined_chart.png")
    fig.savefig(path, dpi=config.CHART_DPI, format=config.CHART_FORMAT)
    plt.close(fig)
    return path


# ── Scenario 3: Manufacturer Savings (Pie Charts) ───────────────────────────
def generate_scenario_03(results: List[Dict[str, Any]]) -> str:
    """Generate pie charts showing AWS vs NHP cost split per variant.

    Args:
        results: List of result dicts from scenario 03 variants.

    Returns:
        Path to the saved combined chart PNG.
    """
    _apply_style()
    fig, axes = plt.subplots(1, 4, figsize=(18, 5))

    for ax, r in zip(axes, results):
        nhp_share = r["monthly_savings"]
        aws_share = r["monthly_aws_remaining"]
        labels = ["NHP Savings", "Remaining AWS"]
        sizes = [nhp_share, aws_share]
        chart_colors = [COLORS[r["variant"]], "#95A5A6"]

        ax.pie(
            sizes, labels=labels, colors=chart_colors,
            autopct="%1.1f%%", startangle=90,
            textprops={"fontsize": 9},
        )
        annual_str = _format_money(r["annual_savings"])
        ax.set_title(f"{r['variant']}\n({r['coverage_pct']:.0f}% coverage)\nSaves {annual_str}/yr",
                      fontsize=10, fontweight="bold")

    fig.suptitle("Manufacturer Savings: AWS vs NHP Cost Split", fontsize=config.CHART_TITLE_SIZE, fontweight="bold")
    plt.tight_layout()

    out_dir = os.path.join(config.ASSETS_DIR, "scenario_03")
    _ensure_dir(out_dir)
    path = os.path.join(out_dir, "scenario_03_combined_chart.png")
    fig.savefig(path, dpi=config.CHART_DPI, format=config.CHART_FORMAT)
    plt.close(fig)
    return path


# ── Scenario 4: Network Growth (Line Chart) ─────────────────────────────────
def generate_scenario_04(results: List[Dict[str, Any]]) -> str:
    """Generate an exponential growth line chart over 5 years.

    Args:
        results: List of result dicts from scenario 04 variants.

    Returns:
        Path to the saved combined chart PNG.
    """
    _apply_style()
    fig, ax = plt.subplots(figsize=(12, 7))

    years = list(range(1, config.SIMULATION_YEARS + 1))

    for r in results:
        color = COLORS[r["variant"]]
        devices = r["yearly_devices"]
        ax.plot(
            years, devices, marker="o", linewidth=2.5,
            color=color, label=f"{r['variant']} ({r['growth_pct']:.0f}%/yr)",
        )
        # Label end point
        ax.annotate(
            f"{devices[-1]:,.0f}",
            xy=(years[-1], devices[-1]),
            xytext=(10, 0), textcoords="offset points",
            fontsize=9, fontweight="bold", color=color,
        )

    ax.set_yscale("log")
    ax.set_title("Network Growth Projection (5 Years)", fontsize=config.CHART_TITLE_SIZE, fontweight="bold")
    ax.set_xlabel("Year")
    ax.set_ylabel("Number of Devices (log scale)")
    ax.set_xticks(years)
    ax.legend(fontsize=10)
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
    ax.grid(True, alpha=0.3)

    _add_watermark(ax)
    plt.tight_layout()

    out_dir = os.path.join(config.ASSETS_DIR, "scenario_04")
    _ensure_dir(out_dir)
    path = os.path.join(out_dir, "scenario_04_combined_chart.png")
    fig.savefig(path, dpi=config.CHART_DPI, format=config.CHART_FORMAT)
    plt.close(fig)
    return path


# ── Scenario 5: Environmental Impact (Bar Chart) ────────────────────────────
def generate_scenario_05(results: List[Dict[str, Any]]) -> str:
    """Generate a bar chart showing CO2 savings and cars-equivalent.

    Args:
        results: List of result dicts from scenario 05 variants.

    Returns:
        Path to the saved combined chart PNG.
    """
    _apply_style()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    variants = [r["variant"] for r in results]
    co2_tons = [r["co2_saved_tons"] for r in results]
    cars = [r["cars_equivalent"] for r in results]
    colors = [COLORS[v] for v in variants]

    # CO2 saved
    bars1 = ax1.bar(variants, co2_tons, color=colors, edgecolor="white", linewidth=1.2)
    for bar, val in zip(bars1, co2_tons):
        ax1.text(
            bar.get_x() + bar.get_width() / 2, bar.get_height() + max(co2_tons) * 0.02,
            f"{val:,.0f}", ha="center", va="bottom", fontweight="bold", fontsize=10,
        )
    ax1.set_title("CO₂ Saved per Year (tons)", fontsize=13, fontweight="bold")
    ax1.set_ylabel("Metric Tons CO₂")
    ax1.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
    _add_watermark(ax1)

    # Cars equivalent
    bars2 = ax2.bar(variants, cars, color=colors, edgecolor="white", linewidth=1.2)
    for bar, val in zip(bars2, cars):
        ax2.text(
            bar.get_x() + bar.get_width() / 2, bar.get_height() + max(cars) * 0.02,
            f"{val:,.0f}", ha="center", va="bottom", fontweight="bold", fontsize=10,
        )
    ax2.set_title("Equivalent Cars Removed from Roads", fontsize=13, fontweight="bold")
    ax2.set_ylabel("Number of Cars")
    ax2.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
    _add_watermark(ax2)

    fig.suptitle("Environmental Impact — NHP", fontsize=config.CHART_TITLE_SIZE, fontweight="bold")
    plt.tight_layout()

    out_dir = os.path.join(config.ASSETS_DIR, "scenario_05")
    _ensure_dir(out_dir)
    path = os.path.join(out_dir, "scenario_05_combined_chart.png")
    fig.savefig(path, dpi=config.CHART_DPI, format=config.CHART_FORMAT)
    plt.close(fig)
    return path


# ── Helper ───────────────────────────────────────────────────────────────────
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
