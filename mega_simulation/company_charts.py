"""
NHP Phase 3 — Per-Company Chart Generator
Produces dedicated charts for each manufacturer's deep-dive report.
"""
import os
from typing import Dict, Any, List

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

from mega_simulation.data import (
    CLOUD_PROVIDERS, REGIONS, VARIANT_NAMES, VARIANT_COLORS,
    VARIANT_EMOJIS, UPTIME_VARIANTS, COVERAGE_VARIANTS,
    TOKEN_PRICE_VARIANTS, DC_REPLACED_VARIANTS, GROWTH_VARIANTS,
    H100_TOPS, NIGHTLY_HOURS, DEVICE_EXTRA_WATT, GPU_REQUEST_TIME_SEC,
    CO2_PER_KWH_KG, DC_CO2_TONS_YEAR, CO2_PER_CAR_TONS, SIMULATION_YEARS,
)
from mega_simulation.company_profiles import CompanyProfile

CHART_DPI: int = 300
WATERMARK: str = "NHP Protocol v2.0"


def _fmt(val: float) -> str:
    if abs(val) >= 1e9: return f"${val/1e9:.1f}B"
    if abs(val) >= 1e6: return f"${val/1e6:.1f}M"
    if abs(val) >= 1e3: return f"${val/1e3:.0f}K"
    return f"${val:.2f}"


def _wm(ax: plt.Axes) -> None:
    ax.text(0.99, 0.01, WATERMARK, transform=ax.transAxes,
            fontsize=7, color="gray", alpha=0.4, ha="right", va="bottom")


def generate_company_charts(
    key: str,
    profile: CompanyProfile,
    output_dir: str,
) -> List[str]:
    """Generate all charts for a single company.

    Args:
        key: Company key (e.g. 'samsung').
        profile: Company profile data.
        output_dir: Directory to save charts.

    Returns:
        List of saved chart file paths.
    """
    os.makedirs(output_dir, exist_ok=True)
    plt.style.use("seaborn-v0_8-darkgrid")
    plt.rcParams["font.family"] = "DejaVu Sans"
    plt.rcParams["font.size"] = 10

    saved: List[str] = []
    saved.append(_chart_fleet_power(key, profile, output_dir))
    saved.append(_chart_cloud_savings(key, profile, output_dir))
    saved.append(_chart_user_income(key, profile, output_dir))
    saved.append(_chart_environmental(key, profile, output_dir))
    saved.append(_chart_network_growth(key, profile, output_dir))
    saved.append(_chart_breakeven(key, profile, output_dir))
    return saved


def _chart_fleet_power(key: str, p: CompanyProfile, out: str) -> str:
    """Chart 1: Fleet computing power — H100 equivalents per variant."""
    fig, ax = plt.subplots(figsize=(10, 6))

    avg_fl = sum(d.tops for d in p.flagship_models) / len(p.flagship_models) if p.flagship_models else 0
    avg_mr = sum(d.tops for d in p.midrange_models) / len(p.midrange_models) if p.midrange_models else 0

    variants = VARIANT_NAMES
    h100_vals = []
    active_vals = []
    for uptime in UPTIME_VARIANTS:
        total = p.total_active_devices_millions * 1_000_000
        active = int(total * uptime)
        fl = int(active * 0.25)
        mr = active - fl
        tops = fl * avg_fl + mr * avg_mr
        h100_vals.append(tops / H100_TOPS)
        active_vals.append(active)

    bars = ax.bar(variants, h100_vals, color=VARIANT_COLORS, edgecolor="white", width=0.6)
    for bar, val, act in zip(bars, h100_vals, active_vals):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(h100_vals)*0.02,
                f"{val:,.0f}\n({act/1e6:.1f}M active)",
                ha="center", fontsize=9, fontweight="bold")

    ax.set_title(f"{p.name} — Fleet Computing Power (H100 Equivalents)", fontsize=14, fontweight="bold")
    ax.set_ylabel("H100 Equivalents")
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda v, _: f"{v:,.0f}"))
    _wm(ax)
    plt.tight_layout()
    path = os.path.join(out, f"{key}_01_fleet_power.png")
    fig.savefig(path, dpi=CHART_DPI)
    plt.close(fig)
    return path


def _chart_cloud_savings(key: str, p: CompanyProfile, out: str) -> str:
    """Chart 2: Cost savings vs all cloud providers (moderate variant)."""
    fig, ax = plt.subplots(figsize=(12, 6))

    total_daily_requests = sum(s.daily_requests_estimate for s in p.ai_services)
    total_daily_gpu_hr = (total_daily_requests * GPU_REQUEST_TIME_SEC) / 3600.0
    coverage = COVERAGE_VARIANTS[1]  # Moderate

    cloud_names = []
    savings = []
    for ck, cloud in CLOUD_PROVIDERS.items():
        per_gpu_hr = cloud.hourly_cost / cloud.gpus_per_instance
        annual_cost = total_daily_gpu_hr * per_gpu_hr * 365
        annual_savings = annual_cost * coverage
        cloud_names.append(f"{cloud.name}\n({cloud.gpu_model})")
        savings.append(annual_savings)

    colors = plt.cm.Set2(np.linspace(0, 1, len(cloud_names)))
    bars = ax.bar(cloud_names, savings, color=colors, edgecolor="white")
    for bar, val in zip(bars, savings):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(savings)*0.02,
                _fmt(val), ha="center", fontsize=9, fontweight="bold")

    ax.set_title(f"{p.name} — Annual Savings: NHP vs Cloud Providers (40% Coverage)",
                fontsize=13, fontweight="bold")
    ax.set_ylabel("Annual Savings (USD)")
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda v, _: _fmt(v)))
    _wm(ax)
    plt.tight_layout()
    path = os.path.join(out, f"{key}_02_cloud_savings.png")
    fig.savefig(path, dpi=CHART_DPI)
    plt.close(fig)
    return path


def _chart_user_income(key: str, p: CompanyProfile, out: str) -> str:
    """Chart 3: User monthly income in primary markets (moderate)."""
    fig, ax = plt.subplots(figsize=(12, 6))

    token_price = TOKEN_PRICE_VARIANTS[1]  # Moderate
    markets = []
    incomes = []
    pcts = []

    for market in p.primary_markets:
        region = None
        for rval in REGIONS.values():
            if rval.name.lower().startswith(market.lower()[:4]):
                region = rval
                break
        if not region:
            from mega_simulation.data import Region
            region = Region(market, market, 0.12, 1000, 0.60, 100, "UTC")

        daily_kwh = (DEVICE_EXTRA_WATT * NIGHTLY_HOURS) / 1000.0
        daily_elec = daily_kwh * region.electricity_cost_kwh
        daily_net = (NIGHTLY_HOURS * token_price) - daily_elec
        monthly_net = daily_net * 30
        pct = (monthly_net / region.avg_monthly_income * 100) if region.avg_monthly_income > 0 else 0

        markets.append(market)
        incomes.append(monthly_net)
        pcts.append(pct)

    bars = ax.bar(markets, incomes, color="#3498DB", edgecolor="white")
    for bar, val, pct in zip(bars, incomes, pcts):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(incomes)*0.03,
                f"${val:.2f}\n({pct:.1f}% of avg)",
                ha="center", fontsize=9, fontweight="bold")

    ax.set_title(f"{p.name} — User Monthly Income by Market ($0.20/GPU-hr)",
                fontsize=13, fontweight="bold")
    ax.set_ylabel("Monthly Net Income (USD)")
    _wm(ax)
    plt.tight_layout()
    path = os.path.join(out, f"{key}_03_user_income.png")
    fig.savefig(path, dpi=CHART_DPI)
    plt.close(fig)
    return path


def _chart_environmental(key: str, p: CompanyProfile, out: str) -> str:
    """Chart 4: Environmental impact — CO2 saved per variant."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    co2_vals = []
    cars_vals = []
    for uptime, dc in zip(UPTIME_VARIANTS, DC_REPLACED_VARIANTS):
        co2_saved = DC_CO2_TONS_YEAR * dc
        total = p.total_active_devices_millions * 1_000_000
        active = int(total * uptime)
        daily_kwh = active * (DEVICE_EXTRA_WATT * NIGHTLY_HOURS) / 1000.0
        co2_added = (daily_kwh * 365 * CO2_PER_KWH_KG) / 1000.0
        net = co2_saved - co2_added
        co2_vals.append(net)
        cars_vals.append(int(net / CO2_PER_CAR_TONS))

    ax1.bar(VARIANT_NAMES, co2_vals, color=VARIANT_COLORS, edgecolor="white")
    for i, val in enumerate(co2_vals):
        ax1.text(i, val + max(co2_vals)*0.02, f"{val:,.0f}",
                ha="center", fontsize=9, fontweight="bold")
    ax1.set_title("Net CO₂ Saved (tons/year)", fontsize=12, fontweight="bold")
    ax1.yaxis.set_major_formatter(ticker.FuncFormatter(lambda v, _: f"{v:,.0f}"))
    _wm(ax1)

    ax2.bar(VARIANT_NAMES, cars_vals, color=VARIANT_COLORS, edgecolor="white")
    for i, val in enumerate(cars_vals):
        ax2.text(i, val + max(cars_vals)*0.02, f"{val:,.0f}",
                ha="center", fontsize=9, fontweight="bold")
    ax2.set_title("Equivalent Cars Removed", fontsize=12, fontweight="bold")
    ax2.yaxis.set_major_formatter(ticker.FuncFormatter(lambda v, _: f"{v:,.0f}"))
    _wm(ax2)

    fig.suptitle(f"{p.name} — Environmental Impact", fontsize=14, fontweight="bold", y=1.02)
    plt.tight_layout()
    path = os.path.join(out, f"{key}_04_environmental.png")
    fig.savefig(path, dpi=CHART_DPI, bbox_inches="tight")
    plt.close(fig)
    return path


def _chart_network_growth(key: str, p: CompanyProfile, out: str) -> str:
    """Chart 5: Network growth projection — 5 years."""
    fig, ax = plt.subplots(figsize=(12, 6))

    base = p.annual_phone_sales_millions * 1_000_000 * 0.05
    max_devices = p.total_active_devices_millions * 1_000_000
    years = list(range(1, SIMULATION_YEARS + 1))

    for i, (vname, growth) in enumerate(zip(VARIANT_NAMES, GROWTH_VARIANTS)):
        projections = []
        current = float(base)
        for y in range(SIMULATION_YEARS):
            current = min(current * (1 + growth), max_devices)
            projections.append(current)
        ax.plot(years, projections, marker="o", linewidth=2.5,
                color=VARIANT_COLORS[i], label=f"{vname} ({growth*100:.0f}%/yr)",
                markersize=8)
        ax.text(years[-1] + 0.1, projections[-1], f"{projections[-1]/1e6:.1f}M",
                fontsize=9, fontweight="bold", color=VARIANT_COLORS[i], va="center")

    ax.set_title(f"{p.name} — NHP Network Growth (5 Years)", fontsize=14, fontweight="bold")
    ax.set_xlabel("Year")
    ax.set_ylabel("Devices")
    ax.set_xticks(years)
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda v, _: f"{v/1e6:.1f}M"))
    ax.legend(loc="upper left")
    _wm(ax)
    plt.tight_layout()
    path = os.path.join(out, f"{key}_05_network_growth.png")
    fig.savefig(path, dpi=CHART_DPI)
    plt.close(fig)
    return path


def _chart_breakeven(key: str, p: CompanyProfile, out: str) -> str:
    """Chart 6: Breakeven & 5yr ROI analysis."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    total_daily_requests = sum(s.daily_requests_estimate for s in p.ai_services)
    total_daily_gpu_hr = (total_daily_requests * GPU_REQUEST_TIME_SEC) / 3600.0
    aws = CLOUD_PROVIDERS["aws_a100"]
    per_gpu_hr = aws.hourly_cost / aws.gpus_per_instance

    dev_costs = [50_000_000, 30_000_000, 20_000_000, 10_000_000]
    ops_monthly = 2_000_000
    breakevens = []
    rois = []

    for cov, dev_cost in zip(COVERAGE_VARIANTS, dev_costs):
        daily_cost = total_daily_gpu_hr * per_gpu_hr
        annual_savings = daily_cost * 365 * cov
        monthly_savings = annual_savings / 12
        net_monthly = monthly_savings - ops_monthly
        if net_monthly > 0:
            be = dev_cost / net_monthly
        else:
            be = 60  # cap at 60 months
        five_yr = (monthly_savings * 60) - dev_cost - (ops_monthly * 60)
        roi = (five_yr / dev_cost * 100) if dev_cost > 0 else 0
        breakevens.append(min(be, 60))
        rois.append(roi)

    bars1 = ax1.bar(VARIANT_NAMES, breakevens, color=VARIANT_COLORS, edgecolor="white")
    for bar, val in zip(bars1, breakevens):
        label = f"{val:.0f} mo" if val < 60 else "60+ mo"
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                label, ha="center", fontsize=10, fontweight="bold")
    ax1.set_title("Breakeven (months)", fontsize=12, fontweight="bold")
    ax1.set_ylabel("Months")
    ax1.axhline(y=12, color="green", linewidth=1, linestyle="--", alpha=0.5, label="1 year")
    ax1.axhline(y=24, color="orange", linewidth=1, linestyle="--", alpha=0.5, label="2 years")
    ax1.legend(fontsize=8)
    _wm(ax1)

    bars2 = ax2.bar(VARIANT_NAMES, rois, color=VARIANT_COLORS, edgecolor="white")
    for bar, val in zip(bars2, rois):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(max(rois), 1)*0.02,
                f"{val:.0f}%", ha="center", fontsize=10, fontweight="bold")
    ax2.set_title("5-Year ROI (%)", fontsize=12, fontweight="bold")
    ax2.set_ylabel("ROI %")
    ax2.axhline(y=0, color="red", linewidth=1, linestyle="--", alpha=0.5)
    _wm(ax2)

    fig.suptitle(f"{p.name} — Breakeven & ROI Analysis (vs AWS)", fontsize=14, fontweight="bold", y=1.02)
    plt.tight_layout()
    path = os.path.join(out, f"{key}_06_breakeven_roi.png")
    fig.savefig(path, dpi=CHART_DPI, bbox_inches="tight")
    plt.close(fig)
    return path
