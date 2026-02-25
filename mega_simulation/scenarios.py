"""
NHP Mega Simulation — Scenario Orchestrator
Generates all 580+ scenarios by iterating over parameter matrices.
Each function returns a list of result dicts for its category.
"""
from typing import Dict, Any, List
from mega_simulation.data import (
    MANUFACTURERS, CLOUD_PROVIDERS, REGIONS, TASK_TYPES, COMPETITORS,
    VARIANT_NAMES, UPTIME_VARIANTS, COVERAGE_VARIANTS,
    TOKEN_PRICE_VARIANTS, DC_REPLACED_VARIANTS, OVERHEAD_VARIANTS,
    GROWTH_VARIANTS, SIMULATION_YEARS,
)
from mega_simulation.engine import (
    compute_fleet_power, compute_cost_comparison, compute_user_income,
    compute_environmental, compute_combined_network, compute_task_feasibility,
    compute_battery_impact, compute_market_size, compute_token_economics,
    compute_competitive, compute_breakeven, compute_risk,
)
from itertools import combinations


def run_category_a() -> List[Dict[str, Any]]:
    """A: Computing Power per Manufacturer (28 scenarios)."""
    results: List[Dict[str, Any]] = []
    for mfg in MANUFACTURERS.values():
        for i, uptime in enumerate(UPTIME_VARIANTS):
            r = compute_fleet_power(mfg, uptime)
            r["variant"] = VARIANT_NAMES[i]
            r["category"] = "A"
            results.append(r)
    return results


def run_category_b() -> List[Dict[str, Any]]:
    """B: NHP vs Cloud Providers cost (140 scenarios)."""
    results: List[Dict[str, Any]] = []
    for mfg in MANUFACTURERS.values():
        for cloud in CLOUD_PROVIDERS.values():
            for i, cov in enumerate(COVERAGE_VARIANTS):
                r = compute_cost_comparison(mfg, cloud, cov)
                r["variant"] = VARIANT_NAMES[i]
                r["category"] = "B"
                results.append(r)
    return results


def run_category_c() -> List[Dict[str, Any]]:
    """C: User Income by Region (40 scenarios)."""
    results: List[Dict[str, Any]] = []
    for region in REGIONS.values():
        for i, tp in enumerate(TOKEN_PRICE_VARIANTS):
            r = compute_user_income(region, tp)
            r["variant"] = VARIANT_NAMES[i]
            r["category"] = "C"
            results.append(r)
    return results


def run_category_d() -> List[Dict[str, Any]]:
    """D: Manufacturer-Specific Savings — top cloud only (28 scenarios)."""
    results: List[Dict[str, Any]] = []
    aws = CLOUD_PROVIDERS["aws_a100"]
    for mfg in MANUFACTURERS.values():
        for i, cov in enumerate(COVERAGE_VARIANTS):
            r = compute_cost_comparison(mfg, aws, cov)
            r["variant"] = VARIANT_NAMES[i]
            r["category"] = "D"
            results.append(r)
    return results


def run_category_e() -> List[Dict[str, Any]]:
    """E: Environmental Impact per Manufacturer (28 scenarios)."""
    results: List[Dict[str, Any]] = []
    for mfg in MANUFACTURERS.values():
        for i, (uptime, dc) in enumerate(zip(UPTIME_VARIANTS, DC_REPLACED_VARIANTS)):
            r = compute_environmental(mfg, uptime, dc)
            r["variant"] = VARIANT_NAMES[i]
            r["category"] = "E"
            results.append(r)
    return results


def run_category_f() -> List[Dict[str, Any]]:
    """F: Network Effects — combined manufacturer fleets (20 scenarios)."""
    results: List[Dict[str, Any]] = []
    mfg_list = list(MANUFACTURERS.values())

    # Key alliances: each single, top-2, top-3, all
    combos = [
        [mfg_list[0], mfg_list[1]],       # Samsung + Apple
        [mfg_list[0], mfg_list[2]],       # Samsung + Xiaomi
        [mfg_list[0], mfg_list[1], mfg_list[2]],  # Samsung + Apple + Xiaomi
        mfg_list[:5],                      # Top 5
        mfg_list,                          # All 7
    ]

    for combo in combos:
        for i, uptime in enumerate(UPTIME_VARIANTS):
            r = compute_combined_network(combo, uptime)
            r["variant"] = VARIANT_NAMES[i]
            r["category"] = "F"
            results.append(r)
    return results


def run_category_g() -> List[Dict[str, Any]]:
    """G: Task Type Feasibility (24 scenarios)."""
    results: List[Dict[str, Any]] = []
    # Use Samsung moderate fleet as reference
    sam = MANUFACTURERS["samsung"]
    ref_power = compute_fleet_power(sam, 0.25)
    fleet_tops = ref_power["total_tops"]
    active = ref_power["active_devices"]
    avg_tops = fleet_tops / active if active > 0 else 0

    for task in TASK_TYPES.values():
        for i, overhead in enumerate(OVERHEAD_VARIANTS):
            r = compute_task_feasibility(task, fleet_tops, active, avg_tops, overhead)
            r["variant"] = VARIANT_NAMES[i]
            r["category"] = "G"
            results.append(r)
    return results


def run_category_h() -> List[Dict[str, Any]]:
    """H: Battery & Device Impact (12 scenarios)."""
    results: List[Dict[str, Any]] = []
    tiers = [
        ("Flagship (heavy use)", 7.0),
        ("Mid-range (moderate use)", 7.0),
        ("Budget (light use)", 5.0),
    ]
    for tier_name, hours in tiers:
        for i, variant in enumerate(VARIANT_NAMES):
            # Scale hours by variant aggressiveness
            scaled_hours = hours * [1.0, 0.8, 0.5, 0.3][i]
            r = compute_battery_impact(tier_name, scaled_hours)
            r["variant"] = variant
            r["category"] = "H"
            results.append(r)
    return results


def run_category_i() -> List[Dict[str, Any]]:
    """I: Market Size TAM/SAM/SOM (40 scenarios)."""
    results: List[Dict[str, Any]] = []
    penetration_rates = [0.10, 0.05, 0.02, 0.005]  # Per variant
    for region in REGIONS.values():
        for i, pen in enumerate(penetration_rates):
            r = compute_market_size(region, pen)
            r["variant"] = VARIANT_NAMES[i]
            r["category"] = "I"
            results.append(r)
    return results


def run_category_j() -> List[Dict[str, Any]]:
    """J: Token Economics (20 scenarios)."""
    results: List[Dict[str, Any]] = []
    scales = [1_000_000, 10_000_000, 100_000_000, 500_000_000, 1_000_000_000]
    for total_devices in scales:
        for i, (uptime, tp) in enumerate(zip(UPTIME_VARIANTS, TOKEN_PRICE_VARIANTS)):
            r = compute_token_economics(total_devices, uptime, tp)
            r["variant"] = VARIANT_NAMES[i]
            r["category"] = "J"
            r["scale_label"] = f"{total_devices:,} devices"
            results.append(r)
    return results


def run_category_k() -> List[Dict[str, Any]]:
    """K: Competitive Positioning (16 scenarios)."""
    results: List[Dict[str, Any]] = []
    for comp in COMPETITORS.values():
        for i, uptime in enumerate(UPTIME_VARIANTS):
            nhp_devices = 300_000_000  # Samsung fleet as reference
            r = compute_competitive(nhp_devices, 20.0, uptime, comp)
            r["variant"] = VARIANT_NAMES[i]
            r["category"] = "K"
            results.append(r)
    return results


def run_category_l() -> List[Dict[str, Any]]:
    """L: Breakeven Analysis (28 scenarios)."""
    results: List[Dict[str, Any]] = []
    aws = CLOUD_PROVIDERS["aws_a100"]
    dev_costs = [50_000_000, 30_000_000, 20_000_000, 10_000_000]
    for mfg in MANUFACTURERS.values():
        for i, (cov, dev_cost) in enumerate(zip(COVERAGE_VARIANTS, dev_costs)):
            r = compute_breakeven(mfg, aws, dev_cost, 2_000_000, cov)
            r["variant"] = VARIANT_NAMES[i]
            r["category"] = "L"
            results.append(r)
    return results


def run_category_m() -> List[Dict[str, Any]]:
    """M: Risk Analysis (40 scenarios)."""
    base_annual_savings: float = 64_000_000  # Moderate Samsung savings

    risks = [
        ("Manufacturer rejects partnership", "رفض المصنّع الشراكة", 0.80, 0.30, "Business"),
        ("Low user adoption", "تبني ضعيف من المستخدمين", 0.50, 0.35, "Business"),
        ("Regulatory ban on device compute", "حظر تنظيمي للحوسبة على الأجهزة", 0.90, 0.10, "Regulatory"),
        ("TEE vulnerability discovered", "اكتشاف ثغرة في TEE", 0.70, 0.05, "Technical"),
        ("Network latency too high", "تأخر الشبكة عالٍ جداً", 0.40, 0.40, "Technical"),
        ("Cloud prices drop 80%", "انخفاض أسعار السحابة 80%", 0.60, 0.20, "Market"),
        ("Competitor launches first", "منافس يطلق أولاً", 0.30, 0.45, "Market"),
        ("Battery degradation backlash", "ردة فعل سلبية بسبب البطارية", 0.35, 0.25, "Technical"),
        ("Token price collapse", "انهيار سعر التوكن", 0.55, 0.30, "Financial"),
        ("Data privacy lawsuit", "دعوى قضائية بخصوص الخصوصية", 0.75, 0.15, "Legal"),
    ]

    results: List[Dict[str, Any]] = []
    severities = [1.0, 0.7, 0.4, 0.2]

    for risk_name, risk_ar, impact, prob, category in risks:
        for i, sev in enumerate(severities):
            r = compute_risk(
                risk_name, risk_ar,
                base_annual_savings,
                impact * sev,
                prob * sev,
                category,
            )
            r["variant"] = VARIANT_NAMES[i]
            r["category"] = "M"
            results.append(r)
    return results


# ═══════════════════════════════════════════════════════════════════════════
# MASTER RUNNER
# ═══════════════════════════════════════════════════════════════════════════

def run_all_categories() -> Dict[str, List[Dict[str, Any]]]:
    """Run all 13 scenario categories and return results.

    Returns:
        Dict mapping category letter to list of result dicts.
    """
    return {
        "A": run_category_a(),
        "B": run_category_b(),
        "C": run_category_c(),
        "D": run_category_d(),
        "E": run_category_e(),
        "F": run_category_f(),
        "G": run_category_g(),
        "H": run_category_h(),
        "I": run_category_i(),
        "J": run_category_j(),
        "K": run_category_k(),
        "L": run_category_l(),
        "M": run_category_m(),
    }
