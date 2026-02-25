"""
NHP Mega Simulation — Core Computation Engine
Pure functions that compute results from input parameters.
No side effects, no I/O. All data flows through arguments.
"""
from typing import Dict, Any, List
from mega_simulation.data import (
    Manufacturer, CloudProvider, Region, TaskType, Competitor,
    H100_TOPS, DEVICE_EXTRA_WATT, NIGHTLY_HOURS,
    GPU_REQUEST_TIME_SEC, CO2_PER_KWH_KG, DC_CO2_TONS_YEAR,
    CO2_PER_CAR_TONS, BATTERY_CYCLE_PER_NIGHT_PCT, BATTERY_TOTAL_CYCLES,
)


# ═══════════════════════════════════════════════════════════════════════════
# A. COMPUTING POWER
# ═══════════════════════════════════════════════════════════════════════════

def compute_fleet_power(
    mfg: Manufacturer,
    uptime: float,
) -> Dict[str, Any]:
    """Calculate total computing power of a manufacturer's fleet.

    Args:
        mfg: Manufacturer profile.
        uptime: Fraction of devices active.

    Returns:
        Dict with fleet TOPS, H100 equivalents, active device counts.
    """
    flagship_count: int = int(mfg.active_devices * mfg.flagship_pct)
    midrange_count: int = mfg.active_devices - flagship_count

    active_flagship: int = int(flagship_count * uptime)
    active_midrange: int = int(midrange_count * uptime)

    flagship_tops: float = active_flagship * mfg.flagship_tops
    midrange_tops: float = active_midrange * mfg.midrange_tops
    total_tops: float = flagship_tops + midrange_tops
    h100_equiv: float = total_tops / H100_TOPS

    return {
        "manufacturer": mfg.name,
        "total_devices": mfg.active_devices,
        "active_devices": active_flagship + active_midrange,
        "active_flagship": active_flagship,
        "active_midrange": active_midrange,
        "total_tops": total_tops,
        "h100_equivalent": h100_equiv,
        "uptime_pct": uptime * 100,
    }


# ═══════════════════════════════════════════════════════════════════════════
# B / D. COST COMPARISON & MANUFACTURER SAVINGS
# ═══════════════════════════════════════════════════════════════════════════

def compute_cost_comparison(
    mfg: Manufacturer,
    cloud: CloudProvider,
    coverage: float,
) -> Dict[str, Any]:
    """Compare NHP cost vs cloud provider for a manufacturer's AI workload.

    Args:
        mfg: Manufacturer profile.
        cloud: Cloud provider to compare against.
        coverage: Fraction of requests served by NHP.

    Returns:
        Dict with daily/monthly/annual costs and savings.
    """
    total_daily_gpu_sec: float = mfg.daily_ai_requests * GPU_REQUEST_TIME_SEC
    total_daily_gpu_hr: float = total_daily_gpu_sec / 3600.0

    # Cloud cost per GPU-hour (normalize to per-GPU-hour)
    cloud_per_gpu_hr: float = cloud.hourly_cost / cloud.gpus_per_instance

    daily_cloud_cost: float = total_daily_gpu_hr * cloud_per_gpu_hr
    daily_nhp_covered: float = daily_cloud_cost * coverage
    daily_cloud_remaining: float = daily_cloud_cost * (1 - coverage)

    monthly_savings: float = daily_nhp_covered * 30.0
    annual_savings: float = monthly_savings * 12.0
    annual_cloud_total: float = daily_cloud_cost * 365.0

    savings_pct: float = (annual_savings / annual_cloud_total * 100) if annual_cloud_total > 0 else 0

    return {
        "manufacturer": mfg.name,
        "cloud_provider": f"{cloud.name} ({cloud.gpu_model})",
        "cloud_short": cloud.short,
        "coverage_pct": coverage * 100,
        "daily_cloud_total": daily_cloud_cost,
        "daily_nhp_savings": daily_nhp_covered,
        "monthly_savings": monthly_savings,
        "annual_savings": annual_savings,
        "annual_cloud_total": annual_cloud_total,
        "savings_pct": savings_pct,
    }


# ═══════════════════════════════════════════════════════════════════════════
# C. USER INCOME BY REGION
# ═══════════════════════════════════════════════════════════════════════════

def compute_user_income(
    region: Region,
    token_price: float,
) -> Dict[str, Any]:
    """Calculate user income in a specific region.

    Args:
        region: Regional parameters (electricity cost, avg income).
        token_price: Revenue per GPU-hour.

    Returns:
        Dict with gross/net income, electricity cost, income as % of
        regional average.
    """
    daily_kwh: float = (DEVICE_EXTRA_WATT * NIGHTLY_HOURS) / 1000.0
    daily_electricity: float = daily_kwh * region.electricity_cost_kwh
    daily_gross: float = NIGHTLY_HOURS * token_price
    daily_net: float = daily_gross - daily_electricity

    monthly_net: float = daily_net * 30.0
    annual_net: float = monthly_net * 12.0
    monthly_electricity: float = daily_electricity * 30.0

    income_pct_of_avg: float = (monthly_net / region.avg_monthly_income * 100) if region.avg_monthly_income > 0 else 0

    return {
        "region": region.name,
        "region_ar": region.name_ar,
        "token_price": token_price,
        "electricity_cost_kwh": region.electricity_cost_kwh,
        "monthly_gross": daily_gross * 30.0,
        "monthly_electricity": monthly_electricity,
        "monthly_net": monthly_net,
        "annual_net": annual_net,
        "income_pct_of_avg": income_pct_of_avg,
        "avg_monthly_income": region.avg_monthly_income,
    }


# ═══════════════════════════════════════════════════════════════════════════
# E. ENVIRONMENTAL IMPACT
# ═══════════════════════════════════════════════════════════════════════════

def compute_environmental(
    mfg: Manufacturer,
    uptime: float,
    dc_replaced: float,
) -> Dict[str, Any]:
    """Calculate environmental impact for a manufacturer's fleet.

    Args:
        mfg: Manufacturer profile.
        uptime: Fraction of devices active.
        dc_replaced: Number of data centers replaced.

    Returns:
        Dict with CO2 saved, phone-side CO2 added, net impact, cars.
    """
    co2_saved: float = DC_CO2_TONS_YEAR * dc_replaced

    # CO2 *added* by phones running NHP
    active_devices: int = int(mfg.active_devices * uptime)
    daily_kwh_all: float = active_devices * (DEVICE_EXTRA_WATT * NIGHTLY_HOURS) / 1000.0
    annual_kwh_all: float = daily_kwh_all * 365.0
    co2_added_tons: float = (annual_kwh_all * CO2_PER_KWH_KG) / 1000.0
    net_co2_saved: float = co2_saved - co2_added_tons
    cars_equivalent: int = int(net_co2_saved / CO2_PER_CAR_TONS)

    return {
        "manufacturer": mfg.name,
        "dc_replaced": dc_replaced,
        "co2_saved_gross": co2_saved,
        "co2_added_phones": co2_added_tons,
        "co2_saved_net": net_co2_saved,
        "cars_equivalent": cars_equivalent,
        "active_devices": active_devices,
    }


# ═══════════════════════════════════════════════════════════════════════════
# F. NETWORK EFFECTS (COMBINED FLEETS)
# ═══════════════════════════════════════════════════════════════════════════

def compute_combined_network(
    manufacturers: List[Manufacturer],
    uptime: float,
) -> Dict[str, Any]:
    """Calculate combined computing power of multiple manufacturers.

    Args:
        manufacturers: List of manufacturer profiles.
        uptime: Fraction of devices active.

    Returns:
        Dict with combined fleet stats.
    """
    total_devices: int = 0
    total_tops: float = 0.0
    names: List[str] = []

    for mfg in manufacturers:
        result = compute_fleet_power(mfg, uptime)
        total_devices += result["active_devices"]
        total_tops += result["total_tops"]
        names.append(mfg.short)

    h100_equiv: float = total_tops / H100_TOPS

    return {
        "alliance": " + ".join(names),
        "manufacturers_count": len(manufacturers),
        "total_active_devices": total_devices,
        "total_tops": total_tops,
        "h100_equivalent": h100_equiv,
        "uptime_pct": uptime * 100,
    }


# ═══════════════════════════════════════════════════════════════════════════
# G. TASK TYPE FEASIBILITY
# ═══════════════════════════════════════════════════════════════════════════

def compute_task_feasibility(
    task: TaskType,
    fleet_tops: float,
    active_devices: int,
    avg_tops_per_device: float,
    overhead: float,
) -> Dict[str, Any]:
    """Evaluate whether NHP can handle a specific task type.

    Args:
        task: AI task type profile.
        fleet_tops: Total fleet TOPS available.
        active_devices: Number of active devices.
        avg_tops_per_device: Average TOPS per device.
        overhead: NHP coordination overhead (0-1).

    Returns:
        Dict with feasibility score, tasks/sec, market share potential.
    """
    effective_tops: float = fleet_tops * (1 - overhead) * task.parallelizable
    device_capable: bool = avg_tops_per_device >= task.min_tops_required

    if task.gpu_seconds_per_task > 0:
        tasks_per_second: float = effective_tops / (task.min_tops_required * task.gpu_seconds_per_task / 1.0)
    else:
        tasks_per_second = 0

    tasks_per_day: float = tasks_per_second * 86400
    tasks_per_month: float = tasks_per_day * 30

    # Revenue estimate (assume $0.001 per task for small tasks, scaled by gpu time)
    revenue_per_task: float = max(0.0001, task.gpu_seconds_per_task * 0.01)
    monthly_revenue: float = tasks_per_month * revenue_per_task
    annual_revenue: float = monthly_revenue * 12

    feasibility_score: float = min(100, (
        (30 if device_capable else 0) +
        (30 * task.parallelizable) +
        (20 if not task.latency_sensitive else 5) +
        (20 * (1 - overhead))
    ))

    return {
        "task_name": task.name,
        "task_name_ar": task.name_ar,
        "device_capable": device_capable,
        "effective_tops": effective_tops,
        "tasks_per_second": tasks_per_second,
        "tasks_per_day": tasks_per_day,
        "feasibility_score": feasibility_score,
        "annual_revenue_estimate": annual_revenue,
        "latency_sensitive": task.latency_sensitive,
        "parallelizable_pct": task.parallelizable * 100,
        "overhead_pct": overhead * 100,
    }


# ═══════════════════════════════════════════════════════════════════════════
# H. BATTERY IMPACT
# ═══════════════════════════════════════════════════════════════════════════

def compute_battery_impact(
    tier_name: str,
    nightly_hours: float = NIGHTLY_HOURS,
) -> Dict[str, Any]:
    """Estimate NHP impact on phone battery lifespan.

    Args:
        tier_name: Device tier label.
        nightly_hours: Hours of GPU operation per night.

    Returns:
        Dict with battery cycle analysis.
    """
    cycles_per_night: float = BATTERY_CYCLE_PER_NIGHT_PCT / 100.0
    cycles_per_year: float = cycles_per_night * 365
    years_of_battery: float = BATTERY_TOTAL_CYCLES / (cycles_per_year + 365 * 0.3)  # 0.3 = normal daily usage
    years_without_nhp: float = BATTERY_TOTAL_CYCLES / (365 * 0.3)
    reduction_months: float = (years_without_nhp - years_of_battery) * 12

    return {
        "tier": tier_name,
        "cycles_per_night": cycles_per_night,
        "extra_cycles_per_year": cycles_per_year,
        "battery_life_with_nhp_years": years_of_battery,
        "battery_life_without_nhp_years": years_without_nhp,
        "life_reduction_months": reduction_months,
    }


# ═══════════════════════════════════════════════════════════════════════════
# I. MARKET SIZE
# ═══════════════════════════════════════════════════════════════════════════

def compute_market_size(
    region: Region,
    penetration_rate: float,
) -> Dict[str, Any]:
    """Calculate TAM/SAM/SOM for a region.

    Args:
        region: Regional parameters.
        penetration_rate: NHP adoption rate among smartphone users.

    Returns:
        Dict with device counts and revenue projections.
    """
    total_smartphones: int = int(region.population_millions * 1_000_000 * region.smartphone_penetration)
    nhp_devices: int = int(total_smartphones * penetration_rate)

    # Revenue from user fees (platform takes ~15%)
    avg_device_monthly_rev: float = NIGHTLY_HOURS * 0.20 * 30 * 0.15  # moderate token price, 15% cut
    monthly_platform_revenue: float = nhp_devices * avg_device_monthly_rev
    annual_platform_revenue: float = monthly_platform_revenue * 12

    return {
        "region": region.name,
        "region_ar": region.name_ar,
        "total_smartphones": total_smartphones,
        "nhp_devices": nhp_devices,
        "penetration_pct": penetration_rate * 100,
        "monthly_platform_revenue": monthly_platform_revenue,
        "annual_platform_revenue": annual_platform_revenue,
    }


# ═══════════════════════════════════════════════════════════════════════════
# J. TOKEN ECONOMICS
# ═══════════════════════════════════════════════════════════════════════════

def compute_token_economics(
    total_devices: int,
    uptime: float,
    token_price: float,
    platform_cut: float = 0.15,
) -> Dict[str, Any]:
    """Model token supply/demand dynamics.

    Args:
        total_devices: Number of devices in network.
        uptime: Fraction active.
        token_price: USD per token (1 token = 1 GPU-hour).
        platform_cut: NHP's fee percentage.

    Returns:
        Dict with token flow analysis.
    """
    active_devices: int = int(total_devices * uptime)
    daily_gpu_hours: float = active_devices * NIGHTLY_HOURS
    monthly_gpu_hours: float = daily_gpu_hours * 30

    total_token_flow_monthly: float = monthly_gpu_hours * token_price
    platform_revenue_monthly: float = total_token_flow_monthly * platform_cut
    user_payouts_monthly: float = total_token_flow_monthly * (1 - platform_cut)

    # Market cap estimate (token_flow * 12 * multiple)
    implied_annual_flow: float = total_token_flow_monthly * 12
    market_cap_conservative: float = implied_annual_flow * 5
    market_cap_aggressive: float = implied_annual_flow * 20

    return {
        "total_devices": total_devices,
        "active_devices": active_devices,
        "token_price": token_price,
        "monthly_gpu_hours": monthly_gpu_hours,
        "total_monthly_flow": total_token_flow_monthly,
        "platform_revenue_monthly": platform_revenue_monthly,
        "user_payouts_monthly": user_payouts_monthly,
        "implied_annual_flow": implied_annual_flow,
        "market_cap_conservative": market_cap_conservative,
        "market_cap_aggressive": market_cap_aggressive,
    }


# ═══════════════════════════════════════════════════════════════════════════
# K. COMPETITIVE POSITIONING
# ═══════════════════════════════════════════════════════════════════════════

def compute_competitive(
    nhp_devices: int,
    nhp_avg_tops: float,
    nhp_uptime: float,
    competitor: Competitor,
) -> Dict[str, Any]:
    """Compare NHP network power vs a competitor.

    Args:
        nhp_devices: NHP active device count.
        nhp_avg_tops: Average TOPS per NHP device.
        nhp_uptime: NHP uptime fraction.
        competitor: Competitor profile.

    Returns:
        Dict with power comparison and advantages.
    """
    nhp_active: int = int(nhp_devices * nhp_uptime)
    nhp_total_tops: float = nhp_active * nhp_avg_tops
    comp_total_tops: float = competitor.device_base_estimate * competitor.avg_tops_per_node

    power_ratio: float = nhp_total_tops / comp_total_tops if comp_total_tops > 0 else float('inf')
    device_ratio: float = nhp_active / competitor.device_base_estimate if competitor.device_base_estimate > 0 else float('inf')

    advantages: List[str] = []
    if not competitor.mfg_partnership:
        advantages.append("Manufacturer partnership")
    if not competitor.tee_protection:
        advantages.append("TEE security")
    if competitor.network_locked:
        advantages.append("Blockchain neutral")
    if nhp_devices > competitor.device_base_estimate:
        advantages.append("Larger device base")

    return {
        "competitor": competitor.name,
        "nhp_active_devices": nhp_active,
        "comp_devices": competitor.device_base_estimate,
        "nhp_total_tops": nhp_total_tops,
        "comp_total_tops": comp_total_tops,
        "power_ratio": power_ratio,
        "device_ratio": device_ratio,
        "nhp_advantages": advantages,
        "comp_device_type": competitor.device_type,
    }


# ═══════════════════════════════════════════════════════════════════════════
# L. BREAKEVEN ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════

def compute_breakeven(
    mfg: Manufacturer,
    cloud: CloudProvider,
    development_cost: float = 50_000_000.0,
    monthly_ops_cost: float = 2_000_000.0,
    coverage: float = 0.40,
) -> Dict[str, Any]:
    """Calculate when NHP becomes profitable for a manufacturer.

    Args:
        mfg: Manufacturer profile.
        cloud: Cloud provider being replaced.
        development_cost: One-time NHP integration cost.
        monthly_ops_cost: Monthly NHP operational cost.
        coverage: Fraction of requests NHP covers.

    Returns:
        Dict with breakeven timeline and ROI.
    """
    cost_result = compute_cost_comparison(mfg, cloud, coverage)
    monthly_savings: float = cost_result["monthly_savings"]
    net_monthly_benefit: float = monthly_savings - monthly_ops_cost

    if net_monthly_benefit > 0:
        breakeven_months: float = development_cost / net_monthly_benefit
    else:
        breakeven_months = float('inf')

    five_year_savings: float = (monthly_savings * 60) - development_cost - (monthly_ops_cost * 60)
    roi_5yr_pct: float = (five_year_savings / development_cost * 100) if development_cost > 0 else 0

    return {
        "manufacturer": mfg.name,
        "cloud_provider": cloud.short,
        "development_cost": development_cost,
        "monthly_ops_cost": monthly_ops_cost,
        "monthly_savings": monthly_savings,
        "net_monthly_benefit": net_monthly_benefit,
        "breakeven_months": breakeven_months,
        "five_year_net": five_year_savings,
        "roi_5yr_pct": roi_5yr_pct,
    }


# ═══════════════════════════════════════════════════════════════════════════
# M. RISK ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════

def compute_risk(
    risk_name: str,
    risk_name_ar: str,
    base_value: float,
    impact_pct: float,
    probability: float,
    category: str,
) -> Dict[str, Any]:
    """Quantify a risk factor.

    Args:
        risk_name: English name of the risk.
        risk_name_ar: Arabic name of the risk.
        base_value: The metric being risked (e.g., annual savings).
        impact_pct: How much the risk reduces the value (0-1).
        probability: Likelihood of the risk materializing (0-1).
        category: Risk category (technical, business, regulatory, etc.)

    Returns:
        Dict with expected loss and severity.
    """
    potential_loss: float = base_value * impact_pct
    expected_loss: float = potential_loss * probability

    severity: str = "🔴 Critical" if expected_loss > base_value * 0.3 else \
                    "🟠 High" if expected_loss > base_value * 0.15 else \
                    "🟡 Medium" if expected_loss > base_value * 0.05 else "🟢 Low"

    return {
        "risk_name": risk_name,
        "risk_name_ar": risk_name_ar,
        "category": category,
        "base_value": base_value,
        "impact_pct": impact_pct * 100,
        "probability_pct": probability * 100,
        "potential_loss": potential_loss,
        "expected_loss": expected_loss,
        "severity": severity,
    }
